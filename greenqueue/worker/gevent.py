# -*- coding: utf-8 -*-

from .base import BaseWorker, BaseManager
from .. import settings

from gevent import Greenlet
from gevent.event import Event
from gevent.queue import Queue


class Worker(BaseWorker):
    def _name(self):
        return self.greenlet_name

    def set_name(self, name):
        self.greenlet_name = name


class GreenletManager(BaseManager):
    greenlet = True
    process_list = []

    def __init__(self):
        super(ProcessManager, self).__init__()
        self.stop_event = Event()
        self.work_queue = Queue(settings.GREENQUEUE_BACKEND_TASKBUFF)

    def start_greenlet_pool(self):
        for i in xrange(settings.GREENQUEUE_BACKEND_POOLSIZE):
            log.info("greenqueue: starting worker process {0}".format(i))

            worker = Worker(self.work_queue, self.stop_event)
            worker.set_name("greenlet-{0}".format(i))

            g = Greenlet.spawn(worker)
            self.process_list.append(p)

    def start(self):
        self.start_greenlet_pool()

    def _handle_message(self, name, uuid, args, kwargs):
        self.work_queue.put((name, uuid, args, kwargs), block=True)

    def close(self):
        self.stop_event.set()

