======================
Memcache Debug Toolbar
======================

The Memcache Debug Toolbar is an add-on for Django Debug Toolbar for tracking
memcached usage. It currently supports both the ``pylibmc`` and ``memcache`` libraries.

This is definitely beta software, but I've found it useful in work and personal
projects. Feedback welcome, patches appreciated. - Ross McFarland

Installation
============

#. Install and configure `Django Debug Toolbar <https://github.com/django-debug-toolbar/django-debug-toolbar>`_.

#. Add the ``memcache_toolbar`` app to your ``INSTALLED_APPS``.

Configuration
=============

#. Add the ``memcache`` or ``pylibmc`` panel to ``DEBUG_TOOLBAR_PANELS``.

   You'll need to add the panel corresponding to the library you'll be using to
   the list of debug toolbar's panels in the order in which you'd like it to
   appear::

	DEBUG_TOOLBAR_PANELS = (
            ...
	    'memcache_toolbar.panels.memcache.MemcachePanel',
	    # if you use pylibmc you'd include its panel instead
	    # 'memcache_toolbar.panels.pylibmc.PylibmcPanel',
	)
