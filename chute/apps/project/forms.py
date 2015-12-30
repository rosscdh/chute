# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, HTML, Fieldset, Div, ButtonHolder, Submit
from parsley.decorators import parsleyfy

from .models import (Project,
                      ProjectCollaborator)
from .signals import (get_facebook_details,
                      get_facebook_feed,
                      populate_playlist_with_feed,)


from urlparse import urlparse


@parsleyfy
class ProjectForm(forms.ModelForm):
    is_facebook_feed = False
    is_rss_atom = False

    name = forms.CharField(label='Name of Project',
                           help_text='Enter a name for this project')

    url = forms.URLField(label='Facebook Page Address',
                         help_text='Enter the complete url to a facebook page',
                         widget=forms.TextInput(attrs={'placeholder': 'https://www.facebook.com/41061info'}),
                         required=False)

    class Meta:
        model = Project
        fields = ('url', 'name',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.token = self.user.facebook_token()

        self.helper = FormHelper()
        self.helper.attrs = {
            'id': 'create-project-form',
            'parsley-validate': ''
        }
        self.helper.form_show_errors = True
        self.helper.form_action = 'project:create'

        self.helper.layout = Layout(
            HTML('{% include "partials/form-errors.html" with form=form %}'),
            Fieldset(
                'Create a Project',
                Div(
                    Field('name'),
                    css_class='form-name clearfix'
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Save')
            )
        )
        if self.token:
            self.helper.layout.extend([
                Fieldset(
                    'Facebook Page',
                    Div(
                        Field('url'),
                        css_class='form-name clearfix'
                    ),
                )
            ])

        super(ProjectForm, self).__init__(*args, **kwargs)

    def clean_url(self):
        data = self.cleaned_data.copy()
        url = data.get('url')
        parsed_url = urlparse(url)

        if 'facebook.com' not in parsed_url.netloc:
            self.is_rss_atom = False
            self.is_facebook_feed = False
            ## set the name
            data['name'] = parsed_url.netloc
        else:

            if self.token is not None:
                raise ValidationError('Sorry, unable to parse facebook feeds without you connecting your facebook account with this account')

            self.is_facebook_feed = True
        return url

    def save(self, *args, **kwargs):
        project = super(ProjectForm, self).save(*args, **kwargs)

        collaborator, is_new = ProjectCollaborator.objects.get_or_create(user=self.user, project=project)

        if self.is_facebook_feed is True:
            project.is_facebook_feed = True
            get_facebook_details.send(sender=self, instance=project, created=True)
            get_facebook_feed.send(sender=self, instance=project, user=self.user, created=True)
            populate_playlist_with_feed.send(sender=self, playlist=project.playlist_set.all().first(), project=project)
        else:
            project.is_rss_atom = True

        return project
