# -*- coding: utf-8 -*-

from threading import Thread, Lock
from time import sleep

from .base import SchedulerMixin


class Scheduler(SchedulerMixin, Thread):
    """
    Threading scheduler.
    """

    def sleep(self, seconds):
        if seconds == 0:
            return
        sleep(seconds)
    
    def return_callback(self, *args):
        with Lock():
            return self.callback(*args)

    def run(self):
        self.start_loop()
