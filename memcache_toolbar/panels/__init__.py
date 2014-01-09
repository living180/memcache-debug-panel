# work around modules with the same name
from __future__ import absolute_import

import logging
import SocketServer
import traceback

from datetime import datetime
from os.path import dirname, realpath

import django

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from debug_toolbar.panels import DebugPanel


logger = logging.getLogger(__name__)

class Calls:
    def __init__(self):
        self.reset()

    def reset(self):
        self._calls = []

    def append(self, call):
        self._calls.append(call)

    def calls(self):
        return self._calls

    def size(self):
        return len(self._calls)

    def last(self):
        return self._calls[-1]

# NOTE this is not even close to thread-safe/aware
instance = Calls()

# based on the function with the same name in ddt's sql, i'd rather just use it
# than copy it, but i can't import it without things blowing up
django_path = realpath(dirname(django.__file__))
socketserver_path = realpath(dirname(SocketServer.__file__))
def tidy_stacktrace(strace):
    trace = []
    for s in strace[:-1]:
        s_path = realpath(s[0])
        if getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {}).get('HIDE_DJANGO_SQL', True) \
            and django_path in s_path and not 'django/contrib' in s_path:
            continue
        if socketserver_path in s_path:
            continue
        trace.append((s[0], s[1], s[2], s[3]))
    return trace

def record(func):
    def recorder(*args, **kwargs):
        stacktrace = tidy_stacktrace(traceback.extract_stack())
        call = {'function': func.__name__, 'args': None, 
                'stacktrace': stacktrace}
        instance.append(call)
        # the try here is just being extra safe, it should not happen
        try:
            a = None
            # first arg is self, do we have another
            if len(args) > 1:
                a = args[1]
                # is it a dictionary (most likely multi)
                if isinstance(a, dict):
                    # just use it's keys
                    a = a.keys()
            # store the args
            call['args'] = a
        except e:
            logger.exception('tracking of call args failed')
        ret = None
        try:
            # the clock starts now
            call['start'] = datetime.now()
            ret = func(*args, **kwargs)
        finally:
            # the clock stops now
            dur = datetime.now() - call['start']
            call['duration'] = (dur.seconds * 1000) + (dur.microseconds / 1000.0)
        return ret
    return recorder


class BasePanel(DebugPanel):
    name = 'Memcache'
    has_content = True

    def process_request(self, request):
        instance.reset()

    def nav_title(self):
        return _('Memcache')

    def nav_subtitle(self):
        duration = 0
        calls = instance.calls()
        for call in calls:
            duration += call['duration']
        n = len(calls)
        if (n > 0):
            return "%d calls, %0.2fms" % (n, duration)
        else:
            return "0 calls"

    def title(self):
        return _('Memcache Calls')

    def url(self):
        return ''

    def content(self):
        duration = 0
        calls = instance.calls()
        for call in calls:
            duration += call['duration']

        context = self.context.copy()
        context.update({
            'calls': calls,
            'count': len(calls),
            'duration': duration,
        })

        return render_to_string('memcache_toolbar/panels/memcache.html',
                context)
