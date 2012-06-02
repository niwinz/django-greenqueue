# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

import logging, os, threading
log = logging.getLogger('greenqueue')

from greenqueue.utils import Singleton

from .base import BaseService
from .. import settings, shortcuts


class ZMQService(BaseService):
    socket = None

    def __init__(self):
        super(ZMQService, self).__init__()
        self.manager = shortcuts.load_worker_class().instance()

    @property
    def zmq(self):
        if self.manager.greenlet:
            return import_module("gevent_zeromq").zmq
        return import_module('zmq')

    def lock(self):
        if self.manager.greenlet:
            return
        
        _lock = getattr(self, '_lock', None)
        if _lock is None:
            _lock = import_module("threading").Lock()

        _lock.acquire()
        setattr(self, '_lock', _lock)

    def unlock(self):
        if self.manager.greenlet:
            return 

        _lock = getattr(self, '_lock', None)
        if _lock is None:
            raise ImproperlyConfigured("Can not release now created lock")
        
        _lock.release()

    def start(self):
        self.manager.start()
        ctx = self.zmq.Context.instance()
        socket = ctx.socket(self.zmq.PULL)
        socket.connect(settings.GREENQUEUE_BIND_ADDRESS)
        
        log.info(u"greenqueue: now connected to {address}. (pid {pid})".format(
            address = settings.GREENQUEUE_BIND_ADDRESS, 
            pid = os.getpid()
        ))

        while True:
            message = socket.recv_pyobj()
            self.manager.handle_message(message)

    def create_socket(self):
        ctx = self.zmq.Context.instance()
        self.socket = ctx.socket(self.zmq.PUSH)
        self.socket.bind(settings.GREENQUEUE_BIND_ADDRESS)

    def send(self, name, args=[], kwargs={}):
        new_uuid = self.create_new_uuid()

        self.lock()
        if self.socket is None:
            self.create_socket()
        
        self.socket.send_pyobj({
            'name': name, 
            'args': args, 
            'kwargs':kwargs,
            'uuid': new_uuid,
        })
        self.unlock()
        return new_uuid
