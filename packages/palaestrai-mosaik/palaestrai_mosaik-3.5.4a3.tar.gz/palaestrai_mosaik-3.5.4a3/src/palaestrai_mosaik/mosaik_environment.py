"""This module contains the :class:`MosaikEnvironment`, which
allows to run mosaik co-simulations with palaestrAI.

"""

from __future__ import annotations

import logging
import queue
import sys
import threading
from copy import copy
from datetime import datetime
from multiprocessing import Event, Process
from typing import Any, Dict, List, Optional, Union

from socket import socket
import mosaik_api_v3
import numpy as np
from loguru import logger
from numpy.random import RandomState
from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from palaestrai.types import SimTime, Space
from palaestrai.util import seeding

from . import loader
from .config import DATE_FORMAT, ENVIRONMENT_LOGGER_NAME
from .simulator import ARLSyncSimulator

LOG = logging.getLogger(ENVIRONMENT_LOGGER_NAME)


class MosaikEnvironment(Environment):
    """The Mosaik environment for palaestrAI.

    Parameters
    ==========
    no_extra_step: bool, optional
        By default, end will be incremented by one. Background is that
        mosaik starts counting by 0 and ends and end-1. Adding 1 will
        force to have the last step at end. Since from the palaestrAI
        perspective, the first step is 'lost', this makes up for it.
        Setting this to True will prevent this behavior

    """

    def __init__(
        self,
        uid: str,
        # worker_uid: str,
        broker_uri: str,
        seed: int,
        module: str,
        description_func: str,
        instance_func: str,
        arl_sync_freq: int,
        end: Union[int, str],
        start_date: Optional[str] = None,
        arl_sync_host: str = "localhost",
        arl_sync_port: int = 0,
        silent: bool = False,
        no_extra_step: bool = False,
        # reward: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(uid, broker_uri, seed)
        self.rng: RandomState = seeding.np_random(self.seed)[0]

        self.sensor_queue: queue.Queue
        self.actuator_queue: queue.Queue
        self.sim_terminate: Event
        self.sim_finished: Event
        self.sync_terminate: threading.Event
        self.sync_finished: threading.Event

        self._module = module
        self._description_func = description_func
        self._instance_func = instance_func

        self._arl_sync_host = arl_sync_host
        self._arl_sync_port = arl_sync_port if arl_sync_port != 0 else find_free_port()
        LOG.warning("%s attempting to use port %s.", log_(self), str(self._arl_sync_port))
        self._mosaik_params = {} if params is None else params
        self._mosaik_params["meta_params"] = {
            "seed": self.rng.randint(sys.maxsize),
            "end": parse_end(end) + (0 if no_extra_step else 1),
            "arl_sync_freq": arl_sync_freq,
            "silent": silent,
        }
        start_date = parse_start_date(start_date, self.rng)
        if start_date is not None:
            self._mosaik_params["meta_params"]["start_date"] = start_date
        self._prev_simtime = SimTime(simtime_ticks=0)

    def start_environment(self):
        self.sensor_queue = queue.Queue(1)
        self.actuator_queue = queue.Queue(1)
        self.sim_terminate = Event()
        self.sim_finished = Event()
        self.sync_terminate = threading.Event()
        self.sync_finished = threading.Event()
        simtime = SimTime(simtime_ticks=0)

        LOG.debug("%s loading sensors and actuators ...", log_(self))
        try:
            description, instance = loader.load_funcs(
                self._module, self._description_func, self._instance_func
            )
        except Exception:
            LOG.exception(
                "%s: Error during loading of loader functions. Module: '%s' "
                "description function: '%s', instance function: '%s'",
                log_(self),
                self._module,
                self._description_func,
                self._instance_func,
            )
            return EnvironmentBaseline(sensors_available=None, actuators_available=None)

        try:
            sensor_description, actuator_description, static_world_state = description(
                self._mosaik_params
            )
        except Exception:
            LOG.exception(
                "%s: Error during calling the description function. Params %s",
                log_(self),
                str(self._mosaik_params),
            )
            return EnvironmentBaseline(sensors_available=None, actuators_available=None)

        self.sensors, self.sen_map = create_sensors(sensor_description)
        self.actuators, self.act_map = create_actuators(actuator_description)
        if not self.sensors or not self.actuators:
            LOG.error(
                "%s: No sensors and/or actuators defined in the environment!! "
                "Sensors=%s, Actuators=%s",
                log_(self),
                str(self.sensors),
                str(self.actuators),
            )
            return EnvironmentBaseline(sensors_available=None, actuators_available=None)

        LOG.debug("%s starting ARLSyncSimulator ...", log_(self))
        self.sync_task = threading.Thread(
            target=_start_simulator,
            args=[
                self._arl_sync_host,
                self._arl_sync_port,
                self.sensor_queue,
                self.actuator_queue,
                self._mosaik_params["meta_params"]["end"],
                self.sync_terminate,
                self.sync_finished,
            ],
        )
        self.sync_task.start()

        LOG.debug(f"{log_(self)} starting Co-Simulation ...")
        self.sim_proc = Process(
            target=_start_world,
            args=(
                instance,
                self._mosaik_params,
                [s.uid for s in self.sensors],
                [a.uid for a in self.actuators],
                self._arl_sync_host,
                self._arl_sync_port,
                self.sim_finished,
            ),
        )
        self.sim_proc.start()

        LOG.info(
            "%s finished setup. Co-simulation is now running. Now waiting for "
            "initial sensor readings ...",
            {log_(self)},
        )
        done, data = self.sensor_queue.get(block=True, timeout=60)
        self.sensors = self._get_sensors_from_queue_data(data)

        return EnvironmentBaseline(
            sensors_available=self.sensors,
            actuators_available=self.actuators,
            simtime=simtime,
        )

    def update(self, actuators):
        try:
            env_state = self._update_mosaik(actuators)
        except Exception:
            LOG.exception("%s: Error during update of environment.", log_(self))
            env_state = EnvironmentState(
                sensor_information=None,
                rewards=None,
                done=True,
                simtime=self._prev_simtime,
            )
        return env_state

    def _update_mosaik(self, actuators):
        data = {}
        for actuator in actuators:
            data[actuator.uid] = actuator.value

        LOG.debug("%s sending actuators to simulation ...", log_(self))
        self.actuator_queue.put(data, block=True, timeout=5)
        LOG.debug("%s waiting for sensor readings ...", log_(self))
        done, data = self.sensor_queue.get(block=True, timeout=60)

        # sensors = []
        self._simtime_ticks = 0
        self._simtime_timestamp = None

        self.sensors = self._get_sensors_from_queue_data(data)
        rewards = self.reward(self.sensors, actuators)
        if not done:
            LOG.info("%s update complete.", log_(self))
        else:
            LOG.info("%s simulation finished! Terminating.", log_(self))
            # Calculate reward with previous sensor values
            # rewards = self.reward(self.sensors, actuators)

        # self.sensors = sensors

        self._prev_simtime = SimTime(
            simtime_ticks=self._simtime_ticks,
            simtime_timestamp=self._simtime_timestamp,
        )

        return EnvironmentState(
            sensor_information=self.sensors,
            rewards=rewards,
            done=done,
            simtime=self._prev_simtime,
        )

    def shutdown(self, reset=False):
        LOG.info(
            "%s starting shutdown of simulation and synchronization processes ...",
            log_(self),
        )
        self.sync_terminate.set()
        self.sync_finished.wait(3)
        if self.sync_finished.is_set():
            self.sync_task.join()
        else:
            self.sync_task.join(5)
            self.sync_task.kill()
        LOG.debug("%s: Synchronization task joined!", log_(self))

        self.sim_finished.wait(3)
        if self.sim_finished.is_set():
            self.sim_proc.join()
            LOG.debug("%s: Simulation process joined!", log_(self))
        else:
            self.sim_proc.join(5)
            self.sim_proc.kill()
            LOG.debug("%s: Simulation process killed ... better be sure!", log_(self))
        self.is_terminal = not reset

        LOG.info("%s: Sync and Sim terminated 'gracefully'", log_(self))
        return True

    def _get_sensors_from_queue_data(self, data):
        sensors = []
        for uid, value in data.items():
            # Special cases for ticks and timestamp
            if uid == "simtime_ticks":
                self._simtime_ticks = value
                continue
            if uid == "simtime_timestamp":
                if value is not None:
                    try:
                        self._simtime_timestamp = datetime.strptime(
                            data["simtime_timestamp"], DATE_FORMAT
                        )
                    except ValueError:
                        LOG.error(
                            "Unable to parse simtime_timestamp: "
                            f"{data['simtime_timestamp']}"
                        )
                continue

            new_sensor = copy(self.sen_map[uid])
            # new_sensor.value = value
            new_sensor.value = np.array(value, dtype=new_sensor.space.dtype)
            sensors.append(new_sensor)
        return sensors


def create_sensors(sensor_defs) -> List[SensorInformation]:
    """Create sensors from the sensor description.

    The description is provided during initialization.

    Returns
    -------
    list
        The *list* containing the created sensor objects.

    """
    sensors = []
    sensor_map = {}
    for sensor in sensor_defs:
        if isinstance(sensor, SensorInformation):
            sensors.append(sensor)
            uid = sensor.uid
        else:
            uid = str(sensor.get("uid", sensor.get("sensor_id", "Unnamed Sensor")))
            try:
                space = Space.from_string(
                    sensor.get("space", sensor.get("observation_space", None))
                )
                value = sensor.get("value", None)
                sensors.append(
                    SensorInformation(
                        uid=uid,
                        space=space,
                        value=value,
                    )
                )
            except RuntimeError:
                LOG.exception(sensor)
                raise
        sensor_map[uid] = copy(sensors[-1])

    return sensors, sensor_map


def create_actuators(actuator_defs) -> List[ActuatorInformation]:
    """Create actuators from the actuator description.

    The description is provided during initialization.

    Returns
    -------
    list
        The *list* containing the created actuator objects.

    """
    actuators = []
    actuator_map = {}
    for actuator in actuator_defs:
        if isinstance(actuator, ActuatorInformation):
            actuators.append(actuator)
            uid = actuator.uid
        else:
            uid = str(
                actuator.get("uid", actuator.get("actuator_id", "Unnamed Actuator"))
            )

            try:
                space = Space.from_string(
                    actuator.get("space", actuator.get("action_space", None))
                )
                value = actuator.get(
                    "value",
                    actuator.get("setpoint", None),
                )
                actuators.append(
                    ActuatorInformation(
                        value=value,
                        uid=uid,
                        space=space,
                    )
                )
            except RuntimeError:
                LOG.exception(actuator)
                raise
        actuator_map[uid] = copy(actuators[-1])
    return actuators, actuator_map


def _start_simulator(host, port, q1, q2, end, terminate, finished):
    argv_backup = sys.argv
    sys.argv = [
        argv_backup[0],
        "--remote",
        f"{host}:{port}",
        "--log-level",
        "error",
    ]

    mosaik_api_v3.start_simulation(ARLSyncSimulator(q1, q2, terminate, finished, end))
    sys.argv = argv_backup


def _start_world(get_world, params, sensors, actuators, host, port, finished):
    """Start the mosaik simulation process

    TODO: Error handling for the case that
    - get_world does not work
    - uid does not match the scheme
    - full_id is not present in entities
    - Mosaik connection errors

    """
    # logger.remove(0)
    # logger.add(sys.stderr, level="WARNING")

    meta_params = params["meta_params"]

    world, entities = get_world(params)
    world.sim_config["ARLSyncSimulator"] = {"connect": f"{host}:{port}"}
    arlsim = world.start(
        "ARLSyncSimulator",
        step_size=meta_params["arl_sync_freq"],
        start_date=meta_params.get("start_date", None),
    )

    for uid in sensors:
        sid, eid, attr = uid.split(".")
        full_id = f"{sid}.{eid}"
        sensor_model = arlsim.ARLSensor(uid=uid)
        world.connect(entities[full_id], sensor_model, (attr, "reading"))

    for uid in actuators:
        sid, eid, attr = uid.split(".")
        full_id = f"{sid}.{eid}"
        actuator_model = arlsim.ARLActuator(uid=uid)
        world.connect(
            actuator_model,
            entities[full_id],
            ("setpoint", attr),
            time_shifted=True,
            initial_data={"setpoint": None},
        )

    logger.disable("mosaik")
    # logger.disable("mosaik_api_v3")
    # logger.remove(0)
    # logger.add(sys.stderr, level="ERROR")

    try:
        world.run(until=meta_params["end"], print_progress=not meta_params["silent"])
    except Exception:
        LOG.exception("Error during the simulation:")

    finished.set()


def parse_start_date(start_date: str, rng: np.random.RandomState):
    if start_date is None:
        LOG.info("Start_date is None, time information will not be available")
        return None
    if start_date == "random":
        start_date = (
            f"2020-{rng.randint(1, 12):02d}-"
            f"{rng.randint(1, 28):02d} "
            f"{rng.randint(0, 23):02d}:00:00+0100"
        )
    try:
        datetime.strptime(start_date, DATE_FORMAT)
    except ValueError:
        LOG.exception(
            "Unable to parse start_date %s (format string: %s)",
            start_date,
            DATE_FORMAT,
        )
    return start_date


def parse_end(end: Union[str, int]) -> int:
    """Read the *end* value from the params dict.

    The *end* value is an integer, but sometimes it is provided
    as float, or as str like '15*60'. In the latter case, the
    str is evaluated (i.e., multiplied). In any case, *end* is
    returned as int.

    """
    if isinstance(end, str):
        smnds = end.split("+")
        end = 0
        for p in smnds:
            parts = p.split("*")
            prod = 1
            for part in parts:
                prod *= float(part)
            end += prod
    return int(end)


def log_(env):
    return f"MosaikEnvironment (id={id(env)}, uid={env.uid})"


def find_free_port():
    port = 0
    with socket() as s:
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
    return port
