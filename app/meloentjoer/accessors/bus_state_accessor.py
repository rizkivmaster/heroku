bus_state_cache = dict()


def upset_bus_state(bus_state):
    """
    :type bus_state:app.meloentjoer.fetcher.track.BusState.BusState
    :param bus_state:
    :return:
    """
    if bus_state.name is not None:
        bus_state_cache[bus_state.name] = bus_state


def get_bus_state(bus_name):
    """
    :type bus_name: str
    :param bus_name:
    :return: BusState
    """
    if bus_name is not None and bus_name in bus_state_cache:
        return bus_state_cache[bus_name]
    return None


def get_all_bus_state():
    return bus_state_cache.values()
