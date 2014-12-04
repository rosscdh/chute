# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from .views import (PlaylistBoxesView,)


urlpatterns = patterns('',
    url(r'^(?P<slug>[\w\d-]+)/boxes/$', login_required(PlaylistBoxesView.as_view()), name='boxes'),
)
