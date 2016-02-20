"""
.. module:: mail_templated.utils
   :synopsis: Additional utils of django-mail-templated package.

.. moduleauthor:: Artem Rizhov <artem.rizhov@gmail.com>
"""

from django.core import mail

from .message import EmailMessage


def send_mail(template_name, context, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, **kwargs):
    """
    Easy wrapper for sending a single email message to a recipient list using
    django template system.

    It works almost the same way as the standard
    :func:`send_mail()<django.core.mail.send_mail>` function.

    .. |main_difference| replace:: The main
        difference is that two first arguments ``subject`` and ``body`` are
        replaced with ``template_name`` and ``context``. However you still can
        pass subject or body as keyword arguments to provide static content if
        needed.

    |main_difference|

    The ``template_name``, ``context``, ``from_email`` and ``recipient_list``
    parameters are required.


    Note
    ----
    |args_note|

    Arguments
    ---------
    template_name : str
        |template_name|
    context : dict
        |context|
    from_email : str
        |from_email|
    recipient_list : list
        |recipient_list|

    Keyword Arguments
    -----------------
    fail_silently : bool
        If it's False, send_mail will raise an :exc:`smtplib.SMTPException`.
        See the :mod:`smtplib` docs for a list of possible exceptions, all of
        which are subclasses of :exc:`smtplib.SMTPException`.
    auth_user | str
        The optional username to use to authenticate to the SMTP server. If
        this isn't provided, Django will use the value of the
        :django:setting:`EMAIL_HOST_USER` setting.
    auth_password | str
        The optional password to use to authenticate to the SMTP server. If
        this isn't provided, Django will use the value of the
        :django:setting:`EMAIL_HOST_PASSWORD` setting.
    connection : EmailBackend
        The optional email backend to use to send the mail. If unspecified,
        an instance of the default backend will be used. See the documentation
        on :ref:`Email backends<django:topic-email-backends>` for more details.
    subject : str
        |subject|
    body : str
        |body|
    render : bool
        |render|

    Returns
    -------
    int
        The number of successfully delivered messages (which can be 0 or 1
        since it can only send one message).

    See Also
    --------
    :func:`django.core.mail.send_mail`
        Documentation for the standard ``send_mail()`` function.
    """

    connection = connection or mail.get_connection(username=auth_user,
                                                   password=auth_password,
                                                   fail_silently=fail_silently)
    clean = kwargs.pop('clean', True)
    return EmailMessage(
        template_name, context, from_email, recipient_list,
        connection=connection, **kwargs).send(clean=clean)

