# -*- coding: utf-8 -*-
from rest_framework import serializers

from chute.apps.me.api.serializers import CollaboratorSerializer
from chute.apps.feed.api.serializers import FeedItemSerializer

from ..models import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    collaborators = serializers.SerializerMethodField('get_collaborators')
    feed = serializers.SerializerMethodField('get_feed')
    client = serializers.SerializerMethodField('get_client')

    is_facebook_feed = serializers.Field()

    detail_url = serializers.SerializerMethodField('get_detail_url')

    class Meta:
        model = Project
        lookup_field = 'slug'
        exclude = ('data',)

    def get_feed(self, obj):
        try:
            return FeedItemSerializer(obj.feeditem_set.all()[:10], many=True, context=self.context).data
        except:
            return []

    def get_client(self, obj):
        return {
            'name': getattr(obj.client, 'name', None)
        }

    def get_detail_url(self, obj):
        return obj.get_absolute_url()

    def get_collaborators(self, obj):
        return CollaboratorSerializer(obj.projectcollaborator_set.all(), many=True).data


class ProjectMiniSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        exclude = ('data', 'feed',)


class ProjectForPlaylistSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        exclude = ('collaborators', 'client', 'data', 'feed',)
