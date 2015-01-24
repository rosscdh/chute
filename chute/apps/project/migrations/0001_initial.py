# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('client', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('client', models.ForeignKey(blank=True, to='client.Client', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectCollaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_project_owner', models.BooleanField(default=False, db_index=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('role', models.IntegerField(default=2, db_index=True, choices=[(0, b'No Access'), (1, b'Owner'), (2, b'Client'), (3, b'Colleague'), (4, b'3rd Party')])),
                ('project', models.ForeignKey(to='project.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='collaborators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='project.ProjectCollaborator'),
            preserve_default=True,
        ),
    ]
