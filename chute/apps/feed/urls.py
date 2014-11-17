# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (VideoTranscodeWebhookView,)


urlpatterns = patterns('',
    url(r'^webhook/(?P<pk>[\d-]+)/$', VideoTranscodeWebhookView.as_view(), name='webhook_heywatch'),
)
