from app.meloentjoer.tracker.BuswayDataExtractionService import BuswayDataExtractionService

__author__ = 'traveloka'

import unittest
from app.meloentjoer.search.TransportationGraphBuilder import TransportationGraphBuilder
from app.meloentjoer.search.SearchService import SearchService


class SearchTransducerTest(unittest.TestCase):
    def test_find(self):
        transportation_graph = TransportationGraphBuilder().generate_realtime_graph()
        busway_extractor = BuswayDataExtractionService(None, None, None)
        search_transducer = SearchService(transportation_graph, busway_extractor)
        search_list = search_transducer.get_direction('Slipi Kemanggisan', 'Slipi Petamburan')
        next_bus = search_transducer.get_next_bus('Pluit', 'Pinang Ranti', 'Slipi Kemanggisan')
        self.assertIsNotNone(search_list)
        self.assertIsNotNone(next_bus)


if __name__ == '__main__':
    unittest.main()
