__author__ = 'traveloka'

from sqlalchemy import create_engine,ForeignKey
from sqlalchemy import Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///jarvis.db',echo=True)
Base = declarative_base()

class Document(Base):
    __tablename__ = "document"

    id = Column(Integer,primary_key=True)
    json = Column(String)

    def __init__(self,json):
        self.json = json

Base.metadata.create_all(engine)