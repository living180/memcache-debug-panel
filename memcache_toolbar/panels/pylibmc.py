from __future__ import absolute_import

import memcache_toolbar.wrappers.pylibmc

from memcache_toolbar.panels import BasePanel

class PylibmcPanel(BasePanel):
    client_wrapper = memcache_toolbar.wrappers.pylibmc.client_wrapper
