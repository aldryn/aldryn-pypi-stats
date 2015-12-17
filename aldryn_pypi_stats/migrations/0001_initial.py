# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyPIStatsDownloadsPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('downloads_period', models.CharField(default='last_month', help_text='Select the period of interest for the downloads statistic.', max_length=16, verbose_name='Period', choices=[('all_time', 'All Time'), ('last_month', 'Last month'), ('last_week', 'Last week'), ('last_day', 'Yesterday')])),
                ('upper_text', models.CharField(default='', help_text='Provide text to display above.', max_length=255, verbose_name='upper text', blank=True)),
                ('lower_text', models.CharField(default='', help_text='Provide text to display below.', max_length=255, verbose_name='lower text', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='PyPIStatsRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(default='', help_text='Provide a descriptive label for your package. E.g., "django CMS', max_length=128, verbose_name='label')),
                ('package_name', models.CharField(default='', help_text='Enter the PyPI package name. E.g., "django-cms"', unique=True, max_length=255, verbose_name='package name')),
            ],
            options={
                'verbose_name': 'repository',
                'verbose_name_plural': 'repositories',
            },
        ),
        migrations.AddField(
            model_name='pypistatsdownloadspluginmodel',
            name='package',
            field=models.ForeignKey(verbose_name='package', to='aldryn_pypi_stats.PyPIStatsRepository', help_text='Select the package to work with.', null=True),
        ),
    ]
