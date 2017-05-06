from django.db import models


class SockQuerySet(models.QuerySet):

    def eligible(self):
        return self.filter(
            match_as_sock1=None,
            match_as_sock2=None,
        )

    def for_user(self, user):
        user_sock_ids = user.socks.values_list('pk', flat=True)
        return self.exclude(pk__in=user_sock_ids)

    def owned_by_user(self, user):
        return self.filter(owner=user)


class SockMatchQuerySet(models.QuerySet):
    pass
