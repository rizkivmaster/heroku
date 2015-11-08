from app.meloentjoer.accessors.entity.BusEstimation import BusEstimation
from app.meloentjoer.common import general_scheduler
from app.meloentjoer.common.databases.PostgreBase import PostgresAccessorBase
from app.meloentjoer.common.logging import logger as __logger
from app.meloentjoer.config import general_config

__bus_estimate_session = PostgresAccessorBase(BusEstimation, general_config.get_database_url())
__estimator_cache = dict()


def __refresh():
    __logger.info('Updating Bus Estimation cache')
    all_prediction = __get_all_bus_estimates()
    for prediction in all_prediction:
        assert isinstance(prediction, BusEstimation)
        estimation_source = prediction.source
        estimation_destination = prediction.destination
        estimation_eta = prediction.eta
        __add_sample(
            estimation_source,
            estimation_destination,
            estimation_eta
        )


__scheduler = general_scheduler.schedule(general_config.get_eta_refresh_period(), __refresh)


# database part
def __get_all_bus_estimates():
    return __bus_estimate_session.query(BusEstimation).all()


def __get_bus_estimate(source, destination):
    """
    :type source: str
    :type destination: str
    :param source:
    :param destination:
    :return:
    """
    searched = BusEstimation(source, destination, None)
    return __bus_estimate_session.query(BusEstimation).filter(BusEstimation.id == searched.id).first()


def __upsert_bus_estimate(source, destination, eta):
    """
    :type source: str
    :type destination: str
    :type eta: float
    :param source:
    :param destination:
    :param eta:
    :return:
    """
    bus_estimate = __get_bus_estimate(source, destination)
    if bus_estimate is None:
        __bus_estimate_session.add(BusEstimation(source, destination, eta))
    else:
        bus_estimate.eta = eta
    __bus_estimate_session.commit()


def __reset():
    __bus_estimate_session.query(BusEstimation).delete()
    __bus_estimate_session.commit()


# logic part
def __add_sample(origin, destination, delta):
    """

    :param origin:
    :param destination:
    :param delta:
    :return:
    """
    added = BusEstimation(origin, destination, delta)
    key = added.id
    delta = float(delta)
    if key in __estimator_cache:
        delta_mean, sample_size = __estimator_cache[key]
        new_delta_mean = (delta + (sample_size * delta_mean)) / (sample_size + 1)
        __estimator_cache[key] = (new_delta_mean, sample_size + 1)
    else:
        __estimator_cache[key] = (delta, 1)


def __predict_eta(origin, destination):
    """
    :type origin: str
    :type destination: str
    :param origin:
    :param destination:
    :return:
    """
    predicted = BusEstimation(origin, destination, None)
    key = predicted.id
    if key in __estimator_cache:
        estimator = __estimator_cache[key]
        return int(estimator[0])
    else:
        return None


# public part
def add_sample(origin, destination, delta):
    __add_sample(origin, destination, delta)
    average_eta = __predict_eta(origin, destination)
    __upsert_bus_estimate(origin, destination, average_eta)


def predict_eta(origin, destination):
    eta = __predict_eta(origin, destination)
    return eta


def reset():
    __estimator_cache.clear()
    __reset()


def start():
    __refresh()
    __scheduler.start()


def stop():
    __scheduler.stop()
