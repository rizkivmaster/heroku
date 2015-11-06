from BusRouteAccessor import BusRouteAccessor
from app.meloentjoer.accessors.bus_routes.BusRoute import BusRoute
from app.meloentjoer.common.databases.ModelBase import ModelBase
from app.meloentjoer.common.databases.PostgreBase import PostgresAccessorBase
from app.meloentjoer.config.GeneralConfig import GeneralConfig
from sqlalchemy import String, Column


class BusRoutePostgresAccessorImpl(PostgresAccessorBase, BusRouteAccessor):
    def __init__(self, config):
        """
        :type config: GeneralConfig
        :return:
        """
        super(BusRoutePostgresAccessorImpl, self).__init__(BusRouteModel,
                                                           config.get_database_url())

    def reset(self):
        self.query(BusRouteModel).delete()
        self.commit()

    def get_bus_route_by_corridor(self, corridor_name):
        """
        :rtype BusRoute
        :param corridor_name:
        :return: BusRoute
        """
        raw_bus_route = self.query(BusRouteModel).filter(BusRouteModel.corridor_name == corridor_name).first()
        return raw_bus_route.to_bus_route() if raw_bus_route is not None else None

    def get_all_bus_routes(self):
        """
        :return:
        :rtype dict[str,BusRoute]
        """
        raw_bus_route_list = self.query(BusRouteModel).all()
        bus_route_list = [bus_route.to_bus_route() for bus_route in raw_bus_route_list]
        return bus_route_list

    def upset_bus_route(self, bus_route):
        """
        :type bus_route: BusRoute
        :param bus_route:
        :return:
        """
        raw_bus_route = self.get_bus_route_by_corridor(bus_route.corridor_name)
        assert (isinstance(raw_bus_route, BusRouteModel) if raw_bus_route is not None else True)
        if raw_bus_route is None:
            raw_bus_route = BusRouteModel()
            raw_bus_route.corridor_name = bus_route.corridor_name
            raw_bus_route.stations = ','.join(bus_route.stations)
            self.add(raw_bus_route)
        raw_bus_route.stations = ','.join(bus_route.stations)
        self.commit()


class BusRouteModel(ModelBase):
    __tablename__ = "BusRouteModel"
    corridor_name = Column(String, primary_key=True)
    stations = Column(String)

    def __init__(self):
        self.corridor_name = None
        self.stations = None

    def to_bus_route(self):
        bus_route = BusRoute()
        bus_route.corridor_name = self.corridor_name
        bus_route.stations = self.stations.split(',')
        return bus_route
