# -*- coding: utf-8 -*-
from .heimdall import CONNECTORS as _CONNECTORS
from functools import wraps


def get_database(format):
    # just two lines to support syntax: @get_database('format')
    # as long as syntax: @get_database(['format1', 'format2'])
    if type(format) is not list:
        format = [format, ]

    def decorator(function):
        # register ``function`` as an IN connector
        for f in format:
            _CONNECTORS['get_database'][f] = function

        @wraps(function)
        def wrapper(*args, **kwargs):
            # call ``function`` and return its result
            return function(*args, **kwargs)
        return wrapper
    return decorator


def create_database(format):
    # just two lines to support syntax: @create_database('format')
    # as long as syntax: @create_database(['format1', 'format2'])
    if type(format) is not list:
        format = [format, ]

    def decorator(function):
        # register ``function`` as an OUT connector
        for f in format:
            _CONNECTORS['create_database'][f] = function

        @wraps(function)
        def wrapper(*args, **kwargs):
            # call ``function`` and return its result
            return function(*args, **kwargs)
        return wrapper
    return decorator
