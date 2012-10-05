==========
Django-Mail-Templated
==========
:Info: Send emails using Django template system
:Author: Artem Rizhov (https://github.com/artemrizhov)

Overview
=================
This is a tiny wrapper around the standard EmailMessage class and send_mail()
function. Just pass template_name and context as the first parameters then use
as normal.

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
Write a template to send a plain text message. Note that first and last newline
will be removed::

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

Or for an html message::

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

Or for a multipart message you can use both blocks::

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

Or leave out some block to set it manually later with EmailMessage class::

    {% block body %}
    This is a plain text message.
    {% endblock %}

Now you can send it::

    from mail_templated import send_mail
    send_mail('email/hello.tpl', {'user': user}, from_email, [user.email])

Or if you wish to add more control over message creation then use the class form::

    from mail_templated import EmailMessage
    message = EmailMessage('email/hello.tpl', {'user': user}, to=[user.email])
    # ... attach a file, etc
    message.send()

That's all. Please create an issue at GitHub if you have any notes,
...or just email :)
