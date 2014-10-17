# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
