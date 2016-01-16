import pickle

from django.core import mail
from django.template import TemplateDoesNotExist
from django.test import TestCase
from django.utils import translation

from . import send_mail, EmailMessage


CONTEXT2 = {'name': 'User2'}
SUBJECT2 = 'Hello User2'
BODY2 = 'User2, this is a plain text message.'


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

    def test_extended(self):
        self._send_mail(
            'mail_templated_test/extended.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a base message.')

    def test_overridden(self):
        self._send_mail(
            'mail_templated_test/overridden.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Overridden hello User',
            'User, this is overridden message.')

    def test_overridden2(self):
        self._send_mail(
            'mail_templated_test/overridden2.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Overridden hello User',
            'User, this is overridden message.\nReally.')

    def test_whitespaces(self):
        self._send_mail(
            'mail_templated_test/whitespaces.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], 'Hello User',
            '  User, this is a message with preceding and trailing whitespaces.  ')


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

    def test_late_init(self):
        message = EmailMessage()
        message.load_template('mail_templated_test/plain.tpl')
        message.context = {'name': 'User'}
        message.from_email = 'from@inter.net'
        message.to = ['to@inter.net']
        message.send()
        self._assertMessage(
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.')

    def test_attach_alternative(self):
        message = EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'])
        message.attach_alternative('HTML alternative', 'text/html')
        message.send()
        self._assertMessage(
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.')
        self.assertEqual(len(message.alternatives), 1)
        self.assertEqual(message.alternatives[0][0],
                         'HTML alternative')
        self.assertEqual(message.alternatives[0][1], 'text/html')

    def test_pickling(self):
        message = EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'])
        self.assertEqual(message.template, None)
        dumped_message = pickle.dumps(message)
        message = pickle.loads(dumped_message)
        message.send()
        self._assertMessage(
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.')

    def test_pickling_rendered(self):
        message = EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            'from@inter.net', ['to@inter.net'], render=True)
        self.assertNotEqual(message.template, None)
        dumped_message = pickle.dumps(message)
        message = pickle.loads(dumped_message)
        message.send()
        self._assertMessage(
            'from@inter.net', ['to@inter.net'], 'Hello User',
            'User, this is a plain text message.')


class RenderTestCase(BaseMailTestCase):

    def _initMessage(self, *args, **kwargs):
        return EmailMessage(
            'mail_templated_test/plain.tpl', {'name': 'User'},
            *args, **kwargs)

    def _assertIsRendered(self, message, is_rendered, subject='Hello User',
                          body='User, this is a plain text message.'):
        if is_rendered:
            self.assertEqual(message.subject, subject)
            self.assertEqual(message.body, body)
            self.assertTrue(message.is_rendered)
        else:
            self.assertEqual(message.subject, None)
            self.assertEqual(message.body, None)
            self.assertFalse(message.is_rendered)

    def test_init_render(self):
        message = self._initMessage(render=True)
        self._assertIsRendered(message, True)
        message.send()
        self._assertIsRendered(message, True)

    def test_init_norender(self):
        message = self._initMessage()
        self._assertIsRendered(message, False)
        message.send()
        self._assertIsRendered(message, True)

    def test_init_notrender(self):
        message = self._initMessage(render=False)
        self._assertIsRendered(message, False)

    def test_init_cantrender(self):
        self.assertRaises(TemplateDoesNotExist, EmailMessage, render=True)

    def test_manual_render(self):
        message = self._initMessage()
        message.render()
        self._assertIsRendered(message, True)
        message.context = CONTEXT2
        message.render()
        self._assertIsRendered(message, True, SUBJECT2, BODY2)
        message.send()
        self._assertIsRendered(message, True, SUBJECT2, BODY2)

    def test_manual_rerender(self):
        message = self._initMessage(render=True)
        message.context = CONTEXT2
        message.render()
        self._assertIsRendered(message, True, SUBJECT2, BODY2)
        message.send()
        self._assertIsRendered(message, True, SUBJECT2, BODY2)

    def test_manual_cantrender(self):
        message = EmailMessage()
        self.assertRaises(TemplateDoesNotExist, message.render)

    def test_send_norender(self):
        message = self._initMessage()
        message.send()
        self._assertIsRendered(message, True)

    def test_send_notrender(self):
        message = self._initMessage()
        message.send(render=False)
        self._assertIsRendered(message, True)

    def test_send_render(self):
        message = self._initMessage()
        message.send(render=True)
        self._assertIsRendered(message, True)

    def test_send_norerender(self):
        message = self._initMessage(render=True)
        message.context = CONTEXT2
        message.send()
        self._assertIsRendered(message, True)

    def test_send_notrerender(self):
        message = self._initMessage(render=True)
        message.context = CONTEXT2
        message.send(render=False)
        self._assertIsRendered(message, True)

    def test_send_rerender(self):
        message = self._initMessage(render=True)
        message.context = CONTEXT2
        message.send(render=True)
        self._assertIsRendered(message, True, SUBJECT2, BODY2)
