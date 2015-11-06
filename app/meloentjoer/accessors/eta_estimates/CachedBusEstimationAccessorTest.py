import unittest

from app.meloentjoer.config.GeneralConfig import GeneralConfig
from app.meloentjoer.accessors.eta_estimates.BusEstimationPostgresAccessorImpl import BusEstimationProsgresAccessorImpl
from CachedBusEstimationAccessor import CachedBusEstimationAccessor
from concurrent.futures import ThreadPoolExecutor


class Tester(unittest.TestCase):
    def testAccessor(self):
        executor = ThreadPoolExecutor(4)
        database_url = GeneralConfig().get_database_url()
        bus_estimation_accessor = BusEstimationProsgresAccessorImpl(database_url)
        bus_estimation_accessor.reset_database()
        accessor = CachedBusEstimationAccessor(bus_estimation_accessor, executor)
        accessor.start()
        accessor.add_sample('jalan1', 'jalan2', 90)
        real_value = accessor.predict_eta('jalan1', 'jalan2')
        self.assertEqual(real_value, 90)
        accessor.add_sample('jalan1', 'jalan2', 10)
        real_value = accessor.predict_eta('jalan1', 'jalan2')
        self.assertEqual(real_value, 50)
        accessor.stop()
        executor.shutdown()


if __name__ == '__main__':
    unittest.main()
