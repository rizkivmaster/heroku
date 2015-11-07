from app.meloentjoer.accessors.entity.BusRoute import BusRoute
from app.meloentjoer.common.databases.ModelBase import ModelBase
from app.meloentjoer.common.databases.PostgreBase import PostgresAccessorBase
from app.meloentjoer.config import general_config as __config
from sqlalchemy import String, Column
from app.meloentjoer.common.logging import logger as __logger


class BusRouteModel(ModelBase):
    __tablename__ = "BusRouteModel"
    corridor_name = Column(String, primary_key=True)
    stations = Column(String)

    def __init__(self):
        bus_routes_session.corridor_name = None
        bus_routes_session.stations = None

    def to_bus_route(self):
        bus_route = BusRoute()
        bus_route.corridor_name = self.corridor_name
        bus_route.stations = self.stations.split(',')
        return bus_route


bus_routes_session = PostgresAccessorBase(BusRouteModel,
                                          __config.get_database_url())


def reset():
    bus_routes_session.query(BusRouteModel).delete()
    bus_routes_session.commit()


def get_bus_route_by_corridor(corridor_name):
    """
    :rtype BusRoute
    :param corridor_name:
    :return: BusRoute
    """
    raw_bus_route = bus_routes_session.query(BusRouteModel).filter(BusRouteModel.corridor_name == corridor_name).first()
    return raw_bus_route.to_bus_route() if raw_bus_route is not None else None


def get_all_bus_routes():
    """
    :return:
    :rtype dict[str,BusRoute]
    """
    raw_bus_route_list = bus_routes_session.query(BusRouteModel).all()
    bus_route_list = [bus_route.to_bus_route() for bus_route in raw_bus_route_list]
    return bus_route_list


def upset_bus_route(bus_route):
    """
    :type bus_route: BusRoute
    :param bus_route:
    :return:
    """
    raw_bus_route = get_bus_route_by_corridor(bus_route.corridor_name)
    try:
        assert (isinstance(raw_bus_route, BusRoute) if raw_bus_route is not None else True)
    except AssertionError, e:
        __logger.error(e)
    if raw_bus_route is None:
        raw_bus_route = BusRouteModel()
        raw_bus_route.corridor_name = bus_route.corridor_name
        raw_bus_route.stations = ','.join(bus_route.stations)
        bus_routes_session.add(raw_bus_route)
    raw_bus_route.stations = ','.join(bus_route.stations)
    bus_routes_session.commit()
