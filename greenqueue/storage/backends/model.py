# -*- coding: utf-8 -*-

from django.db import transaction
from greenqueue.models import TaskResult
from greenqueue.exceptions import ResultDoesNotExist
from .base import BaseStorageBackend


try:
    import cPickle as pickle
except ImportError:
    import pickle

import base64

class StorageBackend(BaseStorageBackend):
    def get(self, uuid, default=None):
        try:
            result_obj = TaskResult.objects.get(uuid=uuid)
        except TaskResult.DoesNotExist:
            if default is None:
                raise ResultDoesNotExist()
            return default

        _val = base64.b64decode(result_obj.result)
        return pickle.loads(_val)

    @transaction.commit_on_success
    def save(self, uuid, value):
        _val = pickle.dumps(value)
        tr = TaskResult.objects.create(uuid=uuid, \
            result=base64.b64encode(_val))
        return value
