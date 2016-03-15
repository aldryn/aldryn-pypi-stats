# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import requests

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from .utils import get_cache_key

logger = logging.getLogger(__name__)

CACHE_DURATION = getattr(settings, "ALDRYN_PYPI_STATS_CACHE_DURATION", 3600)


@python_2_unicode_compatible
class PyPIStatsRepository(models.Model):

    label = models.CharField(_('label'),
        max_length=128, default='', blank=False,
        help_text=_('Provide a descriptive label for your package. E.g., '
                    '"django CMS'))

    package_name = models.CharField(_('package name'),
        max_length=255, blank=False, default='', unique=True,
        help_text=_('Enter the PyPI package name. E.g., "django-cms"'))

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _('repositories')

    def get_json_url(self):
        return "https://pypi.python.org/pypi/{package_name}/json".format(
            package_name=self.package_name)

    def __str__(self):
        return self.label

    def get_cache_key(self):
        """
        Gets the cache key for this specific package configuration.
        """
        return get_cache_key(
            self.__class__.__name__, settings=(self.pk, ))

    def get_data(self, force_refresh=False):
        """
        Fetches the data (from PyPI) for this particular package configuration.

        Manages a cache of the data.
        """
        key = self.get_cache_key()
        if force_refresh:
            data = None
        else:
            data = cache.get(key, None)
        if not data:
            if force_refresh:
                logger.info('Force refresh')
            else:
                logger.info('Natural refresh')
            url = self.get_json_url()
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
            else:
                data = None
            duration = CACHE_DURATION * 2 if force_refresh else CACHE_DURATION
            cache.set(key, data, duration)
        return data


class PyPIStatsBase(CMSPlugin):
    # avoid reverse relation name clashes by not adding a related_name
    # to the parent plugin
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True)

    package = models.ForeignKey('PyPIStatsRepository',
        null=True, verbose_name=_('package'),
        help_text=_('Select the package to work with.'))

    class Meta:
        abstract = True


@python_2_unicode_compatible
class PyPIStatsDownloadsPluginModel(PyPIStatsBase):

    fetched = False

    ALL_TIME = 'all_time'

    CHOICES = (
        (ALL_TIME, _('All Time')),
        ('last_month', _('Last month')),
        ('last_week', _('Last week')),
        ('last_day', _('Yesterday')),
    )

    downloads_period = models.CharField(
        _('Period'), choices=CHOICES, default='last_month', max_length=16,
        help_text=_('Select the period of interest for the '
                    'downloads statistic.'))
    upper_text = models.CharField(
        _('upper text'), max_length=255, default='', blank=True,
        help_text=_('Provide text to display above.'))
    lower_text = models.CharField(
        _('lower text'), max_length=255, default='', blank=True,
        help_text=_('Provide text to display below.'))
    base_count = models.IntegerField(
        _('Base Count'), default=0, help_text=_('Will be added to the total.'))

    def _fetch_statistics(self):
        """Fetches the appropriate statistic from PyPI."""
        time_period_stats = None
        release_stats = 0

        data = self.package.get_data()
        if data:
            # Time-Period Downloads
            try:
                time_period_stats = (
                    data['info']['downloads'][self.downloads_period])
            except (AttributeError, KeyError):
                pass

            # Release Downloads
            try:
                for release in data['releases'].values():
                    for variation in release:
                        release_stats += variation['downloads']
            except (AttributeError, KeyError):
                pass
        return time_period_stats, release_stats

    def get_downloads(self):
        if not self.package or not self.package.package_name:
            return 0

        time_period_stats, release_stats = self._fetch_statistics()
        if self.downloads_period == self.ALL_TIME:
            stats = release_stats
        else:
            stats = time_period_stats

        # add base count
        return stats + self.base_count

    def get_digits(self):
        """Returns the number of downloads as a list of string characters."""
        return list(str(int(self.get_downloads())))

    def __str__(self):
        human = next((c[1] for c in self.CHOICES if c[0] == self.downloads_period))
        return 'Download count for period: %s for package: %s' % (
            human.lower(),
            self.package.package_name if self.package else '[unknown package]',
        )
