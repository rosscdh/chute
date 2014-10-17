# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (ProjectListView,
                    ProjectCreateView,
                    ProjectDetailView,)


urlpatterns = patterns('',
    url(r'^create/$', login_required(ProjectCreateView.as_view()), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', login_required(ProjectDetailView.as_view()), name='detail'),
    url(r'^$', login_required(ProjectListView.as_view()), name='list'),
)
