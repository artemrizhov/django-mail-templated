from django.core import mail
from django.test import TestCase
from django.utils import translation

from . import send_mail, EmailMessage


class SendMailTestCase(TestCase):

    def test_plain(self):
        send_mail(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'])
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.from_email, 'from@inter.net')
        self.assertEqual(message.to, ['to@inter.net'])
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text message.')

    def test_html(self):
        send_mail(
            'mail_templated_test/plain.html', {'name': 'User'},
            'from@inter.net', ['to@inter.net'])
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is an html message.')

    def test_multipart(self):
        send_mail(
            'mail_templated_test/multipart.html', {'name': 'User'},
            'from@inter.net', ['to@inter.net'])
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text part.')
        self.assertEqual(len(message.alternatives), 1)
        self.assertEqual(message.alternatives[0][0],
                         'User, this is an html part.')
        self.assertEqual(message.alternatives[0][1], 'text/html')

    def test_multilang(self):
        translation.activate('en')
        send_mail(
            'mail_templated_test/multilang.html', {'name': 'User'},
            'from@inter.net', ['to@inter.net'])
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text part.')
        translation.deactivate()

    def test_alternatives(self):
        send_mail(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'],
            alternatives=[('HTML alternative', 'text/html')])
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.from_email, 'from@inter.net')
        self.assertEqual(message.to, ['to@inter.net'])
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text message.')
        self.assertEqual(len(message.alternatives), 1)
        self.assertEqual(message.alternatives[0][0],
                         'HTML alternative')
        self.assertEqual(message.alternatives[0][1], 'text/html')

    def test_multipart_alternatives(self):
        send_mail(
            'mail_templated_test/multipart.html', {'name': 'User'},
            'from@inter.net', ['to@inter.net'],
            alternatives=[('HTML alternative', 'text/html')])
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text part.')
        self.assertEqual(len(message.alternatives), 2)
        self.assertEqual(message.alternatives[0][0],
                         'HTML alternative')
        self.assertEqual(message.alternatives[0][1], 'text/html')
        self.assertEqual(message.alternatives[1][0],
                         'User, this is an html part.')
        self.assertEqual(message.alternatives[1][1], 'text/html')


class EmailMessageTestCase(TestCase):

    def test_plain(self):
        message = EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'])
        message.send()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.from_email, 'from@inter.net')
        self.assertEqual(message.to, ['to@inter.net'])
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text message.')

    def test_defaults(self):
        message = EmailMessage(
            'mail_templated_test/empty.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'],
            subject='Static subject', body='Static body')
        message.send()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Static subject')
        self.assertEqual(message.body, 'Static body')

    def test_overridden_defaults(self):
        message = EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'],
            subject='Static subject', body='Static body')
        message.send()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Hello User')
        self.assertEqual(message.body,
                         'User, this is a plain text message.')
