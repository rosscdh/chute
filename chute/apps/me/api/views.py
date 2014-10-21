# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status as http_status

from chute.apps.project.models import Project

from ..services import EnsureCollaboratorService
from .serializers import (UserSerializer,
                          CollaboratorSerializer,)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
    lookup_url_kwarg = 'email'
    filter_fields = ('email', 'username')
    allowed_methods = ('get', 'options', 'head',)


class CollaboratorEndpoint(generics.ListCreateAPIView,
                           generics.RetrieveDestroyAPIView):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    queryset = Project.objects.all()
    serializer_class = CollaboratorSerializer

    def list(self, request, **kwargs):
        self.project = self.get_object()
        collaborator_serializer = self.get_serializer(self.project.projectcollaborator_set.all(), many=True)
        headers = self.get_success_headers(collaborator_serializer)
        return Response(collaborator_serializer.data, status=http_status.HTTP_200_OK, headers=headers)

    def create(self, request, **kwargs):
        project = self.get_object()
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        full_name = '%s %s' % (first_name, last_name)

        service = EnsureCollaboratorService(project=project, email=email, full_name=full_name)
        is_new, user, profile, collaborator, collaborator_is_new = service.process()

        collaborator_serializer = self.get_serializer(project.projectcollaborator_set.all(), many=True)
        headers = self.get_success_headers(collaborator_serializer)

        status = http_status.HTTP_201_CREATED if collaborator_is_new is True else http_status.HTTP_202_ACCEPTED
        return Response(collaborator_serializer.data, status=status, headers=headers)

    # def retrieve(self, request, **kwargs):
    #     import pdb;pdb.set_trace()

    def destroy(self, request, **kwargs):
        project = self.get_object()
        collaborator_record = project.projectcollaborator_set.get(user__email=kwargs.get('email'))
        collaborator_record.delete()

        collaborator_serializer = self.get_serializer(project.projectcollaborator_set.all(), many=True)
        headers = self.get_success_headers(collaborator_serializer)

        return Response(collaborator_serializer.data, status=http_status.HTTP_202_ACCEPTED)