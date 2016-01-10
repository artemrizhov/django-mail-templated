from django.core import mail
from django.test import TestCase
from django.utils import translation

from . import send_mail, EmailMessage


class BaseMailTestCase(TestCase):

    def _assertMessage(self, from_email, to, subject, body):
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.from_email, from_email)
        self.assertEqual(message.to, to)
        self.assertEqual(message.subject, subject)
        self.assertEqual(message.body, body)
        return message


class SendMailTestCase(BaseMailTestCase):

    def _send_mail(self, template_name, context, from_email, to,
                   res_subject, res_body, *args, **kwargs):
        send_mail(template_name, context, from_email, to, *args, **kwargs)
        return self._assertMessage(from_email, to, res_subject, res_body)

    def test_plain(self):
        self._send_mail(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.')

    def test_html(self):
        self._send_mail(
            'mail_templated_test/plain.html', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is an html message.')

    def test_multipart(self):
        message = self._send_mail(
            'mail_templated_test/multipart.html', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text part.')
        self.assertEqual(len(message.alternatives), 1)
        self.assertEqual(message.alternatives[0][0],
                         'User, this is an html part.')
        self.assertEqual(message.alternatives[0][1], 'text/html')

    def test_multilang(self):
        translation.activate('en')
        self._send_mail(
            'mail_templated_test/multilang.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.')
        translation.deactivate()

    def test_alternatives(self):
        message = self._send_mail(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.',
            alternatives=[('HTML alternative', 'text/html')])
        self.assertEqual(len(message.alternatives), 1)
        self.assertEqual(message.alternatives[0][0],
                         'HTML alternative')
        self.assertEqual(message.alternatives[0][1], 'text/html')

    def test_multipart_alternatives(self):
        message = self._send_mail(
            'mail_templated_test/multipart.html', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text part.',
            alternatives=[('HTML alternative', 'text/html')])
        self.assertEqual(len(message.alternatives), 2)
        self.assertEqual(message.alternatives[0][0],
                         'HTML alternative')
        self.assertEqual(message.alternatives[0][1], 'text/html')
        self.assertEqual(message.alternatives[1][0],
                         'User, this is an html part.')
        self.assertEqual(message.alternatives[1][1], 'text/html')


class EmailMessageTestCase(BaseMailTestCase):

    def _send_mail(self, template_name, context, from_email, to,
                   res_subject, res_body, *args, **kwargs):
        message = EmailMessage(template_name, context, from_email, to,
                               *args, **kwargs)
        message.send()
        return self._assertMessage(from_email, to, res_subject, res_body)

    def test_plain(self):
        self._send_mail(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.')

    def test_defaults(self):
        self._send_mail(
            'mail_templated_test/empty.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Static subject',
            'Static body',
            subject='Static subject', body='Static body')

    def test_overridden_defaults(self):
        self._send_mail(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.',
            subject='Static subject', body='Static body')

    def test_render(self):
        message = EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'}, render=True)
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text message.')

    def test_norender(self):
        message = EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'})
        self.assertEqual(message.subject, None)
        self.assertEqual(message.body, None)
