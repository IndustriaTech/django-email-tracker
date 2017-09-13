# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tracker', '0004_trackedemailevent_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackedemailevent',
            name='recipient',
            field=models.EmailField(default='', verbose_name='Recipient', max_length=254, editable=False),
        ),
    ]
