"""
Setup Django environment for tests or for Python shell.
"""
import os
import sys


def init_django():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
    test_dir = os.path.dirname(__file__)
    sys.path.insert(0, test_dir)

    import django
    # Old Django versions do not need such initialisation.
    if hasattr(django, 'setup'):
        django.setup()
