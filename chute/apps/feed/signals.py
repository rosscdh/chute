# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save

from .models import Video
from .services import VideoTranscodeService

import uuid
import logging
logger = logging.getLogger('django.request')


@receiver(pre_save, sender=Video, dispatch_uid='feed.send_video_for_encoding')
def ensure_client_slug(sender, instance, created, **kwargs):
    """
    Send a newly created video object for encoding
    1. user uploads direct to s3 using the javascript helper
    2. that url is saved in video.pre_transcode_storage_url
    3. that url is then sent to be transcoded
    """
    if created:
        service = VideoTranscodeService(video=instance)
        service.create()

    # else:
    #     """
    #     if the video exists then we need to
    #     1. check that the video.pre_transcode_storage_url has not changed
    #     2. if it has then we need to send it for transcoding again
    #     """
    #     previous = instance.__class__.objects.get(pk=instance.pk)

    #     if previous.pre_transcode_storage_url != instance.pre_transcode_storage_url:
    #         service = VideoTranscodeService(video=instance)
    #         service.re_create()            
