Django Mail Templated
=====================

**Send emails using Django template system**

This is a tiny wrapper around the standard ``EmailMessage`` class and
``send_mail()`` function that provides an easy way to create email messages
using the `Django template system
<https://docs.djangoproject.com/es/1.9/topics/templates/>`_.
Just pass ``template_name`` and ``context`` as the first parameters then use as
normal.

Full documentation is available at http://django-mail-templated.rtfd.org/

Features
--------

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


Quick start
-----------

Run:

.. code-block:: console

    pip install django-mail-templated

And register the app in your settings file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'mail_templated'
    )

Create template:

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    {{ user.name }}, this is a plain text message.
    {% endblock %}

    {% block html %}
    {{ user.name }}, this is an <strong>html</strong> message.
    {% endblock %}

Send message:

.. code-block:: python

    from mail_templated import send_mail
    send_mail('email/hello.tpl', {'user': user}, from_email, [user.email])

Advanced usage:

.. code-block:: python

    from mail_templated import EmailMessage

    message = EmailMessage('email/hello.tpl', {'user': user}, from_email,
                           to=[user.email])
    message.render()
    message.send()
