# Website Credibility and UX Audit: solathomas.com

Audit date: November 2, 2026. Branch: `gilbarco-site-redesign`. Scope: `static_site/` only.

## Executive Summary

The site was structurally sound (valid HTML, working form, correct metadata) but had credibility, accessibility, and performance gaps. The most serious were: promises the system does not keep yet (immediate team notification, confirmation email), no privacy notice despite collecting personal data, photos, analytics, and attribution; two technician photos that appear AI-generated with alt text naming them as Sola-Thomas staff; form errors that were not announced to assistive technology; a phone validation pattern that Chrome rejects (so any text passed); and render-blocking third-party fonts and scripts.

This pass fixed every P0, P1 (where code can fix it), and P2 finding plus the cheap P3 items. Items that need owner evidence or decisions (photos, logo permission, equipment list, state list, mailbox monitoring, Formspree notifications, About/team/credential content, counsel review of the privacy notice) are documented below and not filled with assumed facts.

## Initial Discovery

- Design language: navy / red / white, Barlow headings, system sans body, slogan "Fueling Reliability. Delivering Performance."
- Audience: station owners and operators, multi-site operators, facility managers, petroleum equipment companies, in New England and Central Florida.
- Key journeys: (1) emergency call, (802) 793-2871, always visible; (2) service request form; (3) research: services, coverage, experience, who is behind the company.
- Constraints: static GitHub Pages (no build, no server), Formspree form endpoint, owner-approved facts only (`.claude/rules/website-standards.md`), form field names and GA4 events are a contract.

## Findings

Status key: Fixed / Documented: owner decision / Deferred with reason. Severity follows priority (P0 Critical, P1 High, P2 Medium, P3 Low). Effort S/M/L. Evidence is from the pre-change site and the audit captures listed under Before/After Screenshots.

| ID | Page/component | Problem | Evidence | Why it matters | Severity | Priority | Recommendation | Expected impact | Effort | Verification | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CR-01 | service-request sidebar | Promised "team notified right away" and an email confirmation; neither is configured (#24) | before-service-request-1366.png | Broken promise | Critical | P0 | State what is true: we review and contact you | Honest expectations | S | Copy review | Fixed |
| CR-02 | Confirmation panel | "A confirmation will be sent to {email}" | js/service-request.js (before) | Broken promise | Critical | P0 | "We will contact you at {email} or by phone"; keep reference; urgent: call | Honest expectations | S | Form test, success path | Fixed |
| CR-03/04, TE-13 | Site-wide | No privacy notice; PII, photos, GA4, and localStorage attribution undisclosed | No privacy page | Trust, transparency | High | P1 | Add privacy.html describing only what the code does; link in footers and under submit | Disclosure | M | check_site, render | Fixed (counsel review pending) |
| CR-05 | Form note | "used only to respond" overstated | service-request.html | Overclaim | High | P1 | Reworded, links to notice | Accuracy | S | Copy review | Fixed |
| CR-06 / UX-16 | Hero and experience photos | Appear AI-generated; alt text asserted staff identity | Images | Authenticity | High | P1 | Keep images, scene-only alt text, no identity captions; replace with real photos | Lower deception risk | S | Alt text check | Fixed (alt); Documented: owner decision (photos) |
| CR-07 | Gilbarco logo | Brand-guideline permission unconfirmed (#24) | Hero card | Trademark risk | High | P1 | Confirm ASC guidelines; trademark line kept | Risk reduction | S | n/a | Documented: owner decision |
| CR-08 | Equipment list, model placeholder | "Fleet management systems", "Legacy Gilbarco equipment", "Encore 700 S" not on approved list | index.html, form | Unapproved specifics | High | P1 | List kept (plausible, from the previous owner-run Gilbarco page); placeholder now "Model from the data plate"; owner to confirm | Accuracy | S | Copy review | Fixed (placeholder); Documented: owner decision (list) |
| CR-09 | Service cards | Outcome promises and superlatives ("reduce costly downtime", "Around-the-clock response", "One qualified team") | index.html | Unsupported claims | Medium | P2 | Concrete scope only | Credibility | S | check_site, review | Fixed |
| CR-10 | Coverage, state select | "Florida" for Central Florida; "Other" state gave no feedback | index.html | Coverage accuracy | Medium | P2 | "Central Florida"; hint under state | Fewer out-of-area requests | S | Render | Fixed (state list: owner decision) |
| CR-11 | JSON-LD | openingHours Mon-Sun 00:00-23:59 implied 24/7 regular service | index.html | Misleading structured data | Medium | P2 | Removed; 24/7 emergency stays in description | Accuracy | S | JSON parse | Fixed |
| CR-12 | JSON-LD logo | Interim SVG | index.html | Brand | Low | P3 | Official logo | Brand | S | n/a | Documented: owner decision |
| CR-13 | Titles, OG | Title led with third-party brand and was 82 chars; no og:image:alt | index.html | SEO, brand | Low | P3 | "Sola-Thomas \| Gilbarco Service, New England & Central Florida"; og:image:alt/size | Cleaner SERP | S | check_site | Fixed |
| CR-14 | Site | No About, company, team, or credential info | n/a | Buyers research who they hire | High | P1 | Owner supplies facts; nothing invented | Trust | M | n/a | Documented: owner decision |
| CR-15 | Footers | No Privacy link | Footers | Discoverability | Medium | P2 | Link added on all pages | Disclosure | S | Render | Fixed |
| CR-16 | Fallback routing | service@ mailbox monitoring unconfirmed; mailto fallback and photo note route there | Form | Lost requests | High | P1 | Confirm monitoring; phone stays primary | Reliability | S | n/a | Resolved: service@ is monitored and aliases office@ (owner, Nov 2, 2026) |
| CR-17 | Confirmation | Contact channel not stated | js | Expectations | Medium | P2 | "by phone or email", no timing | Clarity | S | Form test | Fixed |
| CR-18 | Photo hint | No privacy guidance | Form | Privacy | Low | P3 | "Avoid photos showing people or customer payment information." | Less PII | S | Render | Fixed |
| CR-19 | Emergency band, contact h2 | "We answer 24/7" implied live answer; "Talk to a Technician" | index.html | Overclaim | Medium | P2 | "Call 24/7 for emergency service"; "Contact Sola-Thomas" | Accuracy | S | Copy review | Fixed (after-hours call handling wording: owner decision) |
| CR-20 | 404 | "now focuses exclusively on Gilbarco..." unapproved, exposes past business | 404.html | Unapproved claim | Medium | P2 | Sentence removed | Accuracy | S | check_site | Fixed |
| CR-22 / TE-14 | sitemap | Stale lastmod; privacy page missing | sitemap.xml | SEO hygiene | Low | P3 | lastmod 2026-11-02, privacy added | Freshness | S | Read file | Fixed |
| Repetition | Home | ASC, 24/7, and regions repeated 5+ times | index.html | Reads as filler | Low | P3 | Pills removed, footer 24/7 line removed, 25+ stated once plus approved copy | Cleaner page | S | Screenshots | Fixed |
| UX-01 | Eyebrows, emergency band | Contrast 4.39, 3.90 (axe: 3 serious) | ux-findings.md | WCAG 1.4.3 | High | P1 | red-700 eyebrows, white band text | axe clean | S | axe | Fixed |
| UX-02 | Mobile menu | No Escape, outside click, or focus return | js/site.js | Keyboard users | High | P1 | Added | Operable menu | S | Playwright | Fixed |
| UX-03 | Form errors | Not linked, not announced, `*` unexplained | service-request.html | Screen reader users cannot complete form | Critical | P0 | aria-describedby per error, role=alert summary, required legend | Accessible form | M | Playwright | Fixed |
| UX-04 | Photos field | Hint and error unassociated | Form | AT | Medium | P2 | aria-describedby | AT clarity | S | Playwright | Fixed |
| UX-05 | Confirmation, busy | No role=status | Form | AT | Low | P3 | role=status; live region for submitting | AT clarity | S | Playwright | Fixed |
| UX-06 | Field borders | 1.75:1 | CSS | WCAG 1.4.11 | Medium | P2 | #6b7c92 border; stronger focus | Visible fields | S | Contrast calc | Fixed |
| UX-07 | Tap targets | Under 24px at 390 | before-index-390.png | Touch usability | High | P1 | 44px hit areas | Fewer mis-taps | M | Playwright measure | Fixed |
| UX-08 | Mobile bar | Padding mismatch, no landmark, no safe area | CSS | Obscured content | High | P1 | nav landmark, calc padding with env(), scroll-padding | Content not hidden | S | Render | Fixed (show-after-hero variant not done: optional) |
| UX-09 | Landmarks, headings | topbar outside header; footer h4 skipped levels | axe | AT navigation | Medium | P2 | topbar in header; footer h2 | axe clean | S | axe | Fixed |
| UX-10 | Motion | Smooth scroll ignored reduced motion | CSS/JS | Vestibular | Medium | P2 | Media query; JS check | Respect preference | S | Code review | Fixed |
| UX-11 | Focus ring | Red ring invisible on red | CSS | Keyboard users | Medium | P2 | Two-tone white + navy ring | Visible focus | S | Render | Fixed |
| UX-12 | Hero pills | Repeat other content | Screenshots | Template feel | Medium | P2 | Removed | Cleaner hero | S | Screenshots | Fixed |
| UX-13 | Services | Six identical icon-tile cards | before-index-1366.png | Template feel, no hierarchy | Medium | P2 | Grid kept; small inline icons; emergency card distinct | Hierarchy | M | Screenshots | Fixed |
| UX-14 | Contact | Service Area card without value; phone repeated | index.html | Redundancy | Low | P3 | Two-up contact | Cleaner | S | Screenshots | Fixed |
| UX-15 | Hero stripe, 25+ | Decorative stripe; 25+ four times | CSS | Noise | Low | P3 | Stripe removed; 25+ once plus approved copy | Cleaner | S | Screenshots | Fixed |
| UX-17 | Card h3 | Weak vs body | CSS | Hierarchy | Low | P3 | 1.4rem | Scannability | S | Screenshots | Fixed |
| UX-19 | Form | No required legend | Form | Clarity | Low | P3 | Added | Clarity | S | Render | Fixed |
| TE-01 | Phone field | pattern invalid in Chrome v-mode; "12345" passed | Console error | Bad leads | High | P1 | JS validation, 10+ digits, inputmode tel | Valid phones | S | Playwright | Fixed |
| TE-02 | Head | Render-blocking fonts and scripts | Lighthouse | LCP 4.7s lab | Medium | P2 | defer scripts, self-hosted Barlow 600/700, preload | Faster paint | M | Render, no failed requests | Fixed (Lighthouse re-run: see Verification Results) |
| TE-03 | Index title | 82 chars | index.html | SERP truncation | Low | P3 | 62 chars | Cleaner SERP | S | Read | Fixed |
| TE-04 | Security headers | No CSP or referrer policy | pages | Defense in depth | Medium | P2 | Meta CSP and referrer | Reduced injection impact | S | No console CSP errors | Fixed (meta CSP limits: no frame-ancestors) |
| TE-05 | fetch | No timeout | js | Stuck "Submitting" | Medium | P2 | 30s (60s with photos) abort then error path | Recoverable | S | Playwright hang test | Fixed |
| TE-06 | crypto | Unguarded | js | Dead form | Low | P3 | Math.random fallback | Resilience | S | Code review | Fixed |
| TE-07 | Honeypot | Silent no-op | js | Autofill victims | Low | P3 | Error box with phone and mailto | Recoverable | S | Playwright | Fixed |
| TE-08 | Photo error | Not specific | js | Clarity | Low | P3 | Names file and sizes | Fewer abandonments | S | Code review | Fixed |
| TE-09 | Caching | No cache-busting | pages | Stale assets | Low | P3 | ?v=20261102 | Fresh deploys | S | Read | Fixed |
| TE-10 | GVR PNG | 720px shown at 210; width attr 724 | image | Weight | Low | P3 | 420px PNG, correct attrs | Smaller | S | File size | Fixed |
| TE-11 | Brand link | aria-label mismatched visible text | HTML | WCAG 2.5.3 | Medium | P2 | Removed | Voice control | S | Read | Fixed |
| TE-12 | 404 redirect | Dropped query string | 404.html | Lost UTMs | Low | P3 | Keeps search and hash | Attribution | S | Code review | Fixed |

## Claim Classification

| Claim | Class | Action |
|---|---|---|
| Gilbarco Veeder-Root ASC | Verified (owner) | Kept; trademark line kept; logo permission pending |
| Slogan, 25+ years copy | Verified (owner) | Verbatim; 25+ attributed to lead technician |
| Services list, 24/7 emergency availability, regions | Verified (owner) | Kept; "Florida" changed to "Central Florida" |
| Phone and service@ email | Verified (owner) | Kept; service@ is monitored and aliases office@ (Nov 2, 2026) |
| Equipment list incl. fleet management, legacy equipment | Plausible-unverified | Kept; owner to confirm |
| "Around-the-clock response", "reduce costly downtime", "One qualified team", "get fueling positions back in service" | Unsupported | Removed |
| "Team notified right away", "email confirmation" | Unsupported (system not configured) | Removed |
| "We answer 24/7", "Talk to a Technician" | Unsupported as worded | Reworded |
| JSON-LD hours Mon-Sun all day | Unsupported | Removed |
| "Sola-Thomas technicians" in photo alt text | Unsupported | Scene-only alt |
| "focuses exclusively on Gilbarco" (404) | Unsupported | Removed |

## Design Decisions and Reasoning

- Services stayed a 3-column grid with hierarchy rather than a redesign: the brand and layout are approved, and six parallel services are parallel content. The fix targets the template tell: big icon tiles became small inline icons, the 24/7 Emergency Repairs card is navy with a call link (the highest-value action), and h3 size rose to 1.4rem.
- Pills and the hero stripe were removed: pills repeated facts shown within a screen (topbar, hero card, footer); the stripe was decoration with no information value.
- Barlow is self-hosted (600/700 latin): removes two third-party origins and a render-blocking stylesheet, tightens the CSP (`font-src 'self'`), and avoids sending visitor IPs to Google for fonts.
- CSP is a meta tag with `'unsafe-inline'` for scripts and styles because GitHub Pages cannot set headers and the pages use an inline GA bootstrap and inline styles. It still restricts origins, form targets, base, and objects. Nonces or hashes are the next step if inline code is removed. A new form endpoint origin must be added to `connect-src` and `form-action` on every page (noted in `js/config.js`).
- Privacy notice scope: describes only what the code does (fields, purpose, Formspree, GA4, localStorage attribution, optional photos, contact). No retention periods, legal-rights language, or compliance claims, because none can be verified from code.
- Photos kept with scene-only alt text: deleting owner-supplied images is the owner's call.

## Baseline Measurements (before)

Lighthouse 12 mobile, lab, simulated slow 4G, 4x CPU:

| Page | Perf | A11y | BP | SEO | FCP | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|---|
| index | 71 | 94 | 100 | 100 | 2.5 s | 4.7 s (p.lead text) | 0 | 300 ms |
| service-request | 74 | 98 | 100 | 100 | 2.6 s | 4.6 s | 0 | 280 ms |

Render-blocking: Google Fonts CSS (~843 ms), config.js and site.js (~306 ms each), site.css. GA 181 KB, ~300 ms main thread. html-validate: no structural errors.

axe-core 4.10.2 at 390 and 1366: serious color-contrast x3 on index (`#services .eyebrow`, `.emergency-band p`, `#contact .eyebrow`); moderate heading-order (footer h4) on all pages; moderate region (`.topbar`, `.mobile-cta`) on all pages. Contrast: red eyebrow on #f4f7fb 4.39; #ffe3e4 on red 3.90; input border 1.75:1.

## Changes Implemented

- `static_site/index.html`, `service-request.html`, `404.html`, new `privacy.html`: identical header (topbar inside header, no brand aria-label) and footer (h2 headings, Privacy link); mobile bar in `<nav aria-label="Quick contact">`; CSP and referrer meta; deferred scripts; versioned assets; copy fixes; pills removed; services redesign; two-item contact; error summary, describedby, legend, state hint; og:image alt/size; JSON-LD without openingHours.
- `static_site/css/site.css`: @font-face, two-tone focus, contrast fixes, 3:1 field borders, 44px targets, safe-area padding, reduced-motion, emergency card, footer titles, privacy prose.
- `static_site/js/site.js`: menu Escape, outside click, focus return.
- `static_site/js/service-request.js`: phone validation, aria-describedby, error summary, timeouts, crypto fallback, honeypot feedback, per-file photo errors, reduced-motion scroll, lazy globals.
- `static_site/js/config.js`: CSP comment. `static_site/fonts/*.woff2` added. `images/Gilbarco_Veeder-Root.png` resized to 420 px. `sitemap.xml` updated. `static_site/README.md` updated.

## Verification Results

Independent QA, November 2, 2026, on branch `audit-fixes` (staged diff). Servers: `python3 -m http.server 8775` from `static_site`, plus a small Node server (port 8776) that serves `404.html` with status 404 for missing paths. Playwright Chromium (`NODE_PATH=$(npm root -g)`), axe-core 4.10.2, Lighthouse 12.8.2. Scripts and screenshots: `qa1.js` to `qa5.js`, `qa-*.png`, `lh-after-*.json` in the audit scratchpad directory.

### Checks

| # | Check | Command / method | Result |
|---|---|---|---|
| 1a | Diff review: field names vs contract | Compared all `name=` attributes in the payload with `docs/service-request-contract.md` | Pass. No field renamed. Payload contains every contract field; utm_* and gclid-type fields are sent only when present. |
| 1b | GA4 events and `data-cta` | Diff grep; click_to_call, click_email, form_start, emergency_checked, generate_lead, form_error all still in JS | Pass. One `data-cta="services"` moved from a paragraph link to the emergency card link. New `confirmation-urgent` and `privacy` values added. |
| 1c | Stale content grep | `grep -rniE "info@\|nationwide\|melbourne\|home services\|business services\|right away\|confirmation will\|we answer\|openingHours" static_site` | Pass. Only hits: the 404 redirect map keys and "For emergencies, call right away" (an instruction to call, not a notification promise). |
| 1d | Live-site fixes still present | Same grep and read | Pass. No notification promise, no "confirmation will be sent", no "We answer 24/7", no openingHoursSpecification. |
| 1e | Copy vs approved facts and JS behavior | Read every changed sentence including privacy.html | Pass with notes (see "Findings from QA"). |
| 2 | `python3 scripts/check_site.py` | Run | Pass: prints `check_site: OK`. |
| 3a | Overflow, console, failed requests | Playwright at 390x844, 768x1024, 1366x900 on index, service-request, privacy, 404 (via Node server) | Pass. scrollWidth equals clientWidth in all 12 combinations. No console errors or warnings (CSP included) and no failed local requests. The expected "404" resource line on the 404 page is excluded. |
| 3b | Keyboard | Tab, Enter, Escape at 390 | Pass. First Tab stop is the skip link. Menu opens with Enter (aria-expanded true), Escape closes it (false) and focus returns to the toggle. |
| 3c | Focus ring | Screenshots `qa-focus-red.png` (red button on navy header) and `qa-focus-band.png` (button on red band) | Pass. White ring on the navy surface, navy outline on the red surface; both visible. |
| 4a | Empty submit | Playwright, Formspree mocked | Pass. 7 `.field.invalid`, 7 `aria-invalid=true`, 0 POSTs, `#errorSummary` role=alert lists the 7 labels, first field focused. |
| 4b | Phone | "12345" then "802-793-2871" | Pass. "12345" rejected with no POST; "802-793-2871" accepted and posted. |
| 4c | Emergency | Checkbox then submit | Pass. Callout shown, priority=EMERGENCY, emergency=yes, `_subject` starts `[EMERGENCY] Service Request ST-...`, emergency note shown in confirmation. |
| 4d | 400 then 200 with photo | Mock 400 first, 200 second | Pass. Exactly 2 POSTs: the first includes the photo, the second has no photo, same request_id, photos_not_uploaded=1, confirmation and photo note shown. |
| 4e | 500 | Mock 500 | Pass. Error box shown, mailto fallback href set, submit button re-enabled and label restored, form still visible. |
| 4f | Success | Mock 200 | Pass. Confirmation visible, focused (`document.activeElement.id=confirmation`), role=status, reference shown. Copy: "We will contact you at {email} or by phone". |
| 4g | GA hooks | `?utm_source=test&utm_medium=qa` landing | Pass. `typeof window.stTrack` is function with deferred scripts. `st_attribution` captured first and last touch; utm_source/utm_medium and attribution_first/last included in the payload. |
| 5 | 404 redirects | Node server, status 404 for missing paths | Pass. `/gilbarco.html` to `/#services`; `/contact?utm_source=x` to `/?utm_source=x#contact`; `/home-services.html` to `/`; `/portal/x` to `/`; `/random-nothing` stays on the 404 page; `/Gilbarco.html/` to `/#services`. |
| 6 | axe-core 4.10.2 | `addScriptTag` on 4 pages at 390 and 1366 | Pass. 0 violations in all 8 runs. "Incomplete" color-contrast items (text over images or gradients, axe cannot decide) on index (6 at 390, 8 at 1366) and service-request (1) were not manually checked. |
| 7 | Lighthouse 12 mobile | `npx -y lighthouse@12 ... --chrome-flags="--headless=new --no-sandbox"` | Pass on all four categories; see table. |
| 8 | Visual review | after-index-390/1366 screenshots, qa-form-errors, qa-form-500 | Pass with nits (see below). |

### Before vs after (Lighthouse mobile, lab, simulated slow 4G, 4x CPU)

| Page | Metric | Before | After |
|---|---|---|---|
| index | Performance | 71 | 97 |
| index | Accessibility / Best practices / SEO | 94 / 100 / 100 | 100 / 100 / 100 |
| index | FCP | 2.5 s | 1.1 s |
| index | LCP | 4.7 s | 2.0 s |
| index | CLS | 0 | 0.024 (the hero `p.lead` shifts on font swap; under the 0.1 target) |
| index | TBT | 300 ms | 170 ms |
| service-request | Performance | 74 | 89 (run 1), 93 (run 2) |
| service-request | Accessibility / Best practices / SEO | 98 / 100 / 100 | 100 / 100 / 100 |
| service-request | FCP | 2.6 s | 1.1 s |
| service-request | LCP | 4.6 s | 1.8 s |
| service-request | CLS | 0 | 0 |
| service-request | TBT | 280 ms | 430 ms (run 1), 310 ms (run 2); not an improvement and within run-to-run noise of the baseline |
| axe (index) | serious contrast x3, heading-order, region | present | 0 violations |

Lab caveats: simulated throttling on a shared sandbox VM served from a local static server (no CDN, no HTTP caching or compression tuning like GitHub Pages), so absolute numbers will differ in production. The sandbox proxy may block or delay Google Analytics, so third-party cost is probably understated; the baseline was measured in the same environment. Two service-request runs differ by 4 points, so treat single scores as approximate. Lab LCP and TBT are not field INP/CLS data.

### Findings from QA

- No regressions were found, so no code fixes were made in this QA pass.
- Privacy notice does not mention cookies. GA4 normally sets first-party cookies (`_ga`) and processes IP addresses; the notice discusses only localStorage. This is an omission, not a false statement. Counsel review (owner decision 9) should cover it. Not changed here because adding wording about cookies needs a decision on consent and GA configuration.
- Privacy notice says Formspree "delivers each request to us by email". That matches the intended setup but the Formspree notification and mailbox monitoring are still unconfirmed (owner decisions 6 and 7).
- Index coverage card repeats "Central Florida" as a heading and again as a bold sub-line (visual redundancy, low).
- Index CLS 0.024 from font swap on the hero paragraph; the standard is met but `size-adjust` on the Barlow fallback would remove it.
- Smooth-scroll plus focus on the first invalid field: a screenshot taken immediately after submit caught the page mid-scroll. After 1.2 s the field was in view below the sticky header (header bottom 72 px, field top 403 px).
- Index visible at 390 px: the sticky call bar appears mid-page only in the full-page screenshot (artifact of stitching), not a defect.

### Checks NOT performed

- Real Formspree delivery, spam filtering, notification email or SMS (all mocked).
- Real devices, Safari/iOS, Firefox, and older browsers; only Chromium was used.
- Screen readers (NVDA, JAWS, VoiceOver, TalkBack). `role=alert` and `role=status` presence was verified in the DOM, not their announcement behavior.
- 320 px width, text zoom to 200%, high-contrast mode, `prefers-reduced-motion` runtime behavior (code review only).
- Manual contrast of axe "incomplete" items; WCAG 2.2 AA conformance as a whole (axe covers a subset).
- GitHub Pages deployment behavior: the real 404 status, MIME types, caching, and the meta CSP under production headers. GA4 requests were not verified against the live property.
- Lighthouse on privacy and 404, and field data (CrUX, INP).
- Legal review of the privacy notice.

### Manual verification still required

1. Submit a real request on a preview deployment and confirm that Formspree delivers it to service@solathomas.com with fields, `[EMERGENCY]` subject, and a photo attachment.
2. Test the photo-failure fallback with a real over-limit upload.
3. Test with VoiceOver on iOS and NVDA on Windows: error summary, field errors, confirmation, mobile menu.
4. Check real phones (iOS Safari, Android Chrome) for tap targets, the sticky call bar, and safe-area padding.
5. Confirm GA4 events arrive (click_to_call, form_start, generate_lead) after deploy.
6. Dave approves copy, photos, logo, and the privacy notice before merge.

## Before/After Screenshots

Directory: `/tmp/claude-0/-home-user-Sola-Thomas-Solutions-Web/57f83ed1-bc47-588e-83e2-b9c0b69df005/scratchpad/audit/`

- Before: `before-{index,service-request,404}-{390,768,1366}.png` (plus `before-index-390-top-viewport.png`, `before-index-390-bottom-viewport.png`, `before-service-request-390-errors.png`)
- After: `after-{index,service-request,privacy,404}-{390,768,1366}.png`

## Remaining Work and Owner Decisions

1. Photos: replace the two AI-looking images with real job-site photos (or approve keeping them).
2. Gilbarco Veeder-Root logo: permission under ASC brand guidelines.
3. Official Sola-Thomas logo (favicon, JSON-LD, og-image).
4. Confirm the supported equipment list (fleet management, legacy equipment, Encore).
5. Confirm the state list and "Other" handling.
6. ~~Confirm service@solathomas.com is monitored~~ Done: monitored, alias of office@ (Nov 2, 2026).
7. Formspree plan, notifications, autoresponse, SMS (#24). Update confirmation copy once an autoresponse is live.
8. About, team, and credential content (owner-supplied facts only).
9. Counsel review of the Privacy Notice.
10. After-hours call handling wording (who answers, voicemail or live).
11. Optional: show the mobile call bar only after the hero scrolls out (UX-08 variant), CSP via nonces, re-run Lighthouse after deploy.

## Final Quality Assessment

Scores are 0 to 5 heuristics from this QA pass, not measurements, standards, or certifications. They reflect the staged branch only. Evidence is from the checks above.

| Dimension | Score | Evidence |
|---|---|---|
| Brand distinctiveness | 3 | Consistent navy/red/white, Barlow headings, slogan verbatim, emergency card distinct. Still uses an interim logo mark and a generic services card grid; the Gilbarco logo carries much of the identity. |
| Visual consistency | 4 | Header, footer, and tokens are identical on index, service-request, privacy, and 404; no overflow at 390, 768, or 1366. Minor nit: duplicate "Central Florida" label in the coverage card. |
| Authenticity | 2 | The two technician photos still look AI-generated and are presented as the owner's team and work (alt text is now scene-only, and there are no staff-identity captions). The interim logo is still in place. There are no real job-site photos, no team or company information, and the "25+" figure is attributed to an unnamed lead technician. Copy is plain and unembellished, but the imagery undermines authenticity until real photos exist. |
| Business credibility | 3 | Unsupported claims (response promises, confirmation email, notification, opening hours, "We answer 24/7") are gone and the grep confirms it. A privacy notice exists and honest expectations are set. Missing: About, credentials, real photos, official logo; GA cookie disclosure and counsel review pending. |
| Content specificity | 4 | Concrete nouns (dispenser, Passport, tank monitor, fueling positions), approved copy used verbatim, services scoped without superlatives. Equipment list is still plausible-unverified (owner decision 4). |
| Navigation and usability | 4 | Skip link is the first Tab stop, the menu works with Enter and Escape and returns focus, the 404 redirect map preserves query strings and hashes, and the emergency phone number is on every page. The old 404 page and sitemap are updated. |
| Accessibility | 4 | axe: 0 violations on 4 pages at 2 widths. Lighthouse A11y 100 on both audited pages. The form has an error summary (role=alert), aria-describedby, and a focused role=status confirmation, with visible two-tone focus. Not verified with real screen readers or at 320 px, and axe passing is not WCAG compliance; the "incomplete" contrast items remain unreviewed. |
| Performance | 4 | Lab LCP 4.7 to 2.0 s (index) and 4.6 to 1.8 s (service-request); Perf 97 and 89 to 93. Service-request TBT of 310 to 430 ms is no better than baseline, and index CLS is 0.024. Lab only. |
| Mobile experience | 4 | No overflow at 390, 44 px targets (per implementer report), safe-area padding, and a labelled sticky call bar. Not checked on real devices, and the hero is long on mobile. |
| Conversion clarity | 4 | Two clear paths (call, request form) repeated in header, hero, emergency band, and mobile bar. The form validates correctly and tells the truth about what happens next. Mailto fallback works on failure. Delivery, notification, and mailbox monitoring are still unconfirmed, so the end-to-end promise cannot be rated higher. |

Overall: the code and copy are materially more accurate, accessible, and faster than the live site, with no regressions found. The two remaining weak points are authenticity (AI-looking photos, interim logo) and unconfirmed back-end delivery; both need owner action, not code.
