# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models


class PyPIStatusBasePlugin(CMSPluginBase):
    module = 'PyPI Stats'
    cache = False


class PyPIStatsDownloadsPlugin(PyPIStatusBasePlugin):
    render_template = 'aldryn_pypi_stats/plugins/downloads.html'
    name = _('Downloads Count')
    model = models.PyPIStatsDownloadsPluginModel

    def render(self, context, instance, placeholder):
        instance.fetched = False
        context['instance'] = instance
        context['digits'] = instance.get_digits()
        context['was_fetched'] = instance.fetched
        return context

plugin_pool.register_plugin(PyPIStatsDownloadsPlugin)
