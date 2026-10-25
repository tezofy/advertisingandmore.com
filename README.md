# Party Services & Rentals — Landing Page

A production-ready, single-page marketing site for **Advertising & More**'s Party
Services & Rentals catalogue. The page is a fully static, dependency-free build
(plain HTML/CSS/JavaScript) styled to match the native `advertisingandmore.com`
brand system — warm, bold and playful, with the agency's navy/gold palette,
"Click For Coffee" CTAs, and the Listen → Plan → Execute → Deliver → Celebrate
voice.

## ✨ Highlights

- **Self-contained static site** — open `index.html` and it works. No framework,
  no runtime dependencies, no build step required to preview or deploy.
- **170 externalized WebP images** (plus 8 brand/testimonial PNGs) — zero inline
  base64/data URIs in the shipped HTML, so the page stays cache-friendly and light
  (~1.7 MB HTML + ~8 MB of optimised image assets).
- **Native A&M brand experience** — hero, agency stats with explicit agency-wide
  disclaimers, featured-experiences mosaic with equal-height tiles, Richard Branson
  quote block, Why-Choose cards, party recipes with wishlist, Top 15 crowd
  favourites (photo-header cards, 3-per-row grid), the "Pick your WOW" category
  band that deep-links into the full services inventory (placed directly above it),
  process timeline, FAQ, testimonials with the client logo above each quote,
  contact form, pre-footer plan band and footer.
- **Conversion architecture** — four "CLICK FOR COFFEE" brand pills plus in-content
  "Request a Quote" CTAs; a two-column pre-footer plan band carrying the real,
  verbatim Dentsu client review.
- **Trust & compliance first** — only the four client-published reviews from the
  parent site, quoted **verbatim** with real logos; no fabricated testimonials,
  ratings or metrics; no `AggregateRating`/`reviewRating` schema; contact-form
  consent checkboxes are opt-in (unchecked by default).
- **Accessible motion** — a shared scroll-reveal system (one-shot, stays visible)
  with full `prefers-reduced-motion` support.
- **Responsive & QA-verified** — tested at 1440, 1024, 768, 390 and 360 px with
  zero console/network errors, no horizontal overflow and no element overlap.
- **SEO-ready** — semantic landmarks, FAQ JSON-LD, Open Graph tags and descriptive
  alt text.

## 🗂 Repository layout

```
party-services-rentals-site/
├── index.html                # Shippable page (built artifact, ready to deploy)
├── assets/
│   ├── img/                  # 170 WebP photos + 4 testimonial PNGs
│   └── brand/                # Client-published brand logos (LinkedIn, Bosch, UMG, Dentsu)
├── build-fragments/          # Reusable section fragments consumed by the pipeline
│   ├── wow-band.html
│   ├── featured-experiences.html
│   ├── party-recipes.html
│   ├── trusted-compact.css
│   └── brand-alignment.css
├── build_top15.py            # Python build pipeline (source → index.html)
├── capture_full.py           # Full-page screenshot utility (Playwright)
└── docs/
    ├── AUDIT-v5-native-brand-rebuild.md   # Full design/QA audit log (Bengali)
    ├── HANDOFF-v3.36-audit-closure.md     # Engineering handoff & changelog (English)
    └── github-description.md              # Short repo description draft
```

## 🚀 Quick start

No installation is needed to run the site itself.

**Option A — open directly**

```bash
# Just open the file in any modern browser
open index.html          # macOS
xdg-open index.html      # Linux
```

**Option B — local web server (recommended, matches production paths)**

```bash
python3 -m http.server 8080
# then visit http://localhost:8080
```

**Option C — GitHub Pages**

Push this repository to a repo named `advertisingandmore.com`, then enable
**Settings → Pages → Deploy from branch (root)**. The entry point is
named `index.html`, every asset uses a relative path and the package ships a
`.nojekyll` file, so the site serves correctly at the project subpath
`https://tezofy.github.io/advertisingandmore.com/` with no extra configuration.
Step-by-step instructions (UI and git) live in `DEPLOY-GITHUB-PAGES.md`.

## 🛠 Rebuilding from source (optional)

The committed `index.html` is the complete built artifact, so rebuilding is only
needed when editing section fragments. The pipeline is plain Python:

```bash
pip install pillow playwright
python3 build_top15.py
```

`build_top15.py` reads a client-owned source template and normalized icon set that
are **not redistributed in this repository** (they remain in the agency's private
workspace). It:

1. injects the section fragments from `build-fragments/`,
2. renders the Top 15 grid from the live catalogue data,
3. externalizes every embedded image into `assets/img/*.webp`, and
4. writes the final standalone HTML.

To regenerate full-page screenshots after a layout change:

```bash
python3 -m playwright install chromium
python3 capture_full.py
```

## 🖼 Assets & licensing

All imagery and logos are client-owned marketing assets sourced from
`advertisingandmore.com` and the project's original uploads. They are included
here for deployment of this client project only and must not be reused in
unrelated work without the rights holder's permission. Testimonial logos
(LinkedIn, Bosch, Universal Music Group, Dentsu) are the clients' own published
marks and are used solely to attribute their verbatim reviews.

## 🛡 Trust & compliance notes

- Testimonial copy is reproduced **verbatim** from the parent site; nothing is
  paraphrased and no review is invented.
- The four agency statistics are explicitly labelled as agency-wide figures
  published on `advertisingandmore.com` — not endorsements of the party services.
- The success seal renders the exact text **"100% SUCCESS RATE"** as supplied.
- No anonymous reviews, no fake ratings, and no review/rating structured data.
- Contact-form consent checkboxes default to unchecked (opt-in), per
  FTC guidance (16 CFR Part 465) and standard privacy practice.

## ✅ Browser & QA coverage

| Viewport | Width × height | Result |
|---|---|---|
| Desktop | 1440 × 900 | ✅ 0 errors |
| Laptop | 1024 × 768 | ✅ 0 errors |
| Tablet | 768 × 1024 | ✅ 0 errors |
| Mobile | 390 × 844 | ✅ 0 errors |
| Small mobile | 360 × 740 | ✅ 0 errors |

Checks cover console/network errors, horizontal overflow, element overlap,
scroll-reveal behaviour (fires once, remains visible), hover states, opt-in
consent defaults and image decoding.

## 📚 Further reading

See `docs/AUDIT-v5-native-brand-rebuild.md` for the full design rationale and
version-by-version QA record (Bengali), and
`docs/HANDOFF-v3.36-audit-closure.md` for the engineering handoff and changelog
(English), including the v5.1 plan band, v5.3 marquee rebuild and v5.4
photo-card / layout refinements.

---

*Built for Advertising & More — Integrated Agency. Questions:
hello@advertisingandmore.com*
