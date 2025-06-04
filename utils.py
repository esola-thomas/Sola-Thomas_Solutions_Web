from django.core.mail import send_mail
from django.conf import settings


def send_contact_notification(data):
    """Send email notification for contact form submissions.

    Parameters
    ----------
    data : dict
        Dictionary containing 'name', 'email', and 'message' keys.
    Returns
    -------
    int or None
        Status code (always 1 in Django's send_mail) if mail sent, else None.
    """
    subject = 'New Contact Form Submission'
    body = (
        f"Name: {data.get('name')}\n"
        f"Email: {data.get('email')}\n"
        f"Message: {data.get('message')}"
    )
    try:
        return send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
    except Exception:
        return None

