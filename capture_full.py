"""Full-page image capture: scrolls the whole page so every lazy image loads
and every one-shot reveal finishes, then takes a complete-page screenshot."""
from playwright.sync_api import sync_playwright

URL = "file:///home/user/party-services-rentals-top15.html"
JOBS = [
    ("desktop", 1440, 900, 1),
    ("mobile", 390, 844, 2),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, w, h, dsf in JOBS:
        page = browser.new_page(viewport={"width": w, "height": h},
                                device_scale_factor=dsf)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(800)
        # walk the page top -> bottom in viewport steps to trigger IO reveals
        total = page.evaluate("document.documentElement.scrollHeight")
        step = h - 120
        y = 0
        while y < total:
            page.evaluate("(v) => window.scrollTo(0, v)", y)
            page.wait_for_timeout(220)
            y += step
        # let the longest one-shot animation (process reveal, 4.8s) fully settle
        page.wait_for_timeout(6500)
        # verify every image actually decoded (walk again if any lazy one missed)
        missing = page.evaluate(
            "Array.from(document.images).filter(i => !i.complete || i.naturalWidth===0).length")
        if missing:
            total = page.evaluate("document.documentElement.scrollHeight")
            y = 0
            while y < total:
                page.evaluate("(v) => window.scrollTo(0, v)", y)
                page.wait_for_timeout(180)
                y += h - 120
            page.wait_for_timeout(3000)
        # freeze the FINAL visual state. The process section's IntersectionObserver
        # restarts its reveal on the full-page viewport resize, so hard-pin those
        # elements to their end state instead of merely pausing mid-cycle.
        page.add_style_tag(content="""
          .op-ic, .op-arrow, .op-title, .op-text, .op-steps, .op-steps::before {
            opacity: 1 !important; transform: none !important;
            animation: none !important;
          }
          .reveal, .t15-card { opacity: 1 !important; transform: none !important; }
          *, *::before, *::after { animation-play-state: paused !important; }
        """)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        page.screenshot(path=f"/home/user/full-page-{name}.png", full_page=True)
        print(name, "captured")
        page.close()
    browser.close()
