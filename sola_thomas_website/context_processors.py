from django.conf import settings

def analytics(request):
    """
    Adds Google Analytics tracking ID to the template context
    """
    return {
        'GA_TRACKING_ID': getattr(settings, 'GA_TRACKING_ID', ''),
    }
