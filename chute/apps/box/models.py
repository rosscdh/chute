# -*- coding: utf-8 -*-
from django.db import models

from uuidfield import UUIDField
from jsonfield import JSONField


class Box(models.Model):
    slug = UUIDField(auto=True,
                     db_index=True,
                     null=True)
    project = models.ForeignKey('project.Project')
    playlist = models.ForeignKey('playlist.Playlist')
    data = JSONField(default={})

    @property
    def mac_address(self):
        return self.data.get('mac_address', None)

    @mac_address.setter
    def mac_address(self, value):
        self.data['mac_address'] = value
