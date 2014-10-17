# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import (DisclaimerView,
                    HomePageView,
                    #InviteKeySignInView,
                    #VerifyTwoFactorView,
                    LogoutView,
                    PrivacyView,
                    SignUpView,
                    StartView,
                    TermsView,
                    LoginErrorView)


urlpatterns = patterns('',
    # Legal Pages
    url(r'^legal/disclaimer/$', DisclaimerView.as_view(), name='disclaimer'),
    url(r'^legal/privacy/$', PrivacyView.as_view(), name='privacy'),
    url(r'^legal/terms/$', TermsView.as_view(), name='terms'),

    url(r'^login-error/$', LoginErrorView.as_view(), name='login-error'),

    url(r'^start/$', StartView.as_view(), name='signin'),
    url(r'^start/signup/$', SignUpView.as_view(), name='signup'),

    #url(r'^start/invite/(?P<key>[-\w\d]+)/$', InviteKeySignInView.as_view(), name='invite'),
    #url(r'^start/invite/$', InviteKeySignInView.as_view(), name='invite_form'),

    url(r'^end/$', login_required(LogoutView.as_view()), name='logout'),
    url(r'^legal/terms/$', TemplateView.as_view(template_name='terms.html'), name='terms'),
    url(r'^welcome/$', TemplateView.as_view(template_name='public/welcome.html'), name='welcome'),

    url(r'^$', HomePageView.as_view(), name='home'),
)
