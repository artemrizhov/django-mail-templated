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

    # Attach alternatives, files, etc., as if you are using the standard
    # EmailMultiAlternatives object.
    message.attach_alternative('HTML alternative', 'text/html')

    # Serialize message after initialization if needed.
    save_message_to_db(pickle.dumps(message))
    # Then restore when ready to continue.
    message = pickle.loads(get_message_from_db())

    # Force the immediate template load if you want to handle it somehow.
    try:
        message.load_template('email/hello.tpl')
    except TemplateDoesNotExist:
        message.load_template('email/default.tpl')

    # You can also set the template object manually.
    message.template = get_template('mail_templated_test/plain.tpl')

    # Force template rendering. If the template was not loaded at this stage then
    # it will be loaded automatically, so you actually don't have to call
    # the `load_template()` method manually.
    message.render()

    # Get compiled subject and body as if you are using the standard Django message
    # object.
    logger.debug('Sending message with subject "{}" and body "{}"'.format(
        message.subject, message.body))

    # Change subject and body manually at any time. But remember they can be
    # overwritten by the template rendering if not rendered yet.
    message.subject = subject
    message.body = body

    # This is also a good point for serialization. Subject and body will also be
    # serialized, the template system will not be used after deserialization.
    message = pickle.loads(pickle.dumps(message))

    # Send message when ready. It will be rendered automatically if needed.
    message.send()


Useful links
------------

* `Django template language
  <http://django.readthedocs.org/en/stable/ref/templates/language.html>`_

* `Built-in template tags and filters
  <http://django.readthedocs.org/en/stable/ref/templates/builtins.html>`_

* `The basics of Django template system
  <http://django.readthedocs.org/en/stable/topics/templates.html>`_
