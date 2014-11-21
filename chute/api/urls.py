# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from rest_framework import routers

from chute.apps.feed.api.views import (FeedItemViewSet, VideoViewSet)
from chute.apps.project.api.views import (ProjectViewSet,)
from chute.apps.playlist.api.views import (PlaylistViewSet,
                                           ProjectPlaylistEndpoint,
                                           ProjectPlaylistDestroyEndpoint,)
# from chute.apps.project.api.views import (S3SignatureEndpoint,
#                                              ProjectUploadVideoEndpoint,
#                                              VideoCommentsEndpoint,
#                                              VideoCommentDetailEndpoint,)
from chute.apps.me.api.views import (UserProfileViewSet,
                                     CollaboratorEndpoint,)

router = routers.SimpleRouter(trailing_slash=True)

"""
ViewSets
"""
router.register(r'users', UserProfileViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'feed', FeedItemViewSet)
router.register(r'video', VideoViewSet)
router.register(r'playlist', PlaylistViewSet)


urlpatterns = patterns('',
    url(r'^projects/(?P<project_slug>[\d\w-]+)/playlist/(?P<pk>[\d\w-]+)/$', ProjectPlaylistEndpoint.as_view(), name='project_playlist_feeditem'),
    url(r'^projects/(?P<project_slug>[\d\w-]+)/playlist/(?P<playlist_pk>[\d\w-]+)/(?P<pk>[\d\w-]+)/$', ProjectPlaylistDestroyEndpoint.as_view(), name='project_playlist_feeditem'),

    url(r'^projects/(?P<slug>[\d\w-]+)/collaborators/((?P<email>.*)/)?$', CollaboratorEndpoint.as_view(), name='project_collaborators'),
) + router.urls
