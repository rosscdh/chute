# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import (FeedItem,)

from .serializers import (FeedItemSerializer,)


class FeedItemViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer
    lookup_field = 'pk'
