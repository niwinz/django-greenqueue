# -*- coding: utf-8 -*-


from .base import BaseWorker, BaseManager
from .. import settings

from multiprocessing import Process, Event, Queue, current_process

import logging
log = logging.getLogger('greenqueue')


class Worker(BaseWorker):
    def _name(self):
        return current_process().name


class ProcessManager(BaseManager):
    process_list = []

    def __init__(self):
        super(ProcessManager, self).__init__()
        self.stop_event = Event()
        self.work_queue = Queue(settings.GREENQUEUE_BACKEND_TASKBUFF)
        self.start_process_pool()

    def start_process_pool(self):
        for i in xrange(settings.GREENQUEUE_BACKEND_POOLSIZE):
            log.info("greenqueue: starting worker process {0}".format(i))

            p = Process(target=Worker(self.work_queue, self.stop_event))
            p.start()

            self.process_list.append(p)

    def _handle_message(self, name, uuid, args, kwargs):
        self.work_queue.put((name, uuid, args, kwargs), block=True)

    def close(self):
        self.stop_event.set()
