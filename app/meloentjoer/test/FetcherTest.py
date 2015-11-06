import unittest
import time
from app.meloentjoer.accessors import bus_route_accessor

import app.meloentjoer.fetcher.transportation_info_fetcher


class FetcherTest(unittest.TestCase):
    def test_transporation_fetcher(self):
        bus_route_accessor.reset()
        app.meloentjoer.fetcher.transportation_info_fetcher.start()
        time.sleep(11)
        routes = bus_route_accessor.get_all_bus_routes()
        self.assertIsNotNone(routes)
        self.assertTrue(len(routes) > 0)
        app.meloentjoer.fetcher.transportation_info_fetcher.stop()

    def runTest(self):
        self.test_transporation_fetcher()
