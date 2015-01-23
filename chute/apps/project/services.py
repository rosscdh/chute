# -*- coding: utf-8 -*-
from collections import Counter

from chute.apps.feed.models import FeedItem

import re
import logging
import facebook
import requests
logger = logging.getLogger('django.request')

#ACCEPTED_POST_TYPES = ['link', 'status', 'photo', 'video']
ACCEPTED_POST_TYPES = ['link', 'photo', 'video']


def _get_pages(data, limit=None):
    counter = 0
    next_uri = data.get('paging', {}).get('next', None)
    pages = data.get('data', [])

    while next_uri not in [None, ''] and (limit is not None and counter < limit):
        pages += data.get('data', [])
        data = requests.get(next_uri).json()
        next_uri = data.get('paging', {}).get('next', None)
        counter += 1

    for item in pages:
        yield item


class FacebookProjectDetailService(object):
    """
    """
    @property
    def token(self):
        token = self.user.facebook_token()
        return token

    def __init__(self, project, **kwargs):
        self.project = project
        self.user = self.project.collaborators.all().last()
        self.graph = None

    def process(self, **kwargs):
        if self.project.is_facebook_feed is not True:
            logger.info('Project is not a facebook_feed: %s' % self.project)
            return None

        self.graph = facebook.GraphAPI(self.token)
        data = self.graph.get_object(self.project.name)
        self.project.data['facebook'] = data
        self.project.save(update_fields=['data'])
        return data


class FacebookFeedGeneratorService(object):
    """
    """
    @property
    def projects(self):
        """
        return iterable of projects to parse
        """
        if self.project is not None:
            yield self.project
        else:
            for pc in self.user.projectcollaborator_set.all().iterator():
                yield pc.project

    @property
    def token(self):
        return self.user.facebook_token()

    def __init__(self, user, **kwargs):
        self.feed_item_class = FeedItem
        self.user = user
        self.project = kwargs.get('project', None)
        self.graph = None

    def template_from_post_type(self, item):
        """
        Derive template from the post type
        """
        TEMPLATES = self.feed_item_class.TEMPLATES
        default_template = TEMPLATES.basic
        template_types = {
            'link': default_template,
            'status': default_template,
            'photo': TEMPLATES.image,
            'video': TEMPLATES.image_left,
        }
        return template_types.get(item.get('type', 'basic'), default_template)


    def post_type_from_item(self, item):
        """
        Default to status post_type
        """
        post_type = self.feed_item_class.POST_TYPES.get_value_by_name( item.get('type', 'basic') )
        return post_type if post_type is not False else item.POST_TYPES.status

    def calculate_wait_for(self, item):
        """
        Method to calculate the amount of time to display this item, based on
        150 wpm (floor avg reading speed) * 1.5
        """
        corpus = '%s %s %s' % (item.get('name'), item.get('description'), item.get('message'))
        words = re.findall(r'\w+', corpus.lower())
        count = Counter(words)
        total = count.values()
        base = (150 / sum(total))
        return  (150 / base) if base > 0 else 30

    def process(self, page_limit=3, **kwargs):
        self.graph = facebook.GraphAPI(self.token)

        for project in self.projects:
            if project.is_facebook_feed is True:
                logger.info('Trying to process feed for: %s on project: %s' % (self.user, project))
                try:
                    feed = self.graph.get_connections(project.name, 'posts')
                except (ValueError, facebook.GraphAPIError) as e:
                    logger.info('Error occured feed for: %s on project: %s - %s' % (self.user, project, e))
                    feed = {}

                for item in _get_pages(feed, limit=page_limit):

                    if item.get('type') not in ACCEPTED_POST_TYPES:
                        logger.info('FeedItem.post_type was not an accepted type: %s should be in: %s' % (item.get('type'), ACCEPTED_POST_TYPES))

                    else:

                        # get crc from specific values
                        crc = self.feed_item_class.crc(item.get('name'),
                                                       item.get('type'))
                        # create
                        feed_item, is_new = self.feed_item_class.objects.get_or_create(project=project,
                                                                                       facebook_crc=crc)
                        feed_item.name = item.get('name', None)
                        feed_item.description = item.get('description', None)
                        feed_item.message = item.get('message', None)
                        feed_item.post_type = self.post_type_from_item(item=item)
                        feed_item.template = self.template_from_post_type(item=item)
                        feed_item.wait_for = self.calculate_wait_for(item=item)
                        feed_item.data = item
                        feed_item.save()
                        logger.info('FeedItem accepted: %s (%s)' % (feed_item.pk, feed_item.name,))
