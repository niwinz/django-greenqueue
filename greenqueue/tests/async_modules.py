# -*- coding: utf-8 -*-

from greenqueue.core import Library

register = Library()

@register.task(name='sum')
def sum(x,y):
    return x+y

