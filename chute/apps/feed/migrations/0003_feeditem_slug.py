# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_video_video_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='slug',
            field=uuidfield.fields.UUIDField(null=True, editable=False, max_length=32, blank=True, unique=True, db_index=True),
            preserve_default=True,
        ),
    ]
