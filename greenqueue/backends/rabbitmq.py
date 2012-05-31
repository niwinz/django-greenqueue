# -*- coding: utf-8 -*-

"""
This module is not fully implemented.
"""

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from .base import BaseService
from .. import settings

from pika.adapters import SelectConnection

import logging
import pickle
import pika
import os

log = logging.getLogger('greenqueue')


class RabbitMQService(BaseService):
    rabbitmq_parameters = None
    channel = None

    def _on_connected(self, _connection):
        log.info("Connected to RabbitMQ")
        _connection.channel(self._on_channel_opened)

    def _on_channel_opened(self, _channel):
        log.info("Channel opened")
        self.channel = _channel
        self.channel.queue_declare(
            queue = settings.GREENQUEUE_RABBITMQ_QUEUE,
            durable = True,
            exclusive = False, 
            auto_delete = False,
            callback = self._on_queue_declared
        )

    def _on_queue_declared(self, frame):
        log.info("Queue declared (%s)", settings.GREENQUEUE_RABBITMQ_QUEUE)
        self.channel.basic_consume(
            self._handle_delivery, 
            queue = settings.GREENQUEUE_RABBITMQ_QUEUE,
        )

    def _handle_delivery(self, channel, method_frame, header_frame, body):
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        self.handle_message(pickle.loads(body))
    
    def start(self):
        self.load_modules()
        
        log.info("Starting connection to RabbitMQ.")

        connection = self.create_async_connection()
        connection.ioloop.start()

    def create_credentials(self):
        if (settings.GREENQUEUE_RABBITMQ_USERNAME is not None and 
            settings.GREENQUEUE_RABBITMQ_PASSWORD is not None):

            return pika.PlainCredentials(
                settings.GREENQUEUE_RABBITMQ_USERNAME,
                settings.GREENQUEUE_RABBITMQ_PASSWORD
            )

        return None

    def create_connection_params(self):
        if not self.rabbitmq_parameters:
            creadentials = self.create_credentials()

            params = {
                'host': settings.GREENQUEUE_RABBITMQ_HOSTNAME,
                'port': settings.GREENQUEUE_RABBITMQ_PORT, 
                'virtual_host': settings.GREENQUEUE_RABBITMQ_VHOST,
            }

            if creadentials:
                params['credentials'] = creadentials
            
            self.rabbitmq_parameters = pika.ConnectionParameters(**params)

        return self.rabbitmq_parameters

    def create_blocking_connection(self):
        return pika.BlockingConnection(self.create_connection_params())

    def create_async_connection(self):
        return SelectConnection(self.create_connection_params(), self._on_connected)

    def send(self, name, args=[], kwargs={}):
        connection = self.create_blocking_connection()
        channel = connection.channel()
        new_uuid = self.create_new_uuid()

        channel.queue_declare(
            queue = settings.GREENQUEUE_RABBITMQ_QUEUE, 
            durable = True,
            exclusive = False, 
            auto_delete = False
        )
        message = {
            'name': name, 
            'args': args, 
            'kwargs':kwargs,
            'uuid': new_uuid,
        }

        channel.basic_publish(
            exchange = settings.GREENQUEUE_RABBITMQ_EXCHANGE,
            routing_key = settings.GREENQUEUE_RABBITMQ_ROUTING_KEY,
            body = pickle.dumps(message, -1),
        )
        connection.close()
        return new_uuid
