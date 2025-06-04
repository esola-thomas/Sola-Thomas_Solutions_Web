from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core import mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import json
from datetime import datetime, timedelta
from .models import WorkOrder, Invoice, Review, ServiceNote, ServiceRequest
from .forms import ReviewForm, InvoiceForm, CustomUserForm, ServiceForm, ServiceNoteForm, ProcessRequestForm
from .tokens import account_activation_token

class ModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='password123',
            is_staff=True
        )
        
        # Create test invoice
        self.invoice = Invoice.objects.create(
            user=self.regular_user,
            amount=150.00,
            details="Test invoice details",
            due_date=timezone.now().date() + timedelta(days=30),
            paid=False
        )
        
        # Create test work order
        self.work_order = WorkOrder.objects.create(
            user=self.regular_user,
            name="Test Service",
            description="This is a test service description",
            date_performed=timezone.now().date() - timedelta(days=7),
            invoice=self.invoice
        )
        
        # Create test review
        self.review = Review.objects.create(
            user=self.regular_user,
            service=self.work_order,
            rating=5,
            comment="Excellent service!"
        )
        
        # Create test service note
        self.note = ServiceNote.objects.create(
            service=self.work_order,
            user=self.regular_user,
            message="This is a test note",
            is_resolved=False
        )
        
        # Create test service request
        self.service_request = ServiceRequest.objects.create(
            user=self.regular_user,
            title="Test Service Request",
            description="Need a new service",
            requested_date=timezone.now().date() + timedelta(days=14),
            status='pending'
        )
    
    def test_service_model(self):
        self.assertEqual(str(self.work_order), "Test Service - testuser")
        self.assertEqual(self.work_order.user, self.regular_user)
        self.assertEqual(self.work_order.invoice, self.invoice)
        
    def test_invoice_model(self):
        self.assertEqual(self.invoice.amount, 150.00)
        self.assertEqual(self.invoice.paid, False)
        self.assertEqual(self.invoice.user, self.regular_user)
        self.assertIn("Invoice #", str(self.invoice))
        
    def test_review_model(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.service, self.work_order)
        self.assertEqual(self.review.user, self.regular_user)
        self.assertIn("Review by testuser", str(self.review))
        
    def test_service_note_model(self):
        self.assertEqual(self.note.message, "This is a test note")
        self.assertEqual(self.note.is_resolved, False)
        self.assertIsNone(self.note.admin_response)
        self.assertEqual(self.note.service, self.work_order)
        self.assertEqual(self.note.user, self.regular_user)
        
    def test_service_request_model(self):
        self.assertEqual(self.service_request.status, 'pending')
        self.assertEqual(self.service_request.title, "Test Service Request")
        self.assertEqual(self.service_request.user, self.regular_user)
        self.assertIsNone(self.service_request.processed_by)
        self.assertIsNone(self.service_request.service)

class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.work_order = WorkOrder.objects.create(
            user=self.user,
            name="Test Service",
            description="This is a test service",
            date_performed=timezone.now().date()
        )
    
    def test_review_form(self):
        form_data = {
            'rating': 4,
            'comment': 'Good service'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invoice_form(self):
        form_data = {
            'user': self.user.id,
            'amount': 100.00,
            'details': 'Test invoice',
            'due_date': timezone.now().date() + timedelta(days=30),
            'paid': False
        }
        form = InvoiceForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_service_form(self):
        form_data = {
            'user': self.user.id,
            'name': 'New Service',
            'description': 'New service description',
            'date_performed': timezone.now().date(),
            'admin_notes': 'Test admin notes',
            'invoice': ''  # Optional field
        }
        form = ServiceForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_service_note_form(self):
        form_data = {
            'message': 'This is a test message'
        }
        form = ServiceNoteForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_process_request_form(self):
        form_data = {
            'status': 'approved',
            'admin_notes': 'Approved request',
            'create_service': True
        }
        form = ProcessRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # Create staff user
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='password123',
            is_staff=True
        )
        
        # Create inactive user for activation testing
        self.inactive_user = User.objects.create_user(
            username='inactiveuser',
            email='inactive@example.com',
            password='password123',
            is_active=False
        )
        
        # Create test data
        self.invoice = Invoice.objects.create(
            user=self.regular_user,
            amount=150.00,
            details="Test invoice details",
            due_date=timezone.now().date() + timedelta(days=30),
            paid=False
        )
        
        self.work_order = WorkOrder.objects.create(
            user=self.regular_user,
            name="Test Service",
            description="This is a test service description",
            date_performed=timezone.now().date() - timedelta(days=7),
            invoice=self.invoice
        )
        
        self.service_note = ServiceNote.objects.create(
            service=self.work_order,
            user=self.regular_user,
            message="This is a test note",
            is_resolved=False
        )
        
        self.service_request = ServiceRequest.objects.create(
            user=self.regular_user,
            title="Test Service Request",
            description="Need a new service",
            requested_date=timezone.now().date() + timedelta(days=14),
            status='pending'
        )
    
    # Authentication tests
    def test_login_view(self):
        response = self.client.get(reverse('clientportal:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientportal/registration/login.html')
        
        # Test valid login
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(reverse('clientportal:login'), login_data)
        self.assertRedirects(response, reverse('clientportal:dashboard'))
        
        # Test invalid login
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('clientportal:login'), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username OR Password is incorrect")
    
    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('clientportal:logout'))
        self.assertRedirects(response, reverse('clientportal:login'))
    
    # Dashboard tests
    def test_dashboard_access(self):
        # Unauthorized access should redirect to login
        response = self.client.get(reverse('clientportal:dashboard'))
        self.assertRedirects(response, f"/portal/login/?next={reverse('clientportal:dashboard')}")
        
        # Log in and access dashboard
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('clientportal:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientportal/dashboard.html')
        
    def test_admin_dashboard_access(self):
        # Regular user should be redirected from admin dashboard
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('clientportal:admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Staff user should access admin dashboard
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('clientportal:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientportal/admin_dashboard.html')
    
    # Service tests
    def test_submit_review(self):
        self.client.login(username='testuser', password='password123')
        
        # Get review form page
        url = reverse('clientportal:submit_review', kwargs={'service_id': self.work_order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Submit a review
        review_data = {
            'rating': 5,
            'comment': 'Excellent service!'
        }
        response = self.client.post(url, review_data)
        self.assertRedirects(response, reverse('clientportal:dashboard'))
        
        # Check if review was created
        self.assertTrue(Review.objects.filter(user=self.regular_user, service=self.work_order).exists())
    
    def test_create_service_as_admin(self):
        self.client.login(username='staffuser', password='password123')
        
        url = reverse('clientportal:create_service')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Create a new service
        service_data = {
            'user': self.regular_user.id,
            'name': 'New Admin Service',
            'description': 'Service created by admin',
            'date_performed': timezone.now().date().isoformat(),
            'admin_notes': 'Test admin notes'
        }
        response = self.client.post(url, service_data)
        self.assertRedirects(response, reverse('clientportal:admin_dashboard'))
        
        # Check if work order was created
        self.assertTrue(WorkOrder.objects.filter(name='New Admin Service').exists())
    
    # Service notes tests
    def test_add_service_note(self):
        self.client.login(username='testuser', password='password123')
        
        url = reverse('clientportal:add_service_note', kwargs={'service_id': self.work_order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Add a new note
        note_data = {
            'message': 'This is a new note'
        }
        response = self.client.post(url, note_data)
        self.assertRedirects(response, reverse('clientportal:view_service_notes', kwargs={'service_id': self.work_order.id}))
        
        # Check if note was created
        self.assertTrue(ServiceNote.objects.filter(message='This is a new note').exists())
    
    def test_respond_to_note_as_admin(self):
        self.client.login(username='staffuser', password='password123')
        
        url = reverse('clientportal:respond_to_note', kwargs={'note_id': self.service_note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Respond to note
        response_data = {
            'admin_response': 'This is an admin response',
            'is_resolved': True
        }
        response = self.client.post(url, response_data)
        self.assertRedirects(response, reverse('clientportal:admin_dashboard'))
        
        # Check if note was updated
        self.service_note.refresh_from_db()
        self.assertEqual(self.service_note.admin_response, 'This is an admin response')
        self.assertTrue(self.service_note.is_resolved)
    
    # Service request tests
    def test_create_service_request(self):
        self.client.login(username='testuser', password='password123')
        
        url = reverse('clientportal:create_service_request')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Create a new service request
        request_data = {
            'title': 'New Service Request',
            'description': 'Please provide this service',
            'requested_date': (timezone.now().date() + timedelta(days=10)).isoformat()
        }
        response = self.client.post(url, request_data)
        self.assertRedirects(response, reverse('clientportal:my_service_requests'))
        
        # Check if request was created
        self.assertTrue(ServiceRequest.objects.filter(title='New Service Request').exists())
    
    def test_process_service_request_as_admin(self):
        self.client.login(username='staffuser', password='password123')
        
        url = reverse('clientportal:process_service_request', kwargs={'request_id': self.service_request.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Process the request
        process_data = {
            'status': 'approved',
            'admin_notes': 'Request approved',
            'create_service': True
        }
        response = self.client.post(url, process_data)
        self.assertRedirects(response, reverse('clientportal:admin_dashboard'))
        
        # Check if request was updated
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.status, 'approved')
        self.assertEqual(self.service_request.admin_notes, 'Request approved')
        self.assertIsNotNone(self.service_request.service)
        self.assertEqual(self.service_request.processed_by, self.staff_user)
    
    # Account activation test
    def test_activate_account(self):
        # Generate valid activation parameters
        uid = urlsafe_base64_encode(force_bytes(self.inactive_user.pk))
        token = account_activation_token.make_token(self.inactive_user)
        
        # Test GET request (should show password set form)
        url = f"{reverse('clientportal:activate_account')}?uid={uid}&token={token}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientportal/set_password.html')
        
        # Test POST request with valid passwords
        password_data = {
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(url, password_data)
        self.assertRedirects(response, reverse('clientportal:login'))
        
        # Check if user is now active
        self.inactive_user.refresh_from_db()
        self.assertTrue(self.inactive_user.is_active)
        
        # Test login with new password
        login_result = self.client.login(username='inactiveuser', password='newpassword123')
        self.assertTrue(login_result)

class UtilsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.invoice = Invoice.objects.create(
            user=self.user,
            amount=150.00,
            details="Test invoice details",
            due_date=timezone.now().date() + timedelta(days=30),
            paid=False
        )
        
        self.work_order = WorkOrder.objects.create(
            user=self.user,
            name="Test Service",
            description="This is a test service description",
            date_performed=timezone.now().date() - timedelta(days=7),
            invoice=self.invoice
        )
        
        self.note = ServiceNote.objects.create(
            service=self.work_order,
            user=self.user,
            message="This is a test note",
            is_resolved=False,
            admin_response="Admin response"
        )
        
        self.service_request = ServiceRequest.objects.create(
            user=self.user,
            title="Test Service Request",
            description="Need a new service",
            requested_date=timezone.now().date() + timedelta(days=14),
            status='approved'
        )
    
    def test_send_service_notification(self):
        from .utils import send_service_notification
        
        # Test email sending
        send_service_notification(self.work_order)
        
        # Check that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify the subject of the message
        self.assertEqual(mail.outbox[0].subject, 'New Work Order Added to Your Account')
        
        # Verify the message is sent to the right person
        self.assertEqual(mail.outbox[0].to[0], self.user.email)
    
    def test_send_invoice_notification(self):
        from .utils import send_invoice_notification
        
        # Test email sending
        send_invoice_notification(self.invoice)
        
        # Check that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify the subject of the message
        self.assertEqual(mail.outbox[0].subject, 'New Invoice from Sola-Thomas Solutions')
        
        # Verify the message is sent to the right person
        self.assertEqual(mail.outbox[0].to[0], self.user.email)
    
    def test_send_note_response_notification(self):
        from .utils import send_note_response_notification
        
        # Test email sending
        send_note_response_notification(self.note)
        
        # Check that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify the subject of the message
        self.assertEqual(mail.outbox[0].subject, 'Response to Your Note from Sola-Thomas Solutions')
        
        # Verify the message is sent to the right person
        self.assertEqual(mail.outbox[0].to[0], self.user.email)
    
    def test_send_request_status_notification(self):
        from .utils import send_request_status_notification
        
        # Test email sending
        send_request_status_notification(self.service_request)
        
        # Check that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify the subject contains the status
        self.assertIn('Approved', mail.outbox[0].subject)
        
        # Verify the message is sent to the right person
        self.assertEqual(mail.outbox[0].to[0], self.user.email)

class TokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            is_active=False
        )
    
    def test_account_activation_token(self):
        from .tokens import account_activation_token
        
        # Generate token
        token = account_activation_token.make_token(self.user)
        
        # Token should be valid
        self.assertTrue(account_activation_token.check_token(self.user, token))
        
        # Activate user (changes the hash)
        self.user.is_active = True
        self.user.save()
        
        # Token should now be invalid
        self.assertFalse(account_activation_token.check_token(self.user, token))
