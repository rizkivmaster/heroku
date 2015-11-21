import logging
import datetime

from app.meloentjoer.accessors import geo_data_accessor, bus_state_accessor, bus_estimation_accessor, \
    next_bus_accessor
from app.meloentjoer.accessors.routes import bus_route_accessor
from app.meloentjoer.accessors.entity.NextBus import NextBus
from app.meloentjoer.common import general_scheduler
from app.meloentjoer.common.logging import logger_factory
from app.meloentjoer.config import general_config as __general_config
from app.meloentjoer.fetcher.entity.BusTrackData import BusTrackData
from app.meloentjoer.accessors.entity.BusState import BusState
from app.meloentjoer.fetcher.util import helper as __helper
import numpy as np

__logger = logger_factory.create_logger('busway_track_fetcher')


def __is_in(stop_list, station_list):
    if len(station_list) < 2 or len(stop_list) < 2:
        return False
    if stop_list[0] == station_list[0]:
        if stop_list[-1] == station_list[-1]:
            return True
        else:
            return __is_in(stop_list, station_list[:-1])
    else:
        return __is_in(stop_list, station_list[1:])


def __locate_bus(bus_coordinates, threshold, coordinates_mapper):
    station_list = []
    for bus_coordinate in bus_coordinates:
        bus_coordinate = np.array(bus_coordinate)
        closest_coordinate, closest_station = min(
            map(lambda x: (np.linalg.norm(bus_coordinate - np.array((x[1], x[2]))), x), coordinates_mapper))
        station_list.append(closest_station[0] if (closest_coordinate < threshold) else None)
    return station_list


def __update_bus_states_and_bus_queues(buses_data,
                                       mapping_threshold,
                                       station_locations,
                                       bus_routes):
    """
    :type buses_data: dict[str,BusTrackData]
    :type bus_routes: list[BusRoute]
    :param buses_data:
    :return:
    """
    bus_names = buses_data.keys()
    bus_coordinates = [(float(buses_data[bus_name].latitude), float(buses_data[bus_name].longitude)) for bus_name in
                       bus_names]
    bus_stops = __locate_bus(bus_coordinates, mapping_threshold, station_locations)
    bus_name_stops = filter(lambda x: x[1] is not None, zip(bus_names, bus_stops))
    # update bus states
    bus_state_list = bus_state_accessor.get_all_bus_state()
    for bus_name, bus_stop in bus_name_stops:
        bus_state = bus_state_accessor.get_bus_state(bus_name)
        if bus_state is not None:
            assert isinstance(bus_state, BusState)
            if not bus_state.last_station == bus_stop:
                bus_state.name = bus_name
                bus_state.previous_station = bus_state.last_station
                bus_state.previous_time_stop = bus_state.last_time_stop
                bus_state.last_station = bus_stop
                bus_state.last_time_stop = datetime.datetime.utcnow()
                bus_state.stop_list.append(bus_stop)
                bus_state_accessor.upset_bus_state(bus_state)

                if bus_state.last_time_stop is not None and bus_state.previous_time_stop is not None:
                    origin = bus_state.previous_station
                    destination = bus_state.last_station
                    delta = (bus_state.last_time_stop - bus_state.previous_time_stop).seconds
                    logging.info('Learn from {0} to {1} is {2}'.format(origin, destination, delta))
                    bus_estimation_accessor.add_sample(origin, destination, delta)

        else:
            bus_state = BusState()
            bus_state.name = bus_name
            bus_state.last_station = bus_stop
            bus_state.last_time_stop = datetime.datetime.utcnow()
            bus_state.stop_list.append(bus_stop)
            bus_state_accessor.upset_bus_state(bus_state)

    # update bus next stop
    next_bus_accessor.reset()
    refreshed_bus_state_list = bus_state_accessor.get_all_bus_state()
    for bus_state in refreshed_bus_state_list:
        for bus_route in bus_routes:
            forward_route = bus_route.stations
            backward_route = bus_route.stations[::-1]
            if __is_in(bus_state.stop_list, forward_route):
                last_station = bus_state.last_station
                last_index = forward_route.index(last_station)
                if last_index + 1 < len(forward_route):
                    next_stop = forward_route[last_index + 1]
                    prediction = bus_estimation_accessor.predict_eta(last_station, next_stop)
                    next_bus = NextBus()
                    next_bus.bus_name = bus_name
                    next_bus.prediction = prediction
                    next_bus.current_station = last_station
                    next_bus_accessor.set_next_bus(forward_route[0], forward_route[-1], next_stop,
                                                   next_bus)

            if __is_in(bus_state.stop_list, backward_route):
                last_station = bus_state.last_station
                last_index = backward_route.index(last_station)
                if last_index + 1 < len(backward_route):
                    next_stop = backward_route[last_index + 1]
                    prediction = bus_estimation_accessor.predict_eta(last_station, next_stop)
                    next_bus = NextBus()
                    next_bus.bus_name = bus_name
                    next_bus.prediction = prediction
                    next_bus.current_station = last_station
                    next_bus_accessor.set_next_bus(forward_route[0], forward_route[-1], next_stop,
                                                   next_bus)


def __refresh():
    __logger.info('Updating Bus Tracking data')
    bus_data = __helper.request_buses()
    mapping_threshold = __general_config.get_mapping_threshold()
    station_location = geo_data_accessor.get_station_location()
    bus_routes = bus_route_accessor.get_all_bus_routes()

    __update_bus_states_and_bus_queues(
        bus_data,
        mapping_threshold,
        station_location,
        bus_routes)


# logic part

__scheduler = general_scheduler.schedule(__general_config.get_eta_refresh_period(), __refresh)


def start():
    # hack: force to update immediately
    __refresh()
    __scheduler.start()


def stop():
    __logger.info('Stopped')
    __scheduler.stop()
