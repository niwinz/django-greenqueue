# -*- coding: utf-8 -*-

from .base import BaseService

class SyncService(BaseService):
    def send(self, name, args=[], kwargs={}):
        _uuid = self.create_new_uuid()
        _task = self.lib.task_by_name(name)

        _result = _task(*args, **kwargs)
        self.storage.save(_uuid, _result)
        return _uuid
