from django.test import TestCase
from django.urls import reverse
import stripe
from unittest.mock import patch

class PaymentViewsTest(TestCase):
    def setUp(self):
        self.payment_intent_id = 'pi_test_123'
    
    # TODO Set Payments
    # @patch('stripe.PaymentIntent.create')
    # def test_create_payment_intent(self, mock_create):
    #     mock_create.return_value = type('obj', (object,), {
    #         'client_secret': 'test_secret'
    #     })
        
    #     response = self.client.post(
    #         reverse('payments:create_payment_intent'),
    #         {'service_id': 1, 'hours': 2},
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 200)
