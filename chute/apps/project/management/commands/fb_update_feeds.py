# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from chute.apps.project.services import (FacebookFeedGeneratorService,)



class Command(BaseCommand):
    """
    Comamnd to save compiled html pages to default storage for use by the remote boxes
    """
    args = None
    help = ""

    def handle(self, *args, **options):

        for u in User.objects.all():
            service = FacebookFeedGeneratorService(user=u)
            service.process(page_limit=5)
