# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, RedirectView, FormView

from chute.apps.me.mailers import ValidateEmailMailer

from .forms import SignUpForm, SignInForm
from .mixins import (UserNotFoundException,
                     UserInactiveException)
from .mixins import (SaveNextUrlInSessionMixin,
                     AuthenticateUserMixin,
                     LogOutMixin)

import urllib
import logging
logger = logging.getLogger('django.request')


class StartView(SaveNextUrlInSessionMixin,
                AuthenticateUserMixin,
                FormView):
    """
    sign in view
    """
    authenticated_user = None
    form_class = SignInForm
    template_name = 'public/start.html'

    def get_success_url(self):
        url = reverse('project:list')

        next = self.request.session.get('next')
        if next is not None:
            url = next

        return url

    def form_invalid(self, form):
        #analytics = AtticusFinch()
        ip_address = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))
        #analytics.anon_event('user.login.invalid', distinct_id=form.data.get('email'), ip_address=ip_address)
        return super(StartView, self).form_invalid(form=form)

    def form_valid(self, form):
        # user a valid form log them in
        try:
            logger.info('authenticating user: %s' % form.cleaned_data.get('email'))
            self.authenticated_user = self.get_auth(form=form)

        except (UserNotFoundException, UserInactiveException):
            return self.form_invalid(form=form)


        self.login(user=self.authenticated_user)

        #analytics = AtticusFinch()
        ip_address = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))
        #analytics.event('user.login', user=self.authenticated_user, ip_address=ip_address)

        logger.info('Signed-up IP_ADDRESS List: %s' % ip_address)

        return super(StartView, self).form_valid(form)


class SignUpView(LogOutMixin,
                 AuthenticateUserMixin,
                 FormView):
    """
    signup view
    """
    template_name = 'public/signup.html'
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('project:list') + '?' + urllib.urlencode({
            'firstseen': 1
        })

    def form_valid(self, form):
        # user a valid form log them in

        form.save()  # save the user
        self.authenticate(form=form)  # log them in

        mailer = ValidateEmailMailer(((self.request.user.get_full_name(), self.request.user.email,),))
        mailer.process(user=self.request.user)

        messages.info(self.request, 'Your account has been created. Please verify your email address. Check your email and click on the link that we\'ve sent you.')

        #analytics = AtticusFinch()
        #analytics.event('user.signup', user=self.request.user, ip_address=self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR')))

        return super(SignUpView, self).form_valid(form)


class LogoutView(LogOutMixin, RedirectView):
    """
    The logout view
    """
    url = '/'


class HomePageView(StartView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('project:list'))
        else:
            return super(HomePageView, self).dispatch(request, *args, **kwargs)


class DisclaimerView(TemplateView):
    template_name = 'public/disclaimer.html'


class PrivacyView(TemplateView):
    template_name = 'public/privacy.html'


class TermsView(TemplateView):
    template_name = 'public/terms.html'


class LoginErrorView(TemplateView):
    template_name = 'public/login-error.html'
