from django.conf import global_settings


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'mail_templated',
)

SECRET_KEY = 'test'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': global_settings.TEMPLATE_LOADERS,
        },
    },
    {
        'BACKEND': 'mail_templated.template_backend.mail_templated.EmailTemplates',
        'OPTIONS': {
            'loaders': global_settings.TEMPLATE_LOADERS,
        },
    },
]