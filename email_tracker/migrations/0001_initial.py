# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Email Category',
                'verbose_name_plural': 'Email Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrackedEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=512, verbose_name='Subject')),
                ('from_email', models.CharField(max_length=255, verbose_name='From email')),
                ('recipients', models.TextField(verbose_name='Recipients')),
                ('cc', models.TextField(verbose_name='Cc')),
                ('bcc', models.TextField(verbose_name='Bcc')),
                ('body', models.TextField(verbose_name='Body', editable=False)),
                ('content_type', models.CharField(default='plain', max_length=64)),
                ('is_sent', models.BooleanField(default=False, verbose_name='Is sent')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('category', models.ForeignKey(verbose_name='Category', blank=True, to='email_tracker.EmailCategory', null=True, on_delete=models.PROTECT)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'Tracked Email',
                'verbose_name_plural': 'Tracked Emails',
            },
            bases=(models.Model,),
        ),
    ]
