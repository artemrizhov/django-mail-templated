from django.conf import settings
from django.test import TestCase
from mail_templated import EmailMessage

class MailTemplatedTest(TestCase):
    def test_simple(self):
        email = EmailMessage('simple.email',
            {'foo': 'bar'}, to=['test@example.com'])
        
        self.assertEqual('kevin spacey', email.subject)
        self.assertEqual('The Admin <admin@example.com>', email.from_email)
        self.assertItemsEqual(['test@example.com'], email.to)
        self.assertDictEqual({
            'X-Wrapped': 'wrap\twrap',
            'X-Other': 'whee',
        }, email.extra_headers)
        self.assertEqual('Hello bar.', email.body)

    def test_body_only(self):
        # import pdb; pdb.set_trace()
        
        email = EmailMessage('body_only.email',
            {'foo': 'bar'}, to=['test@example.com'])
        
        self.assertEqual('', email.subject)
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, email.from_email)
        self.assertItemsEqual(['test@example.com'], email.to)
        self.assertDictEqual({}, email.extra_headers)
        self.assertEqual('Only bar.', email.body)

    def test_change_template_then_context(self):
        email = EmailMessage('body_only.email',
            {'foo': 'bar'}, to=['test@example.com'])
        
        email.template_name = 'simple.email'
        
        # writing to the context doesn't change anything
        # email.context['foo'] = 'baz'

        # but replacing it does:
        email.context = {'foo': 'baz'}

        self.assertEqual('Hello baz.', email.body)

    def test_change_context_then_template(self):
        email = EmailMessage('simple.email',
            {'foo': 'bar'}, to=['test@example.com'])
        
        email.context['foo'] = 'baz'
        email.template_name = 'body_only.email'

        self.assertEqual('Only baz.', email.body)
