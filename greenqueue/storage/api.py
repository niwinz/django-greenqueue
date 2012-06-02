# -*- coding: utf-8 -*-

from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from ..utils import load_class
from .. import settings

def get_storage_backend(path=None, **kwargs):
    """
    Load storage backend.
    """
    path = path or settings.GREENQUEUE_RESULTS_BACKEND
    return load_class(path)(**kwargs)
