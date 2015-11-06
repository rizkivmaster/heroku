import logging

from app.meloentjoer.accessors.bus_routes.BusRouteAccessor import BusRouteAccessor
from app.meloentjoer.common.behavioral.Startable import Startable
from app.meloentjoer.common.executors.PoolExecutor import PoolExecutor
from app.meloentjoer.common.executors.SchedulerExecutor import SchedulerExecutor
from app.meloentjoer.common.util.TrieNode import TrieNode
from app.meloentjoer.config.GeneralConfig import GeneralConfig
from app.meloentjoer.services.autocomplete.AutocompleteService import Autocomplete


class AutocompleteServiceImpl(Autocomplete, Startable):
    def __update(self):
        try:
            route_list = self.bus_routes_accessor.get_all_bus_routes()
            word_pool = set()
            for route in route_list:
                stations = route.stations
                for station in stations:
                    word_pool.add(station)
            for word in word_pool:
                self.add_keyword(word, word)
            self.logger.info('Autocomplete refreshed successfully')
        except Exception, e:
            self.logger.error('AutoComplete service failed to refresh')
            self.logger.error(e)

    def __init__(self,
                 executor,
                 bus_routes_accessor,
                 config,
                 ):
        """
        :type executor: PoolExecutor
        :type bus_routes_accessor: BusRouteAccessor
        :type config: GeneralConfig
        :param executor:
        :param bus_routes_accessor:
        :return:
        """
        self.bus_routes_accessor = bus_routes_accessor
        self.scheduler = SchedulerExecutor(executor,
                                           config.get_autocomplete_refresh_period(),
                                           self.__update)
        self.trie = TrieNode()
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_keyword(self, word, key):
        """
        :type word: str
        :type key: str
        :param word:
        :param key:
        :return:
        """
        self.trie.add_word(word, key)

    def get_words(self, key):
        """
        :type key:str
        :param key:
        :return:
        :rtype: list[str]
        """
        word_list = self.trie.dfs(key)
        return word_list

    def stop(self):
        self.scheduler.stop()

    def start(self):
        self.scheduler.start()
