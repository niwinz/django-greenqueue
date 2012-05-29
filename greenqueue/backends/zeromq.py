# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

import logging, os, threading
log = logging.getLogger('greenqueue')

from greenqueue.utils import Singleton

from .base import BaseService
from .. import settings


class ZMQService(BaseService):
    socket = None

    @property
    def zmq(self):
        return import_module('zmq')

    def start(self):
        self.load_modules()

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

    def create_socket(self):
        ctx = self.zmq.Context.instance()
        self.socket = ctx.socket(self.zmq.PUSH)
        self.socket.bind(settings.GREENQUEUE_BIND_ADDRESS)

    def send(self, name, args=[], kwargs={}):
        new_uuid = self.create_new_uuid()
        
        if self.socket is None:
            with threading.Lock():
                self.create_socket()
        
        with threading.Lock():
            self.socket.send_pyobj({
                'name': name, 
                'args': args, 
                'kwargs':kwargs,
                'uuid': new_uuid,
            })

        return new_uuid
