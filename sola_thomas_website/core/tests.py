from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Service, Testimonial

class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        
    def test_home_page_status_code(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_about_page_status_code(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        
    def test_contact_form_submission(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 302)
        
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 302)
