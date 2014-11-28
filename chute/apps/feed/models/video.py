# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import slugify

from chute.utils import (get_namedtuple_choices, _managed_S3BotoStorage)

from ..signals import send_video_for_transcoding
from ..tasks import send_for_transcoding

from jsonfield import JSONField
from uuidfield import UUIDField

import os
import math
import django_rq


BASE_VIDEO_TYPES = get_namedtuple_choices('BASE_VIDEO_TYPES', (
    (1, 'video_mp4', 'video/mp4'),
    (2, 'video_mov', 'video/mov'),
    (3, 'video_ogg', 'video/ogg'),
))

BASE_TRANSCODE_STATE = get_namedtuple_choices('BASE_TRANSCODE_STATE', (
    (0, 'error', 'Error'),
    (1, 'pending', 'Pending Transcode'),
    (2, 'in_progress', 'In-Progress'),
    (3, 'transcode_complete', 'Transcode Complete'),
))


def _upload_video(instance, filename):
    split_file_name = os.path.split(filename)[-1]
    filename_no_ext, ext = os.path.splitext(split_file_name)

    identifier = '%s' % instance.slug
    full_file_name = '%s-%s%s' % (identifier, slugify(filename_no_ext), ext)

    if identifier in slugify(filename):
        #
        # If we already have this filename as part of the recombined filename
        #
        full_file_name = filename

    return 'uploaded_video/%s' % full_file_name


class Video(models.Model):
    """
    Video Version model
    """
    VIDEO_TYPES = BASE_VIDEO_TYPES
    TRANSCODE_STATE = BASE_TRANSCODE_STATE

    slug = UUIDField(auto=True,
                     db_index=True)
    feed_item = models.ForeignKey('feed.FeedItem')
    name = models.CharField(help_text='Name by which this video will be known', max_length=255)

    video_url = models.URLField(db_index=True)  # stores the initial s3 uplaoded url
    video = models.FileField(upload_to=_upload_video,
                             storage=_managed_S3BotoStorage(),
                             max_length=255,
                             null=True,
                             blank=True)

    video_type = models.IntegerField(choices=VIDEO_TYPES.get_choices(),
                                     default=VIDEO_TYPES.video_mp4,
                                     db_index=True)
    transcode_state = models.IntegerField(choices=TRANSCODE_STATE.get_choices(),
                                          default=TRANSCODE_STATE.pending,
                                          db_index=True)
    # store the retrieved video id for lookups
    # 0 is a HeyWAtch convention means not-processed
    video_id = models.IntegerField(default=0, blank=True, null=True, db_index=True)

    data = JSONField(default={})

    class Meta:
        ordering = ['-id']

    @classmethod
    def secs_to_stamp(cls, secs):
        secs, part = str(secs).split('.')
        secs = int(secs)
        part = int(part[0:3])
        minutes = math.floor(secs / 60)
        seconds = round(secs - minutes * 60, 2)
        hours = math.floor(secs / 3600)
        #time = time - hours * 3600;
        return '%02d:%02d:%02d.%03d' % (hours, minutes, seconds, part)

    @property
    def display_type(self):
        return self.VIDEO_TYPES.get_desc_by_value(self.video_type)

    @property
    def pre_transcode_storage_url(self):
        return self.data.get('pre_transcode_storage_url', None)

    @pre_transcode_storage_url.setter
    def pre_transcode_storage_url(self, value):
        self.data['pre_transcode_storage_url'] = value

    @property
    def download_info(self):
        return self.data.get('download_info', {})

    @download_info.setter
    def download_info(self, value):
        self.data['download_info'] = value

    @property
    def download_id(self):
        return self.data.get('download_info', {}).get('id', 0)  # 0 is heywatches convention

    @download_id.setter
    def download_id(self, value):
        self.download_info['id'] = value

    @property
    def job_info(self):
        return self.data.get('job_info', {})

    @job_info.setter
    def job_info(self, value):
        self.data['job_info'] = value

    @property
    def is_transcode_pending(self):
        return self.transcode_state == self.TRANSCODE_STATE.pending

    @property
    def display_transcode_state(self):
        return self.TRANSCODE_STATE.get_desc_by_value(self.transcode_state)

    def __unicode__(self):
        return u'%s' % self.name

    def get_webhook_url(self):
        return reverse_lazy('feed:webhook_heywatch', kwargs={'pk': self.feed_item.pk})

    def transcode(self):
        send_for_transcoding.delay(video=self)
        #django_rq.enqueue(send_for_transcoding, video=self)

    # def get_absolute_url(self):
    #     return reverse_lazy('project:with_video_detail', kwargs={'slug': self.project.slug, 'version_slug': str(self.slug)})


#
# Signals
#
post_save.connect(send_video_for_transcoding,
                  sender=Video,
                  dispatch_uid='video.post_save.transcode_original_video')
