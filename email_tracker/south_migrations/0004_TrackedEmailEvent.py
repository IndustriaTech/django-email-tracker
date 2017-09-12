# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrackedEmailEvent'
        db.create_table('email_tracker_trackedemailevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', on_delete=models.PROTECT, to=orm['email_tracker.TrackedEmail'])),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('email_tracker', ['TrackedEmailEvent'])

        # Adding field 'TrackedEmail.esp_message_id'
        db.add_column('email_tracker_trackedemail', 'esp_message_id',
                      self.gf('django.db.models.fields.CharField')(max_length=254, unique=True, null=True, blank=True),
                      keep_default=False)


        # Changing field 'TrackedEmail.category'
        db.alter_column('email_tracker_trackedemail', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['email_tracker.EmailCategory'], null=True, on_delete=models.PROTECT))

    def backwards(self, orm):
        # Deleting model 'TrackedEmailEvent'
        db.delete_table('email_tracker_trackedemailevent')

        # Deleting field 'TrackedEmail.esp_message_id'
        db.delete_column('email_tracker_trackedemail', 'esp_message_id')


        # Changing field 'TrackedEmail.category'
        db.alter_column('email_tracker_trackedemail', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['email_tracker.EmailCategory'], null=True))

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
        'email_tracker.trackedemailevent': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'TrackedEmailEvent'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'on_delete': 'models.PROTECT', 'to': "orm['email_tracker.TrackedEmail']"}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['email_tracker']