# -*- coding: utf-8 -*-

from .base import BaseService
from .. import settings, shortcuts
from django.core.exceptions import ImproperlyConfigured


class SyncService(BaseService):
    def __init__(self):
        super(SyncService, self).__init__()
        self.manager = shortcuts.load_worker_class().instance()
        if not self.manager.sync:
            raise ImproperlyConfigured("Current worker manager is not compatible with this backend.")


    def send(self, name, args=[], kwargs={}):
        new_uuid = self.create_new_uuid()
        
        message = {
            'name': name,
            'args': args,
            'kwargs':kwargs,
            'uuid': new_uuid,
        }

        self.manager.handle_message(name, message)
        return new_uuid
