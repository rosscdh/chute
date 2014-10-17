# -*- coding: utf-8 -*-
from django.db import models

from jsonfield import JSONField

import hashlib


class FeedItem(models.Model):
    project = models.ForeignKey('project.Project')
    facebook_crc = models.CharField(max_length=255)
    data = JSONField(default={})

    @staticmethod
    def crc(*args):
        hasher = hashlib.md5()
        for item in args:
            if item is not None:
                hasher.update(item)
        return hasher.hexdigest()

    @property
    def project_name(self):
        return self.data.get('from', {}).get('name')

    @property
    def name(self):
        return self.data.get('name')

    def __unicode__(self):
        return u'%s (%s)' % (self.name,
                             self.project_name)