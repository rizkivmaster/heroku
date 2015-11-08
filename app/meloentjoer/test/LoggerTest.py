import unittest
from app.meloentjoer.common.logging import logger_factory


class LoggerTest(unittest.TestCase):
    def test_logger_factory(self):
        __logger = logger_factory.create_logger('hahahihi')
        __logger.info('test')
