# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import ButtonHolder, Div, HTML, Submit
#from crispy_forms.bootstrap import AppendedText, FieldWithButtons, PrependedText, StrictButton

from .models import FeedItem, Video


class FeedItemForm(forms.ModelForm):
    class Meta:
        model = FeedItem

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(FeedItemForm, self).__init__(*args, **kwargs)


class VideoFeedItemForm(FeedItemForm):
    """
    Save a feedItem with an attached
    Video object
    """
    def __init__(self, *args, **kwargs):
        super(VideoFeedItemForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
          HTML('{% include "partials/form-errors.html" with form=form %}'),
          'name',
          'message',
          'description',
          'template',
          ButtonHolder(
              Submit('submit', 'Continue', css_class='btn btn-primary btn-lg btn-wide'),
              css_class='form-group'
          )
        )

    def save(self, **kwargs):
      import pdb;pdb.set_trace()