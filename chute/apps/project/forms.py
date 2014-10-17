# -*- coding: utf-8 -*-
from django import forms

from .models import (Project,)

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Field, Layout, HTML, Fieldset, Div, ButtonHolder, Submit
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

    class Meta:
        model = Project
        exclude = ('slug', 'collaborators', 'data',)

    def __init__(self, *args, **kwargs):
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
                #Field('client'),
            ),
            ButtonHolder(
                Submit('submit', 'Create')
            )
        )
        super(ProjectForm, self).__init__(*args, **kwargs)
