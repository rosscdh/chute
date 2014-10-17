# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from rest_framework import routers

from chute.apps.project.api.views import (ProjectViewSet,
                                          FeedItemViewSet,)
from chute.apps.playlist.api.views import (PlaylistViewSet,)
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
router.register(r'playlist', PlaylistViewSet)


urlpatterns = patterns('',
    url(r'^projects/(?P<slug>[\d\w-]+)/collaborators/((?P<email>.*)/)?$', CollaboratorEndpoint.as_view(), name='project_collaborators'),
) + router.urls
