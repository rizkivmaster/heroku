from app.meloentjoer.accessors import bus_route_accessor, bus_estimation_accessor, bus_state_accessor, \
    next_bus_accessor
from app.meloentjoer.common.logging import logger as __logger
from app.meloentjoer.fetcher import transportation_info_fetcher, busway_track_fetcher
from app.meloentjoer.services import autocomplete_service, search_service
from app.meloentjoer.config import general_config


def start():
    # warming up
    __logger.info('System is warming up')
    bus_estimation_accessor.start()
    transportation_info_fetcher.start()
    busway_track_fetcher.start()
    autocomplete_service.start()
    __logger.info('All components have been started')


def stop():
    bus_estimation_accessor.stop()
    transportation_info_fetcher.stop()
    busway_track_fetcher.stop()
    autocomplete_service.stop()


start()
