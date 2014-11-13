# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status as http_status
from rest_framework.response import Response

from chute.apps.feed.api.serializers import (FeedItemSerializer,)
from chute.apps.feed.models import (FeedItem,)
from chute.apps.project.models import (Project,)

from ..models import (Playlist,)
from .serializers import (PlaylistSerializer,)


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'pk'


class ProjectPlaylistEndpoint(generics.ListCreateAPIView):
    #queryset = FeedItem.objects.all()
    model = FeedItem
    serializer_class = FeedItemSerializer
    lookup_field = 'pk'

    def initialize_request(self, request, *args, **kwargs):
        # provide the matter object
        self.project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        self.playlist = get_object_or_404(self.project.playlist_set, pk=self.kwargs.get('pk'))
        return super(ProjectPlaylistEndpoint, self).initialize_request(request, *args, **kwargs)

    def get_queryset(self):
        return self.playlist.feed.all()

    def create(self, request, **kwargs):
        feed_item = get_object_or_404(FeedItem, pk=request.DATA.get('feeditem'))
        self.playlist.feed.add(feed_item)
        serializer = self.get_serializer(feed_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=http_status.HTTP_201_CREATED,
                        headers=headers)

class ProjectPlaylistDestroyEndpoint(generics.DestroyAPIView):
    model = FeedItem
    serializer_class = FeedItemSerializer
    lookup_field = 'pk'
    allowed_methods = ('delete', 'options', 'head',)

    def initialize_request(self, request, *args, **kwargs):
        # provide the matter object
        self.project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        self.playlist = get_object_or_404(self.project.playlist_set, pk=self.kwargs.get('playlist_pk'))
        return super(ProjectPlaylistDestroyEndpoint, self).initialize_request(request, *args, **kwargs)

    def delete(self, request, **kwargs):
        feed_item = self.get_object()
        self.playlist.feed.remove(feed_item)
        serializer = self.get_serializer(feed_item)
        return Response(serializer.data, status=http_status.HTTP_202_ACCEPTED)
