# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def get_cache_key(class_name, settings=()):
    """
    Returns the suitable key for this instance's settings.

    Provide a tuple of hashable types that should be considered in the hash.
    Typically, this will be the settings that will be used in the calculated
    value that would be cached.

    E.g., key = self.get_cache_key(('divio/django-cms', 'abc123xyz...', 90))
    """
    return '#{0}:{1}'.format(class_name, hash(tuple(settings)))
