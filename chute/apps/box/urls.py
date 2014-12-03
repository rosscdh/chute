# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (BoxList, BoxCreate, BoxEdit, BoxDetail,)


urlpatterns = patterns('',
    url(r'^/(?P<slug>[\d\w\-\_]+)/edit/$', BoxEdit.as_view(), name='edit'),
    url(r'^/(?P<slug>[\d\w\-\_]+)/$', BoxDetail.as_view(), name='detail'),
    url(r'^/create/$', BoxCreate.as_view(), name='create'),
    url(r'^$', BoxList.as_view(), name='list'),
)
