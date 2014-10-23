# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_feeditem_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='post_type',
            field=models.IntegerField(default=1, choices=[(0, b'Link'), (1, b'Status'), (2, b'Photo'), (3, b'Video')]),
            preserve_default=False,
        ),
    ]
