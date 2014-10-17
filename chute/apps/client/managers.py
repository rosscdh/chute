from django.db import models


class ClientManager(models.Manager):
    def mine(self, user):
        if not user.is_authenticated():
            return []

        return self.get_queryset().filter(lawyer=user)
