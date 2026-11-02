# Sola-Thomas Website

Public site for Sola-Thomas LLC, a Gilbarco Veeder-Root Authorized Service Contractor serving
New England and Central Florida. Plain static HTML/CSS/JS in `static_site/`, deployed to GitHub
Pages on every push to `main` (live at solathomas.com).

@.claude/rules/website-standards.md

## Layout
- `static_site/`: the live site. `index.html`, `service-request.html`, `404.html` (also redirects
  retired URLs), `css/site.css` (design tokens), `js/config.js` (form endpoint, Team Login URL),
  `js/site.js` (nav, attribution, call tracking), `js/service-request.js` (form).
- `docs/service-request-contract.md`: form payload contract with the service-management app.
- `docs/website-credibility-audit.md`: findings, owner decisions, verification history.
- `scripts/check_site.py`: automated standards check. Run it before committing site changes.
- `sola_thomas_website/`: legacy Django project, not deployed. Its `clientportal` app is the
  candidate base for the private service app (GitHub issue #23); do not edit it for site work.

## Commands
- Preview: `cd static_site && python3 -m http.server 8000`
- Check: `python3 scripts/check_site.py`
- Browser tests: Playwright is preinstalled; run node with `NODE_PATH=$(npm root -g)`.

## Open work
- #24 go-live checklist (official logo, Formspree notifications/SMS/autoresponse, Dave approval).
- #23 service app + QuickBooks Online (separate workstream).
