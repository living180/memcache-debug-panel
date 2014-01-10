from __future__ import absolute_import

import collections
import time
import traceback

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from debug_toolbar import settings as dt_settings
from debug_toolbar.panels import Panel
from debug_toolbar.utils import get_stack, render_stacktrace, tidy_stacktrace


class BasePanel(Panel):
    template = 'memcache_toolbar/panels/memcache.html'

    def __init__(self, *args, **kwargs):
        super(BasePanel, self).__init__(*args, **kwargs)
        self.calls = []
        self.total_time = 0

    def enable_instrumentation(self):
        self.client_wrapper.install_recorder(self._recorder)

    def disable_instrumentation(self):
        self.client_wrapper.remove_recorder()

    def process_response(self, request, response):
        self.record_stats({'calls': self.calls, 'total_time': self.total_time})

    @property
    def has_content(self):
        return bool(self.calls)

    def title(self):
        return _('Memcache Calls')

    def nav_title(self):
        return 'Memcache'

    def nav_subtitle(self):
        n = len(self.calls)
        if n == 0:
            return _("0 calls")
        elif n == 1:
            return _("1 call in {:0.2f}ms").format(self.total_time)
        else:
            return _("{} calls in {:0.2f}ms").format(n, self.total_time)

    def _recorder(self, func, name, *args, **kwargs):
        if dt_settings.CONFIG['ENABLE_STACKTRACES']:
            stacktrace = tidy_stacktrace(reversed(get_stack()))[:-2]
        else:
            stacktrace = []
        if len(args) > 1:
            keys = args[1]
            if isinstance(args[1], collections.Mapping):
                # if the first argument is a mapping object (e.g. a dict) it is
                # probably for a *multi call and the keys are the keys from the
                # dictionary
                keys = args[1].keys()
            else:
                # else the key is just the first argument
                keys = args[1]
        else:
            keys = None
        try:
            start = time.time()
            result = func(*args, **kwargs)
        finally:
            elapsed = time.time() - start
            self.calls.append({'name': name, 'keys': keys, 'trace': render_stacktrace(stacktrace), 'time': elapsed})
            self.total_time += elapsed

        return result
