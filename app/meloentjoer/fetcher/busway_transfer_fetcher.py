from app.meloentjoer.accessors.routes import busway_transfer_accessor
from app.meloentjoer.common import general_scheduler
from app.meloentjoer.common.logging import logger_factory
from app.meloentjoer.config import general_config
from app.meloentjoer.fetcher.util import helper

__logger = logger_factory.create_logger(__name__)


def __update():
    __logger.info('Updating busway transfer data')
    route_list = helper.get_busway_transfers()
    for busway_transfer in route_list:
        busway_transfer_accessor.upset_busway_transfer(busway_transfer)


__update_period = general_config.get_busway_transfer_refresh_period()
__scheduler = general_scheduler.schedule(__update_period, __update)


def start():
    __update()
    __scheduler.start()


def stop():
    __logger.info('Stopped')
    __scheduler.stop()
