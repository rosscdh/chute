# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import (Playlist,)
from .serializers import (PlaylistSerializer,)


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'pk'
