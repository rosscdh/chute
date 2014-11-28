# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import chute.apps.feed.models.video
import chute.utils


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_video_transcode_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeditem',
            name='name',
            field=models.CharField(help_text=b'Name by which this item will be known', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(help_text=b'Name by which this video will be known', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(storage=chute.utils._managed_S3BotoStorage, max_length=255, null=True, upload_to=chute.apps.feed.models.video._upload_video, blank=True),
            preserve_default=True,
        ),
    ]
