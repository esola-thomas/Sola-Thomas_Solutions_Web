# Google Analytics Settings
GA_TRACKING_ID = 'G-24QFBN3WGN'

# Add GA_TRACKING_ID to the template context
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sola_thomas_website.context_processors.analytics',
            ],
        },
    },
]
