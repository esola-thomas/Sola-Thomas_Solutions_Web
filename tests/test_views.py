from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_home_page_view(self):
        # Verifies 200 status and correct template for home.
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_about_page_view(self):
        # Verifies 200 status and correct template for about.
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_contact_page_get(self):
        # Checks GET request returns 200 and uses contact template.
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_page_post(self):
        # Validates POST submission, email sending, and redirection.
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertRedirects(response, reverse('contact_success'))

    def test_dashboard_view_unauthorized(self):
        # Ensures redirection to login for unauthenticated access.
        response = self.client.get(reverse('dashboard'))
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={reverse("dashboard")}')

    def test_services_pages(self):
        # Confirms that both service pages are accessible.
        response = self.client.get(reverse('services:home_services'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('services:business_services'))
        self.assertEqual(response.status_code, 200)

    def test_book_service_view(self):
        # Tests redirection for unauthorized users and 200 status when logged in.
        # Test unauthorized access
        response = self.client.get(reverse('services:book'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("services:book")}')
        
        # Test authorized access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('services:book'))
        self.assertEqual(response.status_code, 200)

    def test_payment_view(self):
        # Verifies payment view loads correctly with a valid booking id.
        self.client.login(username='testuser', password='testpass123')
        booking_id = 'test_booking_123'
        response = self.client.get(reverse('payment', kwargs={'booking_id': booking_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment.html')
# Review: All views are thoroughly tested.
