__author__ = 'traveloka'

from app.meloentjoer.search.RealtimeBuswayGenerator import RealtimeBuswayGenerator
from app.meloentjoer.search.TransportationGraphBuilder import TransportationGraphBuilder
import unittest


class SearchTest(unittest.TestCase):
    def test_data_gathering(self):
        transportation_mode = RealtimeBuswayGenerator()
        mode_list = transportation_mode.generate_modes()
        self.assertTrue(len(mode_list) > 0)

    def test_search(self):
        transportation_graph = TransportationGraphBuilder().generate_realtime_graph()
        cost, previous, transport = transportation_graph.find_shortest_path('Slipi Kemanggisan')
        self.assertIsNotNone(cost)
        self.assertIsNotNone(previous)
        self.assertIsNotNone(transport)


if __name__ == '__main__':
    unittest.main()
