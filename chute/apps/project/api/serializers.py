# -*- coding: utf-8 -*-
from rest_framework import serializers

from chute.apps.me.api.serializers import CollaboratorSerializer
from ..models import Project, FeedItem

import datetime
import dateutil.parser


def _get_date_now():
    return datetime.datetime.utcnow().isoformat('T')


class CustomDateTimeField(serializers.DateTimeField):
    # def from_native(self, value):
    #     return datetime.datetime(value).isoformat('T')

    def to_native(self, value):
        if value is None:
            value = _get_date_now()
        return dateutil.parser.parse(value)


class FeedItemSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field(source='pk')
    name = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    picture = serializers.Field(source='data.picture')
    updated_at = CustomDateTimeField(source='data.updated_time')
    absolute_url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = FeedItem
        lookup_field = 'pk'
        exclude = ('data', 'project',)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    collaborators = serializers.SerializerMethodField('get_collaborators')
    feed = serializers.SerializerMethodField('get_feed')
    client = serializers.SerializerMethodField('get_client')

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
