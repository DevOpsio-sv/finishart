# FinishArt production readiness

Date: 16 November 2026. Nothing was committed, pushed, deployed, or changed in DNS.

## Decision

**CONDITIONAL GO.**

The existing site can be attached to `https://finishart.bg` after the manual items below. It is not a claim of finished legal sign-off, and it is not a GO for a Viber button or for live email until those items are confirmed.

## Files changed

- `render_site.py` — bilingual page generator
- `public/bg/**`, `public/en/**`, `public/index.html`, `public/404.html`, `public/sitemap.xml`, `public/robots.txt`
- `public/assets/*` — renamed photographs; unused `facebook.png` removed
- `public/css/styles.css` — header controls, cookie panel, texture path
- `public/js/site.js` — language cookie, form messages, cookie panel
- `src/worker.js` — language and old-path redirects, contact languages, cache headers, cookie clear
- `wrangler.toml` — note only; same Workers static-assets setup
- `tests/check_images.py`, `tests/check_worker.mjs`
- `README.md`

Old Cyrillic HTML directories are removed by the generator. The Worker still 301s those URLs to the Bulgarian pages.

## Image renaming

Each file was opened and named from what is visible. Formats were kept. Sofia and “house bathroom” appear in filenames only where the published project already identifies that photograph.

| Was | Now |
|---|---|
| `hero.jpg` | `painted-interior-tall-windows.jpg` |
| `texture.jpg` | `beige-plaster-texture.jpg` |
| `plaster.jpg` | `worker-filling-drywall-seam.jpg` |
| `apartment.jpg` | `white-apartment-living-room-kitchen.jpg` |
| `trowel.jpg` | `gloved-hand-smoothing-plaster.jpg` |
| `room.jpg` | `room-during-renovation-with-ladder.jpg` |
| `review-owner.jpg` | `review-vladislav-hadzhiangelov.jpg` |
| `review-marketing.jpg` | `review-ginka-milanova.jpg` |
| `review-broker.jpg` | `review-trifon-trifonov.jpg` |
| `logo.png` | `finishart-logo.png` |
| `og.jpg` | `finishart-wordmark-social.jpg` |
| `portfolio-apartments.jpg` | `empty-apartment-wood-floor-balcony.jpg` |
| `portfolio-bath.jpg` | `bathroom-glass-shower-and-vanity.jpg` |
| `portfolio-other.jpg` | `stairwell-two-tone-walls.jpg` |
| `project-before-after.jpg` | `living-room-before-and-after.jpg` |
| `antre-before.jpg` / `antre-after.jpg` | `hallway-before-plaster-repair.jpg` / `hallway-after-paint-and-floor.jpg` |
| `bedroom-before.jpg` / `bedroom-after.jpg` | `bedroom-before-window-reveal.jpg` / `bedroom-after-paint-and-floor.jpg` |
| `bath-sofia-before.jpg` / `bath-sofia-after.jpg` | `sofia-bathroom-before-renovation.jpg` / `sofia-bathroom-after-renovation.jpg` |
| `bath-house.jpg` | `house-bathroom-towel-rail.jpg` |
| `bath-house-2.jpg` | `house-bathroom-before-damaged-shower.jpg` |
| `bath-house-3.jpg` | `house-bathroom-shower-wood-slat-wall.jpg` |
| `bath-house-4.jpg` | `house-bathroom-vanity-leaf-wallpaper.jpg` |
| `office-before.jpg` / `office-after.jpg` | `office-before-concrete-shell.jpg` / `office-after-painted-columns.jpg` |
| `office-before-2.jpg` / `office-after-2.jpg` | `office-before-plasterboard-walls.jpg` / `office-after-painted-walls.jpg` |
| `stairs.jpg` | `spiral-stair-wood-handrail.jpg` |
| `stairs-2.jpg` / `stairs-3.jpg` | `stair-details-before-renovation.jpg` / `stair-details-after-renovation.jpg` |

Bulgarian and English `alt` text describes the same frames. Gallery order is unchanged, including Sofia bathroom after-then-before. `facebook.png` was not referenced; the visible icon is still the existing SVG.

## BG/EN

Bulgarian is the default. English is a full translation of the visible site, not a placeholder.

- URLs: `/bg`, `/en`, `/bg/portfolio`, `/en/portfolio`, and the same suffix for projects and legal pages.
- Trailing slashes are dropped by the existing Wrangler `html_handling`, so canonicals have no trailing slash. `/bg/` still reaches `/bg`.
- The header switch is `BG | EN` on desktop and mobile. It keeps the current path and hash. Choosing a language sets `finishart-lang` for 180 days. `/` then 302s to that language. With no cookie, `/` goes to `/bg`.
- `hreflang` `bg`, `en`, and `x-default` (Bulgarian) are on each pair. Canonicals, titles, descriptions, `lang`, Open Graph locale, and the sitemap alternates match the language.
- Old Wix paths, including the broken `апарта�менти` path, 301 to the Bulgarian pages on the same hostname. The Worker does not redirect `finishart.bg` to `www.finishart.bg`. DNS was not changed.
- Page titles now end in `| ФинишАрт` / `| FinishArt`. The old Wix `| Alex` suffix was not kept.
- The home description no longer calls the company „Финиш Арт ООД“.

## Phone and Viber

Phone is the number already published on the site: `tel:+359882820025` (0882 820025). It is in the header, the menu, the hero quote button, and the footer.

Viber was **not** added. The public site, the Wix copy in this repo, and a web search do not show this number as a Viber account. No Viber link or profile is displayed. When the business confirms the number is registered, the link to use is `viber://chat?number=%2B359882820025`, with the phone link as the fallback. That was not tested on a device.

The contact form is unchanged in fields. It posts to `POST /api/contact`. Validation messages follow the page language. There is no marketing checkbox. A privacy-policy link sits by the button. The lawful basis described for a quote request is Art. 6(1)(b), not a consent tick.

Resend delivery was **not** verified. Without `RESEND_API_KEY` and `CONTACT_FROM` the Worker returns 503 and shows the phone number. A real send still needs those secrets and a confirmed inbox.

## Legal pages and cookies

Footer and legal pages name **Био Дизайн 2021 ЕООД / Bio Design 2021 Ltd., ЕИК 206494745**.

Checked on 16 November 2026 against papagal.bg and finansi.bg, which mirror the Commercial Register. They are not an official extract from portal.registryagency.bg.

- Active, entered 28 April 2021, manager named as Силвена Енчева Войнова.
- Seat in those mirrors: Sofia 1504, Serdika, 17 Yanko Sakazov Blvd.
- The site’s published contact address remains Sofia **1505**, 17 Yanko Sakazov Blvd. The street matches. The postal code does not. Both are stated on the company page.
- Those mirrors say the company is not VAT-registered. No VAT number is published.
- “Working since 2018” stays on the home page as the existing marketing line. It is not the register entry date.
- The register activity text does not specifically list plastering. The company still needs to confirm it is the contracting party.

Pages, in both languages: privacy, cookies, website terms, company details, and the existing accessibility statement. They describe the form, the phone link, the absence of Viber, Cloudflare hosting, the 60-second IP rate limit, Resend, and the Gmail inbox. Items that are not known are marked for confirmation: mailbox retention, Resend and Google contracts, the international-transfer tool, Cloudflare log retention, permission to keep client portraits online, and the right to host the former Wix photographs. This is not a certificate of compliance.

Cookies actually present:

| Name | Provider | Purpose | Category | Duration | Consent |
|---|---|---|---|---|---|
| `finishart-lang` | FinishArt | Remember an explicit language choice | Strictly necessary | 180 days | Not required. Set only after BG/EN is used. |

No analytics, marketing, or third-party cookies, and no tracking scripts. There is no accept/reject banner, because that would invent a choice the site does not offer. Footer **Cookie settings** opens a panel. **Forget language preference** goes to `?forget-lang=1`. The Worker clears the cookie and returns to the page. Strictly necessary behaviour is unaffected because nothing else is stored.

## Cloudflare

The project stays on Workers with static assets (`wrangler.toml`: `main = src/worker.js`, `assets.directory = ./public`, `run_worker_first = true`, `not_found_handling = 404-page`). It is not an SPA.

- `npx wrangler deploy --dry-run` (Wrangler 4.162.0) read the `public` assets and exited without uploading. Upload size of the Worker script was 9.92 KiB.
- `CONTACT_TO` remains a var. `RESEND_API_KEY` and `CONTACT_FROM` stay secrets (`.dev.vars.example`).
- Cache: HTML 5 minutes, CSS/JS 1 day, images, fonts, and `/_files/` 30 days. `/api/contact` is `no-store`.
- Canonical host is `https://finishart.bg`. The Worker serves both hostnames and does not rewrite them. `www.finishart.bg` 301s to the apex through a Cloudflare Redirect Rule. That rule loops if the Worker also redirects the apex to www.
- No production route was added. DNS was not edited.

## Test results

Passed:

- `python render_site.py`
- `python tests/check_images.py` — 30 content images across 32 pages, gallery order, hero priority, texture file
- `node tests/check_worker.mjs` — `/` to `/bg` on the same host, cookie to `/en`, both hostnames without a host swap, old portfolio and bathroom URLs, HTML and image cache headers, English and Bulgarian contact errors, 503 when mail is not configured, cookie-clear redirect, canonical URLs on `https://finishart.bg`
- `npx wrangler deploy --dry-run` — exit 0, no deploy
- Browser on `http://127.0.0.1:3010`: Bulgarian home, English home, language metadata, phone `tel:+359882820025`, portfolio project images (Sofia after, then before), language switch URL for that project, English form validation and the offline message, cookie panel, company page, no horizontal overflow at 390px and 1920px

Not verified:

- A real Resend delivery
- Viber on a phone
- The Cloudflare Redirect Rule from `www.finishart.bg` to `https://finishart.bg` (leave it off until this Worker is deployed, then turn it on; the Worker no longer sends the apex back to www)
- An official Commercial Register extract
- Withdrawal inside the static preview: `python -m http.server` does not run the Worker. The clear link was verified against the Worker module, not against a live device.

There is no separate lint or Node test suite in this repository.

## Remaining manual configuration

1. Confirm the number is on Viber before any Viber button is added.
2. Put `RESEND_API_KEY` and `CONTACT_FROM` in Worker secrets. Send one real enquiry and confirm it arrives at `alex.finishart@gmail.com`.
3. Sign or confirm the Resend and Google arrangements, and record how long enquiry mail is kept.
4. In Cloudflare, keep both hostnames on this Worker, enable the Redirect Rule from `www.finishart.bg` to `https://finishart.bg`, and confirm log retention. Do not redirect the apex to www. Do not drop MX, SPF, DKIM, or DMARC.
5. Download an official register extract and settle 1504 vs 1505, VAT status, and that this company is the party to FinishArt contracts.
6. Confirm rights to host the former Wix photographs and to keep the named client portraits online.
7. Have someone responsible for the business read the privacy, cookie, and terms pages before they are treated as final.

## Local preview

```bash
python render_site.py
python -m http.server 3010 --directory public
npx wrangler dev
```

Static preview: `http://127.0.0.1:3010/bg` and `/en`. Redirects, the contact API, and cookie clearing need `wrangler dev`.
