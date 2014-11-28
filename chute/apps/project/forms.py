# -*- coding: utf-8 -*-
from django import forms
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from .models import (Project,)

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, HTML, Fieldset, Div, ButtonHolder, Submit
from parsley.decorators import parsleyfy


@parsleyfy
class ProjectForm(forms.ModelForm):

    # client = forms.CharField(
    #     error_messages={
    #         'required': "Client name can not be blank."
    #     },
    #     help_text='',
    #     label='Client name',
    #     required=True,
    #     max_length=200,
    #     widget=forms.TextInput(attrs={
    #         'autocomplete': 'off',
    #         'placeholder': 'Acme Inc',
    #         'size': '40',
    #         # Typeahead
    #         'data-items': '4',
    #         'data-provide': 'typeahead',
    #         'data-source': '[]'
    #     })
    # )
    is_facebook_feed = forms.BooleanField(widget=forms.CheckboxInput)

    class Meta:
        model = Project
        exclude = ('slug', 'collaborators', 'data',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        try:
            self.user.auth_token
            self.has_auth_tokens = True
        except:
            self.has_auth_tokens = False

        self.helper = FormHelper()
        self.helper.attrs = {
            'id': 'create-project-form',
            'parsley-validate': ''
        }
        self.helper.form_show_errors = False

        self.helper.layout = Layout(
            HTML('{% include "partials/form-errors.html" with form=form %}'),
            Fieldset(
                '',
                Div(
                    Field('name', css_class=''),
                    css_class='form-name clearfix'
                ),
                Div(
                    Field('is_facebook_feed', css_class=''),
                    css_class='form-name clearfix'
                ) if self.has_auth_tokens else HTML(
                'You should really have connected using Facebook Auth'
                ),
                #Field('client'),
            ),
            ButtonHolder(
                Submit('submit', 'Create')
            )
        )
        super(ProjectForm, self).__init__(*args, **kwargs)
