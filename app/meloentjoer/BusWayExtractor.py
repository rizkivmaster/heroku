__author__ = 'traveloka'
import numpy as np
import BusWayCoordinateFetcher
import BusWayFetcher
import datetime


class BusState:
    def __init__(self):
        self.last_station = None
        self.last_time_stop = None
        self.previous_station = None
        self.previous_time_stop = None
        self.stop_list = []


class BusETAEstimator:
    def __init__(self):
        self.estimator_dictionary = dict()

    def __get_key(self, origin, destination):
        return "{0}_{1}".format(origin,destination)

    def add_sample(self, origin, destination, delta):
        key = self.__get_key(origin, destination)
        delta = float(delta)
        if key in self.estimator_dictionary:
            delta_mean, sample_size = self.estimator_dictionary[key]
            new_delta_mean = (delta+(sample_size*delta_mean))/(sample_size+1)
            self.estimator_dictionary[key] = (new_delta_mean, sample_size+1)
        else:
            self.estimator_dictionary[key] = (delta, 1)

    # params: station name:String, station name:string
    # return: seconds prediction (float)
    def predict_eta(self, origin, destination):
        key = self.__get_key(origin, destination)
        if key in self.estimator_dictionary.has_key(key):
            return self.estimator_dictionary[key]
        else:
            return None


class BusLocator:
    # coordinates_mapper: triple of station name,lat,lon(string,float,float)
    def __init__(self, coordinates_mapper, threshold):
        self.coordinates_mapper = coordinates_mapper
        self.threshold = float(threshold)

    # coordinates: list of coordinate(tuple of float)
    def locate(self, bus_coordinates):
        station_list = []
        for bus_coordinate in bus_coordinates:
            bus_coordinate = np.array(bus_coordinate)
            closest_coordinate, closest_station = min(map(lambda x: (np.linalg.norm(bus_coordinate-np.array((x[1], x[2]))), x), self.coordinates_mapper))
            station_list.append(closest_station[0] if(closest_coordinate < self.threshold) else None)
        return station_list


class BusExtractor:

    def __init__(self, coordinates_mapper, mapping_threshold):
        self.bus_states = dict()
        self.eta_estimator = BusETAEstimator()
        self.bus_locator = BusLocator(coordinates_mapper, mapping_threshold)
        self.bus_coordinate_fetcher = BusWayCoordinateFetcher()
        self.bus_routes = BusWayFetcher().get_routes()
        self.bus_next_stops = dict()

    def __is_in(self, stop_list, station_list):
        if len(station_list) == 0 or len(stop_list) == 0:
            return False
        if stop_list[0] == station_list[0]:
            if stop_list[-1] == station_list[-1]:
                return True
            else:
                return self.__is_in(stop_list, station_list[:-1])
        else:
            return self.__find_segment(stop_list, station_list[1:])

    def __add_sample(self, buses_data):
        bus_names = buses_data.keys()
        bus_coordinates = [(float(buses_data[bus_name]['lat']), float(buses_data[bus_name]['lon'])) for bus_name in bus_names]
        bus_stops = self.bus_locator.locate(bus_coordinates)
        bus_name_stops = filter(lambda x: x[1] is not None, zip(bus_names, bus_stops))
        # update bus states
        for bus_name, bus_stop in bus_name_stops:
            if bus_name in self.bus_states:
                bus_state = BusState(self.bus_states[bus_name])
                if bus_state.last_station == bus_stop:
                    bus_state.previous_station = bus_state.last_station
                    bus_state.last_time_stop = bus_state.last_time_stop
                    bus_state.last_station = bus_name
                    bus_state.last_time_stop = datetime.datetime.utcnow()
                    bus_state.stop_list.append(bus_stop)
                    self.bus_states[bus_name] = bus_state

                    if bus_state.previous_station is not None:
                        origin = bus_state.previous_station
                        destination = bus_state.last_station
                        delta = (bus_state.last_time_stop - bus_state.previous_time_stop).seconds
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
                    if last_index+1 < len(forward_route):
                        next_stop = forward_route[last_index+1]
                        prediction = self.eta_estimator.predict_eta(last_station,next_stop)
                        self.bus_next_stops[next_stop] = (bus_name, prediction)

                if self.__is_in(bus_state.stop_list, backward_route):
                    last_station = bus_state.last_station
                    last_index = backward_route.index(last_station)
                    if last_index+1 < len(backward_route):
                        next_stop = backward_route[last_index+1]
                        prediction = self.eta_estimator.predict_eta(last_station,next_stop)
                        self.bus_next_stops[next_stop] = (bus_name, prediction)

    def run_extractor(self):
        while True:
            buses_data = self.bus_coordinate_fetcher.request_buses()
            self.__add_sample(buses_data)
            print(self.bus_next_stops)