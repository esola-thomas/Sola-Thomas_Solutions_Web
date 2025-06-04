from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.db.models import Exists, OuterRef, Count, Q
from django.core.mail import send_mail
from .models import WorkOrder, Invoice, Review, ServiceNote, ServiceRequest
from .forms import ReviewForm, InvoiceForm, CustomUserForm, ServiceForm, ServiceNoteForm, ServiceNoteResponseForm, ServiceRequestForm, ProcessRequestForm
from .tokens import account_activation_token
from .utils import send_service_notification, send_invoice_notification, send_note_response_notification, send_request_status_notification
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
import pytz
from django.views.decorators.http import require_POST

EST_TIMEZONE = pytz.timezone('US/Eastern')
@login_required
def dashboard(request):
    """
    Regular user dashboard: Shows the user's services, invoices, reviews, and service requests.
    """
    work_orders = WorkOrder.objects.filter(user=request.user)
    
    # Identify services without reviews
    services_without_reviews = work_orders.exclude(
        reviews__user=request.user
    ).order_by('-date_performed')
    
    invoices = Invoice.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    notes = ServiceNote.objects.filter(user=request.user).select_related('service')
    service_requests = ServiceRequest.objects.filter(user=request.user)
    
    # Calculate counts for badges
    unresolved_notes_count = notes.filter(is_resolved=False).count()
    pending_requests_count = service_requests.filter(status='pending').count()
    
    # Current time in EST for context
    current_time_est = timezone.now().astimezone(EST_TIMEZONE)
    
    context = {
        'work_orders': work_orders,
        'work_orders_without_reviews': services_without_reviews,
        'invoices': invoices,
        'reviews': reviews,
        'notes': notes,
        'service_requests': service_requests,
        'unresolved_notes_count': unresolved_notes_count,
        'pending_requests_count': pending_requests_count,
        'current_time_est': current_time_est,
    }
    return render(request, 'clientportal/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    Admin dashboard: Allows staff users to create invoices and view all services,
    invoices, reviews, and manage users.
    """
    # Handle invoice form submission
    if request.method == 'POST' and 'submit-invoice' in request.POST:
        invoice_form = InvoiceForm(request.POST)
        if invoice_form.is_valid():
            invoice = invoice_form.save()
            messages.success(request, "Invoice created successfully.")
            # Send email notification
            try:
                send_invoice_notification(invoice)
            except Exception as e:
                messages.warning(request, f"Invoice created but email notification failed: {str(e)}")
            return redirect('clientportal:admin_dashboard')
        user_form = CustomUserForm()  # Initialize empty user form
    
    # Handle user form submission
    elif request.method == 'POST' and 'submit-user' in request.POST:
        user_form = CustomUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            # Generate a random password that won't be used (user will set via activation)
            user.set_unusable_password()
            user.is_active = False  # User is inactive until they activate account
            user.save()
            
            # Send activation email using settings.SITE_DOMAIN
            mail_subject = 'Activate your Sola-Thomas account'
            message = render_to_string('clientportal/account_activation_email.html', {
                'user': user,
                'domain': settings.SITE_DOMAIN,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                mail_subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message,
            )
            
            messages.success(request, f"User {user.username} created successfully. An activation email has been sent.")
            return redirect('clientportal:admin_dashboard')
        invoice_form = InvoiceForm()  # Initialize empty invoice form
    else:
        invoice_form = InvoiceForm()
        user_form = CustomUserForm()
    
    work_orders = WorkOrder.objects.all()
    invoices = Invoice.objects.all()
    reviews = Review.objects.all()
    users = User.objects.all().order_by('-date_joined')
    notes = ServiceNote.objects.all().select_related('service', 'user').order_by('-created_at')
    service_requests = ServiceRequest.objects.all().order_by('-created_at')
    
    # Calculate counts for badges
    pending_notes_count = notes.filter(admin_response__isnull=True).count()
    pending_requests_count = service_requests.filter(status='pending').count()
    
    context = {
        'invoice_form': invoice_form,
        'user_form': user_form,
        'work_orders': work_orders,
        'invoices': invoices,
        'reviews': reviews,
        'users': users,
        'notes': notes,
        'service_requests': service_requests,
        'pending_notes_count': pending_notes_count,
        'pending_requests_count': pending_requests_count,
    }
    return render(request, 'clientportal/admin_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_invoice(request, invoice_id):
    """
    Allows staff users to edit an existing invoice.
    """
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, f"Invoice #{invoice_id} updated successfully.")
            return redirect('clientportal:admin_dashboard')
    else:
        form = InvoiceForm(instance=invoice)
    
    return render(request, 'clientportal/edit_invoice.html', {
        'form': form,
        'invoice': invoice
    })

@login_required
def submit_review(request, service_id):
    """
    Handles review submission for a specific service (only if the service belongs
    to the current user).
    """
    work_order = get_object_or_404(WorkOrder, pk=service_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.service = service
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect('clientportal:dashboard')
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        # Check if user already submitted a review for this service
        existing_review = Review.objects.filter(user=request.user, service=service).first()
        if (existing_review):
            form = ReviewForm(instance=existing_review)
            messages.info(request, "You're editing your existing review for this service.")
        else:
            form = ReviewForm()
    
    context = {
        'form': form,
        'service': service
    }
    return render(request, 'clientportal/submit_review.html', context)

def activate_account(request):
    """
    Activates the user account and sets the password.
    Uses query parameters for uid and token instead of path parameters.
    """
    uidb64 = request.GET.get('uid')
    token = request.GET.get('token')
    
    if not uidb64 or not token:
        messages.error(request, "Activation link is invalid.")
        return redirect('clientportal:login')
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # If this is a GET request, show the password set form
        if request.method == 'GET':
            return render(request, 'clientportal/set_password.html', {'uid': uidb64, 'token': token})
        
        # If this is a POST request, set the password and activate the account
        elif request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 and password2 and password1 == password2:
                user.set_password(password1)
                user.is_active = True
                user.save()
                messages.success(request, "Your account has been activated. You can now log in.")
                return redirect('clientportal:login')
            else:
                messages.error(request, "Passwords don't match or weren't provided.")
                return render(request, 'clientportal/set_password.html', {'uid': uidb64, 'token': token})
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('clientportal:login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_service(request):
    """
    Allow staff to create a new service for a user.
    """
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            work_order = form.save()
            messages.success(request, f"Work Order '{work_order.name}' created successfully.")
            
            # Send email notification
            try:
                send_service_notification(work_order)
            except Exception as e:
                messages.warning(request, f"Service created but email notification failed: {str(e)}")
                
            return redirect('clientportal:admin_dashboard')
    else:
        form = ServiceForm()
    
    return render(request, 'clientportal/service_form.html', {
        'form': form,
        'title': 'Create Work Order',
        'button_text': 'Create Work Order',
        'is_new': True
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_service(request, service_id):
    """
    Allow staff to edit an existing service.
    """
    work_order = get_object_or_404(WorkOrder, pk=service_id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=work_order)
        if form.is_valid():
            work_order = form.save()
            messages.success(request, f"Work Order '{work_order.name}' updated successfully.")
            return redirect('clientportal:admin_dashboard')
    else:
        form = ServiceForm(instance=work_order)
    
    return render(request, 'clientportal/service_form.html', {
        'form': form,
        'service': work_order,
        'title': 'Edit Work Order',
        'button_text': 'Update Work Order',
        'is_new': False
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def resend_activation_email(request, user_id):
    """
    Resends the activation email to a pending user.
    Only staff members can access this view.
    """
    pending_user = get_object_or_404(User, pk=user_id, is_active=False)
    
    if request.method == 'POST':
        # Send activation email using settings.SITE_DOMAIN
        mail_subject = 'Activate your Sola-Thomas account'
        message = render_to_string('clientportal/account_activation_email.html', {
            'user': pending_user,
            'domain': settings.SITE_DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(pending_user.pk)),
            'token': account_activation_token.make_token(pending_user),
        })
        
        send_mail(
            mail_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [pending_user.email],
            fail_silently=False,
            html_message=message,
        )
        
        messages.success(request, f"Activation email resent to {pending_user.username} ({pending_user.email}).")
        return redirect('clientportal:admin_dashboard')
    else:
        # Show confirmation screen
        return render(request, 'clientportal/resend_activation_confirm.html', {
            'pending_user': pending_user,
        })

@login_required
def add_service_note(request, service_id):
    """
    Allow users to add notes to their services.
    """
    work_order = get_object_or_404(WorkOrder, pk=service_id, user=request.user)
    
    if request.method == 'POST':
        form = ServiceNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.service = work_order
            note.user = request.user
            note.save()
            messages.success(request, "Your note has been submitted successfully.")
            return redirect('clientportal:view_service_notes', service_id=service_id)
    else:
        form = ServiceNoteForm()
    
    return render(request, 'clientportal/add_service_note.html', {
        'form': form,
        'service': work_order
    })

@login_required
def view_service_notes(request, service_id):
    """
    View notes for a specific service.
    """
    work_order = get_object_or_404(WorkOrder, pk=service_id, user=request.user)
    notes = ServiceNote.objects.filter(service=work_order).order_by('-created_at')
    
    return render(request, 'clientportal/view_service_notes.html', {
        'service': work_order,
        'notes': notes
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def respond_to_note(request, note_id):
    """
    Allow admin to respond to a user's note.
    """
    note = get_object_or_404(ServiceNote, pk=note_id)
    
    if request.method == 'POST':
        form = ServiceNoteResponseForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.response_date = timezone.now()
            note.save()
            
            # Send email notification of response
            try:
                send_note_response_notification(note)
            except Exception as e:
                messages.warning(request, f"Response saved but email notification failed: {str(e)}")
                
            messages.success(request, "Your response has been saved and notification sent to the user.")
            return redirect('clientportal:admin_dashboard')
    else:
        form = ServiceNoteResponseForm(instance=note)
    
    return render(request, 'clientportal/respond_to_note.html', {
        'form': form,
        'note': note
    })

@login_required
def create_service_request(request):
    """
    Allows users to submit a new service request.
    """
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            
            messages.success(request, "Your service request has been submitted successfully.")
            # Notify admins about the new request (implemented in a separate utility)
            return redirect('clientportal:my_service_requests')
    else:
        form = ServiceRequestForm()
    
    return render(request, 'clientportal/create_service_request.html', {
        'form': form
    })

@login_required
def my_service_requests(request):
    """
    Allows users to view all their service requests.
    """
    service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'clientportal/my_service_requests.html', {
        'service_requests': service_requests
    })

@login_required
def service_request_detail(request, request_id):
    """
    Shows details of a specific service request to the user.
    """
    service_request = get_object_or_404(ServiceRequest, id=request_id, user=request.user)
    return render(request, 'clientportal/service_request_detail.html', {
        'service_request': service_request
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def process_service_request(request, request_id):
    """
    Allows admins to process (approve/deny/modify) a service request.
    """
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    if request.method == 'POST':
        form = ProcessRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            should_create_service = form.cleaned_data.get('create_service', False)
            service_request = form.save(commit=False)
            service_request.processed_by = request.user
            service_request.processed_at = timezone.now()
            service_request.save()
            
            # If approved and create_service is checked, create a new work order
            if service_request.status == 'approved' and should_create_service:
                work_order = WorkOrder.objects.create(
                    user=service_request.user,
                    name=service_request.title,
                    description=service_request.description,
                    date_performed=service_request.requested_date
                )
                service_request.service = work_order
                service_request.save()

                # Notify the user that their work order has been created
                try:
                    send_service_notification(work_order)
                except Exception as e:
                    messages.warning(request, f"Work order created but email notification failed: {str(e)}")
            
            # Send notification about request status update
            try:
                send_request_status_notification(service_request)
            except Exception as e:
                messages.warning(request, f"Request processed but email notification failed: {str(e)}")
            
            messages.success(request, f"Service request has been {service_request.get_status_display().lower()}.")
            return redirect('clientportal:admin_dashboard')
    else:
        form = ProcessRequestForm(instance=service_request)
    
    return render(request, 'clientportal/process_service_request.html', {
        'form': form,
        'service_request': service_request
    })

# Authentication views moved from authentication app
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('clientportal:dashboard') 
        else:
            messages.info(request, 'Username OR Password is incorrect')
            
    return render(request, 'clientportal/registration/login.html')

def logout_user(request):
    logout(request)
    return redirect('clientportal:login')

def register_user(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account was created for ' + username)
            
            return redirect('clientportal:login')
    
    context = {'form': form}
    return render(request, 'clientportal/registration/register.html', context)

@login_required
@require_POST
def approve_service_cost(request, service_id):
    work_order = get_object_or_404(WorkOrder, id=service_id, user=request.user)
    if work_order.cost_estimate and not work_order.user_approved:
        work_order.user_approved = True
        work_order.save()
        messages.success(request, "You have approved the cost estimate for this work item.")
    else:
        messages.info(request, "This work item is already approved or has no estimate.")
    return redirect('clientportal:dashboard')
