from app.meloentjoer.tracker import BuswayDataExtractionService


class MockBusWayExtractor(object):
    def __init__(self):
        pass

    def get_next_buses(self):
        mock_list = [('Busway', 60, 'RS. Harapan Bunda')]
        return mock_list
