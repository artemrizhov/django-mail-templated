.. Django-Mail-Templated documentation master file, created by
   sphinx-quickstart on Wed Feb 17 21:51:15 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |_| unicode:: 0xA0
  :trim:

.. meta::
   :google-site-verification: Wo1vgdtvf4sgKDTxIHRDzM4YXH7mWP24zLNWCOkKbeY

Welcome to Django |_| Mail |_| Templated documentation!
=======================================================

.. image:: https://readthedocs.org/projects/django-mail-templated/badge/?version=latest
:target: http://django-mail-templated.readthedocs.org/en/latest/?badge=latest
:alt: Documentation Status

Django Mail Templated is a tiny wrapper around the standard ``EmailMessage``
class and ``send_mail()`` function that provides an easy way to create email
messages using the :mod:`Django template system <django.template>`

The `Source code <https://github.com/artemrizhov/django-mail-templated>`_ is
available at GitHub under MIT license.

Features
--------

* Built with OOP, KISS and flexibility in mind. Really small and simple, but
  yet full-featured (I hope).

* Extends and mimics the built-in Django's
  :class:`EmailMessage <django.core.mail.EmailMessage>` and
  :func:`send_mail() <django.core.mail.send_mail>`. Compatible as much as
  possible.

* Fully supports Django template system including template inheritance
  (thanks to *BradWhittington* for the note about the problem).

* Supports any possible template engines and loaders.

* Supports serialisation (thanks to *arjandepooter*).

* Fully covered with tests.

* Tested with Django 1.4-1.9.

* Compatible with Python 3.


Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   getting_started
   api
   troubleshuting
   changelog
   contributors