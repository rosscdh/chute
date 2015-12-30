# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_auto_20150124_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeditem',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
