from sqlalchemy import Column, String, Integer
from sqlalchemy import Binary
from app.meloentjoer.common.databases.ModelBase import ModelBase


class TransportationMode(ModelBase):
    __tablename__ = 'TransportationMode'
    id = Column(Binary, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    price = Column(Integer)
    eta = Column(Integer)
    destination = Column(String)
    origin = Column(String)

    def __init__(self):
        self.name = None
        self.price = None
        self.eta = None
        self.destination = None
        self.origin = None

    def cost(self):
        return self.eta

    def __str__(self):
        return '{0},{1},{2},{3},{4}'.format(self.origin, self.name, self.destination, self.price, self.eta)
