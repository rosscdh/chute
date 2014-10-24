# -*- coding: utf-8 -*-
# from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, check_password

#from revision.apps.invite.models import InviteKey

import logging
logger = logging.getLogger('django.request')


class EmailBackend(object):
    def authenticate(self, username=None, password=None):
        # Check the username/password and return a User.
        user = None
        pwd_valid = False

        if '@' in username:
            email = User.objects.normalize_email(username)

            try:
                user = User.objects.get(email=email)
                pwd_valid = check_password(password, user.password)
            except User.DoesNotExist:
                logger.error('User does not exist: %s' % username)

            if user and pwd_valid:
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# class SecretKeyBackend(EmailBackend):
#     """
#     Used to log users in using nothing but a secret magic key
#     """
#     def authenticate(self, username=None, password=None):
#         # Check the username/password and return a User.
#         user = None

#         try:
#             invite = InviteKey.objects.get(key=username)
#             if invite.has_been_used is True:
#                 logger.error('InviteKey has already been used: %s' % username)
#                 raise ObjectDoesNotExist

#             user = invite.invited_user

#         except Exception as e:
#             logger.error('InviteKey does not exist: %s reason: %s' % (username, e))

#         return user
