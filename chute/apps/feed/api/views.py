# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import (FeedItem, Video,)

from .serializers import (FeedItemSerializer, VideoSerializer)


class FeedItemViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer
    lookup_field = 'pk'


class VideoViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'slug'
