# -*- coding: utf-8 -*-

from .base import BaseWorker, BaseManager, load_modules
from ..core import library

class SyncWorker(BaseWorker):
    def __init__(self, *args, **kwargs):
        super(SyncWorker, self).__init__(*args, **kwargs)
        self.lib = library
        load_modules()

    def _name(self):
        return "sync-worker-0"

    def put_task(self, name, uuid, args, kwargs):
        self._process_task(name, uuid, args, kwargs)

    def run(self):
        pass


class SyncManager(BaseManager):
    sync = True

    def __init__(self):
        super(SyncManager, self).__init__()
        self.worker = SyncWorker(None, None, None)
        self.worker()

    def _handle_message(self, name, uuid, args, kwargs):
        self.worker.put_task(name, uuid, args, kwargs)

    def close(self):
        pass
