# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.timezone import now

import logging, os, threading, datetime
log = logging.getLogger('greenqueue')

from greenqueue.utils import Singleton

from .base import BaseService
from .. import settings, shortcuts


class ZMQService(BaseService):
    socket = None

    def __init__(self):
        super(ZMQService, self).__init__()

    def lock(self):
        _lock = getattr(self, '_lock', None)
        if _lock is None:
            _lock = import_module("threading").Lock()

        _lock.acquire()
        setattr(self, '_lock', _lock)

    def unlock(self):
        _lock = getattr(self, '_lock', None)
        if _lock is None:
            raise ImproperlyConfigured("Can not release now created lock")
        
        _lock.release()

    def start(self):
        self.manager = shortcuts.load_worker_class().instance()
        if self.manager.greenlet:
            zmq = import_module("gevent_zeromq").zmq
        else:
            zmq = import_module('zmq')

        self.manager.start()

        ctx = zmq.Context.instance()

        socket = ctx.socket(zmq.PULL)
        socket.connect(settings.GREENQUEUE_BIND_ADDRESS)
        
        log.info(u"greenqueue: now connected to {address}. (pid {pid})".format(
            address = settings.GREENQUEUE_BIND_ADDRESS, 
            pid = os.getpid()
        ))

        while True:
            message = socket.recv_pyobj()
            ok, name = self.validate_message(message)
            if not ok:
                log.error("greenqueue: ignoring invalid message")
                continue

            self.manager.handle_message(name, message)

    def create_socket(self):
        zmq = import_module('zmq')
        ctx = zmq.Context.instance()

        self.socket = ctx.socket(zmq.PUSH)
        self.socket.bind(settings.GREENQUEUE_BIND_ADDRESS)

    def send(self, name, args=[], kwargs={}, eta=None, countdown=None):
        new_uuid = self.create_new_uuid()

        self.lock()
        if self.socket is None:
            self.create_socket()
        
        message_object = {
            'name': name, 
            'args': args, 
            'kwargs':kwargs,
            'uuid': new_uuid,
        }

        if eta is not None:
            message_object['eta'] = eta.isoformat()
        elif countdown is not None:
            eta = now() + datetime.timedelta(seconds=countdown)
            message_object['eta'] = eta.isoformat()
        
        self.socket.send_pyobj(message_object)
        self.unlock()
        return new_uuid
