# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from jsonfield import JSONField

import hashlib


class FeedItem(models.Model):
    project = models.ForeignKey('project.Project')
    facebook_crc = models.CharField(max_length=255)

    name = models.CharField(null=True, blank=True, max_length=255)
    message = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated_time = models.DateTimeField(auto_now=True, auto_now_add=True)

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

    def __unicode__(self):
        return u'%s (%s)' % (self.name,
                             self.project_name)

    def get_absolute_url(self):
        return reverse('project:feeditem_detail', kwargs={'slug': self.project.slug, 'pk': self.pk})
