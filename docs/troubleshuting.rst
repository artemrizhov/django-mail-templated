Troubleshooting
=================

If the app does not work as expected then please follow these steps:

#.  Update to the latest version:

    .. code-block:: console

        pip install -U django-mail-templated

#.  Run tests within your current Django project environment:

    .. code-block:: console

        python manage.py test mail_templated

#.  Run tests in a standalone mode:

    .. code-block:: console

        python -m mail_templated.tests.run

#.  `Create a GitHub issue
    <https://github.com/artemrizhov/django-mail-templated/issues/new>`_.

You also are welcome to try to fix the problem by yourself:

#.  Fork and clone the `GitHub repository
    <https://github.com/artemrizhov/django-mail-templated>`_.

#.  Add a test case that demonstrates the problem.

#.  Fix it and create a pull request.
