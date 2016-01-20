#!/usr/bin/env python
"""
Run tests without Django project.

This module is added to the app package to make it possible for everyone to run
the tests outside of any Django project context.
"""
import sys

from django_setup import setup_django


def run_tests():
    # Old Django versions requires Django initialisation before we can get the
    # test runner.
    setup_django()

    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['mail_templated'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
