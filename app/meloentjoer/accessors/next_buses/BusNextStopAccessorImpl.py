from app.meloentjoer.accessors.next_buses.BusNextStopAccessor import BusNextStopAccessor
from NextBus import NextBus


class BusNextStopAccessorImpl(BusNextStopAccessor):
    def __init__(self):
        self.bus_next_stop_cache = dict()

    def __key(self, origin, destination, next_stop):
        return '{0}_{1}_{2}'.format(origin, destination, next_stop)

    def set_next_bus(self, origin, destination, next_station, next_bus):
        """
        :param destination:
        :param origin:
        :type next_bus: NextBus
        """
        key = self.__key(origin, destination, next_station)
        self.bus_next_stop_cache[key] = next_bus

    def get_next_stop(self, origin, destination, next_station):
        """
        :type origin
        :type destination
        :type next_station
        :param origin:
        :param destination:
        :param next_station:
        :return:
        """
        key = self.__key(origin, destination, next_station)
        if key is not None and key in self.bus_next_stop_cache:
            return self.bus_next_stop_cache[key]
        return None

    def reset(self):
        self.bus_next_stop_cache = dict()
