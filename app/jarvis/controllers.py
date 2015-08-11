__author__ = 'traveloka'


from sqlalchemy import create_engine,ForeignKey
from sqlalchemy import Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref,sessionmaker
from flask import Blueprint,jsonify
import json

engine = create_engine('postgresql://postgres:postgres@localhost:5432/jarvis',echo=True)
Base = declarative_base()

class Document(Base):
    __tablename__ = "document"

    id = Column(Integer,primary_key=True)
    json = Column(String)

    def __init__(self,json):
        self.json = json

    def __str__(self):
        return '{0} {1}'.format(self.id,self.json)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def listDocument():
    res = session.query(Document).all()
    return [x.__dict__['json'] for x in res]

jarvis = Blueprint('jarvis',__name__)


@jarvis.route('/')
def update():
    results = listDocument()
    return '['+','.join(results)+']'