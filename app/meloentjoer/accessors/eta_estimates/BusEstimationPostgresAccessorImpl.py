from app.meloentjoer.common.behavioral.Accessor import Accessor
from app.meloentjoer.common.databases.PostgreBase import PostgresAccessorBase
from app.meloentjoer.config.GeneralConfig import GeneralConfig
from app.meloentjoer.tracking.util.BusEstimation import BusEstimation


class BusEstimationProsgresAccessorImpl(PostgresAccessorBase, Accessor):
    def __init__(self, config):
        """
        :type config: GeneralConfig
        :param config:
        :return:
        """
        super(BusEstimationProsgresAccessorImpl, self).__init__(BusEstimation, config.get_database_url())

    def get_bus_estimate(self, source, destination):
        """
        :type source: str
        :type destination: str
        :param source:
        :param destination:
        :return:
        """
        searched = BusEstimation(source, destination, None)
        return self.query(BusEstimation).filter(BusEstimation.id == searched.id).first()

    def upsert_bus_estimate(self, source, destination, eta):
        """
        :type source: str
        :type destination: str
        :type eta: float
        :param source:
        :param destination:
        :param eta:
        :return:
        """
        bus_estimate = self.get_bus_estimate(source, destination)
        if bus_estimate is None:
            self.add(BusEstimation(source, destination, eta))
        else:
            bus_estimate.eta = eta
        self.commit()

    def get_all_bus_estimates(self):
        return self.query(BusEstimation).all()

    def reset_database(self):
        self.query(BusEstimation).delete()
        self.commit()
