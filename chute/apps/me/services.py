# -*- coding: utf-8 -*-
"""
Generic Customer services
"""
from django.contrib.auth.models import User

from chute.utils import _get_unique_username

import logging
logger = logging.getLogger('django.request')


class EnsureCollaboratorService(object):
    """
    Service to get or create a Collaborator User
    """
    def __init__(self, project, email, full_name=None):
        self.project = project
        self.email = email
        self.full_name = full_name
        self.is_new, self.user, self.profile, self.collaborator, self.collaborator_is_new = (None, None, None, None, None)

    def process(self):
        if self.email is None:
            logger.error('Email is None, cant create user')
            self.is_new, self.user, self.profile, self.collaborator, self.collaborator_is_new = (None, None, None, None, None)
        else:
            self.is_new, self.user, self.profile, self.collaborator, self.collaborator_is_new = self.get_user(email=self.email)
        return self.is_new, self.user, self.profile, self.collaborator, self.collaborator_is_new

    def get_user(self, email, **kwargs):

        try:
            user = User.objects.get(email=email, **kwargs)
            is_new = False

        except User.DoesNotExist:
            username = _get_unique_username(username=email.split('@')[0])
            user = User.objects.create(username=username,
                                       email=email,
                                       **kwargs)
            is_new = True

        profile = user.profile

        #
        # Set new users to validated email automaticaly
        #
        if is_new is True:
            profile.validated_email = True
            profile.save(update_fields=['data'])

        #
        # Set the users profile to customer by default to customer
        # unless its overridden
        #
        if is_new is True or 'user_class' not in profile.data:
            logger.info('Is a new User')
            profile.data['user_class'] = 'customer'
            profile.save(update_fields=['data'])

        # setup the name of the user
        update_fields = []

        # and set it if they exist but have no name
        if self.full_name is not None:
            logger.info('Full Name was provided')
            # extract the first and last name
            names = self.full_name.split(' ')

            if user.first_name in [None, '']:
                user.first_name = names[0]
                update_fields.append('first_name')
                logger.info('Updating first_name')

            if user.last_name in [None, '']:
                #
                # Try to account for multi barreled names like Crawford d'Heureuse
                #
                user.last_name = ' '.join(names[1:])
                update_fields.append('last_name')
                logger.info('Updating last_name')

            # save the user model if we have updates
            if update_fields:
                user.save(update_fields=update_fields)

        collaborator, collaborator_is_new = self.project.projectcollaborator_set.get_or_create(project=self.project, user=user)

        return is_new, user, profile, collaborator, collaborator_is_new
