# -*- coding: utf-8 -*-


from .base import BaseWorker, BaseManager
from .. import settings

from multiprocessing import Process, Event, Queue, current_process
from threading import Thread, Lock()

import logging
log = logging.getLogger('greenqueue')


class Worker(BaseWorker):
    def _name(self):
        return current_process().name

class ACKWatcher(Thread):
    def __init__(self, queue, stop_event, callback):
        self.queue = queue
        self.stop_event = stop_event
        self.callback

    def run(self):
        while not self.stop_event.is_set():
            ack_uuid = self.queue.get(True)
            with Lock():
                self.callback(ack_uuid)


class ProcessManager(BaseManager):
    process_list = []

    def __init__(self):
        super(ProcessManager, self).__init__()
        self.stop_event = Event()
        self.work_queue = Queue(settings.GREENQUEUE_BACKEND_TASKBUFF)
        self.ack_queue = Queue()

    def start(self):
        self.watcher = ACKWatcher(self.ack_queue, self.stop_event, self._ack_callback)
        self.watcher.start()

        self.start_process_pool()

    def start_process_pool(self):
        for i in xrange(settings.GREENQUEUE_BACKEND_POOLSIZE):
            log.info("greenqueue: starting worker process {0}".format(i))
            
            # Create worker instance.
            w = Worker(self.work_queue, self.ack_queue, self.stop_event)

            # Start process with a worker callable instance.
            p = Process(target=w)
            p.start()

            self.process_list.append(p)

    def _handle_message(self, name, uuid, args, kwargs):
        self.work_queue.put((name, uuid, args, kwargs), block=True)

    def close(self):
        self.stop_event.set()
