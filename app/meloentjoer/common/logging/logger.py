import logging

__logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
__logger.addHandler(ch)


def error(message):
    __logger.error(message)


def info(message):
    __logger.info(message)
