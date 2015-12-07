# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from chute.apps.feed.views import (FeedItemDetail,)
from .views import (ProjectListView,
                    ProjectCreateView,
                    ProjectDetailView,
                    ProjectFeedView,
                    ProjectPlaylistFeedView,
                    ProjectBoxesView,)


urlpatterns = patterns('',
    url(r'^(?P<slug>[\w\d-]+)/feed/$', ProjectFeedView.as_view(), name='project_feed'),
    url(r'^(?P<slug>[\w\d-]+)/playlist/(?P<playlist_pk>[\d]+)/feed/$', ProjectPlaylistFeedView.as_view(), name='project_playlist_feed'),
    url(r'^(?P<slug>[\w\d-]+)/feed/(?P<pk>[\d]+)/$', FeedItemDetail.as_view(), name='feeditem_detail'),

    url(r'^(?P<slug>[\w\d-]+)/boxes/$', login_required(ProjectBoxesView.as_view()), name='boxes'),

    url(r'^create/$', login_required(ProjectCreateView.as_view()), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', login_required(ProjectDetailView.as_view()), name='detail'),
    url(r'^$', login_required(ProjectListView.as_view()), name='list'),
)
