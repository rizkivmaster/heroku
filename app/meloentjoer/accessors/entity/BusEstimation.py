from app.meloentjoer.common.databases.ModelBase import ModelBase
from sqlalchemy import Column, String, Float


class BusEstimation(ModelBase):
    __tablename__ = 'BusEstimation'
    id = Column(String, primary_key=True)
    eta = Column(Float)
    source = Column(String, nullable=True)
    destination = Column(String, nullable=True)

    def __key(self, source, destination):
        """
        :type source: str
        :type destination: str
        :param source:
        :param destination:
        :return:
        """
        return '{0}_{1}'.format(source, destination)

    def __init__(self, source, destination, eta):
        super(BusEstimation, self).__init__()
        self.source = source
        self.destination = destination
        self.id = self.__key(source, destination)
        self.eta = eta
