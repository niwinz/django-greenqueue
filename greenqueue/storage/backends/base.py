# -*- coding: utf-8 -*-

from greenqueue.utils import Singleton
from greenqueue.exceptions import ResultDoesNotExist, TimeoutError

import importlib

class BaseStorageBackend(object):
    __metaclass__ = Singleton
    _sleep = None

    def get(self, uuid, default=None):
        raise NotImplementedError

    def save(self, uuid, result):
        raise NotImplementedError

    def wait(self, uuid, timeout=None, interval=0.5):
        time_elapsed = 0.0
        result = None

        while True: 
            try:
                result = self.get(uuid)
                break
            except ResultDoesNotExist:
                pass
            
            import time
            time.sleep(interval)
            time_elapsed += interval

            if timeout and time_elapsed >= timeout:
                raise TimeoutError("The operation timed out.")

        return result
