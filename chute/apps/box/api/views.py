# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import (Box,)
from .serializers import (BoxSerializer,)


class BoxViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    lookup_field = 'slug'
