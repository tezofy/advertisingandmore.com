# -*- coding: utf-8 -*-
"""
v3.27 — Top 15 Crowd Favourites section for party-services-rentals (17).html
Inserts:
  Block A (CSS + static section shell) before the OUR SERVICES section
  Block B (renderer IIFE) before </body>
Cards are rendered at runtime from the EXISTING catalogData (real images/specs),
and reuse the existing window.toggleWishlist / syncWishlistButtons system.
"""
import base64
import json
import os
import re
import shutil

SRC = "/home/user/uploads/party-services-rentals (17).html"
OUT = "/home/user/party-services-rentals-top15.html"
ICON_DIR = "/home/user/ai-icons/normalized"

# v4.x client-update fragments ported from "party-services-rentals-top15 (20) (6).html"
# (WOW band, party recipes, featured experiences + compact trust strip + deck CSS).
# Extracted verbatim into build-fragments/; data URIs are externalized at build end.
FRAG_DIR = "/home/user/build-fragments"


def _frag(name):
    with open(os.path.join(FRAG_DIR, name), "r", encoding="utf-8") as fh:
        return fh.read()


FRAG_WOW = _frag("wow-band.html")
FRAG_RECIPES = _frag("party-recipes.html")
FRAG_FEATURED = _frag("featured-experiences.html")
# v5.4 — occasion strip removed at client request (no replacement block)
FRAG_TRUST_COMPACT = _frag("trusted-compact.css")
FRAG_BRAND_ALIGN = _frag("brand-alignment.css")

# ============================================================================
# v5 — parent-site native blocks (advertisingandmore.com brand system)
# ============================================================================

# Agency-wide stats + the two protective footnotes the client's own mockup
# (IMG_2043) places beside the trust strip. Figures are agency-wide, exactly as
# published on advertisingandmore.com — never presented as party-page metrics.
BLOCK_STATS = '''
  <section class="am-stats" id="am-stats" aria-label="Advertising and More at a glance">
    <p class="am-stats__logo-note">Brand imagery reflects the original agency website, not endorsements of new party services.</p>
    <div class="am-stats__grid">
      <div class="am-stat">
        <span class="am-stat__ic" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
        </span>
        <div class="am-stat__num">12<span class="am-stat__plus">+</span></div>
        <div class="am-stat__lbl">Years of bold, creative advertising</div>
      </div>
      <div class="am-stat">
        <span class="am-stat__ic" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 2.5 15.3 0 18M12 3c-2.5 2.7-2.5 15.3 0 18"/></svg>
        </span>
        <div class="am-stat__num">150<span class="am-stat__plus">+</span></div>
        <div class="am-stat__lbl">Countries reached worldwide</div>
      </div>
      <div class="am-stat">
        <span class="am-stat__ic" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>
        </span>
        <div class="am-stat__num">98<span class="am-stat__plus">%</span></div>
        <div class="am-stat__lbl">Clients return to us</div>
      </div>
      <div class="am-stat">
        <span class="am-stat__ic" aria-hint="true" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg>
        </span>
        <div class="am-stat__num">100<span class="am-stat__plus">%</span></div>
        <div class="am-stat__lbl">Project success rate</div>
      </div>
    </div>
    <p class="am-stats__note">Agency-wide figures published on advertisingandmore.com</p>
  </section>

  <style id="am-stats-css">
    .am-stats { max-width: 1180px; margin: 0 auto; padding: 26px 24px 10px; text-align: center; }
    .am-stats__logo-note {
      font-size: 0.72rem; line-height: 1.55; color: var(--color-text-light);
      max-width: 720px; margin: 0 auto 22px; font-style: italic;
    }
    .am-stats__grid {
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px;
    }
    .am-stat {
      background: rgba(255, 255, 255, 0.62); border: 1px solid var(--color-border);
      border-radius: 18px; padding: 24px 16px 20px;
      display: flex; flex-direction: column; align-items: center; gap: 8px;
      transition: transform .35s ease, box-shadow .35s ease;
    }
    .am-stat:hover { transform: translateY(-4px); box-shadow: 0 14px 30px rgba(11, 30, 63, .10); }
    .am-stat__ic {
      width: 46px; height: 46px; border-radius: 50%;
      background: rgba(0, 73, 168, .08); color: var(--color-primary);
      display: flex; align-items: center; justify-content: center; margin-bottom: 4px;
    }
    .am-stat__ic svg { width: 24px; height: 24px; }
    .am-stat__num {
      font-family: "Fraunces", Georgia, serif; font-weight: 700;
      font-size: 2.35rem; line-height: 1; color: var(--color-text-dark);
    }
    .am-stat__plus { color: var(--color-accent-gold-hover); }
    .am-stat__lbl {
      font-size: 0.82rem; font-weight: 600; letter-spacing: .04em;
      text-transform: uppercase; color: var(--color-text-muted); line-height: 1.45;
    }
    .am-stats__note {
      font-size: 0.74rem; color: var(--color-text-light); margin: 18px auto 0;
    }
    @media (max-width: 900px) {
      .am-stats__grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
    }
    @media (max-width: 480px) {
      .am-stats { padding: 18px 16px 6px; }
      .am-stat { padding: 18px 10px 14px; }
      .am-stat__num { font-size: 1.9rem; }
      .am-stat__lbl { font-size: 0.72rem; }
    }
  </style>
'''

# Sir Richard Branson quote — verbatim from the live advertisingandmore.com
# "The people" section. Reusing the parent site's own quote makes the sub-page
# read as a native chapter of the same brand.
BLOCK_QUOTE = '''
  <section class="am-quote" aria-label="Richard Branson on aiming for amazing">
    <div class="am-quote__card">
      <span class="am-quote__mark" aria-hidden="true">&ldquo;</span>
      <blockquote class="am-quote__text">
        Don&rsquo;t think what&rsquo;s the cheapest way to do it or what&rsquo;s the fastest way to do it.
        Think, what&rsquo;s the most amazing way to do it?
      </blockquote>
      <div class="am-quote__by">Sir Richard Branson</div>
      <div class="am-quote__role">As featured on advertisingandmore.com</div>
    </div>
  </section>

  <style id="am-quote-css">
    .am-quote { max-width: 980px; margin: 0 auto; padding: 30px 24px 8px; }
    .am-quote__card {
      position: relative; background: #FFFFFF; border: 1px solid var(--color-border);
      border-radius: 22px; padding: 44px 48px 38px; text-align: center;
      box-shadow: 0 10px 28px rgba(11, 30, 63, .06);
    }
    .am-quote__mark {
      position: absolute; top: 6px; left: 34px;
      font-family: "Fraunces", Georgia, serif; font-size: 5.2rem; line-height: 1;
      color: var(--color-accent-gold); opacity: .85;
    }
    .am-quote__text {
      margin: 0; font-family: "Fraunces", Georgia, serif;
      font-size: 1.32rem; line-height: 1.7; font-style: italic;
      color: var(--color-text-dark);
    }
    .am-quote__by {
      margin-top: 20px; font-weight: 700; font-size: 1.02rem;
      color: var(--color-primary); letter-spacing: .02em;
    }
    .am-quote__role { margin-top: 4px; font-size: 0.8rem; color: var(--color-text-light); }
    @media (max-width: 640px) {
      .am-quote__card { padding: 34px 22px 28px; }
      .am-quote__mark { font-size: 3.6rem; left: 18px; }
      .am-quote__text { font-size: 1.06rem; }
    }
  </style>
'''

# ============================================================================
# v5.1 — pre-footer plan band (sits directly above the navy footer)
# Left: the 4th REAL parent-published testimonial (Dentsu, verbatim, logo).
# Right: conversion nudge with the tier-2 "Request a Quote" label, in the
# page's existing gold-pill system, plus a blue party-popper doodle.
# Both columns ride the shared .reveal float-up system in POLISH_JS.
# ============================================================================
BLOCK_PLAN = '''
  <section class="plan-band" id="plan-band" aria-labelledby="plan-band-heading">
    <div class="container">
      <div class="plan-card">
        <div class="plan-col plan-quote">
          <span class="plan-quote__mark" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="currentColor"><path d="M9.4 6C5.6 8.7 3 12.6 3 17.2 3 21.1 5.4 24 9 24c2.6 0 4.5-1.9 4.5-4.4 0-2.4-1.7-4.2-4-4.2-.4 0-.9.1-1 .1.3-2.3 2.1-4.6 4.4-6.1L9.4 6zm13 0c-3.8 2.7-6.4 6.6-6.4 11.2 0 3.9 2.4 6.8 6 6.8 2.6 0 4.5-1.9 4.5-4.4 0-2.4-1.7-4.2-4-4.2-.4 0-.9.1-1 .1.3-2.3 2.1-4.6 4.4-6.1L22.4 6z"/></svg>
          </span>
          <blockquote class="plan-quote__text">&ldquo;Fine staff who has performed outstandingly on all our campaigns. A real asset that gives your company an edge over the competition. Keep up the good work!&rdquo;</blockquote>
          <div class="plan-quote__who">
            <img class="ts-logo plan-quote__logo" src="assets/img/testi-dentsu.png" alt="Dentsu logo" width="120" height="32" loading="lazy">
            <div class="plan-quote__meta">
              <div class="plan-quote__name">Dentsu</div>
              <div class="plan-quote__role">Associate Digital Director</div>
            </div>
          </div>
        </div>
        <div class="plan-col plan-cta">
          <span class="plan-cta__doodle" aria-hidden="true">
            <svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
              <!-- party popper cone, opening toward top-right -->
              <path d="M10 52 30 28 40 36 18 58 Z"/>
              <path d="M30 28 40 36"/>
              <!-- burst rays out of the opening -->
              <path d="M40 30 50 14"/>
              <path d="M46 36 60 30"/>
              <path d="M42 42 52 50"/>
              <!-- confetti: sparkles and dots -->
              <path d="M54 8l1.5 3.5L59 13l-3.5 1.5L54 18l-1.5-3.5L49 13l3.5-1.5z"/>
              <path d="M58 40l1 2.4 2.4 1-2.4 1-1 2.4-1-2.4-2.4-1 2.4-1z"/>
              <circle cx="48" cy="10" r="2.2" fill="currentColor" stroke="none"/>
              <circle cx="60" cy="22" r="1.9" fill="currentColor" stroke="none"/>
              <circle cx="50" cy="56" r="2" fill="currentColor" stroke="none"/>
            </svg>
          </span>
          <p class="plan-cta__eyebrow">Ready when you are</p>
          <h2 class="plan-cta__title" id="plan-band-heading">Let&rsquo;s plan your <span class="text-gold">event.</span></h2>
          <p class="plan-cta__sub">Tell us what you&rsquo;re celebrating, and we&rsquo;ll create a custom party experience just for you.</p>
          <a class="plan-cta__btn" href="#contact">
            Request a Quote
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a>
        </div>
      </div>
    </div>
  </section>

  <style id="plan-band-css">
    .plan-band { padding: clamp(24px, 4vw, 48px) 0 clamp(28px, 4vw, 56px); }
    /* v5.4 — card chrome removed: the "Ready when you are" band now sits
       directly on the shared cream page (transparent, no border/shadow) */
    .plan-card {
      max-width: 1180px; margin: 0 auto;
      background: transparent;
      border: 0;
      border-radius: 24px;
      box-shadow: none;
      display: grid;
      grid-template-columns: 1.12fr 1fr;
      overflow: hidden;
    }
    .plan-col { padding: clamp(28px, 3.4vw, 46px); }
    .plan-quote { position: relative; }
    .plan-quote__mark {
      display: inline-flex; color: var(--color-accent-gold);
      width: 34px; height: 34px; margin-bottom: 10px;
    }
    .plan-quote__mark svg { width: 100%; height: 100%; }
    .plan-quote__text {
      margin: 0 0 22px;
      font-family: "Fraunces", Georgia, serif;
      font-style: italic;
      font-size: clamp(1.02rem, 1.35vw, 1.22rem);
      line-height: 1.7;
      color: var(--color-text-dark);
    }
    .plan-quote__who { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
    .plan-quote__logo {
      width: 128px; max-height: 52px; margin: 0;
      padding: 10px 14px;
    }
    .plan-quote__name { font-weight: 700; color: var(--color-primary-dark); font-size: .98rem; }
    .plan-quote__role { font-size: .82rem; color: var(--color-text-muted); margin-top: 2px; }
    .plan-cta {
      position: relative;
      border-left: 1px solid var(--color-border);
      display: flex; flex-direction: column; justify-content: center;
      text-align: left;
    }
    .plan-cta__doodle {
      position: absolute; top: 22px; right: 26px;
      width: 62px; height: 62px; color: var(--color-primary);
      animation: planDoodleFloat 3.6s ease-in-out infinite;
      pointer-events: none;
    }
    @keyframes planDoodleFloat {
      0%, 100% { transform: translateY(0) rotate(-4deg); }
      50% { transform: translateY(-7px) rotate(4deg); }
    }
    .plan-cta__eyebrow {
      margin: 0 0 8px;
      font-size: .76rem; font-weight: 700; letter-spacing: .14em;
      text-transform: uppercase; color: #C2633F;
    }
    .plan-cta__title {
      margin: 0 0 10px;
      font-family: "Fraunces", Georgia, serif;
      font-size: clamp(1.55rem, 2.6vw, 2.1rem);
      line-height: 1.18; font-weight: 700;
      color: var(--color-text-dark);
    }
    .plan-cta__sub {
      margin: 0 0 24px; max-width: 420px;
      font-size: .96rem; line-height: 1.65; color: var(--color-text-muted);
    }
    .plan-cta__btn {
      align-self: flex-start;
      display: inline-flex; align-items: center; gap: 10px;
      padding: 15px 30px; border-radius: 999px;
      background: linear-gradient(180deg, #FFD84D, #F0BE1F);
      color: #0049A8; font-weight: 800; font-size: .98rem;
      text-decoration: none; white-space: nowrap;
      box-shadow: 0 14px 30px rgba(240, 190, 31, .35);
      transition: transform .3s cubic-bezier(.22,.61,.36,1), box-shadow .3s ease;
    }
    .plan-cta__btn:hover { transform: translateY(-3px); box-shadow: 0 20px 38px rgba(240, 190, 31, .45); }
    .plan-cta__btn svg { width: 18px; height: 18px; }
    @media (max-width: 860px) {
      .plan-card { grid-template-columns: 1fr; }
      .plan-cta {
        border-left: 0; border-top: 1px solid var(--color-border);
        text-align: center; align-items: center;
      }
      .plan-cta__sub { margin-inline: auto; }
      .plan-cta__btn { align-self: center; }
      .plan-quote__who { justify-content: center; }
    }
    @media (max-width: 640px) {
      .plan-band { padding: 18px 0 26px; }
      .plan-col { padding: 24px 20px; }
      .plan-quote__mark { width: 28px; height: 28px; margin-bottom: 6px; }
      .plan-quote__text { font-size: .98rem; line-height: 1.62; margin-bottom: 18px; }
      .plan-quote__logo { width: 108px; padding: 8px 12px; }
      .plan-cta__doodle { width: 46px; height: 46px; top: 16px; right: 18px; }
      .plan-cta__eyebrow { font-size: .7rem; }
      .plan-cta__title { font-size: 1.45rem; }
      .plan-cta__sub { font-size: .9rem; margin-bottom: 20px; }
      .plan-cta__btn { width: 100%; justify-content: center; padding: 14px 22px; font-size: .94rem; }
    }
    @media (prefers-reduced-motion: reduce) {
      .plan-cta__doodle { animation: none; }
    }
  </style>
'''

# One uniform AI-generated badge set (blue/gold/cream), embedded as data URIs.
ICON_URIS = {}
for _i in range(1, 11):
    with open(os.path.join(ICON_DIR, f"cat-{_i}.png"), "rb") as _fh:
        ICON_URIS[f"cat-{_i}"] = "data:image/png;base64," + base64.b64encode(_fh.read()).decode("ascii")

# AI-generated branding badges for the Why Choose (x4) and Our Process (x5)
# sections — same normalized badge set (cream disc, gold ring, blue/gold 3D).
BRAND_ICON_DIR = "/home/user/ai-icons/brand/normalized"
BRAND_ICONS = {}
for _n in [f"wc-{_i}" for _i in range(1, 5)] + [f"op-{_i}" for _i in range(1, 6)]:
    with open(os.path.join(BRAND_ICON_DIR, _n + ".png"), "rb") as _fh:
        BRAND_ICONS[_n] = "data:image/png;base64," + base64.b64encode(_fh.read()).decode("ascii")

# rank -> (catalog key, type, curated marketing hook)
CURATED = [
    ("chatgpt_11",  "Rental",     "The classic midway rebooted for grownups, with high-stakes prizes and carnival nostalgia."),
    ("chatgpt_4",   "Experience", "The ultimate ballroom crowd-pleaser that gets CEOs and managers cheering on their feet."),
    ("chatgpt_41",  "Rental",     "Three switchable DJ channels, glowing headphones and zero noise-curfew complaints from the hotel."),
    ("chatgpt_72",  "Experience", "Force-feedback steering and triple screens for genuine lap-time bragging rights."),
    ("chatgpt_21",  "Experience", "A slow-motion rotating glam platform tailored for viral LinkedIn and Instagram reels."),
    ("chatgpt_64",  "Experience", "A hidden entrance opens into an intimate luxury cocktail haven inside the foyer."),
    ("chatgpt_3",   "Rental",     "Oversized padded gloves and comedy grudge matches that bring pure hilarity."),
    ("chatgpt_9",   "Rental",     "Fast-twitch reflex competition that draws a perpetual queue of eager challengers."),
    ("chatgpt_19",  "Rental",     "Blackjack, roulette and poker with custom branded fun-money chips and professional croupiers."),
    ("chatgpt_31",  "Experience", "Tower-high illuminated robots that turn every grand entrance into a photo moment."),
    ("chatgpt_51",  "Experience", "Flair bartenders shaking theatre-level cocktails that guests queue to photograph."),
    ("chatgpt_83",  "Experience", "Glitter, gems and glow stations that keep the dance floor sparkling all night."),
    ("chatgpt_93",  "Experience", "Guests dive into a flying-cash machine for the most photographed 20 seconds of the night."),
    ("chatgpt_22",  "Experience", "Studio lighting, props and instant prints that empty straight onto social feeds."),
    ("chatgpt_42",  "Rental",     "A glowing reactive dance floor that pulls guests out of their chairs and onto the tiles."),
]

# ---------------------------------------------------------------- CSS + shell
BLOCK_A = '''
  <!-- ==========================================================================
       v3.27 — TOP 15 CROWD FAVOURITES (curated "start here" band)
       Sits between the trusted-brands marquee and the full 100-item catalogue.
       Cards are rendered by the script at the end of <body> from catalogData.
       ========================================================================== -->
  <section class="t15-section" id="top15" aria-labelledby="t15-heading">
    <div class="container">
      <div class="section-header-center">
        <div class="hd-eyebrow">
          <span class="line"></span>
          <span>Our 15 Favourites</span>
        </div>
        <h2 class="heading-display" id="t15-heading">
          Start with the crowd <span class="text-gold">pleasers</span>
        </h2>
      </div>

      <div class="t15-grid" id="t15-grid">
        <!-- cards injected by top15 renderer -->
      </div>
    </div>
  </section>

  <style id="top15-crowd-favourites-css">
    .t15-section {
      position: relative;
      padding: clamp(3.25rem, 6.5vw, 5.25rem) 0 clamp(3rem, 6vw, 4.75rem);
      background:
        radial-gradient(900px 380px at 50% -120px, rgba(255, 206, 27, 0.16), transparent 72%),
        var(--color-bg-page);
      overflow: hidden;
    }
    .t15-section::before {
      content: "";
      position: absolute;
      inset: 0 0 auto 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(0, 73, 168, 0.18), transparent);
    }

    /* Header intentionally uses the site's shared .section-header-center /
       .hd-eyebrow / .heading-display classes so the title matches
       "Everything for your special events." 100% — same font, size,
       navy + #D4A000 gold colors and shape. No local overrides. */

    /* ---------- grid ---------- */
    .t15-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 22px;
    }

    /* ---------- card (v5.4: photo-header design, matching the WOW cards) -- */
    .t15-card {
      position: relative;
      display: flex;
      flex-direction: column;
      padding: 0;
      overflow: hidden;
      background: var(--color-bg-surface, #fff);
      border: 1px solid var(--color-border-card, rgba(0, 73, 168, .12));
      border-radius: 20px;
      box-shadow: 0 12px 30px rgba(11, 30, 63, 0.07);
      transition: transform .35s cubic-bezier(.22,.61,.36,1), box-shadow .35s ease, border-color .35s ease;
      opacity: 0;
      transform: translateY(26px);
    }
    .t15-grid.is-inview .t15-card {
      opacity: 1;
      transform: translateY(0);
      transition: opacity .55s ease, transform .55s cubic-bezier(.22,.61,.36,1), box-shadow .35s ease, border-color .35s ease;
    }
    .t15-card:hover {
      transform: translateY(-6px);
      border-color: rgba(255, 206, 27, .75);
      box-shadow: 0 22px 44px rgba(11, 30, 63, 0.14);
    }
    /* saved card gets a soft pink edge that matches the pink heart state */
    .t15-card:has(.t15-wish.is-active) {
      transform: translateY(-6px);
      border-color: rgba(245, 51, 138, 0.45);
      box-shadow: 0 22px 44px rgba(120, 18, 64, 0.13);
    }

    /* ---- photo header (v5.6: shorter 16/8.4 frame to cut card height) ---- */
    .t15-media {
      position: relative;
      aspect-ratio: 16 / 8.4;
      /* visible so the overlapping badge icon can break the photo edge;
         the card's own overflow:hidden + radius still clip the corners */
      overflow: visible;
      background: #0B1E3F;
    }
    /* absolute fill so the image can't inflate the aspect-ratio box:
       the media height is now driven purely by aspect-ratio (v5.6) */
    .t15-photo {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border-radius: 20px 20px 0 0;
      object-fit: cover;
      display: block;
      transition: transform .7s cubic-bezier(.16, 1, .3, 1);
    }
    .t15-photo--empty { background: linear-gradient(135deg, #10284f, #0B1E3F); }
    .t15-card:hover .t15-photo { transform: scale(1.06); }
    /* subtle readability scrim for the overlaid chips */
    .t15-media::after {
      content: "";
      position: absolute; inset: 0;
      background: linear-gradient(180deg, rgba(11,30,63,.28) 0%, rgba(11,30,63,0) 34%, rgba(11,30,63,0) 70%, rgba(11,30,63,.12) 100%);
      pointer-events: none;
    }
    .t15-rank-pill {
      position: absolute;
      z-index: 2;
      top: 12px;
      left: 12px;
      padding: 6px 12px;
      border-radius: 999px;
      background: linear-gradient(180deg, #FFD84D, #F0BE1F);
      color: var(--color-primary-dark);
      font-family: var(--font-body);
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 1.4px;
      box-shadow: 0 6px 14px rgba(11, 30, 63, .28);
    }
    .t15-pill-short { display: none; }
    /* mobile-only faint serial, overlaid on the photo (no pill ≤640px) */
    .t15-rank-ghost {
      display: none;
      position: absolute;
      z-index: 2;
      top: 10px;
      left: 14px;
      font-family: var(--font-display);
      font-size: 1.9rem;
      font-weight: 700;
      line-height: 1;
      color: rgba(255, 255, 255, .92);
      text-shadow: 0 2px 10px rgba(11, 30, 63, .55);
      pointer-events: none;
      user-select: none;
    }
    /* type chip rides the photo's top-right corner */
    .t15-media .t15-type {
      position: absolute;
      z-index: 2;
      top: 12px;
      right: 12px;
      padding: 5px 11px;
      border-radius: 999px;
      font-family: var(--font-body);
      font-size: 9px;
      font-weight: 800;
      letter-spacing: 1.4px;
      color: #fff;
      background: rgba(11, 30, 63, .62);
      border: 1px solid rgba(255, 255, 255, .28);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
    }
    .t15-media .t15-type--rental { color: #FFE4A8; background: rgba(120, 84, 8, .55); border-color: rgba(255, 206, 27, .45); }

    /* AI-generated circular badge icon — overlaps the photo's bottom-left */
    .t15-icon {
      position: absolute;
      z-index: 3;
      left: 20px;
      bottom: -20px;
      width: 54px;
      height: 54px;
      border-radius: 50%;
      background: #fff;
      padding: 4px;
      box-shadow: 0 10px 22px rgba(11, 30, 63, .22);
    }
    .t15-icon img {
      width: 100%;
      height: 100%;
      display: block;
      border-radius: 50%;
      transition: transform .35s ease;
    }
    .t15-card:hover .t15-icon img { transform: scale(1.07) rotate(-3deg); }

    /* ---- text body (v5.6: compact rhythm) ---- */
    .t15-body {
      display: flex;
      flex-direction: column;
      flex: 1 1 auto;
      padding: 30px 20px 16px;
    }

    /* type chip now lives on the photo header; meta row holds category only */
    .t15-meta {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px 10px;
      margin-bottom: 5px;
    }
    .t15-cat {
      font-family: var(--font-body);
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.1px;
      color: var(--color-gold-text, #A16D12);
    }

    .t15-title {
      margin: 0 0 5px;
      position: relative;
      font-family: var(--font-display);
      font-size: 1.12rem;
      font-weight: 700;
      line-height: 1.25;
      color: var(--color-primary-dark);
      /* reserve two lines so one- and two-line titles keep every card equal height */
      min-height: 2.5em;
      display: flex;
      align-items: center;
    }
    /* v5.4 — hook is a plain marketing description, no quotation marks.
       v5.6 — capped at three lines so every card stays the same compact height */
    .t15-quote {
      margin: 0 0 10px;
      font-family: var(--font-body);
      font-style: normal;
      font-size: .86rem;
      line-height: 1.5;
      color: var(--color-text-body);
      flex-grow: 1;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
      /* reserve three lines so all 15 cards share one compact height */
      min-height: 4.5em;
    }

    /* ---------- footer: specs + wishlist ---------- */
    .t15-divider { height: 1px; background: var(--color-border, #E2E8F0); margin: 0 0 10px; }
    .t15-footer { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    .t15-specs-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 8px 4px;
      background: none;
      border: 0;
      cursor: pointer;
      font-family: var(--font-body);
      font-size: 13px;
      font-weight: 600;
      color: var(--color-primary);
    }
    .t15-specs-btn svg { width: 16px; height: 16px; flex: 0 0 auto; }
    .t15-specs-btn .t15-chevron { transition: transform .3s ease; }
    .t15-specs-btn[aria-expanded="true"] .t15-chevron { transform: rotate(180deg); }
    .t15-specs-btn:hover, .t15-specs-btn:focus-visible { text-decoration: underline; text-underline-offset: 3px; outline: none; }

    .t15-specs-panel {
      max-height: 0;
      overflow: hidden;
      transition: max-height .4s ease;
    }
    .t15-specs-panel ul {
      list-style: none;
      margin: 12px 0 4px;
      padding: 14px 14px 12px;
      border-radius: 14px;
      background: var(--color-cream-light, #FBF8F2);
      border: 1px solid var(--color-border, #E2E8F0);
      display: grid;
      gap: 9px;
    }
    .t15-specs-panel li {
      display: flex;
      gap: 9px;
      align-items: flex-start;
      font-family: var(--font-body);
      font-size: 12.5px;
      line-height: 1.5;
      color: var(--color-text-body);
    }
    .t15-specs-panel li svg { width: 15px; height: 15px; flex: 0 0 auto; margin-top: 2px; stroke: var(--color-accent-gold-hover, #D5A021); }

    /* Three-state wish button: plus (idle) -> gold check (brief) -> pink heart (saved) */
    .t15-wish {
      position: relative;
      width: 42px;
      height: 42px;
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      /* idle state: brand-gold filled circle; the plus itself stays blue */
      background: linear-gradient(180deg, #FFD84D, #F0BE1F);
      border: 1.6px solid #E8B915;
      box-shadow: 0 8px 18px rgba(213, 160, 33, .35);
      cursor: pointer;
      transition: transform .25s ease, background .3s ease, border-color .3s ease, box-shadow .3s ease;
    }
    .t15-wish svg {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      margin: auto;
      width: 20px;
      height: 20px;
      transition: opacity .22s ease, transform .3s cubic-bezier(.34, 1.56, .64, 1);
    }
    .t15-ico-plus { stroke: var(--color-primary, #0049A8); opacity: 1; transform: scale(1); }
    .t15-ico-check, .t15-ico-heart { opacity: 0; transform: scale(.4); }
    .t15-ico-check { stroke: #fff; }
    .t15-ico-heart { fill: #fff; stroke: none; }
    .t15-wish:hover { transform: scale(1.08); border-color: var(--color-accent-gold-hover, #D5A021); }

    /* phase 2 — final pink heart (matches the site's #FF3E8C wishlist pink) */
    .t15-wish.is-active {
      background: linear-gradient(180deg, #FF5FA2, #F5338A);
      border-color: #F5338A;
      box-shadow: 0 10px 24px rgba(245, 51, 138, .42);
    }
    .t15-wish.is-active .t15-ico-plus { opacity: 0; transform: scale(.4); }
    .t15-wish.is-active .t15-ico-heart { opacity: 1; transform: scale(1); }
    .t15-wish.is-active .t15-ico-check { opacity: 0; transform: scale(.4); }
    .t15-wish.is-active:hover { border-color: #F5338A; }

    /* phase 1 — gold check, declared LAST so it wins while both classes
       (is-active + is-checking) are present during the brief transition */
    .t15-wish.is-checking {
      background: linear-gradient(180deg, #FFD84D, #E8B915);
      border-color: #E8B915;
      box-shadow: 0 10px 22px rgba(213, 160, 33, .42);
    }
    .t15-wish.is-checking .t15-ico-plus { opacity: 0; transform: scale(.4); }
    .t15-wish.is-checking .t15-ico-check { opacity: 1; transform: scale(1); }
    .t15-wish.is-checking .t15-ico-heart { opacity: 0; transform: scale(.4); }

    /* flying AI badge icon on its way to the wishlist tray */
    .t15-fly-icon {
      position: fixed;
      z-index: 2600;
      pointer-events: none;
      border-radius: 50%;
      transform: translate(-50%, -50%);
      will-change: transform, opacity;
      box-shadow: 0 12px 26px rgba(11, 30, 63, .28);
    }
    .t15-fly-icon img { width: 100%; height: 100%; display: block; border-radius: 50%; }

    /* landing pop when a badge flies back to its card */
    @keyframes t15IconPop {
      0%   { transform: scale(1); }
      42%  { transform: scale(1.24) rotate(-5deg); }
      100% { transform: scale(1); }
    }
    .t15-icon img.t15-land-pop { animation: t15IconPop .48s cubic-bezier(.34, 1.56, .64, 1); }

    /* landing pop for the main-catalog wishlist button (reverse flight) */
    @keyframes hpBtnLand {
      0%   { transform: scale(1); }
      42%  { transform: scale(1.18); }
      100% { transform: scale(1); }
    }
    .wishlist-btn.hp-btn-land { animation: hpBtnLand .5s cubic-bezier(.34, 1.56, .64, 1); }

    /* ---- anchored mini wishlist sheet: slides in under the clicked button,
       shows the item TITLE only, then slides back down and fades away ---- */
    .wish-mini-sheet {
      position: fixed;
      z-index: 2700;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      max-width: 240px;
      padding: 9px 14px;
      background: #fff;
      border: 1px solid rgba(11, 30, 63, .12);
      border-radius: 12px;
      box-shadow: 0 14px 32px rgba(11, 30, 63, .22);
      font-family: var(--font-body);
      font-size: 12.5px;
      font-weight: 600;
      line-height: 1.35;
      color: var(--color-primary-dark);
      pointer-events: none;
      will-change: transform, opacity;
    }
    .wish-mini-sheet .wms-heart { width: 15px; height: 15px; flex: 0 0 auto; }
    .wish-mini-sheet.is-add .wms-heart { fill: #F5338A; stroke: #F5338A; }
    .wish-mini-sheet.is-remove .wms-heart {
      fill: none; stroke: var(--color-text-muted); stroke-width: 2.2;
    }
    .wish-mini-sheet .wms-title {
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }
    .wish-mini-sheet .wms-caret {
      position: absolute;
      top: -6px;
      width: 12px;
      height: 12px;
      background: #fff;
      border-left: 1px solid rgba(11, 30, 63, .12);
      border-top: 1px solid rgba(11, 30, 63, .12);
      border-radius: 2px;
      transform: rotate(45deg);
    }
    .wish-mini-sheet.is-above .wms-caret {
      top: auto;
      bottom: -6px;
      border-left: 0;
      border-top: 0;
      border-right: 1px solid rgba(11, 30, 63, .12);
      border-bottom: 1px solid rgba(11, 30, 63, .12);
    }
    @media (max-width: 640px) {
      .wish-mini-sheet { max-width: min(200px, 62vw); font-size: 11.5px; padding: 8px 12px; }
    }
    @media (prefers-reduced-motion: reduce) {
      .wish-mini-sheet { will-change: opacity; }
    }

    /* ---------- responsive: always 3 cards per row ---------- */
    @media (max-width: 1024px) {
      .t15-grid { gap: 16px; }
      .t15-body { padding: 28px 16px 14px; }
      .t15-icon { left: 14px; bottom: -18px; width: 50px; height: 50px; }
    }
    @media (max-width: 640px) {
      .t15-grid { gap: 10px; }
      .t15-card { border-radius: 14px; }
      .t15-media { aspect-ratio: 16 / 8.6; }
      /* overlapping badge stays proportional on phones */
      .t15-icon { left: 11px; bottom: -15px; width: 38px; height: 38px; padding: 4px; }
      /* contract: no rank pill ≤640px — a faint white serial sits on the
         photo instead, so cards keep their order without a yellow chip */
      .t15-rank-pill { display: none; }
      .t15-rank-ghost { display: block; top: 9px; left: 12px; font-size: 1.5rem; }
      .t15-media .t15-type { top: 10px; right: 10px; padding: 4px 8px; font-size: 7.5px; letter-spacing: 1px; }
      .t15-body { padding: 22px 11px 10px; }
      .t15-meta { gap: 4px 6px; margin-bottom: 6px; }
      .t15-cat { font-size: 9px; letter-spacing: .8px; }
      .t15-title { font-size: .82rem; margin-bottom: 6px; }
      .t15-quote {
        font-size: .68rem; line-height: 1.45; margin-bottom: 8px; min-height: 2.9em;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
      }
      .t15-divider { margin: 0 0 8px; }
      .t15-footer { gap: 6px; }
      .t15-specs-btn { font-size: 10px; gap: 4px; padding: 6px 0; }
      .t15-specs-btn svg { width: 13px; height: 13px; }
      .t15-specs-label { display: none; }
      .t15-specs-panel ul { padding: 9px; gap: 6px; }
      .t15-specs-panel li { font-size: 10.5px; }
      .t15-wish { width: 36px; height: 36px; }
      .t15-wish svg { width: 16px; height: 16px; }
    }
    @media (max-width: 380px) {
      .t15-icon { width: 34px; height: 34px; }
      .t15-rank-ghost { font-size: 1.25rem; }
      .t15-title { font-size: .76rem; }
      .t15-quote { -webkit-line-clamp: 1; font-size: .62rem; min-height: 1.5em; }
      .t15-wish { width: 32px; height: 32px; }
    }
    @media (prefers-reduced-motion: reduce) {
      .t15-card, .t15-grid.is-inview .t15-card { opacity: 1; transform: none; transition: none; }
      .t15-card:hover, .t15-card:has(.t15-wish.is-active) { transform: none; }
      .t15-fly-icon { display: none !important; }
      .t15-icon img.t15-land-pop, .wishlist-btn.hp-btn-land { animation: none !important; }
      .t15-specs-panel { transition: none; }
      .t15-icon img, .t15-wish { transition: none; }
    }
  </style>

'''

# ---------------------------------------------------------------- renderer JS
BLOCK_B = r'''
  <!-- v3.27 — Top 15 Crowd Favourites renderer (uses catalogData + shared wishlist) -->
  <script>
  (() => {
    if (typeof catalogData === 'undefined') return;
    const grid = document.getElementById('t15-grid');
    if (!grid) return;

    const CURATED = __CURATED_JSON__;

    const CATEGORY_LABELS = {
      'cat-1': '01 Giant Games',
      'cat-2': '02 Carnival Games',
      'cat-3': '03 Photo & Video',
      'cat-4': '04 Performers',
      'cat-5': '05 Music & Nightclub',
      'cat-6': '06 Food & Drinks',
      'cat-7': '07 Foyer & Immersive',
      'cat-8': '08 Adrenaline & VR',
      'cat-9': '09 Pampering',
      'cat-10': '10 Big-Ticket'
    };

    /* One uniform AI-generated icon set: cream disc + gold ring + blue/gold art,
       pre-embedded as data URIs so the single HTML file stays self-contained. */
    const ICONS = __ICONS_JSON__;

    const SVG_INFO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/></svg>';
    const SVG_CHEVRON = '<svg class="t15-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>';
    const SVG_PLUS = '<svg class="t15-ico-plus" viewBox="0 0 24 24" fill="none" stroke-width="2.3" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>';
    const SVG_CHECK = '<svg class="t15-ico-check" viewBox="0 0 24 24" fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';
    const HEART_PATH = 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z';
    const SVG_HEART = '<svg class="t15-ico-heart" viewBox="0 0 24 24" aria-hidden="true"><path d="' + HEART_PATH + '"/></svg>';
    const SVG_SPEC_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

    const esc = (s) => String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

    function cardMarkup(entry, index) {
      const key = entry.key;
      const item = catalogData[key];
      if (!item) return '';
      const rank = index + 1;
      const typeClass = entry.type === 'Rental' ? 't15-type--rental' : 't15-type--experience';
      const specs = (item.specs || []).map((sp) =>
        '<li>' + SVG_SPEC_CHECK + '<span>' + esc(sp) + '</span></li>').join('');
      const panelId = 't15-specs-' + rank;
      const photo = item.img
        ? '<img class="t15-photo" src="' + esc(item.img) + '" alt="' + esc(item.title) + '" loading="lazy" decoding="async">'
        : '<div class="t15-photo t15-photo--empty" aria-hidden="true"></div>';
      return '' +
      '<article class="t15-card" data-t15-key="' + esc(key) + '" style="transition-delay:' + (index * 55) + 'ms">' +
        '<div class="t15-media">' +
          photo +
          '<span class="t15-rank-ghost" aria-hidden="true">' + rank + '</span>' +
          '<span class="t15-rank-pill"><span class="t15-pill-full">#' + rank + ' FAVOURITE</span><span class="t15-pill-short">#' + rank + '</span></span>' +
          '<span class="t15-type ' + typeClass + '">' + esc(entry.type) + '</span>' +
          /* badge icon overlaps the photo's bottom-left; kept here so the
             existing fly-to-tray animation (.t15-icon img) works unchanged */
          '<span class="t15-icon"><img src="' + (ICONS[item.categoryKey] || ICONS['cat-1']) + '" alt="" loading="lazy"></span>' +
        '</div>' +
        '<div class="t15-body">' +
          '<div class="t15-meta">' +
            '<span class="t15-cat">' + esc(CATEGORY_LABELS[item.categoryKey] || item.cat || '') + '</span>' +
          '</div>' +
          '<h3 class="t15-title">' + esc(item.title) + '</h3>' +
          '<p class="t15-quote">' + esc(entry.hook) + '</p>' +
          '<div class="t15-divider" aria-hidden="true"></div>' +
          '<div class="t15-footer">' +
            '<button type="button" class="t15-specs-btn" aria-expanded="false" aria-controls="' + panelId + '">' +
              SVG_INFO + '<span class="t15-specs-label">Quick Specs</span>' + SVG_CHEVRON +
            '</button>' +
            '<button type="button" class="t15-wish" data-wishlist-key="' + esc(key) + '" aria-pressed="false" aria-label="Add ' + esc(item.title) + ' to wishlist">' +
              SVG_PLUS + SVG_CHECK + SVG_HEART +
            '</button>' +
          '</div>' +
          '<div class="t15-specs-panel" id="' + panelId + '" role="region" aria-label="Specifications for ' + esc(item.title) + '"><ul>' + specs + '</ul></div>' +
        '</div>' +
      '</article>';
    }

    grid.innerHTML = CURATED.map(cardMarkup).join('');

    /* ---- flying AI badge icon -> wishlist tray (mirrors the site's v3.24 fly) ---- */
    const reduceMotion = () => window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function trayTargetRect() {
      const t = document.getElementById('wishlist-tray-btn');
      if (t) {
        const icon = t.querySelector('.wishlist-tray-icon');
        const r = (icon || t).getBoundingClientRect();
        if (r.width && r.height) return r;
      }
      // tray not painted yet (first add) -> its fixed bottom-right resting spot
      return { left: window.innerWidth - 60, top: window.innerHeight - 60, width: 40, height: 40 };
    }

    function bumpTray() {
      const t = document.getElementById('wishlist-tray-btn');
      if (!t) return;
      t.classList.remove('hp-tray-bump');
      void t.offsetWidth;
      t.classList.add('hp-tray-bump');
      setTimeout(() => t.classList.remove('hp-tray-bump'), 560);
    }

    function flyCardIcon(card) {
      if (reduceMotion() || typeof Element.prototype.animate !== 'function') return;
      const iconImg = card && card.querySelector('.t15-icon img');
      if (!iconImg) return;
      const f = iconImg.getBoundingClientRect();
      const tr = trayTargetRect();
      const sx = f.left + f.width / 2, sy = f.top + f.height / 2;
      const ex = tr.left + tr.width / 2, ey = tr.top + tr.height / 2;
      const dx = ex - sx, dy = ey - sy;

      const wrap = document.createElement('span');
      wrap.className = 't15-fly-icon';
      wrap.setAttribute('aria-hidden', 'true');
      wrap.style.left = sx + 'px';
      wrap.style.top = sy + 'px';
      wrap.style.width = f.width + 'px';
      wrap.style.height = f.height + 'px';
      const clone = document.createElement('img');
      clone.src = iconImg.src;
      clone.alt = '';
      wrap.appendChild(clone);
      document.body.appendChild(wrap);

      const anim = wrap.animate([
        { transform: 'translate(-50%, -50%) scale(1) rotate(0deg)', opacity: 1, offset: 0 },
        { transform: 'translate(calc(-50% + ' + (dx * 0.5) + 'px), calc(-50% + ' + (dy * 0.42 - 70) + 'px)) scale(1.12) rotate(-8deg)', opacity: 1, offset: 0.5 },
        { transform: 'translate(calc(-50% + ' + dx + 'px), calc(-50% + ' + dy + 'px)) scale(.3) rotate(10deg)', opacity: 0.15, offset: 1 }
      ], { duration: 850, easing: 'cubic-bezier(.3, .7, .4, 1)', fill: 'forwards' });
      anim.onfinish = () => { wrap.remove(); bumpTray(); };
      anim.oncancel = () => wrap.remove();
    }

    /* reverse flight: badge clone travels tray -> card and "lands" with a pop */
    function flyCardIconBack(card) {
      if (reduceMotion() || typeof Element.prototype.animate !== 'function') return;
      const iconImg = card && card.querySelector('.t15-icon img');
      if (!iconImg) return;
      const tr = trayTargetRect();
      const f = iconImg.getBoundingClientRect();
      const sx = tr.left + tr.width / 2, sy = tr.top + tr.height / 2;
      const ex = f.left + f.width / 2, ey = f.top + f.height / 2;
      const dx = ex - sx, dy = ey - sy;

      const wrap = document.createElement('span');
      wrap.className = 't15-fly-icon';
      wrap.setAttribute('aria-hidden', 'true');
      wrap.style.left = sx + 'px';
      wrap.style.top = sy + 'px';
      wrap.style.width = f.width + 'px';
      wrap.style.height = f.height + 'px';
      const clone = document.createElement('img');
      clone.src = iconImg.src;
      clone.alt = '';
      wrap.appendChild(clone);
      document.body.appendChild(wrap);

      const anim = wrap.animate([
        { transform: 'translate(-50%, -50%) scale(.3) rotate(10deg)', opacity: 0.25, offset: 0 },
        { transform: 'translate(calc(-50% + ' + (dx * 0.5) + 'px), calc(-50% + ' + (dy * 0.42 - 70) + 'px)) scale(1.1) rotate(8deg)', opacity: 1, offset: 0.5 },
        { transform: 'translate(calc(-50% + ' + dx + 'px), calc(-50% + ' + dy + 'px)) scale(1) rotate(0deg)', opacity: 1, offset: 1 }
      ], { duration: 850, easing: 'cubic-bezier(.3, .7, .4, 1)', fill: 'forwards' });
      anim.onfinish = () => {
        wrap.remove();
        iconImg.classList.remove('t15-land-pop');
        void iconImg.offsetWidth;
        iconImg.classList.add('t15-land-pop');
        setTimeout(() => iconImg.classList.remove('t15-land-pop'), 520);
      };
      anim.oncancel = () => wrap.remove();
    }

    /* ---- Quick Specs accordion (inline; modals are disabled in this build) ---- */
    grid.addEventListener('click', (ev) => {
      const specsBtn = ev.target.closest('.t15-specs-btn');
      if (specsBtn) {
        const panel = document.getElementById(specsBtn.getAttribute('aria-controls'));
        const open = specsBtn.getAttribute('aria-expanded') === 'true';
        specsBtn.setAttribute('aria-expanded', String(!open));
        if (panel) panel.style.maxHeight = open ? '0px' : (panel.scrollHeight + 24) + 'px';
        return;
      }

      const wishBtn = ev.target.closest('.t15-wish');
      if (wishBtn) {
        const key = wishBtn.getAttribute('data-wishlist-key');
        const willAdd = !wishBtn.classList.contains('is-active');
        const card = wishBtn.closest('.t15-card');
        if (typeof window.toggleWishlist === 'function') {
          window.toggleWishlist(ev, key);          // shared storage / drawer / toast / form
        }
        const active = wishBtn.classList.contains('is-active');
        if (card) card.classList.toggle('is-saved', active);
        const item = catalogData[key];
        wishBtn.setAttribute('aria-label',
          (active ? 'Remove ' : 'Add ') + (item ? item.title : key) + (active ? ' from wishlist' : ' to wishlist'));

        clearTimeout(wishBtn._t15PhaseTimer);
        if (willAdd && active) {
          /* +  ->  gold check (brief)  ->  pink heart (final) */
          wishBtn.classList.add('is-checking');
          wishBtn._t15PhaseTimer = setTimeout(() => wishBtn.classList.remove('is-checking'), 680);
          /* wait two frames so the tray has painted before measuring its rect */
          requestAnimationFrame(() => requestAnimationFrame(() => flyCardIcon(card)));
        } else if (!willAdd && !active) {
          /* symmetric removal: pink heart -> gold check (brief) -> plus,
             while the badge flies back from the tray into this card */
          wishBtn.classList.add('is-checking');
          wishBtn._t15PhaseTimer = setTimeout(() => wishBtn.classList.remove('is-checking'), 680);
          requestAnimationFrame(() => requestAnimationFrame(() => flyCardIconBack(card)));
        }
      }
    });

    /* ---- reflect any pre-existing wishlist state on first paint ---- */
    function syncInitial() {
      if (typeof window.syncWishlistButtons === 'function') window.syncWishlistButtons();
      grid.querySelectorAll('.t15-wish').forEach((btn) => {
        const card = btn.closest('.t15-card');
        if (card) card.classList.toggle('is-saved', btn.classList.contains('is-active'));
      });
    }
    syncInitial();

    /* ---- staggered scroll-in animation ---- */
    if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => { if (en.isIntersecting) { grid.classList.add('is-inview'); io.disconnect(); } });
      }, { threshold: 0.08 });
      io.observe(grid);
    } else {
      grid.classList.add('is-inview');
    }
  })();
  </script>

  <!-- v3.28 — main catalogue (100 cards) reverse flight: a pink heart flies
       OUT of the wishlist tray back to the card being removed. The existing
       v3.24 script keeps handling the forward (add) flight; this additive
       capture-phase listener only acts on removal (button still active at
       click time, because the state flips in the later bubble phase). -->
  <script>
  (() => {
    const PATH = 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z';
    const reduce = () => window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const tray = () => document.getElementById('wishlist-tray-btn');

    function trayRect() {
      const t = tray();
      if (t) {
        const icon = t.querySelector('.wishlist-tray-icon');
        const r = (icon || t).getBoundingClientRect();
        if (r.width && r.height) return r;
      }
      return { left: window.innerWidth - 60, top: window.innerHeight - 60, width: 40, height: 40 };
    }

    function popLanding(btn) {
      btn.classList.remove('hp-btn-land');
      void btn.offsetWidth;
      btn.classList.add('hp-btn-land');
      setTimeout(() => btn.classList.remove('hp-btn-land'), 540);
    }

    function flyHeartBack(btn) {
      if (reduce() || typeof Element.prototype.animate !== 'function') return;
      const tr = trayRect();
      const r = btn.getBoundingClientRect();
      const sx = tr.left + tr.width / 2, sy = tr.top + tr.height / 2;
      const ex = r.left + r.width / 2, ey = r.top + r.height / 2;
      const dx = ex - sx, dy = ey - sy;

      const el = document.createElement('span');
      el.className = 'hp-flying-heart';
      el.setAttribute('aria-hidden', 'true');
      el.innerHTML = '<svg viewBox="0 0 24 24"><path d="' + PATH + '"></path></svg>';
      el.style.left = sx + 'px';
      el.style.top = sy + 'px';
      document.body.appendChild(el);

      const anim = el.animate([
        { transform: 'translate(-50%, -50%) scale(.35)', opacity: 0.3, offset: 0 },
        { transform: 'translate(calc(-50% + ' + (dx * 0.5) + 'px), calc(-50% + ' + (dy * 0.45 - 62) + 'px)) scale(1.2)', opacity: 1, offset: 0.55 },
        { transform: 'translate(calc(-50% + ' + dx + 'px), calc(-50% + ' + dy + 'px)) scale(.9)', opacity: 1, offset: 1 }
      ], { duration: 820, easing: 'cubic-bezier(.3, .7, .4, 1)', fill: 'forwards' });

      anim.onfinish = () => { el.remove(); popLanding(btn); };
      anim.oncancel = () => el.remove();
    }

    document.addEventListener('click', (event) => {
      const btn = event.target && event.target.closest
        ? event.target.closest('.services-grid-12 .catalog-card .wishlist-btn')
        : null;
      if (!btn) return;
      /* capture phase = pre-toggle state: active means this click removes it */
      if (!btn.classList.contains('is-active')) return;
      requestAnimationFrame(() => requestAnimationFrame(() => flyHeartBack(btn)));
    }, true);
  })();
  </script>

  <!-- v3.29 — anchored mini wishlist sheet. Replaces the global stacked toast
       for card wishlist buttons only: a small sheet slides in directly under
       the clicked button showing the item TITLE, then slides back down and
       fades. Every other toast (forms, quote, clear-wishlist, etc.) is
       untouched. A MutationObserver intercepts the toast node before paint,
       so this works regardless of the internal showToast() binding. -->
  <script>
  (() => {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer || typeof MutationObserver === 'undefined') return;

    const HEART_PATH = 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z';
    const reduce = () => window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const esc = (s) => String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

    let pending = null;
    let pendingTimer = null;

    function titleFrom(btn) {
      const card = btn.closest('.t15-card, .catalog-card');
      const t = card && card.querySelector('.t15-title, .service-card-title');
      if (t && t.textContent.trim()) return t.textContent.trim();
      const key = btn.getAttribute('data-wishlist-key');
      if (key && typeof catalogData !== 'undefined' && catalogData[key]) {
        return catalogData[key].title;
      }
      return 'Wishlist updated';
    }

    /* capture phase: remember which card button was clicked before the
       shared toggleWishlist() flips state and emits its global toast */
    document.addEventListener('click', (event) => {
      const btn = event.target && event.target.closest
        ? event.target.closest('.t15-wish, .services-grid-12 .catalog-card .wishlist-btn')
        : null;
      if (!btn) return;
      pending = {
        anchor: btn,
        title: titleFrom(btn),
        willAdd: !btn.classList.contains('is-active')
      };
      clearTimeout(pendingTimer);
      pendingTimer = setTimeout(() => { pending = null; }, 600);
    }, true);

    new MutationObserver((mutations) => {
      if (!pending) return;
      const added = [];
      mutations.forEach((m) => m.addedNodes.forEach((n) => {
        if (n.nodeType === 1 && n.classList && n.classList.contains('toast-pill')) added.push(n);
      }));
      if (!added.length) return;
      const ctx = pending;
      pending = null;
      clearTimeout(pendingTimer);
      added.forEach((n) => n.remove());       // suppress the global toast
      showMiniSheet(ctx);
    }).observe(toastContainer, { childList: true });

    function showMiniSheet(ctx) {
      document.querySelectorAll('.wish-mini-sheet').forEach((n) => {
        if (typeof n._dispose === 'function') n._dispose(); else n.remove();
      });
      const sheet = document.createElement('div');
      sheet.className = 'wish-mini-sheet ' + (ctx.willAdd ? 'is-add' : 'is-remove');
      sheet.innerHTML =
        '<svg class="wms-heart" viewBox="0 0 24 24" aria-hidden="true"><path d="' + HEART_PATH + '"/></svg>' +
        '<span class="wms-title">' + esc(ctx.title) + '</span>' +
        '<span class="wms-caret" aria-hidden="true"></span>';
      sheet.style.visibility = 'hidden';
      document.body.appendChild(sheet);

      const w = sheet.offsetWidth, h = sheet.offsetHeight;
      const r = ctx.anchor.getBoundingClientRect();
      let left = r.left + r.width / 2 - w / 2;
      left = Math.max(10, Math.min(left, window.innerWidth - w - 10));
      let top = r.bottom + 10;
      let above = false;
      if (top + h + 12 > window.innerHeight) { above = true; top = r.top - h - 10; }
      if (top < 8) top = 8;
      sheet.style.left = left + 'px';
      sheet.style.top = top + 'px';
      if (above) sheet.classList.add('is-above');

      const caret = sheet.querySelector('.wms-caret');
      const caretX = r.left + r.width / 2 - left - 6;
      caret.style.left = Math.max(6, Math.min(caretX, w - 18)) + 'px';
      sheet.style.visibility = '';

      const enter = reduce()
        ? [{ opacity: 0 }, { opacity: 1 }]
        : [{ opacity: 0, transform: 'translate(-18px, 10px) scale(.96)' },
           { opacity: 1, transform: 'translate(0, 0) scale(1)' }];
      sheet.animate(enter, {
        duration: reduce() ? 160 : 340,
        easing: 'cubic-bezier(.22, .61, .36, 1)',
        fill: 'forwards'
      });

      const born = performance.now();
      const cleanup = () => {
        window.removeEventListener('scroll', abort, true);
        window.removeEventListener('resize', abort);
        if (sheet.parentNode) sheet.remove();
      };
      sheet._dispose = cleanup;
      /* ignore the click-induced focus/programmatic scroll that can fire
         within the first moments of the sheet's life */
      const abort = () => { if (performance.now() - born > 150) cleanup(); };
      window.addEventListener('scroll', abort, { passive: true, capture: true });
      window.addEventListener('resize', abort);

      setTimeout(() => {
        const exit = reduce()
          ? [{ opacity: 1 }, { opacity: 0 }]
          : above
            ? [{ opacity: 1, transform: 'translate(0, 0)' },
               { opacity: 0, transform: 'translate(-10px, -14px) scale(.97)' }]
            : [{ opacity: 1, transform: 'translate(0, 0)' },
               { opacity: 0, transform: 'translate(-10px, 16px) scale(.97)' }];
        const anim = sheet.animate(exit, {
          duration: reduce() ? 180 : 320,
          easing: 'ease-in',
          fill: 'forwards'
        });
        anim.onfinish = cleanup;
        anim.oncancel = cleanup;
      }, reduce() ? 1300 : 1500);
    }
  })();
  </script>
'''


# ---------------------------------------------------------------- v3.31 sections
# Three new homepage bands (Why Choose Us / Our Process / Testimonials),
# placed in conversion-funnel order. All markup is self-contained and uses the
# site's shared .section-header-center / .hd-eyebrow / .heading-display system.

# v5.3 — the old AI testimonial portraits (jasmine/daniel/priya) were retired
# in v5.1; the testimonials section now uses real client-published logos only,
# so no portrait input directory is required to build.

# Shared header treatment for the three new sections: mirrors the source's
# scoped #services/#contact heading rules (600-weight navy, coral eyebrow,
# gold dash, no gradient ::after line) for 100% homepage consistency.
NEW_SECTION_HEADER_CSS = '''
    #why-choose .section-header-center .heading-display,
    #our-process .section-header-center .heading-display,
    #testimonials .section-header-center .heading-display {
      margin: 0 auto;
      max-width: 63%;
      padding: 6px 0 14px;
      font-family: var(--font-display);
      font-size: 46.8px;
      font-weight: 600;
      line-height: 1.1;
      letter-spacing: -.01em;
      color: #20304D;
      text-align: center;
      text-wrap: balance;
      font-optical-sizing: none;
      font-variation-settings: 'opsz' 14;
    }
    #why-choose .section-header-center .heading-display::after,
    #our-process .section-header-center .heading-display::after,
    #testimonials .section-header-center .heading-display::after {
      content: none !important;
      display: none !important;
    }
    /* gold keyword + hand-drawn underline, verbatim from the site's
       #services/#contact scoped rules for 100% title consistency */
    #why-choose .section-header-center .heading-display .text-gold,
    #our-process .section-header-center .heading-display .text-gold,
    #testimonials .section-header-center .heading-display .text-gold {
      position: relative;
      display: inline-block;
      color: #A16D12;
    }
    #why-choose .section-header-center .heading-display .text-gold::after,
    #our-process .section-header-center .heading-display .text-gold::after,
    #testimonials .section-header-center .heading-display .text-gold::after {
      content: "";
      position: absolute;
      left: 0;
      bottom: -5px;
      width: 100%;
      height: 6px;
      border-bottom: 2px solid #D3A15F;
      border-radius: 0 0 50% 50%;
      box-shadow: 0 2px 3px rgba(211, 161, 95, .25), 0 4px 8px rgba(211, 161, 95, .20);
    }
    #why-choose .section-header-center .hd-eyebrow,
    #our-process .section-header-center .hd-eyebrow,
    #testimonials .section-header-center .hd-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-family: var(--font-body);
      font-size: 13.68px;
      font-weight: 600;
      line-height: 1.65;
      letter-spacing: .1em;
      text-transform: uppercase;
      color: #F0553A;
      margin-bottom: 12px;
      justify-content: center;
    }
    #why-choose .section-header-center .hd-eyebrow .line,
    #our-process .section-header-center .hd-eyebrow .line,
    #testimonials .section-header-center .hd-eyebrow .line {
      width: 22px;
      height: 2px;
      border-radius: 2px;
      background: #D5A021;
      box-shadow: none;
    }
    @media (max-width: 767px) {
      #why-choose .section-header-center .hd-eyebrow,
      #our-process .section-header-center .hd-eyebrow,
      #testimonials .section-header-center .hd-eyebrow {
        font-size: 12.4762px;
        letter-spacing: .1em;
      }
      #why-choose .section-header-center .heading-display,
      #our-process .section-header-center .heading-display,
      #testimonials .section-header-center .heading-display {
        max-width: 100%;
        font-size: 32.832px;
      }
    }
'''

BLOCK_WHY = '''
  <!-- ==========================================================================
       v3.31 — WHY CHOOSE US (trust: why brands rely on Advertising & More)
       Sits between the trusted-brands marquee and the Top 15 band.
       ========================================================================== -->
  <section class="hp2-why" id="why-choose" aria-labelledby="why-choose-heading">
    <div class="container">
      <div class="section-header-center">
        <div class="hd-eyebrow"><span class="line"></span><span>Why Choose Advertising &amp; More</span></div>
        <h2 class="heading-display" id="why-choose-heading">More Than an Event &mdash; A <span class="text-gold">Partner</span> You Can Count On.</h2>
        <p class="section-deck">One team for the idea, the setup and the last song &mdash; so you can stay with your guests instead of chasing vendors.</p>
      </div>
      <div class="wc-grid">
        <article class="wc-card">
          <div class="wc-icon"><img src="__ICO_WC_1__" alt="" loading="lazy" width="62" height="62"></div>
          <div class="wc-body">
            <h3 class="wc-title">Custom Concepts</h3>
            <p class="wc-text" title="Fresh ideas tailored to your goals and style.">Fresh ideas tailored to your goals and style.</p>
          </div>
        </article>
        <article class="wc-card">
          <div class="wc-icon"><img src="__ICO_WC_2__" alt="" loading="lazy" width="62" height="62"></div>
          <div class="wc-body">
            <h3 class="wc-title">Seamless Coordina&shy;tion</h3>
            <p class="wc-text" title="We handle the details so you can enjoy the moment.">We handle the details so you can enjoy the moment.</p>
          </div>
        </article>
        <article class="wc-card">
          <div class="wc-icon"><img src="__ICO_WC_3__" alt="" loading="lazy" width="62" height="62"></div>
          <div class="wc-body">
            <h3 class="wc-title">Creative Execution</h3>
            <p class="wc-text" title="Stunning setups, memorable experiences, zero stress.">Stunning setups, memorable experiences, zero stress.</p>
          </div>
        </article>
        <article class="wc-card">
          <div class="wc-icon"><img src="__ICO_WC_4__" alt="" loading="lazy" width="62" height="62"></div>
          <div class="wc-body">
            <h3 class="wc-title">Agency-Level Branding Support</h3>
            <p class="wc-text" title="Perfect for corporate events and brand activations.">Perfect for corporate events and brand activations.</p>
          </div>
        </article>
      </div>
    </div>
  </section>

  <style id="hp2-why-process-css">
  __NEW_SECTION_HEADER_CSS__
    /* ---------------- Why Choose Us ---------------- */
    .hp2-why {
      position: relative;
      /* no section band — the page's warm cream background runs through */
      background: transparent;
      overflow: hidden;
    }
    .hp2-why::before,
    .hp2-process::before,
    .hp2-testimonials::before {
      content: "";
      position: absolute;
      inset: 0 0 auto 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(0, 73, 168, 0.16), transparent);
    }
    .wc-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 22px;
    }
    .wc-card {
      background: linear-gradient(180deg, #fdfaf3, #fbf3e2);
      border: 1px solid rgba(213, 160, 33, .22);
      border-radius: 18px;
      padding: 30px 24px 28px;
      transition: transform .35s cubic-bezier(.22,.61,.36,1), box-shadow .35s ease, border-color .35s ease;
    }
    .wc-card:hover {
      transform: translateY(-6px);
      border-color: rgba(213, 160, 33, .65);
      box-shadow: 0 20px 40px rgba(11, 30, 63, .12);
    }
    /* The AI badge artwork carries its own cream disc and gold ring, so the
       container stays transparent like the Top 15 icon wrapper. */
    .wc-icon {
      width: 62px;
      height: 62px;
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 18px;
    }
    .wc-icon img {
      width: 62px;
      height: 62px;
      display: block;
      filter: drop-shadow(0 6px 12px rgba(11, 30, 63, .16));
      transition: transform .35s ease;
    }
    .wc-card:hover .wc-icon img { transform: scale(1.06) rotate(-3deg); }
    .wc-title {
      font-family: var(--font-display);
      font-size: 1.18rem;
      font-weight: 700;
      color: var(--color-primary-dark);
      margin: 0 0 8px;
    }
    .wc-text {
      font-size: .96rem;
      line-height: 1.62;
      color: var(--color-text-muted);
      margin: 0;
    }
    /* All four cards stay side by side at every width — badge on top,
       title and description centered beneath each icon. */
    @media (max-width: 1024px) {
      .wc-grid { gap: 14px; }
      .wc-card { padding: 20px 14px 18px; border-radius: 16px; }
      .wc-icon, .wc-icon img { width: 54px; height: 54px; }
      .wc-icon { margin-bottom: 12px; }
      .wc-title { font-size: 1rem; }
      .wc-text { font-size: .85rem; }
    }
    @media (max-width: 640px) {
      .wc-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }
      .wc-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 12px 7px;
        border-radius: 14px;
        min-width: 0;
      }
      .wc-icon, .wc-icon img { width: 44px; height: 44px; }
      .wc-icon { margin-bottom: 9px; }
      .wc-body { width: 100%; min-width: 0; }
      .wc-title {
        font-size: .74rem;
        line-height: 1.28;
        margin: 0 0 5px;
        overflow-wrap: break-word;
        hyphens: auto;
      }
      .wc-text {
        display: block;
        font-size: .62rem;
        line-height: 1.42;
        margin: 0;
        text-align: center;
        overflow-wrap: break-word;
        /* cap at ~3 lines without -webkit-box (which justified narrow text) */
        max-height: 2.65em;
        overflow: hidden;
      }
    }
    @media (max-width: 380px) {
      .wc-grid { gap: 6px; }
      .wc-card { padding: 10px 5px; border-radius: 12px; }
      .wc-icon, .wc-icon img { width: 36px; height: 36px; }
      .wc-icon { margin-bottom: 7px; }
      .wc-title { font-size: .68rem; margin-bottom: 4px; }
      .wc-text { font-size: .58rem; max-height: 2.55em; }
    }
  </style>
'''

def _op_keyframes():
    """Build the synchronized 10s looping flow keyframes.

    Choreography (strict icon -> arrow -> next icon order):
      icon i pops at ICON_START[i]; then the arrow beneath it emerges from
      under that badge and travels to the next one over ARROW_START..+5%;
      it settles exactly when the next badge begins to pop. After badge 5
      the whole chain holds, then fades and replays from step 1."""
    icon_start = [0, 9, 18, 27, 36]
    arrow_start = [4, 13, 22, 31]
    parts = []
    for i in range(1, 6):
        s = icon_start[i - 1]
        start = "0%" if s == 0 else f"0%, {s}%"
        parts.append(f"""
    @keyframes opIcon{i} {{
      {start} {{ opacity: 0; transform: scale(.4); }}
      {s + 3}% {{ opacity: 1; transform: scale(1.22); }}
      {s + 4}% {{ transform: scale(1); }}
      82% {{ opacity: 1; transform: scale(1); }}
      88%, 100% {{ opacity: 1; transform: scale(1); }}
    }}""")
    for j in range(1, 5):
        a = arrow_start[j - 1]
        parts.append(f"""
    @keyframes opArrowH{j} {{
      0%, {a}% {{ opacity: 0; transform: translateX(-58px) scale(.5); }}
      {a + 4}% {{ opacity: 1; transform: translateX(2px) scale(1.06); }}
      {a + 5}%, 82% {{ opacity: 1; transform: translateX(0) scale(1); }}
      88%, 100% {{ opacity: 1; transform: translateX(0) scale(1); }}
    }}
    @keyframes opArrowV{j} {{
      0%, {a}% {{ opacity: 0; transform: translateY(-40px) scale(.5); }}
      {a + 4}% {{ opacity: 1; transform: translateY(2px) scale(1.06); }}
      {a + 5}%, 82% {{ opacity: 1; transform: translateY(0) scale(1); }}
      88%, 100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}""")
    # Copy floats up + brightens in step with its badge. It never vanishes:
    # resting state stays at 55% opacity so every line remains readable.
    for i in range(1, 6):
        s = icon_start[i - 1]
        start = "0%" if s == 0 else f"0%, {s}%"
        parts.append(f"""
    @keyframes opText{i} {{
      {start} {{ opacity: .55; transform: translateY(8px); }}
      {s + 4}% {{ opacity: 1; transform: translateY(0); }}
      82% {{ opacity: 1; transform: none; }}
      88%, 100% {{ opacity: 1; transform: none; }}
    }}""")
    parts.append("""
    @keyframes opLineH {
      0% { opacity: 1; transform: scaleX(0); }
      38% { transform: scaleX(1); }
      82% { opacity: 1; transform: scaleX(1); }
      88%, 100% { opacity: 1; transform: scaleX(1); }
    }
    @keyframes opLineV {
      0% { opacity: 1; transform: scaleY(0); }
      38% { transform: scaleY(1); }
      82% { opacity: 1; transform: scaleY(1); }
      88%, 100% { opacity: 1; transform: scaleY(1); }
    }""")
    return "".join(parts)


OP_KEYFRAMES = _op_keyframes()

BLOCK_PROCESS = '''
  <!-- ==========================================================================
       v3.31 — OUR PROCESS (5-step timeline, lowers enquiry friction)
       Sits between the full catalogue and the drinks showcase.
       ========================================================================== -->
  <section class="hp2-process" id="our-process" aria-labelledby="our-process-heading">
    <div class="container">
      <div class="section-header-center">
        <div class="hd-eyebrow"><span class="line"></span><span>Our Process</span></div>
        <h2 class="heading-display" id="our-process-heading">From Idea to <span class="text-gold">Incredible,</span> Together.</h2>
        <p class="section-deck">Five simple steps, a lot of heart, and just enough caffeine.</p>
      </div>
      <ol class="op-steps op-run">
        <li class="op-step">
          <span class="op-ic"><img src="__ICO_OP_1__" alt="" loading="lazy" width="92" height="92"></span>
          <div class="op-copy">
          <h3 class="op-title">We Listen</h3>
          <p class="op-text">Your goals, ideas and must-haves.</p>
        </div>
          <span class="op-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#D5A021" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg></span>
        </li>
        <li class="op-step">
          <span class="op-ic"><img src="__ICO_OP_2__" alt="" loading="lazy" width="92" height="92"></span>
          <div class="op-copy">
          <h3 class="op-title">We Plan</h3>
          <p class="op-text">Creative concepts, details and logistics.</p>
        </div>
          <span class="op-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#D5A021" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg></span>
        </li>
        <li class="op-step">
          <span class="op-ic"><img src="__ICO_OP_3__" alt="" loading="lazy" width="92" height="92"></span>
          <div class="op-copy">
          <h3 class="op-title">We Execute</h3>
          <p class="op-text">Flawless setup, onsite coordination.</p>
        </div>
          <span class="op-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#D5A021" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg></span>
        </li>
        <li class="op-step">
          <span class="op-ic"><img src="__ICO_OP_4__" alt="" loading="lazy" width="92" height="92"></span>
          <div class="op-copy">
          <h3 class="op-title">We Deliver</h3>
          <p class="op-text">A seamless and memorable event.</p>
        </div>
          <span class="op-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#D5A021" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg></span>
        </li>
        <li class="op-step">
          <span class="op-ic"><img src="__ICO_OP_5__" alt="" loading="lazy" width="92" height="92"></span>
          <div class="op-copy">
          <h3 class="op-title">We Celebrate</h3>
          <p class="op-text">Happy people, lasting memories.</p>
        </div>
        </li>
      </ol>
    </div>
  </section>

  <style id="hp2-process-css">
    .hp2-process {
      position: relative;
      background: transparent;
      overflow: hidden;
    }
    .op-steps {
      position: relative;
      list-style: none;
      margin: 0;
      padding: 0;
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 26px;
    }
    /* connector line runs behind the badge icons, draws itself in each cycle */
    .op-steps::before {
      content: "";
      position: absolute;
      top: 45px;
      left: 10%;
      right: 10%;
      height: 2px;
      background: linear-gradient(90deg, rgba(213,160,33,.18), rgba(213,160,33,.55), rgba(213,160,33,.18));
      transform-origin: left center;
    }
    .op-step {
      position: relative;
      text-align: center;
      margin: 0;
    }
    /* larger AI brand badges (self-contained cream disc + gold ring) */
    .op-ic {
      position: relative;
      z-index: 1;
      width: 92px;
      height: 92px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 16px;
    }
    .op-ic img {
      width: 92px;
      height: 92px;
      display: block;
      filter: drop-shadow(0 8px 16px rgba(11, 30, 63, .18));
      transition: transform .35s ease;
    }
    .op-step:hover .op-ic img { transform: scale(1.07) rotate(-3deg); }
    /* gold arrow disc bridging one step to the next */
    .op-arrow {
      position: absolute;
      top: 28px;
      right: -30px;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--color-bg-page, #F7EDDC);
      border: 1.5px solid rgba(213, 160, 33, .55);
      box-shadow: 0 6px 14px rgba(11, 30, 63, .12);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2;
    }
    .op-arrow svg { width: 18px; height: 18px; display: block; }
    .op-title {
      font-family: var(--font-display);
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--color-primary-dark);
      margin: 0 0 6px;
    }
    .op-text {
      font-size: .92rem;
      line-height: 1.6;
      color: var(--color-text-muted);
      margin: 0;
      max-width: 210px;
      margin-inline: auto;
    }

    /* ---- one-shot sequential reveal: badge pops, arrow flies to the next,
           then every step stays fully visible (no infinite hiding loop) ---- */
    __OP_KEYFRAMES__
    .op-steps.op-run::before { animation: opLineH 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(1) .op-ic { animation: opIcon1 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(2) .op-ic { animation: opIcon2 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(3) .op-ic { animation: opIcon3 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(4) .op-ic { animation: opIcon4 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(5) .op-ic { animation: opIcon5 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(1) .op-arrow { animation: opArrowH1 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(2) .op-arrow { animation: opArrowH2 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(3) .op-arrow { animation: opArrowH3 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(4) .op-arrow { animation: opArrowH4 4.8s ease-out forwards; }
    /* copy never leaves — it only floats up and brightens with its badge */
    .op-run .op-step:nth-child(1) :is(.op-title, .op-text) { animation: opText1 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(2) :is(.op-title, .op-text) { animation: opText2 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(3) :is(.op-title, .op-text) { animation: opText3 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(4) :is(.op-title, .op-text) { animation: opText4 4.8s ease-out forwards; }
    .op-run .op-step:nth-child(5) :is(.op-title, .op-text) { animation: opText5 4.8s ease-out forwards; }

    @media (max-width: 1024px) {
      .op-steps { gap: 18px; }
      .op-ic, .op-ic img { width: 78px; height: 78px; }
      .op-steps::before { top: 38px; }
      .op-arrow { top: 22px; right: -26px; width: 32px; height: 32px; }
      .op-arrow svg { width: 16px; height: 16px; }
    }
    @media (max-width: 860px) {
      /* Vertical rail on one fixed measure. Each slot is a flex row: badge
         fixed on the LEFT and a tight title+copy block on the RIGHT, both
         vertically centred, so there is never stray whitespace between the
         title and description or between the icon and its text. */
      .op-steps {
        --op-ic: 60px;
        --op-arw: 28px;
        --op-gap: 28px;
        --op-cgap: 16px;
        --op-row: 84px;
        grid-template-columns: 1fr;
        gap: var(--op-gap);
      }
      .op-steps::before {
        top: calc(var(--op-row) / 2);
        bottom: calc(var(--op-row) / 2);
        left: calc((var(--op-ic) - 2px) / 2);
        right: auto;
        width: 2px;
        height: auto;
        transform-origin: top center;
        background: linear-gradient(180deg, rgba(213,160,33,.18), rgba(213,160,33,.55), rgba(213,160,33,.18));
      }
      .op-steps.op-run::before { animation-name: opLineV; }
      .op-step {
        position: relative;
        display: flex;
        flex-direction: row;
        align-items: center;
        column-gap: var(--op-cgap);
        text-align: left;
        padding-left: 0;
        /* every slot is the same fixed height, so a two-line description can
           never lengthen one row and break the icon/arrow rhythm */
        min-height: var(--op-row);
      }
      .op-ic {
        position: static;
        flex: 0 0 var(--op-ic);
        width: var(--op-ic);
        height: var(--op-ic);
        margin: 0;
      }
      .op-ic img { width: 100%; height: 100%; }
      /* tight text block: title and description stacked with no empty gap */
      .op-copy { flex: 1 1 auto; min-width: 0; }
      .op-title { padding-top: 0; margin: 0 0 2px; }
      .op-text { max-width: none; margin: 0; }
      /* the disc always centres in the row gap on the icon centre-line,
         i.e. exactly between two consecutive badges */
      .op-arrow {
        position: absolute;
        left: calc((var(--op-ic) - var(--op-arw)) / 2);
        top: calc(100% + (var(--op-gap) - var(--op-arw)) / 2);
        bottom: auto;
        width: var(--op-arw);
        height: var(--op-arw);
        margin: 0;
      }
      .op-arrow svg { width: 14px; height: 14px; transform: rotate(90deg); }
      .op-run .op-step:nth-child(1) .op-arrow { animation-name: opArrowV1; }
      .op-run .op-step:nth-child(2) .op-arrow { animation-name: opArrowV2; }
      .op-run .op-step:nth-child(3) .op-arrow { animation-name: opArrowV3; }
      .op-run .op-step:nth-child(4) .op-arrow { animation-name: opArrowV4; }
    }
    @media (max-width: 480px) {
      /* compact phones: slightly smaller badge + disc, tighter measure */
      .op-steps {
        --op-ic: 52px;
        --op-arw: 26px;
        --op-gap: 24px;
        --op-cgap: 12px;
        --op-row: 84px;
      }
      .op-title { font-size: 1rem; }
      .op-text { font-size: .82rem; }
    }
    @media (prefers-reduced-motion: reduce) {
      .op-steps::before,
      .op-ic,
      .op-arrow,
      .op-title,
      .op-text { animation: none !important; opacity: 1 !important; transform: none !important; }
    }
  </style>
'''

BLOCK_TESTI = '''
  <!-- ==========================================================================
       v3.31 — CLIENT TESTIMONIALS (social proof immediately before enquiry)
       ========================================================================== -->
  <section class="hp2-testimonials" id="testimonials" aria-labelledby="testimonials-heading">
    <div class="container">
      <div class="section-header-center">
        <div class="hd-eyebrow"><span class="line"></span><span>Kind words</span></div>
        <h2 class="heading-display" id="testimonials-heading">Trusted by Brands Who Love to <span class="text-gold">Celebrate.</span></h2>
        <p class="section-deck">The same client words published on advertisingandmore.com &mdash; from partners who trust our agency with their biggest moments.</p>
      </div>
      <div class="ts-wrap" id="ts-wrap">
        <div class="ts-viewport">
          <div class="ts-track" id="ts-track">
            <figure class="ts-slide">
              <div class="ts-card">
                <img class="ts-logo" src="assets/img/testi-linkedin.png" alt="LinkedIn Corporation logo" width="160" height="40" loading="lazy">
                <figcaption class="ts-body">
                  <blockquote class="ts-quote">&ldquo;Congratulations for being the highest earners for LinkedIn. As a token of my appreciation, I would like to reward your hard work. Thank you for a job well done!&rdquo;</blockquote>
                  <div class="ts-name">LinkedIn Corporation</div>
                  <div class="ts-role">Regional Account Director, South East Asia</div>
                </figcaption>
              </div>
            </figure>
            <figure class="ts-slide">
              <div class="ts-card">
                <img class="ts-logo" src="assets/img/testi-bosch.png" alt="Bosch logo" width="160" height="40" loading="lazy">
                <figcaption class="ts-body">
                  <blockquote class="ts-quote">&ldquo;Never failed to provide sound advice &amp; solutions to optimise Bosch&rsquo;s opportunities on digital media. Impeccable professional ethics &amp; pleasant to work with. Highly recommend.&rdquo;</blockquote>
                  <div class="ts-name">Bosch</div>
                  <div class="ts-role">Corporate Communications &amp; Brand Management</div>
                </figcaption>
              </div>
            </figure>
            <figure class="ts-slide">
              <div class="ts-card">
                <img class="ts-logo" src="assets/img/testi-universal.png" alt="Universal Music Group logo" width="160" height="40" loading="lazy">
                <figcaption class="ts-body">
                  <blockquote class="ts-quote">&ldquo;Managed our campaigns on Facebook, Google, YouTube &amp; Mobile for artist launches, showcases &amp; concerts. Genuine interest in our business &amp; an open, honest approach.&rdquo;</blockquote>
                  <div class="ts-name">Universal Music Group</div>
                  <div class="ts-role">Label Manager</div>
                </figcaption>
              </div>
            </figure>
          </div>
        </div>
        <div class="ts-controls">
          <button type="button" class="ts-btn" id="ts-prev" aria-label="Previous testimonial">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          </button>
          <button type="button" class="ts-btn" id="ts-next" aria-label="Next testimonial">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
          </button>
        </div>
        <div class="ts-dots" id="ts-dots" role="tablist" aria-label="Choose testimonial"></div>
      </div>
    </div>
  </section>

  <style id="hp2-testimonials-css">
    .hp2-testimonials {
      position: relative;
      background: transparent;
      overflow: hidden;
    }
    .ts-wrap { max-width: 980px; margin: 0 auto; }
    .ts-viewport { overflow: hidden; border-radius: 22px; }
    .ts-track {
      display: flex;
      transition: transform .55s cubic-bezier(.22,.61,.36,1);
      will-change: transform;
    }
    .ts-slide { flex: 0 0 100%; min-width: 0; margin: 0; padding: 0 4px; }
    /* v5.4 — logo sits ABOVE the quote at every width (the former mobile-only
       stack is now the desktop layout too), matching the mobile arrangement */
    .ts-card {
      display: flex;
      flex-direction: column;
      gap: 18px;
      align-items: center;
      text-align: center;
      /* no card chrome — sits directly on the section's ice-blue band */
      background: transparent;
      border: none;
      border-radius: 22px;
      padding: 20px 40px 24px;
      box-shadow: none;
      height: 100%;
    }
    .ts-logo {
      width: 158px;
      height: auto;
      max-height: 60px;
      flex: 0 0 auto;
      margin: 0 auto;
      object-fit: contain;
      background: #fff;
      border: 1px solid var(--color-border);
      border-radius: 14px;
      padding: 12px 18px;
      box-shadow: 0 8px 20px rgba(11, 30, 63, .10);
    }
    .ts-quote {
      margin: 0 0 14px;
      font-size: 1.06rem;
      line-height: 1.72;
      color: #33475f;
    }
    .ts-name {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1.08rem;
      color: var(--color-primary-dark);
    }
    .ts-role { font-size: .9rem; color: var(--color-text-muted); margin-top: 2px; }
    .ts-controls { display: flex; gap: 10px; justify-content: flex-end; margin-top: 18px; }
    .ts-btn {
      width: 46px;
      height: 46px;
      border-radius: 50%;
      border: 1.6px solid rgba(213, 160, 33, .6);
      background: #fff;
      color: #D5A021;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background .25s ease, color .25s ease, transform .25s ease, box-shadow .25s ease;
    }
    .ts-btn svg { width: 20px; height: 20px; }
    .ts-btn:hover {
      background: linear-gradient(180deg, #FFD84D, #F0BE1F);
      color: #0049A8;
      border-color: #E8B915;
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(213, 160, 33, .35);
    }
    .ts-dots { display: flex; gap: 8px; justify-content: center; margin-top: 16px; }
    .ts-dot {
      width: 10px;
      height: 10px;
      padding: 0;
      border: none;
      border-radius: 50%;
      background: rgba(11, 30, 63, .22);
      cursor: pointer;
      transition: all .3s ease;
    }
    .ts-dot.is-active { width: 26px; border-radius: 999px; background: #D5A021; }
    @media (max-width: 767px) {
      .ts-card { flex-direction: column; text-align: center; gap: 18px; padding: 28px 22px; }
      .ts-logo { width: 150px; max-height: 56px; }
      .ts-quote { font-size: .96rem; line-height: 1.65; }
      .ts-controls { justify-content: center; }
    }
    @media (prefers-reduced-motion: reduce) {
      .ts-track { transition: none; }
      .ts-btn { transition: none; }
    }
  </style>
'''

PROCESS_JS = '''
  <script>
  (function () {
    /* Restart the synchronized process-flow animation every time the section
       scrolls into view, so arriving visitors always see it begin at step 1. */
    const section = document.getElementById('our-process');
    const list = section ? section.querySelector('.op-steps') : null;
    if (!section || !list) return;
    if (window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        list.classList.remove('op-run');
        void list.offsetWidth;          /* force reflow to restart keyframes */
        list.classList.add('op-run');
      });
    }, { threshold: 0.3 });
    io.observe(section);
  })();
  </script>
'''

TESTI_JS = '''
  <script>
  (function () {
    const wrap = document.getElementById('ts-wrap');
    if (!wrap) return;
    const track = document.getElementById('ts-track');
    const slides = track ? track.querySelectorAll('.ts-slide') : [];
    const dotsWrap = document.getElementById('ts-dots');
    const prev = document.getElementById('ts-prev');
    const next = document.getElementById('ts-next');
    if (slides.length < 2) return;
    const reduce = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let index = 0;
    let timer = null;

    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'ts-dot' + (i === 0 ? ' is-active' : '');
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Go to testimonial ' + (i + 1));
      dot.addEventListener('click', () => { goTo(i); restart(); });
      dotsWrap.appendChild(dot);
    });
    const dots = dotsWrap.querySelectorAll('.ts-dot');

    function render() {
      track.style.transform = 'translateX(-' + (index * 100) + '%)';
      dots.forEach((d, i) => d.classList.toggle('is-active', i === index));
    }
    function goTo(i) {
      index = (i + slides.length) % slides.length;
      render();
    }
    function restart() {
      if (reduce || !window.requestAnimationFrame) return;
      if (timer) clearInterval(timer);
      timer = setInterval(() => goTo(index + 1), 6500);
    }
    prev.addEventListener('click', () => { goTo(index - 1); restart(); });
    next.addEventListener('click', () => { goTo(index + 1); restart(); });
    wrap.addEventListener('mouseenter', () => timer && clearInterval(timer));
    wrap.addEventListener('mouseleave', restart);
    wrap.addEventListener('focusin', () => timer && clearInterval(timer));
    wrap.addEventListener('focusout', restart);

    /* touch swipe */
    let startX = null;
    track.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', (e) => {
      if (startX === null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 42) { goTo(index + (dx < 0 ? 1 : -1)); restart(); }
      startX = null;
    }, { passive: true });

    render();
    restart();
  })();
  </script>
'''

# ---------------------------------------------------------------- unified rhythm
# One fixed vertical measure for every homepage section so the page reads as
# one professional, evenly-paced composition. ID selectors + !important win
# over the site's older class-level !important section rules.
RHYTHM_CSS = '''
  <!-- v3.30 — unified section rhythm: equal top/bottom breathing room on
       Trusted brands, Top 15, Services, Drinks showcase and Enquiry -->
  <style id="unified-section-rhythm">
    :root { --uni-section-pad: clamp(2.25rem, 5vw, 4rem); }
    #trusted-brands,
    #why-choose,
    #top15,
    #services,
    #our-process,
    #happy-meeting,
    #testimonials,
    #contact {
      padding-top: var(--uni-section-pad) !important;
      padding-bottom: var(--uni-section-pad) !important;
    }
    /* The drinks section carries its top spacing on an inner wrapper;
       collapse it so the section padding alone controls the rhythm. */
    #happy-meeting .hp-showcase__inner { padding-top: 0 !important; }
    @media (max-width: 900px) {
      :root { --uni-section-pad: 2.5rem; }   /* 40px */
    }
    @media (max-width: 480px) {
      :root { --uni-section-pad: 2rem; }     /* 32px */
    }
  </style>

'''

# v5 — phone hero fix: the bottom-pinned CTA (margin-top:auto) sat flush under
# the description while the floating coffee-cup badge overshoots the pill by
# ~26px, visually covering the last line of copy. Replace the auto-pin with a
# real flow gap so the section grows with its content instead of overlapping.
HERO_FIX_CSS = '''
  <style id="v5-hero-mobile-fix">
    @media (max-width: 1023px) {
      #hero .hb-actions { margin-top: 34px !important; }
      #hero .hb-cta { margin-top: 0 !important; }
    }
  </style>

'''


# ================================================================= v3.35 world-class polish
# Audit-driven layer (no source edits, all injected at build time):
#   - honest form placeholders, optional LinkedIn, softened footer claim
#   - slim trusted-by band, hero CTA clarifier, mid-page CTA panels,
#     FAQ section + accordion, scroll reveals,
#     SEO meta + JSON-LD, image loading priorities.
#   (v5.5: pre-form reassurance cards removed at client request)
FAQ_ITEMS = [
    ("How early should we book our event?",
     "Peak dates — year-end dinners, weddings and product launches — fill up six to ten weeks ahead, so earlier is always better. Send us your date and we will confirm availability within one business day, and we always do our best to accommodate shorter timelines."),
    ("Do you handle delivery, setup and teardown?",
     "Yes. Every rental includes delivery, professional on-site setup and full teardown by our own crew, so your team never lifts a box. A dedicated coordinator stays reachable from the first briefing until the final photo."),
    ("Can rentals and booths be customised with our branding?",
     "Absolutely. As a full-service creative agency we offer agency-level branding — custom backdrops, printed props, branded photo templates, LED wraps and activations tailored to your campaign guidelines, all previewed before the event."),
    ("What kind of budgets do you work with?",
     "From intimate team celebrations to multi-zone corporate activations, every proposal is built around your goals and itemised line by line. You approve a transparent quote before anything is confirmed — no hidden fees, no surprise add-ons."),
    ("Where do you operate?",
     "We are headquartered in Kuala Lumpur and serve events across Peninsular Malaysia, with regional delivery for clients in Singapore and beyond. The first consultation is free and can run online from anywhere in the world."),
    ("What if our plans change or the event is postponed?",
     "Plans move, and we plan for that. Packages can be rescheduled with flexible date transfers, and your coordinator will walk you through the options quickly so neither the budget nor the experience is lost."),
]


def _build_faq_block():
    items = []
    for q, a in FAQ_ITEMS:
        items.append(f'''        <div class="hp3-faq-item">
          <h3 class="hp3-faq-q-wrap">
            <button type="button" class="hp3-faq-q" aria-expanded="false">
              <span>{q}</span>
              <svg class="hp3-faq-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
            </button>
          </h3>
          <div class="hp3-faq-a"><p>{a}</p></div>
        </div>''')
    return '''  <!-- ==========================================================================
       v3.35 — FAQ (objection handling + SEO), sits just before Testimonials
       ========================================================================== -->
  <section class="hp3-faq-section" id="hp3-faq" aria-labelledby="hp3-faq-heading">
    <div class="container">
      <div class="section-header-center">
        <div class="hd-eyebrow"><span class="line"></span><span>Questions, Answered</span></div>
        <h2 class="heading-display" id="hp3-faq-heading">Everything Before You <span class="text-gold">Book.</span></h2>
      </div>
      <div class="hp3-faq-list">
''' + "\n".join(items) + '''
      </div>
    </div>
  </section>

'''


BLOCK_FAQ = _build_faq_block()


POLISH_CSS = '''
  <style id="hp3-polish-css">
    html { scroll-behavior: smooth; }
    /* keep anchor targets clear of the 85px sticky header */
    #trusted-brands, #pick-your-wow, #why-choose, #party-recipes, #top15,
    #services, #featured-experiences, #our-process,
    #happy-meeting, #hp3-faq, #testimonials, #contact { scroll-margin-top: 92px; }

    /* v4.01 (client request) — hero no longer dissolves into the page at its foot */
    #hero.hb-hero::after { content: none !important; display: none !important; background: none !important; }

    /* slim trusted-by band sizing now comes from the v4.12 fragment (#trusted-brands-compact) */

    /* v5.9 — hero CTA clarifier note removed at client request; no
       replacement text is rendered under the coffee pill. */

    /* ---------- mid-page conversion panels ---------- */
    .hp3-cta {
      position: relative;
      overflow: hidden;
      max-width: 1180px;
      margin: clamp(32px, 5vw, 64px) auto;
      padding: clamp(30px, 4vw, 48px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 28px;
      border-radius: 26px;
      border: 1px solid rgba(213, 160, 33, .38);
      background: radial-gradient(120% 150% at 0% 0%, #17356e 0%, #0b1e3f 58%, #081531 100%);
      box-shadow: 0 26px 60px rgba(11, 30, 63, .24);
    }
    .hp3-cta::after {
      content: "";
      position: absolute;
      right: -90px;
      top: -90px;
      width: 280px;
      height: 280px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(240, 190, 31, .30), transparent 70%);
      pointer-events: none;
    }
    .hp3-cta__kicker {
      margin: 0 0 8px;
      font-family: var(--font-body);
      font-size: .76rem;
      font-weight: 700;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: #F0856F;
    }
    .hp3-cta__title {
      margin: 0 0 8px;
      font-family: var(--font-display);
      font-size: clamp(1.35rem, 2.4vw, 1.95rem);
      font-weight: 700;
      line-height: 1.2;
      color: #fff;
    }
    .hp3-cta__title em { font-style: normal; color: #FFD84D; }
    .hp3-cta__sub { margin: 0; font-size: .96rem; line-height: 1.6; color: rgba(255,255,255,.78); max-width: 560px; }
    .hp3-cta__btn {
      position: relative;
      z-index: 1;
      flex: 0 0 auto;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 16px 30px;
      border-radius: 999px;
      background: linear-gradient(180deg, #FFD84D, #F0BE1F);
      color: #0049A8;
      font-family: var(--font-body);
      font-weight: 800;
      font-size: .98rem;
      letter-spacing: .01em;
      text-decoration: none;
      white-space: nowrap;
      box-shadow: 0 14px 30px rgba(240, 190, 31, .35);
      transition: transform .3s cubic-bezier(.22,.61,.36,1), box-shadow .3s ease;
    }
    .hp3-cta__btn:hover { transform: translateY(-3px); box-shadow: 0 20px 38px rgba(240, 190, 31, .45); }
    .hp3-cta__btn svg { width: 18px; height: 18px; }
    @media (max-width: 760px) {
      .hp3-cta { flex-direction: column; text-align: center; gap: 20px; padding: 30px 22px; }
      .hp3-cta__sub { margin-inline: auto; }
    }

    /* v5.5 — pre-form reassurance cards removed at client request */

    /* ---------- FAQ ---------- */
    .hp3-faq-section {
      position: relative;
      background: transparent;
      padding-top: var(--uni-section-pad);
      padding-bottom: var(--uni-section-pad);
    }
    .hp3-faq-list { max-width: 860px; margin: 0 auto; display: grid; gap: 14px; }
    .hp3-faq-item {
      background: linear-gradient(180deg, #fdfaf3, #fbf3e2);
      border: 1px solid rgba(213, 160, 33, .22);
      border-radius: 16px;
      overflow: hidden;
      transition: border-color .3s ease, box-shadow .3s ease;
    }
    .hp3-faq-item.is-open {
      border-color: rgba(213, 160, 33, .6);
      box-shadow: 0 16px 34px rgba(11, 30, 63, .10);
    }
    .hp3-faq-q-wrap { margin: 0; }
    .hp3-faq-q {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 20px 24px;
      border: 0;
      background: none;
      cursor: pointer;
      text-align: left;
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1.05rem;
      color: #20304D;
    }
    .hp3-faq-icon {
      flex: 0 0 auto;
      width: 22px;
      height: 22px;
      color: #D5A021;
      transition: transform .35s cubic-bezier(.22,.61,.36,1);
    }
    .hp3-faq-item.is-open .hp3-faq-icon { transform: rotate(45deg); }
    .hp3-faq-a {
      max-height: 0;
      overflow: hidden;
      transition: max-height .4s cubic-bezier(.22,.61,.36,1);
      padding: 0 24px;
    }
    .hp3-faq-a p {
      margin: 0;
      padding-bottom: 20px;
      font-size: .95rem;
      line-height: 1.72;
      color: var(--color-text-muted);
    }

    /* FAQ heading parity with the three v3.31 section headings */
    #hp3-faq .section-header-center .heading-display {
      margin: 0 auto;
      max-width: 63%;
      padding: 6px 0 14px;
      font-family: var(--font-display);
      font-size: 46.8px;
      font-weight: 600;
      line-height: 1.1;
      letter-spacing: -.01em;
      color: #20304D;
      text-align: center;
      text-wrap: balance;
      font-optical-sizing: none;
      font-variation-settings: 'opsz' 14;
    }
    #hp3-faq .section-header-center .heading-display::after { content: none !important; display: none !important; }
    #hp3-faq .section-header-center .heading-display .text-gold { position: relative; display: inline-block; color: #A16D12; }
    #hp3-faq .section-header-center .heading-display .text-gold::after {
      content: "";
      position: absolute;
      left: 0;
      bottom: -5px;
      width: 100%;
      height: 6px;
      border-bottom: 2px solid #D3A15F;
      border-radius: 0 0 50% 50%;
      box-shadow: 0 2px 3px rgba(211, 161, 95, .25), 0 4px 8px rgba(211, 161, 95, .20);
    }
    #hp3-faq .section-header-center .hd-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-family: var(--font-body);
      font-size: 13.68px;
      font-weight: 600;
      line-height: 1.65;
      letter-spacing: .1em;
      text-transform: uppercase;
      color: #F0553A;
      margin-bottom: 12px;
      justify-content: center;
    }
    #hp3-faq .section-header-center .hd-eyebrow .line {
      width: 22px; height: 2px; border-radius: 2px; background: #D5A021; box-shadow: none;
    }
    @media (max-width: 767px) {
      #hp3-faq .section-header-center .hd-eyebrow { font-size: 12.4762px; letter-spacing: .1em; }
      #hp3-faq .section-header-center .heading-display { max-width: 100%; font-size: 32.832px; }
      .hp3-faq-q { font-size: .98rem; padding: 17px 18px; }
      .hp3-faq-a { padding: 0 18px; }
      .hp3-faq-a p { padding-bottom: 17px; font-size: .9rem; }
    }

    /* ---------- scroll reveal (Top 15 keeps its own is-inview system) ---------- */
    .reveal {
      opacity: 0;
      transform: translateY(26px);
      transition: opacity .7s cubic-bezier(.22,.61,.36,1), transform .7s cubic-bezier(.22,.61,.36,1);
      will-change: opacity, transform;
    }
    .reveal.is-visible { opacity: 1; transform: none; }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
      .hp3-faq-a { transition: none; }
      .hp3-faq-icon { transition: none; }
    }

    /* ---------- v3.36 sticky category filter (catalogue of 100) ---------- */
    #services .category-tabs-container {
      position: sticky;
      top: calc(var(--header-h, 84px) + 10px);
      z-index: 30;
      background: rgba(247, 237, 220, .94);
      backdrop-filter: blur(10px) saturate(1.1);
      -webkit-backdrop-filter: blur(10px) saturate(1.1);
      border: 1px solid rgba(161, 109, 18, .18);
      border-radius: 16px;
      box-shadow: 0 10px 26px rgba(32, 48, 77, .10);
      padding: 10px 12px;
      margin-bottom: 26px;
    }
    @media (max-width: 640px) {
      #services .category-tabs-container {
        top: calc(var(--header-h, 76px) + 8px);
        padding: 8px 10px;
        border-radius: 14px;
      }
    }

    /* ---------- v3.36 drinks section trim (~30% shorter) ---------- */
    #happy-meeting .hp-showcase__leadbox { padding-bottom: 12px; }
    #happy-meeting .hp-showcase__lead { font-size: 16px; }
    #happy-meeting .hp-showcase__grid--drinks { gap: 12px; max-width: 560px; }
    #happy-meeting .hp-showcase__drank { padding: 13px 14px; border-radius: 16px; }
    #happy-meeting .hp-showcase__iconblock { margin-bottom: 10px; }
    #happy-meeting .hp-showcase__iconblock img { height: 56px; }
    #happy-meeting .hp-showcase__dranktitle { margin-bottom: 4px; font-size: 14px; }
    #happy-meeting .hp-showcase__signoffwrap { padding-top: 12px; }
    #happy-meeting .hp-showcase__signoff { font-size: 22px; }
    @media (max-width: 640px) {
      #happy-meeting .hp-showcase__grid--drinks { gap: 10px; }
      #happy-meeting .hp-showcase__iconblock img { height: 46px; }
      #happy-meeting .hp-showcase__drank { padding: 10px 8px; }
    }

    /* ---------- v3.36 de-emphasise the non-funnel Careers link ---------- */
    .site-nav .nav-link[href*="job-vacancy"] { opacity: .8; font-weight: 500; }
    .site-nav .nav-badge-pill { background: rgba(240, 133, 111, .6); padding: 1px 6px; }

    /* ---------- v3.36 unified CTA label fits every pill context ---------- */
    @media (min-width: 1025px) and (max-width: 1280px) {
      .site-nav { gap: 14px; }
      .site-nav .nav-list { gap: 14px; }
      .site-nav .nav-link { font-size: .85rem; }
      .brand-logo .name { white-space: nowrap; }
      .btn-coffee-pill.header-btn { font-size: .74rem; padding: 9px 16px 9px 64px; }
      .btn-coffee-pill.header-btn img.coffee-cup-badge { width: 64px; }
    }
    @media (max-width: 760px) {
      .foot-cta-exact .btn-coffee-pill span { white-space: normal; line-height: 1.2; }
    }
  </style>
'''


POLISH_JS = '''
  <script>
  (function () {
    "use strict";
    var reduce = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---- 1. mid-page CTA panels ---- */
    function ctaBand(kicker, titleHtml, sub) {
      var wrap = document.createElement('div');
      wrap.className = 'hp3-cta';
      wrap.innerHTML =
        '<div class="hp3-cta__text">' +
          '<p class="hp3-cta__kicker">' + kicker + '</p>' +
          '<h3 class="hp3-cta__title">' + titleHtml + '</h3>' +
          '<p class="hp3-cta__sub">' + sub + '</p>' +
        '</div>' +
        '<a class="hp3-cta__btn" href="#contact">' +
          'Request a Quote' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>' +
        '</a>';
      return wrap;
    }
    var t15 = document.getElementById('top15');
    if (t15 && t15.nextElementSibling &&
        !t15.nextElementSibling.classList.contains('hp3-cta')) {
      t15.insertAdjacentElement('afterend', ctaBand(
        'Shortlist ready?',
        'Turn your favourites into a <em>tailored proposal.</em>',
        'Tell us your date and crowd size and we will turn your wishlist into an itemised quote — usually within one business day.'
      ));
    }
    var services = document.getElementById('services');
    if (services) {
      services.insertAdjacentElement('afterend', ctaBand(
        '100+ experiences, one point of contact',
        'Mix rentals, booths and F&amp;B into <em>one seamless event.</em>',
        'No juggling multiple vendors. One coordinator plans, books, sets up and runs every moving piece on your behalf.'
      ));
    }

    /* v5.5 — reassurance cards above the enquiry form removed at client request */

    /* ---- 2. FAQ accordion ---- */
    document.querySelectorAll('.hp3-faq-q').forEach(function (btn) {
      var item = btn.closest('.hp3-faq-item');
      var panel = item.querySelector('.hp3-faq-a');
      btn.addEventListener('click', function () {
        var open = item.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        panel.style.maxHeight = open ? panel.scrollHeight + 'px' : '0px';
      });
    });
    window.addEventListener('resize', function () {
      document.querySelectorAll('.hp3-faq-item.is-open .hp3-faq-a').forEach(function (p) {
        p.style.maxHeight = p.scrollHeight + 'px';
      });
    });

    /* ---- 3. scroll reveal (excludes #top15, which has its own system) ---- */
    var SELECTORS = [
      '#why-choose .section-header-center',
      '#why-choose .wc-card',
      '#our-process .section-header-center',
      '#happy-meeting .section-header-center',
      '#testimonials .section-header-center',
      '#testimonials .ts-card',
      '#hp3-faq .section-header-center',
      '.hp3-faq-item',
      '.hp3-cta',
      '#contact .section-header-center',
      '#plan-band .plan-col'
    ];
    var targets = [];
    SELECTORS.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        if (el.classList.contains('reveal')) return;
        el.classList.add('reveal');
        targets.push(el);
      });
    });
    /* gentle stagger inside card groups */
    document.querySelectorAll('#why-choose .wc-card, .hp3-faq-item').forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i, 5) * 80 + 'ms';
    });
    /* plan-band columns: quote first, conversion column a beat later */
    document.querySelectorAll('#plan-band .plan-col').forEach(function (el, i) {
      el.style.transitionDelay = (i * 140) + 'ms';
    });
    if (reduce || !('IntersectionObserver' in window) ||
        !window.requestAnimationFrame) {
      targets.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      /* Deterministic reveal: rAF-throttled position check on scroll/resize.
         More reliable than threshold-based IO across instant jumps and
         smooth anchor scrolling — an element reveals as soon as its top
         crosses the lower 12% of the viewport, regardless of scroll speed. */
      var pending = targets.slice();
      function check() {
        var vh = window.innerHeight || document.documentElement.clientHeight;
        for (var i = pending.length - 1; i >= 0; i--) {
          var el = pending[i];
          if (el.getBoundingClientRect().top < vh * 0.88) {
            el.classList.add('is-visible');
            pending.splice(i, 1);
          }
        }
        if (!pending.length) {
          window.removeEventListener('scroll', onScroll, { passive: true });
          window.removeEventListener('resize', onScroll);
        }
      }
      var ticking = false;
      function onScroll() {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () { check(); ticking = false; });
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
      check();
    }
  })();

  /* ---- v5.3 trusted-brands: seamless, viewport-proof logo marquee ----
     The source markup ships two mirrored groups animated with a -50%
     translate. When one group is narrower than the viewport the loop
     exposes an empty right edge (the reported "logos vanish on the
     right" bug). Clone the base group until BOTH halves are wider than
     the container, then scale duration to the half width so the travel
     speed stays constant at every breakpoint. */
  (function () {
    var rows = document.querySelectorAll('#trusted-brands .hp-logo-marquee');
    if (!rows.length) return;
    var reduce = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var SPEED = 30;                 /* px per second, forward row */
    var SPEED_REVERSE = 34;         /* opposite row drifts a touch faster */

    function cloneGroup(base) {
      var c = base.cloneNode(true);
      c.setAttribute('data-clone', '');
      c.setAttribute('aria-hidden', 'true');
      c.querySelectorAll('img').forEach(function (img) {
        img.setAttribute('alt', '');
        img.setAttribute('loading', 'lazy');
        img.setAttribute('decoding', 'async');
      });
      return c;
    }

    function halfWidth(track, mirrorEl) {
      /* width of everything in the track before the mirror half begins */
      var w = 0, node = track.firstElementChild;
      while (node && node !== mirrorEl) {
        w += node.getBoundingClientRect().width;
        node = node.nextElementSibling;
      }
      return w;
    }

    function fillRow(marquee) {
      var track = marquee.querySelector('.hp-logo-track');
      var groups = track.querySelectorAll('.hp-logo-group');
      var base = track.querySelector('[data-base]') || groups[0];
      var mirror = track.querySelector('[data-mirror]') || groups[1];
      if (!base || !mirror) return;
      base.setAttribute('data-base', '');
      mirror.setAttribute('data-mirror', '');
      /* undo clones from a previous (resize) run */
      track.querySelectorAll('[data-clone]').forEach(function (n) { n.remove(); });

      var containerW = marquee.clientWidth || window.innerWidth;
      var baseW = base.getBoundingClientRect().width;
      if (!baseW || !containerW) return;
      /* each half must clear the container, plus a quarter-group buffer so
         the masked fade edges never meet a hard content boundary. A
         measure-and-grow loop (rather than one computed count) stays
         correct through mid-animation resize reflows. */
      var target = containerW + baseW * 0.25;
      var copies = 1, guard = 0;
      while (halfWidth(track, mirror) < target && guard < 12) {
        track.insertBefore(cloneGroup(base), mirror);   /* grow first half */
        track.appendChild(cloneGroup(base));            /* grow mirror half */
        copies++; guard++;
      }

      if (!reduce) {
        var halfW = baseW * copies;
        var speed = marquee.classList.contains('hp-logo-marquee-reverse')
          ? SPEED_REVERSE : SPEED;
        track.style.animationDuration = (halfW / speed).toFixed(2) + 's';
      }
    }

    function fillAll() { rows.forEach(fillRow); }
    /* verify after layout settles (covers late viewport changes / font
       swaps that shift card widths); only refills when a half fell short */
    function verifyFill() {
      rows.forEach(function (marquee) {
        var track = marquee.querySelector('.hp-logo-track');
        var mirror = track.querySelector('[data-mirror]');
        var containerW = marquee.clientWidth || window.innerWidth;
        if (mirror && halfWidth(track, mirror) < containerW) fillRow(marquee);
      });
    }

    var resizeTimer = null;
    function onResize() {
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(fillAll, 150);
    }
    fillAll();
    requestAnimationFrame(function () { requestAnimationFrame(verifyFill); });
    window.addEventListener('load', verifyFill);
    window.addEventListener('resize', onResize, { passive: true });
  })();
  </script>
'''


def _head_extras():
    description = ("Party services and event rentals in Kuala Lumpur — 360 video booths, glam photo "
                   "studios, immersive games, live F&B and full-service planning for corporate and "
                   "private celebrations, delivered end to end by Advertising & More.")
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ_ITEMS
        ],
    }
    biz_ld = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Advertising & More Sdn. Bhd. — Party Services & Rentals",
        "url": "https://advertisingandmore.com/",
        "description": description,
        "address": {"@type": "PostalAddress", "addressLocality": "Kuala Lumpur",
                    "addressCountry": "MY"},
        "areaServed": ["Malaysia", "Singapore", "Worldwide"],
        "knowsAbout": ["Event Rentals", "Photo Booth", "360 Video Booth",
                       "Corporate Events", "Event Planning"],
    }
    return '''  <meta name="description" content="''' + description + '''">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Party Services & Rentals | Advertising & More Sdn. Bhd.">
  <meta property="og:description" content="''' + description + '''">
  <meta property="og:site_name" content="Advertising &amp; More">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">''' + json.dumps(biz_ld, ensure_ascii=False) + '''</script>
  <script type="application/ld+json">''' + json.dumps(faq_ld, ensure_ascii=False) + '''</script>
'''


HEAD_EXTRAS = _head_extras()


ASSET_DIR = "/home/user/assets/img"
ASSET_REL = "assets/img"
_DATA_URI_RE = re.compile(r'data:image/(jpeg|jpg|png|webp|gif);base64,([A-Za-z0-9+/=]+)(["\'])', re.IGNORECASE)


def _externalize_images(html):
    """Move every inline data-URI image (img src, JSON catalogue blob, CSS
    url()) to a cached WebP file under assets/img. Content-hash dedupes
    identical bytes; WebP sources pass through untouched (no re-encode loss),
    JPEGs re-encode at q82, PNGs keep alpha via lossless WebP."""
    import hashlib
    from io import BytesIO
    from PIL import Image

    if os.path.isdir(ASSET_DIR):
        for old in os.listdir(ASSET_DIR):
            os.remove(os.path.join(ASSET_DIR, old))
    os.makedirs(ASSET_DIR, exist_ok=True)

    seen = {}          # content hash -> relative url
    replaced = 0
    saved_bytes = 0

    def _to_file(mime, raw):
        key = hashlib.sha256(raw).hexdigest()[:12]
        if key in seen:
            return seen[key]
        name = "hp-%s.webp" % key
        path = os.path.join(ASSET_DIR, name)
        mime = mime.lower()
        if mime == "webp":
            with open(path, "wb") as fh:
                fh.write(raw)  # already WebP — pass through, zero generation loss
        else:
            im = Image.open(BytesIO(raw))
            if mime == "png" or mime == "gif":
                im.save(path, "WEBP", lossless=True, quality=100, method=6)
            else:
                im.convert("RGB").save(path, "WEBP", quality=82, method=6)
        url = "%s/%s" % (ASSET_REL, name)
        seen[key] = url
        return url

    def _repl(m):
        nonlocal replaced, saved_bytes
        mime, b64, quote = m.group(1), m.group(2), m.group(3)
        raw = base64.b64decode(b64)
        saved_bytes += len(b64)
        url = _to_file(mime, raw)
        replaced += 1
        return url + quote

    html = _DATA_URI_RE.sub(_repl, html)
    asset_bytes = sum(os.path.getsize(os.path.join(ASSET_DIR, f))
                      for f in os.listdir(ASSET_DIR))
    print("images externalized : %d uris -> %d webp files | base64 %.2f MB -> assets %.2f MB"
          % (replaced, len(seen), saved_bytes / 1048576, asset_bytes / 1048576))
    return html


def _optimize_images(html):
    """Hero imagery stays eager+high-priority for LCP; every other <img> without
    an explicit loading policy becomes lazy + async-decoded."""
    def _hero(m):
        return re.sub(r"<img\b(?![^>]*loading=)",
                      '<img loading="eager" decoding="async" fetchpriority="high"',
                      m.group(0))
    html = re.sub(r'<section[^>]*id="hero"[\s\S]*?</section>', _hero, html, count=1)
    html = re.sub(r"<img\b(?![^>]*loading=)",
                  '<img loading="lazy" decoding="async"', html)
    return html


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        html = f.read()

    anchor = '''  <!-- ==========================================================================
       OUR SERVICES SECTION (100% ORGANIZED BY 10 CHATGPT CATEGORIES)
       ========================================================================== -->'''
    assert html.count(anchor) == 1, "services anchor not unique/found"
    assert html.count("</body>") == 1, "body close not unique"
    assert 'id="t15-grid"' not in html, "section already present"

    block_b = BLOCK_B.replace("__CURATED_JSON__", json.dumps(
        [{"key": k, "type": t, "hook": h} for k, t, h in CURATED]
    )).replace("__ICONS_JSON__", json.dumps(ICON_URIS))

    # ---- heading parity: make #top15 heading obey the EXACT same scoped
    # rules the source applies to #services/#contact headings (font, color,
    # #A16D12 gold + underline, ::after gradient-line removal, mobile sizes).
    parity = [
        # scoped eyebrow typography/color
        (1, """    #services .section-header-center .hd-eyebrow,
    #contact .section-header-center .hd-eyebrow {
      display: inline-flex;""",
            """    #services .section-header-center .hd-eyebrow,
    #top15 .section-header-center .hd-eyebrow,
    #contact .section-header-center .hd-eyebrow {
      display: inline-flex;"""),
        # scoped eyebrow line/dot decoration
        (1, """    #services .section-header-center .hd-eyebrow .line,
    #contact .section-header-center .hd-eyebrow .line,
    #services .section-header-center .hd-eyebrow .dot,
    #contact .section-header-center .hd-eyebrow .dot {""",
            """    #services .section-header-center .hd-eyebrow .line,
    #top15 .section-header-center .hd-eyebrow .line,
    #contact .section-header-center .hd-eyebrow .line,
    #services .section-header-center .hd-eyebrow .dot,
    #top15 .section-header-center .hd-eyebrow .dot,
    #contact .section-header-center .hd-eyebrow .dot {"""),
        # main desktop heading rule (unique: followed by margin: 0 auto)
        (1, """    #services .section-header-center .heading-display,
    #contact .section-header-center .heading-display {
      margin: 0 auto;""",
            """    #services .section-header-center .heading-display,
    #top15 .section-header-center .heading-display,
    #contact .section-header-center .heading-display {
      margin: 0 auto;"""),
        # gradient-line ::after removal — present in TWO style blocks
        (2, """    #services .section-header-center .heading-display::after,
    #contact .section-header-center .heading-display::after {""",
            """    #services .section-header-center .heading-display::after,
    #top15 .section-header-center .heading-display::after,
    #contact .section-header-center .heading-display::after {"""),
        # gold span color
        (1, """    #services .section-header-center .heading-display .text-gold,
    #contact .section-header-center .heading-display .text-gold {""",
            """    #services .section-header-center .heading-display .text-gold,
    #top15 .section-header-center .heading-display .text-gold,
    #contact .section-header-center .heading-display .text-gold {"""),
        # gold span hand-drawn underline
        (1, """    #services .section-header-center .heading-display .text-gold::after,
    #contact .section-header-center .heading-display .text-gold::after {""",
            """    #services .section-header-center .heading-display .text-gold::after,
    #top15 .section-header-center .heading-display .text-gold::after,
    #contact .section-header-center .heading-display .text-gold::after {"""),
        # mobile eyebrow sizing
        (1, """      #services .section-header-center .hd-eyebrow,
      #contact .section-header-center .hd-eyebrow {""",
            """      #services .section-header-center .hd-eyebrow,
      #top15 .section-header-center .hd-eyebrow,
      #contact .section-header-center .hd-eyebrow {"""),
        # mobile heading size (unique: followed by max-width: 100%)
        (1, """      #services .section-header-center .heading-display,
      #contact .section-header-center .heading-display {
        max-width: 100%;""",
            """      #services .section-header-center .heading-display,
      #top15 .section-header-center .heading-display,
      #contact .section-header-center .heading-display {
        max-width: 100%;"""),
    ]
    for expected, old, new in parity:
        got = html.count(old)
        assert got == expected, "parity selector count %d != %d for %r" % (got, expected, old[:60])
        html = html.replace(old, new)

    # ---- v3.35 — honest copy, softer claims, image loading priorities ----
    def _swap(old, new, count=1):
        assert html.count(old) == count, "swap target missing/not unique: %r" % old[:70]
        return html.replace(old, new)

    html = _swap('placeholder="Ursula Francis Joseph D’Silva-D’Cruz"',
                 'placeholder="Your full name"')
    html = _swap('placeholder="10 800 8989"', 'placeholder="e.g. 10 800 8989"')
    html = _swap('placeholder="https://www.linkedin.com/in/tanyahyacinthfernandez"',
                 'placeholder="linkedin.com/in/your-profile (optional)"')
    html = _swap('autocomplete="url" required>', 'autocomplete="url">')  # LinkedIn now optional
    html = _swap('placeholder="dominic@ibm.com"', 'placeholder="you@company.com"')
    # v5 — seal keeps the parent site's exact "100% Success Rate" badge wording
    # (advertisingandmore.com owns and defends this agency-wide claim itself).

    # ---- v5 — parent-native two-tier CTA system ----
    # Tier 1 (brand pills, header/footer/hero/form): "CLICK FOR COFFEE",
    #   the exact signature CTA used across advertisingandmore.com — left untouched.
    # Tier 2 (in-content band buttons): explicit "Request a Quote", matching the
    #   client's own party-page mockups (IMG_1969 / IMG_1994).
    assert html.count(">CLICK FOR COFFEE<") == 4, "brand CTA count changed"
    html = _swap("<span>Book Your Event</span>", "<span>Request a Quote</span>")
    if "<span>REQUEST DIRECT QUOTE</span>" in html:
        html = html.replace("<span>REQUEST DIRECT QUOTE</span>",
                            "<span>REQUEST A QUOTE</span>")
    # JS-built mid-page CTA bands carry the same label inside POLISH_JS (edited
    # at source in the ctaBand() helper) — no runtime swap needed here.

    # ---- v5 — consent checkboxes: opt-in, never pre-checked (GDPR-safe) ----
    html = _swap('<input id="homepageCompanyProfile" type="checkbox" name="checkbox-1[]" value="one" checked>',
                 '<input id="homepageCompanyProfile" type="checkbox" name="checkbox-1[]" value="one">')
    html = _swap('<input id="homepageMonthlyTips" type="checkbox" name="checkbox-2[]" value="one" checked>',
                 '<input id="homepageMonthlyTips" type="checkbox" name="checkbox-2[]" value="one">')

    # ---- v5 — footer: replace Cloudflare-obfuscated email with the real,
    # publicly published inbox shown on the parent site and client mockups ----
    html = _swap(
        '<a class="footer-email-link" href="/cdn-cgi/l/email-protection#1d75787171725d7c796b786f69746e74737a7c737970726f78337e7270">'
        '<span class="__cf_email__" data-cfemail="f49c9198989bb49590829186809d879d9a93959a90999b8691da979b99">'
        '[email&#160;protected]</span></a>',
        '<a class="footer-email-link" href="mailto:hello@advertisingandmore.com">'
        'hello@advertisingandmore.com</a>')

    # ---- v5 — full-inventory heading: specific benefit over generic label ----
    html = _swap('Everything for your <span class="text-gold">special events.</span>',
                 '100 ways to make your event <span class="text-gold">unforgettable.</span>')

    # ---- v5 — strip Cloudflare-platform tags: they only exist on CF edge
    # servers (which re-inject them automatically) and 404 on a static export ----
    html = _swap('<script data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/'
                 'cloudflare-static/email-decode.min.js"></script>', '')
    _cf = re.findall(r"<script>\(function\(\)\{function c\(\).*?challenge-platform"
                     r".*?</script>", html)
    assert len(_cf) == 2, "expected 2 CF challenge scripts, found %d" % len(_cf)
    html = re.sub(r"<script>\(function\(\)\{function c\(\).*?challenge-platform"
                  r".*?</script>", "", html)
    # keep every header/footer CTA inside the single-page funnel
    assert html.count('href="https://advertisingandmore.com/#contactform"') == 6
    html = html.replace('href="https://advertisingandmore.com/#contactform"', 'href="#contact"')

    # v5.9 — the standalone package ships no job-vacancy-page.html, so the
    # three Careers links would 404 on GitHub Pages; point them at the live
    # site like every other header/footer navigation link.
    assert html.count('href="./job-vacancy-page.html#vacancies"') == 3
    html = html.replace('href="./job-vacancy-page.html#vacancies"',
                        'href="https://advertisingandmore.com/job-vacancy-page.html#vacancies"')

    # v4.30 — add-only wishlist helper for the party-recipe cards
    html = _swap("      window.syncWishlistButtons = syncWishlistButtons;",
                 "      /* v4.30 add-only helper for party-recipe cards */\n"
                 "      window.addToWishlist = function (key) {\n"
                 "        if (!catalogData[key]) return false;\n"
                 "        if (wishlist.has(key)) { syncWishlistButtons(); return false; }\n"
                 "        setWishlist(key, true);\n"
                 "        return true;\n"
                 "      };\n"
                 "      window.syncWishlistButtons = syncWishlistButtons;")

# image externalization runs after every section/script is injected (see end of main)

    # ---- v3.31 — three funnel sections (Why Choose / Process / Testimonials)
    block_why = BLOCK_WHY.replace("__NEW_SECTION_HEADER_CSS__", NEW_SECTION_HEADER_CSS)
    for _i in range(1, 5):
        block_why = block_why.replace("__ICO_WC_%d__" % _i, BRAND_ICONS["wc-%d" % _i])
    block_process = BLOCK_PROCESS.replace("__OP_KEYFRAMES__", OP_KEYFRAMES)
    for _i in range(1, 6):
        block_process = block_process.replace("__ICO_OP_%d__" % _i, BRAND_ICONS["op-%d" % _i])
    # v5 — real, parent-published brand testimonials (logo images, no stock faces)
    block_testi = BLOCK_TESTI
    happy_anchor = '<section class="hp-showcase" id="happy-meeting"'
    contact_anchor = '<section class="homepage-contact-section" id="contact"'
    assert html.count(happy_anchor) == 1, "happy-meeting anchor not unique/found"
    assert html.count(contact_anchor) == 1, "contact anchor not unique/found"
    assert 'id="why-choose"' not in html and 'id="our-process"' not in html \
        and 'id="testimonials"' not in html, "v3.31 sections already present"

    assert html.count("</head>") == 1, "head close not unique"
    html = html.replace("</head>", HEAD_EXTRAS + RHYTHM_CSS + HERO_FIX_CSS + POLISH_CSS
                        + FRAG_BRAND_ALIGN + FRAG_TRUST_COMPACT + "</head>", 1)
    # v5 native funnel: trust -> stats+disclaimer -> featured aspiration ->
    # Branson quote -> Why Choose -> recipes -> Top15 -> WOW orientation ->
    # full inventory (#services, WOW moved here in v5.7) -> process -> drinks ...
    # v5.7 — WOW band moved directly above the services catalogue (#services):
    # its six category cards deep-link into the catalogue filters, so sitting
    # immediately above the target section makes the click path contiguous.
    html = html.replace(anchor, BLOCK_STATS + FRAG_FEATURED + BLOCK_QUOTE
                        + block_why + FRAG_RECIPES + BLOCK_A + FRAG_WOW + anchor, 1)
    html = html.replace(happy_anchor, block_process + happy_anchor, 1)
    html = html.replace(contact_anchor, BLOCK_FAQ + block_testi + contact_anchor, 1)
    # v5.1 — plan band directly above the navy footer
    _footer_marker = '<footer class="site-footer" id="site-footer">'
    assert html.count(_footer_marker) == 1, "footer marker not unique/found"
    html = html.replace(_footer_marker, BLOCK_PLAN + "\n" + _footer_marker, 1)
    html = html.replace("</body>", block_b + TESTI_JS + PROCESS_JS + POLISH_JS + "</body>", 1)

    # ---- image pipeline last: every inline URI (including injected blocks) ----
    html = _externalize_images(html)
    html = _optimize_images(html)
    _hm = re.search(r'<section[^>]*id="hero"[\s\S]*?<img\b[^>]*\bsrc="([^"]+)"', html)
    if _hm:
        hero_rel = _hm.group(1)
        preload = ('<link rel="preload" as="image" href="%s" fetchpriority="high">'
                   % hero_rel)
        # social share card: 1200x630 JPEG (crawlers prefer JPEG over WebP)
        from PIL import Image as _PILImage
        og_abs = os.path.join(os.path.dirname(OUT), "assets", "img", "og-image.jpg")
        with _PILImage.open(os.path.join(os.path.dirname(OUT), hero_rel)) as im:
            im = im.convert("RGB")
            tw, th = 1200, 630
            scale = max(tw / im.width, th / im.height)
            im2 = im.resize((round(im.width * scale), round(im.height * scale)))
            left = (im2.width - tw) // 2
            top = max(0, (im2.height - th) // 3)   # bias toward the upper third
            im2.crop((left, top, left + tw, top + th)).save(og_abs, "JPEG", quality=84)
        og_meta = ('  <meta property="og:image" content="assets/img/og-image.jpg">\n'
                   '  <meta property="og:image:width" content="1200">\n'
                   '  <meta property="og:image:height" content="630">\n'
                   '  <meta property="og:image:alt" content="Party services and event rentals by Advertising & More">\n'
                   '  <meta name="twitter:image" content="assets/img/og-image.jpg">\n')
        html = html.replace('"address": {"@type": "PostalAddress"',
                            '"image": "assets/img/og-image.jpg",\n        "address": {"@type": "PostalAddress"', 1)
        html = html.replace("</head>", preload + "\n" + og_meta + "</head>", 1)

    assert "__PHOTO_" not in html and "__NEW_SECTION" not in html and "__ICO_" not in html \
        and "__OP_KEYFRAMES__" not in html, "unresolved build token"
    assert "data:image" not in html, "inline data URIs remain"

    # v5 — copy the three real client-published testimonial logos (downloaded
    # from advertisingandmore.com) into the page's static asset folder.
    brand_src = "/home/user/assets/brand"
    brand_dst = os.path.join(os.path.dirname(OUT), "assets", "img")
    for _src_name, _dst_name in (
        ("LI-Logo.png", "testi-linkedin.png"),
        ("bosch-tc.png", "testi-bosch.png"),
        ("universal-tc.png", "testi-universal.png"),
        ("dentsu-tc.png", "testi-dentsu.png"),
    ):
        shutil.copyfile(os.path.join(brand_src, _src_name),
                        os.path.join(brand_dst, _dst_name))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    print("curated items :", len(CURATED))
    print("output        :", OUT)
    print("size          : %.2f MB" % (os.path.getsize(OUT) / 1024 / 1024))


if __name__ == "__main__":
    main()
