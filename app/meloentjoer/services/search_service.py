from app.meloentjoer.accessors import bus_estimation_accessor, next_bus_accessor
from app.meloentjoer.accessors.routes import bus_route_accessor, train_route_accessor, walk_route_accessor, \
    busway_transfer_accessor
from app.meloentjoer.accessors.entity.NextBus import NextBus
from app.meloentjoer.common.logging import logger_factory
from app.meloentjoer.common.util.ConnectedGraph import ConnectedGraph
from app.meloentjoer.config import general_config
from app.meloentjoer.services.entity.BuswayMode import BuswayMode
from app.meloentjoer.services.entity.SearchResult import SearchResult
from app.meloentjoer.services.entity.TransportationMode import TransportationMode
from copy import deepcopy

__logger = logger_factory.create_logger('search_service')
__logger.info('Starting Search Service')


def __generate_busway_mode():
    """
    :rtype list[BuswayMode]
    :return:
    """
    mode_list = []
    bus_route_list = bus_route_accessor.get_all_bus_routes()
    """:type :list[BusRoute]"""
    for bus_route in bus_route_list:
        station_list = bus_route.stations
        corridor_name = bus_route.corridor_name
        origin_list = station_list[:-1]
        destination_list = station_list[1:]
        for origin, destination in zip(origin_list, destination_list):
            eta = bus_estimation_accessor.predict_eta(origin, destination)
            eta = eta if eta else general_config.get_default_eta()
            bus_mode = BuswayMode()
            bus_mode.name = 'Transjakarta ' + corridor_name
            bus_mode.corridor = corridor_name
            bus_mode.eta = max(eta / 60, 1)
            bus_mode.price = general_config.get_default_price()
            bus_mode.origin = origin
            bus_mode.destination = destination
            bus_mode.heading_from = station_list[0]
            bus_mode.heading_to = station_list[-1]
            mode_list.append(bus_mode)

        for destination, origin in zip(origin_list, destination_list):
            eta = bus_estimation_accessor.predict_eta(origin, destination)
            eta = eta if eta else general_config.get_default_eta()
            bus_mode = BuswayMode()
            bus_mode.name = 'Transjakarta ' + corridor_name
            bus_mode.corridor = corridor_name
            bus_mode.eta = max(eta / 60, 1)
            bus_mode.price = general_config.get_default_price()
            bus_mode.origin = origin
            bus_mode.destination = destination
            bus_mode.heading_from = station_list[-1]
            bus_mode.heading_to = station_list[0]
            mode_list.append(bus_mode)
    return mode_list


def __generate_train_mode():
    """
    :rtype list[TransportationMode]
    :return:
    """
    mode_list = []
    train_route_list = train_route_accessor.get_all_train_routes()
    """:type :list[TrainRoute]"""
    for train_route in train_route_list:
        station_list = train_route.stations
        line_name = train_route.line_name
        origin_list = station_list[:-1]
        destination_list = station_list[1:]
        for origin, destination in zip(origin_list, destination_list):
            # TODO remove this eta hack!
            eta = 180
            transportation_mode = TransportationMode()
            transportation_mode.eta = eta
            transportation_mode.name = ' '.join(['KRL', origin, '-', destination])
            transportation_mode.origin = origin
            transportation_mode.destination = destination
            # TODO remove this price hack
            transportation_mode.price = 500
            transportation_mode.heading_from = station_list[0]
            transportation_mode.heading_to = station_list[-1]
            mode_list.append(transportation_mode)

        for destination, origin in zip(origin_list, destination_list):
            # TODO remove this eta hack!
            eta = 180
            transportation_mode = TransportationMode()
            transportation_mode.eta = eta
            transportation_mode.name = ' '.join(['KRL', origin, '-', destination])
            transportation_mode.origin = origin
            transportation_mode.destination = destination
            # TODO remove this price hack
            transportation_mode.price = 500
            transportation_mode.heading_from = station_list[-1]
            transportation_mode.heading_to = station_list[0]
            mode_list.append(transportation_mode)
    return mode_list


def __generate_walk_mode():
    """
    :rtype list[TransportationMode]
    :return:
    """
    mode_list = []
    walk_route_list = walk_route_accessor.get_all_walk_routes()
    """ :type :list[WalkRoute]"""
    for walk_route in walk_route_list:
        origin = walk_route.walk_from
        destination = walk_route.walk_to
        transportation_mode = TransportationMode()
        # TODO remove this hack!
        transportation_mode.eta = 60
        transportation_mode.name = 'Jalan Santai'
        transportation_mode.origin = origin
        transportation_mode.destination = destination
        transportation_mode.price = 0
        transportation_mode.heading_from = origin
        transportation_mode.heading_to = destination
        mode_list.append(transportation_mode)

    for walk_route in walk_route_list:
        origin = walk_route.walk_to
        destination = walk_route.walk_from
        transportation_mode = TransportationMode()
        # TODO remove this hack!
        transportation_mode.eta = 60
        transportation_mode.name = 'Jalan Santai'
        transportation_mode.origin = origin
        transportation_mode.destination = destination
        transportation_mode.price = 0
        transportation_mode.heading_from = origin
        transportation_mode.heading_to = destination
        mode_list.append(transportation_mode)
    return mode_list


def __generate_busway_transfer_mode():
    """
    :rtype list[TransportationMode]
    :return:
    """
    mode_list = []
    busway_transfer_list = busway_transfer_accessor.get_all_busway_transfers()
    for busway_transfer in busway_transfer_list:
        origin = busway_transfer.from_station
        destination = busway_transfer.to_station
        transportation_mode = TransportationMode()
        transportation_mode.eta = 60
        transportation_mode.name = 'Jalan Santai'
        transportation_mode.origin = origin
        transportation_mode.destination = destination
        transportation_mode.price = 0
        transportation_mode.heading_from = origin
        transportation_mode.heading_to = destination
        mode_list.append(transportation_mode)

    for busway_transfer in busway_transfer_list:
        origin = busway_transfer.to_station
        destination = busway_transfer.from_station
        transportation_mode = TransportationMode()
        transportation_mode.eta = 60
        transportation_mode.name = 'Jalan Santai'
        transportation_mode.origin = origin
        transportation_mode.destination = destination
        transportation_mode.price = 0
        transportation_mode.heading_from = origin
        transportation_mode.heading_to = destination
        mode_list.append(transportation_mode)
    return mode_list


def __generate_graph(mode_list):
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


def __generate_transportation_graph():
    """
    :rtype ConnectedGraph
    """
    busway_mode_list = __generate_busway_mode()
    train_mode_list = __generate_train_mode()
    walk_mode_list = __generate_walk_mode()
    busway_transfer_mode_list = __generate_busway_transfer_mode()
    total_mode_list = []
    total_mode_list.extend(busway_mode_list)
    total_mode_list.extend(train_mode_list)
    total_mode_list.extend(walk_mode_list)
    total_mode_list.extend(busway_transfer_mode_list)
    connected_graph = __generate_graph(total_mode_list)
    return connected_graph


def __same_mode(mode1, mode2):
    """
    :type mode1:TransportationMode
    :type mode2:TransportationMode
    :param mode1:
    :param mode2:
    :return:
    """
    return mode2.name == mode1.name


def __merge_mode(mode1, mode2):
    """
    :type mode1:TransportationMode
    :type mode2:TransportationMode
    :param mode1:
    :param mode2:
    :return:
    """
    copied_mode = deepcopy(mode2)
    copied_mode.origin = mode1.origin
    return copied_mode


def __merge_list(alis1, alis2):
    if __same_mode(alis1[-1], alis2[0]):
        newlis = []
        newlis.extend(alis1[:-1])
        newlis.append(__merge_mode(alis1[-1], alis2[0]))
        newlis.extend(alis2[1:])
        return newlis
    else:
        newlis = []
        newlis.extend(alis1)
        newlis.extend(alis2)
        return newlis


def __summarize_mode(alis):
    if len(alis) < 2:
        return alis
    else:
        lise1 = __summarize_mode(alis[:len(alis) / 2])
        lise2 = __summarize_mode(alis[len(alis) / 2:])
        return __merge_list(lise1, lise2)


def get_direction(source, destination):
    """
    :rtype list[SearchResult]
    :param source:
    :param destination:
    :return:
    """
    direction_recommendation = []
    connected_graph = __generate_transportation_graph()
    assert isinstance(connected_graph, ConnectedGraph)
    cost, previous, transport = connected_graph.find_shortest_path(source)
    transport_to_destination = transport[destination]
    for transport in transport_to_destination:
        search_result = SearchResult()
        search_result.branch = None
        search_result.source = source
        search_result.destination = destination
        search_result.mode_list = __summarize_mode(transport[1])
        search_result.mode_list_count = len(search_result.mode_list)
        search_result.time = transport[0]
        search_result.price = 0
        direction_recommendation.append(search_result)
    return direction_recommendation


def get_next_bus(source, destination, next_stop):
    next_bus = next_bus_accessor.get_next_stop(source, destination, next_stop)
    if next_bus:
        assert (isinstance(next_bus, NextBus))
    return next_bus
