from django.contrib import admin

from .models import Project, ProjectCollaborator

admin.site.register([Project, ProjectCollaborator])