import unittest

from app.meloentjoer.accessors import bus_estimation_accessor
from app.meloentjoer.accessors.entity.TrainRoute import TrainRoute
from app.meloentjoer.accessors.entity.WalkRoute import WalkRoute
from app.meloentjoer.accessors.routes import bus_route_accessor, walk_route_accessor, train_route_accessor
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

    def test_train_routes_accessor(self):
        train_route_accessor.reset()
        train_route = TrainRoute()
        train_route.line_name = 'Den-en-Toshi'
        train_route.stations = ['Shibuya', 'Aobadai', 'Eda']

        train_route_accessor.upset_train_route(train_route)
        post_train_route = train_route_accessor.get_train_route_by_line('Den-en-Toshi')
        self.assertEqual(post_train_route.line_name, train_route.line_name)
        self.assertSequenceEqual(post_train_route.stations, train_route.stations)

    def test_walk_routes_accessor(self):
        walk_route_accessor.reset()
        walk_route = WalkRoute()
        walk_route.walk_to = 'Test 1'
        walk_route.walk_from = 'Test 2'
        walk_route_accessor.upset_walk_route(walk_route)

        post_walk_route = walk_route_accessor.get_walk_route('Test 2', 'Test 1')

        self.assertEqual(post_walk_route.walk_to, walk_route.walk_to)
        self.assertEqual(post_walk_route.walk_from, walk_route.walk_from)

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
