import datetime
import logging
import pprint

from app.meloentjoer.tracking.BusLocator import BusLocator
from app.meloentjoer.accessors.bus_states.BusState import BusState
from app.meloentjoer.fetcher.track.BusWayTrackFetcher import BusWayCoordinateFetcher
from app.meloentjoer.accessors.geo_data.GeoDataAccessor import station_location, default_threshold
from app.meloentjoer.accessors.eta_estimates.BusEstimationAccessor import BusEstimationAccessor


class BuswayDataExtractionService(object):
    def __init__(self, coordinates_mapper, mapping_threshold, bus_routes):
        if coordinates_mapper is None:
            coordinates_mapper = station_location
        if mapping_threshold is None:
            mapping_threshold = default_threshold
        self.bus_states = dict()
        self.eta_estimator = BusEstimationAccessor()
        self.bus_locator = BusLocator(coordinates_mapper, mapping_threshold)
        self.bus_coordinate_fetcher = BusWayCoordinateFetcher()
        self.bus_routes = bus_routes
        self.bus_next_stops = dict()

    def __is_in(self, stop_list, station_list):
        if len(station_list) < 2 or len(stop_list) < 2:
            return False
        if stop_list[0] == station_list[0]:
            if stop_list[-1] == station_list[-1]:
                return True
            else:
                return self.__is_in(stop_list, station_list[:-1])
        else:
            return self.__is_in(stop_list, station_list[1:])

    def __key(self, source, destination, current):
        """
        :type source:str
        :type destination:str
        :type current:str
        :param source:
        :param destination:
        :param current:
        :return:
        """
        return '{0}_{1}_{2}'.format(source, destination, current)

    def __update_bus_state_and_bus_queue(self, buses_data):
        bus_names = buses_data.keys()
        bus_coordinates = [(float(buses_data[bus_name]['lat']), float(buses_data[bus_name]['lon'])) for bus_name in
                           bus_names]
        bus_stops = self.bus_locator.locate(bus_coordinates)
        bus_name_stops = filter(lambda x: x[1] is not None, zip(bus_names, bus_stops))
        # update bus states
        for bus_name, bus_stop in bus_name_stops:
            if bus_name in self.bus_states:
                bus_state = self.bus_states[bus_name]
                if not bus_state.last_station == bus_stop:
                    bus_state.previous_station = bus_state.last_station
                    bus_state.previous_time_stop = bus_state.last_time_stop
                    bus_state.last_station = bus_stop
                    bus_state.last_time_stop = datetime.datetime.utcnow()
                    bus_state.stop_list.append(bus_stop)
                    self.bus_states[bus_name] = bus_state

                    if bus_state.last_time_stop is not None and bus_state.previous_time_stop is not None:
                        origin = bus_state.previous_station
                        destination = bus_state.last_station
                        delta = (bus_state.last_time_stop - bus_state.previous_time_stop).seconds
                        logging.info('Learn from {0} to {1} is {2}'.format(origin, destination, delta))
                        self.eta_estimator.add_sample(origin, destination, delta)

            else:
                bus_state = BusState()
                bus_state.last_station = bus_stop
                bus_state.last_time_stop = datetime.datetime.utcnow()
                bus_state.stop_list.append(bus_stop)
                self.bus_states[bus_name] = bus_state

        # update bus next stops
        self.bus_next_stops = dict()
        for bus_name in self.bus_states.keys():
            bus_state = self.bus_states[bus_name]
            for bus_corridor in self.bus_routes.keys():
                forward_route = self.bus_routes[bus_corridor]
                backward_route = self.bus_routes[bus_corridor][::-1]
                if self.__is_in(bus_state.stop_list, forward_route):
                    last_station = bus_state.last_station
                    last_index = forward_route.index(last_station)
                    if last_index + 1 < len(forward_route):
                        next_stop = forward_route[last_index + 1]
                        key = self.__key(forward_route[0], forward_route[1], next_stop)
                        prediction = self.eta_estimator.predict_eta(last_station, next_stop)
                        if key not in self.bus_next_stops:
                            self.bus_next_stops[key] = []
                        self.bus_next_stops[key].append((bus_name, prediction, last_station))

                if self.__is_in(bus_state.stop_list, backward_route):
                    last_station = bus_state.last_station
                    last_index = backward_route.index(last_station)
                    if last_index + 1 < len(backward_route):
                        next_stop = backward_route[last_index + 1]
                        key = key = '{0}_{1}_{2}'.format(backward_route[0], backward_route[1], next_stop)
                        prediction = self.eta_estimator.predict_eta(last_station, next_stop)
                        if key not in self.bus_next_stops:
                            self.bus_next_stops[key] = []
                        self.bus_next_stops[key].append((bus_name, prediction, last_station))

    def run_extractor(self):
        while True:
            buses_data = self.bus_coordinate_fetcher.get_buses_coordinates()
            self.__update_bus_state_and_bus_queue(buses_data)
            print(datetime.datetime.now())
            pprint.pprint(self.bus_next_stops)

    def get_next_buses(self, source, destination, next_stop):
        """
        :type next_stop: str
        :type source: str
        :type destination: str
        :param next_stop:
        :return:
        """
        key = self.__key(source, destination, next_stop)
        next_bus_list = self.bus_next_stops[key] if key in self.bus_next_stops else []
        return next_bus_list
