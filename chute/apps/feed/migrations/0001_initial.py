# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import chute.apps.feed.models.video
import jsonfield.fields
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facebook_crc', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('message', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('post_type', models.IntegerField(null=True, choices=[(0, b'Link'), (1, b'Status'), (2, b'Photo'), (3, b'Video')])),
                ('wait_for', models.IntegerField(default=20)),
                ('template', models.IntegerField(default=1, choices=[(1, b'Basic Template'), (2, b'Image Left'), (3, b'Image Simple'), (4, b'Fullscreen Video')])),
                ('updated_time', models.DateTimeField(auto_now=True, auto_now_add=True, null=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', uuidfield.fields.UUIDField(db_index=True, unique=True, max_length=32, editable=False, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('video', models.FileField(max_length=255, null=True, upload_to=chute.apps.feed.models.video._upload_video, blank=True)),
                ('video_url', models.URLField(db_index=True)),
                ('video_type', models.IntegerField(default=1, db_index=True, choices=[(1, b'video/mp4'), (2, b'video/mov'), (3, b'video/ogg')])),
                ('data', jsonfield.fields.JSONField(default={})),
                ('feed_item', models.ForeignKey(to='feed.FeedItem')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
    ]
