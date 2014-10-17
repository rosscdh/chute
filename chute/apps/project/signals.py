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
populate_playlist_with_feed = Signal(providing_args=['playlist', 'project'])


@receiver(get_facebook_details)
def _get_facebook_details(sender, instance, created, **kwargs):
    """
    signal to handle getting the projects facebook details
    """
    service = FacebookProjectDetailService(project=instance)
    service.process()


@receiver(get_facebook_feed)
def _get_facebook_feed(sender, instance, user, created, **kwargs):
    """
    signal to handle getting the projects feeds from facebook
    """
    service = FacebookFeedGeneratorService(user=user,
                                           project=instance)
    service.process()


@receiver(populate_playlist_with_feed)
def _populate_playlist_with_feed(sender, playlist, project, **kwargs):
    """
    signal to handle populating a playlist from the current feed items
    """
    for f in project.feeditem_set.all():
        playlist.feed.add(f)


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


def ensure_project_has_atleast_one_playlist(sender, instance, **kwargs):
    try:
        instance.playlist_set.all()[0]

    except IndexError:
        # does not have a playlist item thus create it
        playlist = instance.playlist_set.model.objects.create(project=instance,
                                                              name='Playlist 1 for %s' % instance.name)
        instance.playlist_set.add(playlist)
