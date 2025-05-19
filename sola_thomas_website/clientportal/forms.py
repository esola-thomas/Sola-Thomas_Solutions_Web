from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.models import User
from .models import Review, Invoice, Service, ServiceNote, ServiceRequest

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['user', 'amount', 'details', 'due_date', 'payment_link', 'paid']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://paymentprovider.com/payment/id'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomUserForm(forms.ModelForm):
    """Form for creating new users with activation email."""
    is_staff = forms.BooleanField(
        required=False, 
        label="Admin access",
        help_text="Designates whether the user can access the admin area."
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['user', 'name', 'description', 'date_performed', 'admin_notes', 'invoice', 'cost_estimate', 'user_approved']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_performed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'invoice': forms.Select(attrs={'class': 'form-control'}),
            'cost_estimate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'user_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ServiceNoteForm(forms.ModelForm):
    class Meta:
        model = ServiceNote
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your message to the admin...'}),
        }

class ServiceNoteResponseForm(forms.ModelForm):
    class Meta:
        model = ServiceNote
        fields = ['admin_response', 'is_resolved']
        widgets = {
            'admin_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_resolved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'requested_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requested_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ProcessRequestForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('pending', 'Keep as Pending'),
        ('approved', 'Approve'),
        ('denied', 'Deny'),
        ('completed', 'Mark as Completed')
    )
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    create_service = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = ServiceRequest
        fields = ['status', 'admin_notes', 'create_service']
        widgets = {
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# Authentication form moved from authentication app
class CreateUserForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
