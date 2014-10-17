# -*- coding: utf-8 -*-
import uuid
import datetime


class VideoCommentsMixin(object):
    """
    Mixin to allow adding and removing of comments
    """
    @property
    def comments(self):
        return [c for c in self.data.get('comments', []) if c.get('is_deleted', False) is False]

    @property
    def comments_by_id(self):
        return sorted(self.comments, key=lambda comment: comment.get('pk'), reverse=False)

    @property
    def comments_by_id_reversed(self):
        return sorted(self.comments, key=lambda comment: comment.get('pk'), reverse=True)

    @comments.setter
    def comments(self, value):
        assert type(value) == list, '%s.comments must be a list []' % self.__class__.__name__
        self.data['comments'] = value

    def add_comment(self, comment, **kwargs):
        comments = self.comments
        index = len(comments) + 1  # save the current index
        kwargs.update({
            'pk': index,
            'uuid': str(uuid.uuid4()),
            'comment': comment,
            'is_deleted': False,
        })
        if 'date_of' not in kwargs:
            kwargs.update({
                'date_of': datetime.datetime.utcnow().isoformat('T')
            })
        # append the object to the list
        comments.append(kwargs)
        # set the comment value in data vai the setter
        self.comments = comments
