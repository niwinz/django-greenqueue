# -*- coding: utf-8 -*-

from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
from gevent import Greenlet
from gevent import sleep

import heapq


class Scheduler(Greenlet):
    sched_list = []
    callback = None

    def __init__(self, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback
        super(Scheduler, self).__init__()

    def push_task(self, eta, task):
        heapq.heappush(self.sched_list, (eta, task))
        sleep(0) # explicit context switch

    def _run(self):
        while not self.stop_event.is_set():
            try:
                eta, task = heapq.heappop(self.sched_list)
            except IndexError:
                sleep(1)
                continue

            now_dt = now()

            if now_dt < eta:
                sleep((eta-now_dt).seconds)
            
            self.callback(*task)
