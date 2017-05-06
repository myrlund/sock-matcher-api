import random

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import SockMatchQuerySet, SockQuerySet


class Sock(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='socks')
    name = models.CharField(_('name'), max_length=100)

    size_description = models.CharField(_('size description'), max_length=100, default='One size fits all')
    image = models.ImageField(_('image of sock'), null=True)
    is_rental = models.BooleanField(_('is rental'), default=False)

    objects = SockQuerySet.as_manager()

    class Meta(object):
        verbose_name = _('sock')
        verbose_name_plural = _('socks')

    def __str__(self):
        return '{} ({})'.format(self.name, self.owner)

    def get_match(self):
        return SockMatch.objects.filter(
            models.Q(sock1=self) |
            models.Q(sock2=self)
        ).first()

    @property
    def matching_sock(self):
        return self.match.get_other_sock(self)

    @property
    def match(self):
        return self.get_match()

    @property
    def has_match(self):
        return (self.get_match() is not None)


class SockPreference(models.Model):

    PREFERENCE_APPROVE = 1
    PREFERENCE_DISAPPROVE = 2
    PREFERENCE_CHOICES = [
        (PREFERENCE_APPROVE, _('Approve')),
        (PREFERENCE_DISAPPROVE, _('Disapprove')),
    ]

    source_sock = models.ForeignKey(Sock, related_name='source_for_preferences')
    target_sock = models.ForeignKey(Sock, related_name='target_for_preferences')

    preference = models.PositiveSmallIntegerField(choices=PREFERENCE_CHOICES)

    class Meta:
        unique_together = [
            ('source_sock', 'target_sock'),
        ]

    @property
    def is_approval(self):
        return self.preference == self.PREFERENCE_APPROVE

    def get_opposite_direction(self):
        return SockPreference.objects.filter(
            source_sock=self.target_sock,
            target_sock=self.source_sock,
        ).first()

    @property
    def opposite_direction(self):
        if hasattr(self, '_opposite_direction'):
            return self._opposite_direction

        self._opposite_direction = self.get_opposite_direction()

        return self._opposite_direction

    @property
    def is_match(self):
        return (
            self.is_approval and
            self.opposite_direction is not None and
            self.opposite_direction.is_approval
        )


class SockMatch(models.Model):

    WINNER_CHOICES = [
        (1, _('Sock 1')),
        (2, _('Sock 2')),
    ]

    sock1 = models.OneToOneField(Sock, verbose_name=_('sock 1'), related_name='match_as_sock1')
    sock2 = models.OneToOneField(Sock, verbose_name=_('sock 2'), related_name='match_as_sock2')

    winner = models.PositiveSmallIntegerField(_('winner'), choices=WINNER_CHOICES)

    objects = SockMatchQuerySet.as_manager()

    class Meta(object):
        verbose_name = _('sock match')
        verbose_name_plural = _('sock matches')

    def save(self, *args, **kwargs):

        if not self.winner:
            self.winner = random.randint(1, 2)

        return super().save(*args, **kwargs)

    def __str__(self):
        return '{} <3 {}'.format(self.sock1, self.sock2)

    def get_other_sock(self, sock):
        if self.sock1 == sock:
            return self.sock2
        if self.sock2 == sock:
            return self.sock1
        raise ValueError('the given sock is not part of this sock match')

    @property
    def winner_sock(self):
        return getattr(self, 'sock{}'.format(self.winner))

    @property
    def loser_sock(self):
        return self.get_other_sock(self.winner_sock)
