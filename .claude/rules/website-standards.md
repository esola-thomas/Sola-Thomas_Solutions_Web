# Website Standards: Authenticity, Credibility, UX

Applies to every change under `static_site/` and to any copy, image, or metadata for solathomas.com.
The goal is a site that is demonstrably authentic, accurate, usable, and professionally built,
not one that merely looks less AI-generated.

## 1. Facts and claims

Publish only facts on this list. Anything else needs owner evidence first (Dave approves), then
gets added here with its source before it ships.

### Approved facts (source: owner roadmap, Oct 24, 2026)
- Company: Sola-Thomas LLC. Gilbarco Veeder-Root Authorized Service Contractor (ASC), confirmed by owner.
- Slogan, exact: "Fueling Reliability. Delivering Performance."
- Experience copy, exact: "Over 25 Years of Hands-On Experience" / "Bringing more than 25 years of
  hands-on experience servicing Gilbarco Veeder-Root equipment, Sola-Thomas delivers knowledgeable,
  professional service for commercial fueling systems." The 25+ years belongs to the lead
  technician, never to the company's age.
- Services: dispenser diagnostics and repairs, preventative maintenance, installations and upgrades,
  emergency repairs, Passport POS, Veeder-Root tank monitoring, supported equipment.
- 24/7 emergency availability. Coverage: New England and Central Florida only.
- Phone (802) 793-2871 (service and emergencies). Email service@solathomas.com (monitored, confirmed by Ernesto, Nov 2, 2026).
- Gilbarco certified; use of the Gilbarco Veeder-Root logo is permitted (confirmed by Ernesto, Nov 2, 2026).
  Wording containing "certified" still needs the exact phrase added to `APPROVED_CLAIM_PHRASES` in
  `scripts/check_site.py` before it ships.

### Never publish
- A mailing address, or info@solathomas.com.
- Residential/home services, business IT services, "nationwide" coverage.
- Invented testimonials, customer names or logos, certifications, licenses, insurance, awards,
  metrics, response-time promises, partnerships, team bios, or screenshots presented as real.
- Promises the system does not yet keep (e.g. "you will receive a confirmation email" before the
  autoresponder is live). Describe what actually happens.

### Claim handling
Classify every claim as Verified / Plausible-unverified / Unsupported. Keep verified, qualify or
remove unverified, remove unsupported. When information is missing, leave a gap and record it in
`docs/website-credibility-audit.md` under owner decisions. Never fill it with plausible fiction.

## 2. Copy

- Say who it serves, what problem it solves, how it works, and what the customer can expect.
- Concrete nouns (dispenser, Passport, tank monitor, fueling position), short sentences.
- Banned: "revolutionize", "cutting-edge", "seamless", "unlock", "empower", "next-generation",
  "world-class", "industry-leading", unsupported superlatives, filler paragraphs.
- Approved copy above is used verbatim; do not paraphrase it.

## 3. Imagery

- Priority: real job-site photos of our technicians and equipment > original diagrams > relevant
  illustration. No generic stock.
- The two current technician images were supplied by the owner and appear AI-generated; replace
  them with real photos when available. Never add more AI or stock images that depict "our team"
  or "our work" without the owner explicitly approving and the audit recording it.
- Gilbarco Veeder-Root marks only as permitted by ASC brand guidelines; keep the trademark notice.
- Every `<img>` has `alt`, `width`, `height`; below-the-fold images `loading="lazy"`; serve WebP at
  800w/1600w with `srcset`/`sizes`.

## 4. Design system

- Reuse tokens in `static_site/css/site.css` (`:root`). Navy/red/white. Barlow for headings,
  system sans for body. No new colors, fonts, or frameworks without a recorded reason.
- Prefer shared CSS over page-specific patches. Header/footer markup is duplicated across pages:
  change all pages together.
- Avoid template tells: identical card grids everywhere, decorative gradients/blobs/glass,
  icons with no information value, animation for its own sake. Vary composition only with purpose.

## 5. Accessibility and UX (WCAG 2.2 AA as the target, not a claim)

- Text contrast ≥ 4.5:1 (≥ 3:1 for large text and UI boundaries). Visible focus on everything.
- Keyboard: skip link, mobile menu operable by Tab/Enter/Escape with correct `aria-expanded`.
- Forms: labels, errors tied with `aria-describedby`, status and confirmation announced via live
  region, touch targets ≥ 44px where feasible.
- Respect `prefers-reduced-motion`. No horizontal scroll at 320px+.
- Emergency path always visible: call (802) 793-2871. The form never replaces the phone for emergencies.

## 6. Technical

- Targets: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (mobile). Label numbers as measured or estimated.
- Do not change form field names: `docs/service-request-contract.md` is an API contract with the
  service-management app. Keep GA4 events and `data-cta` attributes.
- No new runtime dependencies. External assets only from Google Fonts and Google Analytics.
- Every page: `lang`, `<title>`, meta description, canonical (except 404), one `<h1>`, OG tags.

## 7. Verification before any commit touching the site

1. `python3 scripts/check_site.py` passes (also runs as a Claude hook and in the deploy workflow).
2. Playwright render at 390, 768, 1366 widths: no overflow, no console errors, no failed requests.
3. Form behaviour with `https://formspree.io/**` mocked: required fields, emergency flag,
   upload-failure retry, total-failure fallback, success confirmation.
4. axe-core scan on all pages; report violations honestly. Passing axe is not WCAG compliance.
5. Report what ran, what passed, what failed, and what was not checked. No success without evidence.

## 8. Release

`main` auto-deploys to solathomas.com. Work on a branch, open a PR, and merge only after Dave
approves. Update `docs/website-credibility-audit.md` when a change resolves or adds a finding.
