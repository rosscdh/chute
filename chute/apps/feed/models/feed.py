# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from uuidfield import UUIDField
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
    (1, 'basic', 'Basic Template'),
    (2, 'image_left', 'Image Left'),
    (3, 'image', 'Image Simple'),
    (4, 'video_full', 'Fullscreen Video'),
))


class FeedItem(models.Model):
    POST_TYPES = CORE_POST_TYPES
    TEMPLATES = CORE_TEMPLATES

    slug = UUIDField(auto=True,
                     db_index=True,
                     null=True)

    project = models.ForeignKey('project.Project')
    provider_crc = models.CharField(max_length=255, null=True, blank=True)

    name = models.CharField(help_text='Name by which this item will be known', null=True, blank=True, max_length=255)
    message = models.TextField(null=True, blank=True)  # small info
    description = models.TextField(null=True, blank=True)  # big info
    post_type = models.IntegerField(choices=POST_TYPES.get_choices(), null=True)

    wait_for = models.IntegerField(default=20)
    template = models.IntegerField(choices=TEMPLATES.get_choices(),
                                default=TEMPLATES.basic)

    updated_time = models.DateTimeField(null=True, auto_now=True)

    data = JSONField(default={})

    class Meta:
        ordering = ['updated_time']

    @staticmethod
    def crc(*args):
        hasher = hashlib.md5()
        for item in args:
            if item is not None:
                hasher.update(item.encode('utf-8'))
        return hasher.hexdigest()

    @property
    def project_name(self):
        return self.data.get('from', {}).get('name')

    @property
    def template_name(self):
        return self.TEMPLATES.get_name_by_value(self.template)

    @property
    def post_type_name(self):
        return self.POST_TYPES.get_name_by_value(self.post_type)

    def __unicode__(self):
        return u'%s (%s)' % (self.name,
                             self.project_name)

    def get_absolute_url(self):
        return reverse('project:feeditem_detail', kwargs={'slug': self.project.slug, 'pk': self.pk})

