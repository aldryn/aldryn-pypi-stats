# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_pypi_stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pypistatsdownloadspluginmodel',
            name='base_count',
            field=models.IntegerField(default=0, help_text='Will be added to the total.', verbose_name='Base Count'),
        ),
    ]
