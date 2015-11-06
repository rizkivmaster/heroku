from app.meloentjoer.accessors.bus_routes.BusRouteAccessorTest import bus_route_accessor
from app.meloentjoer.common.executors.SchedulerExecutor import SchedulerExecutor
from app.meloentjoer.config import general_config as __gc
from app.meloentjoer.fetcher.geo import helper


def __update():
    route_list = helper.get_busway_routes()
    for route in route_list:
        bus_route_accessor.upset_bus_route(route)


__update_period = __gc.get_geo_refresh_period()
__scheduler = SchedulerExecutor(__update_period, __update)


def start():
    __scheduler.start()


def stop():
    __scheduler.stop()
