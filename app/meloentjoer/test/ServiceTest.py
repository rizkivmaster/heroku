import unittest

from app.meloentjoer import main_component


class ServiceTest(unittest.TestCase):
    def test_autocomplete(self):
        main_component.start()
        bag_of_words = main_component.autocomplete_service.get_words('Stasiun Universitas Indonesia')
        self.assertTrue(len(bag_of_words) > 0)
        main_component.stop()

    def test_search(self):
        main_component.start()
        search_result_list = main_component.search_service.get_direction('Halte Slipi Kemanggisan',
                                                                         'Stasiun Universitas Indonesia')
        self.assertTrue(len(search_result_list) > 0)
        main_component.stop()

    def runTest(self):
        self.test_autocomplete()
        self.test_search()
