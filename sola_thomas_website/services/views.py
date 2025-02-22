from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service

def home_services(request):
    """View function for the home services page."""
    # Get all services marked as home services
    services = Service.objects.filter(category='home').order_by('order')
    context = {
        'services': services,
        'faqs': FAQ.objects.filter(category='home').order_by('order'),
    }
    return render(request, 'services/home_services.html', context)

def business_services(request):
    services = Service.objects.filter(category='business')
    return render(request, 'services/business_services.html', {
        'services': services
    })

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        # Add booking logic here
        return redirect('services:payment', booking_id=1)  # Replace with actual booking ID
    return render(request, 'services/book_service.html', {
        'service': service
    })

@login_required
def payment(request, booking_id):
    # Add payment processing logic here
    return render(request, 'services/payment.html', {
        'booking_id': booking_id
    })
