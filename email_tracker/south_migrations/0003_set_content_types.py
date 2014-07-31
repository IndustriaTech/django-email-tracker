# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.TrackedEmail.objects.filter(body__contains='<html>').update(content_type='html')

    def backwards(self, orm):
        "Write your backwards methods here."

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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['email_tracker.EmailCategory']", 'null': 'True', 'blank': 'True'}),
            'cc': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'plain'", 'max_length': '64'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipients': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['email_tracker']
    symmetrical = True
