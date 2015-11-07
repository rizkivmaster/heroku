from app.meloentjoer.accessors import bus_route_accessor, bus_estimattion_accessor, bus_state_accessor, \
    next_bus_accessor
from app.meloentjoer.fetcher import transportation_info_fetcher, busway_track_fetcher
from app.meloentjoer.services import autocomplete_service, search_service
from app.meloentjoer.config import general_config


def start():
    # warming up
    bus_estimattion_accessor.start()
    bus_state_accessor.reset()
    next_bus_accessor.reset()
    bus_route_accessor.reset()
    transportation_info_fetcher.start()
    busway_track_fetcher.start()
    autocomplete_service.start()


def stop():
    bus_estimattion_accessor.stop()
    transportation_info_fetcher.stop()
    busway_track_fetcher.stop()
    autocomplete_service.stop()

start()