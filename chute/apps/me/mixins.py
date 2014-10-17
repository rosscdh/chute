# -*- coding: utf-8 -*-


class EmailIsValidatedMixin(object):
    """
    Mixin to provide access to saving the validated_email
    property for user.profile
    """
    @property
    def validated_email(self):
        return self.data.get('validated_email', False)

    @validated_email.setter
    def validated_email(self, value):
        if type(value) in [bool]:
            self.data['validated_email'] = value
