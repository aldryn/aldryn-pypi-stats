# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

import requests


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

    def get_cache_key(self, settings=()):
        """
        Returns the suitable key for this instance's settings.

        Provide a tuple hashable types that should be considered in the hash.
        Typically, this will be the settings that will be used in the calculated
        value that would be cached.

        E.g., key = self.get_cache_key(('divio/django-cms', 'abc123xyz...', 90))
        """
        cls_name = self.__class__.__name__
        return '#{0}:{1}'.format(cls_name, hash(tuple(settings)))


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

    downloads_period = models.CharField(_('Period'),
        choices=CHOICES, default='last_month', max_length=16,
        help_text=_('Select the period of interest for the '
                    'downloads statistic.'))

    upper_text = models.CharField(_('upper text'), max_length=255,
        default='', blank=True,
        help_text=_('Provide text to display above.'))

    lower_text = models.CharField(_('lower text'), max_length=255,
        default='', blank=True,
        help_text=_('Provide text to display below.'))

    base_count = models.IntegerField(
        _('Base Count'), default=0,
        help_text=_('Will be added to the total.'),
    )

    def _fetch_statistic(self):
        """Fetches the appropriate statistic from PyPI."""
        time_period_stats = None
        release_stats = 0
        url = self.package.get_json_url()
        self.fetched = True
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            # Time Period Downloads
            try:
                time_period_stats = data['info']['downloads'][self.downloads_period]
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

        cache_key = self.get_cache_key([
            self.package.package_name,
            self.downloads_period,
        ])

        stats = cache.get(cache_key)
        if not stats:
            time_period_stats, release_stats = self._fetch_statistic()
            if self.downloads_period == self.ALL_TIME:
                stats = release_stats
            else:
                stats = time_period_stats
            cache.set(cache_key, stats, CACHE_DURATION)

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
