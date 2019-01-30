from .models import *
import functools


def ignore_disconnect(func):
    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except RuntimeError as err:
            if err.args[1] == 'Empty Instrument':
                pass
            else:
                raise err
    return wrapper