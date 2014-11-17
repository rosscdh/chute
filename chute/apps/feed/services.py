# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

# from vimeo import vimeo
import heywatch

HEYWATCH = settings.get('HEYWATCH', {})


# class VimeoChannelVideos(object):

#   def __init__(self, channel):
#     self.channel = channel
#     self.vimeo = vimeo.VimeoClient(
#                       token='3aa4d9272b68b43bef2a9ee8c5aababd',
#                       key=settings.VIMEO_PUBLIC_KEY,
#                       secret=settings.VIMEO_SECRET_KEY)
#   def process(self):
#     pass


class VideoTranscodeService(object):
  def __init__(self, video):
    self.video = video
    self.hw = heywatch.API(HEYWATCH.get('USERNAME'),
                           HEYWATCH.get('PASSWORD'))

  @property
  def webhook_url(self):
    return HEYWATCH.get('WEBHOOOK_URL', self.video.get_webhook_url())

  def create(self):

    download_resp = self.hw.create('download',
                                   url='http://site.com/yourvideo.mp4',
                                   title='yourtitle')

    job_resp = self.hw.create('job',
                              video_id=download_resp.get('video_id'),
                              format_id='mp4_720p',
                              keep_video_size=True,
                              ping_url_after_encode=self.webhook_url,
                              s3_directive='s3://accesskey:secretkey@myvideobucket/flv/123434.flv')
