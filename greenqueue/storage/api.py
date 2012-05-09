# -*- coding: utf-8 -*-

from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from ..core import load_class

def get_storage_backend(path=None, **kwargs):
    """
    Load storage backend.
    """

    path = path or getattr(settings, "GREENQUEUE_RESULTS_BACKEND",
        "greenqueue.storage.backends.model.StorageBackend")
    return load_class(path)(**kwargs)
