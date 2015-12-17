# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PyPIStatsDownloadsPluginModel.upper_text'
        db.add_column(u'aldryn_pypi_stats_pypistatsdownloadspluginmodel', 'upper_text',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'PyPIStatsDownloadsPluginModel.lower_text'
        db.add_column(u'aldryn_pypi_stats_pypistatsdownloadspluginmodel', 'lower_text',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PyPIStatsDownloadsPluginModel.upper_text'
        db.delete_column(u'aldryn_pypi_stats_pypistatsdownloadspluginmodel', 'upper_text')

        # Deleting field 'PyPIStatsDownloadsPluginModel.lower_text'
        db.delete_column(u'aldryn_pypi_stats_pypistatsdownloadspluginmodel', 'lower_text')


    models = {
        u'aldryn_pypi_stats.pypistatsdownloadspluginmodel': {
            'Meta': {'object_name': 'PyPIStatsDownloadsPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'downloads_period': ('django.db.models.fields.CharField', [], {'default': "u'last_month'", 'max_length': '16'}),
            'lower_text': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_pypi_stats.PyPIStatsRepository']", 'null': 'True'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'subhead_link': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '4096', 'blank': 'True'}),
            'upper_text': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        },
        u'aldryn_pypi_stats.pypistatsrepository': {
            'Meta': {'object_name': 'PyPIStatsRepository'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128'}),
            'package_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'unique': 'True', 'max_length': '255'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_pypi_stats']