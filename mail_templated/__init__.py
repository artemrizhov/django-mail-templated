from django.template.loader import get_template
from django.template.loader_tags import BlockNode
from django.template import Context
from django.conf import settings
from django.core import mail

class EmailMessage(mail.EmailMultiAlternatives):
    """Extends standard EmailMessage class with ability to use templates"""
    
    supported_block_names = ('body', 'subject', 'from', 'html',
        'extra_headers')

    def __init__(self, template_name, context, *args, **kwargs):
        # Save context to process on send().
        self._context = context
        
        # It's not set by default, but we may ommit the html content.
        self.alternatives = []
        
        # the superclass constructor will write to some of our properties,
        # which requires that we initialize self.current_values first.
        self.current_values = {'html': None}

        # This initialises the member variables named by
        # supported_block_names (among others) to values that we want
        # to remember as default values, in case the user replaces the
        # template with one that doesn't specify them.
        super(mail.EmailMultiAlternatives, self).__init__(*args, **kwargs)
        self.default_values = dict(self.current_values)
        
        # This causes template loading and assignment to variables, which
        # may override the defaults set by EmailMultiAlternatives, or the
        # parameters passed in kwargs, with the values from blocks in the
        # template...
        self.template_name = template_name

        # re-override any parameters supplied by the user
        self.current_values.update(kwargs)

    @property
    def template_name(self):
        return self._template_name

    @template_name.setter
    def template_name(self, value):
        self._template_name = value
        # Load the template.
        self.template = get_template(self._template_name)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

        # Render template blocks now, to save rendering them each time
        # we send a message.
        
        # Prepare context
        context = Context(self.context)

        # Restore all values to defaults, in case the new template doesn't
        # define some of them.
        self.current_values = dict(self.default_values)
        
        for block in self._template.nodelist:
            # We are interested in BlockNodes only. Ignore another elements.
            if isinstance(block, BlockNode):
                if block.name == 'from':
                    # we're not allowed to have a method or property
                    # called "from"
                    name = 'from_email'
                else:
                    name = block.name
                setattr(self, name, block.render(context).strip('\n\r'))

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value
    
        # render again with new context
        self.template = getattr(self, 'template', None)
        
    @property
    def from_email(self):
        return self.current_values['from']
    
    @from_email.setter
    def from_email(self, value):
        self.current_values['from'] = value

    @property
    def subject(self):
        return self.current_values['subject']
    
    @subject.setter
    def subject(self, value):
        self.current_values['subject'] = value

    @property
    def body(self):
        return self.current_values['body']
    
    @body.setter
    def body(self, value):
        self.current_values['body'] = value

    @property
    def html(self):
        return self.current_values['html']
    
    @html.setter
    def html(self, value):
        self.current_values['html'] = value

    @property
    def extra_headers(self):
        return self.current_values['extra_headers']
    
    @extra_headers.setter
    def extra_headers(self, value):
        # import pdb; pdb.set_trace()
        
        if not isinstance(value, basestring):
            # ensure that it's a dict-like object
            self.current_values['extra_headers'] = dict(value)
            return
        
        # it's a string, so parse it:
        last_header = None
        headers = []
        
        for line in value.splitlines():
            if line.startswith('\t') or line.startswith(' '):
                last_header += line
            else:
                if last_header is not None:
                    headers.append(last_header)
                last_header = line
        if last_header is not None:
            headers.append(last_header)
        
        extra_headers = {}
        
        for header in headers:
            import re
            mo = re.match("^([A-Za-z0-9_-]*): (.*)", header)
            
            if mo is None:
                raise Exception("Invalid header line: %s" % header)
            
            name, value = mo.group(1, 2)
            extra_headers[name] = value
        
        self.current_values['extra_headers'] = extra_headers

    def send(self, *args, **kwargs):
        "Render email with the current context and send it"
        return super(mail.EmailMultiAlternatives, self).send(*args, **kwargs)
    
    def __repr__(self):
        return "EmailMessage(%s)" % self.current_values

def send_mail(template_name, context, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None):
    """
    Easy wrapper for sending a single message to a recipient list using
    django template system.
    All members of the recipient list will see the other recipients in
    the 'To' field.

    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.
    """

    connection = connection or mail.get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    return EmailMessage(template_name, context, None, None, from_email,
                        recipient_list, connection=connection).send()
