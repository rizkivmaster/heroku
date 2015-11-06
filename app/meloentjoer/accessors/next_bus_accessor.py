__bus_next_stop_cache = dict()


def __key(origin, destination, next_stop):
    return '{0}_{1}_{2}'.format(origin, destination, next_stop)


def set_next_bus(origin, destination, next_station, next_bus):
    """
    :param destination:
    :param origin:
    :type next_bus: NextBus
    """
    key = __key(origin, destination, next_station)
    __bus_next_stop_cache[key] = next_bus


def get_next_stop(origin, destination, next_station):
    """
    :type origin
    :type destination
    :type next_station
    :param origin:
    :param destination:
    :param next_station:
    :return:
    """
    key = __key(origin, destination, next_station)
    if key is not None and key in __bus_next_stop_cache:
        return __bus_next_stop_cache[key]
    return None


def reset():
    bus_next_stop_cache = dict()
