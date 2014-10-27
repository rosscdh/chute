# -*- coding: utf-8 -*-
from django.conf import settings

from collections import Counter
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


class BaseTokenMixin(object):
    @property
    def token(self):
        social_auth = self.user.social_auth.all().first()
        token = social_auth.tokens
        return token


class FacebookProjectDetailService(BaseTokenMixin):
    """
    """
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


class FacebookPageSubscriptionService(BaseTokenMixin):
    """
    """
    PAGE_FIELDS = ['feed',
                   'name',
                   'picture',
                   'description',
                   'founded',
                   'company_overview',
                   'general_info',
                   'hours',
                   'email',
                   'website']

    def __init__(self, project, **kwargs):
        self.project = project
        self.user = self.project.collaborators.all().last()
        self.graph = None
        self.page_id = None
        self.subscriptions = None

    def subscription(self, page_id, data={}, method='list'):
        """
        method = list|destroy|create
        """
        app_graph = facebook.GraphAPI()
        app_graph.access_token = app_graph.get_app_access_token(app_id=settings.SOCIAL_AUTH_FACEBOOK_KEY,
                                                                app_secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET)
        #url = '/v2.1/%s/subscriptions/' % settings.SOCIAL_AUTH_FACEBOOK_KEY
        import pdb;pdb.set_trace()
        url = '/v2.1/%s/subscriptions/' % page_id
        
        if method in ['list', 'GET']:
            return app_graph.request(url, args=data, method='GET')

        if method in ['create', 'POST']:
            return app_graph.request(url, post_args=data, method='POST')

        if method in ['destroy', 'DELETE']:
            return app_graph.request(url, method='DELETE')
        

    def process(self, **kwargs):
        self.graph = facebook.GraphAPI(self.token)
        data = self.graph.get_object(self.project.name)
        self.page_id = data.get('id')

        new_subscription = {
            'object': 'page',
            'fields': ','.join(self.PAGE_FIELDS),
            'callback_url': 'https://2b2dea03.ngrok.com/webhook/facebook/%s/' % self.project.slug,
            'verify_token': 'abc123talkingaboutyouandme',
        }

        #resp = self.subscription(page_id=self.page_id)
        resp = self.subscription(page_id=self.page_id, data=new_subscription, method='create')

        #self.project.data = data
        #self.project.save(update_fields=['data'])
        return resp


class FacebookFeedGeneratorService(BaseTokenMixin):
    """
    """
    @property
    def projects(self):
        """
        return iterable of projects to parse
        """
        return [pc.project for pc in self.user.projectcollaborator_set.all()] if self.project is None else [self.project,]

    def __init__(self, user, **kwargs):
        from .models import FeedItem
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

            try:
                feed = self.graph.get_connections(project.name, 'posts')
            except ValueError:
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
