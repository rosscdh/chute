# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='feed',
            field=models.ManyToManyField(to='project.FeedItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlist',
            name='project',
            field=models.ForeignKey(to='project.Project'),
            preserve_default=True,
        ),
    ]
