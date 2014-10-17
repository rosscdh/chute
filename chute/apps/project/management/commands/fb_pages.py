# -*- coding: utf-8 -*-
import facebook

from django.template import Context
from django.template.loader import get_template
from django.template.defaultfilters import slugify

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.core.management.base import BaseCommand, CommandError

from django.template import Template

from social.apps.django_app.default.models import UserSocialAuth

from ...models import Project, FeedItem


class Command(BaseCommand):
    """
    """
    args = None
    help = ""

    def handle(self, *args, **options):
        self.template = get_template('clean-blog/post.html')

        for p in Project.objects.all():
            entity_name = p.name
            print entity_name

            for feed in p.feeditem_set.all():
                ctx = {
                    'project': p.data
                }
                ctx.update(feed.data)

                context = Context(ctx)
                source = self.template.render(context)
                default_storage.save('compiled/%s/%s.html' % (slugify(entity_name), slugify(ctx.get('name'))), ContentFile(source))

