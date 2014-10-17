# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

import logging
import urlparse
logger = logging.getLogger('django.request')

register = template.Library()

try:
    CURRENT_SITE = Site.objects.get(pk=settings.SITE_ID)
except (OperationalError, ProgrammingError):
    """
    Allow for no tables created yet when running syncdb
    """
    pass


def _DOMAIN_WITH_END_SLASH():
    return '%s/' % (CURRENT_SITE.domain.rstrip('/'))


@register.simple_tag
def admin_url_for(instance):
    content_type = ContentType.objects.get(model=instance._meta.model.__name__.lower())
    return reverse('admin:{app_name}_{model_name}_change'.format(app_name=content_type.app_label, model_name=content_type.model), args=(instance.pk,))


@register.simple_tag
def ABSOLUTE_BASE_URL(path=None):
    """
    Return the full current site domain with optional path appended
    ABSOLUTE_BASE_URL()
        returns: Site.domain http://example.com/

    ABSOLUTE_BASE_URL(path='/my/path/specified.html')
        returns: http://example.com/my/path/specified.html
    """
    return urlparse.urljoin(_DOMAIN_WITH_END_SLASH(), path)
ABSOLUTE_BASE_URL.is_safe = True


@register.simple_tag
def ABSOLUTE_STATIC_URL(path=None):
    """
    Return the full current site domain with {{ STATIC_URL }}
    ABSOLUTE_STATIC_URL()
        returns: http://example.com/static/

    ABSOLUTE_STATIC_URL(path='/my/path/specified.css')
        returns: http://example.com/static/my/path/specified.css
    """
    if path is not None:
        path = path if settings.STATIC_URL in path else '%s%s' % (settings.STATIC_URL, path)
    return urlparse.urljoin(_DOMAIN_WITH_END_SLASH(), path)
ABSOLUTE_STATIC_URL.is_safe = True


@register.simple_tag
def ABSOLUTE_MEDIA_URL(path=None):
    """
    Return the full current site domain with {{ MEDIA_URL }}
    ABSOLUTE_MEDIA_URL()
        returns: http://example.com/media/

    ABSOLUTE_MEDIA_URL(path='/my/path/specified.jpg')
        returns: http://example.com/media/my/path/specified.jpg
    """
    if path is not None:
        path = path if settings.MEDIA_URL in path else '%s%s' % (settings.MEDIA_URL, path)
    return urlparse.urljoin(_DOMAIN_WITH_END_SLASH(), path)
ABSOLUTE_MEDIA_URL.is_safe = True


# @register.inclusion_tag('partials/firstseen.html', takes_context=True)
# def firstseen(context):
#     return {
#         'PROJECT_ENVIRONMENT': settings.PROJECT_ENVIRONMENT,
#         'show': True if context['request'].GET.get('firstseen', '0') == '1' else False,
#     }


# @register.inclusion_tag('partials/javascript/google-analytics.html', takes_context=True)
# def google_analytics(context):
#     return {
#         'user': context['request'].user
#     }


# @register.inclusion_tag('partials/javascript/intercom.html', takes_context=True)
# def intercom(context):
#     return {
#         'app_id': settings.INTERCOM_APP_ID,
#         'user': context['request'].user
#     }


# @register.inclusion_tag('partials/javascript/mixpanel.html', takes_context=True)
# def mixpanel(context):
#     return {
#         'api_token': settings.MIXPANEL_SETTINGS['token'],
#         'user': context['request'].user
#     }


# @register.inclusion_tag('partials/javascript/olark.html', takes_context=True)
# def olark(context):
#     return {
#         'user': context['request'].user
#     }
