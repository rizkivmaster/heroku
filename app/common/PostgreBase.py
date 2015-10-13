__author__ = 'traveloka'
from sqlalchemy import String, Date, BigInteger, create_engine, ForeignKey, Column, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()



class PostgresAccessorBase(Session):

    def __init__(self, model_base, database_url):

        """
        :param model_base: Base from declarative base
        :param database_url: an url for your sql database
        :return: void
        """
        engine = create_engine(database_url, echo=True)
        model_base.metadata.create_all(engine)
        super(PostgresAccessorBase, self).__init__(bind=engine)