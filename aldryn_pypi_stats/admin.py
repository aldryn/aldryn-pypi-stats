# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from . import models


class PyPIStatsRepositoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.PyPIStatsRepository, PyPIStatsRepositoryAdmin)
