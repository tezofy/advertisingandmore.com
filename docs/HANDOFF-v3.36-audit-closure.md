# v3.35–v3.36 — Audit Closure Handoff (2026-10-24)

Pipeline: `python3 build_top15.py` regenerates `party-services-rentals-top15.html`
from the untouched upload source. `uploads/` never modified.

## Audit item → implementation

| # | Audit item | Status | Where |
|---|-----------|--------|-------|
| 1 | Trust band slim 373px → ~190–230px, real logos only | ✅ | POLISH_CSS `#trusted-brands`; 12 `.hp-logo-card` placeholders intentionally empty — fill with **real** client logos only |
| 2 | Neutral form placeholders; LinkedIn optional; core fields name/email/phone/service | ✅ | `_swap()` in main() |
| 3 | One explicit conversion CTA label, coffee motif kept | ✅ | All user-visible CTAs now read **Book a Free Consultation** (header, hero, drawer, 2 mid-page bands, modal, form submit, footer, footer link) |
| 4 | Repeated mid-page CTAs + proof snippet above form | ✅ | 2 navy CTA bands (after Top 15, after Services) → `#contact`; 3-chip reassurance strip directly above the form; no fabricated ratings |
| 5 | Soften "100% SUCCESS RATE" | ✅ | Footer seal now reads **COMMITMENT** |
| 6 | FAQ (objections + SEO) | ✅ | `#hp3-faq`, 6 Q&A, accessible accordion, FAQPage JSON-LD |
| 7 | Sticky category filter on 100-catalogue; drinks trim | ✅ | `#services .category-tabs-container` sticky under header (blur cream surface); drinks section ~30% shorter via POLISH_CSS overrides |
| 8 | Slim 7-link nav | ✅ | Already 7 links; Careers de-emphasised (opacity .8, softer HIRING pill); compact mode 1025–1280px prevents overflow |
| 9 | Meta description, OG/Twitter, Schema.org | ✅ | ProfessionalService + FAQPage JSON-LD (valid); OG + Twitter card incl. 1200×630 `assets/img/og-image.jpg` |
| 10 | Externalize data-URI images, lazy-load, hero preload, LCP ≤2.5s | ✅ | 182 inline URIs → 157 hashed WebP files (`assets/img/`, deduped) + og JPEG; HTML **13.07 MB → 1.62 MB**; 95 lazy / 6 eager hero imgs; hero `<link rel=preload>`; measured LCP **~0.47s** under Slow-4G + 4× CPU throttle |

## Technical notes

- Reveal animation: rAF-throttled scroll/resize position check (replaced threshold
  IntersectionObserver, which missed instant jumps). 21/21 reveal at every
  breakpoint; all visible immediately under prefers-reduced-motion.
- Anchor targets carry `scroll-margin-top: 92px` for the sticky header.
- No data URIs remain (build asserts this). Zero console/HTTP errors in QA
  across 1440/1280/1100/1025/768/390/320; no horizontal overflow.
- Regression suite `shot_t15_v5.py` green (wishlist fly-to-tray, mini-sheets,
  process keyframes, toasts, reduced motion).

## v4.x client-update port (from "party-services-rentals-top15 (20) (6).html", 2026-10-24)

Source-of-truth fragments kept verbatim in `build-fragments/` and injected at the
client's exact section positions. Their inline data URIs go through the same
externalization pipeline (198 URIs → 173 WebP + og JPEG; HTML stays 1.68 MB).

| Client update | Position (final section order) | Notes |
|---|---|---|
| v4.10 WOW band `#pick-your-wow` — 6 photo tiles | after `#trusted-brands`, before `#why-choose` | tile click activates matching catalogue tab (`data-wow-cat`) and smooth-scrolls to `#services`; verified cat-3 |
| v4.30 Party recipes `#party-recipes` — 4 cards | after `#why-choose`, before `#top15` | one click adds 5 real catalogue keys via new `window.addToWishlist` helper (dedupes, toasts, tray sync); verified 5→10 across two recipes, re-click says "Already in your plan" |
| v4.40 Featured experiences `#featured-experiences` — 5-shot mosaic | after `#services`, before `#our-process` | legacy pillar/dot script remains but safely no-ops (elements removed in v4.40); "View Full Gallery" CTA → `#services` |
| v4.12 compact trust strip | directly under hero | measured 121px tall, 31px logo cards; marquee `hpLogoScroll` preserved (identical to client file) |
| v4.20 section-deck style | global head CSS | deck lines added to Why Choose, Recipes, Testimonials |
| v4.01 hero foot fade removed | `#hero.hb-hero::after { content:none }` | crisp hero edge |
| Anonymised testimonial bylines | `#testimonials` | "Corporate/Private Client" + event role instead of invented names (FTC-safe); photos retained |
| og:site_name | head | added |

Section order now: hero → trusted-brands → pick-your-wow → why-choose →
party-recipes → top15 → services → featured-experiences → our-process →
happy-meeting → hp3-faq → testimonials → contact. Regression suite
`shot_t15_v5.py` green; zero console/HTTP errors and no horizontal overflow at
1440/1025/768/390/320; 21/21 reveals; zero data URIs.

## Actions required from the client before go-live

1. Deploy the **`assets/img/` folder next to the HTML** — all image paths are relative.
2. Replace relative `og:image` / JSON-LD `image` with the absolute production URL.
3. Insert real client logos into the 12 empty trust-logo cards (never invent).
4. Add real Google reviews/aggregate rating when available (FTC 16 CFR Part 465 —
   no fabricated testimonials; believable aggregate band is 4.2–4.5 stars).
5. LinkedIn field stays optional; remove the field entirely if desired.

---

# v5 — Native-brand rebuild (2026-10-25)

Rebuild stays in `build_top15.py`; source upload untouched; `python3 build_top15.py` GREEN.
Full Bengali audit + per-mockup verdicts: `AUDIT-v5-native-brand-rebuild.md`.

## v5 changelog
1. New `BLOCK_STATS` (#am-stats): 12+/150+/98%/100% agency-wide, two protective
   footnotes incl. the client mockup's own logo disclaimer.
2. New `BLOCK_QUOTE`: verbatim Sir Richard Branson quote from advertisingandmore.com.
3. Testimonials rewritten: 3 fabricated persona cards (AI faces, 5-star, fake names)
   replaced with the 3 REAL parent-published reviews (LinkedIn, Bosch, Universal),
   logo cards via `assets/img/testi-{linkedin,bosch,universal}.png` (downloaded from
   the live site). Eyebrow -> "Kind words". No star ratings, no schema ratings.
4. Footer seal restored to "100% SUCCESS RATE" (parent-site exact badge).
5. Footer email: Cloudflare-obfuscated placeholder -> mailto:hello@advertisingandmore.com.
6. Both consent checkboxes now opt-in (pre-checked removed).
7. Catalogue H2 -> "100 ways to make your event unforgettable."
8. Two-tier CTA: CLICK FOR COFFEE pills kept (4); in-content bands -> Request a Quote (3).
9. Featured mosaic moved above Why-Choose (emotion-first funnel); process deck added
   ("Five simple steps, a lot of heart, and just enough caffeine.").
10. Cloudflare email-decode + 2 challenge scripts stripped (0 console/network errors).
11. Process animation: 10s infinite loop -> 4.8s one-shot `forwards` reveal; all 5
    steps remain fully visible (fixes step-5 icon opacity:0 defect).
12. `HERO_FIX_CSS` (<=1023px): margin-top:auto pin replaced with 34px flow gap;
    coffee-cup badge no longer covers hero description (6px clearance at 390/360).
13. Dead fabricated-quote carousel removed from `featured-experiences.html`
    (anonymous "Corporate Client"/"Annual Dinner Committee"/"Events Manager" strings;
    markup was already removed in v4.30, JS array was the last remnant).

## QA (Playwright, 1440/1024/768/390/360)
0 console errors, 0 failed requests, 0 horizontal overflow, 0 section overlaps;
wishlist + testimonial carousel functional; output 1.68 MB, 0 data URIs, valid JSON-LD.

---

# v5.1 — pre-footer plan band + testimonial truth correction (2026-10-25)

Build GREEN via `python3 build_top15.py`; `uploads/` untouched. Output 1.69 MB.

## New component: plan band (#plan-band), directly above #site-footer
- White rounded two-column card: left = 4th REAL parent-published testimonial
  (Dentsu, verbatim quote, dentsu-tc.png logo, "Associate Digital Director");
  right = conversion nudge "Let's plan your event." + gold Request a Quote pill
  + animated party-popper doodle (reduced-motion safe).
- Rides the shared .reveal float-up system in POLISH_JS (selector
  '#plan-band .plan-col', 140ms stagger). Note: markup must NOT ship with the
  .reveal class pre-added — the POLISH_JS guard skips elements already carrying it.
- Responsive: two columns >860px; stacked + centered + full-width pill <=640px;
  doodle and type scaled down on phones so the band fits 360px with zero overflow.

## Critical truth correction (parent-site re-audit against live advertisingandmore.com)
The live site has ONE "Kind words" block. v5.0 quotes did not match it, so they
were replaced with the verbatim published text + exact attributions:
- LinkedIn: "Congratulations for being the highest earners for LinkedIn..." /
  Regional Account Director, South East Asia
- Bosch: "Never failed to provide sound advice & solutions..." /
  Corporate Communications & Brand Management
- Universal Music Group: "Managed our campaigns on Facebook, Google, YouTube &
  Mobile..." / Label Manager
- Dentsu (new, plan band): "Fine staff who has performed outstandingly..." /
  Associate Digital Director
- Branson block corrected to the site's actual quote: "Don't think what's the
  cheapest way... Think, what's the most amazing way to do it?"
All 4 logos downloaded from the live site's /2026/07/ media folder into assets/img.

## QA
0 console/network errors across 1440/1024/768/390/360; no overlaps or horizontal
overflow; reveal fires once and stays visible; Dentsu logo decodes; full-page
images regenerated (full-page-desktop/mobile .png + .jpg now include the band).

## v5.2 (2026-10-25) — Occasion strip above Featured Experiences
User asked (Bengali) what could sit ABOVE the "Ultimate Party Playground"
featured block to make it prettier/smarter. Audit: #pick-your-wow and
#featured-experiences are two consecutive photo-heavy sections, so another
image band would repeat/overload. Added a light text-led `#occasion-strip`
(`build-fragments/occasion-strip.html`, wired in build_top15.py via
FRAG_OCCASIONS between WOW and FEATURED): gold-eyebrow + six outlined pills
(Corporate Galas, Product Launches, Weddings, Annual Dinners, Team Building,
Private Celebrations), each with an inline SVG icon and a real in-page anchor
to #services. No new imagery, no invented facts/logos/metrics. Uses existing
.reveal system (new SELECTORS entries, 70ms chip cascade; never pre-classed in
markup — POLISH_JS adds the class). Hover fills yellow #FFCE1B; reduced-motion
safe; <=760px tighter flow, <=380px two-column; fits to 360px with zero
overflow. QA: 0 errors on all 5 viewports, edge-to-edge gaps 0 with
neighbouring sections, reveal one-shot and sticky, qa_v5.py GREEN; full-page
captures regenerated (desktop 1440x13803, mobile 780x32640).
