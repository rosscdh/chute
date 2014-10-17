# -*- coding: utf-8 -*-
from django.dispatch import Signal, receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from .mailers import WelcomeEmail

import logging
LOGGER = logging.getLogger('django.request')


send_welcome_email = Signal(providing_args=['sender', 'instance', 'created'])


@receiver(send_welcome_email, sender=User, dispatch_uid='me.send_welcome_email')
def on_send_welcome_email(sender, **kwargs):
    """
    signal to handle creating the workspace slug
    """
    is_new = kwargs.get('created')
    user = kwargs.get('instance')

    if is_new is True:
        name = user.get_full_name() if user.get_full_name() is not None else ''
        mailer_service = WelcomeEmail(recipients=((name, user.email),))
        mailer_service.process()
