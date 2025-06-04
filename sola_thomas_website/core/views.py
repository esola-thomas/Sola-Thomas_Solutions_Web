from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
import json

# Import the custom forms and email utilities
from .forms import ContactForm
from .email import send_email
from utils import send_contact_notification

# Set up logger
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    # Determine if this is a form submission
    is_submission = request.method == 'POST'
    
    if is_submission:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']
            
            try:
                # Create HTML email content
                html_message = render_to_string('core/email/contact_email.html', {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message_text,
                })
                
                # Plain text version of the email
                plain_message = strip_tags(html_message)
                
                # Use the dedicated contact notification function with HTML content
                status_code = send_contact_notification(
                    name, 
                    email, 
                    subject,
                    plain_message, 
                    html_message
                )
                
                if status_code and 200 <= status_code < 300:
                    messages.success(request, 'Your message has been sent. We will get back to you soon!')
                    # Return a fresh form on success
                    form = ContactForm()
                else:
                    messages.error(request, 'There was a problem sending your message. Please try again later.')
                    logger.error(f"Failed to send email: Status code {status_code}")
            except Exception as e:
                logger.error(f"Failed to send contact email: {str(e)}")
                messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
        else:
            # If form is invalid, don't display a modal but let Django's form validation display errors
            pass
    else:
        # New page load, not a submission
        form = ContactForm()
    
    # Add a context variable to indicate if this is a form submission 
    # This can be used in the template to decide if we show messages
    context = {
        'form': form,
        'is_submission': is_submission
    }
    
    return render(request, 'core/contact.html', context)

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {
        'bookings': request.user.bookings.all(),
        'invoices': request.user.invoices.all()
    })
