"""
Django settings for standalone run of tests
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'mail_templated',
)

SECRET_KEY = 'test'