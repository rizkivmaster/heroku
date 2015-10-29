from app.meloentjoer.common.PostgreBase import PostgresAccessorBase
from app.meloentjoer.tracker.util.BusEstimation import BusEstimation


class BusEstimationAccessor(PostgresAccessorBase):

    def __init__(self, database_url):
        super(BusEstimationAccessor, self).__init__(BusEstimation, database_url)

    def get_bus_estimate(self, id):
        return self.query(BusEstimation).filter(BusEstimation.id == id).first()

    def upsert_bus_estimate(self, id, eta):
        bus_estimate = self.get_bus_estimate(id)
        if bus_estimate is None:
            self.add(BusEstimation(id, eta))
        else:
            bus_estimate.eta = eta
        self.commit()

    def get_all_bus_estimates(self):
        return self.query(BusEstimation).all()