from BusEstimationPostgresAccessorImpl import BusEstimationProsgresAccessorImpl
from app.meloentjoer.common.behavioral.Cacheable import Cacheable
from app.meloentjoer.common.executors.SchedulerExecutor import SchedulerExecutor
from app.meloentjoer.common.behavioral.Startable import Startable
from BusEstimationAccessor import BusEstimationAccessor
from app.meloentjoer.tracking.util.BusEstimation import BusEstimation


class CachedBusEstimationAccessor(BusEstimationAccessor, Startable, Cacheable):
    def refresh(self):
        all_prediction = self.bus_estimation_accessor.get_all_bus_estimates()
        for prediction in all_prediction:
            assert isinstance(prediction, BusEstimation)
            estimation_source = prediction.source
            estimation_destination = prediction.destination
            estimation_eta = prediction.eta
            self.__add_sample(
                estimation_source,
                estimation_destination,
                estimation_eta
            )

    def __init__(self, bus_estimation_accessor, executor):
        """
        :type bus_estimation_accessor: BusEstimationProsgresAccessorImpl
        :param bus_estimation_accessor:
        :param executor:
        :return:
        """
        super(CachedBusEstimationAccessor, self).__init__()
        self.bus_estimation_accessor = bus_estimation_accessor
        self.update_period = 10
        self.estimator_dictionary = dict()
        self.scheduler = SchedulerExecutor(executor, self.update_period, self.refresh)

    def __add_sample(self, origin, destination, delta):
        """

        :param origin:
        :param destination:
        :param delta:
        :return:
        """
        added = BusEstimation(origin, destination, delta)
        key = added.id
        delta = float(delta)
        if key in self.estimator_dictionary:
            delta_mean, sample_size = self.estimator_dictionary[key]
            new_delta_mean = (delta + (sample_size * delta_mean)) / (sample_size + 1)
            self.estimator_dictionary[key] = (new_delta_mean, sample_size + 1)
        else:
            self.estimator_dictionary[key] = (delta, 1)

    def __predict_eta(self, origin, destination):
        """
        :type origin: str
        :type destination: str
        :param origin:
        :param destination:
        :return:
        """
        predicted = BusEstimation(origin, destination, None)
        key = predicted.id
        if key in self.estimator_dictionary:
            estimator = self.estimator_dictionary[key]
            return int(estimator[0])
        else:
            return None

    def add_sample(self, origin, destination, delta):
        self.__add_sample(origin, destination, delta)
        average_eta = self.__predict_eta(origin, destination)
        self.bus_estimation_accessor.upsert_bus_estimate(origin, destination, average_eta)

    def predict_eta(self, origin, destination):
        eta = self.__predict_eta(origin, destination)
        return eta

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.stop()
