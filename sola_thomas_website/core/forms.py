from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
from utils import send_contact_notification

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5})
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        # Send notification email using utility function
        send_contact_notification(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            message=self.cleaned_data['message']
        )
        
        return instance
