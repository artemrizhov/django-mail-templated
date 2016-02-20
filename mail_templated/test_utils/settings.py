"""
Django settings for standalone run of tests
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

INSTALLED_APPS = (
    'mail_templated',
)

SECRET_KEY = 'test'

# Required by Django == 1.7
from django.conf import global_settings
MIDDLEWARE_CLASSES = global_settings.MIDDLEWARE_CLASSES
