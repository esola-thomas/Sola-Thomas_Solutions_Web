from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

app_name = 'clientportal'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('submit_review/<int:service_id>/', views.submit_review, name='submit_review'),
    path('activate/', views.activate_account, name='activate_account'),
    path('edit_invoice/<int:invoice_id>/', views.edit_invoice, name='edit_invoice'),
    path('create_service/', views.create_service, name='create_service'),
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('resend_activation/<int:user_id>/', views.resend_activation_email, name='resend_activation'),
    # New note-related URLs
    path('service/<int:service_id>/add_note/', views.add_service_note, name='add_service_note'),
    path('service/<int:service_id>/notes/', views.view_service_notes, name='view_service_notes'),
    path('note/<int:note_id>/respond/', views.respond_to_note, name='respond_to_note'),
    
    # Service request URLs
    path('request/create/', views.create_service_request, name='create_service_request'),
    path('requests/', views.my_service_requests, name='my_service_requests'),
    path('request/<int:request_id>/', views.service_request_detail, name='service_request_detail'),
    path('request/<int:request_id>/process/', views.process_service_request, name='process_service_request'),
]

# Auth URLs moved from authentication app
urlpatterns += [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Password reset URLs - updated with explicit domain configuration
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='clientportal/registration/password_reset_form.html',
             email_template_name='clientportal/registration/password_reset_email.html',
             subject_template_name='clientportal/registration/password_reset_subject.txt',
             success_url=reverse_lazy('clientportal:password_reset_done'),
             extra_email_context={'domain': settings.SITE_DOMAIN or 'solathomas.com', 'protocol': 'https'}
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='clientportal/registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='clientportal/registration/password_reset_confirm.html',
             success_url='/reset/done/'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='clientportal/registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
