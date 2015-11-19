from app.meloentjoer.accessors.routes import bus_route_accessor
from app.meloentjoer.common import general_scheduler
from app.meloentjoer.common.logging import logger_factory
from app.meloentjoer.common.util.TrieNode import TrieNode
from app.meloentjoer.config import general_config

__logger = logger_factory.create_logger('autocomplete_service')
__logger.info('Starting Autocomplete Service')
__trie = TrieNode()


def __update():
    try:
        __logger.info('Updating Autocomplete Service')
        route_list = bus_route_accessor.get_all_bus_routes()
        word_pool = set()
        for route in route_list:
            stations = route.stations
            for station in stations:
                word_pool.add(station)
        for word in word_pool:
            add_keyword(word, word)
    except Exception, e:
        __logger.error('Autocomplete Service failed to refresh')
        __logger.error(e)


__scheduler = general_scheduler.schedule(general_config.get_autocomplete_refresh_period(), __update)


def add_keyword(word, key):
    """
    :type word: str
    :type key: str
    :param word:
    :param key:
    :return:
    """
    __trie.add_word(word, key)


def get_words(key):
    """
    :type key:str
    :param key:
    :return:
    :rtype: list[str]
    """
    word_list = __trie.dfs(key)
    return list(word_list)


def start():
    __update()
    __scheduler.start()


def stop():
    __logger.info('Stopped')
    __scheduler.stop()
