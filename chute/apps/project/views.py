# -*- coding: utf-8 -*-
from django.views.generic import (CreateView,
                                  DetailView,
                                  ListView,)

from django.views.generic.edit import FormMixin

from rest_framework.renderers import JSONRenderer

from chute.apps.playlist.api.serializers import (PlaylistSerializer,)

from .api.serializers import (ProjectSerializer,)

from .forms import ProjectForm

from .models import (Project,
                     FeedItem)


class ProjectListView(ListView,
                      FormMixin):
    model = Project
    form_class = ProjectForm

    @property
    def project_json(self):
        return JSONRenderer().render(ProjectSerializer(self.get_queryset(),
                                                       many=True,
                                                       context={'request': self.request}).data)

    def get_queryset(self, **kwargs):
        return self.model._default_manager.filter(collaborators__in=[self.request.user])

    def get_context_data(self, **kwargs):
        kwargs = super(ProjectListView, self).get_context_data(**kwargs)
        kwargs.update({
            'form': self.get_form(form_class=self.form_class)
        })
        return kwargs


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm


class ProjectDetailView(DetailView):
    model = Project

    @property
    def project_json(self):
        return JSONRenderer().render(ProjectSerializer(self.object,
                                     context={'request': self.request}).data)

    @property
    def playlist_json(self):
        return JSONRenderer().render(PlaylistSerializer(self.object.playlist_set.all(),
                                                        many=True,
                                                        context={'request': self.request}).data)


class FeedItemDetail(DetailView):
    template_name = 'clean-blog/post.html'
    model = FeedItem

    def get_context_data(self, **kwargs):
        kwargs = super(FeedItemDetail, self).get_context_data(**kwargs)

        kwargs.update(self.object.data)

        kwargs.update({
            'name': self.object.name,
            'message': self.object.message,
            'description': self.object.description,
            'project': self.object.project.data
        })
        return kwargs
