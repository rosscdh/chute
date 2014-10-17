# -*- coding: utf-8 -*-
import logging
import facebook
import requests
logger = logging.getLogger('django.request')


def _get_pages(data, limit=None):
    counter = 0
    next_uri = data.get('paging', {}).get('next', None)

    while next_uri not in [None, ''] and (limit is not None and counter < limit):
        data = requests.get(next_uri).json()
        counter += 1

        next_uri = data.get('paging', {}).get('next', None)

        for item in data.get('data', []):
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

    def process(self, **kwargs):
        from .models import FeedItem
        self.graph = facebook.GraphAPI(self.token)
        for project in self.projects:

            try:
                feed = self.graph.get_connections(project.name, 'feed')
            except ValueError:
                feed = {}

            for item in _get_pages(feed, limit=3):
                # get crc from specific values
                crc = FeedItem.crc(item.get('id'),
                                   item.get('updated_time'))
                # create
                feed, is_new = FeedItem.objects.get_or_create(project=project,
                                                              facebook_crc=crc)
                feed.data = item
                feed.save(update_fields=['data'])
                print feed, is_new
