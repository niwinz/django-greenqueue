# -*- coding: utf-8 -*-

from importlib import import_module
from ..core import library
from ..storage import get_storage_backend
from .. import settings


import logging
log = logging.getLogger('greenqueue')

def load_modules():
    """
    Load all modules contained tasks. This method
    will be executed on all processes.
    """

    for modpath in settings.GREENQUEUE_TASK_MODULES:
        log.debug("greenqueue: loading module %s", modpath)
        import_module(modpath)


class BaseWorker(object):
    storage = None

    def __init__(self, queue, stop_event):
        self.queue = queue
        self.stop_event = stop_event

    def __call__(self):
        self.storage = get_storage_backend()
        self.run()

    def get_callable_for_task(self, task):
        # at the moment tasks only can be functions.
        # on future this can be implemented on Task class.
        return task

    def process_callable(self, uuid, _callable, args, kwargs):
        # at the moment process callables in serie.
        result = _callable(*args, **kwargs)

        # save result to result storag backend.
        self.storage.save(uuid, result)

    def _name(self):
        raise NotImplementedError
        
    @property
    def name(self):
        try:
            return "-" + self._name()
        except NotImplementedError:
            return ''

    def run(self):
        load_modules()
        self.lib = library

        while not self.stop_event.is_set():
            name, uuid, args, kwargs = self.queue.get(True)
            log.debug("greenqueue-worker{0}: received message from queue - {1}:{2}".format(self.name, name, uuid))

            try:
                _task = self.lib.task_by_name(name)
            except ValueError:
                log.error("greenqueue-worker: received unknown or unregistret method call: %s", name)
                continue

            task_callable = self.get_callable_for_task(_task)
            self.process_callable(uuid, task_callable, args, kwargs)


class BaseManager(object):
    greenlet = False
    
    def __init__(self):
        log.info("greenqueue: initializing manager")

    def validate_message(self, message):
        name = None
        if "name" not in message:
            return False, name
        else:
            name = message['name']
        if "uuid" not in message:
            return False, name
        if "args" not in message:
            return False, name
        if "kwargs" not in message:
            return False, name
        return True, name

    def _handle_message(self, name, uuid, args, kwargs):
        raise NotImplementedError

    def handle_message(self, message):
        ok, name = self.validate_message(message)
        if not ok:
            log.error("greenqueue: ignoring invalid message")
            return

        args, kwargs, uuid = message['args'], message['kwargs'], message['uuid']
        return self._handle_message(name, uuid, args, kwargs)

    def close(self):
        raise NotImplementedError

    @classmethod
    def instance(cls):
        _instance = cls()
        return _instance
