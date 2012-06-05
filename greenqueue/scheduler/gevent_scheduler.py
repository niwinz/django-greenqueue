# -*- coding: utf-8 -*-

from gevent import Greenlet
from gevent import sleep

from .base import SchedulerMixin


class Scheduler(SchedulerMixin, Greenlet):
    """
    Gevent scheduler. Only replaces the sleep method for correct
    context switching.
    """

    def sleep(self, seconds):
        sleep(seconds)

    def return_callback(self, *args):
        return self.callback(*args)

    def _run(self):
        self.start_loop()
