__author__ = 'traveloka'


from sqlalchemy import create_engine,ForeignKey
from sqlalchemy import Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref,sessionmaker
import json
import logging
import os

database_url = os.environ['DATABASE_URL']

engine = create_engine(database_url,echo=True)

Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()


class Capsy(Base):
    __tablename__ = "capsy"

    id = Column(Integer,primary_key=True)
    json = Column(String)

    def __init__(self,item):
        self.item = item
        self.update()
        session.add(self)

    def __str__(self):
        return '{0} {1}'.format(self.id,self.json)

    def update(self):
        try:
            self.json = json.dumps(self.item.__dict__)
        except Exception,err:
            logging.error(err.message)


class Captor:
    def __init__(self):
        self.items = []

    def attach(self,item):
        self.items.append(Capsy(item))
        self.update()

    def update(self):
        for item in self.items:
            item.update()
        session.commit()


Base.metadata.create_all(engine)

class TestClass():
    def __init__(self,name,age):
        self.name = name
        self.age = age

# newclass = TestClass('Rizki',30)
# newclass2 = TestClass('Perdana',40)
#
# captor = Captor()
# captor.attach(newclass)
# captor.attach(newclass2)
# captor.update()

import json
def listDocument():
    try:
        res = session.query(Capsy).all()
        return [json.loads(x.json) for x in res]
    except Exception,err:
        logging.error(err.message)

