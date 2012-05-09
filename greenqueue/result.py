# -*- coding: utf-8 -*-

from greenqueue.exceptions import ResultDoesNotExist, TimeoutError

class AsyncResult(object):
    uuid = None
    error = False
    ready = False
    result = None

    def __init__(self, uuid):
        self.uuid = uuid
        from greenqueue.storage.api import get_storage_backend
        self.storage = get_storage_backend()

    def check(self, default=None):
        try:
            self.result = self.storage.get(self.uuid, default)
        except ResultDoesNotExist as e:
            self.error = e
            raise e
        finally:
            self.ready = True

        return self.result

    def is_ready(self):
        return self.ready
    
    def wait(self, timeout=None):
        if self.is_ready():
            return self.result
        
        try:
            self.result = self.storage.wait(self.uuid, timeout=timeout)
        except TimeoutError as e:
            self.error = e
            raise e
        finally:
            self.ready = True
        
        return self.result
