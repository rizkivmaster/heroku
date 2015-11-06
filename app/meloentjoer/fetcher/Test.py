import unittest
import time

from app.meloentjoer.accessors.bus_routes.BusRoutePostgresAccessorImpl import BusRoutePostgresAccessorImpl
from app.meloentjoer.test.TestDefault import *
import transportation_fetcher


class Tester(unittest.TestCase):
    def test_Fetcher(self):
        accessor = BusRoutePostgresAccessorImpl(config)
        accessor.reset()
        transportation_fetcher.start()
        time.sleep(11)
        routes = accessor.get_all_bus_routes()
        self.assertIsNotNone(routes)
        self.assertTrue(len(routes) > 0)
