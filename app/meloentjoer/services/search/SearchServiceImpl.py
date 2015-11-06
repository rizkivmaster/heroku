from app.meloentjoer.accessors.bus_routes.BusRouteAccessor import BusRouteAccessor
from app.meloentjoer.accessors.eta_estimates.BusEstimationAccessor import BusEstimationAccessor
from app.meloentjoer.accessors.next_buses.NextBus import NextBus
from app.meloentjoer.accessors.next_buses.BusNextStopAccessor import BusNextStopAccessor
from app.meloentjoer.common.util.ConnectedGraph import ConnectedGraph
from app.meloentjoer.config.GeneralConfig import GeneralConfig
from app.meloentjoer.search.BuswayMode import BuswayMode
from app.meloentjoer.search.SearchResult import SearchResult
from app.meloentjoer.services.search.SearchService import SearchService


class SearchServiceImpl(SearchService):
    def __generate_busway_mode(self):
        """
        :rtype list[BuswayMode]
        :return:
        """
        mode_list = []
        bus_route_list = self.bus_route_accessor.get_all_bus_routes()
        assert isinstance(bus_route_list, dict)
        for corridor_name in bus_route_list.keys():
            station_list = bus_route_list[corridor_name]
            origin_list = station_list[:-1]
            destination_list = station_list[1:]
            for origin, destination in zip(origin_list, destination_list):
                eta = self.bus_estimation_accessor.predict_eta(origin, destination)
                eta = eta if eta else self.default_eta
                bus_mode = BuswayMode()
                bus_mode.name = 'Transjakarta'
                bus_mode.corridor = corridor_name
                bus_mode.eta = eta
                bus_mode.price = self.default_price
                bus_mode.origin = origin
                bus_mode.destination = destination
                mode_list.append(bus_mode)

            for destination, origin in zip(origin_list, destination_list):
                eta = self.bus_estimation_accessor.predict_eta(origin, destination)
                eta = eta if eta else self.default_eta
                bus_mode = BuswayMode()
                bus_mode.name = 'Transjakarta'
                bus_mode.corridor = corridor_name
                bus_mode.eta = eta
                bus_mode.price = self.default_price
                bus_mode.origin = origin
                bus_mode.destination = destination
                mode_list.append(bus_mode)
        return mode_list

    def __generate_graph(self, mode_list):
        vertices = set()
        edges = dict()
        for mode in mode_list:
            vertices.add(mode.origin)
            vertices.add(mode.destination)
            if mode.origin not in edges:
                edges[mode.origin] = []
            edges[mode.origin].append(mode)
        return_graph = ConnectedGraph(vertices, edges)
        return return_graph

    def __generate_transportation_graph(self):
        """
        :rtype ConnectedGraph
        """
        busway_mode_list = self.__generate_busway_mode()

        connected_graph = self.__generate_graph(busway_mode_list)
        return connected_graph

    def __init__(self,
                 bus_route_accessor,
                 bus_estimation_accessor,
                 next_bus_accessor,
                 config):
        """
        :type config: GeneralConfig
        :type bus_route_accessor: BusRouteAccessor
        :type bus_estimation_accessor: BusEstimationAccessor
        :type next_bus_accessor: BusNextStopAccessor
        :return:
        """
        self.next_bus_accessor = next_bus_accessor
        self.bus_estimation_accessor = bus_estimation_accessor
        self.bus_route_accessor = bus_route_accessor

        self.default_eta = config.get_default_eta()
        self.default_price = config.get_default_price()

    def get_direction(self, source, destination):
        direction_recommendation = []
        connected_graph = self.__generate_transportation_graph()
        assert isinstance(connected_graph, ConnectedGraph)
        cost, previous, transport = connected_graph.find_shortest_path(source)
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
            direction_recommendation.append(search_result)
        return direction_recommendation

    def get_next_bus(self, source, destination, next_stop):
        next_bus = self.next_bus_accessor.get_next_stop(source, destination, next_stop)
        assert (isinstance(next_bus, NextBus))
        return next_bus
