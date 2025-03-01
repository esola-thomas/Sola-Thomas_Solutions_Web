from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_service_notification(service):
    """
    Send a notification email when a new service is created.
    """
    mail_subject = 'New Service Added to Your Account'
    message = render_to_string('clientportal/emails/service_notification.html', {
        'user': service.user,
        'service': service,
        'domain': settings.SITE_DOMAIN,
    })
    
    return send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [service.user.email],
        fail_silently=False,
        html_message=message,
    )

def send_invoice_notification(invoice):
    """
    Send a notification email when a new invoice is created.
    """
    mail_subject = 'New Invoice from Sola-Thomas Solutions'
    message = render_to_string('clientportal/emails/invoice_notification.html', {
        'user': invoice.user,
        'invoice': invoice,
        'domain': settings.SITE_DOMAIN,
    })
    
    return send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [invoice.user.email],
        fail_silently=False,
        html_message=message,
    )

def send_note_response_notification(note):
    """
    Send a notification email when admin responds to a user's note.
    """
    mail_subject = 'Response to Your Note from Sola-Thomas Solutions'
    message = render_to_string('clientportal/emails/note_response_notification.html', {
        'note': note,
        'domain': settings.SITE_DOMAIN,
    })
    
    return send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [note.user.email],
        fail_silently=False,
        html_message=message,
    )

def send_request_status_notification(service_request):
    """
    Send a notification email when a service request status is updated.
    """
    status_display = service_request.get_status_display()
    mail_subject = f'Service Request {status_display}: {service_request.title}'
    
    message = render_to_string('clientportal/emails/service_request_status.html', {
        'service_request': service_request,
        'domain': settings.SITE_DOMAIN,
    })
    
    return send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [service_request.user.email],
        fail_silently=False,
        html_message=message,
    )
