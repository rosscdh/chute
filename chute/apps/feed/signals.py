# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('django.request')


def send_video_for_transcoding(sender, instance, created, **kwargs):
    """
    Send a newly created video object for encoding
    1. user uploads direct to s3 using the javascript helper
    2. that url is saved in video.pre_transcode_storage_url
    3. that url is then sent to be transcoded
    """
    if created is True and instance.is_transcode_pending is True:
        logger.info('Signal to transcode video: %s' % instance)
        instance.transcode()

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
