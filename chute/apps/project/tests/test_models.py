# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..mixins import VideoCommentsMixin
from ..models import Project, Video


class ProjectTest(TestCase):
    subject = Project

    def test_model_gets_slug_automatically(self):
        project = mommy.make('project.Project', name='I should be turned into a slug')
        self.assertEqual(project.slug, 'i-should-be-turned-into-a-slug')


class VideoTest(TestCase):
    subject = Video

    def test_model_has_expeceted_constants(self):
        self.assertTrue(hasattr(self.subject, 'VIDEO_TYPES'))

        self.assertItemsEqual(self.subject.VIDEO_TYPES.get_choices(),
                              [(1, 'video/mp4')])

    def test_model_has_mixin(self):
        self.assertTrue(VideoCommentsMixin in self.subject.__mro__)
