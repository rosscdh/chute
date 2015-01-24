# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copy_facebook_page_name_to_url(apps, schema_editor):
    Project = apps.get_model("project", "Project")
    for project in Project.objects.all():
        project.url = "https://facebook.com/%s" % (project.name,)
        project.save(update_fields=['url'])


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_url'),
    ]

    operations = [
      migrations.RunPython(copy_facebook_page_name_to_url),
    ]
