# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# General settings.

GREENQUEUE_BIND_ADDRESS = getattr(settings, 'GREENQUEUE_BIND_ADDRESS', 'ipc:///tmp/greenqueue.sock')
GREENQUEUE_TASK_MODULES = getattr(settings, 'GREENQUEUE_TASK_MODULES', [])

# Available backends:
# * greenqueue.backends.sync.SyncService (default) -> for testing this runs on sync mode, no workers needed.
# * greenqueue.backends.zeromq.ZMQService -> for normal async use
# * greenqueue.backends.rabbitmq.RabbitMQService

GREENQUEUE_BACKEND = getattr(settings, 'GREENQUEUE_BACKEND', 'greenqueue.backends.sync.SyncService')

# Available worker managers:
# * greenqueue.worker.sync.SyncManager
# * greenqueue.worker.process.ProcessManager
# * greenqueue.worker.pgevent.GreenletManager

GREENQUEUE_WORKER_MANAGER = getattr(settings, 'GREENQUEUE_WORKER_MANAGER', 'greenqueue.worker.sync.SyncManager')

# Result storage.

GREENQUEUE_RESULTS_BACKEND = getattr(settings, "GREENQUEUE_RESULTS_BACKEND", "greenqueue.storage.backends.model.StorageBackend")
GREENQUEUE_IGNORE_RESULT = getattr(settings, "GREENQUEUE_IGNORE_RESULT", True)

# Worker manager settings.

GREENQUEUE_BACKEND_POOLSIZE = getattr(settings, 'GREENQUEUE_BACKEND_POOLSIZE', 2)
GREENQUEUE_BACKEND_TASKBUFF = getattr(settings, 'GREENQUEUE_BACKEND_TASKBUFF', 5)

# RabbitMQ settings.

GREENQUEUE_RABBITMQ_USERNAME = getattr(settings, 'GREENQUEUE_RABBITMQ_USERNAME', None)
GREENQUEUE_RABBITMQ_PASSWORD = getattr(settings, 'GREENQUEUE_RABBITMQ_PASSWORD', None)
GREENQUEUE_RABBITMQ_HOSTNAME = getattr(settings, 'GREENQUEUE_RABBITMQ_HOSTNAME', 'localhost')
GREENQUEUE_RABBITMQ_PORT = getattr(settings, 'GREENQUEUE_RABBITMQ_PORT', 5672)
GREENQUEUE_RABBITMQ_VHOST = getattr(settings, 'GREENQUEUE_RABBITMQ_VHOST', '/')
GREENQUEUE_RABBITMQ_QUEUE = getattr(settings, 'GREENQUEUE_RABBITMQ_QUEUE', 'greenqueue')
GREENQUEUE_RABBITMQ_ROUTING_KEY = getattr(settings, 'GREENQUEUE_RABBITMQ_ROUTING_KEY', GREENQUEUE_RABBITMQ_QUEUE)
GREENQUEUE_RABBITMQ_EXCHANGE = getattr(settings, 'GREENQUEUE_RABBITMQ_EXCHANGE', '')
