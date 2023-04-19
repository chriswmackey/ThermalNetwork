from unittest import TestCase

from thermalnetwork.heat_pump import HeatPump


class TestHeatPump(TestCase):
    def test_calc_src_side_load(self):
        data = {
            "name": "WSHP",
            "type": "HEATPUMP",
            "properties": {
                "cop_c": 3.5,
                "cop_h": 2.5
            }
        }

        hp = HeatPump(data)
        self.assertEquals(hp.name, "WSHP")
        self.assertAlmostEquals(hp.calc_src_side_load(1), 0.60, delta=0.01)
        self.assertAlmostEquals(hp.calc_src_side_load(-1), -1.28, delta=0.01)
