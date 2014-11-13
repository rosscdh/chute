# -*- coding: utf-8 -*-
from django.views.generic import (DetailView,)
from rest_framework.renderers import JSONRenderer

from chute.apps.project.api.serializers import (ProjectMiniSerializer,)

from .models import (FeedItem,)
from .api.serializers import (FeedItemSerializer,)


class FeedItemDetail(DetailView):
    """
    individual feed item used for the primary interface selection display
    """
    template_name = 'clean-blog/post.html'
    model = FeedItem

    @property
    def project_json(self):
        return JSONRenderer().render(ProjectMiniSerializer(self.object.project,
                                     context={'request': self.request}).data)

    @property
    def feed_json(self):
        return JSONRenderer().render(FeedItemSerializer((self.object,),
                                                        many=True,
                                                        context={'request': self.request}).data)

