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

    def start(self):
        raise NotImplementedError

    @classmethod
    def instance(cls):
        _instance = cls()
        return _instance

    def create_new_uuid(self):
        return str(uuid.uuid1())

    def send(self, name, args=[], kwargs={}, eta=None, countdown=None):
        raise NotImplementedError

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
