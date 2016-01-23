==============================
Django-Mail-Templated
==============================

**Send emails using Django template system**

Table of Contents
=================

*   `Overview`_

*   `Installation`_

*   `Usage`_

*   `Troubleshooting`_

*   `Useful links`_

*   `Changelog <https://github.com/artemrizhov/django-mail-templated/blob/master/CHANGELOG.rst>`_

Overview
=================

This is a tiny wrapper around the standard ``EmailMessage`` class and
``send_mail()`` function that provides an easy way to create email messages
using the `Django template system
<https://docs.djangoproject.com/es/1.9/topics/templates/>`_.
Just pass ``template_name`` and ``context`` as the first parameters then use as
normal.

**Features:**

* Built with OOP, KISS and flexibility in mind. Really small and simple, but
  yet full-featured (I hope).

* Extends and mimics the built-in Django's ``EmailMessage`` and
  ``send_mail()``. Compatible as much as possible.

* Fully supports Django template system including template inheritance
  (thanks to *BradWhittington* for the note about the problem).

* Supports any possible template engines and loaders.

* Supports serialisation (thanks to *arjandepooter*).

* Fully covered with tests.

* Tested with Django 1.4-1.9.

* Compatible with Python 3.


Installation
=================

Run:

.. code-block:: console

    pip install django-mail-templated

And register the app in your settings file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'mail_templated'
    )

It is also a good practice to ensure that the app is installed successfully and
is fully compatible with your environment:

.. code-block:: console

    python manage.py test mail_templated

Usage
=================

Creating templates
------------------

Each email template should extend ``"mail_templated/base.tpl"`` or its clone
either directly or via descendants.
This is the only way to provide robust and full support for template
inheritance, because Django template engine takes a lot of changes from time
to time.

Note that first and last newlines inside of block contents will be removed.

**Plain text message:**

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

**HTML message:**

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

**Multipart message:**

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

**Partial template without subject:**

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

Sending messages
----------------

**Fast method using ``send_mail()`` function:**

.. code-block:: python

    from mail_templated import send_mail
    send_mail('email/hello.tpl', {'user': user}, from_email, [user.email])

**More control with ``EmailMessage`` class:**

.. code-block:: python

    from mail_templated import EmailMessage

    # Create new empty message.
    message = EmailMessage()

    # Initialize message on creation.
    message = EmailMessage('email/hello.tpl', {'user': user}, from_email,
                           to=[user.email])

    # Set default subject and body.
    message = EmailMessage(subject=subject, body=body)

    # Initialize message and render template immediately.
    message = EmailMessage('email/hello.tpl', {'user': user}, from_email,
                           to=[user.email], render=True)

    # Initialize message later.
    message.subject = 'Default subject'
    message.context = {'user': user}
    message.template_name = 'email/hello.tpl'
    message.from_email = from_email
    message.to = [user.email]

    # Attach alternatives, files, etc., as if you'd use standard
    # EmailMultiAlternatives object.
    message.attach_alternative('HTML alternative', 'text/html')

    # Serialize message after initialization if needed.
    save_message_to_db(pickle.dumps(message))
    # Then restore when ready to continue.
    message = pickle.loads(get_message_from_db())

    # Force immediate template load if you want to handle this somehow.
    try:
        message.load_template('email/hello.tpl')
    except TemplateDoesNotExist:
        message.load_template('email/default.tpl')

    # You can also set the template object manually.
    message.template = get_template('mail_templated_test/plain.tpl')

    # Force template rendering. If template was not loaded at this stage then
    # it will be loaded automatically, so you actually don't have to call
    # `load_template()` manually.
    message.render()

    # Get compiled subject and body as if you are using the standard Django message
    # object.
    logger.debug('Sending message with subject "{}" and body "{}"'.format(
        message.subject, message.body))

    # Change subject and body manually at any time. But remember they can be
    # overwritten by template rendering if not rendered yet.
    message.subject = subject
    message.body = body

    # This is also good point for serialization. Subject and body will be also
    # serialized, the template system will not be used after deserialization.
    message = pickle.loads(pickle.dumps(message))

    # Send message when ready. It will be rendered automatically if needed.
    message.send()

Look into the `source code
<https://github.com/artemrizhov/django-mail-templated>`_
for more info.

Troubleshooting
=================

If the app does not work as expected please follow the following steps:

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

You are also very welcome to try fixing the problem by yourself:

#.  Fork and clone the `GitHub repository
    <https://github.com/artemrizhov/django-mail-templated>`_.

#.  Add a test case that demonstrates the problem.

#.  Fix it and create a pull request.


Useful links
=================

* `Django template language
  <https://docs.djangoproject.com/es/1.9/ref/templates/language/>`_

* `Built-in template tags and filters
  <https://docs.djangoproject.com/es/1.9/ref/templates/builtins/>`_

* `The basics of Django template system
  <https://docs.djangoproject.com/es/1.9/topics/templates/>`_
