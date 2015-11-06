import time

from app.meloentjoer.common import general_executor

from app.meloentjoer.common.exceptions.AlreadyRunException import AlreadyRunException


class SchedulerExecutor(object):
    def __init__(self, period, task):
        self.period = period
        self.task = task
        self.isOff = True

    def start(self):
        if self.isOff:
            self.isOff = False

            def routine():
                while not self.isOff:
                    self.task()
                    time.sleep(self.period)

            general_executor.submit(routine)
        else:
            raise AlreadyRunException('A process is still running')

    def stop(self):
        self.isOff = True

    def is_running(self):
        return not self.isOff
