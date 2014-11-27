# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import ButtonHolder, Div, HTML, Submit
#from crispy_forms.bootstrap import AppendedText, FieldWithButtons, PrependedText, StrictButton
from parsley.decorators import parsleyfy

from .models import FeedItem, Video

from urlparse import urlparse


@parsleyfy
class FeedItemForm(forms.ModelForm):
    class Meta:
        model = FeedItem

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(FeedItemForm, self).__init__(*args, **kwargs)


@parsleyfy
class VideoFeedItemForm(FeedItemForm):
    """
    Save a feedItem with an attached
    Video object
    """
    message = forms.CharField(label='Short message',
                              help_text='Enter a brief description of this video',
                              required=False,
                              widget=forms.Textarea)
    # hidden field to accept the s3 uploaded to url "video.pre_transcode_storage_url"
    video_url = forms.CharField(required=True,
                                widget=forms.HiddenInput)

    class Meta(FeedItemForm.Meta):
      fields = ('name', 'message', 'video_url',)

    def __init__(self, project, *args, **kwargs):
        self.project = project
        super(VideoFeedItemForm, self).__init__(*args, **kwargs)

        self.helper.form_id = 'video-feeditem-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.attrs = {
            'role': 'form',
            'data-parsley-validate': '',
        }

        self.helper.layout = Layout(
          HTML('{% include "partials/form-errors.html" with form=form %}'),
          HTML('<div id="placeholder-feeditem_video"></div>'),
          HTML('<div class=""><b>Please Note:</b> While the video is uploading please complete the rest of the form.</div>'),
          'name',
          'message',
          'video_url',
          ButtonHolder(
              Submit('submit', 'Save', css_class='btn btn-primary btn-lg btn-wide'),
              css_class='form-group'
          )
        )

    def clean_video_url(self):
        url = urlparse(self.cleaned_data['video_url'])
        self.cleaned_data['video_url'] = '%s://%s%s' % (url.scheme, url.netloc, url.path)
        return self.cleaned_data

    def save(self, **kwargs):
        feed_item = super(VideoFeedItemForm, self).save(commit=False)
        feed_item.project = self.project
        feed_item.post_type = feed_item.POST_TYPES.video
        feed_item.template = feed_item.TEMPLATES.video_full
        feed_item.save()

        video = feed_item.video_set.create(
          name=feed_item.name,
          pre_transcode_storage_url=self.cleaned_data.get('video_url')
        )

        # Add to playlist
        playlist = self.project.playlist_set.all().first()
        playlist.feed.add(feed_item)

        return feed_item
