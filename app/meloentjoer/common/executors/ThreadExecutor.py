from app.meloentjoer.common.executors.PoolExecutor import PoolExecutor
from app.meloentjoer.config.GeneralConfig import GeneralConfig
from thread_executor.futures.thread import ThreadPoolExecutor


class ThreadExecutor(PoolExecutor):

    def __init__(self, config):
        """
        :type config: GeneralConfig
        :param config:
        :return:
        """
        self.executor = ThreadPoolExecutor(32)

    def shutdown(self):
        self.executor.shutdown()

    def submit(self, f):
        self.executor.submit(f)

