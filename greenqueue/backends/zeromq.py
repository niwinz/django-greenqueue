# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.timezone import now

from greenqueue.utils import Singleton
from .base import BaseService
from .. import settings, shortcuts

import logging, os, datetime
log = logging.getLogger('greenqueue')


class ZMQService(BaseService):
    socket = None

    def start(self):
        self.manager = shortcuts.load_worker_class().instance()
        if self.manager.greenlet:
            zmq = import_module("gevent_zeromq").zmq
        else:
            zmq = import_module('zmq')

        self.manager.start()

        ctx = zmq.Context.instance()
        socket = ctx.socket(zmq.PULL)
        socket.bind(settings.GREENQUEUE_BIND_ADDRESS)

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

        socket = ctx.socket(zmq.PUSH)
        socket.connect(settings.GREENQUEUE_BIND_ADDRESS)
        return socket

    def send(self, name, args=[], kwargs={}, eta=None, countdown=None):
        new_uuid = self.create_new_uuid()

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

        socket = self.create_socket()
        socket.send_pyobj(message_object)
        return new_uuid
