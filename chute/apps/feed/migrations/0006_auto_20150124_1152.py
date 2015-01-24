# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import chute.apps.feed.models.video
import chute.utils


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_auto_20141128_1424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feeditem',
            options={'ordering': ['updated_time']},
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(storage=chute.utils.CustomDeconstructableS3BotoStorage(), max_length=255, null=True, upload_to=chute.apps.feed.models.video._upload_video, blank=True),
            preserve_default=True,
        ),
    ]
