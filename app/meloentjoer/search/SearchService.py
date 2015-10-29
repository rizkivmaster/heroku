from app.meloentjoer.controllers.NextBus import NextBus
from app.meloentjoer.search.SearchResult import SearchResult
from app.meloentjoer.tracker.BuswayDataExtractionService import BuswayDataExtractionService


class SearchService(object):

    def __init__(self, transportation_networks, busway_extractor):
        """
        :type transportation_networks: GraphSearchService
        :type busway_extractor: BuswayDataExtractionService
        :param transportation_networks:
        :param busway_extractor:
        :return:
        """
        self.transportation_networks = transportation_networks
        self.busway_extractor = busway_extractor

    def get_direction(self, source, destination):
        """
        :type source: str
        :type destination: str
        :param source: the starting station of the bus
        :param destination: the next station on arriving
        :return:
        """
        return_response = list()
        cost, previous, transport = self.transportation_networks.find_shortest_path(source)
        transport_to_destination = transport[destination]
        for transport in transport_to_destination:
            search_result = SearchResult()
            search_result.branch = None
            search_result.source = source
            search_result.destination = destination
            search_result.mode_list = transport[1]
            search_result.mode_list_count = len(transport[1])
            search_result.time = transport[0]
            search_result.price = 0
            return_response.append(search_result)
        return return_response

    def get_next_bus(self, source, destination, next_stop):
        """
        :type next_stop: str
        :param next_stop:
        :return: list[BusStopResult]
        """
        responses = self.busway_extractor.get_next_buses(source, destination, next_stop)
        if len(responses) > 0:
            response = responses[0]
            bus_stop_result = NextBus()
            bus_stop_result.eta = response[1]
            bus_stop_result.current_stop = response[2]
            return bus_stop_result
        return None
