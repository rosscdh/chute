# -*- coding: utf-8 -*-
from rest_framework import serializers

from chute.apps.project.api.serializers import ProjectForPlaylistSerializer
from chute.apps.feed.api.serializers import FeedItemSerializer
from ..models import Playlist


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field(source='pk')
    project = ProjectForPlaylistSerializer()
    feed = FeedItemSerializer()

    class Meta:
        model = Playlist
        lookup_field = 'pk'
        exclude = ('data',)
