# Service Request Payload Contract

The public form (`static_site/service-request.html`) POSTs `multipart/form-data` to
`ST_CONFIG.formEndpoint` (`static_site/js/config.js`) with `Accept: application/json`.
Any 2xx response is treated as success. Today the endpoint is Formspree; the
service-management app intake API must accept the same fields so the endpoint can be
swapped without touching the page.

## Customer fields

| Field | Required | Notes |
|---|---|---|
| `company_name` | no | max 150 |
| `contact_name` | yes | max 120 |
| `phone` | yes | free text, at least 10 digits/symbols |
| `email` | yes | validated email, also sent as `_replyto` |
| `site_name` | no | station or site name |
| `site_address` | yes | street address |
| `site_city` | yes | |
| `site_state` | yes | `CT` `MA` `ME` `NH` `RI` `VT` `FL` `Other` |
| `site_zip` | no | `12345` or `12345-6789` |
| `equipment_type` | no | `Fuel dispenser`, `Passport POS`, `Payment terminal`, `Veeder-Root tank monitoring`, `Fleet management system`, `Other / not sure` |
| `equipment_model` | no | |
| `description` | yes | max 4000 |
| `emergency` | always | `yes` or `no` |
| `preferred_date` | no | `YYYY-MM-DD`, today or later |
| `lead_source` | no | self-reported: `google_search`, `google_business_profile`, `linkedin`, `facebook`, `instagram`, `referral`, `existing_customer`, `other` |
| `photos` | no | 0..5 image files, 10 MB total (repeated field) |

## System fields

| Field | Notes |
|---|---|
| `request_id` | `ST-YYYYMMDD-XXXXX`, generated in the browser, shown to the customer. Reused on retry, so it is the idempotency / de-duplication key. |
| `submitted_at` | ISO 8601 UTC from the browser clock |
| `priority` | `EMERGENCY` or `standard` |
| `_subject` | Notification subject. Prefixed `[EMERGENCY]` when `emergency=yes`. |
| `_replyto` | Copy of `email` |
| `_gotcha` | Honeypot. Non-empty means spam; the browser never submits it filled. |
| `photos_not_uploaded` | Present only when the upload failed and the request was re-sent without photos (count of photos dropped). |
| `page_url` | Page the form was submitted from |

## Attribution fields

Captured by `static_site/js/site.js` on every page view and kept in `localStorage`
(first touch is preserved, last touch is replaced by campaign or external-referrer visits).

| Field | Notes |
|---|---|
| `utm_source` `utm_medium` `utm_campaign` `utm_term` `utm_content` | Last-touch values, when present |
| `gclid` `fbclid` `msclkid` | Ad click IDs, last touch |
| `referrer` | External referrer of the last touch |
| `landing_page` | Path + query of the last-touch landing |
| `attribution_first` / `attribution_last` | JSON objects with the above keys plus `ts` |

Mapping to the report's source categories (Google Ads, organic, GBP, LinkedIn,
Facebook, Instagram, referral, direct/existing, other) is done in the app: prefer
`gclid` / `utm_*`, then `referrer`, then `lead_source`, else `Other / unknown`.

## Requirements on the intake endpoint

- Treat `request_id` as idempotent: a repeat POST with the same id must not create a second job.
- Reject when `_gotcha` is non-empty (respond 2xx so bots get no signal).
- Notify `service@solathomas.com` (email) and (802) 793-2871 (SMS); emergencies flagged in both.
- Send the customer an acknowledgment email containing `request_id`.
- Store the request before responding 2xx. Never return success for a request that was not saved.
