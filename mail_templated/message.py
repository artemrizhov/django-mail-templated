from django.core import mail
from django.template import Context
from django.template.loader import get_template


class EmailMessage(mail.EmailMultiAlternatives):
    """Extends standard EmailMessage class with ability to use templates"""

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
        The argument list is the same as in the base class except of two first
        parameters 'subject' and 'body' which are replaced with 'template_name'
        and 'context'. However you still can pass subject and body as keyword
        arguments to provide some static content if needed.

        Arguments:
            :param template_name: A name of template that extends
                `mail_templated/base.tpl` with blocks 'subject', 'body' and
                 'html'.
            :type template_name: str
            :param context: A dictionary to be used for template rendering.
            :type context: bool

        Keyword Arguments:
            :param subject: Default message subject.
            :type subject: str
            :param body: Default message body.
            :type body: str
            :param render: If `True`, render template and evaluate `subject`
                and `body` properties immediately. Default is `False`.
            :type render: bool

        Other arguments are passed to the base class method as is.
        """
        self.template_name = template_name
        self.context = context
        subject = kwargs.pop('subject', None)
        body = kwargs.pop('body', None)
        render = kwargs.pop('render', False)
        self.template = None
        self._rendered = False

        super(EmailMessage, self).__init__(subject, body, *args, **kwargs)

        if render and template_name:
            self.render()

    def load_template(self, template_name):
        """
        Load the specified template

        Arguments:
            :param template_name: A name of template with optional blocks
                'subject', 'body' and 'html'.
            :type template_name: str
        """
        self.template = get_template(template_name)

    def render(self):
        """Render email with the current context"""
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
        self._rendered = True

    def send(self, *args, **kwargs):
        """
        Render email if needed and send it

        Arguments:
            :param render: If True, render template even if it is rendered
                already.
            :type render: bool

        Other arguments are passed to the base class method.
        """
        if kwargs.pop('render', False) or not self._rendered:
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
        return dict((k, v) for k, v in self.__dict__.iteritems()
                    if not k in ('template',))

    def __setstate__(self, state):
        """
        Reinitialise the `template` property. It will be loaded if needed.
        """
        self.__dict__ = state
        self.template = None
