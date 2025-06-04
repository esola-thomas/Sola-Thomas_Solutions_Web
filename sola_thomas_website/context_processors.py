from django.conf import settings

def analytics(request):
    """
    Adds Google Analytics tracking ID to the template context
    """
    return {
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
    }
