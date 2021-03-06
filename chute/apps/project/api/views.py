# -*- coding: utf-8 -*-
from rest_framework import viewsets

from chute.apps.client.models import Client

from ..models import (Project,
                      ProjectCollaborator)
from ..signals import (get_facebook_details,
                       get_facebook_feed,
                       populate_playlist_with_feed,)
from .serializers import (ProjectSerializer,)


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

        is_facebook_feed = True if self.request.POST.get('is_facebook_feed') == 'on' else False
        obj.is_facebook_feed = is_facebook_feed
        obj.save(update_fields=['data'])

        if is_facebook_feed is True:
            get_facebook_details.send(sender=self, instance=obj, created=True)
            get_facebook_feed.send(sender=self, instance=obj, user=self.request.user, created=True)
            populate_playlist_with_feed.send(sender=self, playlist=obj.playlist_set.all().first(), project=obj)

        return super(ProjectViewSet, self).post_save(obj, created=created)
