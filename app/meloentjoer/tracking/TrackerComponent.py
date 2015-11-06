__author__ = 'traveloka'

from app.meloentjoer.accessors.eta_estimates import CachedBusEstimationAccessor
from app.meloentjoer.config.GeneralConfig import postgres_config

busETAEstimator = CachedBusEstimationAccessor(postgres_config.get_database_url())
