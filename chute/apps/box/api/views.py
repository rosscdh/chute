# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from chute.apps.playlist.api.serializers import PlaylistSerializer
from chute.apps.playlist.models import Playlist

from ..models import (Box,)
from .serializers import (BoxSerializer,)


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
        mac_address = request.DATA.get('mac_address')
        box, is_new = self.model.objects.get_or_create(mac_address=mac_address)
        serializer = self.serializer_class(box, context={'request': request})
        return Response({
            'box': serializer.data,
            'is_new': is_new,
          })
