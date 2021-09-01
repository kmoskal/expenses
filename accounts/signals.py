from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.conf import settings

from .models import ActivateAccount


@receiver(post_save, sender=ActivateAccount)
def activate_account_confirmation(sender, instance, created, **kwargs):
    """
    Send email to confirmation account.
    """
    account = instance
    activation_link = settings.HOST + settings.HOST_PORT \
                      + settings.ACTIVATION_URL + account.token
    message = get_template("activate-mail/index.html").render({
        'link': activation_link
    })

    email = EmailMessage(
        subject="Expenses activation link",
        body=message,
        from_email="no-reply@chrisoft.pl",
        to=[account.email],
        reply_to=["no-reply@chrisoft.pl"],
    )
    email.content_subtype = "html"
    return email.send()
