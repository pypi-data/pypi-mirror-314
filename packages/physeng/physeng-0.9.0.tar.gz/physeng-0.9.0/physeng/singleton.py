#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

from functools import wraps

def Singleton(class_):
    class_new = class_.__new__
    instance = None

    @wraps(class_.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = class_new(cls, *args, **kwargs)
        return instance
    class_.__new__ = __new__
    return class_
