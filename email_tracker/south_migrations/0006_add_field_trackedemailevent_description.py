# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TrackedEmailEvent.description'
        db.add_column('email_tracker_trackedemailevent', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''))


    def backwards(self, orm):
        # Deleting field 'TrackedEmailEvent.description'
        db.delete_column('email_tracker_trackedemailevent', 'description')


    models = {
        'email_tracker.emailcategory': {
            'Meta': {'object_name': 'EmailCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'email_tracker.trackedemail': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'TrackedEmail'},
            'bcc': ('django.db.models.fields.TextField', [], {}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['email_tracker.EmailCategory']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'cc': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'plain'", 'max_length': '64'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'esp_message_id': ('django.db.models.fields.CharField', [], {'max_length': '254', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipients': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'email_tracker.trackedemailalternative': {
            'Meta': {'object_name': 'TrackedEmailAlternative'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alternatives'", 'to': "orm['email_tracker.TrackedEmail']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'email_tracker.trackedemailevent': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'TrackedEmailEvent'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'on_delete': 'models.PROTECT', 'to': "orm['email_tracker.TrackedEmail']"}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['email_tracker']