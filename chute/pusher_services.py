# -*- coding: UTF-8 -*-
from django.conf import settings

import pusher
import json

import logging
logger = logging.getLogger('django.request')

pusher.host = 'localhost'
pusher.port = '4567'

PUSHER_APP_ID = getattr(settings, 'PUSHER_APP_ID', None)
PUSHER_KEY = getattr(settings, 'PUSHER_KEY', None)
PUSHER_SECRET = getattr(settings, 'PUSHER_SECRET', None)

if PUSHER_APP_ID is None:
    raise Exception("You must specify a PUSHER_APP_ID in your local_settings.py")
if PUSHER_KEY is None:
    raise Exception("You must specify a PUSHER_KEY in your local_settings.py")
if PUSHER_SECRET is None:
    raise Exception("You must specify a PUSHER_SECRET in your local_settings.py")


class PusherPublisherService(object):
    """ Service to push data out to channels on pusher.com
    so the js lib can pick them up """
    channels = None
    event = None
    data = {}

    def __init__(self, channel, event, **kwargs):
        # is we pass in a tuple or list (iterable)
        # otherwise make it a list
        self.channels =  channel if hasattr(channel, '__iter__') else [channel]
        self.event = event

        # append our core data
        self.data.update(kwargs)

        logger.debug('Initialized PusherPublisherService with {data}'.format(data=json.dumps(self.data)))

        if not settings.IS_TESTING:
            self.pusher = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)

    def process(self, **kwargs):
        if not settings.IS_TESTING:

            if 'event' not in kwargs:
                kwargs.update({'event': self.event})

            self.data.update(kwargs)

            for channel in self.channels:
                logger.debug('Sending pusher event on #{channel}'.format(channel=channel))

                self.data.update({
                    'channel': channel,
                })

                try:
                    self.pusher[channel].trigger(self.event, self.data)
                except pusher.UnexpectedReturnStatusError:
                    # ebcause this is a valid response from slanger
                    pass


class PusherAuthService(object):
    """
    Authenticate a presence channel
    """
    channel_name = None
    socket_id = None

    def __init__(self, channel_name, socket_id, **kwargs):
        # is we pass in a tuple or list (iterable)
        # otherwise make it a list
        self.channel_name = channel_name
        self.socket_id = socket_id
        self.data = kwargs

        logger.debug('PusherAuthService with channel_name: %s, socket_id: %s' % (channel_name, socket_id))

        if not settings.IS_TESTING:
            self.pusher = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)

    def process(self, **kwargs):
        if not settings.IS_TESTING:
            logger.debug('Pusher auth on #{channel}'.format(channel=self.channel_name))

            self.data.update({
                'user_id': self.socket_id,
                'user_info': {'name':'Test Name'},
            })

            auth = {}

            try:
                auth = self.pusher[self.channel_name].authenticate(self.socket_id, self.data)
            except:
                # unfortunately pusher lib does not implement decent validation
                pass
            return auth
