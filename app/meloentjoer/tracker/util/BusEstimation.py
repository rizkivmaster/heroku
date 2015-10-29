from app.meloentjoer.common.ModelBase import ModelBase
from sqlalchemy import Column, String, Float


class BusEstimation(ModelBase):
    __tablename__ = 'BusEstimation'
    id = Column(String, primary_key=True)
    eta = Column(Float)

    def __init__(self, id, eta):
        super(BusEstimation, self).__init__()
        self.id = id
        self.eta = eta
