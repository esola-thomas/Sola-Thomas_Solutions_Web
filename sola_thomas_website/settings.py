# Google Analytics Settings
GOOGLE_ANALYTICS_ID = 'G-24QFBN3WGN'

# Add GOOGLE_ANALYTICS_ID to the template context
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
