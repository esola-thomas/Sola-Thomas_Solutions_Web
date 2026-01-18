# Sola-Thomas Solutions - Static Website

This is the simplified static website for Sola-Thomas Solutions, migrated from the Django-based system to pure HTML/CSS/JavaScript.

## Structure

```
static_site/
├── index.html              # Homepage
├── gilbarco.html           # Gilbarco bdroot services page
├── home-services.html      # Home services
├── business-services.html  # Business services
├── service-request.html    # Service request form
├── contact.html            # Contact page
├── css/
│   ├── theme.css          # Main theme styles (dark/light mode)
│   ├── animations.css     # Animation effects
│   ├── home.css           # Homepage specific styles
│   ├── service-request.css # Service request page styles
│   └── pages/             # Other page-specific styles
├── js/
│   ├── theme.js           # Theme toggle functionality
│   └── animations.js      # Scroll animations
├── images/                # Images and photos
└── svg/                   # SVG icons (sun/moon for theme toggle)
```

## Features

- **Responsive Design**: Bootstrap 5.3 for mobile-friendly layouts
- **Dark/Light Theme**: Toggle between themes with persistent localStorage
- **Service Request Form**: Integrated form (configured for Formspree)
- **Phone Number Prominent**: (802) 793-2871 displayed in header, footer, and CTAs
- **Gilbarco bdroot Tab**: Dedicated page for Gilbarco equipment services
- **Clean Navigation**: Simple, intuitive menu structure
- **SEO Optimized**: Meta tags, structured data, Google Analytics
- **Nationwide Service**: Business serving clients across the United States

## Phone Number

The primary contact number **(802) 793-2871** is prominently featured:
- Navigation bar (clickable tel: link)
- Footer
- Service request page
- Emergency notices
- Call-to-action buttons

## Form Submission Setup

The service request form is configured to use **Formspree**. To set up:

1. Create a free account at [formspree.io](https://formspree.io)
2. Create a new form and get your form ID
3. Update `service-request.html` line 82:
   ```html
   <form id="serviceRequestForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```
4. Replace `YOUR_FORM_ID` with your actual Formspree form ID

### Alternative: Netlify Forms

If deploying to Netlify, you can use Netlify Forms instead:

1. Add `data-netlify="true"` to the form tag:
   ```html
   <form id="serviceRequestForm" data-netlify="true" method="POST">
   ```
2. Netlify will automatically handle form submissions

## Deployment Options

### Option 1: Netlify (Recommended)

1. Create account at [netlify.com](https://netlify.com)
2. Connect your GitHub repository or drag/drop the `static_site` folder
3. Site will be live instantly with automatic SSL
4. Configure custom domain if needed
5. Forms will work automatically with Netlify Forms

### Option 2: GitHub Pages

1. Push `static_site` folder to a GitHub repository
2. Go to Settings > Pages
3. Select branch and `/static_site` folder
4. Site will be live at `https://username.github.io/repo-name/`

### Option 3: Vercel

1. Create account at [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `static_site`
4. Deploy with one click

### Option 4: Traditional Hosting

Upload all files from `static_site/` to your web server via FTP/SFTP.

## Local Testing

To test locally, you can use any simple HTTP server:

### Python
```bash
cd static_site
python3 -m http.server 8000
```
Then visit: http://localhost:8000

### Node.js (using npx)
```bash
cd static_site
npx http-server
```

### VS Code Live Server
Install the "Live Server" extension and right-click on `index.html` → "Open with Live Server"

## Google Analytics

The site is configured with Google Analytics tracking ID: **G-24QFBN3WGN**

To change or remove:
1. Edit the tracking ID in all HTML files (search for `G-24QFBN3WGN`)
2. Or remove the entire Google Analytics script block

## Theme Customization

Theme colors are defined in `css/theme.css`. Key CSS variables:

```css
:root {
  --primary-color: #0d6efd;
  --secondary-color: #6c757d;
  --text-color: #212529;
  --bg-color: #ffffff;
}

[data-theme="dark"] {
  --text-color: #f8f9fa;
  --bg-color: #212529;
}
```

## Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## TODO

- [x] Homepage with service request CTA
- [x] Service request form page
- [x] Gilbarco bdroot page
- [x] Home services page
- [x] Business services page
- [x] Contact page
- [x] Remove About page (business is national, not location-specific)
- [x] Update all references to be nationwide (removed Melbourne FL)
- [x] Configure GitHub Actions deployment
- [ ] Configure actual form submission endpoint (Formspree)
- [ ] Test on all devices
- [ ] Deploy to production

## Contact

For questions about this website:
- **Phone**: (802) 793-2871
- **Email**: info@solathomas.com

---

© 2026 Sola-Thomas LLC. All rights reserved.
