# -*- coding: utf-8 -*-
from django.conf import settings
from templated_email import send_templated_mail

import logging
logger = logging.getLogger('django.request')


class BaseMailerService(object):
    email_template = None
    base_email_template_location = 'email/'
    user = {
        "name": None,
        "email": None
    }

    def __init__(self, recipients, from_tuple=None, subject=None, message=None, **kwargs):
        """
        subject : string
        message : string
        from_tuple : (:name, :email)
        recipients : ((:name, :email), (:name, :email),)
        """
        self.subject = getattr(self, 'subject', subject)
        self.message = getattr(self, 'message', message)

        self.from_tuple = self.make_from_tuple(from_tuple=from_tuple)

        self.recipients = []

        for r in recipients:
            u = self.user.copy()
            u.update({
                'name': r[0],
                'email': r[1]
            })
            self.recipients.append(u)

        assert self.email_template  # defined in inherited classes
        assert self.from_tuple
        assert type(self.from_tuple) is dict
        assert self.recipients
        assert type(self.recipients) is list
        assert len(self.recipients) >= 1

    def make_from_tuple(self, from_tuple=None):
        return_tuple_dict = {}
        self.from_tuple = self.user.copy()  # setup the dictionary
        # if no from_tuple is provided simply use the defaults
        base_from_tuple = settings.DEFAULT_FROM[0]

        from_email = self.from_email(name=from_tuple[0] if from_tuple is not None else base_from_tuple[0], email=from_tuple[1] if from_tuple is not None else base_from_tuple[1])  # defaults to site name

        return_tuple_dict.update({
            'name': from_tuple[0] if from_tuple is not None else base_from_tuple[0],  # default site from name
            'email': from_email,
            'reply_to': from_tuple[1] if from_tuple is not None else base_from_tuple[1]  # default is site email if no from_tuple has been specified
        })

        return return_tuple_dict

    def from_email(self, name=None, email=None):
        """
        from email must always come from the default site email to avoid being rejected
        but to handle this we set teh reply_to header to be the lawyers email
        """
        site_email = settings.DEFAULT_FROM[0][1]
        return '%s (via Revision) %s' % (name, site_email) if email != site_email else email

    def process(self, attachments=None, **kwargs):
        self.params = kwargs

        for r in self.recipients:
            context = {
                'from': self.from_tuple.get('name'),
                'from_email': self.from_email(name=self.from_tuple.get('name'), email=self.from_tuple.get('email')),
                'to': r.get('name'),
                'to_email': r.get('email'),
                'subject': self.subject,
                'message': self.message
            }

            logger.debug('Email going out from: %s' % context.get('from_email'))

            context.update(**kwargs)

            self.send_mail(context=context, attachments=attachments)

    def send_mail(self, context, attachments=None):

        send_templated_mail(
            template_name=self.email_template,
            template_prefix=self.base_email_template_location,
            from_email=context.get('from_email'),
            recipient_list=[context.get('to_email')],
            bcc=[],
            context=context,
            attachments=attachments,
            headers={'Reply-To': self.from_tuple.get('reply_to')})


class BaseSpecifiedFromMailerService(BaseMailerService):
    """
    Require the code to pass in a from_tuple
    used for emails that are sent on behalf of the lawyer
    or some other user
    """
    def __init__(self, from_tuple, recipients, subject=None, message=None, **kwargs):
        # see how we require from_tuple and pass it in
        super(BaseSpecifiedFromMailerService, self).__init__(recipients=recipients, from_tuple=from_tuple, subject=subject, message=message, **kwargs)

