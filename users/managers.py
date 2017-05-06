from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserQueryset(models.QuerySet):

    pass


class UserManager(BaseUserManager):

    pass
