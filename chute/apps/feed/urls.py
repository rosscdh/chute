# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from .views import (VideoTranscodeWebhookView,)


urlpatterns = patterns('',
    url(r'^webhook/(?P<pk>[\d-]+)/$', csrf_exempt(VideoTranscodeWebhookView.as_view()), name='webhook_heywatch'),
)
