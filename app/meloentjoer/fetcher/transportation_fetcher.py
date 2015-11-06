from app.meloentjoer.accessors import bus_route_accessor as __bus_route_accessor
from app.meloentjoer.common import general_executor as __executor
from app.meloentjoer.config import general_config as __general_config
from app.meloentjoer.fetcher.geo import helper as __helper


def __update():
    route_list = __helper.get_busway_routes()
    for route in route_list:
        __bus_route_accessor.upset_bus_route(route)


__update_period = __general_config.get_geo_refresh_period()
__scheduler = __executor.schedule(__update_period, __update)


def start():
    __scheduler.start()


def stop():
    __scheduler.stop()
