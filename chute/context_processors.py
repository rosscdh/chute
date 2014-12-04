# -*- coding: utf-8 -*-
from django.conf import settings


def GLOBALS(request, **kwargs):
    return {
        'AWS_ACCESS_KEY_ID': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
        'AWS_STORAGE_BUCKET_NAME': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
        'PUSHER_APP_ID': getattr(settings, 'PUSHER_APP_ID', None),
        'PUSHER_KEY': getattr(settings, 'PUSHER_KEY', None),
    }