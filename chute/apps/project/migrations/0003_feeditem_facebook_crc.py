# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_feeditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='facebook_crc',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]
