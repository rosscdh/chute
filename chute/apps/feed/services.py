# -*- coding: utf-8 -*-
from django.core import files
from django.conf import settings

# from vimeo import vimeo
import requests
from requests.auth import HTTPBasicAuth

import coconut

import tempfile
import time

import logging
logger = logging.getLogger('django.request')


HEYWATCH = getattr(settings, 'HEYWATCH', {})


class VideoTranscodeService(object):
    PREFERRED_FORMAT = 'webm'  # http://www.heywatchencoding.com/h265

    # http://www.heywatchencoding.com/http-live-streaming-tutorial

    def __init__(self, video, **kwargs):
        self.video = video
        self.video_api = coconut.API(HEYWATCH.get('USERNAME'),
                                     HEYWATCH.get('PASSWORD'))

    def retrieve_video_id(self, download_id):
        """
        Loop a few times to try get teh video id as there is delay on their side
        """
        logger.info('Retrieving the video_id for download: %s' % download_id)

        counter = 0
        max_count = 10
        video_id = None

        while video_id in [0, None]:
            download_resp = self.video_api.info('download', download_id)

            video_id = download_resp.get('video_id', 0)  # returns 0 by default

            time.sleep(5)
            counter += 1
            if counter >= max_count:
                break

        if video_id not in [0, None]:
            # update the download resp info
            self.video.video_id = video_id
            self.video.download_info = download_resp

            if self.video.pk is not None:
                # only if we are updating an existing video
                self.video.save(update_fields=['video_id', 'data'])

        return video_id

    def fresh_video_details(self):
        logger.info('getting fresh_video_details')
        return self.video_api.info('video', self.video.video_id)

    def create(self):
        if not self.video.pre_transcode_storage_url:
            logger.error('no video.pre_transcode_storage_url defined for %s value is: %s' % (self.video, self.video.pre_transcode_storage_url))

        else:
            logger.info('Creating heywatch download object')
            download_resp = self.video_api.create('download',
                                           url=self.video.pre_transcode_storage_url,
                                           title=self.video.name)
            logger.info('heywatch download object: %s' % download_resp)
            self.video.download_info = download_resp

            if self.video.pk is not None:
                # only if we are updating an existing video
                self.video.save(update_fields=['data'])

            # Now create the video transcode job
            self.create_job()

    def re_create(self):
        """
        If the video.pre_transcode_storage_url is changed to a enw one
        we should then delete the old one
        """
        self.video.video.delete()  # remove the current transcoded file from s3
        # should probably also delete the current video.pre_transcode_storage_url
        # as there is a bit of a churn here
        # no issue a normal create event
        self.create()

    def create_job(self):
        """
        Should be made async
        """
        from chute.apps.public.templatetags.chute_tags import ABSOLUTE_BASE_URL

        job_resp = None
        video_id = self.retrieve_video_id(download_id=self.video.download_id)

        if video_id is not None:
            job_resp = self.video_api.create('job',
                                      video_id=video_id,
                                      format_id=self.PREFERRED_FORMAT,
                                      ping_url_after_encode=ABSOLUTE_BASE_URL(str(self.video.get_webhook_url())))

            # save the job response object
            self.video.job_info = job_resp
            # Update the status
            self.video.transcode_state = self.video.TRANSCODE_STATE.in_progress

            if self.video.pk is not None:
                # only if we are updating an existing video
                self.video.save(update_fields=['data', 'transcode_state'])

        return job_resp, self.video


class VideoTranscodeCompleteService(VideoTranscodeService):
    def __init__(self, video, filename, **kwargs):
        self.filename = filename
        super(VideoTranscodeCompleteService, self).__init__(video=video, **kwargs)

    def download_and_store(self):
        video_url = None

        if self.video.video_id in [0, None]:
            self.retrieve_video_id(download_id=self.video.download_id)

        # get a new version of the video details from HW
        video_info = self.fresh_video_details()
        specs = video_info.get('specs', {})
        thumbnails = specs.get('thumbnails', {})
        video = video_info.get('video', {})
        length_seconds = video_info.get('length', 60)

        video_pictures = [thumbnails.get('small'), thumbnails.get('medium'), thumbnails.get('large'),]

        # Update the status
        self.video.transcode_state = self.video.TRANSCODE_STATE.transcode_complete
        logger.debug('Upating video.transcode_state = transcode_complete: %s' % self.video)

        logger.info('Updating the video_url from fresh_video_details: %s' % self.video)
        # GET THE CONVERTED VIDEO URL FROM HEYWATCH
        video_url = video_info.get('link')

        if video_url is not None:
            logger.info('Downloading the video from: %s' % video_url)
            request = requests.get(video_url, auth=HTTPBasicAuth(settings.HEYWATCH.get('USERNAME'), settings.HEYWATCH.get('PASSWORD')), stream=True)

            if request.status_code != requests.codes.ok:
                # error out
                logger.error('Could not download the video: %s (video_id: %s) due to: %s' % (video_url, self.video.video_id, request))

            lf = tempfile.NamedTemporaryFile(suffix='.mov')

            # Read the streamed image in sections
            logger.debug('Writing downloaded file to local temp file: %s' % self.video)
            for block in request.iter_content(1024 * 8):
                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                lf.write(block)

            logger.debug('Saving file to video.video object (s3): %s' % self.video)
            #video_name = getattr(self.video, 'name', 'Untitled Video')
            #self.video.video.save(video_name, files.File(lf))
            self.video.video = files.File(lf)

        if self.video.pk is not None:
            # update wait for
            feed_item = self.video.feed_item
            feed_item.wait_for = length_seconds
            feed_item.save(update_fields=['wait_for'])
            # save teh video info
            self.video.data['video_info'] = video_info
            # only if we are updating an existing video
            self.video.save(update_fields=['video', 'video_url', 'transcode_state', 'data'])
