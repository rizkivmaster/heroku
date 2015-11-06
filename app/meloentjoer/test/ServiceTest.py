import unittest
import time

from app.meloentjoer.accessors import bus_route_accessor
from app.meloentjoer.fetcher import transportation_info_fetcher
from app.meloentjoer.services import autocomplete_service


class ServiceTest(unittest.TestCase):
    def test_autocomplete(self):
        transportation_info_fetcher.start()
        autocomplete_service.start()
        time.sleep(10)
        routes_list = bus_route_accessor.get_all_bus_routes()
        bus_route = routes_list[0]
        station = bus_route.stations[0]
        bag_of_words = autocomplete_service.get_words(station[0:3])
        self.assertTrue(len(bag_of_words) > 0)
        transportation_info_fetcher.stop()
        autocomplete_service.stop()

    def runTest(self):
        self.test_autocomplete()
