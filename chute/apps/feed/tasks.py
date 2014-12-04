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
def download_and_store_video(video, **kwargs):
    """
    **kwargs looks like:
    encoded_video_id    ["46537298"]
    encoded_video_url   [""]
    filename    ["webm_4.webm"]
    format_id   ["webm"]
    heywatch_ping_type  ["encode"]
    job_id  ["25044580"]
    link    ["http://heywatch.com/encoded_video/46537298.bin"]
    video_id    ["46537291"]
    """
    if video is not None:
        logger.info('recieved task download_and_store_video: %s' % video)
        download_service = VideoTranscodeCompleteService(video=video, filename=kwargs.get('filename'))
        download_service.download_and_store()
        return True