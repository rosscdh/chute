# -*- coding: utf-8 -*-
from django.db import models

from chute.utils import get_namedtuple_choices

from jsonfield import JSONField

#
# These are the master permissions set
# 1. Any change to this must be cascaded in the following permission dicts
#
GRANULAR_PERMISSIONS = (
    ("manage_participants", u"Can manage participants"),
    ("manage_document_reviews", u"Can manage document reviews"),
    ("manage_items", u"Can manage checklist items and categories"),
    ("manage_signature_requests", u"Can manage signatures & send documents for signature"),
    ("manage_clients", u"Can manage clients"),
    ("manage_tasks", u"Can manage item tasks"),
    ("manage_attachments", u"Can manage attachments on items"),
)
#
# Matter.owner (Workspace.lawyer)
#
PROJECT_OWNER_PERMISSIONS = dict.fromkeys([key for key, value in GRANULAR_PERMISSIONS], True)  # Grant the owner all permissions by default
#
# Matter.participants.user_class == 'lawyer'
#
PRIVILEGED_USER_PERMISSIONS = {
    "manage_participants": False,
    "manage_document_reviews": True,
    "manage_items": True,
    "manage_signature_requests": True,
    "manage_clients": False,
    "manage_tasks": True,
    "manage_attachments": True,
}
#
# Matter.participants.user_class == 'customer'|'client'
#
UNPRIVILEGED_USER_PERMISSIONS = {
    "manage_participants": False,
    "manage_document_reviews": False,
    "manage_items": False,
    "manage_signature_requests": False,
    "manage_clients": False,
    "manage_tasks": False,
    "manage_attachments": False,
}
#
# Not logged in or random user permissions
#
ANONYMOUS_USER_PERMISSIONS = dict.fromkeys([key for key, value in GRANULAR_PERMISSIONS], False)

ROLES = get_namedtuple_choices('ROLES', (
    (0, 'noone', 'No Access'),
    (1, 'owner', 'Owner'),
    (2, 'client', 'Client'),
    (3, 'colleague', 'Colleague'),
    (4, 'thirdparty', '3rd Party'),
))


class ProjectCollaborator(models.Model):
    """
    Model to store the Users permissions with regards to a project
    """
    # ROLES are simply for the GUI as ideally all of our users would
    # simple have 1 or more of a set of permission
    ROLES = ROLES
    PERMISSIONS = PROJECT_OWNER_PERMISSIONS.keys()  # as the PROJECT_OWNER_PERMISSIONS always has ALL of them
    PROJECT_OWNER_PERMISSIONS = PROJECT_OWNER_PERMISSIONS
    PRIVILEGED_USER_PERMISSIONS = PRIVILEGED_USER_PERMISSIONS
    UNPRIVILEGED_USER_PERMISSIONS = UNPRIVILEGED_USER_PERMISSIONS
    ANONYMOUS_USER_PERMISSIONS = ANONYMOUS_USER_PERMISSIONS

    project = models.ForeignKey('project.Project')
    user = models.ForeignKey('auth.User')
    is_project_owner = models.BooleanField(default=False, db_index=True)  # is this user a matter owner

    data = JSONField(default={})
    role = models.IntegerField(choices=ROLES.get_choices(), default=ROLES.client, db_index=True)  # default to client to meet the original requirements

    @property
    def display_role(self):
        return self.ROLES.get_desc_by_value(self.role)

    @property
    def role_name(self):
        return self.ROLES.get_name_by_value(self.role)

    @property
    def permissions(self):
        """
        combine the default permissions and override with the specific users
        permissions; this allows for the addition of new permissions easily
        """
        default_permissions = self.default_permissions().copy()
        user_permissions = self.data.get('permissions', default_permissions)
        default_permissions.update(user_permissions)
        return default_permissions

    @permissions.setter
    def permissions(self, value):
        if type(value) not in [dict] and len(value.keys()) > 0:
            raise Exception('ProjectCollaborator.permissions must be a dict of permissions %s' %
                            self.default_permissions())
        self.data['permissions'] = self.clean_permissions(**value)

    @classmethod
    def clean_permissions(cls, **kwargs):
        """
        Pass in a set of permissions and remove those that do not exist in
        the base set of permissions
        """
        kwargs_to_test = kwargs.copy()  # clone the kwargs dict so we can pop on it

        for permission in kwargs:
            if permission not in cls.PERMISSIONS:
                kwargs_to_test.pop(permission)
                # @TODO ? need to check for boolean value?
        return kwargs_to_test

    def __unicode__(self):
        return u'%s (%s)' % (self.user.get_full_name(), self.project.name)

    def default_permissions(self, user_class=None):
        """
        Class to provide a wrapper for user permissions
        The default permissions here MUST be kept up-to-date with the Workspace.Meta.permissions tuple
        """
        if self.is_project_owner is True or self.role == self.ROLES.owner or user_class == 'owner':
            return PROJECT_OWNER_PERMISSIONS

        # check the user is a participant
        if self.user in self.workspace.participants.all():
            # they are! so continue evaluation
            # cater to lawyer and client roles
            if self.role == self.ROLES.colleague or user_class == 'colleague':
                # Lawyers currently can do everything the owner can except clients and participants
                return PRIVILEGED_USER_PERMISSIONS

            elif self.role == self.ROLES.client or user_class == 'client':
                # Clients by default can currently see all items (allow by default)
                return UNPRIVILEGED_USER_PERMISSIONS

        # Anon permissions, for anyone else that does not match
        return ANONYMOUS_USER_PERMISSIONS

    def reset_permissions(self):
        self.permissions = self.default_permissions()

    def update_permissions(self, **kwargs):
        self.permissions = kwargs

    def has_permission(self, **kwargs):
        """
        .has_permission(manage_items=True)
        """
        permissions = self.permissions
        return all(req_perm in permissions and permissions[req_perm] == value for req_perm, value in kwargs.iteritems())
