import unittest

from app.meloentjoer.test.AccessorTest import AccessorTest
from app.meloentjoer.test.FetcherTest import FetcherTest
from app.meloentjoer.test.ServiceTest import ServiceTest

test_suite = unittest.TestSuite()
test_suite.addTest(AccessorTest())
test_suite.addTest(ServiceTest())
test_suite.addTest(FetcherTest())
test_suite.run()
