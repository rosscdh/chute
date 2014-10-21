# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20141021_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='wait_for',
            field=models.IntegerField(default=20),
            preserve_default=True,
        ),
    ]
