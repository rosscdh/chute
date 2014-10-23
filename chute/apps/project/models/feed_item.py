# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from jsonfield import JSONField

from chute.utils import get_namedtuple_choices

import hashlib

CORE_POST_TYPES = get_namedtuple_choices('TEMPLATES', (
    (0, 'link', 'Link'),
    (1, 'status', 'Status'),
    (2, 'photo', 'Photo'),
    (3, 'video', 'Video'),
))

CORE_TEMPLATES = get_namedtuple_choices('TEMPLATES', (
    ('basic', 'basic', 'Basic Template'),
))


class FeedItem(models.Model):
    POST_TYPES = CORE_POST_TYPES
    TEMPLATES = CORE_TEMPLATES

    project = models.ForeignKey('project.Project')
    facebook_crc = models.CharField(max_length=255)

    name = models.CharField(null=True, blank=True, max_length=255)
    message = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    post_type = models.IntegerField(choices=POST_TYPES.get_choices())

    wait_for = models.IntegerField(default=20)
    template = models.CharField(choices=TEMPLATES.get_choices(), default=TEMPLATES.basic, max_length=64)

    updated_time = models.DateTimeField(null=True, auto_now=True, auto_now_add=True)

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
