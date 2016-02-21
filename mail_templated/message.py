"""
.. module:: mail_templated.message
   :synopsis: Main classes of django-mail-templated package.

.. moduleauthor:: Artem Rizhov <artem.rizhov@gmail.com>
"""

from django.core import mail
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from .conf import app_settings


class EmailMessage(mail.EmailMultiAlternatives):
    """
    Extends standard EmailMultiAlternatives class with ability to use templates

    See Also
    --------
    :class:`django.core.mail.EmailMessage`
        Documentation for the standard email message classes.
    """

    _extra_context = None
    _extra_context_fingerprint = None

    def __init__(self, template_name=None, context={}, *args, **kwargs):
        """
        Initialize single templated email message (which can be sent to
        multiple recipients).

        When using with a user-specific message template for mass mailing,
        create new EmailMessage object for each user. Think about this class
        instance like about a single paper letter (you would not reuse it,
        right?).

        The class tries to provide interface as close to the standard Django
        classes as possible.
        |main_difference|

        All parameters are optional and can be set at any time prior to calling
        the :meth:`render()` and :meth:`send()` methods.

        Note
        ----

        .. |args_note| replace:: The set of possible parameters is not limited
            by the list below. Any additional parameters are passed to the
            constructor of
            :class:`EmailMultiAlternatives <django.core.mail.EmailMessage>`
            class.

        |args_note|

        .. |template_name| replace:: The template name that extends
            `mail_templated/base.tpl` with (optional) blocks ``{% subject %}``,
            ``{% body %}`` and ``{% html %}``.

        .. |context| replace:: A dictionary to be used as a context for
            template rendering.

        .. |from_email| replace:: The email address for the "From:" field.

        .. |recipient_list| replace:: The recipient email addresses. Each
            member of this list will see the other recipients in the "To:"
            field of the email message.

        .. |subject| replace:: Default message subject. Used if
            ``{% subject %}`` block is empty or does not exist in the
            specified email template.

        .. |body| replace:: Default message body. Used if ``{% body %}``
            block is empty or does not exist in the specified email template.

        .. |render| replace:: If ``True``, render template and set ``subject``,
            ``body`` and ``html`` properties immediately. Default is ``False``.

        Arguments
        ---------
        template_name : str
            |template_name|
        context : dict
            |context|
        from_email : str
            |from_email|
        recipient_list : list
            |recipient_list|

        Keyword Arguments
        -----------------
        subject : str
            |subject|
        body : str
            |body|
        render : bool
            |render|
        clean : bool
            If ``True``, remove any template specific properties from the
            message object. This may be useful if you pass ``render=True``.
            Default is ``False``.
        """
        self.template_name = template_name
        self.context = context
        subject = kwargs.pop('subject', None)
        body = kwargs.pop('body', None)
        render = kwargs.pop('render', False)
        clean = kwargs.pop('clean', False)
        self.template = None
        self._is_rendered = False

        super(EmailMessage, self).__init__(subject, body, *args, **kwargs)

        if render:
            self.render()
        if clean:
            self.clean()

    @property
    def is_rendered(self):
        return self._is_rendered

    @property
    def extra_context(self):
        cls = self.__class__
        tag_var_format = str(app_settings.TAG_VAR_FORMAT)
        tag_format = str(app_settings.TAG_FORMAT)
        if cls._extra_context_fingerprint != (tag_var_format, tag_format):
            cls._extra_context = dict(
                (tag_var_format.format(BLOCK=block.upper(),
                                       BOUND=bound.upper()),
                 mark_safe(tag_format.format(block=block, bound=bound)))
                for block in ('subject', 'body', 'html')
                for bound in ('start', 'end'))
            cls._extra_context_fingerprint = (tag_var_format, tag_format)
        return cls._extra_context

    def load_template(self, template_name=None):
        """
        Load a template by it's name using the current
        :ref:`template loaders <django:template-loaders>`.

        Arguments
        ---------
        template_name : str
            |template_name| If not specified then the
            :attr:`~mail_templated.EmailMessage.template_name` property is
            used.
        """
        self.template = get_template(template_name or self.template_name)

    def render(self, context=None, clean=False):
        """
        Render email with provided context

        Arguments
        ---------
        context : dict
            |context| If not specified then the
            :attr:`~mail_templated.EmailMessage.context` property is
            used.

        Keyword Arguments
        -----------------
        clean : bool
            If ``True``, remove any template specific properties from the
            message object. Default is ``False``.
        """
        # Load template if it is not loaded yet.
        if not self.template:
            self.load_template(self.template_name)
        # The signature of the `render()` method was changed in Django 1.7.
        # https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/#get-template-and-select-template
        if hasattr(self.template, 'template'):
            context = (context or self.context).copy()
        else:
            context = Context(context or self.context)
        # Add tag strings to the context.
        context.update(self.extra_context)
        result = self.template.render(context)
        # Don't overwrite default value with empty one.
        subject = self._get_block(result, 'subject')
        if subject:
            self.subject = self._get_block(result, 'subject')
        body = self._get_block(result, 'body')
        is_html_body = False
        # The html block is optional, and it also may be set manually.
        html = self._get_block(result, 'html')
        if html:
            if not body:
                # This is an html message without plain text part.
                body = html
                is_html_body = True
            else:
                # Add alternative content.
                self.attach_alternative(html, 'text/html')
        # Don't overwrite default value with empty one.
        if body:
            self.body = body
            if is_html_body:
                self.content_subtype = 'html'
        self._is_rendered = True
        if clean:
            self.clean()

    def send(self, *args, **kwargs):
        """
        Send email message, render if it is not rendered yet.

        Note
        ----
        Any extra arguments are passed to
        :class:`EmailMultiAlternatives.send() <django.core.mail.EmailMessage>`.

        Keyword Arguments
        -----------------
        clean : bool
            If ``True``, remove any template specific properties from the
            message object. Default is ``False``.
        """
        clean = kwargs.pop('clean', False)
        if not self._is_rendered:
            self.render()
        if clean:
            self.clean()
        return super(EmailMessage, self).send(*args, **kwargs)

    def clean(self):
        """
        Remove any template specific properties from the message object.

        Useful if you want to serialize rendered message without
        template-specific properties. Also allows to avoid conflicts with
        Djrill/Mandrill and other third-party systems that may fail because
        of non-standard properties of the message object.

        The messages should be rendered already, or you will have to setup the
        ``context`` and ``template``/``template_name`` after deserialization.

        In most cases you can pass the ``clean`` parameter to the constructor
        or another appropriate method of this class.
        """
        del self.context
        del self.template
        del self.template_name


    def _get_block(self, content, name):
        marks = tuple(app_settings.TAG_FORMAT.format(block=name, bound=bound)
                      for bound in ('start', 'end'))
        start, end = (content.find(m) for m in marks)
        if start == -1 or end == -1:
            return
        return content[start + len(marks[0]) : end].strip('\n\r')

    def __getstate__(self):
        """
        Exclude Template objects from pickling, b/c they can't be pickled.
        """
        return dict((k, v) for k, v in self.__dict__.items()
                    if not k in ('template',))

    def __setstate__(self, state):
        """
        Reinitialise the `template` property. It will be loaded if needed.
        """
        self.__dict__ = state
        self.template = None
