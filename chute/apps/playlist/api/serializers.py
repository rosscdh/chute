# -*- coding: utf-8 -*-
from rest_framework import serializers

from chute.apps.me.api.serializers import CollaboratorSerializer
from ..models import Playlist


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Playlist
        lookup_field = 'pk'
        exclude = ('data',)
