# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from storages.backends.s3boto import S3BotoStorage

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from collections import namedtuple, OrderedDict

import os
import uuid
import logging
logger = logging.getLogger('django.request')


def _model_slug_exists(model, queryset=None, **kwargs):
    #
    # allow override of queryset
    #
    queryset = model.objects if queryset is None else queryset
    try:
        return queryset.get(**kwargs)
    except model.DoesNotExist:
        return None
    except model.MultipleObjectsReturned:
        #
        # in case we have the same key (which we do in a few cases)
        #
        return None


def _user_exists(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def _get_unique_username(username):
    username = slugify(username)  # apply the transforms first so that the lookup acts on the actual username
    username = username[0:29]
    while _user_exists(username=username):
        logger.info('Username %s exists, trying to create another' % username)
        username = '%s-%s' % (username, uuid.uuid4().get_hex()[:4])
        username = username[0:29]  # be aware of fencepost error here field limit is 30

    return username


def get_namedtuple_choices(name, choices_tuple):
    """Factory function for quickly making a namedtuple suitable for use in a
    Django model as a choices attribute on a field. It will preserve order.

    Usage::

        class MyModel(models.Model):
            COLORS = get_namedtuple_choices('COLORS', (
                (0, 'black', 'Black'),
                (1, 'white', 'White'),
            ))
            colors = models.PositiveIntegerField(choices=COLORS)

        >>> MyModel.COLORS.black
        0
        >>> MyModel.COLORS.get_choices()
        [(0, 'Black'), (1, 'White')]

        class OtherModel(models.Model):
            GRADES = get_namedtuple_choices('GRADES', (
                ('FR', 'fr', 'Freshman'),
                ('SR', 'sr', 'Senior'),
            ))
            grade = models.CharField(max_length=2, choices=GRADES)

        >>> OtherModel.GRADES.fr
        'FR'
        >>> OtherModel.GRADES.get_choices()
        [('fr', 'Freshman'), ('sr', 'Senior')]

    """
    class Choices(namedtuple(name, [name for val, name, desc in choices_tuple])):
        __slots__ = ()
        _choices = tuple([desc for val, name, desc in choices_tuple])

        def get_choices(self):
            return zip(tuple(self), self._choices)

        def get_choices_dict(self):
            """
            Return an ordered dict of key and their values
            must be ordered correctly as there are items that depend on the key
            order
            """
            choices = OrderedDict()
            for k, v in self.get_choices():
                choices[k] = v
            return choices

        def get_all(self):
            for val, name, desc in choices_tuple:
                yield val, name, desc

        def get_values(self):
            values = []
            for val, name, desc in choices_tuple:
                if isinstance(val, type([])):
                    values.extend(val)
                else:
                    values.append(val)
            return values

        def get_value_by_name(self, input_name):
            for val, name, desc in choices_tuple:
                if name == input_name:
                    return val
            return False

        def get_desc_by_value(self, input_value):
            for val, name, desc in choices_tuple:
                if val == input_value:
                    return desc
            return False

        def get_name_by_value(self, input_value):
            for val, name, desc in choices_tuple:
                if val == input_value:
                    return name
            return False

        def is_valid(self, selection):
            for val, name, desc in choices_tuple:
                if val == selection or name == selection or desc == selection:
                    return True
            return False

    return Choices._make([val for val, name, desc in choices_tuple])


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def _managed_S3BotoStorage():
    return OverwriteStorage() if settings.PROJECT_ENVIRONMENT in ['test'] else S3BotoStorage()
