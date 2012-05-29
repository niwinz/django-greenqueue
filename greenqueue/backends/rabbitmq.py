# -*- coding: utf-8 -*-

"""
This module is not fully implemented.
"""


from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

import logging, os
log = logging.getLogger('greenqueue')

from .base import BaseService
from .. import settings


class RabbitMQService(BaseService):
    def __init__(self):
        super(ZMQService, self).__init__()

    def start(self):
        self.load_modules()

        log.info("greenqueue: now listening on %s. (pid %s)",
            settings.GREENQUEUE_BIND_ADDRESS, os.getpid())
        
        while True:
            message = socket.recv_pyobj()
            self.handle_message(message)

    def send(self, name, args=[], kwargs={}):
        parameters = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue="test", durable=True,
            exclusive=False, auto_delete=False)

        channel.basic_publish(exchange='',
            routing_key="test",
            body="Hello World!",
            properties=pika.BasicProperties(content_type="text/plain",delivery_mode=1)
        )

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
