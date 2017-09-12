# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tracker', '0003_trackedemailalternative'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackedemailevent',
            name='description',
            field=models.TextField(default='', verbose_name='Description', editable=False),
            preserve_default=False,
        ),
    ]
