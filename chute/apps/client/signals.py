# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save

from chute.utils import _model_slug_exists

from .models import Client


import uuid
import logging
logger = logging.getLogger('django.request')


@receiver(pre_save, sender=Client, dispatch_uid='client.ensure_slug')
def ensure_client_slug(sender, instance, **kwargs):
    """
    signal to handle creating the workspace slug
    """

    if instance.slug in [None, '']:

        final_slug = slugify(instance.name)[:32]

        while _model_slug_exists(model=Client, slug=final_slug):
            logger.info('Client %s exists, trying to create another' % final_slug)

            slug = '%s-%s' % (final_slug, uuid.uuid4().get_hex()[:4])
            slug = slug[:30]
            final_slug = slugify(slug)

        instance.slug = final_slug