import logging
from logging.handlers import BaseRotatingHandler

__logger = logging.getLogger('meloentjoer')
logging.basicConfig(level=logging.DEBUG)
__logger.addHandler(BaseRotatingHandler('mj.log', 'w'))

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
__logger.addHandler(ch)


def error(message):
    __logger.error(message)


def info(message):
    __logger.info(message)
