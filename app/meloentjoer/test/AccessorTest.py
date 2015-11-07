import unittest

from app.meloentjoer.accessors import bus_route_accessor, bus_estimation_accessor
from app.meloentjoer.accessors.entity.BusRoute import BusRoute


class AccessorTest(unittest.TestCase):
    def test_bus_routes_accessor(self):
        bus_route = BusRoute()
        bus_route.stations = ['Station1', 'Station 2']
        bus_route.corridor_name = 'Test'

        bus_route_accessor.reset()
        bus_route_accessor.upset_bus_route(bus_route)

        post_bus_route = bus_route_accessor.get_bus_route_by_corridor('Test')

        assert (post_bus_route.stations[1] == bus_route.stations[1])
        assert (post_bus_route.stations[0] == bus_route.stations[0])

    def test_bus_estimate_accessor(self):
        bus_estimation_accessor.reset()
        bus_estimation_accessor.start()
        bus_estimation_accessor.add_sample('jalan1', 'jalan2', 90)
        real_value = bus_estimation_accessor.predict_eta('jalan1', 'jalan2')
        self.assertEqual(real_value, 90)
        bus_estimation_accessor.add_sample('jalan1', 'jalan2', 10)
        real_value = bus_estimation_accessor.predict_eta('jalan1', 'jalan2')
        self.assertEqual(real_value, 50)
        bus_estimation_accessor.stop()

    def runTest(self):
        self.test_bus_estimate_accessor()
        self.test_bus_routes_accessor()