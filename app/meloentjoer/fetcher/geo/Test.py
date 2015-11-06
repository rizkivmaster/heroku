import unittest

from app.meloentjoer.accessors.bus_routes.BusRoutePostgresAccessorImpl import BusRoutePostgresAccessorImpl
from app.meloentjoer.fetcher.geo.TransportationFetcher import TransportationFetcher
from app.meloentjoer.test.TestDefault import *
import time


class Tester(unittest.TestCase):
    def test_Fetcher(self):
        accessor = BusRoutePostgresAccessorImpl(config)
        accessor.reset()
        fetcher = TransportationFetcher(executor, accessor, config)
        fetcher.start()
        time.sleep(11)
        routes = accessor.get_all_bus_routes()
        self.assertIsNotNone(routes)
        self.assertTrue(len(routes) > 0)
