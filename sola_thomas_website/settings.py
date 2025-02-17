# Google Analytics Settings
GA_TRACKING_ID = 'G-XXXXXXXXXX'  # Replace with your actual tracking ID

# Add GA_TRACKING_ID to the template context
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sola_thomas_website.context_processors.analytics',  # Add this line
            ],
        },
    },
]
