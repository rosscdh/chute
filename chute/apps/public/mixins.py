# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout

import logging
logger = logging.getLogger('django.request')


class UserInactiveException(Exception):
    message = 'User is not active'


class UserNotFoundException(Exception):
    message = 'User could not be authenticated'


class AuthenticateUserMixin(object):
    def get_auth(self, form):
        return authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])

    def authenticate(self, form):
        user = self.get_auth(form=form)
        self.login(user=user)

    def login(self, user=None):
        if user is not None:
            logger.info('user is authenticated: %s' % user)

            if user.is_active:
                logger.info('user is active: %s' % user)
                login(self.request, user)
            else:
                logger.info('user is not active: %s' % user)
                raise UserInactiveException
        else:
            logger.info('User not authenticated')
            raise UserNotFoundException


class LogOutMixin(object):
    """
    Mixin that will log the current user out
    and continue showing the view as an non authenticated user
    """
    def dispatch(self, request, *args, **kwargs):
        """
        If the user is logged in log them out
        """
        if request.user.is_authenticated() is True:
            logout(request)

        return super(LogOutMixin, self).dispatch(request, *args, **kwargs)


class SaveNextUrlInSessionMixin(object):
    """
    A mixin that will save a ?next=/path/to/next/page
    url in the session
    """
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next', None)
        self.save_next_in_session(next=next)
        return super(SaveNextUrlInSessionMixin, self).get(request, *args, **kwargs)

    def save_next_in_session(self, next=None):
        if next is not None:
            self.request.session['next'] = next
