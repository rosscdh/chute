# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from .mixins import EmailIsValidatedMixin
from .managers import CustomUserManager

from jsonfield import JSONField
#from sorl.thumbnail.images import ImageFile

import logging
logger = logging.getLogger('django.request')


class UserProfile(EmailIsValidatedMixin,
                  models.Model):
    """
    Base User Profile, where we store all the interesting information about
    users
    """
    user = models.OneToOneField('auth.User',
                                unique=True,
                                related_name='profile')

    data = JSONField(default={})

    @property
    def firm_name(self):
        return self.data.get('firm_name', None)

    # @property
    # def firm_logo(self):
    #     firm_logo = self.data.get('firm_logo', None)
    #     if firm_logo is not None:
    #         return ImageFile(firm_logo)
    #     return firm_logo

    def __unicode__(self):
        return '%s <%s>' % (self.user.get_full_name(), self.user.email)


#
# Automatically create profile object for each new user model
#


def _get_or_create_user_profile(user):
    # set the profile
    try:
        # added like this so django noobs can see the result of get_or_create
        profile, is_new = UserProfile.objects.get_or_create(user=user)
        return (profile, is_new,)

    except Exception as e:
        logger.critical('transaction.atomic() integrity error: %s' % e)

    return (None, None,)


#
# User model overrides
#

# used to trigger profile creation by accidental refernce. Rather use the _create_user_profile def above
User.profile = property(lambda u: _get_or_create_user_profile(user=u)[0])
User.add_to_class('objects', CustomUserManager())


"""
Overide the user get_full_name method to actually return somethign useful if
there is no name.

Used to return the email address as their name, if no first/last name exist.
"""
def get_full_name(self, **kwargs):
    name = '%s %s' % (self.first_name, self.last_name)
    if name.strip() in ['', None]:
        name = self.email
    return name

User.add_to_class('get_full_name', get_full_name)


"""
Add in the get_initials method, which returns the user initials based on their
first and last name
"""
def get_initials(self):
    initials = None
    try:
        initials = '%s%s' % (self.first_name[0], self.last_name[0])
        initials = initials.strip().upper()
    except IndexError:
        pass

    if initials in ['', None]:
        return None
    return initials

User.add_to_class('get_initials', get_initials)
