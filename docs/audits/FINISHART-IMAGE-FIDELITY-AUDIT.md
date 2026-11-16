# FinishArt image fidelity audit

Compared the local static site with the live Wix site on 16 Nov 2026.

- Reference: https://vasilevasilvena.wixsite.com/alex
- Portfolio: https://vasilevasilvena.wixsite.com/alex/portfolio
- Local check: `python -m http.server 3010 --directory public`

Wix was read in a browser (rendered images, not only HTML) and from the portfolio sitemaps. Each Wix media id was downloaded from `static.wixstatic.com` and compared with the local file using a 16×16 average hash plus the published crop rectangle. A hash distance of 0–2 means the same photograph.

This is not a claim of pixel-perfect page layout. Image identity, crop, and order were checked. Browser chrome, the Wix banner, and the Consentik cookie bar were ignored.

## Comparison table

| Page | Section | Wix image | Previous local image | Problem | Fix | Validation |
|---|---|---|---|---|---|---|
| Home | Header / footer logo | `a86e04_2ccfd23a…` white wordmark, transparent | `logo.png` 835×230 | Same wordmark once placed on the terra background | Left in place | Composited both on `#823c2e`; they match |
| Home | Hero | `a86e04_cafcc78b…` 1536×2048 | `hero.jpg` 1350×1800 | Same photo, reduced file | Replaced with the original JPEG. `fetchpriority="high"` | File is 1536×2048. Rendered natural size matches |
| Home | Защо ние? texture | `11062b_4f5f004a…` JPEG, EXIF orientation 6, landscape plaster | `texture.jpg` 1200×1800, no EXIF | Same pixels stored sideways, so the cover background was rotated 90° | Saved the oriented landscape JPEG, long edge 2400 | File is 2400×1600. CSS still uses `texture.jpg` |
| Home | Нашият ангажимент | `a86e04_fce88de0…` 2816×1536 | `plaster.jpg` 1800×982 | Same photo, soft JPEG | Replaced with a 2400px JPEG from the original | Hash match to the Wix file |
| Home | Интериорно боядисване | `a86e04_ec15b077…` 1397×1024, cover center | `apartment.jpg` same pixels, 93 KB | Over-compressed | Replaced with the original JPEG | Hash distance 1. Frame is 276×325, `object-position: center` |
| Home | Шпакловка | `11062b_266d4465…` crop `y=327` `h=2346` of 2003×3000 (symmetric) | `trowel.jpg` plus `object-position: center 42%` | Focal point sat too high | Original-based 1602×2400 JPEG. Removed the inline position | Center crop matches the Wix crop (hash distance 3 vs 16 for the old position) |
| Home | Основен ремонт | `edcb2e19a98747b6…` center crop `x=1051` `w=2252` of 4355×2638 | `room.jpg` plus `object-position: 72%` | Crop showed the right edge instead of the window wall | 2400px JPEG. Position is center | Center crop hash distance 0 against the Wix crop. Old 72% position was 74 |
| Home | Review, owner | `a86e04_4d28efd4…` 1536×1024, cover center, arch mask | `review-owner.jpg`, `object-position: center 30%` | Same photo. Vertical position did not change a landscape-in-portrait crop. File was a heavy recompress | Sharper JPEG. Position follows the element default, center | Hash distance 0. Arch radius kept; the Wix slide is visibly semicircular |
| Home | Review, marketing | `a86e04_2df2a417…` crop `y=476` `h=1891` of 1350×2843 | `review-marketing.jpg` 855×1800, `object-position: center 20%` | Same photo, biased toward the top | 950×2000 JPEG from the original. Center crop, which matches the equal top and bottom Wix trim | Hash distance 0 on the full photo |
| Home | Review, broker | `a86e04_f6db8871…` crop `y=51` `h=1435` of 1024×1536 | `review-broker.jpg` | Same photo, nearly the full frame. Soft file | Sharper JPEG at the original 1024×1536 | Hash distance 0 |
| Home | Service card frame | Displayed about 276×325, cover | CSS `aspect-ratio: 276 / 340` | Frame was taller than Wix, so the crop was tighter. Intrinsic `height` attributes also stretched the box | Frame is `276 / 325` with `height: auto` and attributes `276`×`325` | At a 663px viewport the boxes were 472×556 (ratio 0.849) |
| Home | Open Graph | `a86e04_514c095b…` black wordmark on transparency | `og.jpg` white wordmark on terra | Different social image | `og.jpg` is that wordmark on white, 1536×1024 | Not shown in the page. Used only by `og:image` |
| Home | Facebook icon | `64a918_ecce7132…` 125×125 | Inline SVG, plus unused `facebook.png` | The PNG byte-matches Wix and is not displayed | Left both. The visible icon stays the existing SVG | No page change |
| Portfolio | Three collection covers | `a86e04_02754e96…`, `a86e04_80fb2764…`, `a86e04_92bdd68b…` | Matching JPEGs, smaller | Same photographs | Higher-quality JPEGs, same filenames | Hash distance 0–2 |
| Апартаменти | Project gallery | Антре преди/след, спалня преди/след | Same four files, after photos downscaled | Order was already correct. After photos were 1437×1800 vs 1792×2244 | Replaced with sharper files. Order unchanged | Lightbox still uses `data-zoom` |
| Баня София | Gallery | After image, then before image | Before, then after | Order reversed | Order is after, then before. Both files upgraded | DOM order matches the Wix sitemap |
| Баня в къща | Gallery | Large bath, then the three detail photos | Detail, detail, large, detail | Large photo was third | Order is `bath-house.jpg`, `bath-house-2.jpg`, `bath-house-3.jpg`, `bath-house-4.jpg` | First lightbox target is the wide bath photo |
| Други обекти | Collection and projects | Office (4 photos) and stairs (3 photos), published on Wix by 18 Oct 2026 | Collection had no project images | Galleries were missing | Added the two project pages and their thumbnails. Copy is the Wix text | Pages return the four and three images. Clicking the first office photo opens that file in the lightbox |
| All content images | Loading | Wix lazy-loads below the fold | No `loading` attribute | Hero competed with later images | Hero is eager and high priority. Other content images are `loading="lazy"` | Hero request is prioritized in the homepage markup |

## Image inventory

### Wix originals recovered

| Role | Wix media | Original size | Local file after the fix |
|---|---|---|---|
| Logo | `a86e04_2ccfd23a8d4c4c03958415ba84347d37` | 1536×1024 PNG, trimmed content about 814×208 | `logo.png` 835×230, unchanged |
| Hero | `a86e04_cafcc78be52a4b3c9ced7895c98c4cec` | 1536×2048 JPEG | `hero.jpg` 1536×2048 |
| Beige texture | `11062b_4f5f004a79a946b89cd612239ba63715` | 3264×4896 stored, EXIF 6, displays 4896×3264 | `texture.jpg` 2400×1600 |
| Commitment | `a86e04_fce88de0072e498bbd6e1302f83864cc` | 2816×1536 | `plaster.jpg` 2400×1309 |
| Interior painting | `a86e04_ec15b0773f0847698d7c0df511f304ab` | 1397×1024 | `apartment.jpg` 1397×1024 |
| Plastering | `11062b_266d446528464279b41fa9780ea578d8` | 2003×3000 | `trowel.jpg` 1602×2400 |
| Renovation | `edcb2e19a98747b6a0cf1cadbbae0a3e` | 4355×2638 | `room.jpg` 2400×1454 |
| Owner review | `a86e04_4d28efd4780b454291639ac6c2ecddd8` | 1536×1024 | `review-owner.jpg` |
| Marketing review | `a86e04_2df2a417c7484b2182880a128789cf9a` | 1350×2843 | `review-marketing.jpg` 950×2000 |
| Broker review | `a86e04_f6db887150b24ee6977c12441dc2c514` | 1024×1536 | `review-broker.jpg` |
| Open Graph | `a86e04_514c095b6c5d43e792661e3af6e239b4` | 1536×1024 PNG | `og.jpg` |
| Apartments cover | `a86e04_02754e96294c44caa963829cc6c8f60a` | 2816×1536 | `portfolio-apartments.jpg` 2400×1309 |
| Bath cover | `a86e04_80fb2764d2914b528cc05fe79a4b2ccc` | 1536×1024 | `portfolio-bath.jpg` |
| Other cover | `a86e04_92bdd68b7d8842e1b263484ecd860b50` | 1536×1024 | `portfolio-other.jpg` |
| Apartment card | `a86e04_16dd20d1b2834e1c9694c0c0220db81f` | 2956×1285 | `project-before-after.jpg` 2400×1043 |
| Antre / bedroom | `a86e04_16d732d1…`, `a86e04_86378cfa…`, `a86e04_1286165a…`, `a86e04_4ca2cbee…` | 1200×1600 and 1792×2244 | `antre-*.jpg`, `bedroom-*.jpg` |
| Sofia bath | `a86e04_68b9a6db…`, `a86e04_a2e90634…` | 2638×1501 and 2643×1511 | `bath-sofia-after.jpg`, `bath-sofia-before.jpg` |
| House bath | `aea723ade18b4eb0b9a490cf623f4049` and three `a86e04_…` details | 4580×3280, 704×1389, 688×1445, 688×1440 | `bath-house.jpg` 2560×1833 and `bath-house-2/3/4.jpg` |
| Office | `a86e04_4249ce5d…`, `a86e04_5587ba1f…`, `a86e04_867b160b…`, `a86e04_a4593965…` | up to 2528×1520 | `office-before.jpg`, `office-after.jpg`, `office-before-2.jpg`, `office-after-2.jpg` |
| Stairs | `74314df2204f45d080230ef02adb07c4`, `a86e04_0285d5ce…`, `a86e04_6a5560ec…` | 4032×3024 and two 1024×1536 | `stairs.jpg`, `stairs-2.jpg`, `stairs-3.jpg` |
| Facebook | `64a918_ecce71321e844673b977c572d915fa2b` | 125×125 | `facebook.png`, unused, byte-identical |

Wix also repeats the logo and the Facebook icon in the header and footer. Those are the same files, not extra photographs.

### Local files that were already the right photograph

Every homepage and existing portfolio photograph hashed to its Wix original. None of them was a stock substitute or a swapped project. The defects were resolution, EXIF orientation, focal point, gallery order, and two missing projects.

`facebook.png` is unused. It was not deleted.

## Confirmed fixes

- `public/assets/` photographs replaced from the downloaded Wix masters. Opaque PNG masters were saved as JPEG. Long edges are capped at 2000–2560 px so a gallery does not ship a 4–7 MB file. The hero and the apartment photo are the original JPEGs, not recompressed.
- `public/css/styles.css`: service cards use `aspect-ratio: 276 / 325`, `height: auto`, and `object-position: center`. The arch on review photos is unchanged.
- `render_site.py` regenerated the HTML. Removed `object-position: center 42%`, `72%`, `center 30%`, and `center 20%`. Hero is `fetchpriority="high"`. Below-the-fold images are `loading="lazy"`.
- Bath Sofia gallery order is the finished bath, then the earlier state.
- House bath gallery starts with the wide photograph.
- New pages, using the Wix wording:
  - `/portfolio-collections/my-portfolio/шпакловка-и-боядисване-на-офис-пространства`
  - `/portfolio-collections/my-portfolio/реновация-на-стълбище`
- `tests/check_images.py` checks that every `<img src="/assets/...">` exists, has real pixels, the texture is landscape, the bath galleries are in the Wix order, and the two new galleries are present.

## Unresolved

- Masters larger than the cap were not uploaded at full camera size. The 4580×3280 bath, the 4355×2638 renovation, and the 4896×3264 texture were recovered and then saved at 2400–2560 px on the long edge. That is sharper than the previous files and is the size a full-bleed or lightbox view needs. It is not the untouched camera file.
- The local browser used for screenshots was about 384–663 px wide. A separate 1440×900 screenshot pass was not captured, because forcing a 1440 px layout inside the tool’s smaller capture window clipped the picture. Crop identity at desktop was checked against Wix’s own crop URLs (`x`, `y`, `w`, `h`) rather than a side-by-side 1440 screenshot.
- Wix was inspected at its desktop render (content width about 1905 px). A separate Wix mobile art-direction pass was not completed. The desktop HTML did not advertise a second set of mobile photographs. Local overflow at 390×844 was 0, and the hero loaded at 1536×2048.
- Review photos stay in the existing semicircular mask. That matches the Wix slide, which is visibly an arch even though the `<img>` itself reports `border-radius: 0`.
- Existing captions were not rewritten. The house-bath caption „Бяна - преди“ is still there.
- `facebook.png` remains unused. The visible icon is the inline SVG.
- The logo file still contains a faint transparent gradient. On the terra header it matches the Wix wordmark, so it was not replaced.

## Screenshot evidence

Saved in `docs/audits/screenshots/`.

| File | What it shows |
|---|---|
| `wix-reviews.png` | Wix service row and the start of the client arch. The renovation card is the centered window, not the right edge |
| `before-service-cards.png` | Local renovation card before the fix, cropped to the right-hand window |
| `after-room-card.png` | Same card after the center crop. The ceiling and window sit in the middle of the frame |

Measured after the fix, without relying on those pictures:

- Hero natural size 1536×2048, box 390×521 at a 390 px viewport, horizontal overflow 0.
- Service boxes 472×556 at a 663 px viewport, ratio 0.849, `object-position: 50% 50%`, all three natural sizes non-zero.
- „Други обекти“ thumbnails keep their file ratios (1536×1024 and 2400×1800).
- Office lightbox opens `/assets/office-before.jpg`.

## Validation

There is no Node lint, typecheck, or production build in this repository. The site is static HTML generated by `render_site.py`.

- `python render_site.py` completed and rewrote the pages, sitemap, and robots file.
- `python tests/check_images.py` passed: 30 local images across 13 pages.
- Browser checks on `http://127.0.0.1:3010`: images returned HTTP 200, natural dimensions were non-zero, service frames were not stretched, gallery lightbox opened the clicked file, and `scrollWidth - clientWidth` was 0 at the measured widths, including 390 px.
- No image request failed on the pages that were opened.

## Scope

Changes are limited to image files, image attributes, the service-card frame, gallery order, and the two portfolio projects that had no local images. Colors, type, navigation, prices, and existing sentences were not redesigned. The new project pages repeat the Wix location, date, services, and stair description so the photographs have the same pages as on Wix. One README sentence that said the „Други обекти“ collection had no projects was updated, because that is no longer true.
