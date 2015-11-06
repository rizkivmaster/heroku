from app.meloentjoer.controllers.main_controller import MeloentjoerController
from app.meloentjoer.fetcher.geo.TransportationFetcher import TransportationFetcher
from app.meloentjoer.search.AutocompleteService import AutocompleteService
from app.meloentjoer.search.SearchService import SearchService
from app.meloentjoer.search.TransportationGraphBuilder import TransportationGraphBuilder
from app.meloentjoer.tracking.BuswayDataExtractionService import BuswayDataExtractionService
from app.meloentjoer.accessors.geo_data.GeoDataAccessor import station_location, default_threshold
from app.meloentjoer.config.GeneralConfig import common_config
from flask import Flask


class MeloentjoerApp(object):
    def __init__(self):
        self.common_config = common_config
        self.bus_routes = TransportationFetcher().get_busway_routes()
        self.busway_data_extraction_service = BuswayDataExtractionService(
            station_location,
            default_threshold,
            self.bus_routes)
        self.transportation_networks = TransportationGraphBuilder().generate_realtime_graph()

        # services
        self.search_service = SearchService(self.transportation_networks, self.busway_data_extraction_service)
        self.autocomplete_service = AutocompleteService()

        # controllers
        self.meloentjoer_controller = \
            MeloentjoerController(
                self.common_config,
                self.search_service,
                self.autocomplete_service
            )

    def run(self):
        runner = Flask(__name__)
        runner.logger.info('Loading meloentjoer')
        runner.register_blueprint(self.meloentjoer_controller.meloentjoer, url_prefix='/meloentjoer')
