# Prevent 'django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.'
import django
django.setup()

from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.contrib.auth import get_user_model

User = get_user_model()


def send_email(**kwargs) -> str:
    """
    Send email with recently updated and created dishes
    Email will be sent to all registered users
    """
    recipients = []
    users = User.objects.filter(email__isnull=False)

    for user in users:
        recipients.append(user.email)

    if len(recipients) < 1:
        return "Emails haven't been sent, no active users"

    updated = kwargs['updated_dishes']
    created = kwargs['created_dishes']

    if len(updated) > 0 or len(created) > 0:

        email = EmailMessage(
            "Hello, your favourite restaurants got some new dishes for you",
            f" Updated dishes: {[(i.name, i.menu.name) for i in updated]}"
            f" New dishes: {[(i.name, i.menu.name) for i in created]}",
            "emenu@emenu.com",
            recipients
        )

        try:
            email.send(fail_silently=False)
        except SMTPException as e:
            return f"Emails haven't been sent: {e}"

    return "Emails have been sent"
