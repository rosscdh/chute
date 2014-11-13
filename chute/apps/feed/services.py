# -*- coding: utf-8 -*-
from django.conf import settings
from vimeo import vimeo


class VimeoChannelVideos(object):

  def __init__(self, channel):
    self.channel = channel
    self.vimeo = vimeo.VimeoClient(
                      token='3aa4d9272b68b43bef2a9ee8c5aababd',
                      key=settings.VIMEO_PUBLIC_KEY,
                      secret=settings.VIMEO_SECRET_KEY)
  def process(self):
    pass