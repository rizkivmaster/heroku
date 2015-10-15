__author__ = 'traveloka'
from app.common.PostgreBase import Base, PostgresAccessorBase, Column, String, Float


class BusETAEstimator:
    def __init__(self):
        self.estimator_dictionary = dict()

    def get_key(self, origin, destination):
        return "{0}_{1}".format(origin, destination)

    def add_sample(self, origin, destination, delta):
        key = self.get_key(origin, destination)
        delta = float(delta)
        if key in self.estimator_dictionary:
            delta_mean, sample_size = self.estimator_dictionary[key]
            new_delta_mean = (delta+(sample_size*delta_mean))/(sample_size+1)
            self.estimator_dictionary[key] = (new_delta_mean, sample_size+1)
        else:
            self.estimator_dictionary[key] = (delta, 1)

    # params: station name:String, station name:string
    # return: seconds prediction (float)
    def predict_eta(self, origin, destination):
        key = self.get_key(origin, destination)
        if key in self.estimator_dictionary:
            estimator = self.estimator_dictionary[key]
            return int(estimator[0])
        else:
            return None


class BusEstimation(Base):

    __tablename__ = 'BusEstimation'
    id = Column(String, primary_key=True)
    eta = Column(Float)

    def __init__(self, id, eta):
        self.id = id
        self.eta = eta


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

    def get_all_bus_estimates(self):
        return self.query(BusEstimation).all()


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
        prediction = super(CachedBusETAEstimator, self).predict_eta(origin, destination)
        if prediction is None:
            prediction = self.bus_estimation_accessor.get_bus_estimate(id)
            if prediction is not None:
                self.estimator_dictionary[id] = (prediction.eta, 1)



