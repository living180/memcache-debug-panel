from __future__ import absolute_import

import logging

from memcache_toolbar.wrappers import ClientWrapper

logger = logging.getLogger(__name__)

try:
    import memcache

    client_wrapper = ClientWrapper(memcache.Client)
    logger.debug('patched memcache.Client for tracking')
except Exception:
    logger.warn('unable to patch memcache.Client for tracking', exc_info=True)
