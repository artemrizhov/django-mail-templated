Getting started
===============

Installation
------------

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


Creating templates
------------------

Each email template should extend :ref:`mail_templated/base.tpl <inheritance>`
or its clone either directly or via descendants.

Note: newlines at the begin and end of message part blocks will be removed.

Plain text message:

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

HTML message:

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

Multipart message:

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text part.
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> part.
    {% endblock %}


Sending messages
----------------

Fast method using :ref:`send_mail() <working_with_send_mail>` function:

.. code-block:: python

    from mail_templated import send_mail

    send_mail('email/hello.tpl', {'user': user}, from_email, [user.email])

More control with :ref:`EmailMessage <working_with_emailmessage>` class:

.. code-block:: python

    from mail_templated import EmailMessage

    message = EmailMessage('email/hello.tpl', {'user': user}, from_email,
                           to=[user.email])
    # TODO: Add more useful commands here.
    message.send()

Proceed to the :ref:`advanced_usage` section to find more details.
