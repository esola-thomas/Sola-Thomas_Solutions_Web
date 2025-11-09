# Static Site Configuration & GitHub Pages Setup

This document explains the changes made to convert this Django application into a static site for GitHub Pages deployment, and how to revert if needed.

## Table of Contents
1. [What Changed](#what-changed)
2. [Security Improvements](#security-improvements)
3. [GitHub Secrets Setup](#github-secrets-setup)
4. [GitHub Pages Configuration](#github-pages-configuration)
5. [How to Revert to Dynamic Site](#how-to-revert-to-dynamic-site)
6. [Local Development](#local-development)

---

## What Changed

### 1. **Disabled Dynamic Features**
The following features have been disabled for static site deployment:

- **Authentication System**: Login/logout functionality
- **Client Portal**: All `/portal/*` routes including:
  - User dashboard
  - Work orders
  - Invoices
  - Service requests
  - Admin dashboard
- **Admin Panel**: Django admin interface at `/admin/`
- **Contact Form**: Server-side form processing (replaced with direct email/phone links)
- **Database Operations**: All CRUD operations

### 2. **Security Updates**
All exposed API keys and secrets have been moved to environment variables:

- Django SECRET_KEY
- SendGrid API Key
- Supabase Database Credentials

### 3. **New Files Created**
- `.env.example` - Template for environment variables
- `.github/workflows/deploy-static-site.yml` - GitHub Pages deployment workflow
- `STATIC_SITE_SETUP.md` - This documentation

### 4. **Modified Files**

#### `sola_thomas_website/sola_thomas_website/settings.py`
- Replaced hardcoded secrets with environment variables
- Commented out authentication-related apps and middleware
- Clear markers added for easy reverting

#### `sola_thomas_website/sola_thomas_website/urls.py`
- Disabled `/admin/` and `/portal/` routes
- Added clear markers for reverting

#### `sola_thomas_website/core/views.py`
- Disabled contact form server-side processing
- Disabled dashboard view
- Original code preserved in comments

#### `.github/workflows/build-docker.yml`
- Renamed to `build-docker.yml.disabled`
- Can be re-enabled by removing `.disabled` extension

---

## Security Improvements

### Previously Exposed Secrets (NOW SECURED)

**IMPORTANT**: The following secrets were previously hardcoded and are now protected:

1. **Django Secret Key** (settings.py:60)
   - Old: Hardcoded in settings
   - New: `DJANGO_SECRET_KEY` environment variable

2. **SendGrid API Key** (settings.py:201)
   - Old: `'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'`
   - New: `SENDGRID_API_KEY` environment variable
   - **ACTION REQUIRED**: This key should be rotated immediately

3. **Supabase Database Credentials** (settings.py:139-142)
   - Old: Hardcoded username, password, host
   - New: Environment variables (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, etc.)
   - **ACTION REQUIRED**: These credentials should be rotated immediately

### Recommended Actions

⚠️ **CRITICAL**: Since these secrets were previously committed to Git:

1. **Rotate SendGrid API Key**
   - Go to SendGrid dashboard
   - Create new API key
   - Delete old key: `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`
   - Update GitHub Secret with new key

2. **Rotate Supabase Database Password**
   - Go to Supabase dashboard
   - Reset database password
   - Update GitHub Secret with new password

3. **Generate New Django Secret Key**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```
   - Update GitHub Secret with new key

---

## GitHub Secrets Setup

### Required Secrets for Dynamic Site (if reverting)

If you plan to re-enable the dynamic features, add these secrets to your GitHub repository:

**Location**: Repository → Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DJANGO_SECRET_KEY` | Django secret key for cryptographic signing | Generate with Django command above |
| `SENDGRID_API_KEY` | SendGrid API key for email functionality | `SG.xxxxx...` (create new key) |
| `DB_NAME` | Database name | `postgres` |
| `DB_USER` | Database username | `postgres.xxxxx` (from Supabase) |
| `DB_PASSWORD` | Database password | Your new rotated password |
| `DB_HOST` | Database host | `aws-0-us-west-1.pooler.supabase.com` |
| `DB_PORT` | Database port | `5432` |

### For Static Site Only

The static site GitHub Pages deployment only needs:
- `DJANGO_SECRET_KEY` (optional, will use default if not provided)

All other secrets are not needed since dynamic features are disabled.

---

## GitHub Pages Configuration

### Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
4. The workflow will automatically deploy on push to `main` branch

### Custom Domain (Optional)

1. In Pages settings, add your custom domain: `solathomas.com`
2. Configure DNS records:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
          185.199.109.153
          185.199.110.153
          185.199.111.153

   Type: CNAME
   Name: www
   Value: esola-thomas.github.io
   ```
3. Enable "Enforce HTTPS" in GitHub Pages settings

### Verify Deployment

After pushing to main branch:
1. Go to **Actions** tab in GitHub
2. Watch the "Deploy Static Site to GitHub Pages" workflow
3. Once complete, visit: `https://esola-thomas.github.io/Sola-Thomas_Solutions_Web/`
4. Or your custom domain if configured

---

## How to Revert to Dynamic Site

If you need to restore full dynamic functionality:

### Step 1: Uncomment Code

#### In `sola_thomas_website/sola_thomas_website/settings.py`:

1. Uncomment INSTALLED_APPS (lines 80-84, 88):
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',  # Remove # DISABLED FOR STATIC SITE
       'django.contrib.auth',  # Remove # DISABLED FOR STATIC SITE
       # ... etc
   ```

2. Uncomment MIDDLEWARE (lines 101, 103-105):
   ```python
   MIDDLEWARE = [
       'django.contrib.sessions.middleware.SessionMiddleware',  # Remove # DISABLED
       # ... etc
   ```

3. Uncomment AUTHENTICATION_BACKENDS (lines 226-234):
   ```python
   AUTHENTICATION_BACKENDS = [
       'clientportal.backend_authenticate.EmailOrUsernameModelBackend',
       'django.contrib.auth.backends.ModelBackend',
   ]
   # ... etc
   ```

#### In `sola_thomas_website/sola_thomas_website/urls.py`:

Uncomment lines 31-32:
```python
path('admin/', admin.site.urls),
path('portal/', include('clientportal.urls')),
```

#### In `sola_thomas_website/core/views.py`:

1. Replace the `contact()` function (lines 24-92) with the commented original code
2. Uncomment the `dashboard()` function (lines 98-103)

### Step 2: Update Environment Variables

Create a `.env` file in the project root (use `.env.example` as template):
```bash
cp .env.example .env
```

Fill in the values with your **NEW ROTATED** secrets.

### Step 3: Switch Workflows

```bash
# Disable static site workflow
mv .github/workflows/deploy-static-site.yml .github/workflows/deploy-static-site.yml.disabled

# Re-enable Docker workflow
mv .github/workflows/build-docker.yml.disabled .github/workflows/build-docker.yml
```

### Step 4: Add GitHub Secrets

Add all required secrets listed in [GitHub Secrets Setup](#github-secrets-setup).

### Step 5: Deploy

Push changes to trigger Docker build and deployment to your server.

---

## Local Development

### For Static Site Development

```bash
cd sola_thomas_website
python manage.py collectstatic
python manage.py runserver
```

Visit public pages:
- http://localhost:8000/ (Home)
- http://localhost:8000/about/
- http://localhost:8000/contact/
- http://localhost:8000/services/home-services/
- http://localhost:8000/services/business-services/

### For Dynamic Site Development (After Reverting)

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file with your secrets

4. Run migrations:
   ```bash
   cd sola_thomas_website
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

7. Access:
   - Public site: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Portal: http://localhost:8000/portal/

---

## Support

For questions or issues:
- Email: info@solathomas.com
- Phone: (802) 793-5422

## Summary of Changes

✅ All API keys secured with environment variables
✅ Client portal disabled (easily revertable)
✅ Contact form replaced with static alternative
✅ GitHub Pages deployment workflow created
✅ Documentation provided for reverting changes
✅ Security best practices implemented

**Status**: Ready for static site deployment to GitHub Pages
