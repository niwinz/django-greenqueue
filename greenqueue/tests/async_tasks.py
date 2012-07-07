# -*- coding: utf-8 -*-

from greenqueue.core import Library
import io

register = Library()

@register.task(name='touch')
def touch(num):
    with io.open("/tmp/greequeue.touch", "w") as f:
        f.write(unicode(num))

    return num
