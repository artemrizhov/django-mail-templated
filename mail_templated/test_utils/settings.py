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

# The TEMPLATES setting is required since Django 1.10.
if hasattr(global_settings, 'TEMPLATES'):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [],
            },
        },
    ]
