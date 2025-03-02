#!/usr/bin/env python3
"""
Test Django template rendering of static tags.
"""
import os
import sys
import django
from django.template import Template, Context

# Add Django project to path
sys.path.append('/home/esolathomas/ws/sola_thomas_website')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sola_thomas_website.settings')
os.environ['DEPLOYMENT'] = 'True'

# Initialize Django
django.setup()

# Test template rendering
template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Template</title>
</head>
<body>
    <div style="background-image: url({% static 'images/hero_blue_waves_background.jpg' %});">
        This has a background image
    </div>
    <img src="{% static 'images/contact-us-icon.png' %}" alt="Contact">
</body>
</html>
"""

def test_template():
    from django.template import engines
    from django.conf import settings
    
    django_engine = engines['django']
    template = django_engine.from_string(template_str)
    context = {'STATIC_URL': settings.STATIC_URL}
    rendered = template.render(context)
    
    print("Template rendered as:")
    print("--------------------")
    print(rendered)
    print("--------------------")
    
    if '/static/images/' in rendered:
        print("✓ Static URLs correctly rendered")
    else:
        print("✗ Problem with static URL rendering")

if __name__ == "__main__":
    try:
        test_template()
    except Exception as e:
        print(f"Error testing template: {str(e)}")
