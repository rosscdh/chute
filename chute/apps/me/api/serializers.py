# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from rest_framework import serializers

from chute.apps.project.models import ProjectCollaborator


class UserSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='get_full_name')
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'first_name', 'last_name')


class CollaboratorSerializer(serializers.Serializer):
    pk = serializers.Field(source='user.pk')
    name = serializers.Field(source='user.get_full_name')
    email = serializers.Field(source='user.email')
    initials = serializers.Field(source='user.get_initials')
    user_class = serializers.Field(source='role_name')

    class Meta:
        model = ProjectCollaborator
