from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email(subject, message, to_email, html_message=None):
    """
    Utility function to send emails using SendGrid
    
    Parameters:
    - subject: Email subject
    - message: Plain text message content
    - to_email: Recipient email address
    - html_message: Optional HTML content for the email
    
    Returns:
    - status code on success, None on failure
    """
    try:
        # Create email message
        if html_message:
            email = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=to_email,
                subject=subject,
                plain_text_content=message,
                html_content=html_message
            )
        else:
            email = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=to_email,
                subject=subject,
                plain_text_content=message
            )
        
        # Send email via SendGrid
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(email)
        logger.info(f"Email sent successfully with status code: {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return None


def send_contact_notification(name, email, subject, message, html_content=None):
    """
    Send notification when contact form is submitted
    
    Parameters:
    - name: Name of the person submitting the form
    - email: Email of the person submitting the form
    - subject: Subject of their message
    - message: The message they sent
    - html_content: Optional HTML formatted message
    
    Returns:
    - status code on success, None on failure
    """
    email_subject = f"Sola-Thomas Web Contact Form: {subject}"
    
    email_body = f"""
    New contact form submission:
    
    Name: {name}
    Email: {email}
    Subject: {subject}
    
    Message:
    {message}
    """
    
    return send_email(email_subject, email_body, settings.CONTACT_EMAIL, html_content)
