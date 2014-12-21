# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Track.ogg'
        db.alter_column(u'music_track', 'ogg', self.gf('django.db.models.fields.files.FileField')(max_length=500))

        # Changing field 'Track.flac'
        db.alter_column(u'music_track', 'flac', self.gf('django.db.models.fields.files.FileField')(max_length=500))

        # Changing field 'Track.mp3'
        db.alter_column(u'music_track', 'mp3', self.gf('django.db.models.fields.files.FileField')(max_length=500))

    def backwards(self, orm):

        # Changing field 'Track.ogg'
        db.alter_column(u'music_track', 'ogg', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'Track.flac'
        db.alter_column(u'music_track', 'flac', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'Track.mp3'
        db.alter_column(u'music_track', 'mp3', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    models = {
        u'music.album': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Album'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('mftb5.utils.mdfield.MarkdownTextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'music.track': {
            'Meta': {'ordering': "['track_number']", 'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_tracks'", 'to': u"orm['music.Album']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('mftb5.utils.mdfield.MarkdownTextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flac': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karaoke_flac': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'karaoke_mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'karaoke_ogg': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'ogg': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'track_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['music']