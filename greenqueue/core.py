# -*- coding: utf-8 -*-


from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from greenqueue.utils import Singleton

from . import settings
from . import result
from . import shortcuts

import logging
log = logging.getLogger('greenqueue')


class Library(object):
    __metaclass__ = Singleton
    __tasks__ = {}

    @classmethod
    def task_list(cls):
        for _name, _task in cls.__tasks__.iteritems():
            yield _name, _task

    @classmethod
    def task_by_name(cls, name):
        if name not in cls.__tasks__:
            raise ValueError("task %s does not exist or not registred" % (name))
        return cls.__tasks__[name]

    @classmethod
    def add_to_class(cls, name, func):
        log.debug("greenqueue: library registring method '%s'", name)
        cls.__tasks__[name] = func
        return func

    def task(self, name=None, compile_function=None):
        if name is None and compile_function is None:
            # @register.tag()
            return self.task_function
        elif name is not None and compile_function is None:
            if callable(name):
                # @register.tag
                return self.task_function(name)
            else:
                # @register.tag('somename') or @register.tag(name='somename')
                def dec(func):
                    return self.task(name, func)
                return dec
        elif name is not None and compile_function is not None:
            # register.tag('somename', somefunc)
            self.add_to_class(name, compile_function)
            return compile_function
        else:
            raise ImproperlyConfigured("invalid task registration")

    def task_function(self, func):
        self.add_to_class(getattr(func, "_decorated_function", func).__name__, func)
        return func

    @classmethod
    def send_task(cls, name, args=[], kwargs={}):
        # load main backend
        backend_class = shortcuts.load_backend_class()

        # obtain client instance
        client = backend_class.instance()

        # send task to workers
        uuid = client.send(name, args, kwargs)
        return result.AsyncResult(uuid)


library = Library
register = Library()
