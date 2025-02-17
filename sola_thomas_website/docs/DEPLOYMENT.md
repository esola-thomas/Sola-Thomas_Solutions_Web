# Deployment Checklist

## Pre-deployment
- [ ] Set DEBUG = False in settings.py
- [ ] Update ALLOWED_HOSTS with production domain
- [ ] Configure production database settings
- [ ] Set up proper email backend
- [ ] Configure Stripe live keys

## Security
- [ ] Enable HTTPS
- [ ] Set SESSION_COOKIE_SECURE = True
- [ ] Set CSRF_COOKIE_SECURE = True
- [ ] Review security middleware settings
- [ ] Update SECRET_KEY

## Static Files
- [ ] Run python manage.py collectstatic
- [ ] Configure static files hosting
- [ ] Set up media files storage

## Monitoring
- [ ] Set up error logging
- [ ] Configure performance monitoring
- [ ] Set up backup system
- [ ] Implement health checks

## SEO & Performance
- [ ] Add robots.txt
- [ ] Create sitemap.xml
- [ ] Configure meta tags
- [ ] Optimize static assets
