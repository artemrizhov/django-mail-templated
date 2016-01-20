"""
Setup Django environment for tests or for Python shell.
"""
import os
import sys


def setup_django():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mail_templated.test_utils.settings'
    test_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.insert(0, test_dir)

    import django
    # Old Django versions do not need such initialisation.
    if hasattr(django, 'setup'):
        django.setup()
