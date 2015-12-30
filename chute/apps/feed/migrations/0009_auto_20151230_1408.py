# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20151228_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeditem',
            name='provider_crc',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
