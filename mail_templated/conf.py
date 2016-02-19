import importlib

from django.conf import settings
from django.utils.functional import empty, LazyObject


SETTINGS_MODULE = 'mail_templated.default_settings'


class AppSettings(object):

    def __init__(self, settings_module):
        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)

        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }


class LazyAppSettings(LazyObject):
    """Ensure the settings are loaded after Django setup and if needed only"""

    def _setup(self):
        self._wrapped = AppSettings(SETTINGS_MODULE)

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Settings'.
        if self._wrapped is empty:
            return '<AppSettings [Unevaluated]>'
        return '<AppSettings "%(settings_module)s">' % {
            'settings_module': self._wrapped.SETTINGS_MODULE,
        }

    def __getattr__(self, name):
        full_name = 'MAIL_TEMPLATED_' + name
        value = getattr(settings, full_name, empty)
        if value is not empty:
            return value
        if self._wrapped is empty:
            self._setup()
        return getattr(self._wrapped, name)


app_settings = LazyAppSettings()
