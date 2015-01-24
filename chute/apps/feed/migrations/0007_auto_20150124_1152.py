# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_auto_20150124_1152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feeditem',
            old_name='facebook_crc',
            new_name='provider_crc',
        ),
    ]
