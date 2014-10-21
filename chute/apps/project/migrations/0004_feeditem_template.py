# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_feeditem_wait_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='template',
            field=models.CharField(default=b'basic', max_length=64, choices=[(b'basic', b'Basic Template')]),
            preserve_default=True,
        ),
    ]
