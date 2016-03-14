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
and ``context`` instead of (good) old ``subject`` and ``body``. However you can
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


Serialization
-------------

**mail_templated** supports the :mod:`python:pickle` module. You can serialize
the message object at any stage. However what really makes sense is serializing
before invoking the :meth:`~mail_templated.EmailMessage.load_template()` method
or after invoking the :meth:`~mail_templated.EmailMessage.render()` method.
If you decide to serialize just between the calls to these methods then you
will lost the compiled template instance, because it can not be serialized with
``pickle``.

Let's play with the email object a little.

.. code-block:: python

    >>> import pickle
    >>> from mail_templated import EmailMessage
    >>> message = EmailMessage('email/message.tpl', {})

As soon as the message exists, you can serialize it.

.. code-block:: python

    >>> # Serialize the message.
    >>> pickled_message = pickle.dumps(message)
    >>> # Let's see how it looks now.
    >>> print repr(pickled_message)
    "ccopy_reg\n_reconstructor\np0\n(cmail_templated.message\nEmailMessage\np1\
    nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS'body'\np6\nNsS'extra_headers'
    \np7\n(dp8\nsS'attachments'\np9\n(lp10\nsS'_is_rendered'\np11\nI00\nsS'cc'\
    np12\n(lp13\nsS'template_name'\np14\nS'mail_templated_test/plain.tpl'\np15\
    nsS'alternatives'\np16\n(lp17\nsS'bcc'\np18\n(lp19\nsS'to'\np20\n(lp21\nsS'
    connection'\np22\nNsS'context'\np23\n(dp24\nsS'reply_to'\np25\n(lp26\nsS'fr
    om_email'\np27\nS'webmaster@localhost'\np28\nsS'subject'\np29\nNsb."

Now you can store it somewhere for later use. Then load and de-serialize the
message when needed, and it is ready for further processing.

.. code-block:: python

    >>> # De-serialize the message.
    >>> message2 = pickle.loads(pickled_message)
    >>> # Check the message state.
    >>> print repr(message2)
    <mail_templated.message.EmailMessage object at 0x7ffb8ad2e810>
    >>> print repr(message2.template)
    None
    >>> # The template is not loaded yet. Load the template
    >>> message2.load_template()
    >>> # How is it now?
    >>> print repr(message2.template)
    <django.template.backends.django.Template object at 0x7ffb8a11c050>
    >>> # Good! It's ready for rendering.

While the template is loaded, let's try to serialize and de-serialize it again.

.. code-block:: python

    >>> # Serialize/de-serialize again.
    >>> message3 = pickle.loads(pickle.dumps(message2))
    >>> # Is the message still alive?
    >>> print repr(message3)
    <mail_templated.message.EmailMessage object at 0x7ffb8ad4f790>
    >>> # Yes, it's still alive, that's good. What about the template?
    >>> print repr(message3.template)
    None
    >>> # Ooops! We lost the template object. So now we have to load it again.
    >>> message3.load_template()
    >>> print repr(message3.template)
    <django.template.backends.django.Template object at 0x7ffb8a0fdf10>
    >>> # Phew! It's here now.

Actually if lost, the template will be loaded automatically again when you try
to render it. You will not see any errors. Just your code will do some useless
extra work.

.. code-block:: python

    >>> message4 = pickle.loads(pickle.dumps(message3))
    >>> print repr(message4.template)
    None
    >>> # Oh no! We lost it again :(
    >>> message4.render()
    >>> # Hmm... There is no any error!
    >>> print repr(message4.template)
    <django.template.backends.django.Template object at 0x7ffb8a0b4d50>
    >>> # Magic? No, this is by design!

So, remember to load the template just before the rendering, not before
serialization.

Once rendered, you can serialize/de-serialize it again without problems.

.. code-block:: python

    >>> # Check the message state.
    >>> print repr([message4.is_rendered, message4.subject, message4.body])
    [True, u'Test subject', u'Test body']
    >>> # Continue the tortures.
    >>> message5 = pickle.loads(pickle.dumps(message4))
    >>> # The author said it should work fine now.
    >>> print repr(message5.template)
    None
    >>> # :`(
    >>> # :```(
    >>> # But wait!
    >>> print repr([message5.is_rendered, message5.subject, message5.body])
    [True, u'Test subject', u'Test body']
    >>> # Heh, the template is not needed anymore! :D

There are so many combination how you can load, render and serialize the
message, so that I'm afraid I can't describe all of them here. These examples
should help you to construct your own combination.


Cleanup for third-party libraries
---------------------------------

There are many third-party libraries that help you to work with email messages.
If a library can work with the standard :class:`django.core.mail.EmailMessage`
class then it probably can work without problems with
:class:`mail_templated.EmailMessage`. However some library may be surprised
by the additional attributes on the email message object.
For example, the Djrill app will pass your ``template_name`` to the Mandrill
service because it provides it's own template system, and it uses the
``template_name`` parameter too (what a surprise!).

If something similar happens to your messages then you should wipe out
the tracks of the **mail_templated** app. The most easy way to do this is to
delete the conflicting attributes. The ``EmailMessage`` class provides a
convenient method :meth:`~mail_templated.EmailMessage.clean()` for this
purpose. It removes the most expensive and risky properties -
:attr:`~mail_templated.EmailMessage.context`,
:attr:`~mail_templated.EmailMessage.template` and
:attr:`~mail_templated.EmailMessage.template_name`.

If you use the :func:`~mail_templated.send_mail()` function then the cleanup is
invoked for you automatically just after rendering. You can disable this
behaviour by passing the ``clean=False`` keyword argument.

If you use the :class:`~mail_templated.EmailMessage` class then you should care
of cleanup yourself. Fortunately there are many places where you can invoke the
``clean()`` method either directly or via special keyword argument ``clean``.

.. code-block:: python

    # Invoke the cleanup right on the initialisation.
    message = EmailMessage('email/message.tpl', {}, render=True, clean=True)
    # Call the method manually after rendering.
    message.render()
    message.clean()
    # Pass `clean=True` to the `render()` method.
    message.render(clean=True)
    # The `send()` method also supports this argument.
    message.send(clean=True)

There is no much difference in these variants. Just choice one that makes your
code clean and clear.


.. Sending multiple emails with same template
   ------------------------------------------
