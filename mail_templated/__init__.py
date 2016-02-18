"""
.. module:: mail_templated
   :synopsis: Helpers to easily send email with Django templates.

.. moduleauthor:: Artem Rizhov <artem.rizhov@gmail.com>


Like the standard :mod:`django.core.mail` module, :mod:`mail_templated`
provides two options to send an email message:

* `send_mail()`_ function for simple usage,
* `EmailMessage`_ class for advanced usage.
"""

from .utils import send_mail
from .message import EmailMessage