# -*- coding: utf-8 -*-
from django.db import models

from uuidfield import UUIDField
from jsonfield import JSONField


class Box(models.Model):
    slug = UUIDField(auto=True,
                     db_index=True,
                     null=True)
    mac_address = models.CharField(max_length=64, db_index=True)
    project = models.ForeignKey('project.Project', null=True, blank=True)
    playlist = models.ForeignKey('playlist.Playlist', null=True, blank=True)
    data = JSONField(default={})

    @property
    def name(self):
        return self.data.get('name', None)

    @name.setter
    def name(self, value):
        self.data['name'] = value

    def __unicode__(self):
        return '%s - %s' % (self.name, self.mac_address)