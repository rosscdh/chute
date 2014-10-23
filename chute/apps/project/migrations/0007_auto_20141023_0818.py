# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20141023_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeditem',
            name='post_type',
            field=models.IntegerField(null=True, choices=[(0, b'Link'), (1, b'Status'), (2, b'Photo'), (3, b'Video')]),
        ),
    ]
