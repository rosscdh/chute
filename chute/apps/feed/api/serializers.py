# -*- coding: utf-8 -*-
from rest_framework import serializers

import urlparse

from chute.apps.me.api.serializers import CollaboratorSerializer

from ..models import (FeedItem, Video,)

import urllib2
import datetime
import dateutil.parser


def _get_date_now():
    return datetime.datetime.utcnow().isoformat('T')


class CustomDateTimeField(serializers.DateTimeField):
    def to_native(self, value):
        if value is None:
            value = _get_date_now()
        return dateutil.parser.parse(value)


class FeedItemSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field(source='pk')
    name = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    #picture = serializers.Field(source='data.picture')
    picture = serializers.SerializerMethodField('get_picture')
    video = serializers.SerializerMethodField('get_video')
    updated_at = CustomDateTimeField(source='data.updated_time')
    absolute_url = serializers.Field(source='get_absolute_url')
    template_name = serializers.Field(source='template_name')
    post_type = serializers.Field(source='post_type_name')

    class Meta:
        model = FeedItem
        lookup_field = 'pk'
        exclude = ('data', 'project',)

    def get_picture(self, obj):
        picture = obj.data.get('picture')
        if picture:
            if 'safe_image.php' in picture:
                picture = urllib2.unquote(picture)
                url = dict(urlparse.parse_qsl(urlparse.urlsplit(picture).query))
                return url.get('url', None)
            else:
                return picture.replace('/v/t1.0-9/s130x130','')
        else:
            return picture

    def get_video(self, obj):
        if obj.post_type == obj.POST_TYPES.video:
            video = obj.video_set.all().first()
            if video and video.transcode_state == video.TRANSCODE_STATE.transcode_complete:
                return video.video.url
        return None 


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        lookup_field = 'slug'
