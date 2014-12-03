# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from ..models import (Box,)
from .serializers import (BoxSerializer,)


class BoxViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    lookup_field = 'slug'


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
