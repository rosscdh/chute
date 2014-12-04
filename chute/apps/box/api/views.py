# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from chute.apps.playlist.api.serializers import PlaylistSerializer
from chute.apps.playlist.models import Playlist
from chute.pusher_services import PusherAuthService

from ..models import (Box,)
from .serializers import (BoxSerializer,)

import logging
logger = logging.getLogger('django.request')


class BoxViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    lookup_field = 'slug'


class BoxPlaylistEndpoint(generics.RetrieveAPIView):
    model = Box
    serializer_class = PlaylistSerializer
    lookup_field = 'mac_address'

    def dispatch(self, request, *args, **kwargs):
        self.playlist = Playlist()
        self.project = self.get_object().project
        return super(BoxPlaylistEndpoint, self).dispatch(request=request, *args, **kwargs)

    def get_serializer(self, instance, **kwargs):
        if self.project is not None:
            self.playlist = self.object.project.playlist_set.all().first() if self.object.playlist is None else self.object.playlist
            kwargs.update({'instance': self.playlist})
        return super(BoxPlaylistEndpoint, self).get_serializer(**kwargs)

    def retrieve(self, request, **kwargs):
        status_code = status.HTTP_200_OK

        if self.playlist.pk is None:
            status_code = status.HTTP_206_PARTIAL_CONTENT

        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        return Response(serializer.data, status=status_code)


class BoxRegistrationEndpoint(generics.CreateAPIView):
    model = Box
    serializer_class = BoxSerializer

    def create(self, request, **kwargs):
        status_code = status.HTTP_200_OK
        extra_data = {}
        mac_address = request.DATA.get('mac_address')
        project_slug = request.DATA.get('project', None)
        #playlist_uuid = request.DATA.get('playlist', None)

        box, is_new = self.model.objects.get_or_create(mac_address=mac_address)

        if project_slug is not None:
            logger.info('registering box: %s with project: %s' % (box, project_slug))

            try:
                project = box.project.__class__.objects.get(slug=project_slug)
                box.project = project
                box.save(update_fields=['project'])

            except box.project.__class__.DoesNotExist:
                extra_data['error'] = {'message': 'A project with that slug: %s could not be found' % project_slug}
                status_code = status.HTTP_406_NOT_ACCEPTABLE

        serializer = self.serializer_class(box, context={'request': request})

        response = {
            'box': serializer.data,
            'is_new': is_new,
        }
        response.update(extra_data)

        return Response(response, status_code)


class BoxPusherPresenceAuthEndpoint(views.APIView):
    def post(self, request, **kwargs):
        s = PusherAuthService(channel_name=request.DATA.get('channel_name'),
                              socket_id=request.DATA.get('socket_id'))
        json_data = s.process()
        return Response(json_data)
