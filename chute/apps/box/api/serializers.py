# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Box


class BoxSerializer(serializers.HyperlinkedModelSerializer):
    mac_address = serializers.Field(source='mac_address')

    class Meta:
        model = Box
        exclude = ('data',)
