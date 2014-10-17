# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..mixins import VideoCommentsMixin
from ..models import Video


class VideoCommentsMixinTest(TestCase):
    subject = VideoCommentsMixin
    model = Video

    def setUp(self):
        super(VideoCommentsMixinTest, self).setUp()
        self.video = mommy.make('project.Video')

    def test_invalid_comments_setter_value(self):
        with self.assertRaises(Exception):
            self.video.comments = 'This should be a list and not a string'

    def test_comments_setter(self):
        expected_comment = {'comment': 'working comment'}
        self.video.comments = [expected_comment]
        self.assertEqual(self.video.comments, [expected_comment])

    def test_model_has_mixin(self):
        self.assertTrue(self.subject in self.model.__mro__)

    def test_add_comment(self):
        self.video.add_comment(comment='Testing 123')
        self.assertEqual(self.video.comments[0].get('comment'), 'Testing 123')
        self.assertItemsEqual(self.video.comments[0].keys(), ['comment', 'pk', 'date_of', 'is_deleted'])

        self.video.add_comment(comment='Testing 456')
        self.video.add_comment(comment='Testing 789')
        self.assertEqual(self.video.comments[0].get('comment'), 'Testing 123')
        self.assertEqual(self.video.comments[1].get('comment'), 'Testing 456')
        self.assertEqual(self.video.comments[2].get('comment'), 'Testing 789')


    def test_empty_comments_are_returned(self):
        self.assertItemsEqual(self.video.comments, [])
