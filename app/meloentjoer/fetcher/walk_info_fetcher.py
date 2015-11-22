from app.meloentjoer.accessors.routes import walk_route_accessor
from app.meloentjoer.common import general_scheduler
from app.meloentjoer.common.logging import logger_factory
from app.meloentjoer.config import general_config
from app.meloentjoer.fetcher.util import helper as __helper

__logger = logger_factory.create_logger(__name__)


def __update():
    walk_route_list = __helper.get_walk_routes()
    for walk_route in walk_route_list:
        walk_route_accessor.upset_walk_route(walk_route)
    __logger.info('Updated')


__update_period = general_config.get_walk_route_refresh_period()
__scheduler = general_scheduler.schedule(__update_period, __update)


def start():
    __update()
    __scheduler.start()
    __logger.info('Started')


def stop():
    __logger.info('Stopped')
    __scheduler.stop()
