"""
.. module:: mail_templated.message
   :synopsis: Main classes of django-mail-templated package.

.. moduleauthor:: Artem Rizhov <artem.rizhov@gmail.com>
"""

from django.core import mail
from django.template import Context
from django.template.loader import get_template


class EmailMessage(mail.EmailMultiAlternatives):
    """
    Extends standard EmailMultiAlternatives class with ability to use templates

    See Also
    --------
    :class:`django.core.mail.EmailMessage`
        Documentation for the standard email message classes.
    """

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
        """
        self.template_name = template_name
        self.context = context
        subject = kwargs.pop('subject', None)
        body = kwargs.pop('body', None)
        render = kwargs.pop('render', False)
        self.template = None
        self._is_rendered = False

        super(EmailMessage, self).__init__(subject, body, *args, **kwargs)

        if render:
            self.render()

    @property
    def is_rendered(self):
        return self._is_rendered

    def load_template(self, template_name):
        """
        Load a template by it's name using the current
        :ref:`template loaders <django:template-loaders>`.

        Arguments
        ---------
        template_name : str
            |template_name|
        """
        self.template = get_template(template_name)

    def render(self):
        """
        Render email with the current context
        """
        # Load template if it is not loaded yet.
        if not self.template:
            self.load_template(self.template_name)
        result = self.template.render(Context(self.context))
        # Don't overwrite default static value with empty one.
        self.subject = self._get_block(result, 'subject') or self.subject
        self.body = self._get_block(result, 'body') or self.body
        # The html block is optional, and it also may be set manually.
        html = self._get_block(result, 'html')
        if html:
            if not self.body:
                # This is html only message.
                self.body = html
                self.content_subtype = 'html'
            else:
                # Add alternative content.
                self.attach_alternative(html, 'text/html')
        self._is_rendered = True

    def send(self, *args, **kwargs):
        """
        Send email message, render if it is not rendered yet.

        All arguments are passed to
        :class:`EmailMultiAlternatives.send() <django.core.mail.EmailMessage>`.
        """
        if not self._is_rendered:
            self.render()
        return super(EmailMessage, self).send(*args, **kwargs)


    def _get_block(self, content, name):
        marks = tuple('{{#{}_{}#}}'.format(p, name) for p in ('start', 'end'))
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
