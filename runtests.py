import sys
from django.conf import settings
from test_init import init_django  # Initialize Django.


init_django()

from django.test.utils import get_runner
def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['mail_templated'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
