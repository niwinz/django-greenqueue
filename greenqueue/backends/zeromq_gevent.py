# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

import logging, os, importlib
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
        return importlib.import_module("gevent_zeromq").zmq

    def load_gevent_patches(self):
        # this method not works with django >= 1.4
        if not self.patched:
            monkey = importlib.import_module('.monkey', 'gevent')
            monkey.patch_all()
            self.patched = True

    def start(self):
        # load all modules
        #self.load_gevent_patches()
        self.load_modules()

        self.pool = importlib.import_module('.pool', 'gevent')\
            .Pool(settings.GREENQUEUE_BACKEND_POOLSIZE)
        
        ctx = self.zmq.Context.instance()
        socket = ctx.socket(self.zmq.PULL)
        socket.connect(settings.GREENQUEUE_BIND_ADDRESS)
        
        log.info(u"greenqueue: now connected to {address}. (pid {pid})".format(
            address = settings.GREENQUEUE_BIND_ADDRESS, 
            pid = os.getpid()
        ))

        while True:
            message = socket.recv_pyobj()
            self.handle_message(message)

    def process_callable(self, uuid, _callable, args, kwargs):
        def _greenlet():
            result = _callable(*args, **kwargs)
            self.storage.save(uuid, result)

        self.pool.spawn(_greenlet)

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
