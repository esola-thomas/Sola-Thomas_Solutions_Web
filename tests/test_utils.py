from django.test import TestCase, Client
from django.core import mail
from django.urls import reverse
from django.conf import settings
from utils import send_contact_notification
import json

class UtilsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_send_contact_notification(self):
        # Checks that an email is sent and contains correct details.
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        }
        send_contact_notification(test_data)
        
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, 'New Contact Form Submission')
        self.assertIn(test_data['name'], sent_mail.body)
        self.assertIn(test_data['email'], sent_mail.body)
        self.assertIn(test_data['message'], sent_mail.body)

    def test_stripe_payment_intent(self):
        # Tests Stripe API endpoint returns a valid client secret.
        response = self.client.post(
            reverse('create_payment_intent'),
            data=json.dumps({'amount': 1000}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('clientSecret', data)

class ContextProcessorTests(TestCase):
    def test_google_analytics_context(self):
        # Verifies Google Analytics ID is present in template context.
        response = self.client.get(reverse('home'))
        self.assertIn('GOOGLE_ANALYTICS_ID', response.context)
        self.assertEqual(response.context['GOOGLE_ANALYTICS_ID'], settings.GOOGLE_ANALYTICS_ID)
# Review: Utility and context processor functions are properly verified.
