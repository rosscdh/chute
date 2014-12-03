# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0002_auto_20141203_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='mac_address',
            field=models.CharField(default=123456789, max_length=64, db_index=True),
            preserve_default=False,
        ),
    ]
