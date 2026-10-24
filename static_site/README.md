# solathomas.com (static site)

Public website for Sola-Thomas, a Gilbarco Veeder-Root Authorized Service Contractor
serving New England and Central Florida. Deployed to GitHub Pages from this folder on
every push to `main` (`.github/workflows/deploy-static-site.yml`).

## Pages

| Path | Purpose |
|---|---|
| `index.html` | Homepage: services, qualifications, coverage, 24/7 emergency, contact |
| `service-request.html` | Customer service request form |
| `404.html` | Not-found page. Also redirects retired URLs (old IT-services pages and Django routes) to current pages. |
| `robots.txt`, `sitemap.xml` | Search engine files. Update `sitemap.xml` when pages are added. |

## Configuration

`js/config.js`:

- `formEndpoint`: where service requests are POSTed (Formspree today, app intake API later).
  Field names are a contract: `../docs/service-request-contract.md`.
- `teamLoginUrl`: set to the private app's login URL to show the **Team Login** footer link.

## Brand assets

- `images/logo-mark.svg` and `favicon.svg`: interim mark. Replace with the official
  Sola-Thomas logo (navy with red fuel nozzle) when the source file is available, and
  re-render `images/og-image.png` (1200x630).
- `images/Gilbarco_Veeder-Root.png`: use subject to Gilbarco brand guidelines.

Colors and type live in `css/site.css` (`:root` tokens). No frameworks; the only external
assets are Google Fonts (Barlow) and Google Analytics (`G-24QFBN3WGN`).

## Analytics events

`click_to_call` (with `link_location`), `click_email`, `form_start`, `emergency_checked`,
`generate_lead` (mark as a key event in GA4), `form_error`.

## Local testing

```bash
cd static_site && python3 -m http.server 8000
```

`404.html` redirects only work on GitHub Pages (the local server does not serve it for missing paths).
