import logging

logging.basicConfig(filename='mj.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
__logger = logging.getLogger()
# ch = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# __logger.addHandler(ch)


def error(message):
    __logger.error(message)


def info(message):
    __logger.info(message)
