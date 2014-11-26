# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_feeditem_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='transcode_state',
            field=models.IntegerField(default=1, db_index=True, choices=[(0, b'Error'), (1, b'Pending Transcode'), (2, b'In-Progress'), (3, b'Transcode Complete')]),
            preserve_default=True,
        ),
    ]
