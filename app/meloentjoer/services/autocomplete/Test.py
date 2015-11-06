import unittest
import time

from app.meloentjoer.accessors.bus_routes.BusRoutePostgresAccessorImpl import BusRoutePostgresAccessorImpl
from app.meloentjoer.fetcher.geo.TransportationFetcher import TransportationFetcher
from app.meloentjoer.services.autocomplete.AutocompleteServiceImpl import AutocompleteServiceImpl
from app.meloentjoer.test.TestDefault import *


class ServiceTest(unittest.TestCase):
    def testAutocomplete(self):
        accessor = BusRoutePostgresAccessorImpl(config.get_database_url())
        fetcher = TransportationFetcher(executor,
                                        accessor,
                                        config)
        fetcher.start()
        service = AutocompleteServiceImpl(executor,
                                          accessor,
                                          config)
        service.start()
        time.sleep(10)
        routes_list = accessor.get_all_bus_routes()
        bus_route = routes_list[0]
        station = bus_route.stations[0]
        bag_of_words = service.get_words(station[0:3])
        self.assertTrue(len(bag_of_words) > 0)
        fetcher.stop()
        service.stop()
        executor.shutdown()
