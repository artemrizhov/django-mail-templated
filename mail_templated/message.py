from django.core import mail
from django.template import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode


class EmailMessage(mail.EmailMultiAlternatives):
    """Extends standard EmailMessage class with ability to use templates"""

    def __init__(self, template_name, context, *args, **kwargs):
        self._subject = None
        self._body = None
        self._html = None
        # This causes template loading.
        self.template_name = template_name
        # Save context for processing on send().
        self.context = context
        super(EmailMessage, self).__init__(*args, **kwargs)

    @property
    def template_name(self):
        return self._template_name

    @template_name.setter
    def template_name(self, value):
        self._template_name = value

        # Load the template.
        # In Django 1.7 get_template() returned a django.template.Template.
        # In Django 1.8 it returns a django.template.backends.django.Template.
        template = get_template(self._template_name)
        self.template = getattr(template, 'template', template)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
        # Prepare template blocks to not search them each time we send
        # a message.
        for block in self._template.nodelist:
            # We are interested in BlockNodes only. Ignore another elements.
            if isinstance(block, BlockNode):
                if block.name == 'subject':
                    self._subject = block
                elif block.name == 'body':
                    self._body = block
                if block.name == 'html':
                    self._html = block

    def send(self, *args, **kwargs):
        """Render email with the current context and send it"""
        # Prepare context
        context = Context(self.context)
        # Assume the subject may be set manually.
        if self._subject is not None:
            self.subject = self._subject.render(context).strip('\n\r')
        # Same for body.
        if self._body is not None:
            self.body = self._body.render(context).strip('\n\r')
        # The html block is optional, and it also may be set manually.
        if self._html is not None:
            html = self._html.render(context).strip('\n\r')
            if html:
                if not self.body:
                    # This is html only message.
                    self.body = html
                    self.content_subtype = 'html'
                else:
                    # Add alternative content.
                    self.attach_alternative(html, 'text/html')
        return super(EmailMessage, self).send(*args, **kwargs)

    def __getstate__(self):
        """
        Exclude BlockNode and Template objects from pickling, b/c they can't
        be pickled.
        """
        return dict((k, v) for k, v in self.__dict__.iteritems()
                    if not k in ('_body', '_html', '_subject', '_template'))

    def __setstate__(self, state):
        """
        Use the template_name setter after unpickling so the orignal values of
        _body, _html, _subject and _template will be restored.
        """
        self.__dict__ = state
        self.template_name = self._template_name
