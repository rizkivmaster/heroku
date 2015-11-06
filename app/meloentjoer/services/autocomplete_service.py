import logging
from app.meloentjoer.accessors import bus_route_accessor
from app.meloentjoer.common import general_scheduler
from app.meloentjoer.common.util.TrieNode import TrieNode
from app.meloentjoer.config import general_config

__trie = TrieNode()
__logger = logging.getLogger('autocomplete_service')


def __update():
    try:
        route_list = bus_route_accessor.get_all_bus_routes()
        word_pool = set()
        for route in route_list:
            stations = route.stations
            for station in stations:
                word_pool.add(station)
        for word in word_pool:
            add_keyword(word, word)
        __logger.info('Autocomplete refreshed successfully')
    except Exception, e:
        __logger.error('AutoComplete service failed to refresh')
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
    return word_list


def stop():
    __scheduler.stop()


def start():
    __scheduler.start()
