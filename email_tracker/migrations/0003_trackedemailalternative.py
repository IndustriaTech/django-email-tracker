# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_tracker', '0002_TrackedEmailEvent'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackedEmailAlternative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mimetype', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('email', models.ForeignKey(related_name='alternatives', to='email_tracker.TrackedEmail', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Alternative',
                'verbose_name_plural': 'Alternatives',
            },
        ),
    ]
