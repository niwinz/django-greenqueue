# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from greenqueue.utils import Singleton

from .. import settings, core
from ..storage import get_storage_backend

import logging, os, uuid
log = logging.getLogger('greenqueue')


class BaseService(object):
    __metaclass__ = Singleton

    modules_loaded = False
    lib = core.library
    storage = get_storage_backend()

    @classmethod
    def load_modules(cls):
        for modpath in settings.GREENQUEUE_TASK_MODULES:
            log.debug("greenqueue: loading module %s", modpath)
            import_module(modpath)

    def start(self):
        # load all modules
        self.load_modules()
        
    def close(self):
        raise NotImplementedError()

    def create_new_uuid(self):
        return str(uuid.uuid1())

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

    def get_callable_for_task(self, task):
        # at the moment tasks only can be functions.
        # on future this can be implemented on Task class.
        return task

    def process_callable(self, uuid, _callable, args, kwargs):
        # at the moment process callables in serie.
        result = _callable(*args, **kwargs)

        # save result to result storag backend.
        self.storage.save(uuid, result)

    def handle_message(self, message):
        ok, name = self.validate_message(message)
        if not ok:
            log.error("greenqueue: ignoring invalid message")
            return
        
        try:
            _task = self.lib.task_by_name(name)
        except ValueError:
            log.error("greenqueue: received unknown or unregistret method call: %s", name)
            return
        
        task_callable = self.get_callable_for_task(_task)
        args, kwargs, uuid = message['args'], message['kwargs'], message['uuid']
        self.process_callable(uuid, task_callable, args, kwargs)

    @classmethod
    def instance(cls):
        if not cls.modules_loaded:
            cls.modules_loaded = True
            cls.load_modules()

        return cls()
