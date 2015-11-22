from app.meloentjoer.accessors.entity.TrainRoute import TrainRoute
from app.meloentjoer.common.databases.ModelBase import ModelBase
from app.meloentjoer.common.databases.PostgreBase import PostgresAccessorBase
from app.meloentjoer.config import general_config as __config
from sqlalchemy import String, Column
from app.meloentjoer.common.logging import logger_factory

__logger = logger_factory.create_logger(__name__)


class TrainRouteModel(ModelBase):
    __tablename__ = "TrainRouteModel"
    line_name = Column(String, primary_key=True)
    stations = Column(String)

    def __init__(self):
        self.line_name = None
        self.stations = None

    def to_train_route(self):
        train_route = TrainRoute()
        train_route.line_name = self.line_name
        train_route.stations = self.stations.split(';')
        return train_route

    def from_train_route(self, train_route):
        """
        :type train_route : TrainRoute
        """
        self.line_name = train_route.line_name
        self.stations = ';'.join(train_route.stations)


train_routes_session = PostgresAccessorBase(TrainRouteModel,
                                            __config.get_database_url())


def reset():
    train_routes_session.query(TrainRouteModel).delete()
    train_routes_session.commit()


def get_train_route_by_line(line_name):
    """
    :rtype :TrainRoute
    :param line_name:
    """
    raw_train_route = train_routes_session.query(TrainRouteModel).filter(
        TrainRouteModel.line_name == line_name).first()
    return raw_train_route.to_train_route() if raw_train_route is not None else None


def get_all_train_routes():
    """
    :return:
    :rtype dict[str,TrainRoute]
    """
    raw_train_route_list = train_routes_session.query(TrainRouteModel).all()
    train_route_list = [train_route.to_train_route() for train_route in raw_train_route_list]
    return train_route_list


def upset_train_route(train_route):
    """
    :type train_route: TrainRoute
    :param train_route:
    :return:
    """
    raw_train_route = get_train_route_by_line(train_route.line_name)
    if raw_train_route is None:
        raw_train_route = TrainRouteModel()
        raw_train_route.from_train_route(train_route)
        train_routes_session.add(raw_train_route)
    train_routes_session.commit()
