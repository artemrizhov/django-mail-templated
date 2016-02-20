.. _advanced_usage:

Advanced usage
==============


.. _plain_and_html:

Plain text and HTML messages
----------------------------

All messages that you create with **mail_templated** are instances of
the :class:`mail_templated.EmailMessage` class which extends
:class:`django.core.mail.EmailMultiAlternatives
<django.core.mail.EmailMessage>`. This does not mean all messages are
multipart messages by default, but they become so if both ``body`` and ``html``
template blocks are not empty in the template rendering output.

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

In this case the ``body`` part goes to the body of the email message, and the
``html`` part is attached as alternative.

If you define only one of ``html`` and ``body`` blocks, it goes to the body of
email message with appropriate content type ``text/plain`` or ``text/html``.

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

The template above produces an HTML message without a plain text alternative.

Unused block is empty by default, because it is defined empty in the
:ref:`base template <inheritance>`. If you override both blocks but one of
them is rendered as empty string, this produces the same result as if the block
is not used at all. For example, let's review this template:

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block subject %}Subject{% endblock %}
    {% block body %}{{ plaintext_message }}{% endblock %}
    {% block html %}{{ html_message }}{% endblock %}

If the ``plaintext_message`` variable is empty then **mail_templated** will
create a message without the plain text part. This way you can be sure the
users will not see empty messages. However, only newlines are truncated from
the email parts (this is done for convenient template formatting).
If the part contains just one space character then it is considered as
non-empty.


.. _default_parts:

Default subject and body
------------------------

Both the :func:`mail_templated.send_mail()` function and the
:class:`mail_templated.EmailMessage` class got new parameters ``template_name``
and ``context`` instead of (good) old ``subject`` and ``body``. Hover you can
still pass both old parameters as keyword arguments. In this case they will be
treated as default values. If there is no appropriate part in the message
template (:ref:`or it is empty <plain_and_html>`) then the default value will
be used.

Let's review this template without subject:

.. code-block:: html+django

    {% extends "mail_templated/base.tpl" %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

Now pass default subject and body to the
:func:`send_mail() <mail_templated.send_mail()>` function:

.. code-block:: python

    from mail_templated import send_mail

    send_mail('email/without_subject.tpl', {},
              'from@inter.net', ['to@inter.net'],
              subject='Default subject', body='Default subject')

The default ``subject`` will be used since there is no subject in the template.
However the default ``body`` will be replaced by the value from the template.
The html part also overrides default ``body`` if the body part is empty.


.. _inheritance:

Base email template and inheritance
-----------------------------------

The email template is rendered as a solid document, and all email message parts
(subject, body and html) appears concatenated after rendering. For this purpose
the base template ``mail_templated/base.tpl`` contains special markers for the
email message parts, so that they can be found and extracted after rendering.

This approach eliminates the dependency on the inner implementation of the
Django template engine. It would be a bad idea to extract and render the
blocks objects separately, because the template engine implementation tends to
change.
But anyway you should not worry about that markup in normal situation.
Extend the base template provided by **mail_templated** and use the template
blocks as usually.

You can define your own base template. Just ensure your base template extends
the base of the base email templates, and any content is defined inside of
blocks ``subject``, ``body`` and ``html``.

**templates/email/base.html**

.. code-block:: html+django

  {% extends "mail_templated/base.tpl" %}

  {% block subject %}
  {{ COMPANY_NAME }} {% block subject_content %}{% endblock %}
  {% endblock %}

  {% block html %}
    <img src="{{ COMPANY_LOGO_URL }}" />
    {% block body_content %}
      {% include 'templates/email/parts/standard_greetings.html' %}
    {% endblock %}
  {% endblock %}

Now you can extend it as usually:

**templates/email/news.html**

.. code-block:: html+django

  {% extends "email/base.html" %}

  {% block subject_content %}{{ article.title }}{% endblock %}

  {% block body_content %}
    {{ block.super }}
    You probably will be interested in this news:
    {{ article.preview }}
  {% endblock %}

As you can see, there is nothing special about template inheritance. Actually
it is even not required to extend the base of the base email templates. The
most base template is just a helper that adds markers to the template. It is
better to use it if you want to be sure new version of the **mail_templated**
app will be compatible with your code. But if you want, you can use your own
base template with markers for the email parts.

The most base template looks like this:

**mail_templated/base.tpl**

.. code-block:: html+django

  {{ TAG_START_SUBJECT }}{% block subject %}{% endblock %}{{ TAG_END_SUBJECT }}

  {{ TAG_START_BODY }}{% block body %}{% endblock %}{{ TAG_END_BODY }}

  {{ TAG_START_HTML }}{% block html %}{% endblock %}{{ TAG_END_HTML }}

Let's review a simple template as an example:

.. code-block:: html+django

  {% extends "mail_templated/base.tpl" %}

  {% block subject %}This is a subject{% endblock %}
  {% block body %}This is a plain text body{% endblock %}
  {% block html %}This is an html body{% endblock %}

This will compile to:

.. code-block:: html

  ###start_subject###This is a subject###end_subject###
  ###start_body###This is a plain text body###end_body###
  ###start_html###This is an html body###end_html###

You can see that final document contains special tags for the message parts.
These markers is the main thing that the base template adds to your message.
Instead of extending it, you can use the markers just in your template:

.. code-block:: html+django

  ###start_subject###New for {{ week }}###end_subject###
  ###start_body###
  Hellow, {{ username }}! Below is a list of news for {{ week }}.
  ###end_body###
  ###start_html###
  Hellow, <strong>{{ username }}</strong>!
  Below is a list of news for <strong>{{ week }}</strong>.
  ###end_html###

This is the most efficient and the most inflexible way to define your
templates. They will be compiled fast, but there is a chance you will go home
much later.

The format of these tags can be changed in settings.
The :meth:`python:str.format()` method is used to format the tags. Please see
the :ref:`python:formatstrings` docs if you need more info about formatting.

.. code-block:: python

  # Default value is '###{bound}_{block}###'
  MAIL_TEMPLATED_TAG_FORMAT='<!--{block}:{bound}-->'

.. code-block:: html+django

  <!--subject:start-->This is a subject<!--subject:end-->
  <!--body:start-->This is a plain text body<!--body:end-->
  <!--html:start-->This is an html body<!--html:end-->

If there is any probability that the format will change in the future then you
probably want to use some variables. **mail_templated** provides such
variable to the context of your templates automatically.

.. code-block:: html+django

  {{ TAG_START_SUBJECT }}This is a subject{{ TAG_END_SUBJECT }}
  {{ TAG_START_BODY }}This is a plain text body{{ TAG_END_BODY }}
  {{ TAG_START_HTML }}This is an html body{{ TAG_END_HTML }}

You even can change the name format for these variables if the default format
conflicts with your code or you just hate it for some personal reason
(unfortunately there is no format for the names of these settings, I hope this
is not so important really).

.. code-block:: python

  # Default value is 'TAG_{BOUND}_{BLOCK}'
  MAIL_TEMPLATED_TAG_VAR_FORMAT='{BLOCK}_{BOUND}'
  # TODO: Define format for the format of format.

.. code-block:: html+django

  {{ SUBJECT_START }}This is a subject{{ SUBJECT_END }}
  {{ BODY_START }}This is a plain text body{{ BODY_END }}
  {{ HTML_START }}This is an html body{{ HTML_END }}

Finally you may decide to define your own base template:

.. code-block:: html+django

  {{ SUBJECT_START }}{% block subject %}{% endblock %}{{ SUBJECT_END }}
  {{ HTML_START }}{% block body %}{% endblock %}{{ HTML_END }}
  {{ BODY_START }}
  Please use a modern email client to see the html part of this message.
  {{ BODY_END }}

or without these tag name variables:

.. code-block:: html+django

  <!--subject:start-->{% block subject %}{% endblock %}<!--subject:end-->
  <!--body:start-->{% block body %}{% endblock %}<!--body:end-->
  <!--html:start-->
  Please use a modern email client to see the html part of this message.
  <!--html:end-->

Don't forget to add a :mod:`test <django.test>` that checks the
**mail_templated** app with your format of templates. Something like this
would be fine:

.. code-block:: python

    from django.core import mail
    from django.test import TestCase

    from mail_templated import send_mail


    class SendMailTestCase(TestCase):

        def test_plain(self):
            send_mail('email/test.tpl', {'name': 'User'},
                      'from@inter.net', ['to@inter.net'])
            self.assertEqual(len(mail.outbox), 1)
            message = mail.outbox[0]
            self.assertEqual(message.from_email, 'from@inter.net')
            self.assertEqual(message.to, ['to@inter.net'])
            self.assertEqual(message.subject, 'Message for User')
            self.assertEqual(message.body, 'Hello, User!')


.. _working_with_send_mail:

Working with send_mail() function
---------------------------------

You probably know that the API for
:func:`Django's send_mail() <django.core.mail.send_mail()>` function from
:mod:`django.core.mail` is frozen. Any new code wanting to extend the
functionality goes to the :class:`django.core.mail.EmailMessage` class.
The :func:`mail_templated.send_mail()` function works almost exactly the same
way as the standard one. But it is much more powerful than it seems at the
first look. The magic is done by passing all extra keyword arguments to the
:class:`mail_templated.EmailMessage` class constructor, which then passes them
to the base class :class:`django.core.mail.EmailMultiAlternatives
<django.core.mail.EmailMessage>`. Thus you can use all those features that are
accessible via parameters of the ``EmailMessage`` class constructor.

For example, you can add attachments like in this example:

.. code-block:: python

    send_mail(
        'email/message.tpl', context_dict, from_email, [email],
        attachments=[('attachment.png', content, 'image/png')])

The limitation of this feature is that you can't attach a file from the file
system. But if the content is in the variable already then this will work well
for you.

You can attach alternatives the same way:

.. code-block:: python

    send_mail(
        'email/message.tpl', context_dict, from_email, [email],
        alternatives=[('HTML alternative', 'text/html')])

You can also specify ``cc``, ``bcc``, ``reply_to`` and extra ``headers``.
Please review the API documentations for detailed info about parameters:

* :func:`mail_templated.send_mail()`
* :class:`mail_templated.EmailMessage`
* :class:`django.core.mail.EmailMessage and
  django.core.mail.EmailMultiAlternatives
  <django.core.mail.EmailMessage>`



.. _working_with_emailmessage:

Working with EmailMessage class
-------------------------------

The :class:`mail_templated.EmailMessage` class supports all the features that
are supported by the :class:`django.core.mail.EmailMultiAlternatives
<django.core.mail.EmailMessage>` class. And of course it provides ability
to use templates. If you have a complex task that can not be done in one step
then this class is probably what you need. In other case consider the
:ref:`send_mail() function<working_with_send_mail>`.

The message instance may be initialized with many various parameters. The most
common case will probably look like this:

.. code-block:: python

    message = EmailMessage('email/message.tpl', context, from_email, [email])

But you are free to create completely empty message and initialize it later.

.. code-block:: python

    message = EmailMessage()
    message.template_name = 'email/message.tpl'
    message.context = {'user_names': []}
    message.from_email = from_email
    message.to = []
    for user in users:
        message.context['user_names'].append(user)
        message.to.append(user.email)

The ``EmailMessage`` class has all methods that are available in the base
classes, so you can use this class in the usual way.

.. code-block:: python

    message.attach_alternative(html_content, 'text/html')
    message.attach_file(image_file_name, 'image/png')

Finally just send the message when you are done.

.. code-block:: python

    message.send()

As you can see this is almost regular email message object. You just set
``template_name`` and ``context`` instead of ``subject`` and ``body``, and all
the work is done behind the scene. But in fact you have more control that you
can use when needed. This will be described in the next sections.

Please review the API documentations for detailed info about parameters and
attributes:

* :class:`mail_templated.EmailMessage`
* :class:`django.core.mail.EmailMessage and
  django.core.mail.EmailMultiAlternatives
  <django.core.mail.EmailMessage>`


Loading and rendering the email template
----------------------------------------

The template that you specify via
:attr:`~mail_templated.EmailMessage.template_name` on the
:class:`~mail_templated.EmailMessage` class initialization is loaded and
rendered automatically when you call the
:meth:`~mail_templated.EmailMessage.send()` method. It tries to do this as late
as possible. But you can take the control and force this at any time. The
``EmailMessage`` class provides two methods for this needs:
:meth:`~mail_templated.EmailMessage.load_template()` and
:meth:`~mail_templated.EmailMessage.render()`.

The most fragmented approach looks like this:

.. code-block:: python

    message = EmailMessage()
    message.template_name = 'email/message.tpl'
    message.load_template()
    message.render()
    message.send()

You can pass the template name either to the constructor or to the
``load_template()`` method:

.. code-block:: python

    message = EmailMessage('email/message.tpl')
    message.load_template()

    message = EmailMessage()
    message.load_template('email/message.tpl')

You even can load it manually and then set via the
:attr:`~mail_templated.EmailMessage.template` property.

.. code-block:: python

    message = EmailMessage()
    message.template = get_template('email/message.tpl')

And you even can omit the call to the ``load_template()`` method and just use
the ``render()`` method only. When you try to render the template in any way,
it will be loaded automatically if not loaded yet.

Before you render the template, a context dict should be provided. There are
also few variants how you can do this.

.. code-block:: python

    message = EmailMessage('email/message.tpl', context)
    message.render()

    message = EmailMessage('email/message.tpl')
    message.context = context
    message.render()

    message = EmailMessage('email/message.tpl')
    message.render(context)

Finally you can pass ``render=True`` to the constructor if you want to render
it immediately.

.. code-block:: python

    message = EmailMessage('email/message.tpl', context, render=True)

There is also nothing wrong (expect of efficiency) if you want to load and
render one template, then load and render another one.

.. code-block:: python

    message = EmailMessage(customer.message_template_file, context,
                           from_email, [email])
    message.render()
    if not is_valid_html(message.body):
        message.load_template('email/fallback_message.tpl')
        message.context.update(fallback_extra_context)
        message.render()
    message.send()

As you can see in this example, you can access the resulting subject and body
as soon as the message is rendered.

.. code-block:: python

    message = EmailMessage('email/message.tpl', context, render=True)
    logger.debug('Subject: ' + message.subject)
    logger.debug('Body: ' + message.body)
    if message.alternatives:
        logger.debug('Alternarive: ' + message.alternatives[0][0])

When rendered, the message object becomes very similar to the standard Django's
:class:`~django.core.mail.EmailMessage` class. You can check current status via
the :attr:`~mail_templated.EmailMessage.is_rendered` property.


.. Sending multiple emails with same template
   ------------------------------------------

.. Using with third-party libraries
   --------------------------------


More examples
-------------

.. code-block:: python

    # Serialize message after initialization if needed.
    save_message_to_db(pickle.dumps(message))
    # Then restore when ready to continue.
    message = pickle.loads(get_message_from_db())
