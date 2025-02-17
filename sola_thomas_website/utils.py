from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email(subject, message, to_email):
    """
    Utility function to send emails using SendGrid
    """
    email = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=message
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(email)
        logger.info(f"Email sent successfully with status code: {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return None

def send_contact_notification(name, email, message):
    """
    Send notification when contact form is submitted
    """
    subject = f"New Contact Form Submission from {name}"
    email_body = f"""
    New contact form submission:
    
    Name: {name}
    Email: {email}
    Message:
    {message}
    """
    return send_email(subject, email_body, settings.CONTACT_EMAIL)
