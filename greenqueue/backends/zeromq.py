# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

import logging, os
log = logging.getLogger('greenqueue')

from greenqueue.utils import Singleton

from .base import BaseService
from .. import settings

import threading


class ZMQService(BaseService):
    def __init__(self):
        super(ZMQService, self).__init__()
        self.socket = None

    @property
    def zmq(self):
        return import_module('zmq')

    def start(self):
        self.load_modules()

        ctx = self.zmq.Context.instance()
        socket = ctx.socket(self.zmq.PULL)
        socket.connect(settings.GREENQUEUE_BIND_ADDRESS)
        
        log.info("greenqueue: now listening on %s. (pid %s)",
            settings.GREENQUEUE_BIND_ADDRESS, os.getpid())
        
        while True:
            message = socket.recv_pyobj()
            self.handle_message(message)

    def close(self):
        #if self.socket is not None:
        #    self.socket.close()
        pass

    def create_socket(self):
        ctx = self.zmq.Context.instance()
        self.socket = ctx.socket(self.zmq.PUSH)
        self.socket.bind(settings.GREENQUEUE_BIND_ADDRESS)

    def send(self, name, args=[], kwargs={}):
        new_uuid = self.create_new_uuid()

        with threading.Lock():
            if self.socket is None:
                self.create_socket()

        with threading.Lock():
            self.socket.send_pyobj({
                'name': name, 
                'args': args, 
                'kwargs':kwargs,
                'uuid': new_uuid,
            })

        return new_uuid
