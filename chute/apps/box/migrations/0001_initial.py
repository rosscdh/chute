# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '__first__'),
        ('project', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', uuidfield.fields.UUIDField(null=True, editable=False, max_length=32, blank=True, unique=True, db_index=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('playlist', models.ForeignKey(to='playlist.Playlist')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
