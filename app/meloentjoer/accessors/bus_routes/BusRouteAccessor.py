from app.meloentjoer.common.behavioral.Accessor import Accessor


class BusRouteAccessor(Accessor):
    def get_bus_route_by_corridor(self, corridor_name):
        """
        :type corridor_name: str
        :param corridor_name:
        :return:
        :rtype BusRoute
        """
        pass

    def get_all_bus_routes(self):
        """
        :return:
        :rtype dict[str, BusRoute]
        """
        pass

    def upset_bus_route(self, bus_route):
        pass

    def reset(self):
        """
        delete all records
        :return:
        """
        pass
