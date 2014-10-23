# -*- coding: utf-8 -*-
from collections import Counter
import re
import logging
import facebook
import requests
logger = logging.getLogger('django.request')


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
        social_auth = self.user.social_auth.all().first()
        token = social_auth.tokens
        return token

    def __init__(self, project, **kwargs):
        self.project = project
        self.user = self.project.collaborators.all().last()
        self.graph = None

    def process(self, **kwargs):
        self.graph = facebook.GraphAPI(self.token)
        data = self.graph.get_object(self.project.name)
        self.project.data = data
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
        return [pc.project for pc in self.user.projectcollaborator_set.all()] if self.project is None else [self.project,]

    @property
    def token(self):
        social_auth = self.user.social_auth.all().first()
        token = social_auth.tokens
        return token

    def __init__(self, user, **kwargs):
        self.user = user
        self.project = kwargs.get('project', None)
        self.graph = None

    def calculate_wait_for(self, item):
        """
        Method to calculate the amount of time to display this item, based on
        150 wpm (floor avg reading speed) * 1.5
        """
        corpus = '%s %s %s' % (item.get('name'), item.get('description'), item.get('message'))
        words = re.findall(r'\w+', corpus.lower())
        count = Counter(words)
        base = (150 / sum(count.values()))
        return  (150 / base)

    def process(self, **kwargs):
        from .models import FeedItem
        self.graph = facebook.GraphAPI(self.token)
        for project in self.projects:

            try:
                feed = self.graph.get_connections(project.name, 'posts')
            except ValueError:
                feed = {}

            for item in _get_pages(feed, limit=3):
                # get crc from specific values
                crc = FeedItem.crc(item.get('id'),
                                   item.get('updated_time'))
                # create
                feed, is_new = FeedItem.objects.get_or_create(project=project,
                                                              facebook_crc=crc)
                feed.name = item.get('name', None)
                feed.description = item.get('description', None)
                feed.message = item.get('message', None)
                feed.wait_for = self.calculate_wait_for(item=item)
                feed.data = item
                feed.save()
                print feed, is_new
