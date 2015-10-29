from app.meloentjoer.search.TransportationMode import TransportationMode
from SearchResult import SearchResult
from BusStopResult import BusStopResult


class MockSearchTransducer(object):
    def __init__(self):
        pass

    def get_direction(self, source, destination):
        """
        :type source: str
        :type destination: str
        :param source: the starting station of the bus
        :param destination: the next station on arriving
        :return:
        """
        return_response = list()
        for index in range(0, 2):
            search_result = SearchResult()
            search_result.branch = None
            search_result.source = source
            search_result.destination = destination
            mode_list = []
            for index2 in range(0, 5):
                transportation_mode = TransportationMode()
                transportation_mode.price = 10
                transportation_mode.name = 'TransJakarta'
                transportation_mode.eta = 60
                transportation_mode.destination = 'Slipi Petamburan'
                transportation_mode.origin = 'Slipi Kemanggisan'
                mode_list.append(transportation_mode)
            search_result.mode_list = mode_list
            search_result.mode_list_count = len(mode_list)
            search_result.time = 120
            search_result.price = 0
            return_response.append(search_result)
        return return_response

    def get_next_bus(self):
        """
        """
        return_list = []
        for index in range(0, 10):
            bus_stop_result = BusStopResult()
            bus_stop_result.eta = index
            bus_stop_result.source = 'Loren Ipsum ' + str(index)
            return_list.append(bus_stop_result)
        return return_list
