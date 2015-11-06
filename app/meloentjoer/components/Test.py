import unittest
from app.meloentjoer.components.MainComponent import MainComponent


class Test(unittest.TestCase):
    def test_Component(self):
        autocomplete_service = MainComponent()
        autocomplete_service.