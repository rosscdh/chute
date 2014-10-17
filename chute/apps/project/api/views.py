# -*- coding: utf-8 -*-
from rest_framework import viewsets

from chute.apps.client.models import Client

from ..models import (Project,
                      FeedItem,
                      ProjectCollaborator)
from ..signals import (get_facebook_details,
                       get_facebook_feed)
from .serializers import (ProjectSerializer,
                          FeedItemSerializer,)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def pre_save(self, obj):
        client_name = self.request.POST.get('client', None)
        if client_name:
            client, is_new = Client.objects.get_or_create(name=client_name, owner=self.request.user)
            obj.client = client

        return super(ProjectViewSet, self).pre_save(obj=obj)

    def post_save(self, obj, created):
        collaborator, is_new = ProjectCollaborator.objects.get_or_create(user=self.request.user, project=obj)

        get_facebook_details.send(sender=self, instance=obj, created=True)
        get_facebook_feed.send(sender=self, instance=obj, user=self.request.user, created=True)

        return super(ProjectViewSet, self).post_save(obj, created=created)


class FeedItemViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer
    lookup_field = 'pk'
