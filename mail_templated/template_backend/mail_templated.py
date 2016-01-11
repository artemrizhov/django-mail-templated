import types

from django.conf import settings
from django.template import Engine
from django.template.backends.django import DjangoTemplates


BASE_TEMPLATE = 'mail_templated/base.tpl'


def _add_extends(template_code):
    # If this templates extends another one then do nothing.
    parts = template_code[template_code.find('{%'):].split(None, 2)
    if len(parts) == 3 and parts[1] == 'extends':
        return template_code
    # Make this template extending the special base template with markers
    # for the email message parts. This will be used by the EmailMessage
    # class split the resulting file.
    template_code = \
        '{{% extends "{}" %}}'.format(BASE_TEMPLATE) + template_code
    return template_code


class EmailEngine(Engine):
    """
    Make the email templates extending the base email class automatically.
    """

    def find_template_loader(self, loader):
        loader = super(EmailEngine, self).find_template_loader(loader)
        if loader is not None:
            # Patch the `get_contents()` method to add base template on load.
            old_get_contents = loader.get_contents
            def new_get_contents(self, origin, *args, **kwargs):
                contents = old_get_contents(origin, *args, **kwargs)
                # Don't extend the base template with itself.
                if origin.template_name != BASE_TEMPLATE:
                    contents = _add_extends(contents)
                return contents
            loader.get_contents = types.MethodType(new_get_contents, loader)
        return loader

    def from_string(self, template_code, *args, **kwargs):
        template_code = _add_extends(template_code)
        return super(EmailEngine, self).from_string(
            template_code, *args, **kwargs)


class EmailTemplates(DjangoTemplates):
    def __init__(self, params):
        """
        Replaces Engine class with EmailEngine.

        This method should be checked and fixed if any change happens in the
        base class in the future.
        """
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        options.setdefault('debug', settings.DEBUG)
        options.setdefault('file_charset', settings.FILE_CHARSET)
        # For Django >= 1.9.
        if hasattr(self, 'get_templatetag_libraries'):
            libraries = options.get('libraries', {})
            options['libraries'] = self.get_templatetag_libraries(libraries)
        # Skip `DjangoTemplates.__init__()` because it is reimplemented here.
        super(DjangoTemplates, self).__init__(params)
        self.engine = EmailEngine(self.dirs, self.app_dirs, **options)
