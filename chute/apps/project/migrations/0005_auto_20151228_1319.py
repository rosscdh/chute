# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20150124_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='url',
            field=models.URLField(help_text=b'URL to the resource', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
