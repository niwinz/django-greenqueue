# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

GREENQUEUE_BIND_ADDRESS = getattr(settings, 'GREENQUEUE_BIND_ADDRESS', 'ipc:///tmp/greenqueue.sock')
GREENQUEUE_TASK_MODULES = getattr(settings, 'GREENQUEUE_TASK_MODULES', [])

# Available backends:
# * greenqueue.backends.zeromq.ZMQService -> for normal async use
# * greenqueue.backends.sync.SyncService -> for testing this runs on sync mode, no workers needed.
# * greenqueue.backends.rabbitmq.RabbitMQService
#
# By default, sync backend is set.

GREENQUEUE_BACKEND = getattr(settings, 'GREENQUEUE_BACKEND', 'greenqueue.backends.sync.SyncService')

# This settings is only used with gevent_zeromq.ZMQService backend.
GREENQUEUE_BACKEND_POOLSIZE = getattr(settings, 'GREENQUEUE_BACKEND_POOLSIZE', 10)


GREENQUEUE_RABBITMQ_USERNAME = getattr(settings, 'GREENQUEUE_RABBITMQ_USERNAME', None)
GREENQUEUE_RABBITMQ_PASSWORD = getattr(settings, 'GREENQUEUE_RABBITMQ_PASSWORD', None)
GREENQUEUE_RABBITMQ_HOSTNAME = getattr(settings, 'GREENQUEUE_RABBITMQ_HOSTNAME', 'localhost')
GREENQUEUE_RABBITMQ_PORT = getattr(settings, 'GREENQUEUE_RABBITMQ_PORT', 5672)
GREENQUEUE_RABBITMQ_VHOST = getattr(settings, 'GREENQUEUE_RABBITMQ_VHOST', '/')
GREENQUEUE_RABBITMQ_QUEUE = getattr(settings, 'GREENQUEUE_RABBITMQ_QUEUE', 'greenqueue')
GREENQUEUE_RABBITMQ_ROUTING_KEY = getattr(settings, 'GREENQUEUE_RABBITMQ_ROUTING_KEY',
                                                                GREENQUEUE_RABBITMQ_QUEUE)
GREENQUEUE_RABBITMQ_EXCHANGE = getattr(settings, 'GREENQUEUE_RABBITMQ_EXCHANGE', '')
