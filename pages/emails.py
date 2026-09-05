from django.conf import settings
from django.core.mail import EmailMessage


def send_contact_email(*, name, sender_email, subject, message):
    """Deliver one contact-form submission to the site owner's inbox."""
    body = (
        "New contact form submission\n\n"
        f"Name: {name}\n"
        f"Email: {sender_email}\n\n"
        "Message:\n"
        f"{message}"
    )
    email = EmailMessage(
        subject=f"{settings.CONTACT_EMAIL_SUBJECT_PREFIX} {subject}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECEIVER_EMAIL],
        reply_to=[sender_email],
    )
    return email.send(fail_silently=False)
