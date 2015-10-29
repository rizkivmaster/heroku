from app.meloentjoer.tracker.BusETAEstimator import BusETAEstimator
from app.meloentjoer.tracker.BusEstimationAccessor import BusEstimationAccessor


class CachedBusETAEstimator(BusETAEstimator):
    def __init__(self, database_url):
        super(CachedBusETAEstimator, self).__init__()
        self.bus_estimation_accessor = BusEstimationAccessor(database_url)

    def add_sample(self, origin, destination, delta):
        super(CachedBusETAEstimator, self).add_sample(origin, destination, delta)
        average_eta = super(CachedBusETAEstimator, self).predict_eta(origin, destination)
        id = self.get_key(origin, destination)
        self.bus_estimation_accessor.upsert_bus_estimate(id, average_eta)

    def predict_eta(self, origin, destination):
        id = self.get_key(origin, destination)
        eta = super(CachedBusETAEstimator, self).predict_eta(origin, destination)
        if eta is not None:
            return eta
        prediction = self.bus_estimation_accessor.get_bus_estimate(id)
        if prediction is not None:
            self.estimator_dictionary[id] = (prediction.eta, 1)
            return prediction.eta
        return None