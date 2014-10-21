# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=255)),
                ('data', jsonfield.fields.JSONField(default={})),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
