from django_rq import job

from .services import (VideoTranscodeCompleteService,
                       VideoTranscodeService,)

import logging
logger = logging.getLogger('django.request')


@job
def send_for_transcoding(video):
    logger.info('recieved task send_for_transcoding: %s' % video)
    transcode_service = VideoTranscodeService(video=video)
    transcode_service.create()
    return True


@job
def download_and_store_video(video):
    if video is not None:
        logger.info('recieved task download_and_store_video: %s' % video)
        download_service = VideoTranscodeCompleteService(video=video)
        download_service.download_and_store()
        return True