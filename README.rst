==============================
Django-Mail-Templated
==============================
:Info: Send emails using Django template system
:Author: Artem Rizhov (https://github.com/artemrizhov)

Overview
=================
This is a tiny wrapper around the standard ``EmailMessage`` class and
``send_mail()`` function.
Just pass template_name and context as the first parameters then use as normal.

Features:

* Built with OOP, KISS and flexibility in mind. Really small and simple, but
  yet full-featured (I hope).

* Extends and mimics the built-in Django ``EmailMessage`` and ``send_mail()``.
  Compatible as much as possible.

* Fully supports Django template system including template inheritance
  (thanks to *BradWhittington* for the note about the problem).

* Supports any possible template engines and loaders.

* Supports serialisation (thanks to *arjandepooter*).

* Fully covered with tests.

* Tested with Django 1.4-1.9.

* Compatible with Python 3.


Installation
=================
Run::

    $ pip install django-mail-templated

And register the app in your settings file::

    INSTALLED_APPS = (
        ...
        'mail_templated'
    )

Usage
=================

Each email template should extend ``"mail_templated/base.tpl"`` or it's clone
either directly or via descendants.
This is the only way to provide robust and full support for template
inheritance, because Django template engine takes a lot of changes from time
to time.

Note that first and last newlines inside of block contents will be removed.

Plain text message::

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

HTML message::

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

Multipart message::

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

Partial template without subject::

    {% extends "mail_templated/base.tpl" %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

Fast method with ``send_mail()`` function::

    from mail_templated import send_mail
    send_mail('email/hello.tpl', {'user': user}, from_email, [user.email])

More control with ``EmailMessage`` class::

    from mail_templated import EmailMessage

    # Render immediately on initialisation.
    message = EmailMessage('email/hello.tpl', {'user': user}, from_email,
                           to=[user.email], render=True)
    send_to_queue(message)  # The message may be serialised safely.

    # Initialize and render later.
    message = EmailMessage(to=[user.email])
    message.load_template('email/hello.tpl')
    message.context = {'user': user}
    message.render()
    message.from_email = from_email
    message.to = [user.email]

    # Attach alternatives, files, etc.
    message.attach_alternative('HTML alternative', 'text/html')

    # Set default subject and body
    message = EmailMessage('email/hello.tpl', {'user': user},
                           subject=subject, body=body)

    # Change subject or body manually at any time.
    message.subject = subject
    message.body = body


    message.send()

Look into the source code for more info.

Please create an issue at GitHub if you have any notes.
Pull requests are welcome!
