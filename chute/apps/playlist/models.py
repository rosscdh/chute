# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse_lazy

from .signals import ensure_playlist_slug

from jsonfield import JSONField


class Playlist(models.Model):
    slug = models.SlugField(blank=True)  # blank to allow slug to be auto-generated
    name = models.CharField(max_length=255)

    project = models.ForeignKey('project.Project')
    feed = models.ManyToManyField('project.FeedItem')

    data = JSONField(default={})

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse_lazy('project:detail', kwargs={'slug': self.slug})

#
# Signals
#
pre_save.connect(ensure_playlist_slug, sender=Playlist, dispatch_uid='playlist.pre_save.ensure_playlist_slug')
