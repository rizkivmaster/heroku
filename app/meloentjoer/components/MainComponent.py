from app.meloentjoer.accessors.bus_routes.BusRoutePostgresAccessorImpl import BusRoutePostgresAccessorImpl
from app.meloentjoer.accessors.bus_states.BusStateAccessorImpl import BusStatePostgresAccessorImpl
from app.meloentjoer.accessors.eta_estimates.BusEstimationPostgresAccessorImpl import BusEstimationProsgresAccessorImpl
from app.meloentjoer.accessors.eta_estimates.CachedBusEstimationAccessor import CachedBusEstimationAccessor
from app.meloentjoer.accessors.geo_data.GeoDataAccessor import GeoDataAccessor
from app.meloentjoer.accessors.next_buses.BusNextStopAccessorImpl import BusNextStopAccessorImpl
from app.meloentjoer.common.behavioral.Startable import Startable
from app.meloentjoer.common.executors.ThreadExecutor import ThreadExecutor
from app.meloentjoer.config.GeneralConfig import GeneralConfig
from app.meloentjoer.fetcher.geo.TransportationFetcher import TransportationFetcher
from app.meloentjoer.fetcher.track.BusWayTrackFetcher import BusWayTrackFetcher
from app.meloentjoer.services.autocomplete.AutocompleteServiceImpl import AutocompleteServiceImpl
from app.meloentjoer.services.search.SearchServiceImpl import SearchServiceImpl


class MainComponent(Startable):
    def __init__(self):
        self.config = GeneralConfig()
        self.pool_executor = ThreadExecutor(self.config)

        self.bus_route_accessor = BusRoutePostgresAccessorImpl(self.config)
        self.bus_state_accessor = BusStatePostgresAccessorImpl()
        postgres_bus_estimation_accessor = BusEstimationProsgresAccessorImpl(self.config)
        self.bus_estimation_accessor = CachedBusEstimationAccessor(postgres_bus_estimation_accessor, self.pool_executor)
        self.geo_data_accessor = GeoDataAccessor()
        self.next_bus_accessor = BusNextStopAccessorImpl()

        self.transportation_fetcher = TransportationFetcher(self.pool_executor,
                                                            self.bus_route_accessor,
                                                            self.config)
        self.busway_track_fetcher = BusWayTrackFetcher(self.pool_executor, self.bus_estimation_accessor,
                                                       self.bus_state_accessor, self.next_bus_accessor,
                                                       self.geo_data_accessor, self.bus_route_accessor, self.config)

        self.autocomplete_service = AutocompleteServiceImpl(self.pool_executor, self.bus_route_accessor, self.config)
        self.search_service = SearchServiceImpl(self.bus_route_accessor, self.bus_estimation_accessor,
                                                self.next_bus_accessor, self.config)

