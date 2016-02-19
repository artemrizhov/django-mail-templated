from django.core import mail
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from .conf import app_settings


class EmailMessage(mail.EmailMultiAlternatives):
    """Extends standard EmailMessage class with ability to use templates"""

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
            :type context: dict

        Keyword Arguments:
            :param subject: Default message subject.
            :type subject: str
            :param body: Default message body.
            :type body: str
            :param render: If `True`, render template and evaluate `subject`
                and `body` properties immediately. Default is `False`.
            :type render: bool
            :param clean: If `True', remove any template specific properties
                from the message object. This forces immediate rendering like
                the `render` parameter does. Default is `False`.
            :type clean: bool

        Other arguments are passed to the base class method as is.
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

        if render or clean:
            self.render(clean=clean)

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

    def load_template(self, template_name):
        """
        Load the specified template

        Arguments:
            :param template_name: A name of template with optional blocks
                'subject', 'body' and 'html'.
            :type template_name: str
        """
        self.template = get_template(template_name)

    def render(self, clean=False):
        """
        Render email with the current context

        Arguments:
            :param clean: If `True', remove any template specific properties
                from the message object. Default is `False`.
            :type clean: bool
        """
        # Load template if it is not loaded yet.
        if not self.template:
            self.load_template(self.template_name)
        context = Context(self.context)
        # Add tag strings to the context dict.
        context.update(self.extra_context)
        result = self.template.render(context)
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
        if clean:
            self.clean()

    def send(self, *args, **kwargs):
        """
        Render email if needed and send it

        Keyword Arguments:
            :param clean: If `True', remove any template specific properties
                from the message object before sending. Default is `False`.
            :type clean: bool

        Other arguments are passed to the base class method as is.
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

        The messages should be rendered already,
        or you will have to setup the `context` and `template`/`template_name`
        after deserialization.

        In most cases you can pass the `clean` parameter to the constructor
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
