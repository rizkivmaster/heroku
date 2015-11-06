import urllib2
import xml.etree.ElementTree as Et
import logging
import datetime

from app.meloentjoer.accessors.eta_estimates.BusEstimationAccessor import BusEstimationAccessor
from app.meloentjoer.accessors.next_buses.BusNextStopAccessor import BusNextStopAccessor
from app.meloentjoer.common.behavioral.Cacheable import Cacheable
from app.meloentjoer.common.executors.SchedulerExecutor import SchedulerExecutor
from app.meloentjoer.common.behavioral.Startable import Startable
from app.meloentjoer.accessors.bus_routes.BusRoute import BusRoute
from app.meloentjoer.accessors.bus_routes.BusRouteAccessor import BusRouteAccessor
from app.meloentjoer.accessors.next_buses.NextBus import NextBus
from app.meloentjoer.config.GeneralConfig import GeneralConfig
from app.meloentjoer.fetcher.track.BusTrackData import BusTrackData
from app.meloentjoer.accessors.bus_states.BusState import BusState
from app.meloentjoer.accessors.geo_data.GeoDataAccessor import GeoDataAccessor
from app.meloentjoer.accessors.bus_states.BusStateAccessor import BusStateAccessor
import numpy as np


class BusWayTrackFetcher(Startable, Cacheable):
    def refresh(self):
        bus_data = self.__request_buses()
        mapping_threshold = self.general_config.get_mapping_threshold()
        station_location = self.geo_data_accessor.get_station_location()
        bus_routes = self.bus_routes_accessor.get_all_bus_routes()

        self.__update_bus_states_and_bus_queues(
            bus_data,
            mapping_threshold,
            station_location,
            bus_routes
        )

    def __init__(self,
                 executor,
                 bus_estimation_accessor,
                 bus_state_accessor,
                 bus_next_stop_accessor,
                 geo_data_accessor,
                 bus_routes_accessor,
                 general_config):
        """
        :type: executor: PoolExecutor
        :type general_config: GeneralConfig
        :type bus_state_accessor: BusStateAccessor
        :type bus_next_stop_accessor: BusNextStopAccessor
        :type geo_data_accessor: GeoDataAccessor
        :type bus_estimation_accessor: BusEstimationAccessor
        :type bus_routes_accessor: BusRouteAccessor
        :param executor: Startable
        :return:
        """
        self.scheduler = SchedulerExecutor(executor, 2, self.refresh)

        self.bus_estimation_accessor = bus_estimation_accessor
        self.bus_state_accessor = bus_state_accessor
        self.bus_next_stop_accessor = bus_next_stop_accessor
        self.geo_data_accessor = geo_data_accessor
        self.bus_routes_accessor = bus_routes_accessor

        self.general_config = general_config

        self.refresh_period = 3

    def __get_session_key(self):
        req = urllib2.Request('http://smartcityjakarta.com/bustrack/')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Accept-Language', 'en-US,en;q=0.5')
        req.add_header('Cache-Control', 'max-age=0')
        req.add_header('Connection', 'keep-alive')
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
        req.add_header('Host', 'smartcityjakarta.com')
        test = urllib2.urlopen(req)
        try:
            for value in test.info().values():
                if 'PHPSESSID' in value:
                    return value.split(";")[0]
        except Exception, e:
            logging.error(e)
        return None

    def __request_buses(self):
        """
        :rtype dict[str,BusTrackData]
        :return:
        """
        req = urllib2.Request('http://smartcityjakarta.com/bustrack/stadtbus_rapperswil.php')
        req.add_header('Accept', 'application/xml, text/xml, */*; q=0.01')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Connection', 'keep-alive')
        req.add_header('Accept-Language', 'en-US,en;q=0.5')
        req.add_header('Cache-Control', 'max-age=0')
        req.add_header('Connection', 'keep-alive')
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
        req.add_header('Host', 'smartcityjakarta.com')
        req.add_header('Referer', 'http://smartcityjakarta.com/bustrack/')
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        session_key = self.__get_session_key()
        if session_key is None:
            logging.error('No session key found')
            return None
        req.add_header('Cookie', session_key)
        response = urllib2.urlopen(req)
        htmlfile = response.read()
        root = Et.fromstring(htmlfile)
        dix = dict()
        for bus in root[3]:
            dixx = dict()
            for node in bus:
                dixx[node.tag] = node.text
            bus_track_data = BusTrackData()
            bus_track_data.name = dixx['identifier']
            bus_track_data.longitude = float(dixx['lon'])
            bus_track_data.latitude = float(dixx['lat'])
            bus_track_data.speed = float(dixx['speedKmh'])
            dix[bus_track_data.name] = bus_track_data
        return dix

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

    def __bus_queue_key(self, source, destination, current):
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

    def __locate_bus(self, bus_coordinates, threshold, coordinates_mapper):
        station_list = []
        for bus_coordinate in bus_coordinates:
            bus_coordinate = np.array(bus_coordinate)
            closest_coordinate, closest_station = min(
                map(lambda x: (np.linalg.norm(bus_coordinate - np.array((x[1], x[2]))), x), coordinates_mapper))
            station_list.append(closest_station[0] if (closest_coordinate < threshold) else None)
        return station_list

    def __update_bus_states_and_bus_queues(self,
                                           buses_data,
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
        bus_stops = self.__locate_bus(bus_coordinates, mapping_threshold, station_locations)
        bus_name_stops = filter(lambda x: x[1] is not None, zip(bus_names, bus_stops))
        # update bus states
        bus_state_list = self.bus_state_accessor.get_all_bus_state()
        for bus_name, bus_stop in bus_name_stops:
            bus_state = self.bus_state_accessor.get_bus_state(bus_name)
            if bus_name is not None:
                assert (isinstance(bus_state, BusState))
                if not bus_state.last_station == bus_stop:
                    bus_state.previous_station = bus_state.last_station
                    bus_state.previous_time_stop = bus_state.last_time_stop
                    bus_state.last_station = bus_stop
                    bus_state.last_time_stop = datetime.datetime.utcnow()
                    bus_state.stop_list.append(bus_stop)
                    self.bus_state_accessor.upset_bus_state(bus_state)

                    if bus_state.last_time_stop is not None and bus_state.previous_time_stop is not None:
                        origin = bus_state.previous_station
                        destination = bus_state.last_station
                        delta = (bus_state.last_time_stop - bus_state.previous_time_stop).seconds
                        logging.info('Learn from {0} to {1} is {2}'.format(origin, destination, delta))
                        self.bus_estimation_accessor.add_sample(origin, destination, delta)

            else:
                bus_state = BusState()
                bus_state.last_station = bus_stop
                bus_state.last_time_stop = datetime.datetime.utcnow()
                bus_state.stop_list.append(bus_stop)
                self.bus_state_accessor.upset_bus_state(bus_state)

        # update bus next stop
        self.bus_next_stop_accessor.reset()
        refreshed_bus_state_list = self.bus_state_accessor.get_all_bus_state()
        for bus_state in refreshed_bus_state_list:
            for bus_route in bus_routes:
                forward_route = bus_route.stations
                backward_route = bus_route.stations[::-1]
                if self.__is_in(bus_state.stop_list, forward_route):
                    last_station = bus_state.last_station
                    last_index = forward_route.index(last_station)
                    if last_index + 1 < len(forward_route):
                        next_stop = forward_route[last_index + 1]
                        prediction = self.bus_estimation_accessor.predict_eta(last_station, next_stop)
                        next_bus = NextBus()
                        next_bus.bus_name = bus_name
                        next_bus.prediction = prediction
                        next_bus.current_station = last_station
                        self.bus_next_stop_accessor.set_next_bus(forward_route[0], forward_route[-1], next_stop,
                                                                 next_bus)

                if self.__is_in(bus_state.stop_list, backward_route):
                    last_station = bus_state.last_station
                    last_index = backward_route.index(last_station)
                    if last_index + 1 < len(backward_route):
                        next_stop = backward_route[last_index + 1]
                        prediction = self.bus_estimation_accessor.predict_eta(last_station, next_stop)
                        next_bus = NextBus()
                        next_bus.bus_name = bus_name
                        next_bus.prediction = prediction
                        next_bus.current_station = last_station
                        self.bus_next_stop_accessor.set_next_bus(forward_route[0], forward_route[-1], next_stop,
                                                                 next_bus)

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.stop()
