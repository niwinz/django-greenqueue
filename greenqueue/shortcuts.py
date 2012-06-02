# -*- coding: utf-8 -*-

from .utils import load_class
from . import settings


def load_backend_class():
    """
    Load a default backend class instance."
    """
    return load_class(settings.GREENQUEUE_BACKEND)


def load_worker_class():
    """
    Load a default worker class intance.
    """
    return load_class(settings.GREENQUEUE_WORKER_MANAGER)
