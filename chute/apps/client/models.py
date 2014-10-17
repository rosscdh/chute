# -*- coding: utf-8 -*-
from django.db import models

#from rulez import registry as rulez_registry
from jsonfield import JSONField

from .managers import ClientManager


class Client(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    owner = models.ForeignKey('auth.User', related_name='clients')
    data = JSONField(default={})

    objects = ClientManager()

    def __unicode__(self):
        return self.name

    def can_read(self, user):
        return self.lawyer == user

    def can_edit(self, user):
        return self.lawyer == user

    def can_delete(self, user):
        return self.lawyer == user


# rulez_registry.register("can_read", Client)
# rulez_registry.register("can_edit", Client)
# rulez_registry.register("can_delete", Client)


from .signals import (ensure_client_slug,)
