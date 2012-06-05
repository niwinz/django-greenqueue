# -*- coding: utf-8 -*-

from django.utils.timezone import now
import heapq


class SchedulerMixin(object):
    sched_list = []
    callback = None

    def __init__(self, stop_event, callback):
        self.stop_event = stop_event
        self.callback = callback
        super(SchedulerMixin, self).__init__()

    def sleep(self, seconds):
        raise NotImplementedError

    def push_task(self, eta, task):
        heapq.heappush(self.sched_list, (eta, task))
        self.sleep(0)

    def return_callback(self, *args):
        raise NotImplementedError

    def start_loop(self):
        while not self.stop_event.is_set():
            try:
                eta, task = heapq.heappop(self.sched_list)
            except IndexError:
                self.sleep(1)
                continue

            now_dt = now()
            if now_dt < eta:
                self.sleep((eta-now_dt).seconds)

            self.return_callback(*task)



