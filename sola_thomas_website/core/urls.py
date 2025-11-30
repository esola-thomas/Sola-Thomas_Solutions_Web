from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # ============================================================================
    # STATIC SITE MODE: Dashboard disabled (requires authentication)
    # To re-enable: Uncomment the line below
    # ============================================================================
    # path('dashboard/', views.dashboard, name='dashboard'),  # DISABLED FOR STATIC SITE
]
