__author__ = 'rizkivmaster'
from sqlalchemy import String, Date, BigInteger, create_engine, ForeignKey, Column, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

database_url = os.environ['DATABASE_URL']
print('DATABASE URL: ' +database_url)
engine = create_engine(database_url, echo=True)

Base = declarative_base()

class Record(Base):
    __tablename__ = 'records'
    date = Column(Date)
    accountingId = Column(String, primary_key=True)
    accountingPost = Column(String)
    accountingType = Column(String)
    notes = Column(String)
    amount = Column(BigInteger)

    def __init__(self,date=None,accountingId=None,accountingPost=None,accountingType=None,notes=None,amount=None):
        self.date = date
        self.accountingPost = accountingPost
        self.accountingId = accountingId
        self.accountingType = accountingType
        self.notes = notes
        self.amount = amount

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
recordSession = Session()

class RecordAccessor:
    def addRecord(self,record):
        recordSession.add(record)
        recordSession.commit()

    def removeRecord(self,record):
        result = recordSession.query(Record).filter(Record.accountingId==record.accountingId).first()
        recordSession.delete(result)
        recordSession.commit()

    def getRecordById(self,accountingId):
        result = recordSession.query(Record).filter(Record.accountingId==accountingId).first()
        return result

    def updateRecord(self,record):
        recordSession.commit()

    def getAllRecords(self,accountingPost=None):
        if(accountingPost):
            return recordSession.query(Record).filter(Record.accountingPost==accountingPost).order_by(desc(Record.date)).all()
        else:
            return  recordSession.query(Record).order_by(desc(Record.date)).all()

recordAccessor = RecordAccessor()