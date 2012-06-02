# -*- coding: utf-8 -*-

class Singleton(type):
    """ Singleton metaclass. """
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance


from importlib import import_module

def load_class(path):
    """
    Load class from path.
    """

    try:
        mod_name, klass_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except AttributeError as e:
        raise ImproperlyConfigured(u'Error importing %s: "%s"' % (mod_name, e))

    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" class' % (mod_name, klass_name))

    return klass
