from django.contrib import admin

from .models import FeedItem, Video

admin.site.register([FeedItem, Video])