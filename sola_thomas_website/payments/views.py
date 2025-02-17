import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from services.models import Service

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_page(request):
    services = Service.objects.all()
    return render(request, 'payments/payment.html', {
        'services': services,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@csrf_exempt
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        service_id = data['service_id']
        hours = float(data['hours'])
        
        service = Service.objects.get(id=service_id)
        amount = int(service.hourly_rate * hours * 100)  # Convert to cents

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            metadata={
                'service_id': service_id,
                'hours': hours
            }
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        
        if event['type'] == 'payment_intent.succeeded':
            # Handle successful payment
            payment_intent = event['data']['object']
            # Add your payment success logic here
            
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
