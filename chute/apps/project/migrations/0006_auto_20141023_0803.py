# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_feeditem_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeditem',
            name='template',
            field=models.IntegerField(default=1, choices=[(1, b'Basic Template')]),
        ),
    ]
