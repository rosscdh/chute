# -*- coding: utf-8 -*-
from django.conf import settings


def GLOBALS(request, **kwargs):
    return {
        'AWS_ACCESS_KEY_ID': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
        'AWS_STORAGE_BUCKET_NAME': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
    }