from django.test import TestCase
from django.urls import reverse
from .models import Service

class ServicesViewsTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Test Service',
            description='Test Description',
            hourly_rate=100.00
        )
    
    def test_home_services_page(self):
        response = self.client.get(reverse('services:home_services'))
        self.assertEqual(response.status_code, 200)
        
    def test_business_services_page(self):
        response = self.client.get(reverse('services:business_services'))
        self.assertEqual(response.status_code, 200)

    # TODO: Implement test for book_service view once the feature is ready
    # - Need to create mock service booking data
    # - Test both GET (form display) and POST (form submission) requests
    # - Verify successful booking redirects to confirmation page
    # - Test validation errors handling
    # def test_book_service_page(self):
    #     response = self.client.get(
    #         reverse('services:book_service', args=[self.service.id])
    #     )
    #     self.assertEqual(response.status_code, 200)
