# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_id',
            field=models.IntegerField(default=0, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
