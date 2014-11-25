# -*- coding: utf-8 -*-
from django import forms

from .models import FeedItem, Video


class FeedItemForm(forms.ModelForm):
    class Meta:
        model = FeedItem


class VideoFeedItemForm(FeedItemForm):
    """
    Save a feedItem with an attached
    Video object
    """
    def save(self, **kwargs):
      import pdb;pdb.set_trace()