from __future__ import absolute_import

import logging

from memcache_toolbar.wrappers import ClientWrapper

logger = logging.getLogger(__name__)

try:
    import pylibmc

    client_wrapper = ClientWrapper(pylibmc.Client)
    logger.debug('patched pylibmc.Client for tracking')
except Exception:
    logger.warn('unable to patch pylibmc.Client for tracking', exc_info=True)

