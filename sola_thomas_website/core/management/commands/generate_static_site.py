"""
Django management command to generate static HTML files for GitHub Pages deployment.

This command renders Django templates to static HTML files with proper paths for
GitHub Pages, which serves the site from a subdirectory.
"""

import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate static HTML files for GitHub Pages deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='staticsite',
            help='Output directory for generated static site (default: staticsite)'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='/Sola-Thomas_Solutions_Web',
            help='Base URL path for GitHub Pages (default: /Sola-Thomas_Solutions_Web)'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        base_url = options['base_url'].rstrip('/')

        # Create output directory
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        # Define pages to generate
        pages = [
            {'template': 'core/home.html', 'output': 'index.html', 'title': 'Home'},
            {'template': 'core/about.html', 'output': 'about/index.html', 'title': 'About'},
            {'template': 'core/contact.html', 'output': 'contact/index.html', 'title': 'Contact'},
            {'template': 'services/home_services.html', 'output': 'services/home-services/index.html', 'title': 'Home Services'},
            {'template': 'services/business_services.html', 'output': 'services/business-services/index.html', 'title': 'Business Services'},
        ]

        # Context for templates
        context = {
            'GA_TRACKING_ID': getattr(settings, 'GA_TRACKING_ID', ''),
            'base_url': base_url,
            'static_url': f'{base_url}/static',
            'current_year': datetime.now().year,
        }

        # Generate each page
        for page in pages:
            self.generate_page(
                output_dir,
                page['template'],
                page['output'],
                context,
                base_url
            )
            self.stdout.write(
                self.style.SUCCESS(f"Generated {page['output']}")
            )

        # Copy static files
        static_src = os.path.join(settings.BASE_DIR, 'static')
        static_dest = os.path.join(output_dir, 'static')
        if os.path.exists(static_src):
            shutil.copytree(static_src, static_dest)
            self.stdout.write(
                self.style.SUCCESS(f"Copied static files to {static_dest}")
            )

        # Create .nojekyll file to prevent Jekyll processing
        nojekyll_path = os.path.join(output_dir, '.nojekyll')
        with open(nojekyll_path, 'w') as f:
            pass
        self.stdout.write(
            self.style.SUCCESS("Created .nojekyll file")
        )

        self.stdout.write(
            self.style.SUCCESS(f"\nStatic site generated in '{output_dir}' directory")
        )

    def generate_page(self, output_dir, template_name, output_path, context, base_url):
        """Generate a single static HTML page."""
        # Create output directory if needed
        output_file = os.path.join(output_dir, output_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Read the template file directly and process it
        template_dirs = [
            os.path.join(settings.BASE_DIR, 'templates'),
        ]

        # Add app template directories
        for app in ['core', 'services']:
            app_template_dir = os.path.join(settings.BASE_DIR, app, 'templates')
            if os.path.exists(app_template_dir):
                template_dirs.append(app_template_dir)

        # Find and read the template
        template_content = None
        for template_dir in template_dirs:
            template_path = os.path.join(template_dir, template_name)
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    template_content = f.read()
                break

        if template_content is None:
            raise FileNotFoundError(f"Template {template_name} not found")

        # Read base template
        base_template_path = os.path.join(settings.BASE_DIR, 'templates', 'base.html')
        with open(base_template_path, 'r') as f:
            base_content = f.read()

        # Process templates to static HTML
        html_content = self.process_template(
            template_content,
            base_content,
            context,
            base_url,
            template_name
        )

        # Write output file
        with open(output_file, 'w') as f:
            f.write(html_content)

    def process_template(self, child_content, base_content, context, base_url, template_name):
        """Process Django templates to static HTML."""
        static_url = f'{base_url}/static'

        # Extract blocks from child template
        blocks = self.extract_blocks(child_content)

        # Start with base template
        html = base_content

        # Replace block content
        for block_name, block_content in blocks.items():
            # Replace {% block name %}...{% endblock %} with content
            import re
            pattern = r'\{%\s*block\s+' + block_name + r'\s*%\}.*?\{%\s*endblock\s*%\}'
            html = re.sub(pattern, block_content, html, flags=re.DOTALL)

        # Process template tags
        html = self.process_static_tags(html, static_url)
        html = self.process_url_tags(html, base_url)
        html = self.process_hardcoded_home_links(html, base_url)
        html = self.process_now_tag(html, context.get('current_year', datetime.now().year))
        html = self.process_if_authenticated(html)
        html = self.process_ga_tracking_id(html, context.get('GA_TRACKING_ID', ''))
        html = self.remove_template_artifacts(html)

        return html

    def extract_blocks(self, content):
        """Extract block content from a Django template."""
        import re
        blocks = {}

        # Pattern to match {% block name %}...{% endblock %}
        pattern = r'\{%\s*block\s+(\w+)\s*%\}(.*?)\{%\s*endblock\s*%\}'
        matches = re.findall(pattern, content, re.DOTALL)

        for name, block_content in matches:
            blocks[name] = block_content.strip()

        return blocks

    def process_static_tags(self, html, static_url):
        """Replace {% static 'path' %} tags with actual URLs."""
        import re
        pattern = r'\{%\s*static\s+[\'"]([^\'"]+)[\'"]\s*%\}'
        return re.sub(pattern, f'{static_url}/\\1', html)

    def process_url_tags(self, html, base_url):
        """Replace {% url 'name' %} tags with actual URLs."""
        import re

        # URL mappings
        url_map = {
            'core:home': '',
            'core:about': '/about/',
            'core:contact': '/contact/',
            'core:dashboard': '/dashboard/',
            'services:home_services': '/services/home-services/',
            'services:business_services': '/services/business-services/',
            'clientportal:dashboard': '/portal/dashboard/',
            'clientportal:login': '/portal/login/',
            'clientportal:logout': '/portal/logout/',
            'clientportal:password_reset': '/portal/password_reset/',
        }

        for url_name, path in url_map.items():
            escaped_name = re.escape(url_name)
            pattern = r'\{%\s*url\s+[\'"]' + escaped_name + r'[\'"]\s*%\}'
            replacement = f'{base_url}{path}' if path else f'{base_url}/'
            html = re.sub(pattern, replacement, html)

        # Handle any remaining url tags with a fallback
        remaining_pattern = r'\{%\s*url\s+[\'"]([^\'"]+)[\'\"]\s*%\}'
        html = re.sub(remaining_pattern, f'{base_url}/', html)

        return html

    def process_hardcoded_home_links(self, html, base_url):
        """Replace hardcoded home links with base_url-prefixed versions."""
        import re
        # Replace href="/" with href="/base_url/" but not href="/something"
        # Only replace exact root links
        html = re.sub(r'href="/"', f'href="{base_url}/"', html)
        return html

    def process_now_tag(self, html, year):
        """Replace {% now "Y" %} tags with the current year."""
        import re
        pattern = r'\{%\s*now\s+[\'"]Y[\'"]\s*%\}'
        return re.sub(pattern, str(year), html)

    def process_if_authenticated(self, html):
        """Process {% if user.is_authenticated %} blocks - show unauthenticated version."""
        import re

        # Remove authenticated content, keep unauthenticated content
        pattern = r'\{%\s*if\s+user\.is_authenticated\s*%\}.*?\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}'
        html = re.sub(pattern, r'\1', html, flags=re.DOTALL)

        # Remove any remaining authenticated-only blocks (without else)
        pattern = r'\{%\s*if\s+user\.is_authenticated\s*%\}.*?\{%\s*endif\s*%\}'
        html = re.sub(pattern, '', html, flags=re.DOTALL)

        return html

    def process_ga_tracking_id(self, html, tracking_id):
        """Replace {{ GA_TRACKING_ID }} with actual value."""
        return html.replace('{{ GA_TRACKING_ID }}', tracking_id)

    def remove_template_artifacts(self, html):
        """Remove remaining Django template artifacts."""
        import re

        # Remove {% load static %} and other load tags
        html = re.sub(r'\{%\s*load\s+\w+\s*%\}', '', html)

        # Remove {% extends %} tags
        html = re.sub(r'\{%\s*extends\s+[^\}]+%\}', '', html)

        # Remove template comments
        html = re.sub(r'\{#.*?#\}', '', html, flags=re.DOTALL)

        # Remove csrf_token tags
        html = re.sub(r'\{%\s*csrf_token\s*%\}', '', html)

        # Remove for loops for form fields (will be empty in static site)
        html = re.sub(r'\{%\s*for\s+\w+\s+in\s+\w+\s*%\}.*?\{%\s*endfor\s*%\}', '', html, flags=re.DOTALL)

        # Remove remaining empty blocks
        html = re.sub(r'\{%\s*block\s+\w+\s*%\}\s*\{%\s*endblock\s*%\}', '', html)

        # Remove blocks with default content (keep the default content)
        html = re.sub(r'\{%\s*block\s+\w+\s*%\}([^{]*)\{%\s*endblock\s*%\}', r'\1', html)

        # Remove any remaining block tags (without matching endblock)
        html = re.sub(r'\{%\s*block\s+\w+\s*%\}', '', html)
        html = re.sub(r'\{%\s*endblock\s*%\}', '', html)

        # Remove variable references that might be left (like {{ request.build_absolute_uri }})
        html = re.sub(r'\{\{\s*request\.[^\}]+\}\}', '', html)
        html = re.sub(r'\{\{\s*\w+\.?\w*\s*\}\}', '', html)

        # Clean up extra whitespace and empty lines
        html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)

        return html
