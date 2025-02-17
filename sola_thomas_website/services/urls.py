from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('home-services/', views.home_services, name='home_services'),
    path('business-services/', views.business_services, name='business_services'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
]
