from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.managers import UserManager, UserQueryset


class User(AbstractBaseUser):

    # Username
    USERNAME_FIELD = 'username'
    username = models.SlugField(_('username'), unique=True)

    # Timestamps
    created_at = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modified time'), auto_now=True)

    objects = UserManager.from_queryset(UserQueryset)()

    class Meta(object):
        verbose_name = _('user')
        verbose_name_plural = _('users')

    ########################
    # Permission overrides #
    ########################

    is_staff = True
    is_superuser = True

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm_name):
        return True

    def __str__(self):
        return self.get_full_name()

    # Convenience methods

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    @property
    def full_name(self):
        return self.get_full_name()
