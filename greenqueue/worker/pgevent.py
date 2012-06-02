# -*- coding: utf-8 -*-

from .base import BaseWorker, BaseManager
from .. import settings

import gevent
from gevent import Greenlet
from gevent.event import Event
from gevent.queue import Queue

from Queue import Empty

import logging
log = logging.getLogger('greenqueue')



class Worker(BaseWorker):
    def _name(self):
        return self.greenlet_name

    def set_name(self, name):
        self.greenlet_name = name


class ACKWatcher(Greenlet):
    """
    This is a dummy ack watcher greenlet, because the zeromq backend not precise
    ack managment.
    """

    def __init__(self, queue, stop_event, callback):
        super(ACKWatcher, self).__init__()
        self.queue = queue
        self.stop_event = stop_event
        self.callback = callback

    def _run(self):
        while not self.stop_event.is_set():
            try:
                ack_uuid = self.queue.get(True, 1)
                self.callback(ack_uuid)
            except Empty:
                pass


class GreenletManager(BaseManager):
    greenlet = True
    process_list = []

    def __init__(self):
        super(GreenletManager, self).__init__()
        self.stop_event = Event()
        self.work_queue = Queue(settings.GREENQUEUE_BACKEND_TASKBUFF)
        self.ack_queue = Queue()

    def start_greenlet_pool(self):
        for i in xrange(settings.GREENQUEUE_BACKEND_POOLSIZE):
            log.info("greenqueue: starting worker process {0}".format(i))

            worker = Worker(self.work_queue, self.ack_queue, self.stop_event)
            worker.set_name("greenlet-{0}".format(i))

            g = Greenlet.spawn(worker)
            self.process_list.append(g)

    def start(self):
        # starts a dummy watcher, because zeromq is not need ack.
        self.watcher = ACKWatcher(self.ack_queue, self.stop_event, self._ack_callback)
        self.watcher.start()

        self.start_greenlet_pool()

    def _handle_message(self, name, uuid, args, kwargs):
        self.work_queue.put((name, uuid, args, kwargs), block=True)

    def close(self):
        self.stop_event.set()

