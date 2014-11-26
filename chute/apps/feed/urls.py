# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from .views import (VideoTranscodeWebhookView,
                    VideoFeedItemForm,)


urlpatterns = patterns('',
    url(r'^webhook/(?P<pk>[\d-]+)/$', csrf_exempt(VideoTranscodeWebhookView.as_view()), name='webhook_heywatch'),

    url(r'^(?P<project_slug>[\w-]+)/video/((?P<slug>[\w-]+)/)?$', VideoFeedItemForm.as_view(), name='create_video_feeditem'),
)
