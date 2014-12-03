# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='playlist',
            field=models.ForeignKey(blank=True, to='playlist.Playlist', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='box',
            name='project',
            field=models.ForeignKey(blank=True, to='project.Project', null=True),
            preserve_default=True,
        ),
    ]
