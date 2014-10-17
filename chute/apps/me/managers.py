# -*- coding: utf-8 -*-
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """
    Override the UserManager to ensure we prefetch the profile and related
    objects
    """
    def get_queryset(self):
        return super(CustomUserManager, self).get_queryset().select_related('profile')
