# -*- coding: utf-8 -*-
from django.dispatch import Signal, receiver
from django.template.defaultfilters import slugify

from chute.utils import _model_slug_exists

from chute.apps.project.services import (FacebookProjectDetailService,
                                         FacebookFeedGeneratorService)

import uuid
import logging
logger = logging.getLogger('django.request')


get_facebook_details = Signal(providing_args=['instance', 'created'])
get_facebook_feed = Signal(providing_args=['instance', 'user', 'created'])


def ensure_project_slug(sender, instance, **kwargs):
    """
    signal to handle creating the workspace slug
    """
    if instance.slug in [None, '']:

        final_slug = slugify(instance.name)[:32]

        while _model_slug_exists(model=instance.__class__.objects.model, slug=final_slug):
            logger.info('Project %s exists, trying to create another' % final_slug)
            slug = '%s-%s' % (final_slug, uuid.uuid4().get_hex()[:4])
            slug = slug[:30]
            final_slug = slugify(slug)

        instance.slug = final_slug


@receiver(get_facebook_details)
def _get_facebook_details(sender, instance, created, **kwargs):
    """
    signal to handle getting the projects facebook details
    """
    #if created is True and kwargs.get('update_fields', None) is None:
    if kwargs.get('update_fields', None) is None:
        service = FacebookProjectDetailService(project=instance)
        service.process()

@receiver(get_facebook_feed)
def _get_facebook_feed(sender, instance, user, created, **kwargs):
    """
    signal to handle getting the projects feeds from facebook
    """
    if kwargs.get('update_fields', None) is None:
        service = FacebookFeedGeneratorService(user=user,
                                         project=instance)
        service.process()


def ensure_project_has_atleast_one_playlist(sender, instance, **kwargs):
    try:
        instance.playlist_set.all()[0]

    except IndexError:
        # does not have a playlist item thus create it
        playlist = instance.playlist_set.model.objects.create(project=instance,
                                                              name='Playlist 1 for %s' % instance.name)
        instance.playlist_set.add(playlist)
