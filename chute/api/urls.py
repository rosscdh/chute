# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

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
from chute.apps.box.api.views import (BoxRegistrationEndpoint,
                                      BoxPusherPresenceAuthEndpoint,
                                      BoxPlaylistEndpoint,
                                      BoxViewSet,)
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
router.register(r'box', BoxViewSet)


urlpatterns = patterns('',
    url(r'^projects/(?P<project_slug>[\d\w-]+)/playlist/(?P<pk>[\d\w-]+)/$', ProjectPlaylistEndpoint.as_view(), name='project_playlist_feeditem'),
    url(r'^projects/(?P<project_slug>[\d\w-]+)/playlist/(?P<playlist_pk>[\d\w-]+)/(?P<pk>[\d\w-]+)/$', ProjectPlaylistDestroyEndpoint.as_view(), name='project_playlist_feeditem'),
    url(r'^projects/(?P<slug>[\d\w-]+)/collaborators/((?P<email>.*)/)?$', CollaboratorEndpoint.as_view(), name='project_collaborators'),

    url(r'^box/(?P<mac_address>[\d\w-]+)/playlist/$', csrf_exempt(BoxPlaylistEndpoint.as_view()), name='box_playlist'),
    url(r'^box/auth/pusher/$', csrf_exempt(BoxPusherPresenceAuthEndpoint.as_view()), name='pusher_auth'),
    url(r'^box/register/$', csrf_exempt(BoxRegistrationEndpoint.as_view()), name='box_registration'),
) + router.urls
