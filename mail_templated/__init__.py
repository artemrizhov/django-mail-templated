from django.core import mail

from .message import EmailMessage


def send_mail(template_name, context, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, *args, **kwargs):
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
    clean = kwargs.pop('clean', True)
    return EmailMessage(
        template_name, context, from_email, recipient_list,
        connection=connection, *args, **kwargs).send(clean=clean)
