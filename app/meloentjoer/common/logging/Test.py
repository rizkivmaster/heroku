import unittest

from Logger import Logger


class Test(unittest.TestCase):
    def test_Logger(self):
        logger = Logger(self)
        logger.info('test')
        logger.error('test')
