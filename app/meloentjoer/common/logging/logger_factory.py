import logging


class Logger(object):
    def __init__(self, name=None):
        """
        :type name: str
        :param name:
        :return:
        """
        self.__logger = logging.getLogger(name)
        channel = logging.FileHandler(filename='mj.log', mode='a')
        self.__logger.addHandler(channel)
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - {0} - %(message)s'.format(name))
        channel.setFormatter(formatter)
        self.__channel = channel

    def error(self, message):
        self.__logger.error(message)

    def info(self, message):
        self.__logger.info(message)

    def debug(self, message):
        self.__logger.debug(message)


def create_logger(name):
    return Logger(name)
