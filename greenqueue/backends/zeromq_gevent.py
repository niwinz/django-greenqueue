# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

import logging, os
log = logging.getLogger('greenqueue')

from greenqueue.utils import Singleton

from .base import BaseService
from .. import settings


class ZMQService(BaseService):
    patched = False

    def __init__(self):
        super(ZMQService, self).__init__()
        self.socket = None
    
    @property
    def zmq(self):
        return import_module('zmq', 'gevent_zeromq')

    def load_gevent_patches(self):
        if not self.patched:
            monkey = importlib.import_module('monkey', 'gevent')
            monkey.patch_all()
            self.patched = True

    def start(self):
        # load all modules
        self.load_gevent_patches()
        self.load_modules()

        self.pool = importlib.import_module('pool', 'gevent')\
            .Pool(settings.GREENQUEUE_BACKEND_POOLSIZE)
        
        ctx = self.zmq.Context.instance()
        socket = ctx.socket(self.zmq.PULL)
        socket.bind(settings.GREENQUEUE_BIND_ADDRESS)

        log.info("greenqueue: now listening on %s. (pid %s)",
            settings.GREENQUEUE_BIND_ADDRESS, os.getpid())

        # recv loop
        while True:
            message = self.socket.recv_pyobj()
            self.handle_message(message)

    def close(self):
        if self.socket is not None:
            self.socket.close()

    def process_callable(self, uuid, _callable, args, kwargs):
        self.pool.spawn(_callable, *args, **kwargs)
        self.storage.save(uuid, result)

    def create_socket(self):
        ctx = self.zmq.Context.instance()
        self.socket = ctx.socket(self.zmq.PUSH)
        self.socket.bind(settings.GREENQUEUE_BIND_ADDRESS)

    def send(self, name, args=[], kwargs={}):
        if self.socket is None:
            self.create_socket()

        new_uuid = self.create_new_uuid()

        self.socket.send_pyobj({
            'name': name, 
            'args': args, 
            'kwargs':kwargs,
            'uuid': new_uuid,
        })

        return new_uuid
