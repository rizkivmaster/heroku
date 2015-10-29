__author__ = 'traveloka'

from app.meloentjoer.tracker.ChacedBusETAEstimator import CachedBusETAEstimator
from app.meloentjoer.config.Configs import postgres_config

busETAEstimator = CachedBusETAEstimator(postgres_config.get_database_url())
