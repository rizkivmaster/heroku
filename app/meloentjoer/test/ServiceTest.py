import unittest
import time

from app.meloentjoer.accessors import bus_route_accessor
from app.meloentjoer.fetcher import transportation_info_fetcher
from app.meloentjoer.services import autocomplete_service
from app.meloentjoer.test import test_component


class ServiceTest(unittest.TestCase):
    def test_autocomplete(self):
        test_component.start()
        routes_list = test_component.bus_route_accessor.get_all_bus_routes()
        bus_route = routes_list[0]
        station = bus_route.stations[0]
        bag_of_words = test_component.autocomplete_service.get_words(station[0:3])
        self.assertTrue(len(bag_of_words) > 0)

    def test_search(self):
        test_component.start()
        time.sleep(10)
        search_result_list = test_component.search_service.get_direction('Slipi Kemanggisan', 'Cawang Sutoyo')
        self.assertTrue(len(search_result_list) > 0)

    def runTest(self):
        self.test_autocomplete()
        self.test_search()
