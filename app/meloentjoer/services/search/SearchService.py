class SearchService(object):
    def get_direction(self, source, destination):
        """
        :type source: str
        :type destination: str
        :param source: the starting station of the bus
        :param destination: the next station on arriving
        :return:
        :rtype list[SearchResult]
        """
        pass

    def get_next_bus(self, source, destination, next_stop):
        """
        :type next_stop: str
        :param next_stop:
        :return: list[BusStopResult]
        :rtype NextBus
        """
        pass
