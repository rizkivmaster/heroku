__author__ = 'traveloka'

import unittest

from app.meloentjoer.fetcher.geo.TransportationFetcher import TransportationFetcher


class TransportationFetcherTest(unittest.TestCase):

    def test_fetch_train(self):
        fetcher = TransportationFetcher()
        train_list = fetcher.get_train_routes()
        self.assertIsNotNone(train_list)



if __name__ == '__main__':
    unittest.main()