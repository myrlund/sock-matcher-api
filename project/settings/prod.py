import os

from .base import *


DEBUG = False

# Prepend prod apps
INSTALLED_APPS = [
    'collectfast',
    's3_folder_storage',
] + INSTALLED_APPS

ALLOWED_HOSTS = [
    'sock-matcher.herokuapp.com',
]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

AWS_LOCATION = 'static/'
AWS_PRELOAD_METADATA = True
AWS_S3_FILE_OVERWRITE = False

# Use S3 as file storage backend
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = 'media'
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATIC_S3_PATH = 'static'
STATIC_ROOT = '/%s/' % STATIC_S3_PATH
STATIC_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = STATICFILES_STORAGE
