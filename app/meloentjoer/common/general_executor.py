from app.meloentjoer.common.executors.SchedulerExecutor import SchedulerExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from app.meloentjoer.config import general_config

executor = ThreadPoolExecutor(general_config.get_thread_size())


def submit(func):
    executor.submit(func)


def shutdown():
    executor.shutdown()


def schedule(period, task):
    return SchedulerExecutor(period, task)
