# -*- coding: utf-8 -*-
from django.views.generic import (DetailView, UpdateView,)

from rest_framework.renderers import JSONRenderer
import django_rq

from chute.apps.project.api.serializers import (ProjectMiniSerializer,)

from .models import (FeedItem,)
from .api.serializers import (FeedItemSerializer,)
from .tasks import download_and_store_video


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


class VideoTranscodeWebhookView(UpdateView):
    template_name = 'feed/webhook.html'
    model = FeedItem
    http_method_names = [u'post']

    def post(self, request, **kwargs):
        """
        Recieve the webhook encoding complete from heywatch
        and then proceed to download and store the video object
        """
        feed_object = self.get_object()

        django_rq.enqueue(download_and_store_video, video=feed_object.video_set.all().first())

        return super(VideoTranscodeWebhookView, self).post(request, **kwargs)