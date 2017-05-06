import os

from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    'sock-matcher.herokuapp.com',
]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
