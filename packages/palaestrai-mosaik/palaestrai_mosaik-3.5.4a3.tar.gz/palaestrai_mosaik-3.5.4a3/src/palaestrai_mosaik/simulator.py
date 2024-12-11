"""This module contains the :class:`.ARLSyncSimulator`, which is used
by the :class:`.MosaikEnvironment` for synchronization.

"""

import json
import logging
import queue
from datetime import datetime, timedelta

import mosaik_api_v3
from midas.util.dict_util import convert
from mosaik.exceptions import SimulationError

from .config import SIMULATOR_LOGGER_NAME

LOG = logging.getLogger(SIMULATOR_LOGGER_NAME)

META = {
    "type": "time-based",
    "models": {
        "ARLSensor": {"public": True, "params": ["uid"], "attrs": ["reading"]},
        "ARLActuator": {
            "public": True,
            "params": ["uid"],
            "attrs": ["setpoint"],
        },
    },
}


class ARLSyncSimulator(mosaik_api_v3.Simulator):
    """A simulator for the synchronization of palaestrAI and mosaik.

    Attributes
    ----------
    sid : str
        The simulator id for this simulator given by mosaik
    step_size : int
        The step_size of this simulator
    models : dict
        A dictionary containing all models of this simulator.
        Currently, there is no reason why there should be more than one
        agent model.

    """

    def __init__(self, sensor_queue, actuator_queue, terminate, finished, end):
        super().__init__(META)

        self.sensor_queue = sensor_queue
        self.actuator_queue = actuator_queue
        self.sync_terminate = terminate
        self.sync_finished = finished

        self._end = end
        self.sid = None
        self.step_size = None
        self.models = {}
        self.a_uid_dict = {}
        self.s_uid_dict = {}
        self.model_ctr = {"ARLSensor": 0, "ARLActuator": 0}
        self._env = None
        self._sim_time = 0
        self._now_dt = None
        self._timeout = 15
        self._aq_timeout = 3
        self._sq_timeout = 5
        self._external_shutdown = False
        self._current_sensors = {}
        self._notified_done = False

    def init(self, sid, **sim_params):
        """Initialize this simulator.

        Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator id provided by mosaik.

        Returns
        -------
        dict
            The meta description for this simulator as *dict*.

        """
        self.sid = sid
        self.step_size = sim_params["step_size"]
        if "start_date" in sim_params and sim_params["start_date"] is not None:
            try:
                self._now_dt = datetime.strptime(
                    sim_params["start_date"], "%Y-%m-%d %H:%M:%S%z"
                )
            except Exception:
                LOG.exception(
                    "Unable to parse start date: %s. Time information will "
                    "not be available!",
                    str(sim_params["start_date"]),
                )
                self._now_dt = None
        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity)

        Parameters
        ----------
        num : int
            The number of models to create in one go.
        model : str
            The model to create. Needs to be present in the META.

        Returns
        -------
        list
            A *list* of the entities created during this call.

        """
        if num != 1:
            raise ValueError(
                "Only one model per sensor/actuator allowed but %d"
                " (%s) were requested",
                num,
                str(type(num)),
            )

        uid = model_params["uid"]
        if model == "ARLSensor":
            if uid in self.s_uid_dict:
                raise ValueError(
                    "A Sensor model with uid '%s' was already created "
                    "but only one model per uid is allowed.",
                    uid,
                )
        elif model == "ARLActuator":
            if uid in self.a_uid_dict:
                raise ValueError(
                    "An Actuator model with uid '%s' was already created "
                    "but only one model per uid is allowed.",
                    uid,
                )
        else:
            raise ValueError(
                "Invalid model: '%s'. Use ARLSensor or ARLActuator.", model
            )
        num_models = self.model_ctr[model]
        self.model_ctr[model] += 1

        eid = f"{model}-{num_models}"
        self.models[eid] = {"uid": uid, "value": None}

        if model == "ARLSensor":
            self.s_uid_dict[uid] = eid
        elif model == "ARLActuator":
            self.a_uid_dict[uid] = eid

        return [{"eid": eid, "type": model}]

    def step(self, time, inputs, max_advance=0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation time (the current step).
        inputs : dict
            A *dict* with inputs for the models.

        Returns
        -------
        int
            The simulation time at which this simulator should
            perform its next step.

        """
        self._sim_time = time
        # LOG.info("Stepping at time %d", time)
        self._current_sensors = {"simtime_ticks": self._sim_time}
        if self._now_dt is not None:
            self._now_dt += timedelta(seconds=self.step_size)
            self._current_sensors["simtime_timestamp"] = self._now_dt.strftime(
                "%Y-%m-%d %H:%M:%S%z"
            )

        if self.sync_terminate.is_set():
            raise SimulationError(
                "Stop was requested. Terminating simulation."
            )

        for sensor_eid, readings in inputs.items():
            log_msg = {
                "id": f"{self.sid}.{sensor_eid}",
                "name": sensor_eid,
                "type": sensor_eid.split("-")[0],
                "uid": self.models[sensor_eid]["uid"],
                "sim_time": self._sim_time,
                "msg_type": "input",
            }
            readings = readings["reading"]
            for src_eid, value in readings.items():
                if isinstance(value, bool):
                    value = 1 if value else 0
                self._current_sensors[self.models[sensor_eid]["uid"]] = value
                log_msg["reading"] = value
            LOG.debug(json.dumps(log_msg))

        if self._sim_time + self.step_size >= self._end:
            LOG.info("Repent, the end is nigh. Final readings are coming.")
            self._notified_done = True

        success = False
        while not success:
            try:
                self.sensor_queue.put(
                    (self._notified_done, self._current_sensors),
                    block=True,
                    timeout=self._sq_timeout,
                )
                success = True
            except queue.Full:
                LOG.exception("Failed to fill queue!")

        return time + self.step_size

    def get_data(self, outputs):
        """Return requested outputs (if feasible).

        Since this simulator does not generate output for its own, an
        empty dict is returned.

        Parameters
        ----------
        outputs : dict
            Requested outputs.

        Returns
        -------
        dict
            An empty dictionary, since no output is generated.

        """
        if self.sync_terminate.is_set():
            raise SimulationError(
                "Stop was requested. Terminating simulation."
            )

        data = {}
        success = False
        to_ctr = self._timeout
        if not self._notified_done:
            while not success:
                try:
                    actuator_data = self.actuator_queue.get(
                        block=True, timeout=3
                    )
                    success = True
                except queue.Empty:
                    to_ctr -= 1
                    if to_ctr <= 0:
                        raise SimulationError(
                            "No actuators after %.1f seconds. Stopping mosaik"
                            % (self._timeout * 3)
                        )
                    elif to_ctr < self._timeout / 2:
                        LOG.warning(
                            f"At step {self._sim_time}: Failed to get actuator "
                            "data from queue (queue is empty). Timeout in "
                            f"{to_ctr * 3}"
                        )

            for uid, value in actuator_data.items():
                self.models[self.a_uid_dict[uid]]["value"] = value
        else:
            for eid in self.models:
                self.models[uid]["value"] = None

        for eid, attrs in outputs.items():
            log_msg = {
                "id": f"{self.sid}.{eid}",
                "name": eid,
                "type": eid.split("-")[0],
                "uid": self.models[eid]["uid"],
                "sim_time": self._sim_time,
                "msg_type": "output",
            }

            try:
                value = convert({"val": self.models[eid]["value"]})["val"]
            except Exception:
                LOG.exception(
                    "Error converting %s to basic type",
                    str(self.models[eid]["value"]),
                )
                value = None

            data[eid] = {"setpoint": value}
            log_msg["setpoint"] = value

            try:
                LOG.debug(json.dumps(log_msg))
            except Exception:
                LOG.exception("Error constructing log message")

        return data

    def finalize(self) -> None:
        if not self._notified_done:
            try:
                self.sensor_queue.put(
                    (True, self._current_sensors),
                    block=True,
                    timeout=self._sq_timeout,
                )
            except queue.Full:
                LOG.error(
                    "Sensor queue is full! Following data could not be saved: "
                    f"{self._current_sensors}"
                )
        self.sync_finished.set()
