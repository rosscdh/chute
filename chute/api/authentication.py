# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication


class NoAuth(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        return (User.objects.get(pk=1), '1234567890')

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'NoAuth'
