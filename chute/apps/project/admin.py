from django.contrib import admin

from .models import Project, ProjectCollaborator, FeedItem

admin.site.register([Project, ProjectCollaborator, FeedItem])