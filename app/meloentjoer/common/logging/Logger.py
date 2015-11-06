import logging


class Logger(object):
    def __init__(self, clazz):
        self.logger = logging.getLogger(clazz.__class__.__name__)
        logging.basicConfig(level=logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

    def error(self,
              message):
        logging.error(message)

    def info(self,
             message):
        logging.info(message)
