from __future__ import absolute_import

import threading

_TRACKED_METHOD_NAMES = [
    'add',
    'append',
    'cas',
    'decr',
    'delete',
    'delete_multi',
    'flush_all',
    'get',
    'get_multi',
    'gets',
    'incr',
    'prepend',
    'replace',
    'set',
    'set_multi',
]

class ClientWrapper(object):
    def __init__(self, client_class):
        self.recorders = {}
        for name in _TRACKED_METHOD_NAMES:
            setattr(client_class, name, self._wrap_method(getattr(client_class, name), name))

    def _wrap_method(self, orig_method, name):
        def wrapper(*args, **kwargs):
            recorder = self.recorders.get(threading.current_thread())
            if recorder is not None:
                return recorder(orig_method, name, *args, **kwargs)
            else:
                return orig_method(*args, **kwargs)
        return wrapper

    def install_recorder(self, recorder):
        self.recorders[threading.current_thread()] = recorder

    def remove_recorder(self):
        self.recorders.pop(threading.current_thread())
