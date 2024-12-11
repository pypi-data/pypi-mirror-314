import unittest
from unittest.mock import MagicMock

from palaestrai_mosaik.simulator import ARLSyncSimulator


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.sen_queue = MagicMock()
        self.sen_queue.put = MagicMock()
        self.act_queue = MagicMock()
        self.act_queue.get = MagicMock(side_effect=[{}])
        self.start_date = "2020-01-01 00:00:00+0100"
        self.test_eid1 = "ARLSensor-0"
        self.test_eid2 = "ARLSensor-1"
        self.test_eid3 = "ARLActuator-0"
        self.test_uid1 = "TestEnv.TestSim.TestMod.TestAttr1"
        self.test_uid2 = "TestEnv.TestSim.TestMod.TestAttr2"
        self.test_uid3 = "TestEnv.TestSim.TestMod.TestAttr3"

    def test_create(self):
        sim = ARLSyncSimulator(
            self.sen_queue, self.act_queue, MagicMock(), MagicMock(), 9000
        )

        sim.init("ARLSyncSimulator", step_size=900, start_date=self.start_date)

        entities = sim.create(1, "ARLSensor", uid=self.test_uid1)
        entities = sim.create(1, "ARLSensor", uid=self.test_uid2)

        self.assertEqual(self.test_eid2, entities[0]["eid"])
        self.assertIn(self.test_uid1, sim.s_uid_dict)
        self.assertIn(self.test_uid2, sim.s_uid_dict)

        with self.assertRaises(ValueError) as ctx:
            sim.create(1, "ARLSensor", uid=self.test_uid1)
        self.assertIn("A Sensor model with uid ", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            sim.create(2, "ARLSensor", uid=self.test_uid3)
        self.assertIn(
            "Only one model per sensor/actuator allowed", str(ctx.exception)
        )

        self.assertEqual(2, sim.model_ctr["ARLSensor"])

        sim.create(1, "ARLActuator", uid=self.test_uid1)
        self.assertIn(self.test_uid1, sim.a_uid_dict)

    def test_step(self):
        sync_terminate = MagicMock()
        sync_terminate.is_set = MagicMock(return_value=False)

        sim = ARLSyncSimulator(
            self.sen_queue, self.act_queue, sync_terminate, MagicMock(), 9000
        )
        sim.sid = "ARLSyncSimulator"
        sim.step_size = 900

        res = sim.step(0, {})

        self.assertEqual(900, res)

        with self.assertRaises(KeyError) as ctx:
            sim.step(
                900, {self.test_eid1: {"reading": {"DummySim.DummyMod": 1}}}
            )
        self.assertEqual(f"'{self.test_eid1}'", str(ctx.exception))

        sim.models[self.test_eid1] = {"uid": self.test_uid1, "value": None}
        res = sim.step(
            900, {self.test_eid1: {"reading": {"DummySim.DummyMod": 1}}}
        )

        self.assertEqual(1800, res)
        self.sen_queue.put.assert_called_with(
            (False, {"simtime_ticks": 900, self.test_uid1: 1}),
            block=True,
            timeout=5,
        )

    def test_get_data(self):
        sync_terminate = MagicMock()
        sync_terminate.is_set = MagicMock(return_value=False)

        sim = ARLSyncSimulator(
            self.sen_queue, self.act_queue, sync_terminate, MagicMock(), 9000
        )
        sim.sid = "ARLSyncSimulator"
        sim._sim_time = 0

        sim.get_data({})

        self.act_queue.get.assert_called_with(block=True, timeout=3)

        sim.models[self.test_eid3] = {"uid": self.test_uid1, "value": 1}
        sim.a_uid_dict[self.test_uid1] = self.test_eid3

        self.act_queue.get = MagicMock(side_effect=[{self.test_uid1: 2}])

        outputs = sim.get_data({self.test_eid3: ["setpoint"]})

        self.assertIn(self.test_eid3, outputs)
        self.assertIn("setpoint", outputs[self.test_eid3])
        self.assertEqual(2, outputs[self.test_eid3]["setpoint"])


if __name__ == "__main__":
    unittest.main()
