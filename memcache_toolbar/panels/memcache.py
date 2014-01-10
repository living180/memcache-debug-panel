from __future__ import absolute_import

import memcache_toolbar.wrappers.memcache

from memcache_toolbar.panels import BasePanel

class MemcachePanel(BasePanel):
    client_wrapper = memcache_toolbar.wrappers.memcache.client_wrapper
