from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def home_services(request):
    """View function for the home services page."""
    return render(request, 'services/home_services.html')

def business_services(request):
    return render(request, 'services/business_services.html')

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
