__author__ = 'traveloka'
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class PostgresAccessorBase(Session):
    def __init__(self, model_base, database_url):
        """
        :type model_base: ModelBase
        :type database_url: str
        :param model_base: Base from declarative base
        :param database_url: an url for your sql database
        :return: void
        """
        self.model_base = model_base
        engine = create_engine(database_url, echo=False)
        model_base.metadata.create_all(engine)
        super(PostgresAccessorBase, self).__init__(bind=engine)
