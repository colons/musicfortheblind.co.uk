# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Story'
        db.create_table(u'news_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('deck', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('content', self.gf('mftb5.utils.mdfield.MarkdownTextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Album'], null=True, blank=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Track'], null=True, blank=True)),
            ('content_html', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'news', ['Story'])


    def backwards(self, orm):
        # Deleting model 'Story'
        db.delete_table(u'news_story')


    models = {
        u'music.album': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Album'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('mftb5.utils.mdfield.MarkdownTextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'music.track': {
            'Meta': {'ordering': "['track_number']", 'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_tracks'", 'blank': 'True', 'to': u"orm['music.Album']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('mftb5.utils.mdfield.MarkdownTextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flac': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karaoke_flac': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'karaoke_mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'karaoke_ogg': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'ogg': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'track_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'news.story': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Story'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Album']", 'null': 'True', 'blank': 'True'}),
            'content': ('mftb5.utils.mdfield.MarkdownTextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deck': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Track']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['news']