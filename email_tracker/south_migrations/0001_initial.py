# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailCategory'
        db.create_table('email_tracker_emailcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('email_tracker', ['EmailCategory'])

        # Adding model 'TrackedEmail'
        db.create_table('email_tracker_trackedemail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('from_email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('recipients', self.gf('django.db.models.fields.TextField')()),
            ('cc', self.gf('django.db.models.fields.TextField')()),
            ('bcc', self.gf('django.db.models.fields.TextField')()),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('is_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['email_tracker.EmailCategory'], null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('email_tracker', ['TrackedEmail'])


    def backwards(self, orm):
        # Deleting model 'EmailCategory'
        db.delete_table('email_tracker_emailcategory')

        # Deleting model 'TrackedEmail'
        db.delete_table('email_tracker_trackedemail')


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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipients': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['email_tracker']