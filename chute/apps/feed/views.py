# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic.edit import ModelFormMixin
from django.views.generic import (DetailView, FormView, UpdateView,)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import StaticHTMLRenderer


from chute.apps.project.api.serializers import (ProjectMiniSerializer,)
from chute.apps.project.models import (Project,)

from .models import (FeedItem,)
from .api.serializers import (FeedItemSerializer,)
from .tasks import download_and_store_video
from .forms import VideoFeedItemForm

import base64
import hmac
import sha


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


class VideoFeedItemForm(FormView, ModelFormMixin):
    template_name = 'feed/feeditem_form.html'
    form_class = VideoFeedItemForm
    model = FeedItem

    def dispatch(self, request, **kwargs):
        self.project = Project.objects.get(slug=kwargs.get('project_slug'))
        self.object = self.get_object()
        return super(VideoFeedItemForm, self).dispatch(request=request, **kwargs)

    def get_object(self, **kwargs):
        if self.kwargs.get('slug') is not None:
            return self.model.objects.get(slug=self.kwargs.get('slug'))
        return None

    def get_form_kwargs(self):
        kwargs = super(VideoFeedItemForm, self).get_form_kwargs()
        kwargs.update({
            'project': self.project
        })
        return kwargs

    def get_success_url(self):
        return reverse('project:detail', kwargs={'slug': self.project.slug})


class S3SignatureEndpoint(APIView):
    """
    Provide a signed key for the sending object
    """
    renderer_classes = (StaticHTMLRenderer,)

    def get(self, request, **kwargs):
        to_sign = str(request.GET.get('to_sign'))
        signature = base64.b64encode(hmac.new(settings.AWS_SECRET_ACCESS_KEY, to_sign, sha).digest())

        return Response(signature, status=http_status.HTTP_200_OK)


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

        download_and_store_video.delay(video=feed_object.video_set.all().first())

        return super(VideoTranscodeWebhookView, self).post(request, **kwargs)
