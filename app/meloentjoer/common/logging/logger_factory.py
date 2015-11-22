import logging
import traceback
import sys


class Logger(object):
    def __init__(self, name=None):
        """
        :type name: str
        :param name:
        :return:
        """
        logging.basicConfig(filename='mj.log',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - {0} - %(message)s'.format(name))
        self.__logger = logging.getLogger(name)
        # create console handler and set level to debug

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - {0} - %(message)s'.format(name))
        ch.setFormatter(formatter)
        self.__logger.addHandler(ch)

    def error(self, message):
        self.__logger.error(message)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

    def info(self, message):
        self.__logger.info(message)

    def debug(self, message):
        self.__logger.debug(message)


def create_logger(name):
    return Logger(name)
