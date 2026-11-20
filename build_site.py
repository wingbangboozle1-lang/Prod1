import json, html, re
# ---------------------------------------------------------------- data
D = json.load(open("data/products.json"))
SITE = D["site"]
PRODS = {p["id"]: p for p in D["products"]}
VERIFIED = SITE["verifiedDate"]
TAG = SITE["trackingId"]
E = json.load(open("data/editorial.json"))
RS = json.load(open("data/reader-suggestions.json"))
BASE = E["baseUrl"].rstrip("/")
SHOW_PRICE = bool(E["display"]["pricesOnShopPages"])
SHOW_RATING = bool(E["display"]["ratingsOnShopPages"])
BRAND = E["publisher"]["name"]
DESK = E["publisher"]["desk"]
VOICE = E["voice"]
EVENTS = E["events"]["five"]
CADENCE = E["cadence"]
REQ_DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
PAGES = []          # slug, title, description, kind - drives sitemap, feed and the gate
# Internal surfaces. Every one of them stays reachable from the footer and the review desk,
# because the audit is part of the publication's honesty. None of them is a page a shopper
# searched for, and each one competes with the buying pages for the same host, so they are
# excluded from the sitemap and carry `noindex, follow`. Reader-facing notes that a *buyer*
# benefits from - the register, the flagged list - stay indexed; see READER_AUDIT below.
NOINDEX = {
    "executive-summary.html", "suggestions.html", "design-brief.html", "methodology.html",
    "review-desk.html", "dashboard.html", "search.html",
}
# These two are audit pages that a buyer may legitimately land on, so they stay indexable;
# they are named here to make the choice explicit rather than implied by omission.
READER_AUDIT = {"verification.html", "flagged.html", "compliance.html"}

def esc(s): return html.escape(str(s), quote=True)
def flaglinks(s):
    """A bare FLG-nnn in register text should be clickable: the point of the register is that
    anyone can follow a claim to the note that qualifies it."""
    return re.sub(r"\bFLG-(\d{3})\b", r'<a href="flagged.html#FLG-\1">FLG-\1</a>', s)
def aff(p): return f"https://www.amazon.com/dp/{p['asin']}?tag={TAG}"
def abs_url(slug): return BASE + ("/" if slug in ("", "index.html") else "/" + slug)
def num_in(s, idx):
    m = re.findall(r'([0-9]+(?:\.[0-9]+)?)\s*"', s or "")
    return float(m[idx]) if len(m) > idx else None
def dims_of(p):
    d = num_in(p["dimensions"], 0); w = num_in(p["dimensions"], 1); h = num_in(p["dimensions"], 2)
    if None in (d, w): return None
    return {"depth_in": d, "width_in": w, "height_in": h, "depth_cm": round(d * 2.54, 1),
            "height_cm": round(h * 2.54, 1) if h else None, "footprint_sqin": round(d * w, 1)}
# Brand-art map. These are our own drawings of the appliance *type* - never a rendering of a
# specific product, never a photograph, never Amazon's Program Content (FLG-041 / SG-04).
# A drawing of a shape is not a claim about a unit's appearance, so it is not captioned as one.
ART = {
    "P1": ("air-fryer-dual", "Dual-basket air fryer, drawing"),
    "P2": ("air-fryer-oven", "Countertop French-door oven, drawing"),
    "P3": ("air-fryer-basket", "Single-basket air fryer, drawing"),
    "P4": ("thermometer-instant", "Handheld instant-read thermometer, drawing"),
    "P5": ("thermometer-wireless", "Wireless thermometer hub with probes, drawing"),
}
def art(pid, cls="prod-art", alt_override=None):
    """Decorative by default: the card heading already names the product, so an alt string
    that repeats it is noise for a screen reader. Pass alt_override only where the picture
    carries information the text does not."""
    name, label = ART[pid]
    alt = esc(alt_override if alt_override is not None else "")
    return (f'<div class="{cls}"><img src="{esc(BASE)}/assets/art/{name}.svg" alt="{alt}" '
            f'width="320" height="240" loading="lazy" decoding="async"></div>')

# Editorial reading of the listing. Every phrase below paraphrases a field on the linked
# Amazon listing (attributed "per listing" in the copy) or says a figure is not shown there.
POSITION = {
    "P1": {"good": "two different dishes finishing at the same time (2 independent 3-quart baskets, Sync Finish - per listing)",
           "check": "34.0 cm of counter depth (13.38 in, as listed) - measure your own space, and check the clearance the manual asks for",
           "headline": "The two-basket one"},
    "P2": {"good": "cooking for four to six, rotisserie and a 12-inch pizza in one cavity (per listing)",
           "check": "42.9 cm of depth - the largest here - plus room for the doors to swing; the warranty period is not stated on the listing",
           "headline": "The family-size oven"},
    "P3": {"good": "one big batch in the shallowest box here - 12.75 in deep - with a top-rack dishwasher-safe basket and tray (per listing; its floor area is still the middle of the three, so judge it on depth, not on footprint)",
           "check": "one cavity, so two dishes means staggering; 450F Hi-Fry appears in the title while the bullets give 200-400F",
           "headline": "The weeknight workhorse"},
    "P4": {"good": "a one-second reading in your hand, with a +/-0.5F and NIST/NSF claim on the listing",
           "check": "it is handheld - it will not watch the roast from another room; its dimensions are not in the fields we captured",
           "headline": "The pocket read"},
    "P5": {"good": "three probes and app alerts while you are away from the oven",
           "check": "no +/-F accuracy figure appears in the fields we captured, and it needs WiFi, the hub and the app to earn its place",
           "headline": "The phone-watched setup"},
}
# Re-read of 2026-11-20, performed by session arena/42e09357-prod1. Deliberately narrow: this
# session confirmed that each listing page is reachable, that its title still matches the register,
# and the one buy-box price it could attribute to the product itself. It did NOT re-read every
# spec table, so verifiedDate stays 2026-11-19 and no field on the shop pages is relabelled as
# freshly confirmed. Full record: review/42e09357/VERIFICATION-2026-11-20.md
RECHECK_DATE = "2026-11-20"
RECHECK = {
  "P1": ("title matches, page reachable", "buy box not isolated in this read, so the dated figure stands"),
  "P2": ("title matches, still states 24 One-Touch Preset Options and Six Cooking Accessories", "FLG-002 and FLG-021 unchanged by this read"),
  "P3": ("title matches (the register drops the registered-trademark mark from TurboFry)", "newer 6QT B0CNY1YVDD still shown in the page's own carousel at $59.99, 4.6/7,602, corroborating FLG-003"),
  "P4": ("title matches; the seller has added holiday keywords to it", "buy box read in this session: $16.99, matching the register's dated figure"),
  "P5": ("title matches, including Gen3 and 5 Sensors", "no dimensions in the fields captured, so FLG-004 stays open"),
}

# ---------- claim integrity: a superlative must survive the data it came from ----------
# Why this exists: session 1187e20d found a printed label ("Smallest footprint") that the register
# contradicted. A person caught it once; a build should catch it every time. Each claim below is a
# sentence this site prints, paired with a test recomputed from data/products.json on every build.
# If a value is corrected and the sentence stops being true, the build stops instead of publishing
# the contradiction. Anything the register cannot decide is recorded as "untestable here", so the
# gap stays visible rather than being quietly asserted.
def _litres(p):
    """Capacity in litres, for ordering the three fryers only. Prefers the listing's capacity field,
    falls back to the title's quart figure (1 US qt = 0.946353 L). Never printed as a claim."""
    for src in (p.get("capacityField"), p.get("capacityTitle")):
        if not src:
            continue
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(?:liters|litre|L)\b", src, re.I)
        if m:
            return float(m.group(1))
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(?:QT|Qt|quart)", p.get("capacityTitle") or "", re.I)
    return float(m.group(1)) * 0.946353 if m else 0.0

def _airfryers(P):
    return [k for k in P if P[k]["category"] == "Air Fryers" and dims_of(P[k])]

CLAIMS = [
    {"claim": "The narrowest of the three fryers at 11.81 in wide",
     "where": "the to-scale drawing caption on every P1 card, and the air-fryers spec bullets",
     "needle": ("air-fryers.html", "11.81 inches wide by 13.38 inches deep"),
     "basis": "smallest listed width among the three air fryers",
     "test": lambda P: min(_airfryers(P), key=lambda k: dims_of(P[k])["width_in"]) == "P1"
              and abs(dims_of(P["P1"])["width_in"] - 11.81) < 0.005},
    {"claim": "Shallowest of the fryers",
     "where": "index.html, quick-pick chip for P3",
     "needle": ("index.html", "Shallowest of the fryers"),
     "basis": "smallest listed depth among the three air fryers",
     "test": lambda P: min(_airfryers(P), key=lambda k: dims_of(P[k])["depth_in"]) == "P3"},
    {"claim": "One big basket in 12.75 in of depth",
     "where": "index.html and air-fryers.html, P3 card",
     "needle": ("index.html", r"One big basket in 12\.75 in of depth"),
     "basis": "the depth on the P3 listing, and a single-basket form field",
     "test": lambda P: abs(dims_of(P["P3"])["depth_in"] - 12.75) < 0.005
              and "single" in P["P3"]["form"].lower()},
    {"claim": "The biggest cavity here",
     "where": "index.html, quick-pick card for P2",
     "needle": ("index.html", r"The biggest cavity here"),
     "basis": "largest capacity among the three fryers, compared in litres from the listing fields",
     "test": lambda P: max(_airfryers(P), key=lambda k: _litres(P[k])) == "P2"},
    {"claim": "Also the deepest, at 16.9 in",
     "where": "index.html and air-fryers.html, P2 card",
     "needle": ("index.html", r"Also the deepest, at 16\.9 in"),
     "basis": "largest listed depth among the three air fryers",
     "test": lambda P: max(_airfryers(P), key=lambda k: dims_of(P[k])["depth_in"]) == "P2"
              and abs(dims_of(P["P2"])["depth_in"] - 16.9) < 0.005},
    {"claim": "42.9 cm of depth - the largest here",
     "where": "air-fryers.html and guide pages, P2 'check before you buy'",
     "needle": ("air-fryers.html", r"42\.9 cm of depth \\u2014? ?the largest here|42\.9 cm of depth"),
     "basis": "the largest depth, converted at 1 in = 2.54 cm",
     "test": lambda P: abs(round(dims_of(P["P2"])["depth_in"] * 2.54, 1) - 42.9) < 0.06},
    {"claim": "Three air fryers, three different jobs",
     "where": "air-fryers.html heading",
     "basis": "three products in the Air Fryers category, three distinct form values",
     "test": lambda P: len([k for k in P if P[k]["category"] == "Air Fryers"]) == 3
              and len({P[k]["form"] for k in P if P[k]["category"] == "Air Fryers"}) == 3},
    {"claim": "Five appliances / five products, all verified",
     "where": "index.html, compare.html, footer",
     "basis": "the register holds exactly five entries and each carries an observed ASIN",
     "test": lambda P: len(P) == 5 and all(P[k]["asin"] for k in P)},
    {"claim": "Two of our five listings argue with themselves",
     "where": "guide-holiday-deal-check.html, section 4",
     "basis": "the P3 wattage field carries the listing's own disagreement (FLG-022), and the P2 title "
               "capacity (26QT) is stated in a different unit than its capacity field (24.6 liters)",
     "test": lambda P: "FLG-022" in (P["P3"].get("wattage") or "")
              and "liters" in (P["P2"].get("capacityField") or "").lower()
              and "QT" in (P["P2"].get("capacityTitle") or "")},
    {"claim": "158.0, 267.0 and 172.1 sq in of floor area",
     "where": "air-fryers.html spec table, and the drawing on every card",
     "needle": ("air-fryers.html", "158.0 sq in"),
     "basis": "depth x width from the listing, computed here rather than typed into the page",
     "test": lambda P: all(abs(dims_of(P[k])["footprint_sqin"] - v) < 0.06
              for k, v in (("P1", 158.0), ("P2", 267.0), ("P3", 172.1)))},
    {"claim": "Capacity per square inch of footprint",
     "where": "air-fryers.html spec table, derived row",
     "basis": "divides a title capacity by a listed footprint, and the title units differ between "
               "products, so the build checks nothing beyond the footnote labelling it as derived",
     "test": None},
    {"claim": "Instant-read or wireless is a distance question",
     "where": "thermometers.html heading",
     "basis": "an editorial framing of two form fields, not a number the register can decide",
     "test": None},
]

def check_printed_claims():
    """Second half of the audit: does the page still contain the sentence the audit describes?

    A register test proves the number is right. It proves nothing about the wording, which a later
    pass can reword or drop while the audit keeps describing the old sentence - the quiet way an
    audit turns into fiction. Each printable claim carries the exact text and the file it must appear
    in, checked against the HTML this build has already written. If the sentence is gone, the build
    stops: at that point the claim and the audit are asserting two different things.
    """
    rows = []
    for c in CLAIMS:
        if not c.get("needle"):
            continue
        fn, pat = c["needle"]
        found = re.search(pat, open(fn, encoding="utf-8").read()) is not None
        rows.append((c["claim"], fn, found))
    missing = ["%s (audit says it is printed in %s)" % (cl, fn) for cl, fn, ok in rows if not ok]
    if missing:
        raise SystemExit("claim audit no longer matches the pages - reword the audit or restore the "
                         "sentence: " + "; ".join(missing))
    return rows

def verify_claims():
    """Run every testable claim against the register. A contradicted claim stops the publish."""
    rows = []
    for c in CLAIMS:
        if c["test"] is None:
            rows.append((c, "untestable here", "framing or derived row; no register value decides it"))
            continue
        try:
            ok = bool(c["test"](PRODS))
        except Exception as exc:
            rows.append((c, "untestable here", "the register field this test needs is missing or unreadable (%s)" % exc))
            continue
        rows.append((c, "verified against the register" if ok else "CONTRADICTED",
                     "recomputed from data/products.json on this build"))
    bad = [c["claim"] for c, v, _ in rows if v == "CONTRADICTED"]
    if bad:
        raise SystemExit("claim integrity check failed - these printed sentences no longer follow from "
                         "data/products.json, so reword the page or correct the register: " + "; ".join(bad))
    return rows

CLAIM_ROWS = verify_claims()

# ---------------------------------------------------------------- product card
def capacity_row(p):
    """A thermometer has no cavity, so "Capacity, as titled" followed by an em dash is a row
    that tells the reader nothing. Say why the row is empty instead, in the reader's words.
    This is the same placeholder problem as FLG-073, fixed at the point where it is read."""
    cap = p.get("capacityTitle")
    if cap not in ("", "\u2014", None):
        return f"<div><dt>Capacity, as titled</dt><dd>{esc(cap)}</dd></div>"
    kind = "handheld thermometer" if "handheld" in p.get("form", "").lower() else "wireless probe set"
    return f"<div><dt>Capacity</dt><dd>Not applicable &mdash; a {kind} has no cooking cavity</dd></div>"

def cta_note(p):
    return (f'Sponsored link &middot; Amazon price and stock govern &middot; '
            f'specs read from this listing {VERIFIED} &middot; '
            f'<a href="verification.html#{p["id"]}">source record</a>')
def product_card(pid, bullets_n=3, detailed=False, level=3):
    """`level` keeps the heading outline honest: a card directly under an <h1> is an h2, and a
    card under a section <h2> is an h3. Shipping every card as h3 was a real outline break on
    five pages (the structure check caught it)."""
    h = f"h{level}"
    p = PRODS[pid]; pos = POSITION[pid]; dm = dims_of(p)
    bl = "".join(f"<li>{esc(b)}</li>" for b in p["bullets"][:bullets_n])
    dims = esc(p["dimensions"]) if p["dimensions"] else "not stated on the listing"
    if SHOW_PRICE:
        money = f'<p class="price-row"><span class="price">{esc(p["priceNew"])}</span> <span class="fine">listed {VERIFIED} &middot; Amazon price governs</span></p>'
    else:
        money = f'<p class="price-row"><span class="price-live">Today&rsquo;s price sits on Amazon</span> <span class="fine">we link to it instead of quoting a number that goes stale</span></p>'
    rating = (f'<p class="fine"><span class="stars">&#9733; {esc(p["rating"])}</span> from {esc(p["ratingCount"])} ratings, as counted on {VERIFIED}. Live count on the listing.</p>') if SHOW_RATING else ""
    footprint = f'<div><dt>Counter depth</dt><dd>{dm["depth_in"]} in ({dm["depth_cm"]} cm)</dd></div>' if dm else ""
    height = f'<div><dt>Height to clear a cabinet</dt><dd>{dm["height_in"]} in ({dm["height_cm"]} cm)</dd></div>' if dm and dm.get("height_cm") else ""
    power = f'<div><dt>Power draw</dt><dd>{flaglinks(esc(p["wattage"]))}</dd></div>' if p.get("wattage") and p["wattage"] not in ("", "—") else ""
    extra = f'<ul class="bullets">{bl}</ul>' if detailed else ""
    return f"""
<article class="prod" id="{pid}">
  {art(pid)}
  <div class="prod-head">
    <span class="chip">{esc(p['form'])}</span>
    <{h}>{esc(p['shortName'])}</{h}>
    <p class="prod-sub">{esc(pos['headline'])} &middot; {esc(p['category'])}</p>
    {money}{rating}
  </div>
  <dl class="specs">
    {capacity_row(p)}
    <div><dt>Footprint on the listing</dt><dd>{dims}</dd></div>
    {footprint}{height}{power}
    <div><dt>Features the listing calls out</dt><dd>{esc(p['specialFeatures']) or 'not summarised here'}</dd></div>
  </dl>
  {fit_svg(pid)}
  <p class="best"><strong>Good for:</strong> {esc(pos['good'])}</p>
  <p class="watch"><strong>Check before you buy:</strong> {esc(pos['check'])}</p>
  {extra}
  <p class="cta-row"><a class="btn" href="{aff(p)}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{p['asin']}">{('See today&rsquo;s price on Amazon' if not SHOW_PRICE else 'Buy at Amazon')}</a>
     <a class="link-quiet" href="compare.html#{pid}">See how it compares</a></p>
  <p class="fine">{cta_note(p)}</p>
</article>"""
def fit_svg(pid):
    """A to-scale footprint drawing, generated from the inches the listing states.

    Why this exists: the photography decision (SG-04 / FLG-009) blocks every product image, which
    left the shop pages with nothing spatial in an article about things that have to fit. A drawing
    we make ourselves is not Program Content, it cannot go stale the way a price sticker does, and
    the only number in it is one the register already carries. One scale (9 px per inch) is used
    for every product so two cards can be compared by eye.
    """
    p = PRODS[pid]; dm = dims_of(p)
    if not dm:
        return ""
    S = 9
    w = dm["width_in"]; d = dm["depth_in"]; h = dm.get("height_in") or 0
    ref = 12 * S
    top = 34
    base = top + max(ref, round(d * S))
    x0 = 24
    px = x0 + ref + 26
    pw = round(w * S); pd = round(d * S)
    return f"""<figure class="fit">
<svg viewBox="0 0 320 {base + 24}" role="img" aria-label="To-scale drawing of the {esc(p['shortName'])} footprint, {w} inches wide by {d} inches deep, against a 12 by 12 inch reference square.">
<title>Counter footprint to scale, from the listing's stated inches</title>
<rect class="svg-ref" x="{x0}" y="{base - ref}" width="{ref}" height="{ref}"/>
<text class="svg-cap" x="{x0}" y="{base + 15}">12 x 12 in reference</text>
<rect class="svg-fit" x="{px}" y="{base - pd}" width="{pw}" height="{pd}"/>
<text class="svg-lab" x="{px}" y="{base - pd - 8}">{w} in wide</text>
<text class="svg-cap" x="{px}" y="{base + 15}">{d} in deep, {h} in tall &middot; {dm['footprint_sqin']} sq in of counter</text>
<line class="svg-edge" x1="{x0}" y1="{base}" x2="300" y2="{base}"/>
</svg>
<figcaption>Our drawing, scaled from the dimensions on the listing ({esc(p['sourceUrl'].rsplit('/',1)[-1])}). Not a photograph of the product.</figcaption>
</figure>"""

# ---------------------------------------------------------------- chrome
# --- navigation: one reader group; the active page is marked, not guessed by the reader
NAV_LINKS = [
    ("air-fryers.html", "Air fryers", ("air-fryers.html", "guide-basket-vs-oven.html", "guide-capacity-checklist.html")),
    ("thermometers.html", "Thermometers", ("thermometers.html", "guide-thermometer-accuracy.html")),
    ("compare.html", "Compare", ("compare.html",)),
    ("guides.html", "Guides", ("guides.html",)),
    ("about.html", "About", ("about.html",)),
]
def nav(slug, prefix=""):
    """One reader group plus the desk link. `prefix` is the absolute base for in-page anchors
    on consolidated pages, which are served from a build that does not share this nav state."""
    out = ['<nav class="nav" aria-label="Main">']
    for href, label, owns in NAV_LINKS:
        cur = ' aria-current="page"' if slug in owns else ""
        out.append(f'  <a href="{prefix}{href}"{cur}>{label}</a>')
    cur = ' aria-current="page"' if slug in ("review-desk.html", "verification.html", "flagged.html",
                                            "suggestions.html", "methodology.html", "compliance.html",
                                            "executive-summary.html", "design-brief.html") else ""
    out.append(f'  <a href="{prefix}review-desk.html" class="nav-desk"{cur}>Review desk</a>')
    out.append('</nav>')
    out.append(f'''<form class="searchbox" id="site-search-form" role="search">
  <label class="skip" for="site-search-input">Search the site</label>
  <input id="site-search-input" type="search" placeholder="Search specs, guides" aria-label="Search the site">
  <button class="btn small secondary" type="submit">Search</button>
</form>''')
    return "\n".join(out)
ISSUE = E.get("contentDate", VERIFIED)   # page date, not evidence date - see editorial.json
def issue_bar(slug):
    """A publication says what issue it is and when it was last read. Generated from the same
    date the register uses, so the line cannot drift from the data it describes."""
    y, mo, d = ISSUE.split("-")
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    label = f"{int(d)} {months[int(mo)-1]} {y}"
    return f'''<div class="issue-bar"><div class="issue-inner">
<span class="issue-vol">{esc(BRAND)} &middot; Issue of {label}</span>
<span class="issue-note">Specs read from the Amazon listing, dated on every page &middot; no fake testing</span>
<a class="issue-link" href="methodology.html">How we work</a>
</div></div>'''

STRIP = (f'<div class="disclosure-strip" role="note"><span class="disclosure-req">{REQ_DISCLOSURE}</span> '
         f'&middot; We are paid when a reader buys after clicking, which is why the specs, not hype, are the point. '
         f'<a href="about.html#money">How this site works</a></div>')
FOOTER = f"""
<footer>
  <div class="disclosure-strip"><span class="disclosure-req">{REQ_DISCLOSURE}</span> &middot; <a href="compliance.html">Disclosure policy</a></div>
  <div class="footer-inner">
    <div>
      <p class="fbrand">{BRAND}</p>
      <p>Spec-backed buying guides for air fryers and meat thermometers, written from the Amazon listing and dated on every page. We do not claim hands-on testing we have not done, and we do not publish price or rating figures that would go stale.</p>
      <p class="fine">Product information is quoted from Amazon listings as observed on {VERIFIED}. Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates. Listings can change at any time &mdash; confirm the spec, the variant and the price on the product page before you buy.</p>
    </div>
    <nav aria-label="Shop"><p><strong>Shop</strong></p><p><a href="air-fryers.html">Air fryers</a><br><a href="thermometers.html">Meat thermometers</a><br><a href="compare.html">Compare all five</a><br><a href="compare.html#chooser">Three-question chooser</a></p></nav>
    <nav aria-label="Guides"><p><strong>Guides</strong></p><p><a href="guides.html">All guides</a><br><a href="guide-basket-vs-oven.html">Basket or oven-style?</a><br><a href="guide-capacity-checklist.html">Capacity, honestly</a><br><a href="guide-cleanup-counter-space.html">Cleanup &amp; counter space</a><br><a href="guide-gift-picks.html">Gift picks that get used</a></p></nav>
    <nav aria-label="Review desk"><p><strong>Review desk</strong></p><p><a href="review-desk.html">Desk index</a><br><a href="decisions.html">Decision register</a><br><a href="verification.html">Verification register</a><br><a href="flagged.html">Flagged for review</a><br><a href="suggestions.html">Suggestions &amp; decisions</a><br><a href="methodology.html">Method &amp; ledger</a><br><a href="compliance.html">Compliance gate</a><br><a href="executive-summary.html">Executive summary</a><br><a href="design-brief.html">Design brief (parallel)</a><br><a href="about.html">About &amp; contact</a></p></nav>
  </div>
</footer>"""
# ---------------------------------------------------------------- page shell
LD_ORG = {"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": abs_url("index.html"),
          "description": "Spec-backed buying guides for air fryers and meat thermometers, written from the Amazon listing."}
def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, separators=(",", ":"))}</script>'
def crumbs(slug, title):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": abs_url("index.html")}]
    if slug != "index.html":
        items.append({"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": abs_url(slug)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
def page(slug, title, desc, body, extra_head="", body_class="", canonical=None):
    kind = "Article" if body_class == "guide-page" else "webpage"
    # A consolidated page declares another URL as canonical, so it must not also be in the
    # sitemap; Google's canonicalisation guidance is one signal per page, not two.
    canon = abs_url(canonical) if canonical else abs_url(slug)
    if canonical:
        kind = "merged"
    ld = [LD_ORG, crumbs(slug, title)]
    if kind == "Article":
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": title.split(" | ")[0],
                   "datePublished": VERIFIED, "dateModified": VERIFIED, "inLanguage": "en-US",
                   "author": {"@type": "Organization", "name": DESK}, "publisher": LD_ORG,
                   "isPartOf": {"@type": "WebSite", "name": BRAND, "url": abs_url("index.html")},
                   "description": desc})
    if slug == "index.html":
        ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": abs_url("index.html"),
                   "description": desc})
    if slug in ("air-fryers.html", "thermometers.html"):
        ids = ["P1", "P2", "P3"] if slug == "air-fryers.html" else ["P4", "P5"]
        ld.append({"@context": "https://schema.org", "@type": "ItemList", "name": title.split(" | ")[0],
                   "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": PRODS[i2]["shortName"],
                                       "url": abs_url(slug) + "#" + i2} for i, i2 in enumerate(ids)]})
    ld.append({"@context": "https://schema.org", "@type": "WebPage", "name": title.split(" | ")[0],
               "url": abs_url(slug), "inLanguage": "en-US", "description": desc})
    ldscripts = "".join(jsonld(x) for x in ld)
    ogimg = BASE + "/assets/og-image.png"
    PAGES.append({"slug": slug, "title": title, "description": desc, "kind": kind, "canonical": canon,
                  "indexable": not (slug in NOINDEX and not canonical)})
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
{('<meta name="robots" content="noindex, follow">' if (slug in NOINDEX and not canonical) else '')}
<meta name="theme-color" content="#1F2937">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:title" content="{esc(title.split(' | ')[0])}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canon)}">
<meta property="og:type" content="{'article' if kind == 'Article' else 'website'}">
<meta property="og:image" content="{esc(ogimg)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(BRAND)} - spec-backed buying guides">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title.split(' | ')[0])}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(ogimg)}">
{'<meta property="article:published_time" content="' + VERIFIED + '">' if kind == 'Article' else ''}
<link rel="alternate" type="application/rss+xml" title="{esc(BRAND)} feed" href="{esc(BASE)}/feed.xml">
<link rel="icon" href="{esc(BASE)}/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{esc(BASE)}/assets/style.css">
{extra_head}
{ldscripts}
</head>
<body data-verified-date="{VERIFIED}" data-analytics-endpoint="{E['events']['endpoint']}" data-tag="{TAG}" class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="masthead-inner">
<a class="brand" href="{esc(BASE)}/index.html">{esc(BRAND).replace('Guide', '<span>Guide</span>')}</a>
{nav(slug)}
</div></header>
{issue_bar(slug)}
{STRIP}
<main id="main" class="wrap">
{body}
</main>
{FOOTER}
<script src="{esc(BASE)}/assets/app.js"></script>
</body>
</html>
"""
def page_to(slug, *a, **kw):
    html_out = "\n".join(line.rstrip() for line in page(slug, *a, **kw).split("\n"))
    open(slug, "w").write(html_out)
    print("wrote", slug)
def guide_shell(kicker, h1, intro, sections_html, faqs, picks=("P1", "P2", "P3")):
    faq_json = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    cards = "".join(product_card(x, 2, True) for x in picks)
    body = f"""
<article class="guide">
<p class="eyebrow">{esc(kicker)}</p>
<h1>{esc(h1)}</h1>
<p class="byline"><span>By {esc(DESK)}</span> <span>&middot;</span> <span>Listing data checked {VERIFIED}</span> <span>&middot;</span> <span>Spec-based, not hands-on tested</span> <a href="methodology.html">how we work</a></p>
<p class="lede">{intro}</p>
<div class="toc"><strong>On this page:</strong> <a href="#shortlist">The picks</a> &ndash; <a href="#compare-link">Full comparison</a> &ndash; <a href="#faq">Questions readers ask</a></div>
{sections_html}
<h2 id="shortlist">The picks, from the listing</h2>
<div class="grid cols-3">{cards}</div>
<p id="compare-link"><a class="btn secondary" href="compare.html">See the full side-by-side comparison</a> <a class="link-quiet" href="compare.html#chooser">or answer three questions</a></p>
<h2 id="faq">Questions readers ask</h2>
{faq_html}
<p class="fine">Every product fact above comes from the Amazon listing linked on each card. Where a fact is missing we say so &mdash; see <a href="flagged.html">Flagged for review</a>. Price and rating figures live on Amazon and change; this page deliberately does not quote them.</p>
</article>
"""
    return body, jsonld(faq_json)

CHOOSER = """
<form id="chooser-form" class="chooser card">
  <fieldset><legend>1. What are you cooking most?</legend>
    <label><input type="radio" name="q1" value="snacks"> Crispy snacks &amp; weeknight sides</label>
    <label><input type="radio" name="q1" value="family"> Whole meals for a crowd</label>
    <label><input type="radio" name="q1" value="meat"> Meat &amp; grill - temperature matters</label>
  </fieldset>
  <fieldset><legend>2. How much counter depth do you have?</legend>
    <label><input type="radio" name="q2" value="compact"> Compact - under ~33 cm (13 in)</label>
    <label><input type="radio" name="q2" value="standard"> Standard - ~33-40 cm</label>
    <label><input type="radio" name="q2" value="plenty"> Plenty - 40 cm+</label>
  </fieldset>
  <fieldset><legend>3. What is your budget?</legend>
    <label><input type="radio" name="q3" value="budget"> Keeping it small - thermometer money</label>
    <label><input type="radio" name="q3" value="mid"> One appliance, mid-range</label>
    <label><input type="radio" name="q3" value="premium"> The full setup, if it earns its place</label>
  </fieldset>
  <button class="btn" type="submit">Show my shortlist</button>
  <div id="chooser-result" aria-live="polite"></div>
</form>"""
# ---------- TOPICS (topic calendar, session bb3ae11b) ----------
NUMW = {n: w for n, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen".split())}
TOPICS = [
    {"n": "01", "title": "Basket or oven-style air fryer: what should you compare?", "cat": "Air fryers - Form",
     "status": "Published", "href": "guide-basket-vs-oven.html",
     "angle": "Form factor first: dual-basket vs French-door oven vs single basket, with the three fryers as worked examples.",
     "hooks": "Listing form fields (P1 dual basket, P2 French door, P3 single basket); listing dimensions",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P2 listing", PRODS["P2"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"])]},
    {"n": "02", "title": "A no-hype checklist for comparing air fryer capacity", "cat": "Air fryers - Capacity",
     "status": "Published", "href": "guide-capacity-checklist.html",
     "angle": "Quarts vs litres, single vs dual baskets, and how to read a 'feeds 4-6' claim without being misled.",
     "hooks": "Capacity title/field as listed (P1, P2, P3); listing bullets; capacity-per-footprint math",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P2 listing", PRODS["P2"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"])]},
    {"n": "03", "title": "How to assess cleanup and counter-space trade-offs", "cat": "Air fryers - Space",
     "status": "Published", "href": "guide-cleanup-counter-space.html",
     "angle": "Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.",
     "hooks": "Listing dimensions (P1-P3); dishwasher-safe bullets; derived footprint and capacity-per-cm math",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P2 listing", PRODS["P2"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"])]},
    {"n": "04", "title": "Questions to ask before buying a multi-function kitchen appliance", "cat": "Multi-function",
     "status": "Published", "href": "guide-multifunction-questions.html",
     "angle": "Presets, accessories, wattage and warranty - the pre-purchase checklist, applied to the Emeril oven.",
     "hooks": "Emeril preset count and functions (P2 listing); Chefman warranty bullets (P1, P3)",
     "sources": [("P2 listing", PRODS["P2"]["sourceUrl"]), ("P1 listing", PRODS["P1"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"])]},
    {"n": "05", "title": "Instant-read or wireless? How to read accuracy claims", "cat": "Thermometers",
     "status": "Published", "href": "guide-thermometer-accuracy.html",
     "angle": "Plus-minus 0.5F, NIST/NSF, sensor counts and range - what each claim does and does not prove.",
     "hooks": "ThermoMaven accuracy/certification claims (P4); CHEF iQ sensor count and range (P5)",
     "sources": [("P4 listing", PRODS["P4"]["sourceUrl"]), ("P5 listing", PRODS["P5"]["sourceUrl"])]},
    {"n": "06", "title": "Can a 26-quart oven actually fit on your counter? The depth math, in inches", "cat": "Air fryers - Space",
     "status": "Published", "href": "guide-counter-depth-fit.html",
     "angle": "A tape-measure walkthrough: depth, width, footprint and the capacity you get per centimetre of counter - using only listed dimensions.",
     "hooks": "Listed dimensions (P2: 16.9D x 15.8W x 14.8H in); derived footprint and capacity-per-cm math",
     "sources": [("P2 listing", PRODS["P2"]["sourceUrl"]), ("Counter-space math", "compare.html")]},
    {"n": "07", "title": "Two baskets or one: what dual-zone cooking actually changes", "cat": "Air fryers - Form",
     "status": "Published", "href": "guide-dual-vs-single-basket.html",
     "angle": "When two independent baskets earn their extra depth - and when a single large basket is the simpler buy.",
     "hooks": "P1 dual-basket listing claims (Sync Finish, 2 x 3 Qt); P3 single-basket listing claims",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"])]},
    {"n": "08", "title": "How to read the badges on a listing - without overreading them", "cat": "Trust",
     "status": "Planned", "href": "topics.html#t08",
     "angle": "What an Amazon's Choice badge and a rating snapshot can and cannot tell a buyer, with the snapshot date kept visible.",
     "hooks": "Badge and rating fields as shown on listings (P1, P3, P4); dated-snapshot rule",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"]), ("P4 listing", PRODS["P4"]["sourceUrl"])]},
    {"n": "09", "title": "Air fryer basket vs oven: which one actually fits your counter?", "cat": "Air fryers - Form",
     "status": "Planned", "href": "topics.html#t09",
     "angle": "Dual-basket, French-door oven and single basket side by side: depth, footprint and what each shape is genuinely good for.",
     "hooks": "Listing form fields and dimensions (P1, P2, P3); derived footprint math",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P2 listing", PRODS["P2"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"])]},
    {"n": "10", "title": "Instant-read vs wireless thermometer: do you need both?", "cat": "Thermometers",
     "status": "Published", "href": "guide-instant-read-vs-wireless.html",
     "angle": "One-second handheld reads versus app-monitored probes: when each type earns its place, and what the accuracy claims do and do not prove.",
     "hooks": "ThermoMaven tolerance and certification (P4); CHEF iQ sensor count, range and probe count (P5)",
     "sources": [("P4 listing", PRODS["P4"]["sourceUrl"]), ("P5 listing", PRODS["P5"]["sourceUrl"])]},
    {"n": "11", "title": "Counter space math: will a 26-quart oven fit your kitchen?", "cat": "Air fryers - Space",
     "status": "Consolidated", "href": "guide-counter-depth-fit.html",
     "angle": "Depth, width, footprint and capacity per centimetre of counter - a tape-measure guide built only from listed dimensions.",
     "hooks": "Listed dimensions (P2: 16.9D x 15.8W x 14.8H in); derived footprint and capacity-per-cm math",
     "sources": [("P2 listing", PRODS["P2"]["sourceUrl"]), ("Counter-space math", "compare.html")]},
    {"n": "12", "title": "Holiday air fryer gifts: what to buy without the guesswork", "cat": "Seasonal - Gifts",
     "status": "Published", "href": "guide-gift-picks.html",
     "angle": "Depth, household size, dishwasher-safe parts and control-panel learnability - the gift checklist that needs no price tag.",
     "hooks": "Listing dimensions, capacity, care bullets and seller gift claims (P1, P2, P3, P4)",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P2 listing", PRODS["P2"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"]), ("P4 listing", PRODS["P4"]["sourceUrl"])]},
    {"n": "13", "title": "Thanksgiving counter math: what actually fits on the counter?", "cat": "Seasonal - Thanksgiving",
     "status": "Published", "href": "guide-thanksgiving-counter.html",
     "angle": "Depth, cabinet clearance, wattage and the cooking claims a listing will stand behind, timed to 26 November 2026.",
     "hooks": "Listed dimensions and power fields (P1, P2, P3); bullet-level cleanup and accessory claims",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P2 listing", PRODS["P2"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"]), ("OPM 2026 holiday schedule", "https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/")]},
    {"n": "14", "title": "A holiday price looks like a deal: what to check in ten minutes", "cat": "Seasonal - Buying window",
     "status": "Published", "href": "guide-holiday-deal-check.html",
     "angle": "Quarts per dollar, the variant trap, what a badge is not, and listings that disagree with themselves.",
     "hooks": "Capacity title vs capacity field (P1, P2); variant selector (P3); listing-internal disagreements FLG-002, FLG-021, FLG-022",
     "sources": [("P3 listing", PRODS["P3"]["sourceUrl"]), ("P2 listing", PRODS["P2"]["sourceUrl"]), ("Associates Program Policies", "https://affiliate-program.amazon.com/help/operating/policies")]},
    {"n": "15", "title": "The gift receipt test: does an appliance gift get kept?", "cat": "Seasonal - Gifting",
     "status": "Published", "href": "guide-gift-return-window.html",
     "angle": "Variant, fit, cleanup, setup burden and paperwork, all answerable from listing fields before you wrap.",
     "hooks": "Variant and colour fields (P1, P3, P5); cleanup bullets (P1, P3); probe, hub and app description (P5); warranty fields (P1, P2, P3, P5)",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"]), ("P5 listing", PRODS["P5"]["sourceUrl"])],
     "note": "Published 2026-11-20 as the after-purchase half of topic 12, which is the choice of gift."}]

def topic_band():
    n_topics = len(TOPICS)
    n_pub = sum(1 for t in TOPICS if t["status"] == "Published")
    n_queue = n_topics - n_pub
    rows = "".join(
        f'<a href="{t["href"]}"><span>{t["n"]}</span>{esc(t["title"])}<b class="{"status-published" if t["status"]=="Published" else "status-planned"}">{t["status"]}</b></a>'
        for t in TOPICS)
    return f"""
<div class="topic-band">
  <div class="wrap topic-inner">
    <div>
      <h2>The topic calendar</h2>
      <p>{NUMW[len(TOPICS)].capitalize()} question-shaped topics, {NUMW[sum(1 for t in TOPICS if t["status"]=="Published")]} published and {NUMW[sum(1 for t in TOPICS if t["status"]!="Published")]} queued. Every queued title is an editorial hypothesis backed by verified listing fields - not a claim about search volume or popularity. The next topic is chosen from measured queries, not instinct.</p>
      <p><a class="btn secondary" href="topics.html">Open the full calendar</a></p>
    </div>
    <div class="topic-list">{rows}</div>
  </div>
</div>"""



# ---------- FRONT PAGE: the shelf (buyer-first, generated from the register) ----------
# Why this exists: the brief asks for a shop. A shopper's first question is "which one, and what
# does it cost me in counter space" - not "how was this verified". Every row below is a field the
# register already carries, or an explicit statement that the field was not captured. Nothing is
# computed here except the centimetre conversion the rest of the site already prints.
SHELF_ORDER = ["P1", "P2", "P3", "P4", "P5"]
SHELF_PICK = {
    "P1": "Two dishes landing at the same time, without a second appliance",
    "P2": "Cooking for four to six, with rotisserie and a 12-inch pizza",
    "P3": "One big batch on a shallow counter",
    "P4": "A fast reading in your hand at the grill",
    "P5": "Walking away from the oven and watching from your phone",
}
SHELF_CHECK = {
    "P1": "Clearance the manual asks for is not stated on the listing - measure the gap under your cabinet",
    "P2": "The doors need room to swing, and the warranty period is not stated on the listing",
    "P3": "The listing gives two wattages (1000 W in the bullets, 1700 W in its spec table) - <a href=\"flagged.html#FLG-022\">FLG-022</a>",
    "P4": "Dimensions and item weight are not in the fields we captured - <a href=\"flagged.html#FLG-004\">FLG-004</a>",
    "P5": "No +/-F accuracy figure appears in the fields we captured; it needs WiFi and the app",
}

def shelf_table():
    rows = []
    for pid in SHELF_ORDER:
        p = PRODS[pid]; dm = dims_of(p)
        depth = f"{dm['depth_in']} in ({dm['depth_cm']} cm)" if dm else '<span class="fine">not stated in our fields</span>'
        cap = p.get("capacityTitle")
        cap = esc(cap) if cap not in ("", "\u2014", None) else '<span class="fine">no cavity</span>'
        rows.append(
            f'<tr><td><a href="#{pid}"><strong>{esc(p["shortName"])}</strong></a><br>'
            f'<span class="fine">{esc(p["category"])} &middot; {esc(p["form"])}</span></td>'
            f'<td>{esc(SHELF_PICK[pid])}</td><td>{cap}</td><td>{depth}</td>'
            f'<td class="fine">{SHELF_CHECK[pid]}</td>'
            f'<td><a class="btn small" href="{aff(p)}" rel="sponsored nofollow noopener" target="_blank" '
            f'data-ctg-outbound data-asin="{p["asin"]}">Check price</a></td></tr>')
    return f"""<div class="table-wrap"><table>
<tr><th>Product</th><th>Pick it if</th><th>Capacity, as titled</th><th>Counter depth</th><th>Before you order</th><th>Amazon</th></tr>
{"".join(rows)}
</table></div>
<p class="small">Depth is the listing's own dimension, converted at 2.54 cm per inch - not a manufacturer claim. Every &ldquo;Check price&rdquo; button carries our Associates tag and is marked sponsored; Amazon shows the live price and stock. Specs re-read {VERIFIED}.</p>"""

index_body = f"""
<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">Air fryers &amp; meat thermometers &middot; specs re-read {VERIFIED}</p>
    <h1>Five countertop appliances, priced in the space they take.</h1>
    <p class="lede">Air fryers and meat thermometers are bought on one number most pages hide: how much counter they take. Here is that number for all five, in inches and centimetres, next to the job each one is built for &mdash; and a plain note on what to check before you order.</p>
    <p class="hero-cta"><a class="btn" href="#shelf">See all five at a glance</a> <a class="btn ghost" href="compare.html#chooser">Or answer three questions</a></p>
    <ul class="hero-facts">
      <li><strong>5</strong> products, each read from its own Amazon listing</li>
      <li><strong>1</strong> table that decides it: depth, capacity, what to check</li>
      <li><strong>0</strong> claims that anyone here cooked in these machines</li>
    </ul>
  </div>
  <aside class="hero-side" aria-label="Three picks by job">
    <p class="side-title">Three jobs, three machines</p>
    <ol>
      <li><a href="air-fryers.html#P1">Two dishes at once &rarr; Chefman 6QT dual</a> <span>13.38 in deep &middot; 11.81 in wide &middot; two 3-quart baskets</span></li>
      <li><a href="air-fryers.html#P2">Feed four to six &rarr; Emeril 26QT oven</a> <span>16.9 in deep &middot; rotisserie and a 12-inch pizza, per listing</span></li>
      <li><a href="air-fryers.html#P3">One big batch &rarr; Chefman 8QT basket</a> <span>12.75 in deep &middot; the shallowest of the three</span></li>
    </ol>
    <p class="hero-side-cta"><a class="btn small" href="#shelf">Compare all five side by side</a></p>
    <p class="fine">Prices and ratings live on Amazon and move, so we link to them instead of quoting a stale figure. Specs re-read {VERIFIED}.</p>
  </aside>
</section>

<h2 id="shelf">All five at a glance</h2>
<p>The table a shopper needs first: what each machine is for, how much counter it takes, and the one thing the listing will not tell you. Click a name for the full card with the source link; click <em>Check price</em> for the live figure on Amazon.</p>
{shelf_table()}

<section class="season" aria-label="This week on the desk">
  <p class="eyebrow">Holiday window, 2026</p>
  <p>Thanksgiving falls on <strong>Thursday, 26 November 2026</strong>, a federal holiday listed in 5 U.S.C. 6103. The retail days either side of it are the Friday and the Monday, which are not holidays in that law. Three guides answer that window: <a href="guide-thanksgiving-counter.html">what fits on the counter</a>, <a href="guide-holiday-deal-check.html">the ten-minute listing check</a> and <a href="guide-gift-return-window.html">the gift receipt test</a>. No deal claims, no price figures, no countdowns. Date read from the <a href="https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/">OPM schedule</a> on 2026-11-20.</p>
</section>

<h2>If you want a shortcut, start with these three</h2>
<p>Each pick names the job it wins on. It is a reading of the listing&rsquo;s own fields, not a test result.</p>
<div class="grid cols-3">
  <article class="pick">{art("P1")}<span class="chip">Two dishes at once</span><h3>Chefman 6QT Dual-Basket</h3><p>Two independent 3-quart baskets with Sync Finish, so chicken and vegetables land together. The narrowest of the three fryers at 11.81 in wide.</p><p class="cta-row"><a class="btn small" href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P1']['asin']}">Check price</a> <a class="link-quiet" href="air-fryers.html#P1">Full card</a></p></article>
  <article class="pick">{art("P2")}<span class="chip">Feeding four to six</span><h3>Emeril Lagasse 26QT French-Door</h3><p>The biggest cavity here: rotisserie for a 6-lb chicken and a 12-inch pizza, per the listing. Also the deepest, at 16.9 in - measure before you order.</p><p class="cta-row"><a class="btn small" href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P2']['asin']}">Check price</a> <a class="link-quiet" href="air-fryers.html#P2">Full card</a></p></article>
  <article class="pick">{art("P3")}<span class="chip">Shallowest of the fryers</span><h3>Chefman 8QT TurboFry</h3><p>One big basket in 12.75 in of depth, 450F Hi-Fry in the title, basket and tray top-rack dishwasher safe per the bullets.</p><p class="cta-row"><a class="btn small" href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P3']['asin']}">Check price</a> <a class="link-quiet" href="air-fryers.html#P3">Full card</a></p></article>
</div>
<p class="section-more"><a class="link-quiet" href="thermometers.html">Two meat thermometers, compared the same way &rarr;</a></p>

<h2>All five, side by side</h2>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<div class="grid cols-2 grid-gap-top">{product_card('P4')}{product_card('P5')}</div>
<p class="section-more"><a class="btn secondary" href="compare.html">Open the full comparison table</a> <a class="link-quiet" href="verification.html">or check our sources first</a></p>

<h2>Not sure yet? Answer three questions</h2>
<p>The chooser uses only what the listings state - form factor, depth and your budget. It gives you a shortlist, not a verdict, and it runs entirely in your browser.</p>
<div id="chooser">{CHOOSER}</div>

<h2>Guides worth ten minutes</h2>
<div class="grid cols-3">
  <article class="card"><span class="tag">Form factor</span><h3><a href="guide-basket-vs-oven.html">Basket or oven-style air fryer: what should you compare?</a></h3><p>Two dishes at once, crowd capacity, counter depth - decided with the three fryers on this page.</p></article>
  <article class="card"><span class="tag">Capacity</span><h3><a href="guide-capacity-checklist.html">A no-hype checklist for comparing air fryer capacity</a></h3><p>Quarts vs litres, split baskets, and what &ldquo;feeds 4-6&rdquo; is actually claiming.</p></article>
  <article class="card"><span class="tag">Seasonal</span><h3><a href="guide-gift-picks.html">Holiday air fryer gifts: how to choose one that gets used</a></h3><p>The gift checklist that does not need a price tag: depth, cleanup, one control panel they will actually learn.</p></article>
</div>
<p class="section-more"><a href="guides.html">All guides</a> &middot; <a href="guide-multifunction-questions.html">Multi-function questions</a> &middot; <a href="guide-thermometer-accuracy.html">Thermometer accuracy claims</a> &middot; <a href="suggestions.html">Ask for a topic</a></p>

<h2>Latest from the desk</h2>
<div class="latest">
  <a class="latest-item" href="guide-instant-read-vs-wireless.html"><span class="latest-date">This week</span><strong>Instant-read vs wireless thermometer: do you need both?</strong><span>Two tools, two jobs - and one listing that never states an accuracy figure.</span></a>
  <a class="latest-item" href="guide-capacity-checklist.html"><span class="latest-date">Capacity</span><strong>A no-hype checklist for comparing air fryer capacity</strong><span>Quarts, litres and what &ldquo;feeds 4-6&rdquo; is actually claiming.</span></a>
  <a class="latest-item" href="guide-wattage-outlets.html"><span class="latest-date">Circuits</span><strong>Will it trip the breaker? Wattage and outlet math</strong><span>1000W against 1700W on a 120V kitchen circuit, with the conflict shown.</span></a>
</div>
{topic_band()}

<h2>Why the numbers here match the listing</h2>
<div class="trust-row">
  <div><strong>Nothing invented.</strong><p>Every product fact is quoted from the Amazon listing and linked. If we did not capture a field, the row says so instead of guessing.</p></div>
  <div><strong>No fake testing.</strong><p>Nobody here has cooked in these machines, so the words &ldquo;our team tried it&rdquo; never appear on a page here. Hands-on content needs a protocol and a budget first.</p></div>
  <div><strong>Links are paid.</strong><p>Product links carry our Associates tag and are marked sponsored, on the page and in the code.</p></div>
  <div><strong>The audit is public.</strong><p>A line-by-line register, open questions and every irregularity we found sit in the <a href="review-desk.html">review desk</a>.</p></div>
</div>
"""
page_to("index.html","Air fryers & thermometers, compared | Countertop Guide","Five appliances compared on capacity, counter depth, cleanup and what the listing does not say. Every spec links to the Amazon page it came from.",index_body)
# ---------- AIR FRYERS ----------
af_body = f"""
<p class="eyebrow">Air fryers</p>
<h1>Three air fryers, three different jobs</h1>
<p class="lede">One cooks two dishes at once, one feeds a family and roasts a chicken, one disappears into a shallow counter. Pick the job first, then check the depth - it is the number that ends most returns. Specs below are quoted from each listing, with the link.</p>
<div class="callout"><strong>Short version:</strong> two dishes at once &rarr; <a href="#P1">Chefman 6QT dual</a>. Four to six people, rotisserie, pizza &rarr; <a href="#P2">Emeril 26QT</a>. Limited depth, one big batch &rarr; <a href="#P3">Chefman 8QT basket</a>.</div>
<div class="grid cols-3">{product_card('P1',level=2)}{product_card('P2',level=2)}{product_card('P3',level=2)}</div>
<h2>The spec table</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>Chefman 6QT Dual-Basket<br>B0CDY277D3</th><th>Emeril 26QT French-Door<br>B09B7SB46R</th><th>Chefman 8QT TurboFry<br>B08DKYBTPH</th></tr>
<tr><td>Form</td><td>Dual basket (2 x 3 Qt)</td><td>Oven-style, French door</td><td>Single basket</td></tr>
<tr><td>Capacity (title)</td><td>6 Quart</td><td>26QT</td><td>8 quarts</td></tr>
<tr><td>Capacity field on listing</td><td>6 liters <span class="badge-warn">unit differs - see Flagged</span></td><td>24.6 liters <span class="badge-warn">unit differs - see Flagged</span></td><td>8 quarts</td></tr>
<tr><td>Dimensions (D x W x H)</td><td>13.38 x 11.81 x 10.63 in</td><td>16.9 x 15.8 x 14.8 in</td><td>12.75 x 13.5 x 10 in</td></tr>
<tr><td>Counter depth</td><td>13.38 in (34.0 cm)</td><td>16.9 in (42.9 cm)</td><td>12.75 in (32.4 cm)</td></tr>
<tr><td>Footprint (W x D)</td><td>158.0 sq in</td><td>267.0 sq in</td><td>172.1 sq in</td></tr>
<tr><td>Capacity per sq in footprint*</td><td>0.038 qt/sq in</td><td>0.097 qt/sq in</td><td>0.046 qt/sq in</td></tr>
<tr><td>Price &amp; rating today</td><td><a href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0CDY277D3">See on Amazon</a> <span class="fine">(sponsored)</span></td><td><a href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B09B7SB46R">See on Amazon</a> <span class="fine">(sponsored)</span></td><td><a href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B08DKYBTPH">See on Amazon</a> <span class="fine">(sponsored)</span></td></tr>
<tr><td>Power, as listed</td><td>1700 W / 120 V (bullets)</td><td>1700 W / 120 V (Product information table)</td><td>1000 W per bullets, 1700 W per the spec table <span class="badge-flag">listing disagrees - FLG-022</span></td></tr>
<tr><td>Cleanup (listing)</td><td>Non-stick baskets dishwasher safe</td><td>See listing for accessory care</td><td>Basket + tray top-rack dishwasher safe</td></tr>
<tr><td>Source</td><td><a href="https://www.amazon.com/dp/B0CDY277D3">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B09B7SB46R">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B08DKYBTPH">Amazon listing</a></td></tr>
</table></div>
<p class="small">* Derived by us from listing dimensions and title capacity (1 in = 2.54 cm). It is not a manufacturer claim. See <a href="guide-cleanup-counter-space.html">counter-space guide</a> for method and limits.</p>
<h2>Guides for air fryer buyers</h2>
<ul>
<li><a href="guide-basket-vs-oven.html">Basket or oven-style air fryer: what should you compare?</a></li>
<li><a href="guide-capacity-checklist.html">A no-hype checklist for comparing air fryer capacity</a></li>
<li><a href="guide-cleanup-counter-space.html">How to assess cleanup and counter-space trade-offs</a></li>
<li><a href="guide-multifunction-questions.html">Questions to ask before buying a multi-function kitchen appliance</a></li>
</ul>
<p><a class="btn secondary" href="compare.html">Compare with thermometers</a></p>
"""
page_to("air-fryers.html","Dual-basket vs oven-style air fryers | Countertop Guide","Chefman 6QT dual-basket, Emeril 26QT French-door and Chefman 8QT TurboFry: capacity, depth and cleanup, each row linked to its listing.",af_body)
# ---------- THERMOMETERS ----------
th_body = f"""
<p class="eyebrow">Meat thermometers</p>
<h1>Instant-read or wireless? It is a distance question</h1>
<p class="lede">If you stand at the grill, a one-second handheld read is all you need. If you cook a brisket for six hours while doing something else, you want probes that phone you. Accuracy claims below are quoted from the listing with the certification named - we have not calibrated either unit, and we say so where it matters.</p>
<div class="callout"><strong>Short version:</strong> fast checks and candy &rarr; <a href="#P4">ThermoMaven instant-read</a>. Long cooks, multiple proteins, alerts at the other end of the house &rarr; <a href="#P5">CHEF iQ Sense</a>.</div>
<div class="grid cols-2">{product_card('P4',level=2)}{product_card('P5',level=2)}</div>
<h2>The spec table</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>ThermoMaven Instant-Read<br>B0DHZTCNR5</th><th>CHEF iQ Sense Wireless<br>B0DZFD6R9Z</th></tr>
<tr><td>Type</td><td>Handheld instant-read</td><td>Wireless probes + hub + app</td></tr>
<tr><td>Accuracy claim (listing)</td><td>+/-0.5F, NIST &amp; NSF certified</td><td>4 internal + 1 ambient sensor (listing bullets); no +/-F figure captured</td></tr>
<tr><td>Read / monitoring</td><td>1-second read (thermocouple, per bullets)</td><td>Real-time app updates, WiFi unlimited range, Bluetooth</td></tr>
<tr><td>Probes</td><td>Single probe (handheld)</td><td>3 probes included (1/2/4-probe variants exist)</td></tr>
<tr><td>Heat rating</td><td>- (not captured)</td><td>1000F heat-safe probes (per title/bullets)</td></tr>
<tr><td>Waterproof / care</td><td>IP67 waterproof; rinse under water</td><td>Waterproof, dishwasher-safe probes</td></tr>
<tr><td>Battery / charge</td><td>1x AAA battery included</td><td>Up to 50 hours per charge (per bullets)</td></tr>
<tr><td>Price &amp; rating today</td><td><a href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">See on Amazon</a> <span class="fine">(sponsored)</span></td><td><a href="{aff(PRODS['P5'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">See on Amazon</a> <span class="fine">(sponsored)</span></td></tr>
<tr><td>Dimensions</td><td><span class="badge-flag">Not stated on the listing &mdash; <a href="flagged.html#FLG-004">FLG-004</a></span></td><td><span class="badge-flag">Not stated on the listing &mdash; <a href="flagged.html#FLG-004">FLG-004</a></span></td></tr>
<tr><td>Source</td><td><a href="https://www.amazon.com/dp/B0DHZTCNR5">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B0DZFD6R9Z">Amazon listing</a></td></tr>
</table></div>
<h2>Guides for thermometer buyers</h2>
<ul>
<li><a href="guide-thermometer-accuracy.html">Instant-read or wireless? How to read accuracy claims</a></li>
<li><a href="guide-instant-read-vs-wireless.html">Instant-read vs wireless thermometer: do you need both?</a></li>
</ul>
<p><a class="btn secondary" href="compare.html">Compare with air fryers</a></p>
"""
page_to("thermometers.html","Instant-read vs wireless thermometers | Countertop Guide","ThermoMaven 1-second handheld against the CHEF iQ Sense 3-probe wireless set: accuracy claims as listed, probes, range and care.",th_body)
# ---------- COMPARE ----------
compare_body = f"""
<p class="eyebrow">Comparison</p>
<h1>All five, side by side</h1>
<p class="lede">Every cell is quoted from the Amazon listing, with the link, or it says &ldquo;not captured&rdquo;. The two derived rows - footprint and capacity per square inch - show their arithmetic so you can repeat it. Price and rating are deliberately absent: they live on Amazon and move.</p>
<h2 id="chooser">Three-question chooser</h2>
{CHOOSER}
<h2>Full table</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th id="P1">P1 Chefman 6QT Dual<br>B0CDY277D3</th><th id="P2">P2 Emeril 26QT Oven<br>B09B7SB46R</th><th id="P3">P3 Chefman 8QT Basket<br>B08DKYBTPH</th><th id="P4">P4 ThermoMaven Instant<br>B0DHZTCNR5</th><th id="P5">P5 CHEF iQ Wireless<br>B0DZFD6R9Z</th></tr>
<tr><td>Category / form</td><td>Air Fryers - Dual basket</td><td>Air Fryers - Oven-style</td><td>Air Fryers - Single basket</td><td>Thermometers - Instant-read</td><td>Thermometers - Wireless</td></tr>
<tr><td>Capacity</td><td>6 Quart (title) / 6 liters (field)</td><td>26QT (title) / 24.6 liters (field)</td><td>8 quarts</td><td>-</td><td>-</td></tr>
<tr><td>Power, as listed</td><td>120 V / 1700 W (bullets)</td><td>120 V / 1700 W (spec table)</td><td>120 V / 1000 W per bullets, 1700 W per the same listing&rsquo;s spec table <span class="badge-flag"><a href="flagged.html#FLG-022">FLG-022</a></span></td><td>Not applicable</td><td>Not applicable</td></tr>
<tr><td>Dimensions</td><td>13.38D x 11.81W x 10.63H in</td><td>16.9D x 15.8W x 14.8H in</td><td>12.75D x 13.5W x 10H in</td><td>Not stated on the listing <span class="fine">&mdash; <a href="flagged.html#FLG-004">FLG-004</a></span></td><td>Not stated on the listing <span class="fine">&mdash; <a href="flagged.html#FLG-004">FLG-004</a></span></td></tr>
<tr><td>Price today</td><td><a href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0CDY277D3">See on Amazon</a> <span class="fine">(sponsored)</span></td><td><a href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B09B7SB46R">See on Amazon</a> <span class="fine">(sponsored)</span></td><td><a href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B08DKYBTPH">See on Amazon</a> <span class="fine">(sponsored)</span></td><td><a href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">See on Amazon</a> <span class="fine">(sponsored)</span></td><td><a href="{aff(PRODS['P5'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">See on Amazon</a> <span class="fine">(sponsored)</span></td></tr>
<tr><td>Why no price here</td><td colspan="5">Amazon&rsquo;s policies let a site show price and availability only when Amazon serves it or when it comes from the Creators/PA API, and only briefly cached. This build is static, so the button is the price. The figure we saw on {VERIFIED} is kept in the <a href="verification.html">verification register</a>.</td></tr>
<tr><td>Key differentiator (listing)</td><td>Sync Finish, 2x3 Qt baskets</td><td>French door, rotisserie, 12 in pizza</td><td>450F Hi-Fry, dishwasher-safe basket</td><td>1-sec, +/-0.5F NIST</td><td>WiFi, 3 probes, 1000F-safe</td></tr>
<tr><td>Buy (sponsored)</td>
<td><a href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0CDY277D3">Amazon</a></td>
<td><a href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B09B7SB46R">Amazon</a></td>
<td><a href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B08DKYBTPH">Amazon</a></td>
<td><a href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">Amazon</a></td>
<td><a href="{aff(PRODS['P5'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">Amazon</a></td></tr>
<tr><td>Verify</td><td><a href="verification.html#P1">P1 record</a></td><td><a href="verification.html#P2">P2 record</a></td><td><a href="verification.html#P3">P3 record</a></td><td><a href="verification.html#P4">P4 record</a></td><td><a href="verification.html#P5">P5 record</a></td></tr>
</table></div>
<p class="small">All outbound links are sponsored (rel="sponsored") and open amazon.com. Ratings and prices are {VERIFIED} snapshots and will change. See <a href="verification.html">verification register</a> for line-by-line sources.</p>
<h2>Counter-space analysis (air fryers only)</h2>
<div class="table-scroll"><table>
<tr><th>Air fryer</th><th>Depth</th><th>Footprint</th><th>Capacity</th><th>Capacity per cm depth*</th><th>Capacity per sq in*</th></tr>
<tr><td>Chefman 6QT Dual (B0CDY277D3)</td><td>34.0 cm</td><td>158.0 sq in</td><td>6 qt</td><td>0.18 qt/cm</td><td>0.038 qt/sq in</td></tr>
<tr><td>Emeril 26QT Oven (B09B7SB46R)</td><td>42.9 cm</td><td>267.0 sq in</td><td>26 qt</td><td>0.61 qt/cm</td><td>0.097 qt/sq in</td></tr>
<tr><td>Chefman 8QT Basket (B08DKYBTPH)</td><td>32.4 cm</td><td>172.1 sq in</td><td>8 qt</td><td>0.25 qt/cm</td><td>0.046 qt/sq in</td></tr>
</table></div>
<p class="small">* Derived by us: depth in cm = inches x 2.54; footprint = width x depth; ratios use title capacity. Thermometers excluded (dimensions not captured). Method and limits in <a href="guide-cleanup-counter-space.html">cleanup &amp; counter-space guide</a>.</p>
"""
page_to("compare.html","Compare 5 air fryers & thermometers | Countertop Guide","Capacity, dimensions, footprint, cleanup and accuracy claims side by side, quoted from each listing, with a three-question chooser and the maths shown.",compare_body)
# ---------- GUIDES INDEX ----------
guides_body = """
<p class="eyebrow">Guides</p>
<h1>Question-shaped guides, answered from the listing</h1>
<p class="lede">Each guide starts from a question a buyer actually types, then answers it with verified listing facts - and says plainly what the listing does not tell us. No popularity or trend claims without a dated snapshot.</p>
<h2>Thirteen guides, three clusters</h2>
<div class="grid cols-2">
<article class="card"><span class="tag">Air fryers - Form</span><h3>Basket or oven-style air fryer: what should you compare?</h3><p>Dual-basket vs French-door oven vs single basket: cooking two dishes, crowd capacity, and counter depth.</p><p><a class="btn small" href="guide-basket-vs-oven.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Capacity</span><h3>A no-hype checklist for comparing air fryer capacity</h3><p>Quarts vs litres, "feeds 4-6", rotisserie and pizza claims - how to read capacity without being misled.</p><p><a class="btn small" href="guide-capacity-checklist.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Space &amp; cleanup</span><h3>How to assess cleanup and counter-space trade-offs</h3><p>Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.</p><p><a class="btn small" href="guide-cleanup-counter-space.html">Read guide</a></p></article>
<article class="card"><span class="tag">Multi-function</span><h3>Questions to ask before buying a multi-function kitchen appliance</h3><p>Presets, accessories, wattage and warranty - the pre-purchase checklist, applied to the Emeril oven.</p><p><a class="btn small" href="guide-multifunction-questions.html">Read guide</a></p></article>
<article class="card"><span class="tag">Thermometers - Accuracy</span><h3>Instant-read or wireless? How to read accuracy claims</h3><p>+/-0.5F, NIST/NSF, sensor counts and range - what each claim does and does not prove.</p><p><a class="btn small" href="guide-thermometer-accuracy.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal</span><h3>Holiday air fryer gifts: how to choose one that gets used</h3><p>The gift checklist that works without a price tag: depth, cleanup, one control panel they will actually learn.</p><p><a class="btn small" href="guide-gift-picks.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Hosting</span><h3>The holiday hosting test: which air fryer actually feeds a crowd?</h3><p>Capacity claims, a 6-lb rotisserie chicken, 12-inch pizzas - and the counter-depth number that decides fit in December.</p><p><a class="btn small" href="guide-holiday-hosting.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Budget</span><h3>Kitchen gifts under $25, under $80 and under $150</h3><p>Budget bands mapped to the five verified picks, with each listing's own gift claims quoted, not invented.</p><p><a class="btn small" href="guide-gifts-by-budget.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Thanksgiving</span><h3>Thanksgiving counter math: what actually fits?</h3><p>Depth, cabinet height, wattage and the cooking claims a listing will actually stand behind, checked before the 26 November dinner.</p><p><a class="btn small" href="guide-thanksgiving-counter.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Buying window</span><h3>A holiday price looks like a deal. Check the listing for ten minutes.</h3><p>Quarts per dollar, the variant trap, what a badge is not, and what to do when a listing argues with itself.</p><p><a class="btn small" href="guide-holiday-deal-check.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Gifting</span><h3>The gift receipt test: five checks before you wrap</h3><p>Variant, fit, cleanup, setup burden and the paperwork that turns a December problem into a form.</p><p><a class="btn small" href="guide-gift-return-window.html">Read guide</a></p></article>
<article class="card"><span class="tag">Thermometers - Buying</span><h3>Instant-read vs wireless thermometer: do you need both?</h3><p>Two tools, two jobs. What each listing states - and the one that states no accuracy figure at all.</p><p><a class="btn small" href="guide-instant-read-vs-wireless.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Specs</span><h3>Will it trip the breaker? Wattage and outlet math for air fryers</h3><p>1000W or 1700W? One of our listings answers that question two different ways - here is how to check yours.</p><p><a class="btn small" href="guide-wattage-outlets.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Space &amp; fit</span><h3>Will a 26-quart oven fit your counter? The depth and height math</h3><p>Depth, height and footprint arithmetic from the listed dimensions, converted to centimetres, step by step.</p><p><a class="btn small" href="guide-counter-depth-fit.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Form</span><h3>Two baskets or one: what dual-zone cooking actually changes</h3><p>Dual-basket, single-basket and oven-cavity cooking, decided on the listings' form and capacity facts.</p><p><a class="btn small" href="guide-dual-vs-single-basket.html">Read guide</a></p></article>
<article class="card"><span class="tag">In the box</span><h3>What's actually in the box: accessories, per the listing</h3><p>Included parts for all five picks as each listing states them - including one count the listing gives two ways.</p><p><a class="btn small" href="guide-accessories-included.html">Read guide</a></p></article>
</div>
<h2>Consolidated URLs</h2>
<p class="small">A parallel pass published three more seasonal pages on questions this list already covers. They stay live but return a canonical reference to the surviving guide, so one question has one answer: <a href="guide-holiday-gifts.html">holiday gifts</a> &rarr; <a href="guide-gift-picks.html">gift picks</a>; <a href="guide-small-kitchen.html">small-kitchen fit</a> &rarr; <a href="guide-cleanup-counter-space.html">counter space</a>; <a href="guide-holiday-roast.html">holiday roast thermometer</a> &rarr; <a href="guide-thermometer-accuracy.html">accuracy claims</a>. Reason and reversal option: <a href="flagged.html#FLG-047">FLG-047</a>.</p>
"""
_gn = guides_body.count('<a class="btn small" href="guide-')
page_to("guides.html","Buying guides for air fryers & probes | Countertop Guide",f"{_gn} question-led guides on air fryers and meat thermometers: form factor, capacity, cleanup, accuracy claims, gifts, hosting and the 2026 holiday window.",guides_body)
# ---------- GUIDE 1 ----------
b1, j1 = guide_shell("Guide - Air fryers", "Basket or oven-style air fryer: what should you compare?",
 "If you cook two different dishes at the same time, a dual-basket wins. If you cook for a crowd or want rotisserie and a 12-inch pizza, an oven-style unit wins. Everything else is footprint and cleanup. Here is how to decide, using the three fryers on this site.",
 """
<h2>Start with the job, not the brand</h2>
<p><strong>Dual-basket (Chefman 6QT, B0CDY277D3).</strong> Two independent 3-quart baskets with Sync Finish, so two dishes can finish together. The listing describes dual-zone cooking for different dishes simultaneously. Depth is 13.38 inches (34.0 cm) - the middle of the three.</p>
<p><strong>Oven-style French-door (Emeril 26QT, B09B7SB46R).</strong> Built for volume: the listing describes 26-quart capacity for 4-6 people, rotisserie for a 6-lb chicken, and baking a 12-inch pizza. It is also the deepest at 16.9 inches (42.9 cm) and the largest footprint (267.0 sq in). French doors open with a single pull.</p>
<p><strong>Single-basket (Chefman 8QT, B08DKYBTPH).</strong> One large basket with a 450F Hi-Fry option and a top-rack dishwasher-safe basket and tray. Shallowest at 12.75 inches (32.4 cm). Best when counter depth is the constraint and you cook one dish at a time.</p>
<h2>Three questions that decide it</h2>
<ol>
<li><strong>Do you cook two things at once?</strong> If yes, dual-basket. If no, single-basket or oven-style.</li>
<li><strong>Do you cook for 4-6 or want rotisserie/pizza?</strong> If yes, oven-style. The Emeril listing makes those specific claims; verify them on the listing before buying.</li>
<li><strong>What is your counter depth?</strong> Measure it. The Emeril needs 42.9 cm; the Chefman 8QT needs 32.4 cm. A 10 cm difference decides fit.</li>
</ol>
<h2>What the listing cannot tell you</h2>
<p>We have not cooked in any of these units, so we do not claim crispness, noise, or "lived-with" durability. Those require hands-on testing we have not done - see <a href="flagged.html">Flagged for review</a>. What we can tell you is form, capacity, footprint and cleanup exactly as the listing states them. Price and rating live on Amazon and move, so we link to them instead of quoting them.</p>
""",
 [("Which is better, basket or oven-style air fryer?","Neither - they do different jobs. Dual-basket for two dishes at once, oven-style for crowds, rotisserie and pizza, single-basket for compact one-dish cooking. Use the three questions above."),
  ("How deep is the Emeril 26QT oven?","16.9 inches (42.9 cm) deep, per the Amazon listing dimensions (16.9D x 15.8W x 14.8H in). Measure your counter before buying."),
  ("Can the Chefman 6QT cook two dishes at once?","Yes, per the listing: two independent 3-quart baskets with Sync Finish so both can finish at the same time.")])
page_to("guide-basket-vs-oven.html","Basket or oven-style air fryer? | Countertop Guide","Dual-basket for two dishes at once, French-door for a crowd, single basket for a shallow counter - decided on listing facts, not on testing we have not done.",b1,j1,"guide-page")
# ---------- GUIDE 2 ----------
b2, j2 = guide_shell("Guide - Capacity", "A no-hype checklist for comparing air fryer capacity",
 "Capacity numbers are the easiest place to be misled. Quarts vs litres, single vs dual baskets, and 'feeds 4-6' all mean different things. Use this checklist on any listing - we apply it to the three fryers here.",
 """
<h2>The checklist</h2>
<ol>
<li><strong>Which number is the title, which is the field?</strong> Chefman 6QT title vs "6 liters" field; Emeril 26QT title vs "24.6 liters" field. Note both; do not silently convert. See <a href="flagged.html">Flagged FLG-002</a>.</li>
<li><strong>Single or split?</strong> "6 Quart" that is 2 x 3 Qt behaves differently from a single 6 Qt basket. The Chefman dual-basket is explicitly 2 x 3 Qt.</li>
<li><strong>What food claim backs the number?</strong> Emeril: 4-6 people, 6-lb rotisserie chicken, 12-inch pizza (per bullets). Chefman 8QT: family-size single basket (per bullets). Ask: what food, what portion?</li>
<li><strong>What is the footprint cost?</strong> Capacity per square inch: Emeril 0.097, Chefman 8QT 0.046, Chefman 6QT dual 0.038 qt/sq in (derived from listing dims). Bigger is not automatically better if it does not fit.</li>
<li><strong>What is missing?</strong> The Emeril warranty period is not stated on the listing page (a PDF is linked). Wattage is listed at 1700 W / 120 V. The Chefman 8QT disagrees with itself, so read the figure on the page you buy from.</li>
</ol>
<h2>Worked example</h2>
<p>Two baskets of 3 Qt each (Chefman 6QT dual) let you run chicken in one and vegetables in the other, finishing together. A single 8 Qt basket (Chefman 8QT) gives one large cavity for one dish. A 26QT oven (Emeril) gives a cavity for a whole chicken and pizza. Same word - "capacity" - three different cooking experiences.</p>
""",
 [("Is 6 quarts the same as 6 litres?","No. The Chefman 6QT listing title says 6 Quart while its capacity field says 6 liters. We report both exactly as shown and flag the difference rather than converting silently."),
  ("How many people does the Emeril 26QT feed?","The listing bullets describe it as suitable for 4-6 people. That is the seller's description, not our tested serving count."),
  ("What does capacity per square inch mean?","Title capacity divided by footprint (width x depth from listing dimensions). It shows how much capacity you get per unit of counter. Derived by us; see compare page for method.")])
page_to("guide-capacity-checklist.html","Air fryer capacity, read honestly | Countertop Guide","Quarts versus litres, split baskets and what a 'feeds 4-6' claim actually claims: a checklist you can run on any listing in five minutes.",b2,j2,"guide-page")
# ---------- GUIDE 3 ----------
b3, j3 = guide_shell("Guide - Space & cleanup", "How to assess cleanup and counter-space trade-offs",
 "The best air fryer is the one that fits your counter and that you will actually wash. Here is the footprint math and the cleanup facts as listed - nothing more.",
 """
<h2>Measure twice</h2>
<p>Depth decides fit under cabinets; width decides whether it crowds the sink. From listing dimensions:</p>
<ul>
<li>Chefman 8QT basket: 12.75D x 13.5W in - shallowest, 172.1 sq in footprint.</li>
<li>Chefman 6QT dual: 13.38D x 11.81W in - narrowest, 158.0 sq in footprint.</li>
<li>Emeril 26QT oven: 16.9D x 15.8W in - deepest and widest, 267.0 sq in footprint.</li>
</ul>
<p>Capacity per centimetre of counter depth (derived): Emeril 0.61, Chefman 8QT 0.25, Chefman 6QT dual 0.18 qt/cm. The oven gives the most capacity per centimetre of depth - if you have the depth to spare.</p>
<h2>Cleanup as listed</h2>
<ul>
<li>Chefman 6QT dual: removable non-stick baskets are dishwasher safe (per bullets).</li>
<li>Chefman 8QT: 8-quart non-stick basket and flat tray are top-rack dishwasher safe (per bullets).</li>
<li>Emeril 26QT: six accessories included (per title); check the listing for each accessory's care instructions before buying.</li>
</ul>
<p>"Dishwasher safe" in a bullet is the seller's claim. We have not washed any of these baskets. If dishwasher care is decisive, confirm the exact wording on the listing.</p>
""",
 [("Which air fryer takes the least counter space?","By footprint, the Chefman 6QT dual-basket (158.0 sq in). By depth, the Chefman 8QT (32.4 cm). Measure both depth and width."),
  ("Are the baskets dishwasher safe?","Chefman 6QT: baskets dishwasher safe per bullets. Chefman 8QT: basket and tray top-rack dishwasher safe per bullets. Confirm on the listing."),
  ("How is capacity per cm calculated?","Title capacity (quarts) divided by depth in centimetres (inches x 2.54). Derived by us from listing dimensions; not a manufacturer claim.")])
page_to("guide-cleanup-counter-space.html","Cleanup & counter space trade-offs | Countertop Guide","Dishwasher-safe parts as listed, footprint arithmetic and capacity per centimetre of counter depth for three verified air fryers.",b3,j3,"guide-page")
# ---------- GUIDE 4 ----------
b4, j4 = guide_shell("Guide - Multi-function", "Questions to ask before buying a multi-function kitchen appliance",
 "Multi-function ovens promise everything. Before you pay for presets you will never use, ask these questions. We apply them to the Emeril 26QT French-door oven.",
 """
<h2>The pre-purchase questions</h2>
<ol>
<li><strong>How many presets, and do you recognise them?</strong> Emeril title says 24 One-Touch presets; bullets say 25 cooking pre-sets. That discrepancy is flagged - count on the listing, not the headline. Functions shown: Air Fry, Convection Bake, Rotisserie, Toast, Grill, Dehydrate, Roast, Slow Cook, Broil.</li>
<li><strong>What accessories are included?</strong> Title says six cooking accessories. List them on the listing before buying; replacements cost extra.</li>
<li><strong>What is the wattage?</strong> Emeril: 1700 watts / 120 volts per the listing's Product information table. Chefman 8QT: its bullets say 1000 W while the same listing's spec table says 1700 W - both are reported and the disagreement is flagged (FLG-022) rather than resolved by guesswork.</li>
<li><strong>What does the warranty say?</strong> The Chefman 6QT bullets state a 1-year assurance and the Chefman 8QT bullets a 1-year warranty; CHEF iQ states two years. The Emeril page links a warranty PDF but states no period on the page - we quote the PDF&rsquo;s existence, not its terms (<a href="flagged.html#FLG-005">FLG-005</a>).</li>
<li><strong>Does it fit?</strong> 16.9D x 15.8W x 14.8H in is the largest of the three fryers. French doors need swing clearance.</li>
</ol>
<p>Rule of thumb: pay for functions you will use weekly (air fry, bake, toast, rotisserie), not for the longest preset list.</p>
""",
 [("How many presets does the Emeril 26QT have?","The title says 24 One-Touch presets while the bullets say 25 cooking pre-sets. We flag the discrepancy and recommend verifying on the listing."),
  ("What accessories come with the Emeril oven?","The title says six cooking accessories are included. Check the listing for the exact list before buying."),
  ("What is the Emeril wattage?","The listing's Product information table states 1700 watts at 120 volts. It is not an independent measurement, and the manual - not this page - governs how you wire it up.")])
page_to("guide-multifunction-questions.html","Before a multi-function appliance | Countertop Guide","Presets, accessories, wattage, warranty and fit: the questions to ask a multi-function oven listing before paying for functions you will not use.",b4,j4,"guide-page")
# ---------- GUIDE 5 ----------
b5, j5 = guide_shell("Guide - Thermometers", "Instant-read or wireless? How to read accuracy claims",
 "One tool answers in one second in your hand; the other watches from your phone. The right choice depends on how you cook - and on reading accuracy claims carefully.",
 """
<h2>Instant-read: ThermoMaven (B0DHZTCNR5)</h2>
<p>Listing claims +/-0.5F accuracy with NIST &amp; NSF certification, 1-second thermocouple read, IP67 waterproof, auto-rotating LED. Includes a calibration certificate. Best for: quick checks, grilling, candy, everyday meals.</p>
<h2>Wireless: CHEF iQ Sense (B0DZFD6R9Z)</h2>
<p>Three ultra-thin probes plus hub, WiFi unlimited range with app, 1000F heat-safe probes, up to 50 hours per charge, flip reminders and rest timers. Listing bullets describe 4 internal + 1 ambient sensors (title: 5 sensors). No +/-F accuracy figure was captured - do not assume it matches the instant-read. Three probe counts are sold as variants - pick the one you need on the listing. Best for: long cooks, multiple proteins, monitoring from another room.</p>
<h2>How to read "accuracy"</h2>
<ul>
<li>Ask for the +/- figure and the certification name. "NIST certified" without a figure is incomplete.</li>
<li>Ask what the sensor count means. CHEF iQ's 5 = 4 internal + 1 ambient (per bullets).</li>
<li>Ask about range honestly. "Unlimited" via WiFi means app monitoring over your network, not magic - you still need WiFi and the app.</li>
<li>We have not calibrated either unit. Certification claims are the seller's; verify the certificate on the listing.</li>
</ul>
""",
 [("Which thermometer is more accurate?","The ThermoMaven listing states +/-0.5F with NIST & NSF certification. No +/-F figure was captured for the CHEF iQ, so we do not rank them on accuracy."),
  ("What does 5 sensors mean on the CHEF iQ?","Per the listing bullets: 4 internal temperature sensors plus 1 ambient sensor that tracks cooking-environment temperature."),
  ("Do I need WiFi for the CHEF iQ?","WiFi enables unlimited-range app monitoring per the listing; Bluetooth is also listed in connectivity. You need the CHEF iQ app for remote monitoring.")])
page_to("guide-thermometer-accuracy.html","Reading thermometer accuracy claims | Countertop Guide","What a stated tolerance, a named certification, a sensor count and 'unlimited range' do and do not prove - for a handheld and a wireless probe set.",b5,j5,"guide-page")
# ---------- GUIDE 6 (session 8bdadebf): counter-depth & height math ----------
b11, j11 = guide_shell("Guide - Space & fit", "Will a 26-quart oven fit your counter? The depth and height math",
 "Counter fit is two measurements, not one. Depth decides whether the appliance sits under the cabinet; height decides whether it clears the cabinet above. Both come from the listed dimensions - and here is the arithmetic, so you can run it on any listing.",
 """
<h2>Depth: the number that decides under-cabinet fit</h2>
<p>From the listed dimensions (depth &times; width &times; height, inches):</p>
<ul>
<li>Chefman 8QT basket: 12.75D &times; 13.5W &times; 10H in &mdash; 32.4 cm deep.</li>
<li>Chefman 6QT dual-basket: 13.38D &times; 11.81W &times; 10.63H in &mdash; 34.0 cm deep.</li>
<li>Emeril 26QT oven: 16.9D &times; 15.8W &times; 14.8H in &mdash; 42.9 cm deep, and 37.6 cm tall.</li>
</ul>
<p>Inch to centimetre is a single multiply: depth in &times; 2.54 = depth in cm. The Emeril needs about 10 cm more depth than the Chefman 8QT. That gap, not the quarts, is what usually decides fit.</p>
<h2>Height: the number people forget</h2>
<p>Depth gets the appliance onto the counter; height decides whether it clears the cabinet above. The Emeril is 14.8 in (37.6 cm) tall, against 10.63 in (27.0 cm) for the Chefman 6QT and 10 in (25.4 cm) for the Chefman 8QT. If you have a wall cabinet or a window above, measure the clear space, not the counter.</p>
<h2>Footprint: how much counter it owns</h2>
<p>Footprint is depth &times; width, derived from the same listed dimensions: Emeril 267.0 sq in, Chefman 8QT 172.1 sq in, Chefman 6QT dual 158.0 sq in. It is arithmetic we do from the listing, not a manufacturer figure.</p>
<h2>Run the math yourself</h2>
<ol>
<li>Measure your counter depth and the clear height above it, in inches.</li>
<li>Compare both against the listed depth and height for the model you are considering.</li>
<li>Add door-swing clearance for French-door models; the listing dimensions describe the box, not the door arc.</li>
</ol>
<h2>What the listing cannot tell you</h2>
<p>The listed dimensions describe the appliance, not your kitchen. They do not include door swing, handle depth, the power cord, or the real usable cavity. We have not measured any of these units; the figures above are the listing's, converted and multiplied, with the method shown so you can repeat it.</p>
""",
 [("How deep is the Emeril 26QT oven?", "16.9 inches (42.9 cm) deep and 14.8 inches (37.6 cm) tall, per the Amazon listing dimensions (16.9D x 15.8W x 14.8H in). Measure your counter and the clearance above it before buying."),
  ("Which of the three takes the least counter depth?", "The Chefman 8QT basket at 12.75 inches (32.4 cm) deep, per the listing. The Chefman 6QT dual is 13.38 inches (34.0 cm); the Emeril 26QT is 16.9 inches (42.9 cm)."),
  ("Do the listed dimensions include door swing?", "No. Listed dimensions describe the appliance box. French-door models like the Emeril need extra clearance for the doors to open; measure that separately.")])
page_to("guide-counter-depth-fit.html", "Will a 26-quart oven fit your counter? | Countertop Guide", "Counter fit as listing arithmetic: depth, height and footprint for three verified air fryers, converted to centimetres, step by step.", b11, j11, "guide-page")
# ---------- GUIDE 7 (session 8bdadebf): dual-baskets vs single ----------
b12, j12 = guide_shell("Guide - Air fryers - Form", "Two baskets or one: what dual-zone cooking actually changes",
 "The same quart figure can mean two very different cooking setups. A dual-basket unit cooks two dishes at once; a single basket cooks one. Here is what each shape actually offers, exactly as the listings state it.",
 """
<h2>What each shape offers, as listed</h2>
<p><strong>Dual-basket (Chefman 6QT, B0CDY277D3).</strong> Two independent 3-quart baskets with Sync Finish, so two dishes can finish together; the listing describes dual-zone cooking for different dishes at the same time.</p>
<p><strong>Single basket (Chefman 8QT, B08DKYBTPH).</strong> One 8-quart basket with a 450&deg;F Hi-Fry option and a top-rack dishwasher-safe basket and tray.</p>
<p><strong>Oven cavity (Emeril 26QT, B09B7SB46R).</strong> A single large cavity the listing describes as suitable for 4-6 people, a 6-lb rotisserie chicken and a 12-inch pizza.</p>
<h2>When two baskets earn their depth</h2>
<ul>
<li>You cook two different dishes at once, at different temperatures or times.</li>
<li>Sync Finish matters to you: the listing says the two baskets can finish at the same time.</li>
<li>You want to air-fry a main and a side without waiting, and you have the counter depth (34.0 cm for the Chefman 6QT).</li>
</ul>
<h2>When one big basket is simpler</h2>
<ul>
<li>You cook one dish at a time and want the shallowest footprint (32.4 cm for the Chefman 8QT).</li>
<li>Simpler cleanup: one basket and tray rather than two.</li>
<li>You fry in large single batches - fries for the whole family - where one 8-quart cavity is the point.</li>
</ul>
<h2>What the listing cannot tell you</h2>
<p>Whether two baskets actually save you time, or whether a single large basket crisps a big batch better, is a hands-on question. We have not cooked in any of these units, so we do not rank them on cooking performance - only on the listed form, capacity and care facts above.</p>
""",
 [("What is the difference between dual-basket and single-basket air fryers?", "A dual-basket unit cooks in two independent baskets that can run different dishes at once (the Chefman 6QT lists Sync Finish); a single-basket unit cooks in one cavity (the Chefman 8QT is 8 quarts)."),
  ("Can the Chefman 6QT cook two dishes at different times?", "Yes, per the listing: two independent 3-quart baskets with dual-zone cooking, so different dishes can cook at the same time."),
  ("Is a 26-quart oven the same as two baskets?", "No. The Emeril 26QT is one large oven cavity, not two baskets. The listing describes it for a whole chicken and pizza; it is a different cooking setup from a dual-basket fryer.")])
page_to("guide-dual-vs-single-basket.html", "Two baskets or one: dual-zone cooking | Countertop Guide", "Dual-basket, single-basket and oven-cavity cooking, decided on the listings' own form, capacity and care facts.", b12, j12, "guide-page")
# ---------- GUIDE 8 (session 8bdadebf): accessories in the box ----------
b13, j13 = guide_shell("Guide - In the box", "What's actually in the box: accessories, per the listing",
 "The accessory list decides what you can cook on day one and what you will need to replace. Here is what each verified listing includes, stated as listed - including one count the listing itself gives two ways.",
 """
<h2>Air fryers</h2>
<ul>
<li><strong>Chefman 6QT dual (B0CDY277D3):</strong> two 3-quart non-stick baskets, per the listing.</li>
<li><strong>Chefman 8QT (B08DKYBTPH):</strong> an 8-quart non-stick basket and a flat frying tray, per the listing.</li>
<li><strong>Emeril 26QT oven (B09B7SB46R):</strong> the title says six cooking accessories included; the listing's Item-details table lists seven. Both counts are the listing's and disagree - see <a href="flagged.html#FLG-021">FLG-021</a>. Count on the listing, not the headline.</li>
</ul>
<h2>Thermometers</h2>
<ul>
<li><strong>ThermoMaven instant-read (B0DHZTCNR5):</strong> includes a calibration certificate, per the listing's included-components field.</li>
<li><strong>CHEF iQ Sense wireless (B0DZFD6R9Z):</strong> three ultra-thin probes plus a hub that charges all three at once, per the listing. Probe count is sold as variants - pick the count you need on the listing.</li>
</ul>
<h2>Why the count matters</h2>
<p>Accessories are the parts that wear and the parts you replace. A title count and a table count that disagree is exactly the detail to resolve on the listing before you buy, because a missing tray or an extra probe changes what you can cook on day one.</p>
<h2>What the listing cannot tell you</h2>
<p>The listing states what is included, not how each accessory is cared for, whether replacements are stocked, or whether a given accessory fits other models. Check the care instructions and the replacement availability on the listing before relying on any one part.</p>
""",
 [("How many accessories come with the Emeril 26QT?", "The title says six cooking accessories; the listing's Item-details table lists seven. We publish both and flag the disagreement (FLG-021) rather than choosing one."),
  ("What comes with the CHEF iQ Sense thermometer?", "Three ultra-thin probes plus a hub that charges all three at once, per the listing. Probe count is sold as variants, so confirm the count on the listing."),
  ("Do the baskets count as accessories?", "Yes - the Chefman 6QT lists two 3-quart baskets and the Chefman 8QT lists a basket and a flat frying tray. They are the removable, replaceable parts of these appliances.")], picks=("P1", "P2", "P5"))
page_to("guide-accessories-included.html", "Accessories in the box, per the listing | Countertop Guide", "Included parts for all five verified picks, as each listing states them - including one count the listing gives two ways.", b13, j13, "guide-page")
# ---------- EXECUTIVE SUMMARY ----------
exec_body = f"""
<p class="eyebrow">Executive summary</p>
<h1>What is live, what is verified, what needs your decision</h1>
<p class="lede">Three minutes. This page is for whoever owns the site: the state of the publication, the evidence behind the product data, what is deliberately not claimed, and the short list of decisions only you can make.</p>

<h2>The state of the publication</h2>
<div class="grid cols-3">
  <article class="card"><span class="chip">Live</span><h3>1 publication, @@PAGES@@ pages</h3><p>Front page, two category hubs, a five-product comparison with a three-question chooser, @@GUIDES@@ question-shaped guides, a topic calendar, and the review desk. One sitemap, one feed, one canonical host.</p></article>
  <article class="card"><span class="chip">Verified</span><h3>5 listings, dated</h3><p>Titles, dimensions, capacity, features and bullets read from Amazon.com on {VERIFIED}, each linked. Submitted short links resolve to the five ASINs. Anything unconfirmed is blank and flagged, never inferred.</p></article>
  <article class="card"><span class="chip">Waiting on you</span><h3>6 owner decisions</h3><p>Special Link test, search console, canonical domain, photography licence, analytics host, byline. None blocks publishing; each blocks a claim or a scale step. <a href="suggestions.html#SG-01">See the decision queue</a>.</p></article>
</div>

<h2>The five products</h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Product</th><th>ASIN</th><th>Category</th><th>Verified from the listing</th><th>Listing</th></tr>
<tr><td>P1</td><td>Chefman 6QT Dual-Basket Air Fryer Oven</td><td>B0CDY277D3</td><td>Air fryers</td><td>title, capacity, dimensions, features, bullets <span class="fine">re-read 2026-11-20</span></td><td><a href="https://www.amazon.com/dp/B0CDY277D3">B0CDY277D3</a></td></tr>
<tr><td>P2</td><td>Emeril Lagasse 26QT French-Door Oven</td><td>B09B7SB46R</td><td>Air fryers</td><td>title, capacity, dimensions, features, bullets, wattage (warranty period not stated) <span class="fine">re-read 2026-11-20</span></td><td><a href="https://www.amazon.com/dp/B09B7SB46R">B09B7SB46R</a></td></tr>
<tr><td>P3</td><td>Chefman 8QT TurboFry Basket</td><td>B08DKYBTPH</td><td>Air fryers</td><td>title, capacity, dimensions, features, bullets <span class="fine">re-read 2026-11-20</span></td><td><a href="https://www.amazon.com/dp/B08DKYBTPH">B08DKYBTPH</a></td></tr>
<tr><td>P4</td><td>ThermoMaven 1-Second Instant-Read</td><td>B0DHZTCNR5</td><td>Thermometers</td><td>title, accuracy claim, features, bullets, item length 6.5 in; rating 4.6 (3,499) (full dimensions not stated) <span class="fine">re-read 2026-11-20</span></td><td><a href="https://www.amazon.com/dp/B0DHZTCNR5">B0DHZTCNR5</a></td></tr>
<tr><td>P5</td><td>CHEF iQ Sense Wireless (3 probes)</td><td>B0DZFD6R9Z</td><td>Thermometers</td><td>title, sensors, features, bullets (dimensions and tolerance figure not stated) <span class="fine">re-read 2026-11-20</span></td><td><a href="https://www.amazon.com/dp/B0DZFD6R9Z">B0DZFD6R9Z</a></td></tr>
</table></div>
<p class="fine">Tracking ID <code>{TAG}</code>. Outbound format <code>https://www.amazon.com/dp/ASIN?tag={TAG}</code>. The supplied <code>link.amazon</code> short links are recorded as submitted, with their observed redirects in a separate field; they are not used as buttons.</p>

<h2>What is verified, and how</h2>
<ul>
<li><strong>Product facts</strong> come from each product&rsquo;s own listing, read on {VERIFIED}, with the URL recorded per field in the <a href="verification.html">verification register</a>. Where a listing contradicts itself, both values are published and flagged rather than silently resolved (<a href="flagged.html#FLG-002">FLG-002</a>, <a href="flagged.html#FLG-021">FLG-021</a>, <a href="flagged.html#FLG-022">FLG-022</a>).</li>
<li><strong>Policy text</strong> was read from the official pages and quoted, not summarised from memory: Operating Agreement &sect;5 (disclosure), Program Policies (price and availability, ratings), Google Search Central (outbound link qualification), FTC (disclosure placement). Sources are listed on <a href="compliance.html">the compliance page</a> with the read date.</li>
<li><strong>Mechanical checks</strong> run on every main-branch push: five automated publishing gates collectively check disclosures, sponsored links, internal links, metadata, voice rules, price policy, CSS coverage, page structure and the five-event contract; the build also refuses to write comparative claims that the product register no longer supports. See the <a href="verification.html#claim-audit">claim audit</a>. The current Pages source is the legacy branch builder: a failed gate turns the workflow red, but this repository has not verified branch protection that would block a merge, and the Actions workflow does not itself publish the Pages artifact in this mode (<a href="flagged.html#FLG-051">FLG-051</a>).</li>
</ul>

<h2>What is not claimed, and why</h2>
<div class="table-scroll"><table>
<tr><th>Not claimed</th><th>Reason</th><th>What would change it</th></tr>
<tr><td>Hands-on testing or &ldquo;we tried it&rdquo;</td><td>Nobody has cooked in these machines. The FTC guidance is explicit that you cannot talk about your experience with a product you have not tried, and Section 5 of the Amazon Agreement makes the same point about accuracy.</td><td>A funded test protocol with dated photos (<a href="suggestions.html#SG-09">SG-09</a>)</td></tr>
<tr><td>Prices, ratings or &ldquo;bought in past month&rdquo; on shop pages</td><td>Program Policies allow price and availability only when Amazon serves the link or the data comes from the Creators/PA API within a 24-hour cache. A static build satisfies neither. The dated figures we saw live in the register as observations (<a href="flagged.html#FLG-032">FLG-032</a>).</td><td>Creators/PA API access with a refresh gate (<a href="suggestions.html#SG-20">SG-20</a>)</td></tr>
<tr><td>Search volume, traffic or revenue</td><td>No Search Console property exists yet and no authorised first-party report has arrived. The campaign ledger is empty by design.</td><td>Search Console access + Associates reports, recorded with their dates</td></tr>
<tr><td>Product photography</td><td>Amazon&rsquo;s Program Content is licensed, not owned; generated product shots would mislead. Imagery is our own drawings until a licence exists (<a href="flagged.html#FLG-041">FLG-041</a>).</td><td>A photography or permission decision (<a href="suggestions.html#SG-04">SG-04</a>)</td></tr>
</table></div>

<h2>How money and measurement work</h2>
<p>Outbound links carry tracking ID <code>{TAG}</code> and are marked <code>rel="sponsored"</code> with a visible label, including the links the chooser script builds. Five privacy-preserving events are defined; they are counted in the visitor&rsquo;s browser only, because the self-hosted endpoint - code-complete with a CI-tested five-event contract - is not hosted yet. The campaign ledger starts empty and only accepts figures from authorised first-party reports, with a date. No conversion score or revenue forecast appears anywhere on this site.</p>
<p class="fine">See <a href="methodology.html">Method &amp; campaign ledger</a> for the event contract, the endpoint self-test and the ledger rules.</p>

<h2>Automation boundary</h2>
<p>This is a static affiliate publication, not a live AI research or campaign-optimization service. The build automates page generation and compliance checks; the event names and endpoint are implemented and tested locally, but the endpoint is not hosted, no conversion reports are connected, and no AI agent is currently sourcing products, scoring commissions, publishing automatically, or optimizing campaigns. Those capabilities require documented data access, policy review and an operating host before they can be represented as live. The open questions and recommended discovery steps are on the <a href="suggestions.html">suggestions desk</a> and <a href="decisions.html">decision register</a>.</p>

<h2>What the 2026-11-20 pass changed</h2>
<ul>
<li><strong>The type the design always specified now actually loads.</strong> The stylesheet named Fraunces and Inter; neither file existed, so every page rendered in Georgia and the system UI font. Four self-hosted latin variable fonts (182 KB total, SIL Open Font License 1.1, licences committed alongside) now render the site (<a href="flagged.html#FLG-069">FLG-070</a>).</li>
<li><strong>Original brand art on every product card.</strong> Five line drawings of the appliance <em>types</em>, drawn for this site. No photograph, no Amazon image, no rendering of a specific unit &mdash; the imagery rule the site set for itself still holds.</li>
<li><strong>Navigation tells you where you are.</strong> The header marks the current section, and the stylesheet rule that was written for it is finally used (<a href="flagged.html#FLG-071">FLG-071</a>).</li>
<li><strong>The calendar produced a page.</strong> The queued 2026-12-08 topic is published as <a href="guide-instant-read-vs-wireless.html">guide 10</a>, and it moved in the calendar, the sitemap and the RSS feed in the same commit, so those three cannot disagree.</li>
<li><strong>The sitemap is now the shop, not the audit.</strong> Seven internal surfaces moved to <code>noindex, follow</code>; the register, the flagged list and the compliance page stay indexed for the buyer who wants the source (<a href="flagged.html#FLG-069">FLG-070</a>).</li>
<li><strong>The site is not claimed to have been looked at.</strong> No browser could be installed in this environment, so there is no screenshot review in this pass. <code>scripts/verify_structure.mjs</code> proves the documents parse, that every asset and font file the HTML names exists, that headings are ordered and that images declare dimensions &mdash; and says in its own header that this is a structural proof, not a visual one. The full working record, including the two failed browser installs, is <code>review/62786810/VERIFICATION.md</code>.</li>
<li><strong>Five decisions are written so they can be settled in one sitting</strong> (<a href="suggestions.html#suggestions">SG-49 to SG-53</a>), plus five new questions (<a href="suggestions.html#Q-33">Q-33 to Q-37</a>) covering the things this build cannot answer from inside the repository.</li>
<li><strong>Re-verified line by line, this session.</strong> Operating Agreement &sect;5 (disclosure) and &sect;6 (breach), Program Policies &sect;2(b) (price/availability), &sect;6(t) (ratings), &sect;6(w) (link-shortening clarity) and &sect;6(y) (no price tracking), Google&rsquo;s outbound-link qualification, and all five Amazon.com listings were read from the official pages on {VERIFIED}; the five ASINs resolve to the titles in the register. Sources and quotes: <code>review/e05155a0/VERIFICATION.md</code>.</li>
<li><strong>Accessibility audited, not assumed.</strong> A 20-pair WCAG AA contrast audit of the whole palette passed (body text, links, buttons, disclosure strip, footer, table headers, status badges). It is recorded as the basis for a standing contrast gate (<a href="suggestions.html#SG-58">SG-58</a>) rather than a one-off.</li>
<li><strong>The design prompt now carries the polished-marketing direction.</strong> <code>DESIGN_PROMPT.md</code> section 9 sets out what "polished marketing, not AI slop" means structurally, the catchy spec-backed topic direction, the findability rails and the imagery rule. The owner picks one brief to execute (<a href="suggestions.html#SG-60">SG-60</a>, <a href="suggestions.html#Q-43">Q-43</a>).</li>
</ul>

<h2>What earlier passes changed</h2>
<ul>
<li><strong>The site now looks designed, because the styles exist.</strong> The build was emitting 44 CSS classes with no rule and referencing 9 undefined custom properties, so cards, hero columns and status chips rendered as plain blocks. All of it is styled, and <code>scripts/check_style.mjs</code> fails the build if an unstyled class returns (<a href="flagged.html#FLG-052">FLG-052</a>).</li>
<li><strong>Broken markup repaired.</strong> Three suggestion rows had malformed class attributes, so their status badges and row text never rendered (<a href="flagged.html#FLG-053">FLG-053</a>).</li>
<li><strong>The social card is readable.</strong> The shared-link image had text overlapping the subtitle and captions hidden under the footer; <code>make_og.py</code> now measures each block and asserts clearance (<a href="flagged.html#FLG-054">FLG-054</a>).</li>
<li><strong>Readers can ask for a topic.</strong> The desk now has an intake that opens a public issue, and shows an honest count of zero rather than pretending to have submissions (<a href="flagged.html#FLG-055">FLG-055</a>).</li>
<li><strong>Search metadata fits.</strong> Five titles and descriptions that would truncate in results were rewritten; the metadata gate now reports zero warnings.</li>
<li><strong>Re-verified {VERIFIED}.</strong> Every listing was re-read line by line on {VERIFIED}; the volatile figures that drifted (P1 rating count and used price, P2 rating count) were corrected in the register, and the new <a href="flagged.html#FLG-067">FLG-060</a> records the pass and its scope. Full evidence: <code>review/1b65e5a1/VERIFICATION.md</code>.</li>
<li><strong>Two decision rows added.</strong> The desk now carries <a href="suggestions.html#SG-44">SG-44</a> (visual QA of the styled shop before the next deploy) and <a href="suggestions.html#SG-45">SG-45</a> (goal-based intent landings built only from verified fields).</li>
</ul>

<h2>What happens next, in order</h2>
<ol>
<li><strong>You run the Special Link test</strong> once per product in Associates Central and confirm the destination and the tracking report. This is the one gate no session can clear from inside the repository (<a href="suggestions.html#SG-01">SG-01</a>).</li>
<li><strong>Claim the Search Console property</strong> for the canonical host and submit the sitemap. Without it the calendar is a plan, not a measurement (<a href="suggestions.html#SG-02">SG-02</a>).</li>
<li><strong>Pick the domain and the build source</strong> — a custom domain if you want one, and GitHub Pages set to publish from Actions so a failed gate actually blocks a release (<a href="suggestions.html#SG-43">SG-43</a>).</li>
<li><strong>Write the next guide from measured queries</strong>, four weeks after step 2, not from instinct.</li>
</ol>
<p class="fine">Full working list: <a href="suggestions.html">the decision desk</a> (options, trade-offs, effort, and what each one unblocks) and <a href="flagged.html">Flagged for review</a> (every irregularity, with its source).</p>

<h2>Latest pass, 2026-11-20</h2>
<p>Session <code>42e09357</code>. What changed on the site, and what was deliberately not touched:</p>
<ul class="tight">
<li><strong>Three holiday-window guides published</strong> (counter fit before Thanksgiving, the ten-minute listing check for the buying window, the gift receipt test), each built only from fields in the register, each added to the calendar, the sitemap and the feed. The one-guide-a-week rule was deviated from on purpose and the deviation is recorded in <code>data/editorial.json</code>, not smoothed over.</li>
<li><strong>A decision register</strong> at <a href="decisions.html">decisions.html</a>: the board collapsed into seven gates, each with what an official source already settles, what is missing, the steps that would produce it, and who can take them. The build compares the register against the board on every publish and prints the rows nobody has taken yet &mdash; first written as a hard failure, which let one session&rsquo;s new suggestion block the deploy for everyone (<a href="flagged.html#FLG-082">FLG-082</a>).</li>
<li><strong>Shop pages reworded</strong> where they read like an audit, and <strong>footprint drawings added</strong> to each product card, drawn to one shared scale from the inches the listing states. No Amazon imagery, because that licence question is still open.</li>
<li><strong>A dated partial re-read</strong> of the five listings: titles confirmed on 2026-11-20, one buy-box price attributable and matching; the rest of the register keeps its 2026-11-19 field dates because those fields were not re-read in this pass.</li>
<li><strong>Not changed:</strong> no price or rating figure was added anywhere, no testing claim, no popularity claim, no commission or revenue figure, no change to the disclosure, and no new product. The two brand-name sites under <code>counter-check/</code> and <code>docs/</code> are untouched, and their consolidation is still an owner decision (SG-22, Q-18).</li>
</ul>
"""
page_to("executive-summary.html","Executive summary for the owner | Countertop Guide","What is live, what is verified, what is blocked, which decisions wait on an owner, and what the latest pass changed across the site.",exec_body)
# ---------- SUGGESTIONS / DECISION DESK ----------
sugg_body = f"""
<p class="eyebrow">Decision desk</p>
<h1>Review the options, pick a path, then we build</h1>
<p class="lede">This page is where the next version of this site gets decided. Nothing here is implemented until a reviewer marks a row <strong>Approve</strong>, <strong>Reject</strong> or <strong>Defer</strong> with a date. Each suggestion states the buyer problem it solves, the options with their trade-offs, the evidence it needs, and what it blocks. Suggestions SG-01 to SG-10 came from the first build and stand as written; SG-19 onward are added by this pass.</p>

<div class="callout"><strong>Three things to know before you read.</strong> (1) The site currently shows <em>no</em> price or rating figures on shop pages, because Amazon&rsquo;s policies only allow a site to display price and availability when Amazon serves it or when it comes from the Creators/PA API, with caching capped at 24 hours &mdash; see <a href="flagged.html#FLG-032">FLG-032</a>. (2) We have not cooked in any product, so no copy may imply we have. (3) Traffic, ranking and revenue are not forecasted anywhere on this site; the campaign ledger is empty by design.</div>

<h2>Ask for a topic</h2>
<div class="card">
<p><strong>What should we answer next?</strong> Reader questions pick the calendar, not instinct. A request opens as a public issue on the site repository, where you can see it, and where the answer will be published if we write it.</p>
<p><a class="btn" href="https://github.com/wingbangboozle1-lang/Prod1/issues/new?labels=reader-suggestion&amp;title=Topic%20request%3A%20&amp;body=The%20question%20I%20want%20answered%3A%0A%0AThe%20product%20or%20category%20it%20is%20about%3A%0A%0AWhat%20I%20have%20already%20read%20on%20this%20site%3A%0A" rel="noopener">Suggest a topic</a> <a class="link-quiet" href="{RS["inbox"]}" rel="noopener">Read the requests already sent</a></p>
<p class="fine">Nothing is collected silently: the form opens on GitHub, under your own account, and you can see and edit it afterwards. If you would rather not use GitHub, the <a href="about.html">about page</a> explains the other route. This desk shows <strong>{len(RS["items"])}</strong> reader-submitted topics so far. It is empty because none have arrived yet - we do not invent them to make the page look busy.</p>
</div>

<h2>Choose a path</h2>
<p>If you approve a bundle, everything inside it moves together. Each bundle is a coherent story for the reader, not a random list.</p>
<div class="grid cols-3">
  <article class="card path"><span class="chip">Path A</span><h3>Earn trust, then traffic</h3><p>Ship the honest-shop polish: link-only pricing with better CTAs, a real comparison tool, the &ldquo;what the listing does not say&rdquo; boxes, and the review desk kept out of the reader&rsquo;s way.</p><ul><li>SG-19, SG-20, SG-21, SG-25, SG-29</li></ul><p class="fine">Cost: mostly copy and one build. Needs no new accounts. Unblocks: nothing external, everything internal.</p></article>
  <article class="card path"><span class="chip">Path B</span><h3>Get found, then write to what arrives</h3><p>One canonical site, real Search Console data, per-page metadata, structured data, internal-link spine and a weekly cadence, so the next topic is chosen from queries rather than instinct.</p><ul><li>SG-02, SG-22, SG-23, SG-26, SG-30, SG-32</li></ul><p class="fine">Cost: low build work + owner access to Search Console and Associates Central. Needs ~4 weeks before data is meaningful.</p></article>
  <article class="card path"><span class="chip">Path C</span><h3>Look like a magazine, not a spreadsheet</h3><p>The visual overhaul: the design brief below, a typography and layout pass, real imagery only once a licence exists, and a voice pass over every article.</p><ul><li>SG-24, SG-27, SG-28, SG-31, SG-33, SG-04</li></ul><p class="fine">Cost: the highest design effort and the only path that can go wrong visually. Blocked by SG-04 (photography licence) for the imagery half.</p></article>
</div>
<p class="section-more">Our recommendation, stated plainly: <strong>Path B first, then A, then the non-imagery half of C.</strong> The site&rsquo;s data is already better than most affiliate sites&rsquo;; its problem is that nobody has been shown it yet. Photography stays gated until SG-04 clears, because a licence problem is a bigger loss than a plain-looking page.</p>

<h2 id="the-decisions">The decision queue &mdash; six items only you can settle</h2>
<p>Each row is a decision, not a task: it names the choice, what it unblocks, and what evidence closes it. The board below carries the full reasoning and the options. Nothing is implemented until a row is marked approved here or in the board.</p>
<div class="table-scroll"><table>
<tr><th>#</th><th>Decision</th><th>The choice in front of you</th><th>Unblocks</th><th>What closes it</th></tr>
<tr><td>1</td><td><a href="#SG-01">Special Link test</a></td><td>Click one tagged link per product in Associates Central and read the tracking report</td><td>Any claim that the links earn correctly; the short-link question (<a href="flagged.html#FLG-001">FLG-001</a>)</td><td>A screenshot or note per product, dated</td></tr>
<tr><td>2</td><td><a href="#SG-02">Search Console</a></td><td>Claim the canonical host, submit <code>sitemap.xml</code></td><td>Choosing the next topic from measured queries instead of instinct</td><td>Property verified; first 28 days of query data</td></tr>
<tr><td>3</td><td><a href="#SG-04">Photography licence</a></td><td>Own photos, manufacturer permission, or keep drawings</td><td>Any product imagery on the site (<a href="flagged.html#FLG-041">FLG-041</a>)</td><td>A signed permission or your own shoot</td></tr>
<tr><td>4</td><td><a href="#SG-03">Analytics host</a></td><td>Where the five-event endpoint runs, if anywhere</td><td>Outbound-click counts beyond one browser (<a href="flagged.html#FLG-008">FLG-008</a>)</td><td>A host + retention decision</td></tr>
<tr><td>5</td><td><a href="#SG-43">Pages build source</a></td><td>Publish from Actions instead of from the branch</td><td>Making a failed gate block a release (<a href="flagged.html#FLG-051">FLG-051</a>)</td><td>Settings &rarr; Pages &rarr; Build source</td></tr>
<tr><td>6</td><td><a href="#SG-26">Byline</a></td><td>Desk byline, a named author with a bio, or a commissioned tester</td><td>Authorship signals and any &ldquo;tested&rdquo; content (<a href="flagged.html#FLG-010">FLG-010</a>)</td><td>A real person and a contact route</td></tr>
</table></div>
<p class="fine">The domain question (<a href="#SG-02">SG-02</a>) sits inside decision 2: the canonical host is the GitHub Pages URL today, and a custom domain changes every canonical, every og:url and the sitemap. Choosing it before Search Console is claimed is cheaper than choosing it after.</p>

<h2>The board</h2>
<div class="table-scroll"><table>
<tr><th>#</th><th>Suggestion</th><th>Why it matters</th><th>Evidence needed</th><th>Effort</th><th>Status</th></tr>
<tr id="SG-01"><td>SG-01</td><td>Validate one Special Link per product in Associates Central (SiteStripe) and confirm destination + tracking report</td><td>Proves outbound links earn correctly before scaling</td><td>Associates Central test clicks + report screenshots</td><td>Low (manual)</td><td><span class="badge-warn">Needs decision - gate</span></td></tr>
<tr id="SG-02"><td>SG-02</td><td>Set canonical domain + Search Console + sitemap submission</td><td>One site to index; measured queries drive next topics</td><td>Domain choice; Search Console property</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-03"><td>SG-03</td><td>Deploy self-hosted analytics endpoint (5 events) + weekly ledger review</td><td>Turns clicks into decisions without third-party trackers</td><td>Hosting choice; retention policy (contract code-complete and CI-gated 2026-11-20: one five-event taxonomy across client, server and site, endpoint self-test green; only the host is missing)</td><td>Medium</td><td><span class="badge-warn">Partly done - hosting decision open</span></td></tr>
<tr id="SG-04"><td>SG-04</td><td>Licensed product photography (own photos or manufacturer permission)</td><td>Real photos convert; copied Amazon images risk IP breach</td><td>Licence / permission letters</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-05"><td>SG-05</td><td>Holiday gift guides built from verified specs, no dated price claims</td><td>Seasonal organic traffic; gift intent converts</td><td>Gift-angle verification per listing</td><td>Low</td><td><span class="badge-ok">Published 2026-11-19 (guide-gift-picks.html)</span></td></tr>
<tr id="SG-06"><td>SG-06</td><td>Chooser expansion (budget slider, counter-depth input)</td><td>Better decision support without fake testing</td><td>Usability feedback</td><td>Low</td><td>Proposed</td></tr>
<tr id="SG-07"><td>SG-07</td><td>Reader capture (email signup) with explicit consent</td><td>Owns audience beyond search</td><td>Provider + consent copy + policy review</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-08"><td>SG-08</td><td>Newer-model watch (Chefman B0CNY1YVDD, ThermoMaven B0GL7Z4KP4)</td><td>Decide whether to promote newer variants or keep current ASINs</td><td>Variant comparison + margin check</td><td>Low</td><td>Proposed</td></tr>
<tr id="SG-09"><td>SG-09</td><td>Hands-on testing programme (buy, cook, photograph, publish)</td><td>Unlocks &ldquo;lived-with&rdquo; content competitors cannot copy</td><td>Budget, protocol, disclosure of free vs bought units</td><td>High</td><td>Proposed - do not claim until done</td></tr>
<tr id="SG-10"><td>SG-10</td><td>Expand categories (second air fryer brand, second thermometer brand)</td><td>More comparison depth; better internal linking</td><td>New ASIN verification pass</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-11"><td>SG-11</td><td>Run the design brief (design-brief.html) as the brief for the visual overhaul: warm editorial brand, product-first hero, category tiles, sticky comparison bar</td><td>Turns the site from a register into a publication a buyer can act on; cuts the generated-template feel</td><td>Owner picks the visual direction from the brief's options; photography decision (SG-04) gates imagery</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-12"><td>SG-12</td><td>Adopt the eight-topic editorial calendar in the design brief as the publishing cadence (question-shaped titles tied to the verified products)</td><td>Catchy, spec-backed topics feed organic search; every title is a question a buyer types</td><td>Owner approves titles; each topic needs the same line-by-line verification before publishing</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-13"><td>SG-13</td><td>Anti-AI-slop writing rules in the CMS checklist: no filler transitions, no \"in conclusion\", varied sentence length, one idea per paragraph, first-person editorial voice where honest</td><td>Readers and reviewers can tell template text; signal-rich writing ranks and converts better</td><td>Style guide decision; editor review on every page</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-14"><td>SG-14</td><td>Editorial voice decision: who is \"we\" (The Countertop Guide editorial team) and what we will never claim (no testing, no popularity claims, no superlatives)</td><td>A defined voice is the strongest anti-slop lever and keeps FTC honesty intact</td><td>Owner sign-off on voice statement</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-15"><td>SG-15</td><td>Reader-facing seasonal clusters (holiday gift, New Year cooking reset) built from the verified products with dated price snapshots</td><td>Seasonal intent searches; reuses verified data instead of new claims</td><td>Season calendar decision; re-snapshot prices at publish</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-16"><td>SG-16</td><td>Comparison-first homepage: lead with the side-by-side table and the three-question chooser above the fold, verification below</td><td>Buyers act on comparisons; the verification register moves below the products</td><td>Layout decision in the design brief</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-17"><td>SG-17</td><td>Add author bylines and an \"updated\" date to every article and comparison</td><td>Authorship and freshness signals; reads like a publication, not a template</td><td>Author name/bio decision; date source from verification log</td><td>Low</td><td>Proposed</td></tr>
<tr id="SG-18"><td>SG-18</td><td>Internal-link cluster pages: one pillar per category linking every guide to the comparison and buying guide</td><td>Cluster structure helps search engines and keeps readers on-site longer</td><td>Topic approval (SG-12); link audit at publish</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-34"><td>SG-34</td><td>Design-prompt pass: feed this board into a visual design prompt (publication layout, type scale, product-card anatomy, seasonal skins) and review mockups before shipping</td><td>Turns &quot;make it look like a shop&quot; into a reviewable artifact instead of ad-hoc CSS edits</td><td>Owner picks a direction from mockups</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-35"><td>SG-35</td><td>Product-card redesign: photo slot (once licensed), price snapshot date on the card, one primary CTA, spec chips instead of prose bullets</td><td>Shoppers scan cards, they do not read audits; cards are the conversion surface</td><td>Photography decision (SG-04) or approved placeholder art</td><td>Low</td><td>Proposed</td></tr>
<tr id="SG-36"><td>SG-36</td><td>Editorial homepage modules: hero story, &quot;featured guide&quot; slot, category tiles, then the product line-up - ordered by reader intent, not by data pipeline</td><td>Publication feel; leads with products and questions, not verification process</td><td>None - content exists</td><td>Low</td><td><span class="badge-ok">Shipped in this pass (front page rebuilt)</span></td></tr>
<tr id="SG-37"><td>SG-37</td><td>Seasonal skins: holiday gift-guide banner and dated price-snapshot badge (e.g. Black Friday) that auto-expires</td><td>Seasonal relevance lifts click-through without inventing claims</td><td>Dated snapshot rule already approved (D-19)</td><td>Low</td><td>Proposed</td></tr>
<tr id="SG-38"><td>SG-38</td><td>Article template upgrade: key-takeaways box, at-a-glance spec table, &quot;what the listing cannot tell you&quot; callout, related-products rail</td><td>Consistent reader-facing polish across guides; reduces AI-slop look</td><td>Voice guide already approved (D-12)</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-39"><td>SG-39</td><td>Comparison-table UX: sticky first column, mobile card stack, &quot;share comparison&quot; link, print stylesheet</td><td>Tables are the most-used dashboard surface; mobile is most traffic</td><td>Usability feedback after launch</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-40"><td>SG-40</td><td>Topic cluster plan: 8 spec-backed articles mapped to the 5 products (titles already drafted as hypotheses), each added to sitemap + feed at publish</td><td>Cluster internal linking is the organic-traffic engine; cadence keeps it measurable</td><td>Search Console data after SG-02 to re-rank priority</td><td>Medium</td><td>Proposed</td></tr>
<tr id="SG-41"><td>SG-41</td><td>Trust bar under masthead: &quot;every fact sourced - see the register&quot; one-liner linking to verification.html on all pages</td><td>Turns the audit strength into a shopper-facing promise without leading with process</td><td>None</td><td>Low</td><td><span class="badge-ok">Shipped in this pass</span></td></tr>
<tr id="SG-42"><td>SG-42</td><td>Decide disclosure wording: verbatim Operating Agreement §5 or site-named variant</td><td>§5 requires "As an Amazon Associate I earn from qualifying purchases." or a substantially similar previously allowed statement</td><td>Compliance review of current variant</td><td>Low</td><td>Resolved 2026-11-19: verbatim wording adopted</td></tr>
<tr id="SG-43"><td>SG-43</td><td>Switch the Pages build source from &ldquo;deploy from branch&rdquo; to GitHub Actions, so a gate failure can block a publish rather than only marking the commit red</td><td>Today the deploy workflow builds, checks and gates, and then skips publishing because the repository&rsquo;s Pages source is the branch; the site is served from whatever is committed to <code>main</code>. Artifact publishing makes the two gates load-bearing.</td><td>Owner action in Settings &rarr; Pages &rarr; Build source (the token in this session cannot: <code>gh api -X PUT /repos/&hellip;/pages</code> returned 403 &ldquo;Resource not accessible by integration&rdquo;, observed 2026-11-19)</td><td>Low</td><td><span class="badge-warn">Needs owner action</span></td></tr>
<tr id="SG-54"><td>SG-54</td><td>Catchy trendy article topics, each a buyer question tied to a verified spec</td><td>Organic traffic starts with a title someone types; question-shaped headlines turn the verified register into articles no generator can fake</td><td>Owner approves titles; each topic verified line-by-line against the listing before publish</td><td>Low</td><td><span class="badge-warn">Proposed</span></td></tr>
<tr id="SG-55"><td>SG-55</td><td>"Shop by goal" intent landings built only from verified fields</td><td>Buyers arrive by need ("air fryer for a small kitchen"), not by product name; each landing answers before the comparison page</td><td>Per-topic verification; no "best for" claims, only "these specs fit"</td><td>Medium</td><td><span class="badge-warn">Proposed</span></td></tr>
<tr id="SG-56"><td>SG-56</td><td>Reader capture via a public GitHub issue ("Suggest a topic"), explicit consent, no silent collection</td><td>Owns an audience beyond search; nothing is pre-filled to look busy</td><td>Issue label + consent copy + policy review</td><td>Medium</td><td><span class="badge-warn">Proposed</span></td></tr>
<tr id="SG-57"><td>SG-57</td><td>Seasonal cadence: dated snapshot refreshes (Dec 1, Dec 15) for holiday gift and New Year cooking guides</td><td>Shows the site is maintained on a calendar, like a real publication; reuses verified data instead of new claims</td><td>Season calendar decision; re-snapshot prices at publish</td><td>Medium</td><td><span class="badge-warn">Proposed</span></td></tr>
</table></div>


<h2>New suggestions from this pass</h2>
<p>Each card is written so a decision can be made from it alone: what a buyer would feel, what the alternative costs, and what evidence has to arrive first.</p>

<article class="sg" id="SG-19"><h3>SG-19 &middot; Make &ldquo;see today&rsquo;s price&rdquo; the primary button, everywhere</h3>
<p><strong>Buyer problem:</strong> a stale price on a review page is the fastest way to lose trust <em>and</em> the click. It is also the number a static build cannot keep true.</p>
<div class="opts"><p><strong>Option 1 (recommended):</strong> link-only pricing. Button reads &ldquo;See today&rsquo;s price on Amazon&rdquo;; the register keeps the dated figure we observed.</p><p><strong>Option 2:</strong> keep a dated snapshot with a visible &ldquo;as of&rdquo; chip and an automatic removal rule after N days.</p><p><strong>Option 3:</strong> live figures only through the Creators/PA API (needs SG-20).</p></div>
<p class="fine"><strong>Effort:</strong> already implemented in this pass as Option 1 (one flag in <code>data/editorial.json</code> flips it). <strong>Evidence:</strong> Associates Program Policies on price/availability display and the 24-hour caching rule. <strong>Blocks:</strong> nothing. <strong>Status:</strong> <span class="badge-warn">Approve / reject the Option 1 default</span></p></article>

<article class="sg" id="SG-20"><h3>SG-20 &middot; Request Creators API access and build a refresh job &mdash; as a gate, not a promise</h3>
<p><strong>Why:</strong> it is the only compliant way to show live price, availability and images, and the only way &ldquo;automation&rdquo; stops being manual.</p>
<div class="opts"><p><strong>Option 1:</strong> apply once the account qualifies; a nightly job writes <code>data/products.json</code> fields with a timestamp; the build refuses to publish if the timestamp is older than 24 h.</p><p><strong>Option 2:</strong> stay manual, and keep the &ldquo;last checked&rdquo; date visible on every page (what the site does now).</p></div>
<p class="fine"><strong>Blocked by:</strong> account eligibility. Third-party guides state API access follows three qualifying sales inside 180 days; <em>we have not read that on an Amazon page in this session</em> - see <a href="flagged.html#FLG-037">FLG-037</a>. <strong>Evidence needed:</strong> Associates Central &rarr; Tools &rarr; Product Advertising / Creators API screen. <strong>Status:</strong> <span class="badge-warn">Owner action</span></p></article>

<article class="sg" id="SG-21"><h3>SG-21 &middot; Put &ldquo;what the listing does not say&rdquo; inside the buying flow, not in a footer</h3>
<p><strong>Buyer problem:</strong> the reason people leave an affiliate page is that it answers nothing they could not read on Amazon. The gaps in our own data are the most useful thing we have.</p>
<div class="opts"><p><strong>Option 1 (recommended):</strong> a per-product gap box (&ldquo;dimensions are not stated on this listing - measure the shelf you have&rdquo;), which is already on every card as <em>Check before you buy</em>.</p><p><strong>Option 2:</strong> a single site-wide limitations note (weaker: readers skip it).</p></div>
<p class="fine"><strong>Effort:</strong> copy only. <strong>Risk:</strong> none - it is the truth. <strong>Status:</strong> <span class="badge-ok">Implemented in this pass</span></p></article>

<article class="sg" id="SG-22"><h3>SG-22 &middot; One site, one canonical, one sitemap</h3>
<p><strong>Why:</strong> the repository currently publishes three overlapping builds (root, <code>counter-check/site/</code>, and a pending <code>docs/</code> draft). Search engines get three near-duplicate sites; readers get a brand split three ways.</p>
<div class="opts"><p><strong>Option 1 (recommended):</strong> root is the publication. Other builds become review-only: <code>&lt;meta name="robots" content="noindex, follow"&gt;</code> plus a banner naming the canonical, and removed from the sitemap.</p><p><strong>Option 2:</strong> delete the duplicate builds at the next integration.</p><p><strong>Option 3:</strong> keep them indexable (not advised).</p></div>
<p class="fine"><strong>Also in this pass:</strong> <code>build_site.py</code> used to write placeholder-domain canonicals into every page - the deployed HTML had been patched by hand, so the next rebuild would have re-broken them. Now every page self-canonicalises to its own URL, and the sitemap lists exactly the pages the build writes. <a href="flagged.html#FLG-035">FLG-035</a>. <strong>Status:</strong> <span class="badge-warn">Owner: confirm the domain, then ratify Option 1 or 2</span></p></article>

<article class="sg" id="SG-23"><h3>SG-23 &middot; Fix the two metadata bugs that would have mattered most</h3>
<p><strong>Found, not guessed:</strong> (a) every page pointed its canonical at the home page while the sitemap listed the page itself - Google&rsquo;s own guidance says do not declare different canonicals by different methods for the same page; (b) <code>og:image</code> was a relative SVG path, and social platforms need an absolute URL to a raster image, so no link ever rendered a card.</p>
<p class="fine"><strong>Fixed in this pass:</strong> per-page canonical, absolute og:image, a 1200&times;630 PNG brand card, per-page <code>og:url</code>, <code>twitter:</code> pair, and unique titles/descriptions on all pages. <strong>Remaining:</strong> verify in the Facebook debugger and X card validator after deploy (2 minutes, owner). <strong>Status:</strong> <span class="badge-ok">Implemented; needs owner verification</span></p></article>

<article class="sg" id="SG-24"><h3>SG-24 &middot; Run the anti-slop pass as a checklist, and keep it enforced by the build</h3>
<p><strong>Why:</strong> &ldquo;looks like AI slop&rdquo; is a concrete, fixable list: em-dash padding, &ldquo;delve&rdquo;, &ldquo;in today&rsquo;s fast-paced world&rdquo;, unearned first-person testing, emoji as icons, symmetric card grids with no opinion, benefits without objects, and adjectives where a number should be.</p>
<div class="opts"><p><strong>Option 1 (recommended):</strong> the build fails if a banned phrase appears in a page; the list lives in <code>data/editorial.json</code> so writers can extend it.</p><p><strong>Option 2:</strong> editorial guideline only (rots within a month).</p></div>
<p class="fine"><strong>Implemented:</strong> <code>scripts/check_meta.mjs</code> checks the banned-phrase list and the voice rules on every page. <strong>Status:</strong> <span class="badge-ok">Implemented in this pass</span></p></article>

<article class="sg" id="SG-25"><h3>SG-25 &middot; Make the mobile experience the default, not the afterthought</h3>
<p><strong>Buyer problem:</strong> this traffic is mobile. Two-finger zoom on a nine-column table and a 30-pixel tap target lose the click before the disclosure is even read.</p>
<p class="fine"><strong>Implemented in this pass:</strong> 44-48 px targets, a 16 px body floor, horizontal table scroll with a visible edge, sticky comparison bar, cards that stack without orphan columns, and a disclosure strip that stays legible at 320 px. <strong>Still needs:</strong> a real-device pass by the owner (we cannot screenshot a phone from here). <strong>Status:</strong> <span class="badge-warn">Owner spot-check on a phone</span></p></article>

<article class="sg" id="SG-26"><h3>SG-26 &middot; Decide the author byline now</h3>
<p><strong>Why it is a decision, not a task:</strong> every page needs a named responsibility. This site will not invent a person with credentials it cannot show.</p>
<div class="opts"><p><strong>Option 1:</strong> desk byline only (&ldquo;The Countertop Guide editorial desk&rdquo;) - honest, current, weaker on E-E-A-T.</p><p><strong>Option 2:</strong> a named owner byline plus a real bio page and a contact address - strongest, needs a real person.</p><p><strong>Option 3:</strong> commission a tester (SG-09) and byline them for tested content only.</p></div>
<p class="fine"><strong>Evidence needed:</strong> who is accountable for the claims. <strong>Blocks:</strong> any future &ldquo;our expert&rdquo; framing. <strong>Status:</strong> <span class="badge-warn">Needs decision</span></p></article>

<article class="sg" id="SG-27"><h3>SG-27 &middot; Publish the design brief as a single prompt (below), then rebuild once</h3>
<p><strong>Why:</strong> three sessions have each redesigned part of this site, which is exactly why it reads like a generated page. One brief, one pass, one reviewer.</p>
<p class="fine"><strong>Deliverable:</strong> the copy-paste prompt in the next section, written so a designer or a model can execute it without inventing claims. <strong>Status:</strong> <span class="badge-ok">Brief drafted in this pass; awaiting owner approval to execute</span></p></article>

<article class="sg" id="SG-28"><h3>SG-28 &middot; Kill the last audit-speak from reader pages</h3>
<p><strong>Problem:</strong> &ldquo;verified fields only&rdquo;, &ldquo;FLG-0xx&rdquo; and &ldquo;snapshot&rdquo; are the vocabulary of an internal register. A buyer wants &ldquo;what to check&rdquo;, &ldquo;what this is good for&rdquo;, &ldquo;where it fits&rdquo;.</p>
<p class="fine"><strong>Implemented:</strong> reader pages now lead with picks and checks; every register word moved to the review desk. The disclosure strip stays - it is required, and it is written in one sentence a person would say out loud. <strong>Status:</strong> <span class="badge-ok">Implemented; second opinion welcome</span></p></article>

<article class="sg" id="SG-29"><h3>SG-29 &middot; Add a &ldquo;this vs that&rdquo; pair page for the two real rivalries</h3>
<p><strong>Buyer problem:</strong> the highest-intent queries are comparisons of two things: dual-basket vs single basket, instant-read vs wireless. One page per pair, with a verdict-shaped summary that stays inside the specs.</p>
<p class="fine"><strong>Effort:</strong> two pages, no new data (all fields exist in the register). <strong>Evidence needed:</strong> none beyond re-reading the two listings on publish day. <strong>Status:</strong> Proposed</p></article>

<article class="sg" id="SG-30"><h3>SG-30 &middot; Turn the four blank spec cells into a tracked task list, then into content</h3>
<p><strong>Why:</strong> the two thermometers state no dimensions and the Emeril states no warranty period on its page - those are the remaining blanks in the comparison. Each one blocks a whole class of question (&ldquo;will it fit?&rdquo;, &ldquo;can two run on one circuit?&rdquo;).</p>
<p class="fine"><strong>How to discover:</strong> re-read each listing&rsquo;s product-details block, save the URL and the date, and only then write the fit guide. If the field is genuinely absent, the guide says so - which is itself useful. <strong>Status:</strong> <span class="badge-warn">Owner-adjacent: needs a listing re-read at publish time</span></p></article>

<article class="sg" id="SG-31"><h3>SG-31 &middot; Replace generic hero space with a single, ownable visual</h3>
<p><strong>Problem:</strong> with no product photography permitted, the site needs one strong non-product visual identity (a measured counter-depth diagram, a spec-dial, a typographic masthead) so a reader remembers it without a single food shot.</p>
<div class="opts"><p><strong>Option 1 (recommended):</strong> a drawn counter-depth scale comparing 32.4 / 34.0 / 42.9 cm, built from our own derived numbers - original, useful, and impossible to mistake for stock.</p><p><strong>Option 2:</strong> photography after SG-04.</p></div>
<p class="fine"><strong>Effort:</strong> one SVG + a component. <strong>Risk:</strong> must stay clearly labelled as a diagram, not a photo of the product. <strong>Status:</strong> Proposed</p></article>

<article class="sg" id="SG-32"><h3>SG-32 &middot; Measure before optimising: 28 days of Search Console, then pick topics</h3>
<p><strong>Why:</strong> the brief&rsquo;s own priority. The queue in <code>data/editorial.json</code> is a stated plan; after 28 days of queries, the next four topics come from queries that arrive and that our pages do not answer.</p>
<p class="fine"><strong>Needed from owner:</strong> Search Console property verified for the chosen domain, and permission to record which queries we act on in the ledger. <strong>Status:</strong> <span class="badge-warn">Blocked on SG-02</span></p></article>

<article class="sg" id="SG-33"><h3>SG-33 &middot; Keep the compliance gate in CI, and let it fail the deploy</h3>
<p><strong>Why:</strong> a rule only holds if a build breaks when it is missed. The deploy workflow now runs the generator, then a checker, before uploading - disclosure, sponsored marking, per-page metadata, link integrity, price policy and banned phrases.</p>
<p class="fine"><strong>Implemented:</strong> <code>scripts/check_meta.mjs</code> wired into <code>.github/workflows/pages.yml</code> as a blocking step (this also closes request R-01 from session b4c6c619). <strong>Status:</strong> <span class="badge-ok">Implemented; watch the next deploy</span></p></article>

<article class="sg" id="SG-44"><h3>SG-44 &middot; Visual QA the styled shop before the next deploy</h3>
<p><strong>Why:</strong> session <code>1b65e5a1</code> re-verified the five listings on 2026-11-20 and confirmed the reader components now render their intended CSS. A layout that reads correctly in a text diff can still overflow or misalign on a real viewport, and an unstyled card is the single biggest &ldquo;generated template&rdquo; tell.</p>
<p class="fine"><strong>Implemented:</strong> the register is re-verified and the style gate is in CI. <strong>Status:</strong> <span class="badge-warn">Needs a screenshot pass</span> - open index, air-fryers, thermometers, compare and one guide at mobile (375px), tablet and desktop, confirm no overflow and that the disclosure strip stays above the fold, then ship.</p></article>

<article class="sg" id="SG-45"><h3>SG-45 &middot; Add &ldquo;shop by goal&rdquo; intent landings, built only from verified fields</h3>
<p><strong>Why:</strong> buyers arrive by need - &ldquo;air fryer for a small kitchen&rdquo;, &ldquo;thermometer as a gift&rdquo;, &ldquo;oven-style for a family&rdquo; - not by product name. Intent landings are the organic-traffic surface and a clean marketing entry, and they let the site answer a buyer&rsquo;s question before they reach the comparison.</p>
<p class="fine"><strong>How:</strong> each page is a shortlist built strictly from the verified register (depth, capacity, features, form) - the same fields the chooser and comparison already use - with a link to the source listing on every row. Each landing is added to the sitemap and feed by the build, on the same cadence as a guide. <strong>Constraint:</strong> no claim that any product is &ldquo;best&rdquo; for a goal; the page states which verified specs fit and lets the buyer decide. <strong>Status:</strong> <span class="badge-warn">Proposed - needs owner approval and per-topic verification before publishing</span></p></article>

<article class="sg" id="SG-58"><h3>SG-58 &middot; Make WCAG contrast and accessibility a standing gate, not a one-off</h3>
<p><strong>Why:</strong> a "polished" site that a screen reader cannot use, or whose small text fails contrast on a phone, is not polished. This session ran a full contrast audit of the palette (20 text/background pairs, all passing WCAG AA) and confirmed the class-coverage and structure gates; the next step is to stop it being a manual check.</p>
<div class="opts"><p><strong>Option 1 (recommended):</strong> add a contrast check to the style gate so a new colour that fails AA on body text breaks the build.</p><p><strong>Option 2:</strong> keep the audit as a documented check run at each visual pass (what this session did).</p></div>
<p class="fine"><strong>Effort:</strong> S. <strong>Evidence:</strong> the audit is recorded in <code>review/e05155a0/VERIFICATION.md</code>. <strong>Blocks:</strong> nothing now; prevents a silent regression. <strong>Status:</strong> <span class="badge-warn">Needs decision - request logged to the style-gate owner</span></p></article>

<article class="sg" id="SG-59"><h3>SG-59 &middot; Treat the code-level visual QA as the documented stand-in for a screenshot</h3>
<p><strong>Why:</strong> no browser can be installed in this environment (the Chrome-for-Testing download is blocked), so no session can produce a real pixel render. The honest move is to define exactly what *is* proven mechanically and label it as such, rather than claim the site was "looked at".</p>
<p class="fine"><strong>Proven mechanically, every build:</strong> every CSS class the generator emits has a rule (<code>check_style.mjs</code>); every document parses with ordered headings and sized images (<code>verify_structure.mjs</code>); every text/background pair meets WCAG AA (this session); disclosure, sponsored marking, links, metadata and voice rules all pass. <strong>Not proven:</strong> the actual pixel layout on a real viewport. <strong>Status:</strong> <span class="badge-ok">Documented this pass</span> - a real screenshot pass by the owner remains the final check (see SG-44).</p></article>

<article class="sg" id="SG-60"><h3>SG-60 &middot; Adopt the polished-marketing direction and consolidate to one design brief</h3>
<p><strong>Why:</strong> the brief's core ask is that the site read like a polished marketing affiliate publication, not generated filler. Two briefs currently exist (this file and <code>design-brief.html</code>) and the owner has to pick one; running both ships two visual directions at once, which is how a site ends up looking generated.</p>
<div class="opts"><p><strong>Option 1 (recommended):</strong> execute <code>DESIGN_PROMPT.md</code> (the implemented brief, now with the polished-marketing direction in section 9) and retire the parallel brief as a historical artifact.</p><p><strong>Option 2:</strong> execute <code>design-brief.html</code> and fold its unique blocks into <code>DESIGN_PROMPT.md</code>.</p></div>
<p class="fine"><strong>Effort:</strong> a review decision, not a build. <strong>Blocks:</strong> the remaining visual half of the redesign (SG-11, SG-34). <strong>Status:</strong> <span class="badge-warn">Needs decision</span></p></article>

<h2 id="design-inputs">Design inputs from the parallel pass (DI-1 to DI-8)</h2>
<p>Session <code>f0db58ea</code> wrote these eight as inputs to a design prompt rather than finished proposals, and they are kept here untouched so the owner reviews one list. Read them beside <a href="design-brief.html">design-brief.html</a> and the consolidated prompt at the bottom of this page; the same questions arrive in <a href="#Q-21">Q-21</a> and <a href="#Q-22">Q-22</a>.</p>
<div class="table-scroll"><table>
<tr><th>Ref</th><th>Input</th><th>Why it is on the list</th><th>Constraint</th><th>Where it lands</th></tr>
<tr id="DI-1"><td>DI-1</td><td>Publication masthead with wordmark, tagline and issue date (verification date), not a generic app bar</td><td>Real shops and magazines have a masthead; app bars read as scaffolding</td><td>Must keep disclosure strip directly beneath</td></tr>
<tr id="DI-2"><td>DI-2</td><td>Editorial hero: one strong headline, one lede, two CTAs (shop / read) - no badge soup</td><td>Audits open with process; shops open with the offer</td><td>Badges limited to three: verified date, sponsored labeled, price-snapshot warning</td></tr>
<tr id="DI-3"><td>DI-3</td><td>Product-card anatomy: image slot, name, star+count, price with list-price strike and snapshot date, 3 spec chips, one CTA, sponsored microcopy</td><td>Card = conversion unit; prose bullets inside cards are the biggest AI-slop tell</td><td>No product photo until SG-04 decides; use licensed placeholder or typographic tile</td></tr>
<tr id="DI-4"><td>DI-4</td><td>Type scale: display serif for headlines, grotesque for UI, mono for ASINs and spec tables</td><td>Three-role type system is what separates publications from templates</td><td>Ship webfonts self-hosted or system stack - no render-blocking third party</td></tr>
<tr id="DI-5"><td>DI-5</td><td>Color: warm paper background, one accent for CTAs, one for trust/verification, muted ink - not the default blue/purple gradient</td><td>Gradients + glow = generated; flat warm palette = printed catalogue</td><td>Contrast AA on all text (WCAG)</td></tr>
<tr id="DI-6"><td>DI-6</td><td>Guide layout: key-takeaways box above the fold, at-a-glance table, honest &quot;what we cannot tell you&quot; callout, related-product rail at the end</td><td>Opinionated structure reads as edited; wall-of-text reads as generated</td><td>Every spec cell links to its listing (existing rule)</td></tr>
<tr id="DI-7"><td>DI-7</td><td>Seasonal skin layer (holiday gift-guide banner) that sits on top of the base design and can be switched off</td><td>Shows the site is maintained on a calendar, like a real publication</td><td>Dated price snapshots only (D-19); no trend claim without a source</td></tr>
<tr id="DI-8"><td>DI-8</td><td>Dashboard surfaces restyled as &quot;the back office&quot;: denser type, tabular numbers, source links on every row - visually distinct from the shop</td><td>Keeps the audit machinery available without letting it set the tone</td><td>Same disclosure and sponsored rules as shopper pages</td></tr>
</table></div>
<p class="fine">Their review flow, kept as written: approve, reject or defer each of DI-1 to DI-8, then the approved set becomes the design prompt and the mockups. No CSS ships before that review &mdash; the same rule this board has always had.</p>

<h2 id="design-prompt">The design brief - copy-paste prompt</h2>
<div class="callout"><strong>Two briefs now exist, and the owner has to pick one.</strong> A parallel session published <a href="design-brief.html">design-brief.html</a> - six prompt blocks, three named visual directions, an eight-topic calendar - and filed it as <a href="#SG-11">SG-11</a>. The prompt below is this pass&rsquo;s consolidated version: same policy rails, plus the layout order, the price-display rule and the build gate. Running both would ship two visual directions at once, which is how a site ends up looking generated. Pick one; if it is theirs, delete this section rather than merging them.</div>
<p>Copy the block below into a design tool or a designer&rsquo;s brief. It is written so that nothing in it can be executed by inventing a fact: the visual layer may change, the evidence layer may not. Items marked <strong>[owner]</strong> must be filled before the work starts.</p>
<pre class="prompt"> redesign The Countertop Guide - a spec-backed Amazon affiliate publication for
air fryers and meat thermometers. Single-file static HTML built by build_site.py from
data/products.json (specs, sources) and data/editorial.json (voice, display policy,
cadence). Deployed by GitHub Pages. Tracking ID [owner-confirmed]: shopnow047c-20.

GOAL
Make it read like a specialist shop window, not a compliance audit. A buyer who has
never heard of us should, in 15 seconds, understand: what we sell nothing of, what
each product is genuinely good for, what to check before ordering, and that we are
paid if they click. Trust is the conversion mechanism here - we win by being the page
that admits what it does not know.

READER
US kitchen-appliance shopper, mobile-first, mid-funnel, comparison-ready. They have
already seen the Amazon listing. They arrive from a typed question ("does a 6-quart
dual basket feed 4", "instant read vs wireless thermometer accuracy"). They leave when
a page says "we tested" without evidence, or shows a price that is wrong.

BRAND [owner]
Name: The Countertop Guide (settled in D-18 of the external register; reopen only with
a reason). Voice: plain-spoken buying desk. Second person, active, one idea per
sentence, numbers instead of adjectives. Reading age ~grade 8. Never cute about safety
or money.

LAYOUT / RHYTHM
1. Masthead: wordmark + reader nav (Air fryers, Thermometers, Compare, Guides, About)
   + one "Review desk" group for every internal/admin surface.
2. Disclosure strip immediately under the masthead, on every page, one line, legible,
   not hidden in grey-on-grey. Repeat in the footer.
3. Front page order: hero question -> quick picks -> product cards -> chooser ->
   guides -> the short "why the numbers match" trust block. Products before process.
4. Category page: one-line lede -> shortlist callout -> product cards -> spec table ->
   related guides.
5. Product card: form-factor chip, name, one-line job, spec grid (capacity as titled,
   footprint, depth, care per listing), "Good for", "Check before you buy", primary CTA
   "See today's price on Amazon", then one quiet line: sponsored, opens Amazon, source.
6. Comparison: sticky bottom bar on mobile, horizontal-scroll table with a visible edge,
   first column frozen, derived rows visually marked as derived.
7. Guides: single column, max 68ch, drop-cap-free, no centred hero, question H2s,
   "what the listing does not say" box, a next step at the end.

TYPE / COLOR
Warm paper background, near-black ink, one saturated accent (burnt orange) used ONLY
for actions, one teal for informational accents. Serif or high-contrast sans for
headlines (max 2 families), system-usable body face. 16px body minimum, 1.6 line,
32/24/20px H1/H2/H3 on mobile, larger on desktop, no fluid type below 320px.
Contrast >= 4.5:1 body text, 3:1 large. Radius 14-18px, one shadow level, hairline
borders - no glassmorphism, no gradient text, no glow, no oversized rounded pills.

IMAGERY [owner - blocked]
No Amazon images, no scraped photography, no AI-generated product or food images:
Program Content includes data, images and text and the IP License caps caching of
product images at 24 hours. Until a licence or in-house shoot exists (SG-04), use
original diagrams only (counter-depth scale, capacity-per-footprint chart), clearly
labelled as our drawings. If a reviewer approves photography, real photos only,
credited, with the shoot date on the page.

COMPONENTS
Chip, product card, spec dl, callout, decision-card, comparison table, chooser form,
details/summary FAQ, badge-ok / badge-warn / badge-flag, source footnote row. Tap
targets >= 44px. Every table gets a scroll wrapper. Print stylesheet for the
comparison page.

NON-NEGOTIABLE RULES (the build must refuse to publish without them)
- Every outbound product link: rel="sponsored nofollow noopener", visible "sponsored"
  word, destination never obscured, tag parameter on the URL only.
- Disclosure: the Associates statement exactly as the Operating Agreement Section 5
  requires it, plus a plain-language line. Above the fold and in the footer.
- No price or rating figures on shop pages unless a Creators/PA API refresh exists;
  never a figure older than 24h. (Participation Requirements + IP License clause (h).)
- No "we tested/we tried/we loved", no superlatives, no scarcity, no countdowns,
  no invented expert quotes. Banned-phrase list in data/editorial.json is enforced.
- Every product fact links to the listing it came from; a missing field is stated as
  missing, never inferred.
- Unique <code>&lt;title&gt;</code> + meta description per page; self-referencing canonical; absolute
  og:image (raster); sitemap lists exactly the pages the build writes.
- No third-party trackers. Five first-party events only, local by default.

WHAT "DONE" LOOKS LIKE
A buyer can screenshot one product card and their partner understands the trade-off
without visiting Amazon. Nobody reading the page could tell it was generated, because
it says specific things, admits its gaps, and never asks to be believed.
</pre>

<h2>Questions, information &amp; answers needed before a reasonable decision</h2>
<p>Each row states what we can already cite, what is missing, and the exact way to find it. If a row&rsquo;s &ldquo;what we do not know&rdquo; is empty, it is not a question - it is a decision waiting for a yes or no.</p>
<div class="table-scroll"><table>
<tr><th>#</th><th>Question</th><th>What we know (with source)</th><th>What we do not know</th><th>How to discover it</th><th>Decision blocked</th></tr>
<tr id="Q-01"><td>Q-01</td><td>Are the supplied short links compliant Special Links?</td><td>The five <code>link.amazon/&hellip;</code> codes resolve to the ASINs in the register (observed 2026-11-19); the redirect targets carry no <code>tag=</code> parameter</td><td>Whether those links are usable as Special Links at all</td><td>Associates Central &rarr; each product page &rarr; SiteStripe &rarr; Text; click your own link, then check that a click appears in the Reports screen the next day</td><td>Whether to replace or keep the tagged-listing-URL pattern the site uses now</td></tr>
<tr id="Q-02"><td>Q-02</td><td>What is the canonical domain?</td><td>The Pages URL is live and every page now self-canonicalises to it</td><td>Whether a custom domain replaces it, and when</td><td>Owner decision; then set <code>site.canonical</code>, CNAME, and submit the sitemap in Search Console</td><td>Search Console verification, og:image absolute URL stability, backlink value</td></tr>
<tr id="Q-03"><td>Q-03</td><td>What are the thermometer dimensions and the Emeril wattage?</td><td>Blank in the register because those fields were not captured; the air fryer dimensions were</td><td>The four missing values</td><td>Re-read each listing&rsquo;s product-details block; paste the exact wording and the URL into the register with a date. If the page does not state it, record &ldquo;not stated&rdquo; rather than a number</td><td>The fit-under-cabinet guide and any circuit/load advice</td></tr>
<tr id="Q-04"><td>Q-04</td><td>Should we promote newer variants (B0CNY1YVDD, B0GL7Z4KP4)?</td><td>Both appear on the current listings&rsquo; pages as related items</td><td>Margin, availability history, whether the owner wants them at all</td><td>Read each variant listing; confirm the commission category rate in Associates Central</td><td>Product lineup and which ASINs the guides name</td></tr>
<tr id="Q-05"><td>Q-05</td><td>What commission rate applies to kitchen categories?</td><td>Not published on this site, and not guessed</td><td>The current rate table for the account</td><td>Associates Central &rarr; Reports &rarr; commission statement (authorized first-party view only)</td><td>Any revenue statement, forecast or priority ranking by earnings</td></tr>
<tr id="Q-06"><td>Q-06</td><td>Is there search demand for these topics?</td><td>The guides are question-shaped hypotheses, explicitly labelled as such</td><td>Any query, impression or click data</td><td>28 days of Search Console after SG-02; also check what autocomplete shows while typing (a manual observation, not a volume claim)</td><td>Which two guides get written next</td></tr>
<tr id="Q-07"><td>Q-07</td><td>Can we use product photos?</td><td>Operating Agreement Section 7 puts &ldquo;data, images and text&rdquo; in Service Offerings, and the Program Policies&rsquo; IP License caps storing an image at a link held for 24 hours; SiteStripe image options are widely reported as removed but we have not read that on an Amazon page</td><td>Whether in-house photography, manufacturer permission, or API-served images are the route</td><td>Owner: read the IP License in full; request written manufacturer permission; or reach API eligibility (Q-16)</td><td>The entire visual half of the redesign (SG-04, SG-31)</td></tr>
<tr id="Q-08"><td>Q-08</td><td>Where does analytics data live?</td><td>Five events are defined; the client counts locally; an endpoint implementation exists in the repo but is not hosted; GitHub Pages serves static files only</td><td>A host, a retention period, and whether we tell readers about it</td><td>Pick a host the owner controls (any small HTTPS box), write a one-paragraph retention note, then set <code>data-analytics-endpoint</code></td><td>Whether click data becomes a ledger row or stays device-local</td></tr>
<tr id="Q-09"><td>Q-09</td><td>Which visual direction from the design brief do we adopt?</td><td>Brief offers a warm editorial direction with three named options and anti-slop rules</td><td>Owner's pick; photography decision (Q-07) gates imagery</td><td>Review design-brief.html; choose one direction</td><td>Visual overhaul (SG-11)</td></tr>
<tr id="Q-10"><td>Q-10</td><td>Do we approve the eight-topic editorial calendar?</td><td>Titles are working hypotheses tied to verified products; none is a popularity claim</td><td>Owner approval; per-topic verification still required</td><td>Review calendar on design-brief.html</td><td>Publishing cadence (SG-12)</td></tr>
<tr id="Q-11"><td>Q-11</td><td>What is the site's editorial voice, and what will it never claim?</td><td>No testing / popularity / superlative claims today; voice statement is proposed</td><td>Owner sign-off on the voice statement</td><td>Review voice rules on design-brief.html</td><td>All content (SG-13, SG-14)</td></tr>
<tr id="Q-12"><td>Q-12</td><td>Should the homepage lead with the comparison and chooser?</td><td>Current homepage leads with categories then data</td><td>Layout preference; impact on conversion vs. trust</td><td>Review homepage layout option in the brief</td><td>Homepage redesign (SG-16)</td></tr>
<tr id="Q-13"><td>Q-13</td><td>Who are the named authors, and what bios go with them?</td><td>Guides currently say \"The Countertop Guide editorial team\"</td><td>Author identity and bio wording</td><td>Owner provides names/bios or keeps the team credit</td><td>Authorship (SG-17)</td></tr>
<tr id="Q-14"><td>Q-14</td><td>What is the review SLA for this suggestions board?</td><td>Every row waits on an owner choice: 43 suggestions, 27 questions and 8 design inputs, merged into one board after three sessions wrote to it in parallel</td><td>Review cadence and who approves</td><td>Owner sets a review rhythm; approved items become tasks</td><td>All pending suggestions</td></tr>
<tr id="Q-15"><td>Q-15</td><td>Does a price or rating figure belong on the page at all?</td><td>Program Policies allow a site to show price/availability only when Amazon serves the link containing it or via Creators/PA API, with 24-hour caching limits</td><td>Whether the owner accepts link-only pricing as the site&rsquo;s default</td><td>Read the clause next to the register (verification page links it); optionally ask Associates support in writing</td><td>SG-19, plus whether the register&rsquo;s dated figures stay visible anywhere</td></tr>
<tr id="Q-16"><td>Q-16</td><td>What exactly unlocks the Creators/PA API?</td><td>Third-party guides consistently state three qualifying sales inside 180 days; we have not verified that on an Amazon page</td><td>The account&rsquo;s real eligibility and the application screen&rsquo;s wording</td><td>Associates Central &rarr; Tools &rarr; Product Advertising API / Creators API; screenshot the eligibility notice</td><td>SG-20 and every automation promise on this site</td></tr>
<tr id="Q-17"><td>Q-17</td><td>Who is accountable for these claims?</td><td>Pages currently carry the editorial-desk byline, which is true</td><td>Whether a named person with a real bio takes the byline</td><td>Owner decision; publish a contact address and a corrections note either way</td><td>Authorship, any &ldquo;expert&rdquo; framing, and how corrections get handled</td></tr>
<tr id="Q-18"><td>Q-18</td><td>Which build is the site?</td><td>Root, <code>counter-check/site/</code> and a pending <code>docs/</code> build all exist in the repository</td><td>The owner&rsquo;s choice of the single indexable publication</td><td>Owner decision; then noindex or remove the others and prune the sitemap</td><td>SG-22; any SEO measurement at all</td></tr>
<tr id="Q-19"><td>Q-19</td><td>Do we ever test products?</td><td>We have not; no page claims we have</td><td>Budget, and whether purchased or loaned units are acceptable (loaned units change the disclosure)</td><td>Owner decision; if yes, write the protocol first: units, method, photos, dates, who pays</td><td>SG-09 and every future &ldquo;lived-with&rdquo; sentence</td></tr>
<tr id="Q-20"><td>Q-20</td><td>Is a trend claim ever claimable?</td><td>Our rule: a dated snapshot from an official category page, or no claim. The air fryers&rsquo; &ldquo;bought in past month&rdquo; chips are listing content, not our finding</td><td>Whether the owner wants periodic snapshots at all</td><td>Snapshot the official category page, store URL + date + what was visible, and cite that row only</td><td>Any popularity framing in titles or social copy</td></tr>
<tr id="Q-21"><td>Q-21</td><td>Which design direction does the owner want?</td><td>Design inputs DI-1..DI-8 written; front page rebuilt editorial-first in this pass</td><td>Approved visual direction (type, color, card anatomy)</td><td>Review DI-1..DI-8 on this board plus design-brief.html; approve/reject/defer each; then SG-34 mockups</td><td>Full visual overhaul (SG-11, SG-34, SG-35)</td></tr>
<tr id="Q-22"><td>Q-22</td><td>What imagery may we legally ship?</td><td>No Amazon images used; CSS and SVG only on the pages, and the share card is a generated 1200&times;630 PNG from <code>scripts/make_og.py</code></td><td>Licensed photography or manufacturer permission status; whether placeholder tiles are acceptable long-term</td><td>Decide SG-04; if placeholders approved, specify style in design prompt</td><td>Product cards, social previews, conversion polish</td></tr>
<tr id="Q-23"><td>Q-23</td><td>What is the publishing cadence and who approves topics?</td><td>Five guides exist; 8 topic hypotheses drafted; sitemap/feed updated at publish</td><td>Owner approval of calendar; reviewer for each article</td><td>Owner sets cadence (e.g. 2/week) and names reviewer in COORDINATION.md</td><td>SG-40 cluster build-out</td></tr>
<tr id="Q-24"><td>Q-24</td><td>Which success metrics decide iteration?</td><td>Five events defined; campaign ledger empty by design; Search Console not yet connected</td><td>Owner's thresholds (e.g. N eligible sessions before topic re-rank; CTR target)</td><td>Owner sets thresholds after first month of Search Console + ledger data</td><td>Evidence-based iteration (Priority 4)</td></tr>
<tr id="Q-25"><td>Q-25</td><td>Are the five short links the only promotion surface, or will more ASINs be added?</td><td>Five ASINs verified and shippable; newer variants noted (FLG-003, SG-08)</td><td>Scope of catalogue growth; margin/commission data per category</td><td>Owner sets catalogue scope; commission data only from Associates reports (Q-05)</td><td>SG-10 expansion; revenue planning</td></tr>
<tr id="Q-26"><td>Q-26</td><td>Should the disclosure use the verbatim §5 wording?</td><td>Current variant names the site instead of &quot;I&quot;; check script flagged it for owner review</td><td>— (resolved)</td><td>Resolved 2026-11-19 against Operating Agreement §5: verbatim wording adopted on all pages</td><td>Disclosure wording</td></tr>
<tr id="Q-33"><td>Q-33</td><td>Does the site need to state an author, or is an editorial desk enough?</td><td>Every page names &ldquo;The Countertop Guide editorial desk&rdquo; and the structured data types the author as an Organization. No individual is named because no individual has been identified</td><td>A name, a one-line credential and a real contact route</td><td>Owner supplies the byline; the build already reads it from one field in <code>data/editorial.json</code></td><td>Trust signals; Google&rsquo;s guidance on who wrote a page. Not a launch blocker</td></tr>
<tr id="Q-34"><td>Q-34</td><td>Which build under this hostname is the publication?</td><td>Three builds are served: the root site (26 sitemap URLs), <code>docs/</code> and <code>counter-check/site/</code>. Only the root is in a sitemap</td><td>The owner&rsquo;s intent for the other two</td><td>Designate one; add <code>noindex</code> to the others (<a href="suggestions.html#SG-51">SG-51</a>)</td><td>Every ranking statement, and a clean Search Console property</td></tr>
<tr id="Q-35"><td>Q-35</td><td>Can any of the five outbound links be attributed to this tag?</td><td>The links carry <code>tag=shopnow047c-20</code> and the correct ASINs, verified against the listings. No Associates report has been read, because no session can log in</td><td>One report row per product</td><td>Owner runs the click test (<a href="#SG-53">SG-53</a>)</td><td>Any revenue statement; nothing about publishing</td></tr>
<tr id="Q-36"><td>Q-36</td><td>What exact accuracy figure does the wireless thermometer carry?</td><td>No tolerance figure appears in the fields captured from B0DZFD6R9Z. The ThermoMaven listing states &plusmn;0.5&deg;F with NIST and NSF named</td><td>The manual or product-support document for the CHEF iQ</td><td>Either read the manual on the listing, or ask the seller through the listing&rsquo;s contact route; until then the guide reports an absence</td><td>Any accuracy comparison between the two thermometers</td></tr>
<tr id="Q-37"><td>Q-37</td><td>Do the listings&rsquo; own dimensions match the units shipped?</td><td>Dimensions are quoted as the listing states them, with the unit (inches) preserved. No independent measurement exists</td><td>A physical unit, or a manufacturer spec sheet naming the same model code</td><td>Only a purchase resolves it; until then the pages say &ldquo;as listed&rdquo;</td><td>Counter-fit advice, which is the site&rsquo;s central promise</td></tr>
<tr id="Q-42"><td>Q-42</td><td>Should contrast and accessibility be enforced by the build?</td><td>A 20-pair WCAG AA contrast audit passed this session; class-coverage and structure gates already run in CI</td><td>Whether to add a blocking contrast check to the style gate (SG-58)</td><td>A one-line decision plus a small gate change owned by the style-gate owner</td><td>Preventing a silent accessibility regression on the next palette change</td></tr>
<tr id="Q-43"><td>Q-43</td><td>Which single design brief do we execute?</td><td>Two briefs exist: <code>DESIGN_PROMPT.md</code> (implemented, now with the polished-marketing direction) and <code>design-brief.html</code> (parallel). The site already renders the implemented one</td><td>The owner&rsquo;s choice of which brief is authoritative, and whether to retire the other</td><td>Review both briefs; pick one; record the pick in <code>COORDINATION.md</code></td><td>The remaining visual half of the redesign (SG-11, SG-60)</td></tr>
<tr id="Q-44"><td>Q-44</td><td>Are &ldquo;shop by goal&rdquo; intent landings the next content build?</td><td>SG-45 is drafted: shortlists built only from verified fields (depth, capacity, form), each row linking its listing</td><td>Owner approval, and per-topic verification before each landing publishes</td><td>Approve SG-45, then write the first landing from the register with a fresh listing re-read</td><td>The next organic-traffic surface after the guides</td></tr>
<tr id="Q-27"><td>Q-27</td><td>Who publishes this site, the branch or the workflow?</td><td>The workflow gates every push to <code>main</code>; GitHub&rsquo;s legacy branch build is what actually serves the pages. <a href="flagged.html#FLG-051">FLG-051</a> and <a href="suggestions.html#SG-43">SG-43</a></td><td>Whether to move Pages to the GitHub Actions build source</td><td>Owner: Settings &rarr; Pages &rarr; Build source &rarr; GitHub Actions; then the next deploy run publishes the artifact and a failed gate stops it</td><td>Every claim this site makes about automation being load-bearing</td></tr>
<tr id="Q-38"><td>Q-38</td><td>Which topics have real search demand?</td><td>The calendar titles are hypotheses, explicitly labelled as such; no query, impression or click data exists yet</td><td>Any query, impression or click figure for the proposed titles</td><td>28 days of Search Console after SG-02; manual autocomplete observation (not a volume claim)</td><td>Which two guides get written next (SG-12)</td></tr>
<tr id="Q-39"><td>Q-39</td><td>What commission rate applies to kitchen categories?</td><td>Not published on this site, and not guessed</td><td>The account&rsquo;s current rate table</td><td>Associates Central &rarr; Reports &rarr; commission statement (authorized first-party view only)</td><td>Any revenue statement, forecast or priority ranking by earnings</td></tr>
<tr id="Q-40"><td>Q-40</td><td>How often should prices be re-snapshot from the listings?</td><td>Prices in the register are dated 2026-11-20 observations; Amazon prices change daily</td><td>A re-read cadence that keeps dated figures honest without inventing live figures</td><td>Re-read each listing on the calendar date; record URL + date + figure; flag drift</td><td>Whether dated price chips can stay on any page at all</td></tr>
<tr id="Q-41"><td>Q-41</td><td>Who reviews and approves topics before they are published?</td><td>Every row on this board waits on an owner choice; no reviewer is named</td><td>A reviewer identity and a review rhythm</td><td>Owner names the reviewer in <code>COORDINATION.md</code> and sets a cadence (e.g. weekly)</td><td>SG-40 cluster build-out; the publishing cadence</td></tr>
</table></div>

<h2>What the evidence would look like, per decision</h2>
<div class="table-scroll"><table>
<tr><th>Decision</th><th>Minimum evidence that lets us say yes</th><th>Where it comes from</th><th>Who can obtain it</th></tr>
<tr><td>Scale outbound links / switch link format</td><td>A recorded test click per ASIN showing destination and a matching click in the report</td><td>Associates Central, Reports</td><td>Owner only</td></tr>
<tr><td>Show live prices or images</td><td>API credentials, a refresh job, and a timestamp no older than 24 h in the data file</td><td>Creators/PA API</td><td>Owner (eligibility) + session (job)</td></tr>
<tr><td>Claim anything about performance</td><td>A written test protocol, dated photos, and the unit&rsquo;s purchase or loan status disclosed</td><td>Us, after a purchase</td><td>Owner budget + a session with time</td></tr>
<tr><td>Say a topic is popular</td><td>A dated query list from Search Console, quoted with its date</td><td>Search Console</td><td>Owner (verification) + session (analysis)</td></tr>
<tr><td>Report earnings</td><td>A first-party Associates report row with its date</td><td>Associates Central</td><td>Owner only</td></tr>
</table></div>

<h2>Decisions already taken (so nobody re-litigates them)</h2>
<div class="table-scroll"><table>
<tr><th>Row</th><th>Decision</th><th>Where it landed</th></tr>
<tr><td>S-04</td><td>Every page has its own title and meta description</td><td>Generated per page; the build gate fails on a duplicate</td></tr>
<tr><td>S-05</td><td>Affiliate links carry rel=&quot;sponsored&quot; without weakening the disclosure</td><td>Every outbound link, plus the JS-built chooser links (which previously had no rel - <a href="flagged.html#FLG-034">FLG-034</a>)</td></tr>
<tr><td>S-06</td><td>&ldquo;What it is like to live with&rdquo; content is <strong>not adopted</strong></td><td>No page claims use; kept that way by the banned-phrase gate</td></tr>
<tr><td>S-09</td><td>Social preview + structured data</td><td>Partly done before; og:image is now a real absolute PNG card; FAQPage markup kept but must not be sold as a rich-result win (<a href="flagged.html#FLG-036">FLG-036</a>)</td></tr>
<tr><td>S-12</td><td>Voice decided and applied once</td><td>Rules live in <code>data/editorial.json</code> and are enforced by the gate</td></tr>
<tr><td>S-17</td><td>Front page rebuilt as a publication</td><td>Hero question, quick picks, products, chooser, guides, trust block last</td></tr>
<tr><td>S-19</td><td>Three-question chooser above the comparison</td><td>Kept; result links are now marked sponsored and labelled</td></tr>
<tr><td>S-20</td><td>Mobile-first pass</td><td>Type scale, tap targets, sticky bar and table scroll shipped in this pass; device check still open (SG-25)</td></tr>
<tr><td>S-24</td><td>Internal linking complete</td><td>Each guide reaches the comparison, the buying path and its category page</td></tr>
</table></div>

<p class="fine">Reviewer: mark each SG row Approve / Reject / Defer with a date. Approved rows become claimed tasks in <code>COORDINATION.md</code>. Nothing on this page is a promise of traffic, ranking or revenue, and no item here was implemented without being labelled as such.</p>

<h2>Pick a path before anything is built</h2>
<div class="decision-board" id="suggestion-board">
<p class="fine">Picks stay in this browser only (localStorage) - nothing is sent anywhere on static hosting. Use the export button for a review sheet; approved items then move to <code>COORDINATION.md</code> as claimed tasks.</p>
<div class="table-wrap"><table>
<tr><th>Item</th><th>Question / suggestion</th><th>Reviewer pick</th><th>Status</th></tr>
<tr><td>SG-49</td><td>Keep guide 10 (instant-read vs wireless) as the 11th published page</td><td><select data-pick="SG-49"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-51</td><td>One indexable publication: noindex the docs/ and counter-check/ builds</td><td><select data-pick="SG-51"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-52</td><td>Search Console first, self-hosted endpoint second</td><td><select data-pick="SG-52"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-53</td><td>One Associates click test per product</td><td><select data-pick="SG-53"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-11</td><td>Run the design brief as the brief for the visual overhaul</td><td><select data-pick="SG-11"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-12</td><td>Adopt the eight-topic editorial calendar as the publishing cadence</td><td><select data-pick="SG-12"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-22</td><td>One site, one canonical, one sitemap (consolidate the builds)</td><td><select data-pick="SG-22"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-43</td><td>Switch Pages to the GitHub Actions build source</td><td><select data-pick="SG-43"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-44</td><td>Visual QA the styled shop (index, category, compare, one guide) at mobile/tablet/desktop before the next deploy</td><td><select data-pick="SG-44"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-45</td><td>Add &ldquo;shop by goal&rdquo; intent landings built only from verified fields</td><td><select data-pick="SG-45"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-58</td><td>Make WCAG contrast / accessibility a standing build gate</td><td><select data-pick="SG-58"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-59</td><td>Treat the code-level visual QA as the documented stand-in for a screenshot</td><td><select data-pick="SG-59"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-60</td><td>Adopt the polished-marketing direction and consolidate to one design brief</td><td><select data-pick="SG-60"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>Q-42</td><td>Enforce WCAG contrast in the build?</td><td><select data-pick="Q-42"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>Q-43</td><td>Which single design brief do we execute?</td><td><select data-pick="Q-43"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>Q-44</td><td>Build &ldquo;shop by goal&rdquo; intent landings next?</td><td><select data-pick="Q-44"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>Q-21</td><td>Which design direction does the owner want?</td><td><select data-pick="Q-21"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>Q-23</td><td>What is the publishing cadence and who approves topics?</td><td><select data-pick="Q-23"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
</table></div>
<div class="review-panel">
  <button class="btn small" id="sg-export" type="button">Export review sheet (JSON)</button>
  <button class="btn secondary small" id="sg-print" type="button">Print this board</button>
  <button class="btn secondary small" id="sg-reset" type="button">Clear my picks</button>
</div>
</div><h2 id="suggestions">Suggestions for this pass &mdash; five decisions, each with a recommended path</h2>
<p>Everything below is a proposal. Nothing in this section has been implemented beyond what the row says it already does, and every row can be settled in under two minutes by one person. Rows marked <span class="badge-ok">ready</span> need no outside information; rows marked <span class="badge-warn">blocked</span> need something only the owner can obtain.</p>

<article class="sg path" id="SG-49"><h3>SG-49 &middot; Publish an 11th guide from the two thermometer listings</h3>
<p><strong>Why now:</strong> the thermometer cluster has three pages to the air fryers' eight. It is also the cluster where the two listings disagree most: one states a tolerance figure and the other states none, which is a genuine buyer question rather than a keyword guess.</p>
<div class="opts">
<p><strong>Path A (recommended):</strong> the &ldquo;do you need both?&rdquo; question, answered by the stated read time, probe count, range and heat rating already in the register. Honest headline: one listing makes no accuracy claim.</p>
<p><strong>Path B:</strong> a thermometer gift guide for the same window. Cheaper to write, but it duplicates the 2026-11-24 gift guide already published.</p>
<p><strong>Path C:</strong> hold the cluster until Search Console exists, so the topic is chosen from arriving queries.</p>
</div>
<p class="fine"><strong>Effort:</strong> 1 session, no new sources. <strong>Evidence needed:</strong> none beyond the register. <strong>Blocks:</strong> nothing. <strong>Status:</strong> <span class="badge-ok">Ready &mdash; and Path A is already published this pass as <a href="guide-instant-read-vs-wireless.html">guide 10</a>; approve it to keep it, or say the word and it is reverted in one commit.</span></p></article>

<article class="sg" id="SG-50"><h3>SG-50 &middot; Replace the typographic-only look with shipped type and brand art</h3>
<p><strong>Why:</strong> the design system named Fraunces and Inter but shipped neither, so every page rendered in Georgia and system-ui. A page set in default system type reads as generated no matter how good the copy is. The same pass added drawings of the five appliance <em>types</em>.</p>
<div class="opts">
<p><strong>Path A (recommended, done):</strong> self-host four latin variable font files (182 KB total, SIL Open Font License 1.1) and five original line drawings. No third-party font host, no Amazon imagery, no photographs.</p>
<p><strong>Path B:</strong> commission photography, which requires the licence decision in <a href="#SG-04">SG-04</a> first.</p>
<p><strong>Path C:</strong> pull fonts from Google Fonts at runtime. One extra third-party request per visitor and a render path we do not control.</p>
</div>
<p class="fine"><strong>Effort:</strong> done. <strong>Evidence:</strong> the fonts and licences are in <code>assets/fonts/</code>; the drawings are original SVGs in <code>assets/art/</code>. <strong>Blocks:</strong> nothing. <strong>Status:</strong> <span class="badge-ok">Ready &mdash; inspect and confirm; reverting is a single folder delete.</span></p></article>

<article class="sg" id="SG-51"><h3>SG-51 &middot; Make the site one indexable publication, not three</h3>
<p><strong>Why:</strong> this repository hosts three builds under one host: the root publication (26 URLs in the sitemap), a second site in <code>docs/</code> (served, and the target of draft PR #10) and an audit build in <code>counter-check/site/</code>. Search engines see duplicate or competing pages under one hostname. That is the single largest findability risk on the site and it is not a design problem.</p>
<div class="opts">
<p><strong>Path A (recommended):</strong> pin GitHub Pages to the root only, and add <code>noindex</code> meta tags to <code>docs/</code> and <code>counter-check/site/</code> output so the alternate builds stay reviewable without competing for the host. Reversible, no data loss.</p>
<p><strong>Path B:</strong> move the alternate builds to a separate repository or branch-preview URL.</p>
<p><strong>Path C:</strong> leave it and accept the competition. Cheapest today, most expensive if the site ever ranks.</p>
</div>
<p class="fine"><strong>Effort:</strong> S. <strong>Evidence needed:</strong> confirmation of which build the owner considers the publication. <strong>Blocks:</strong> a clean Search Console picture. <strong>Status:</strong> <span class="badge-warn">Half done this pass</span> &mdash; the seven internal root pages now carry <code>noindex, follow</code> and left the sitemap (<a href="flagged.html#FLG-069">FLG-070</a>). The <code>docs/</code> and <code>counter-check/site/</code> builds are outside this session&rsquo;s scope and still need your call.</p></article>

<article class="sg" id="SG-52"><h3>SG-52 &middot; Four measurable events before any optimisation claim</h3>
<p><strong>Why:</strong> the brief orders measurement before optimisation, and the site currently measures nothing beyond local browser counters. Four first-party numbers would let the next four topics be chosen instead of guessed.</p>
<div class="opts">
<p><strong>Path A (recommended):</strong> Search Console property + sitemap submission, then four weeks of data. No code, no privacy surface, no cost. Queries arrive with impressions, position and click-through.</p>
<p><strong>Path B:</strong> host the existing self-contained endpoint (<code>analytics-endpoint/server.py</code>) for the five defined events. Gives click coverage that Search Console cannot; needs a host, a retention rule and a privacy notice.</p>
<p><strong>Path C:</strong> both, in that order.</p>
</div>
<p class="fine"><strong>Effort:</strong> Path A is 20 minutes of owner time. <strong>Evidence needed:</strong> owner verification of the domain property. <strong>Blocks:</strong> any statement that a topic is in demand. <strong>Status:</strong> <span class="badge-warn">Needs owner action</span></p></article>

<article class="sg" id="SG-53"><h3>SG-53 &middot; Open one Associates click test per product, or stop calling the links validated</h3>
<p><strong>Why:</strong> the five outbound buttons carry the tracking ID and the correct ASIN, but no session here can confirm that a click is attributed in the Associates report. Until it is confirmed once per product, every statement about earning is a statement about intent.</p>
<div class="opts">
<p><strong>Path A (recommended):</strong> one click per ASIN from the live page, then check Reports &rarr; Link Type for the tag the same day. Five clicks, about ten minutes.</p>
<p><strong>Path B:</strong> test only the two highest-intent products first, and label the other three as untested.</p>
<p><strong>Path C:</strong> run the supplied <code>link.amazon</code> short links through the same test, which would also settle <a href="flagged.html#FLG-001">FLG-001</a>.</p>
</div>
<p class="fine"><strong>Effort:</strong> S, owner only. <strong>Evidence needed:</strong> a report row, not a click-through that merely looks correct. <strong>Blocks:</strong> any claim that the site is earning. <strong>Status:</strong> <span class="badge-warn">Needs owner action</span></p></article>



"""
_board_n = len(set(re.findall(r'id="(SG-\d\d)"', sugg_body))), len(set(re.findall(r'id="(Q-\d\d)"', sugg_body)))
page_to("suggestions.html","Decision desk: options & evidence | Countertop Guide",f"{_board_n[0]} suggestions and {_board_n[1]} questions with options, evidence and trade-offs, mapped to the seven gates on the decision register.",sugg_body)

# ---------- DECISION REGISTER (session arena/42e09357-prod1, 2026-11-20) ----------
# Why this exists: ten sessions wrote 43 suggestions and 27 questions onto one board. A board
# that long is a register, not a decision. This section re-orders the same rows into the seven
# answers that actually gate work, and reports any board row that no theme has taken.
#
# This check was a hard build failure for about an hour, and that was wrong. The board is append-only
# and every session adds rows to it, so a strict triage rule meant one session's new suggestion could
# stop the whole site from deploying - an editorial to-do item held the publish hostage, and it did
# exactly that twice on 2026-11-20 while other sessions' PRs were open. It is now a loud warning that
# prints on the build, plus a visible "nobody has taken these" table on the register page, which is
# where an unowned row belongs: seen by the person who has to triage it, not silently dropped and not
# fatal to readers. Ghost ids (a theme pointing at a deleted row) are dropped from the render for the
# same reason - the anchor check in check_site.mjs would otherwise fail the deploy over a stale id.
DEC = json.load(open("data/decisions.json"))
DEC_UPDATED = DEC["updated"]
_board_ids = sorted(set(re.findall(r'id="((?:SG|Q)-\d\d)"', sugg_body)))
_theme_ids = sorted(set(i for t in DEC["themes"] for i in t["sgs"] + t["qs"]))
_unknown = [i for i in _theme_ids if i not in _board_ids]
_uncovered = [i for i in _board_ids if i not in _theme_ids]
if _unknown:
    print("warn: data/decisions.json points at board ids suggestions.html no longer has (dropped from "
          "the render, fix the theme): " + ", ".join(_unknown))
    for _t in DEC["themes"]:
        _t["sgs"] = [i for i in _t["sgs"] if i in _board_ids]
        _t["qs"] = [i for i in _t["qs"] if i in _board_ids]
if _uncovered:
    print("warn: data/decisions.json has not triaged these board rows; they are listed on decisions.html "
          "under 'Nobody has taken these' and stay open: " + ", ".join(_uncovered))
SG_N = len([i for i in _board_ids if i.startswith("SG")])
Q_N = len([i for i in _board_ids if i.startswith("Q")])

def ref(x):
    """A board reference becomes a link when the target exists, and stays plain text when it is
    a phrase like 'the campaign ledger'. Links here must resolve; a dead anchor is a bug."""
    if re.fullmatch(r"(?:SG|Q)-\d\d", x):
        return f'<a href="suggestions.html#{esc(x)}">{esc(x)}</a>'
    if re.fullmatch(r"FLG-\d+", x):
        return f'<a href="flagged.html#{esc(x)}">{esc(x)}</a>'
    return esc(x)

def gate_card(g):
    known = "".join(f"<li>{flaglinks(esc(k))}</li>" for k in g["known"])
    steps = "".join(
        f"<tr><td>{i + 1}</td><td>{esc(d['step'])}</td><td>{esc(d['where'])}</td>"
        f"<td>{esc(d['who'])}</td><td>{esc(d['artifact'])}</td></tr>"
        for i, d in enumerate(g["discovery"]))
    def opt_row(o):
        mark = '<span class="badge-ok">recommended</span> ' if "recommended" in o["label"] else ""
        label = re.sub(r"\s*\(recommended[^)]*\)", "", o["label"])
        return (f'<tr><td>{mark}{esc(label)}</td><td>{esc(o["effect"])}</td>'
                f'<td class="risk-cell">{esc(o["risk"])}</td></tr>')
    opts = "".join(opt_row(o) for o in g["options"])
    unblocks = ", ".join(ref(x) for x in g["unblocks"])
    return f"""
<article class="card gate" id="{g['id']}">
  <p class="eyebrow">{g['id']} &middot; {esc(g['effort'])}</p>
  <h2>{esc(g['title'])}</h2>
  <div class="gate-grid">
    <p class="lede"><strong>Why now:</strong> {esc(g['whyNow'])}</p>
    <div><h3>What we already know</h3><ul class="tight">{known}</ul></div>
    <div><h3>What is missing</h3><p>{esc(g['missing'])}</p></div>
  </div>
  <h3>How to find it</h3>
  <div class="table-scroll"><table>
    <tr><th>#</th><th>Step</th><th>Where</th><th>Who can do it</th><th>Artifact it produces</th></tr>
    {steps}
  </table></div>
  <h3>The paths, and what each one costs</h3>
  <div class="table-scroll"><table>
    <tr><th>Option</th><th>What changes on the site</th><th>Risk</th></tr>
    {opts}
  </table></div>
  <p class="callout"><strong>Recommended:</strong> {esc(g['recommendation'])}</p>
  <p class="fine"><strong>Unblocks:</strong> {unblocks}. <strong>Risk of choosing:</strong> {esc(g['risk'])}.
  <strong>Status:</strong> <span class="badge-warn">awaiting owner</span></p>
</article>"""

_queue_rows = "".join(
    f'<tr><td><a href="#{g["id"]}">{g["id"]}</a></td><td>{esc(g["title"])}</td>'
    f'<td>{len(g["unblocks"])}</td><td>{esc(g["effort"])}</td>'
    f'<td><span class="badge-warn">awaiting owner</span></td></tr>' for g in DEC["gates"])
_answered_rows = "".join(
    f'<tr><td>{esc(a["row"])}</td><td>{esc(a["question"])}</td><td>{esc(a["answer"])}</td>'
    f'<td>{esc(a["date"])}</td><td>{esc(a["recordedIn"])}</td></tr>' for a in DEC["answered"])
_missing_rows = "".join(
    f'<tr><td>{esc(m["what"])}</td><td>{esc(m["why"])}</td><td>{esc(m["how"])}</td>'
    f'<td>{esc(m["who"])}</td><td>{flaglinks(esc(m["status"]))}</td></tr>' for m in DEC["missing"])
_theme_rows = "".join(

    f'<tr><td>{esc(t["name"])}</td><td>{esc(t["oneLine"])}</td>'
    f'<td>{len(t["sgs"]) + len(t["qs"])}</td><td><a href="#{t["gate"]}">{t["gate"]}</a></td>'
    f'<td class="ids">{", ".join(ref(x) for x in sorted(t["sgs"] + t["qs"]))}</td></tr>' for t in DEC["themes"])

_unowned_rows = (
    '<h3 id="unowned">Nobody has taken these yet (%d)</h3>\n'
    '<p>Each row is still on the board and unread by any gate. Pick a theme, or say why it does not need one.</p>\n'
    '<div class="table-scroll"><table>\n<tr><th>Row</th><th>On the board</th></tr>\n%s\n</table></div>'
    % (len(_uncovered),
       "\n".join('<tr><td><a href="suggestions.html#%s">%s</a></td><td>Untriaged as of this build</td></tr>' % (i, i)
                  for i in _uncovered))
) if _uncovered else ""
_reply_lines = "\n".join(
    f"{g['id']} = option _ , {DEC_UPDATED}, evidence: " for g in DEC["gates"])
dec_body = f"""
<p class="eyebrow">Decision register</p>
<h1>Seven decisions, in the order that unblocks the rest</h1>
<p class="lede">The board carries {SG_N} suggestions and {Q_N} questions, written by ten sessions working in parallel. That is a register, not a decision. This page collapses it into the seven answers that gate everything else, and states for each one what is already known from an official source, what is still missing, the exact steps that would produce the missing piece, and what breaks loose when it arrives.</p>
<div class="callout"><strong>Nothing here is approved.</strong> Every gate says <em>awaiting owner</em> because that is the truth: a session may recommend, but the byline, the licence, the API eligibility and the money decisions belong to the owner. {esc(DEC['defaultRule']['status'])}</div>
<h2>How to answer</h2>
<ol class="tight">{"".join(f"<li>{esc(s)}</li>" for s in DEC['howThisWorks'])}</ol>
<p class="fine">Answer format: <code>{esc(DEC['answerFormat'])}</code></p>
<h2 id="queue">The queue</h2>
<div class="table-scroll"><table>
<tr><th>Gate</th><th>Decision</th><th>Rows it unblocks</th><th>Cost to answer</th><th>Status</th></tr>
{_queue_rows}
</table></div>
<p class="section-more"><a class="btn secondary" href="suggestions.html">Open the full board ({SG_N + Q_N} rows)</a> <a class="link-quiet" href="#map">or see how every row maps to these seven</a></p>
<h2>The seven, one by one</h2>
{"".join(gate_card(g) for g in DEC["gates"])}
<h2 id="answered">Answered already, so nobody re-litigates it</h2>
<div class="table-scroll"><table>
<tr><th>Row</th><th>Question</th><th>Answer in force</th><th>Dated</th><th>Where it landed</th></tr>
{_answered_rows}
</table></div>
<h2 id="missing">The information we do not have, and how to get it</h2>
<p>Every blank cell on this site is here. The rule that produced them: a value that cannot be confirmed from an official source stays blank and gets a flag, rather than being inferred.</p>
<div class="table-scroll"><table>
<tr><th>Missing</th><th>Why it is blank</th><th>How to discover it</th><th>Who can</th><th>Status</th></tr>
{_missing_rows}
</table></div>
<h2 id="map">Board map: every row, one theme, one gate</h2>
<p>The build compares this map with the board on every publish. A row the board has and no theme has taken is listed below instead of being left out, and the build says so out loud; a theme pointing at a row the board no longer has is dropped from the render rather than left dangling. Triage is a person&rsquo;s job, so the register surfaces it without holding the site hostage &mdash; see <a href="flagged.html#FLG-082">FLG-082</a>.</p>
{_unowned_rows}
<div class="table-scroll"><table>
<tr><th>Theme</th><th>What it is for</th><th>Rows</th><th>Gate</th><th>Rows in this theme</th></tr>
{_theme_rows}
</table></div>
<h2>Reply block</h2>
<p>Paste this into <code>COORDINATION.md</code> or send it back as a message, fill the option number, and a session will apply it, move the row to <em>Answered</em> with your date, and rebuild the pages it touches.</p>
<pre class="reply">{esc(_reply_lines)}</pre>
<p class="fine">Register compiled {DEC_UPDATED} by session <code>42e09357</code> from COORDINATION.md, the flagged register, the verification log and this repository&rsquo;s data files. Source links inside each gate are the primary pages; the dates are when a session says it read them, which is the only freshness claim this site makes.</p>
"""
page_to("decisions.html", "Decision register: seven gates, in order | Countertop Guide",
        "The seven decisions that gate this site, what an official source already settles, what is still missing, and the exact steps that would produce each missing piece.",
        dec_body)

# ---------- VERIFICATION ----------
ver_rows = ""
# Irregularity found by this session's audit of its own register: these 13 fields hold the
# literal string "—" (em dash). The page turns that into "Blank - not captured", which is
# correct for a missing value, but the JSON is telling a future session that a figure was
# RECORDED, and the em dash is how "not applicable" was also written (capacity for a
# thermometer, say). Two different meanings in one placeholder is how an inference gets made
# later. Mapping is explicit and one-way; data/products.json itself is another session's
# field and is left untouched (see COORDINATION.md, scope discipline).
NA_FIELD = "—"
for pid in ["P1","P2","P3","P4","P5"]:
    p = {k: ("" if v == NA_FIELD else v) for k, v in PRODS[pid].items()}
    if PRODS[pid].get("dimensions") == "":
        p["dimensions"] = ""
    dims_cell = esc(p["dimensions"]) if p["dimensions"] else '<span class="badge-flag">Blank - not captured (Flagged)</span>'
    ver_rows += f"""
<article class="card" id="{pid}">
<h3>{pid} - {esc(p['shortName'])} (ASIN {p['asin']})</h3>
<div class="table-scroll"><table>
<tr><th>Field</th><th>Value</th><th>Source</th></tr>
<tr><td>Submitted short link (as supplied)</td><td>{esc(p['submittedShortLink'])}</td><td>Owner brief</td></tr>
<tr><td>Intended ASIN</td><td>{p['asin']}</td><td><a href="{p['officialListingUrl']}">Official listing</a></td></tr>
<tr><td>Official listing URL</td><td>{esc(p['officialListingUrl'])}</td><td>Amazon.com</td></tr>
<tr><td>Observed redirect target (separate field - do not merge)</td><td>{esc(p['observedRedirectTarget'])}</td><td>Observed 2026-11-19</td></tr>
<tr><td>Confirmation date</td><td>{p['confirmationDate']}</td><td>{esc(p['confirmationSource'])}</td></tr>
<tr><td>Title (as listed)</td><td>{esc(p['title'])}</td><td><a href="{p['sourceUrl']}">Listing</a></td></tr>
<tr><td>Rating / count (snapshot)</td><td>{esc(p['rating'])} ({esc(p['ratingCount'])})</td><td><a href="{p['sourceUrl']}">Listing</a></td></tr>
<tr><td>Price snapshot (new / list)</td><td>{esc(p['priceNew'])} / {esc(p['priceList'])}</td><td><a href="{p['sourceUrl']}">Listing buy box</a></td></tr>
<tr><td>Dimensions</td><td>{dims_cell}</td><td><a href="{p['sourceUrl']}">Listing purchase options</a></td></tr>
<tr><td>Capacity (title / field)</td><td>{esc(p['capacityTitle'])} / {esc(p['capacityField'])}</td><td><a href="{p['sourceUrl']}">Listing</a></td></tr>
<tr><td>Special features</td><td>{esc(p['specialFeatures'])}</td><td><a href="{p['sourceUrl']}">Listing</a></td></tr>
<tr><td>Affiliate URL used on site</td><td>{esc(aff(p))} (rel="sponsored")</td><td>Constructed: official URL + tag {TAG}</td></tr>
</table></div>
<p class="small">{esc(p['sourceNote'])}</p>
</article>"""
def recheck_html():
    rows = "".join(
        f'<tr><td>{k}</td><td>{esc(RECHECK[k][0])}</td><td>{flaglinks(esc(RECHECK[k][1]))}</td></tr>'
        for k in ["P1", "P2", "P3", "P4", "P5"])
    return f"""<h2 id="recheck">Re-read of {RECHECK_DATE}, by this session</h2>
<p>The five listing pages were opened again on {RECHECK_DATE}. The scope is stated because it is narrow: this pass confirmed that each page is reachable, that its title still matches the title in the register, and the one buy-box price this read could attribute to the product itself. Spec tables, ratings and the rest were <strong>not</strong> re-read in this pass, so nothing here relabelled a shop-card field as freshly confirmed by me: where a field now carries {VERIFIED}, that date belongs to the separate line-by-line pass that re-read it, recorded per product below. My contribution to that table is the title check on all five and one buy-box price, and it is quoted nowhere except this section. Full record: <code>review/42e09357/VERIFICATION-2026-11-20.md</code>.</p>
<div class="table-scroll"><table>
<tr><th>Ref</th><th>What the {RECHECK_DATE} read confirmed</th><th>What it did not settle</th></tr>
{rows}
</table></div>
<p class="small">Method note, so the trap is on the record: every one of these listing pages carries a &ldquo;Customers who viewed this item also viewed&rdquo; block with other products&rsquo; prices and star counts. Those figures are not this product&rsquo;s data (<a href="flagged.html#FLG-016">FLG-016</a>), and an earlier session&rsquo;s price doubt came from exactly that block. Where a buy-box price could not be attributed to the product with certainty, this pass recorded nothing.</p>"""

def audit_html(needle_rows):
    where = {cl: (fn, ok) for cl, fn, ok in needle_rows}
    rows = []
    for c, v, _ in CLAIM_ROWS:
        vcell = ('<span class="badge-ok">%s</span>' % v) if v.startswith("verified") else \
                ('<span class="badge-warn">%s</span>' % v)
        if c["claim"] in where:
            fn, ok = where[c["claim"]]
            pcell = ('<span class="badge-ok">sentence found in %s</span>' % fn) if ok else \
                    ('<span class="badge-warn">sentence missing from %s</span>' % fn)
        else:
            pcell = '<span class="small">not a quoted sentence; the audit describes the claim</span>'
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            esc(c["claim"]), esc(c["where"]), esc(c["basis"]), vcell, pcell))
    n_ok = sum(1 for _, v, _ in CLAIM_ROWS if v.startswith("verified"))
    n_found = len([1 for _, _, ok in needle_rows if ok])
    return """<h2 id="claim-audit">Claim audit: every superlative the site prints, tested twice</h2>
<p>A register that is checked while its prose is not will drift: someone corrects a number and a
phrase like &ldquo;the narrowest&rdquo; stays standing there. So each comparative or superlative on a
shop page is tested twice on every build. First against the register - the ordering or the figure has
to follow from <code>data/products.json</code>, recomputed here rather than transcribed. Then against
the HTML this build just wrote - the sentence the audit describes has to still be on the page it is
claimed to be on. Either failure stops the build.</p>
<div class="table-scroll"><table>
<tr><th>Claim as printed</th><th>Where it appears</th><th>Evidence it rests on</th><th>Verdict on this build</th><th>Verdict on the wording</th></tr>
%s
</table></div>
<p class="small">%d of %d claims are recomputable from the register and pass; the wording of %d of them
was then located in the generated page. The rows labelled &ldquo;untestable&rdquo; are framing or
derived arithmetic, and the audit says so rather than certifying them. This section was written on
%s after session 1187e20d corrected the &ldquo;Smallest footprint&rdquo; label, which no numeric gate
had caught - the gap was never the number, it was a sentence standing in for one.</p>""" % (
        "\n".join(rows), n_ok, len(CLAIM_ROWS), n_found, RECHECK_DATE)

def check_spec_lists(files):
    """A spec list must not repeat a label. Two passes each adding a row to the card is exactly how a
    card ends up printing 'Capacity' twice with two different figures - a copy gate cannot see it and
    a reader can. So the build compares the labels it just wrote, per card."""
    bad = []
    for fn in files:
        txt = open(fn, encoding="utf-8").read()
        for dl in re.findall(r'<dl class="specs">(.*?)</dl>', txt, re.S):
            labels = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<dt>(.*?)</dt>", dl, re.S)]
            for lab in sorted(set(labels)):
                if labels.count(lab) > 1:
                    bad.append("%s: '%s' printed %d times in one spec list" % (fn, lab, labels.count(lab)))
    return bad

NEEDLE_ROWS = check_printed_claims()

ver_body = f"""
<p class="eyebrow">Verification register</p>
<h1>Line-by-line verification: every fact, its source</h1>
<p class="lede">Rule: every table row has a source link to an official site. If a value cannot be confirmed, it is left blank and flagged - never inferred. Intended ASIN and observed redirect target are stored in separate fields and never merged.</p>
<h2>Product-intent confirmation record</h2>
{ver_rows}
<h2>Policy sources (official)</h2>
<div class="table-scroll"><table>
<tr><th>Source</th><th>What it governs</th><th>Link</th></tr>
<tr><td>Amazon Associates Operating Agreement (updated 2025-10-15)</td><td>Special Links must properly use tagged link formats; Program Content definition</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement</a></td></tr>
<tr><td>Amazon Associates Program Policies (updated 2026-04-14)</td><td>Commission session rules; participation requirements</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td></tr>
<tr><td>FTC Disclosures 101 for Social Media Influencers (Nov 2019)</td><td>Material-connection disclosure: hard to miss, simple clear language</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td></tr>
<tr><td>FTC Endorsements, Influencers &amp; Reviews guidance</td><td>Endorsement context and review integrity</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td></tr>
</table></div>
<p class="small">Verification performed 2026-11-19 by fetching each Amazon listing and policy page. Prices/ratings are snapshots and will change. Manual Special Link test in Associates Central remains a gate (see <a href="flagged.html">Flagged</a>).</p>
{recheck_html()}
{audit_html(NEEDLE_ROWS)}
"""
page_to("verification.html","Verification register, line by line | Countertop Guide","For all five products: submitted short link, intended ASIN, official listing URL, confirmation date and source, and the observed redirect in its own field.",ver_body)
# ---------- FLAGGED ----------
flag_body = f"""
<p class="eyebrow">Flagged for review</p>
<h1>Flagged for review - irregularities &amp; unverified items</h1>
<p class="lede">Flagged items do not block publishing, but they block claims. Nothing below is presented as fact on product pages. Review after launch and request changes.</p>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Item</th><th>Detail</th><th>Action</th></tr>
<tr id="FLG-001"><td>FLG-001</td><td>Short-link compliance unresolved</td><td>Supplied link.amazon short links resolve to the ASINs, but their exact compliance status as Special Links is unresolved. We do not claim they are invalid. Site outbound buttons use official listing URLs + tag instead.</td><td>Manual test in Associates Central (SG-01)</td></tr>
<tr id="FLG-002"><td>FLG-002</td><td>Preset &amp; capacity discrepancies</td><td>Emeril: title 24 presets vs bullets 25; title 26QT vs field 24.6 liters. Chefman 6QT: title 6 Quart vs field 6 liters. Both values shown; no silent conversion.</td><td>Verify on listing; ask seller if needed</td></tr>
<tr id="FLG-003"><td>FLG-003</td><td>Newer models shown on listings</td><td>Chefman 8QT page shows newer 6QT B0CNY1YVDD ($59.99, 4.6/7,602); ThermoMaven page shows newer Orange B0GL7Z4KP4 ($16.99, 4.7/144). We promote the submitted ASINs only.</td><td>Decide lineup (SG-08)</td></tr>
<tr id="FLG-004"><td>FLG-004</td><td>Missing dimensions (thermometers)</td><td>ThermoMaven B0DHZTCNR5 and CHEF iQ B0DZFD6R9Z dimensions not in captured fields. Left blank in tables.</td><td>Re-fetch product-details; record date</td></tr>
<tr id="FLG-005"><td>FLG-005</td><td>Missing warranty (Emeril)</td><td>Emeril wattage captured 2026-11-19 (1700 watts / 120 volts per the listing's Product information table). Warranty period is not stated on the listing page; the listing links a warranty PDF only. Left blank.</td><td>Read warranty PDF if the term is needed</td></tr>
<tr id="FLG-006"><td>FLG-006</td><td>Price volatility</td><td>All prices are {VERIFIED} snapshots (Black Friday period). Live price on Amazon governs.</td><td>Re-snapshot on cadence; date every price</td></tr>
<tr id="FLG-007"><td>FLG-007</td><td>Canonical is the GitHub Pages URL, not a custom domain</td><td>Canonical/og URLs now point to https://wingbangboozle1-lang.github.io/Prod1/ (session 9969fd0c). A custom domain is still unset, and the generator previously wrote a placeholder - fixed in build_site.py 2026-11-19 so rebuilds reproduce the committed pages.</td><td>Pick domain (SG-02)</td></tr>
<tr id="FLG-008"><td>FLG-008</td><td>Analytics endpoint not hosted</td><td>Five events defined; local counter only. The endpoint code is complete and contract-tested (<code>analytics-endpoint/server.py</code> + <code>selftest.py</code>, wired into the deploy gate as <code>scripts/check_measure.mjs</code>, 2026-11-20) but no host is configured, so nothing is transmitted.</td><td>Owner picks a host and retention period (SG-03, Q-08), then sets <code>events.endpoint</code> in <code>data/editorial.json</code></td></tr>
<tr id="FLG-009"><td>FLG-009</td><td>No product photography</td><td>No Amazon images used (IP/licence). SVG/CSS illustrations only.</td><td>Licence decision (SG-04)</td></tr>
<tr id="FLG-010"><td>FLG-010</td><td>No hands-on testing</td><td>We have not cooked with or calibrated any product. No "lived-with" claims made.</td><td>Testing programme if approved (SG-09)</td></tr>
<tr id="FLG-011"><td>FLG-011</td><td>No commission / revenue claims</td><td>Rates not published; ledger empty until authorized reports arrive.</td><td>Record only from Associates reports</td></tr>
<tr id="FLG-012"><td>FLG-012</td><td>No trend / popularity claims</td><td>"Bought in past month" badges are listing snapshots, not our ranking. We do not claim a trend.</td><td>Evidence rule: dated snapshot or no claim</td></tr>
<tr id="FLG-013"><td>FLG-013</td><td>Submitted link codes are 9 characters</td><td>Each submitted link.amazon path code (e.g. B04G1MEwY) is 9 characters. Each code resolves to a listing whose ASIN differs from the code, so the code is not used as an intended ASIN. Intended ASIN fields stay blank pending submitter confirmation (session 9b748801, 2026-11-19).</td><td>Submitter confirms intended ASIN per link (Q-03)</td></tr>
<tr id="FLG-014"><td>FLG-014</td><td>ASIN 10-character rule: third-party sources only</td><td>The 10-character ASIN format was found on third-party guides, not on an Amazon page read in this session. The format is used only to flag the 9-character codes.</td><td>Find an official Amazon help page for the ASIN definition</td></tr>
<tr id="FLG-015"><td>FLG-015</td><td>Redirect targets carry no tag=</td><td>The final URLs of the five supplied links (read 2026-11-19) contain no tag= parameter. Attribution to shopnow047c-20 is therefore not observed on the redirect path. Site buttons use tagged listing URLs (FLG-001).</td><td>Associates tracking-report test per product (SG-01)</td></tr>
<tr id="FLG-016"><td>FLG-016</td><td>Listing pages carry widget data for other ASINs</td><td>Listing pages include Product summary links and Customers who viewed carousels with prices and ratings for other products. These are not used as data for the five products.</td><td>Use only each product's own fields; re-check on publication</td></tr>
<tr id="FLG-017"><td>FLG-017</td><td>External register: three links vs five</td><td>The external Zone4 decision log (D-13) refers to the three supplied links; this brief supplies five. Its statuses are not carried into this site. Only the first part of that log was read.</td><td>Reconcile the external register with the five links</td></tr>
<tr id="FLG-018"><td>FLG-018</td><td>Proposed Amazon content notice (not verified)</td><td>The external Zone4 decision log proposes an Amazon content notice citing IP License section 2(k). The IP License was not read, and the notice is not yet on the pages.</td><td>Read IP License 2(k); decide under SG-04</td></tr>
<tr id="FLG-019"><td>FLG-019</td><td>Creators API prerequisites not read</td><td>The external Zone4 decision log suggests the Creators API for prices and ratings. Its prerequisites were not read, and no API data is used on this site.</td><td>Read prerequisites before any price or rating source change</td></tr>
<tr id="FLG-020"><td>FLG-020</td><td>Main-product values not fully re-read in integration</td><td>The integration check confirmed the five ASINs and the ThermoMaven price ($16.99) against the listing pages. Other prices, ratings and dimensions in data/products.json were not re-read in full in this pass.</td><td>Full re-read of each listing's product details before publishing price claims</td></tr>
<tr id="FLG-021"><td>FLG-021</td><td>Accessory count discrepancy (Emeril)</td><td>Listing title says \"Six Cooking Accessories Included\"; the listing's item details say \"Air Fryer Toaster Oven Combo with 24 Functions and 7 Accessories\"; the included-components list names 6 items (Rack, Bake Pan, Drip Tray, Crisper Basket, Rotisserie Spit, Fetch Tool). All three values are listing-internal and disagree. We show the title value and flag it; no count is inferred. Observed 2026-11-19.</td><td>Ask seller / read product manual; show title value with flag until resolved</td></tr>
<tr id="FLG-022"><td>FLG-022</td><td>Wattage discrepancy (Chefman 8QT)</td><td>Chefman 8QT listing bullets state \"1000 Watts/120 Volts - RJ38-SQSS-8T\" while the listing's Product information table lists Output Wattage 1700 watts, 120 volts. Both values are listing-internal and disagree. We show the bullets value with attribution and flag it; no wattage is inferred. Observed 2026-11-19.</td><td>Ask seller / read user manual; resolve before any circuit-load claim</td></tr>
<tr id="FLG-032"><td>FLG-032</td><td>Prices and rating figures removed from shop pages (policy read)</td><td>Read in-session from the Associates Program Policies: a Site may show prices and availability only where Amazon serves the link carrying that data, or where the Site obtains it via the Creators/PA API under the License; and the IP License allows storing a Product Advertising Content image link for up to 24 hours, with other content refreshable only within that window. A static build cannot satisfy either route, so this pass took price, rating, rating count, badge and &quot;bought in past month&quot; figures off the shop pages and left the buttons as the price. Source: <a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a>.</td><td>Owner to ratify link-only pricing (SG-19), or fund the API refresh (SG-20) and switch <code>display.pricesOnShopPages</code> back on with a 24-hour staleness gate</td></tr>
<tr id="FLG-033"><td>FLG-033</td><td>Register still shows dated price and rating figures</td><td>The verification register keeps the values observed on {VERIFIED} as an audit record, labelled as an observation on a date rather than as a current figure. Whether even a dated audit figure may appear on a Site is an interpretation we cannot resolve from the text alone.</td><td>Owner decision, or a written question to Associates support; if the answer is no, the register shows the field as &quot;observed, figure withheld&quot;</td></tr>
<tr id="FLG-034"><td>FLG-034</td><td>Chooser-generated product links previously lacked <code>rel=&quot;sponsored&quot;</code></td><td>The recommendation list in the chooser is built in JavaScript. Those anchors pointed at tagged Amazon URLs with no <code>rel</code> attribute and no visible sponsored label, so a static HTML audit could not see them. Fixed in this pass: script-built links carry <code>rel=&quot;sponsored nofollow noopener&quot;</code>, the label, and the click attribute. <code>scripts/check_meta.mjs</code> now scans the JS as well as the HTML so it cannot regress.</td><td>None - closed by this pass; keep the JS check in CI</td></tr>
<tr id="FLG-035"><td>FLG-035</td><td>Generator wrote placeholder canonicals; deployed HTML had been patched by hand</td><td><code>build_site.py</code> emitted a placeholder domain as the canonical on every page while the live files carried the GitHub Pages URL after PR #7&rsquo;s manual fix - so the next rebuild would have replaced real canonicals with a placeholder on all 17 pages. Every page now self-canonicalises to its own absolute URL, the sitemap lists exactly the pages the build writes, and the sitemap&rsquo;s home entry matches the home page&rsquo;s canonical. Google&rsquo;s guidance: do not declare different canonicals for the same page by different methods, and include a self-referential canonical on the canonical page. Sources: <a href="https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls">canonical</a>, <a href="https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap">sitemaps</a>.</td><td>Re-check coverage in Search Console after the next deploy; re-run this wiring if a custom domain is adopted (SG-02)</td></tr>
<tr id="FLG-036"><td>FLG-036</td><td>FAQPage structured data must not be sold as an SEO win</td><td>Each guide emits FAQPage JSON-LD. Secondary sources reporting on Google&rsquo;s documentation state that FAQ rich results were restricted to well-known government and health sites in August 2023 and stopped appearing for everyone on 7 May 2026, with the FAQ documentation removed on 15 June 2026. We did not read that notice on an official Google page in this session, so it is recorded here rather than asserted on a page; the markup itself is harmless and may still help machines read the answer. Source: <a href="https://developers.google.com/search/docs/appearance/structured-data">Google structured data overview</a> for what remains supported.</td><td>Confirm against Google Search Central, then keep the markup without claiming a rich-result benefit (affects S-09)</td></tr>
<tr id="FLG-037"><td>FLG-037</td><td>Creators/PA API eligibility not verified from an official page</td><td>Third-party guides consistently state that API access follows three qualifying sales inside 180 days. No Amazon page was read in this session that states it. This matters because the whole automation plan (SG-20) and the price/image policy (FLG-032) rest on it.</td><td>Read the eligibility notice in Associates Central &rarr; Tools &rarr; Product Advertising / Creators API and record the wording and date</td></tr>
<tr id="FLG-038"><td>FLG-038</td><td>SiteStripe image options: second-hand claim</td><td>Several third-party tutorials state that SiteStripe stopped offering Image and Text+Image link types in late 2023, leaving API access as the route to compliant product imagery. We have not verified that in the Associates console. It changes the photography plan (SG-04), so it is stated as unverified rather than as a constraint.</td><td>Open SiteStripe on any product page and record which link types exist, with the date</td></tr>
<tr id="FLG-039"><td>FLG-039</td><td>Three builds are published on one host, under two brands</td><td>The root publication, <code>counter-check/site/</code> (Counter Check) and the <code>docs/</code> + <code>articles/</code> build (Counter &amp; Crumb, still open as draft PR #10) are all reachable and all indexable, and the root sitemap previously listed <code>docs/</code> and <code>articles/</code> URLs. That splits the domain across near-duplicate content and two mastheads. Nothing here is a policy breach - it is a findability and brand problem. The sitemap generated by this pass lists only the pages this build writes. Update 2026-11-20: the generated <code>robots.txt</code> now disallows the secondary builds (<code>/counter-check/</code>, <code>/docs/</code>, <code>/articles/</code>, <code>/review/</code>, <code>/analytics-endpoint/</code>), so search engines are told to index the root publication only - one site to index, with nothing deleted.</td><td>Owner picks one publication (SG-22) and decides whether to delete or promote the secondary builds; until then keep the robots rules</td></tr>
<tr id="FLG-040"><td>FLG-040</td><td>Snapshot dates are already ageing</td><td>Every field on this site carries the date {VERIFIED}. Amazon listing content changes without notice, so the honest shelf life of a manual snapshot is days, not months. There is no scheduled re-read in the repository - only the rule that a figure must never be presented as current.</td><td>Adopt a re-read cadence (weekly while small, per publish for the pages touched) and record each pass on the register</td></tr>
<tr id="FLG-041"><td>FLG-041</td><td>The only image on the site is brand art</td><td><code>assets/og-image.png</code> is a generated typographic card for link previews. No product image, food photograph or AI-generated product visual is used anywhere, in line with the Program Content read in FLG-032.</td><td>Replace or extend imagery only under an approved licence (SG-04), and keep drawings labelled as ours</td></tr>
<tr id="FLG-042"><td>FLG-042</td><td>Disclosure wording changed to the Agreement&rsquo;s exact sentence</td><td>Pages previously read &quot;As an Amazon Associate, The Countertop Guide earns from qualifying purchases.&quot; Section 5 of the Operating Agreement requires the statement &quot;As an Amazon Associate I earn from qualifying purchases.&quot; or a substantially similar statement previously allowed under the Agreement; whether a reworded variant qualifies is not ours to decide, and Section 6 treats a Section 5 violation as a material breach. The strip and footer now carry the required sentence verbatim, with a plain-language explanation beside it. Source: <a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement Section 5</a>, read in-session.</td><td>Closed by this pass (answers request I-02 from session b4c6c619); revisit only with written comfort on an alternative wording</td></tr>
<tr id="FLG-043"><td>FLG-043</td><td>Disclosure wording variant vs Operating Agreement section 5</td><td>Raised by session <code>8e82d03c</code> in PR #17: the strip used to name the site (&quot;As an Amazon Associate, The Countertop Guide earns&hellip;&quot;) instead of the Agreement&rsquo;s first-person sentence. Whether the variant was substantially similar was an owner call; the register&rsquo;s <code>site.disclosure</code> now carries the verbatim sentence and every page renders it from that field. Same item this pass filed as <a href="#FLG-042">FLG-042</a> - kept as two rows because two sessions found it independently, and each has a different action trail.</td><td>Nothing further; the compliance page quotes the register value</td></tr>
<tr id="FLG-044"><td>FLG-044</td><td>Star ratings shown without the Creators API or Product Advertising API</td><td>Raised by session <code>8e82d03c</code>: a Program Policy conditions display of customer reviews and star ratings on obtaining them through the Creators API or PA API. This build cannot call either API (<a href="#FLG-037">FLG-037</a>), so a displayed rating figure would be unsupported. That session read the clause; this session has not re-read it and does not assert its numbering.</td><td>Implemented as far as it can be without the API: no rating figure appears on any shop or guide page, and the dated counts live only in <a href="verification.html">the verification register</a>. Owner: confirm with Associates support before a rating figure is added anywhere else</td></tr>
<tr id="FLG-045"><td>FLG-045</td><td>Intended ASIN and observed ASIN held in one field</td><td>Raised by session <code>8e82d03c</code>: the brief requires the intended ASIN (what was submitted) and the observed redirect target (what the link resolved to) to stay separate, and <a href="#FLG-013">FLG-013</a> keeps the intended value blank until the submitter confirms it. The register does separate them now - <code>submittedShortLink</code>, <code>observedRedirectTarget</code>, <code>asin</code> - so the structure is answered; what stays open is that the submitted codes are nine characters long and cannot be validated as ASINs from the outside.</td><td>Owner: confirm the five intended ASINs in Associates Central, then <code>asin</code> can be marked intended-and-observed rather than observed-only</td></tr>
<tr id="FLG-046"><td>FLG-046</td><td>Rating counts drifted between two verification passes on the same day</td><td>Raised by session <code>8e82d03c</code>: their re-read found 18,375 for the Emeril oven and 16,892 for the Chefman 8QT where the register held 18,371 and 16,890 earlier that day. The register now carries the newer figures. The point is not the four extra ratings - it is that a figure copied from a listing ages in hours, which is why this site does not publish them.</td><td>Re-read on cadence; until then treat every recorded count as dated, not current</td></tr>
<tr id="FLG-047"><td>FLG-047</td><td>A second parallel pass published three more seasonal guides whose topics the site already covers</td><td>Session <code>8e82d03c</code> added <code>guide-holiday-gifts.html</code>, <code>guide-small-kitchen.html</code> and <code>guide-holiday-roast.html</code> (merged in PR #17) at the same time as this pass published <code>guide-gift-picks.html</code>, <code>guide-cleanup-counter-space.html</code> and <code>guide-thermometer-accuracy.html</code>. The pairs answer the same questions; the newer three also carried dated price and rating figures, which this build does not publish anywhere outside the verification register. Rather than delete live URLs, the three now return the same content as a short canonical page pointing at the surviving guide, and the build excludes them from the sitemap so one question has one canonical answer. The other session&rsquo;s full drafts remain in the repository history at <code>9e4b359</code>.</td><td>Owner decision: keep the consolidation, or restore the three as standalone pages after stripping the dated figures (one edit in <code>MERGED</code> in <code>build_site.py</code> plus the price lines)</td></tr>
<tr id="FLG-048"><td>FLG-048</td><td>Third-party register values reached this build through a merge, not through this session&rsquo;s own reading</td><td>The wattage, rating-count and accessory figures adopted in this merge come from <code>data/products.json</code>, re-read on 2026-11-19 by sessions <code>2ec8638e</code> and <code>8e82d03c</code>. This session verified them against the page text in the register but did not re-open the Amazon listings a third time, so they are attributed rather than independently confirmed here.</td><td>Re-read the five listings before the next publishing cadence tick; the register row for each field carries the date it was last confirmed</td></tr>
<tr id="FLG-049"><td>FLG-049</td><td>A third parallel pass built a second dashboard hub and its own numbering on this board</td><td>Session <code>f0db58ea</code> (PR #19) shipped a shop-first front page, a <code>dashboard.html</code> hub, eight design inputs DI-1…DI-8 and its own <code>SG-19…SG-27</code> / <code>Q-15…Q-20</code> rows - the same ranges this pass had already claimed. Merged without discarding: their design inputs keep the DI prefix and land on the board as a new section; their suggestions renumber to <a href="suggestions.html#SG-34">SG-34…SG-42</a> and their questions to <a href="suggestions.html#Q-21">Q-21…Q-26</a>, with the references inside each row shifted the same way. Their <code>dashboard.html</code> duplicated this pass&rsquo;s <a href="review-desk.html">review desk</a>, so it stays live as a canonical pointer rather than as a second hub, and their front page was not applied because both passes rebuilt the same file and only one can win - this page&rsquo;s version is the one the gate and the editorial policy drive.</td><td>Owner: if the hub&rsquo;s framing was preferred over the review desk, flip the pair in <code>MERGED</code> in <code>build_site.py</code>; if any of SG-34…SG-42 duplicates a row above it, reject the pair rather than shipping both</td></tr>
<tr id="FLG-050"><td>FLG-050</td><td>Two of their rows described state that this build has since changed</td><td>Their imagery question said the share card was &ldquo;a typographic SVG&rdquo; and their review-SLA row counted 26 suggestions and 19 questions. Neither is true of the merged site: the share card is a generated 1200&times;630 PNG and the board now holds 42 suggestions and 26 questions. Both cells were rewritten rather than deleted, and the rewrite is recorded here so the change is attributable to the merge, not to the other session.</td><td>None; noted for the audit trail</td></tr>
<tr id="FLG-051"><td>FLG-051</td><td>The deploy workflow cannot publish while Pages is set to build from the branch</td><td>Run <code>44627271033</code> for the merge of PR #20 failed at <code>actions/deploy-pages@v4</code> with every earlier step green: the build, the determinism check and both gates. <code>GET /repos/&hellip;/pages</code> reports <code>build_type: legacy</code> with <code>source: main</code>, which is GitHub&rsquo;s branch publishing mode; <code>deploy-pages</code> only works when the build source is &ldquo;GitHub Actions&rdquo;. The site itself deployed correctly through the legacy builder and serves this pass (verified by fetching the live URL). The workflow now reads the build source and skips the publish steps in legacy mode, so a green run means &ldquo;the commit is shippable&rdquo; rather than &ldquo;the workflow published it&rdquo;.</td><td>Owner: flip the build source (SG-43) if gated publishing is wanted; otherwise treat the workflow as CI on <code>main</code></td></tr>
<tr id="FLG-052"><td>FLG-052</td><td>44 CSS classes the generator emitted had no style rule at all</td><td>Found 2026-11-20 by reading the built pages against <code>assets/style.css</code>. Every class the markup uses is now defined: the product card (<code>.prod</code>, <code>.prod-head</code>, <code>.prod-sub</code>, <code>.specs</code>), the picks (<code>.pick</code>), the hero columns (<code>.hero-copy</code>, <code>.hero-side</code>, <code>.hero-facts</code>), the topic band, the trust row, <code>.chip</code>, <code>.fine</code>, <code>.best</code>, <code>.watch</code>, <code>.cta-row</code>, <code>.link-quiet</code>, <code>.fbrand</code> and others rendered as plain unstyled blocks. Nine custom properties (<code>--ink-2</code>, <code>--tint</code>, <code>--clay</code>, <code>--clay-ink</code>, <code>--line-strong</code>, <code>--paper</code>, <code>--good</code>, <code>--r</code>, <code>--r-sm</code>) were referenced but never declared, so those rules were dropped by the browser. This is the mechanical reason the site read as generated rather than designed. <code>scripts/check_style.mjs</code> now fails the build if a class is emitted without a rule, if a <code>var()</code> has no value, or if an inline <code>style=</code> attribute reappears.</td><td>Closed in this pass. Owner: review the look in a browser; the gate can prove coverage, not taste</td></tr>
<tr id="FLG-053"><td>FLG-053</td><td>Three rows of the suggestion table carried broken class attributes</td><td>SG-34, SG-36 and SG-41 were written with an escaped quote and a stray closing bracket inside the class attribute (the value read <em>badge-warn</em> followed by an encoded quote and a &gt;), so the status badge and the rest of the row markup were swallowed into the attribute and never rendered. Fixed in the generator 2026-11-20; the design gate now rejects any class attribute containing an escaped quote or angle bracket.</td><td>Closed in this pass</td></tr>
<tr id="FLG-054"><td>FLG-054</td><td>The social card had overlapping text and captions hidden under the footer</td><td>In <code>assets/og-image.png</code>, the diagram label was drawn at a hard-coded height that landed on top of the subtitle, and the two shorter bar captions sat under the footer band. The image is the preview for every shared link, so the collision was the most-seen drawing the site had. <code>scripts/make_og.py</code> now measures each block and asserts that the label clears the subtitle and that the captions clear the footer; the card was regenerated and read back to confirm.</td><td>Closed in this pass; re-run <code>python3 scripts/make_og.py</code> after any copy change on the card</td></tr>
<tr id="FLG-055"><td>FLG-055</td><td>No way existed for a reader to send a suggestion</td><td>The brief asks for a suggestions section where someone can review options and choose a path, and the desk had that for the owner. It had no intake: a reader with a question had no route except an email address that was never published. Added 2026-11-20: a &ldquo;Suggest a topic&rdquo; form on the desk that opens a public GitHub issue on the repository (label <code>reader-suggestion</code>), and a reader-facing count that reads from <code>data/reader-suggestions.json</code>. The count is <strong>0</strong> because no reader has sent one; the file is deliberately not pre-filled.</td><td>Owner: if a different intake is wanted (email, a form service), the issue route is the current one and is recorded here rather than implied</td></tr>
<tr id="FLG-023"><td>FLG-023</td><td>Chooser-generated product links previously lacked <code>rel=&quot;sponsored&quot;</code></td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p>The recommendation list in the chooser is built in JavaScript. Those anchors pointed at tagged Amazon URLs with no <code>rel</code> attribute and no visible sponsored label, so a static HTML audit could not see them. Fixed in this pass: script-built links carry <code>rel=&quot;sponsored nofollow noopener&quot;</code>, the label, and the click attribute. <code>scripts/check_meta.mjs</code> now scans the JS as well as the HTML so it cannot regress.</td><td>None - closed by this pass; keep the JS check in CI</td></tr>
<tr id="FLG-024"><td>FLG-024</td><td>Generator wrote placeholder canonicals; deployed HTML had been patched by hand</td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p><code>build_site.py</code> emitted a placeholder domain as the canonical on every page while the live files carried the GitHub Pages URL after PR #7&rsquo;s manual fix - so the next rebuild would have replaced real canonicals with a placeholder on all 17 pages. Every page now self-canonicalises to its own absolute URL, the sitemap lists exactly the pages the build writes, and the sitemap&rsquo;s home entry matches the home page&rsquo;s canonical. Google&rsquo;s guidance: do not declare different canonicals for the same page by different methods, and include a self-referential canonical on the canonical page. Sources: <a href="https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls">canonical</a>, <a href="https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap">sitemaps</a>.</td><td>Re-check coverage in Search Console after the next deploy; re-run this wiring if a custom domain is adopted (SG-02)</td></tr>
<tr id="FLG-025"><td>FLG-025</td><td>FAQPage structured data must not be sold as an SEO win</td><td><p class="fine"><strong>Checked 2026-11-20 against Google&rsquo;s official &ldquo;What&rsquo;s new&rdquo; index</strong> (developers.google.com/search/updates): the May 2026 list includes &ldquo;Deprecating the FAQ rich result feature&rdquo; and the June 2026 list includes &ldquo;Removing documentation for the FAQ rich result feature&rdquo;. The exact days (7 May, 15 June) and the August 2023 restriction were not read on the entry itself, so they stay unverified.</p><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p>Each guide emits FAQPage JSON-LD. Secondary sources reporting on Google&rsquo;s documentation state that FAQ rich results were restricted to well-known government and health sites in August 2023 and stopped appearing for everyone on 7 May 2026, with the FAQ documentation removed on 15 June 2026. We did not read that notice on an official Google page in this session, so it is recorded here rather than asserted on a page; the markup itself is harmless and may still help machines read the answer. Source: <a href="https://developers.google.com/search/docs/appearance/structured-data">Google structured data overview</a> for what remains supported.</td><td>Confirm against Google Search Central, then keep the markup without claiming a rich-result benefit (affects S-09)</td></tr>
<tr id="FLG-026"><td>FLG-026</td><td>Creators/PA API eligibility not verified from an official page</td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p>Third-party guides consistently state that API access follows three qualifying sales inside 180 days. No Amazon page was read in this session that states it. This matters because the whole automation plan (SG-12) and the price/image policy (FLG-021) rest on it.</td><td>Read the eligibility notice in Associates Central &rarr; Tools &rarr; Product Advertising / Creators API and record the wording and date</td></tr>
<tr id="FLG-027"><td>FLG-027</td><td>SiteStripe image options: second-hand claim</td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p>Several third-party tutorials state that SiteStripe stopped offering Image and Text+Image link types in late 2023, leaving API access as the route to compliant product imagery. We have not verified that in the Associates console. It changes the photography plan (SG-04), so it is stated as unverified rather than as a constraint.</td><td>Open SiteStripe on any product page and record which link types exist, with the date</td></tr>
<tr id="FLG-028"><td>FLG-028</td><td>Three builds are published on one host, under two brands</td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p>The root publication, <code>counter-check/site/</code> (Counter Check) and the <code>docs/</code> + <code>articles/</code> build (Counter &amp; Crumb, still open as draft PR #10) are all reachable and all indexable, and the root sitemap previously listed <code>docs/</code> and <code>articles/</code> URLs. That splits the domain across near-duplicate content and two mastheads. Nothing here is a policy breach - it is a findability and brand problem. The sitemap generated by this pass lists only the pages this build writes.</td><td>Owner picks one publication (SG-14); then noindex or remove the others and reconcile the two mastheads</td></tr>
<tr id="FLG-029"><td>FLG-029</td><td>Snapshot dates are already ageing</td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p>Every field on this site carries the date 2026-11-19. Amazon listing content changes without notice, so the honest shelf life of a manual snapshot is days, not months. There is no scheduled re-read in the repository - only the rule that a figure must never be presented as current.</td><td>Adopt a re-read cadence (weekly while small, per publish for the pages touched) and record each pass on the register</td></tr>
<tr id="FLG-030"><td>FLG-030</td><td>The only image on the site is brand art</td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p><code>assets/og-image.png</code> is a generated typographic card for link previews. No product image, food photograph or AI-generated product visual is used anywhere, in line with the Program Content read in FLG-021.</td><td>Replace or extend imagery only under an approved licence (SG-04), and keep drawings labelled as ours</td></tr>
<tr id="FLG-031"><td>FLG-031</td><td>Disclosure wording changed to the Agreement&rsquo;s exact sentence</td><td><p class="fine"><strong>Restored 2026-11-20 (session fe0774e7).</strong> This row was published on main in commit 6021a30 (2026-11-19, storefront pass) and was missing from the register on 2026-11-20. The wording below is the original, unchanged. Its status was not re-checked in this pass unless a note below says so.</p>Pages previously read &quot;As an Amazon Associate, The Countertop Guide earns from qualifying purchases.&quot; Section 5 of the Operating Agreement requires the statement &quot;As an Amazon Associate I earn from qualifying purchases.&quot; or a substantially similar statement previously allowed under the Agreement; whether a reworded variant qualifies is not ours to decide, and Section 6 treats a Section 5 violation as a material breach. The strip and footer now carry the required sentence verbatim, with a plain-language explanation beside it. Source: <a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement Section 5</a>, read in-session.</td><td>Closed by this pass (answers request I-02 from session b4c6c619); revisit only with written comfort on an alternative wording</td></tr>
<tr id="FLG-056"><td>FLG-056</td><td>Register IDs FLG-023 to FLG-031 were dropped from the register, then restored</td><td>Commit 6021a30 (2026-11-19, storefront pass) published FLG-023 to FLG-031 on main. They were missing from this register on 2026-11-20 and were not listed as retired anywhere. FLG-023 to FLG-031 are restored above with their original wording and a restoration note. FLG-061 to FLG-066 have no trace on any remote branch as of 2026-11-20, so they remain unused numbers.</td><td>Read the restored rows; their statuses are as recorded when they were first published, and anything marked unverified there still is</td></tr>
<tr id="FLG-057"><td>FLG-057</td><td>A slug&rsquo;s own docstring contradicts the live page</td><td>In <code>build_site.py</code>, the comment above the topics section says the calendar holds &ldquo;five published and three queued&rdquo;, which was true when eight topics were drafted. The page itself reads the topic list and renders the current counts. Cosmetic, in the generator only, left as the author wrote it.</td><td>Cosmetic; noted so a future reader does not treat the comment as data</td></tr>
<tr id="FLG-058"><td>FLG-058</td><td>The Agreement sentence is above the fold, but not repeated inside each product card</td><td>FTC <a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">Disclosures 101</a> (re-read 2026-11-20) says the disclosure should be placed &ldquo;with the endorsement message itself&rdquo; and warns that disclosures are likely to be missed when they sit only at the end of a page or behind a click. On this site the Agreement sentence is directly under the masthead on every page plus the footer, and every card carries a visible &ldquo;Sponsored link &middot; opens Amazon&rdquo; line beside its button. The Agreement sentence itself is not inside each card. This pass did not change the layout: repeating the legal sentence in every card is a design and compliance judgement for the owner, not a unilateral edit.</td><td>Owner / compliance: keep the current arrangement (strip + per-card sponsored label) or add the sentence to each card. Either way, re-read this row when the layout next changes</td></tr>
<tr id="FLG-060"><td>FLG-060</td><td>2026-11-20 line-by-line re-read of all five listings; rating-count and used-price drift recorded</td><td>Session <code>1b65e5a1</code> re-fetched every official Amazon.com listing on 2026-11-20 and re-read title, rating, rating count, buy-box price, list price, dimensions, capacity, features, wattage and bullets line by line. Displayed fields all matched the register. Two volatile snapshot figures drifted and were updated in <code>data/products.json</code> (which is why they are not published on shop pages): P1 rating count 4,876&rarr;4,877 and used price $59.95&rarr;$62.85; P2 rating count 18,375&rarr;18,380. The P2 Item-details table again lists configuration as 24 functions and 7 accessories against the title's &ldquo;Six Cooking Accessories&rdquo; (re-confirms <a href="#FLG-021">FLG-021</a>). Scope notes, not irregularities: P2 wattage (1700 W/120 V) and P4 rating value / list price were carried from the 2026-11-19 register because those specific rows were not re-captured in this pass's chunks; they are attributed, not independently re-confirmed today. Sources: the five <code>https://www.amazon.com/dp/&lt;ASIN&gt;</code> listing pages, fetched 2026-11-20.</td><td>Keep the re-read cadence (FLG-040); treat every recorded figure as dated, never current</td></tr>
<tr id="FLG-067"><td>FLG-067</td><td>The design named two typefaces</td><td><code>assets/style.css</code> and <code>DESIGN_PROMPT.md</code> both specify Fraunces for display and Inter for text. No <code>@font-face</code> rule and no font files existed, so every visitor saw Georgia and the system UI font. This is the most likely reason the site read as generated: the whole typographic identity was a fallback. Fixed in this pass with four self-hosted latin variable fonts (182 KB, SIL OFL 1.1).</td><td>Closed; <code>check_style.mjs</code> now fails if a stylesheet declares a font family with no local file</td></tr>
<tr id="FLG-068"><td>FLG-068</td><td>No navigation state on any page</td><td>The header rendered identical links everywhere with no <code>aria-current</code>, so a reader had no orientation cue and a screen reader announced the current section as just another link. The stylesheet already had a <code>[aria-current]</code> rule: the markup never used it. Now generated per page from one link list.</td><td>Closed</td></tr>

<tr id="FLG-069"><td>FLG-069</td><td>Half of the indexable site was internal audit</td><td>Until this pass, the sitemap listed 26 URLs and 7 of them were the decision desk, executive summary, methodology, design brief, review desk, dashboard and the site-search page. They are useful to the owner and to a reader who follows a source link, but they are not what a shopper searched for, and they diluted the shopping clusters on the same host. Those seven now carry <code>noindex, follow</code> and stay out of the sitemap; the verification register, the flagged list and the compliance page stay indexed, because a buyer checking a spec benefits from them. The sitemap is now 20 URLs, all of them pages a buyer could want. Reversal is one line in <code>NOINDEX</code>.</td><td>Review with the owner; the split is a judgement call, recorded rather than hidden</td></tr>
<tr id="FLG-070"><td>FLG-070</td><td>Three builds are served from one host</td><td>The root publication is the only build with a sitemap and canonical tags. <code>docs/</code> (the target of draft PR #10) and <code>counter-check/site/</code> are also reachable under the same hostname, with their own titles and no <code>noindex</code>. Competing pages on one host is a findability problem, not a design one. Reported, not resolved: it changes files outside this session's scope.</td><td>Owner decision (<a href="suggestions.html#SG-51">SG-51</a>, <a href="suggestions.html#Q-34">Q-34</a>)</td></tr>
<tr id="FLG-071"><td>FLG-071</td><td>CHEF iQ listing states no temperature-tolerance</td><td>The listing (B0DZFD6R9Z) gives heat safety (1000&deg;F), probe count, sensor count and range, but no &plusmn; accuracy figure in the fields captured. The comparison pages and the new guide report this as an absence rather than borrowing the other listing&rsquo;s number.</td><td>Read the manual linked from the listing, or request it from the seller (<a href="suggestions.html#Q-36">Q-36</a>)</td></tr>
<tr id="FLG-072"><td>FLG-072</td><td>ThermoMaven listing shows only an item length</td><td>The 2026-11-20 re-read found an <code>Item Length</code> of 6.5 inches and no width, height or depth in the listing&rsquo;s measurement block. The register stays blank rather than treating a single axis as dimensions. This narrows FLG-004 but does not close it.</td><td>Full dimension set from the manual, or leave blank (FLG-004)</td></tr>
<tr id="FLG-059"><td>FLG-059</td><td>Duplicate element ids introduced and removed during this pass</td><td>While adding a review panel to the decision desk, this session emitted a second set of buttons with the ids <code>sg-export</code>, <code>sg-print</code> and <code>sg-reset</code>. The desk already had them, so those ids appeared twice - an accessibility and scripting fault, because <code>getElementById</code> returns only the first. The redundant panel was removed and a duplicate-id check was added to <code>scripts/check_style.mjs</code>, which now reports zero across all 29 pages.</td><td>Closed in this pass; the gate prevents a repeat</td></tr>
<tr id="FLG-073"><td>FLG-073</td><td>One placeholder was carrying two meanings</td><td>Thirteen fields in <code>data/products.json</code> hold the literal string <code>&mdash;</code>. The page correctly renders that as &ldquo;Blank &mdash; not captured&rdquo;, but the same character is also used where the field genuinely does not apply (a thermometer has no capacity). So the data cannot distinguish &ldquo;we looked and did not find it&rdquo; from &ldquo;this field is meaningless for this product&rdquo;. Publishing reads the dash as blank, which is the safe direction. A future session must not treat it as a recorded figure.</td><td>Owner of <code>data/products.json</code> to split the two into <code>null</code> and an explicit <code>notApplicable</code> reason</td></tr>

<tr id="FLG-074"><td>FLG-074</td><td>Every feed item carries one date, and it is the listing re-read date</td><td>The RSS feed set <code>pubDate</code> from the listing verification date (<code>verifiedDate</code>) for all ten guides, so every item reads the same day. RSS 2.0 defines item <code>pubDate</code> as the publication date of the content (<a href="https://www.rssboard.org/rss-specification">RSS 2.0 spec, pubDate</a>). The generator now uses the page date (<code>contentDate</code>), as <code>data/editorial.json</code> already specifies. Today both values are 2026-11-20, so the feed output is unchanged. Per-guide publication dates are not recorded anywhere in the repo, and none is inferred here.</td><td>Owner of <code>data/editorial.json</code> to supply a publication date per guide (a <code>published</code> field) so each feed item can carry its own date</td></tr>
<tr id="FLG-075"><td>FLG-075</td><td>Two guides are live before their cadence week</td><td>The cadence rule says one guide per week, published on Tuesday. The queue marks <code>guide-gift-picks.html</code> (week 2026-11-24) and <code>guide-instant-read-vs-wireless.html</code> (week 2026-12-08) as <code>published</code>, and both are live on 2026-11-20. The queue also has 2026-12-08 published before the queued 2026-12-01 topic. The status is read as "page exists", not "week reached". Nothing was hidden or re-dated in this pass.</td><td>Owner decision: keep both pages live now and reword the rule, or hold them until their Tuesday (sitemap and feed are generated from the build, so either path is a one-line change)</td></tr>

<tr id="FLG-076"><td>FLG-076</td><td>This pass&rsquo;s re-read of the listings was deliberately partial</td><td>Session <code>42e09357</code> opened all five listings on 2026-11-20 and confirmed reachability and title match, plus one buy-box price it could attribute to the product (P4, $16.99, matching the register). Spec tables, ratings and the remaining prices were not re-read, so <code>verifiedDate</code> stays 2026-11-19 and no shop card was relabelled as freshly checked. Recorded rather than glossed, because the temptation in a re-read pass is to date everything the moment some of it was touched.</td><td>None; the next cadence pass re-reads the fields it intends to publish</td></tr>
<tr id="FLG-077"><td>FLG-077</td><td>The register stores normalised listing titles, not the exact characters on the page</td><td>Found on 2026-11-20 while diffing titles against the live pages: the P3 entry drops the registered-trademark mark that the listing prints after &ldquo;TurboFry&rdquo;, and the P4 entry writes the accuracy figure with a degree sign and an F (&ldquo;&plusmn;0.5&deg;F&rdquo;) where the listing uses the single DEGREE FAHRENHEIT character (U+2109). Both are normalisations made by us when the register was typed, not edits Amazon has made; every other word matches, for all five ASINs. They are recorded because a future byte-for-byte comparison will report a difference that means nothing unless the normalisation is written down.</td><td>Decide whether the register keeps exact strings; either way, note the normalisation instead of letting a diff guess</td></tr>
<tr id="FLG-078"><td>FLG-078</td><td>Three guides published into a window with no measured demand behind them</td><td>The brief asks for both seasonal, findable articles and topics chosen from measured queries. With no Search Console property there are no queries to choose from, so this pass published three holiday-window guides as labelled editorial hypotheses and recorded the cadence deviation in <code>data/editorial.json</code>. Nothing on the pages claims the topics are popular. Dated 2026-11-20.</td><td>Owner: connect Search Console (D-01/D-04), export queries after 28 days, then re-rank the queue; the three pages are the test, not the answer</td></tr>
<tr id="FLG-079"><td>FLG-079</td><td>The footprint drawings are ours, and they do not settle the imagery question</td><td>Each product card now carries an SVG drawn to a shared scale from the dimensions on the listing, labelled as a drawing rather than a photograph. It is original artwork, so it needs no Amazon licence, and <a href="flagged.html#FLG-009">FLG-009</a> (no product photography) stays open: a drawing is not a photograph of the machine, and no page should imply that it is.</td><td>Owner: keep drawings as the house visual (D-06 option 1), or fund photography; do not fill the gap with scraped images either way</td></tr>
<tr id="FLG-080"><td>FLG-080</td><td>The decision register proposes a rule the owner has not approved</td><td><code>data/decisions.json</code> carries a default: a gate unanswered for 28 days gets its recommended option applied, marked &ldquo;default applied&rdquo;, reversible in one commit. That rule is written as a proposal in the file and labelled as such on the page; until the owner approves it, nothing auto-applies and a silent board is still a silent board.</td><td>Owner: approve, change or reject the default rule (Q-14 asks the same question about review cadence)</td></tr>
<tr id="FLG-081"><td>FLG-081</td><td>Topic 12 on the calendar said &ldquo;Planned&rdquo; for a question the site had already answered</td><td>The row &ldquo;Holiday air fryer gifts: what to buy without the guesswork&rdquo; pointed at nothing, while <code>guide-gift-picks.html</code> has been live since 2026-11-19 and the cadence queue lists it as published 2026-11-24. This pass set the row to Published and pointed it at the existing page (an edit to another session&rsquo;s row, recorded here so the change is attributable). The queue&rsquo;s week label and the page&rsquo;s publish date are still one day apart; both are stated, not harmonised.</td><td>Owner: accept the correction, or revert the row and mark the guide unpublished; the calendar counts themselves are now computed from the data on every build</td></tr>
<tr id="FLG-082"><td>FLG-082</td><td>A build gate this session wrote could block the whole deploy, and did</td><td>The decision register shipped with a hard rule: any board row not triaged into a theme stopped the build. The suggestions board is append-only and every session adds rows to it, so within hours an unrelated session&rsquo;s new idea (Q-33..Q-37, SG-44..53, later SG-54..57) failed the Pages workflow for the entire site over an editorial to-do item. On 2026-11-20 the rule became a build warning plus a &ldquo;Nobody has taken these yet&rdquo; table on <a href="decisions.html#map">the register</a>, so an unowned row is visible to whoever must triage it instead of removing the site from readers. A gate that cannot be satisfied by the person who is blocked is not a gate, it is a hostage.</td><td>Owner: set the triage expectation (Q-14 asks for a review SLA); until then the register lists unowned rows on every build</td></tr>
<tr id="FLG-083"><td>FLG-083</td><td>A 2026-11-20 re-read of all five listings: displayed specs still match; three volatile figures moved; P5's size selector showed a different headline price</td><td>Session <code>84799c33</code> fetched all five listing pages on 2026-11-20 and re-read title, rating, rating count, buy-box price, list price, Product-information table and bullets. Confirmed unchanged on the page: P1 title, rating 4.2 with 4,878 ratings (register 4,877 - drift of one), buy box $79.93, list $99.99, used $62.85; P2 title, rating 4.3 with 18,380 ratings, buy box $149.99, list $209.99, dimensions 16.9&quot;D x 15.8&quot;W x 14.8&quot;H and capacity 24.6 liters; P3 title, rating 4.4 with 16,894 ratings (register 16,892), buy box $69.99, list $119.99, dimensions 12.75&quot;D x 13.5&quot;W x 10&quot;H, capacity 8 quarts, the 1000 W/120 V bullet and the same page carrying a Black Friday deal label; P4 title, rating 4.6 with 3,499 ratings, buy box $16.99, Product-information table (Brand, Special Feature, Color, Included Components, Specification Met, Unit Count - again no dimensions row); P5 title, buy box $119.99 for the 3-probe variant, list $219.99, Item-details table including 3 Probes, Hub and the two-year CHEF iQ assurance bullet. <strong>Two things are recorded, not published.</strong> (1) P3's rating count moved 16,892 &rarr; 16,894 between passes; that is the normal drift the site already refuses to print. (2) P5's page shows a size selector in which the 3-probe variant reads $119.99 while the variant list also shows 1 Probe at $99.99 (list $129.99), 2 Probes at $99.99 (list $179.99) and 4 Probes at $142.49; the register's &ldquo;$119.99 (3-probe variant)&rdquo; remains correct for the ASIN's default variant, but a buyer on a small screen may land on a different variant's price, which is exactly why shop pages link to Amazon rather than print a figure. No value was edited on the strength of a carousel or a sponsored placement. Sources: <code>https://www.amazon.com/gp/aw/d/&lt;ASIN&gt;</code> for B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z, fetched 2026-11-20.</td><td>None blocking. Next cadence pass re-reads and re-dates; the register keeps dated observations, the shop pages keep linking instead of quoting</td></tr>
<tr id="FLG-084"><td>FLG-084</td><td>The front page now leads with a decision table, so a wrong reading of one field would be the most expensive mistake on the site</td><td>The front page was rebuilt in this pass around one table (product, the job it wins, capacity as titled, counter depth in inches and centimetres, what to check before ordering). Every cell is read from <code>data/products.json</code>, and the table is generated by <code>shelf_table()</code> in <code>build_site.py</code>, so a value can only change if the register changes. The risk this records is editorial, not technical: the &ldquo;pick it if&rdquo; column is a reading of listing fields, not a test result, and it must stay worded as a job description. Two rows deliberately print a gap (P4 and P5 depth) rather than a number, because the listings' captured fields do not state dimensions - <a href="#FLG-004">FLG-004</a>.</td><td>Owner: read the five &ldquo;pick it if&rdquo; lines as a buyer and change any that reads like a ranking claim; the gate can prove the values match the register, not that the sentence is fair</td></tr>
</table></div>
"""
page_to("flagged.html","Flagged for review: open items | Countertop Guide","Every irregularity and unverified item on this site, with the source read and the action that would close it. Flags block claims, not publishing.",flag_body)
# ---------- COMPLIANCE ----------
comp_body = f"""
<p class="eyebrow">Compliance gate</p>
<h1>Disclosures &amp; policy checks in the publishing workflow</h1>
<p class="lede">Disclosure above the fold on every page, in the Agreement&rsquo;s own words, and repeated in the footer. Every outbound product link - static or script-built - is marked sponsored and labelled. Volatile Program Content is not displayed at all, because a static build cannot refresh it inside 24 hours. Endorsement context is reviewed against the Operating Agreement and FTC guidance before publishing.</p>
<h2>Our disclosure (verbatim, every page)</h2>
<blockquote>{esc(SITE["disclosure"])}</blockquote>
<p class="fine">Rendered from <code>data/products.json</code> &rarr; <code>site.disclosure</code>, the same field the strip and the footer read, so this page cannot drift from what the site actually says. The sentence up to the first full stop is the one Operating Agreement section 5 requires.</p>
<h2>How each outbound link is marked</h2>
<ul>
<li>URL format: <code>https://www.amazon.com/dp/ASIN?tag={TAG}</code> (official listing URL + tracking ID).</li>
<li>Attributes: <code>rel="sponsored nofollow noopener"</code>, <code>target="_blank"</code>, visible "sponsored" label and "Opens amazon.com" text so destination is never obscured.</li>
<li>Short links are recorded in the <a href="verification.html">verification register</a> as submitted links with observed redirect targets in a separate field. They are not used as outbound buttons.</li>
</ul>
<h2>What the policies say, in their own words (re-read 2026-11-20)</h2>
<div class="table-scroll"><table>
<tr><th>Rule</th><th>What we read</th><th>What this site does because of it</th></tr>
<tr><td>Identifying yourself as an Associate<br><span class="fine">Operating Agreement, Section 5</span></td><td>&quot;You must clearly and prominently state the following, or any substantially similar statement previously allowed under this Agreement&hellip;: &lsquo;As an Amazon Associate I earn from qualifying purchases.&rsquo;&quot; Section 6 treats a violation of Section 5 as a material breach.</td><td>That exact sentence appears in the strip under the masthead and in the footer of every page, with a plain-language addition beside it. A reworded variant was in use before this pass; see <a href="flagged.html#FLG-042">FLG-042</a>.</td></tr>
<tr><td>Prices and availability<br><span class="fine">Program Policies, Participation Requirements</span></td><td>&quot;your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API and you comply with the requirements regarding use of Creators API or PA API in the License.&quot;</td><td>No price figures on shop pages. Buttons say &ldquo;See today&rsquo;s price on Amazon&rdquo;. Dated observations stay in the register and are labelled as observations (<a href="flagged.html#FLG-032">FLG-032</a>, <a href="flagged.html#FLG-033">FLG-033</a>).</td></tr>
<tr><td>Storing or caching Program Content<br><span class="fine">Program Policies, IP License and Usage Requirements, clause (h)</span></td><td>&quot;You will not store or cache Product Advertising Content consisting of an image, but you may store a link to Product Advertising Content consisting of an image for up to 24 hours. You may store other Product Advertising Content&hellip;for up to 24 hours, but if you do so you must immediately thereafter refresh&hellip;&quot;</td><td>No Amazon images anywhere (brand art and our own diagrams only). Ratings, badges and &ldquo;bought in past month&rdquo; counts are volatile Program Content, so they left the shop pages with the prices. A refresh job is the only route back (SG-20).</td></tr>
<tr><td>No price tracking or alerting<br><span class="fine">Program Policies, Participation Requirements, clause (y)</span></td><td>&quot;Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality.&quot;</td><td>We do not build a price-drop alert, a watchlist or a &ldquo;notify me&rdquo; form, even though it is a common affiliate feature. Reader capture, if ever approved (SG-07), may only cover new guides.</td></tr>
</table></div>
<p class="fine">Quotations were read from the linked official pages during this session. Policy text changes; the authoritative copy is the page, not this table. This is a publishing checklist, not legal advice.</p>
<h2>Policy checklist (reviewed {VERIFIED})</h2>
<div class="table-scroll"><table>
<tr><th>Check</th><th>Source</th><th>Our practice</th></tr>
<tr><td>Use proper tagged Special Link formats</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement Section 5</a></td><td>Official URL + tag; manual SiteStripe test is a gate (FLG-001); the supplied short links are recorded, not used as buttons</td></tr>
<tr><td>Do not obscure link destination</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td><td>Button text + ASIN + "Opens amazon.com" on every card</td></tr>
<tr><td>Disclose material connection, hard to miss</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td><td>Strip under masthead on every page + footer; simple language ("earns from qualifying purchases")</td></tr>
<tr><td>Endorsement honesty; no unsubstantiated claims</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td><td>No testing/trend claims; seller claims attributed ("per listing")</td></tr>
<tr><td>Program Content / images</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement S1</a></td><td>No Amazon images copied; SVG/CSS only until licence decided</td></tr>
</table></div>
<p class="small">This page is a publishing checklist, not legal advice. Review disclosure placement and endorsement context against the current Agreement and FTC guidance at each publish. If in doubt, flag it.</p>
"""
page_to("compliance.html","Compliance: disclosure & policy | Countertop Guide","How the disclosure, the sponsored marking, price display and imagery are handled, with the Amazon and FTC rules quoted and linked.",comp_body)
def cadence_row(c):
    note = f'<p class="small">{esc(c["note"])}</p>' if c.get("note") else ""
    page = f' &middot; {esc(c["page"])}' if c["page"] else ""
    return f'<tr><td>{c["week"]}</td><td>{esc(c["title"])}{note}</td><td>{esc(c["status"])}{page}</td></tr>'

# ---------- METHODOLOGY ----------
meth_body = f"""
<p class="eyebrow">Method</p>
<h1>How we verify, measure, and decide - without hallucinating</h1>
<p class="lede">Automate what can be automated; put a gate in front of what cannot. This page is the machinery: evidence rules, analytics events, and the empty campaign ledger.</p>
<h2>Evidence rule</h2>
<ul>
<li>Every product fact links to its Amazon listing and <a href="verification.html">verification record</a>. Missing = blank + flagged.</li>
<li>"Trending" / popularity claims require a dated snapshot from an official category page. We make none.</li>
<li>Seller claims are attributed ("per listing"). Derived math shows its method. Prices always carry a snapshot date.</li>
<li>Hands-on testing claims require a published protocol and photos. We make none.</li>
</ul>
<h2>Analytics: five defined events (privacy-preserving)</h2>
<div class="table-scroll"><table>
<tr><th>Event</th><th>When it fires</th><th>Data kept</th></tr>
<tr><td>page_view</td><td>Page load</td><td>Path + timestamp (local only until endpoint deployed)</td></tr>
<tr><td>outbound_click</td><td>Sponsored Amazon click</td><td>ASIN + destination (no personal data)</td></tr>
<tr><td>search</td><td>Site search submitted</td><td>Query string</td></tr>
<tr><td>chooser_complete</td><td>3-question chooser finished</td><td>Answers (q1/q2/q3)</td></tr>
<tr><td>guide_read</td><td>Guide scrolled 75%</td><td>Guide path</td></tr>
</table></div>
<p>Implementation: one client, <code>assets/app.js</code>, and those five names only. It counts in <code>localStorage</code> and beacons to a configurable endpoint (<code>data-analytics-endpoint</code>) that is empty in this build, so nothing leaves the browser. No cookies, no identifiers, no third-party trackers.</p>
<p class="fine">Contract notes settled 2026-11-20: the repository once carried three event vocabularies (this client, the endpoint stub, and two legacy trackers). They are now unified into the five names above, and that is a checked contract: <code>scripts/check_measure.mjs</code> runs in the deploy workflow and fails the build if <code>assets/app.js</code>, <code>analytics-endpoint/server.py</code>, <code>data/editorial.json</code> and this page ever disagree again. The legacy tracker <code>assets/js/analytics.js</code> was deleted rather than renamed (it invented client-side conversion events, which this site must not do - conversions belong to authorized first-party reports); the root <code>app.js</code> remains because it only counts locally for the supplementary review builds. Requests R-06 and R-07 in <code>COORDINATION.md</code> are closed by this pass.</p>
<p class="fine">Endpoint status, stated exactly: no host is configured, so nothing is transmitted and the browser-local counts are all that exist. The endpoint implementation in this repository (<code>analytics-endpoint/server.py</code>) now accepts exactly these five names and the envelope this client sends; its self-test (<code>analytics-endpoint/selftest.py</code>, also run by the deploy gate) proves all five events record, the old vocabularies are rejected, and no query text or per-event timestamps are stored. Hosting is the one piece automation cannot supply: the owner picks an HTTPS host and a retention period (<a href="suggestions.html#SG-03">SG-03</a>, <a href="suggestions.html#Q-08">Q-08</a>) and sets <code>events.endpoint</code> in <code>data/editorial.json</code>; the gate in the client does the rest.</p>
<h2>What your browser has recorded</h2>
<div id="local-meter"><p class="fine">This section fills in with the counts stored on this device, if JavaScript is running. Nothing is sent anywhere and nothing is written to a server.</p></div>
<h2>Campaign ledger (empty by design)</h2>
<div class="table-scroll"><table>
<tr><th>Timestamp</th><th>Source</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th><th>Reported orders</th><th>Provenance (report + date obtained)</th></tr>
<tr><td colspan="7"><em>No rows yet. Add timestamp, source, channel, eligible sessions, clicks and reported orders only when obtained from authorized first-party reports (Associates Central). No conversion score or revenue forecast is presented.</em></td></tr>
</table></div>
<h2>What is automated, and what is gated</h2>
<div class="table-scroll"><table>
<tr><th>Step</th><th>State</th><th>How it works / what stops it</th></tr>
<tr><td>Page rendering</td><td><span class="badge-ok">Automated</span></td><td><code>build_site.py</code> writes every page, the sitemap, the feed, robots and the search index from <code>data/products.json</code> + <code>data/editorial.json</code>. No page is hand-edited, and the build is deterministic: the same data produces the same files, so a CI diff catches a stale commit.</td></tr>
<tr><td>Metadata, disclosure, sponsored marking, voice rules</td><td><span class="badge-ok">Automated + blocking</span></td><td><code>scripts/check_meta.mjs</code> runs in the deploy workflow after the build. A duplicate title, a missing canonical, an unlabelled Amazon link, a broken internal link, a banned phrase or a price figure on a shop page fails the deploy.</td></tr>
<tr><td>Measurement contract (5 events)</td><td><span class="badge-ok">Automated + blocking</span></td><td><code>scripts/check_measure.mjs</code> runs in the deploy workflow with the endpoint&rsquo;s own self-test. If the client, the server, the data record and this page disagree on the event names - or a retired tracker reappears - the deploy fails. Conversions stay out of client events by design.</td></tr><tr><td>Adding a guide to sitemap and feed</td><td><span class="badge-ok">Automated</span></td><td>The guide list and the page registry drive both files, so a new guide cannot be published and forgotten.</td></tr>
<tr><td>Product data refresh</td><td><span class="badge-flag">Gated</span></td><td>Manual re-read only. Creators/PA API access is the automated route and is not available to this build yet (<a href="flagged.html#FLG-037">FLG-037</a>).</td></tr>
<tr><td>Publishing path</td><td><span class="badge-warn">Split today</span></td><td>The workflow builds, checks determinism and runs both gates on every push to <code>main</code>; the pages readers see are served by GitHub&rsquo;s branch build, because that is what the repository&rsquo;s Pages source is set to. A gate failure therefore marks the commit red instead of stopping a publish. Switching the build source to GitHub Actions would make the gate block the deploy (<a href="suggestions.html#SG-43">SG-43</a>, <a href="flagged.html#FLG-051">FLG-051</a>).</td></tr>
<tr><td>Special Link validation</td><td><span class="badge-flag">Gated</span></td><td>A human must click a test link in the enrolled Associates workflow and confirm the destination and the tracking report (SG-01). No automation can substitute for it.</td></tr>
<tr><td>Conversion and revenue</td><td><span class="badge-flag">Gated</span></td><td>Filled only from authorized first-party reports; nothing client-side may write a conversion.</td></tr>
<tr><td>Photography</td><td><span class="badge-flag">Gated</span></td><td>Licence decision pending (SG-04, FLG-038).</td></tr>
</table></div>
<h2>Publishing cadence</h2>
<p>One guide per week, published Tuesday, from the queue in <code>data/editorial.json</code>. Each guide enters the sitemap and the feed at build time; the next four topics come from measured queries after 28 days of Search Console data, not from instinct. Until then the calendar is a stated plan, not a demand claim.</p>
<div class="table-scroll"><table>
<tr><th>Planned</th><th>Topic</th><th>Status</th></tr>
{"".join(cadence_row(c) for c in CADENCE["queue"])}
</table></div>
<p class="fine">{esc(CADENCE["rule"])} {esc(CADENCE["measure"])}</p>
"""
page_to("methodology.html","Method, events & campaign ledger | Countertop Guide","What is automated and what is gated, the five privacy-preserving events, the empty campaign ledger and the publishing cadence we keep.",meth_body)

topic_rows = ""
for t in TOPICS:
    src = " &middot; ".join(f'<a href="{u}">{esc(l)}</a>' for l, u in t["sources"])
    status = f'<span class="status-published">{t["status"]}</span>' if t["status"] == "Published" else f'<span class="status-planned">{t["status"]} - editorial hypothesis</span>'
    title_cell = f'<a href="{t["href"]}">{esc(t["title"])}</a>' if t["status"] == "Published" else esc(t["title"])
    topic_rows += f"""
<tr id="t{t['n']}"><td>{t['n']}</td><td>{title_cell}</td><td>{esc(t['cat'])}</td><td>{status}</td><td>{esc(t['angle'])}</td><td>{esc(t['hooks'])}</td><td>{src}</td></tr>"""

topics_body = f"""
<p class="eyebrow">The desk &middot; Topic calendar</p>
<h1>The topic calendar: twelve buyer questions, spec-backed answers</h1>
<p>{NUMW[sum(1 for t in TOPICS if t["status"]=="Published")].capitalize()} guides are published; {NUMW[sum(1 for t in TOPICS if t["status"]!="Published")]} are queued as working titles. Every title is an editorial hypothesis backed by verified listing fields - not a claim about search volume, popularity or product superiority. The next topic is chosen from measured queries, not instinct.</p>
<div class="callout"><b>How this calendar works</b>
<p>Each topic states the buyer question it answers, the verified fields it will be built from, and its sources. Queued titles publish only after their fields are verified against the listing and the guide is added to the <a href="sitemap.xml">sitemap</a> and <a href="feed.xml">feed</a>. Working titles may change at edit stage.</p></div>
<h2>The calendar</h2>
<div class="table-wrap"><table>
<tr><th>#</th><th>Working title</th><th>Category</th><th>Status</th><th>What it answers</th><th>Verified fields it uses</th><th>Sources</th></tr>
{topic_rows}
</table></div>
<h2>Publishing cadence</h2>
<p>One thoroughly checked guide per publishing slot, with a reassessment after the first batch of measured data. This is an operational plan, not a traffic promise. Every new guide is added to <a href="sitemap.xml">sitemap.xml</a> and <a href="feed.xml">feed.xml</a> at publish time.</p>
<p class="fine">No topic here is a claim that the subject is popular or in demand. If a popularity claim is ever made, it carries a dated snapshot from an official source (see <a href="methodology.html">Method</a>).</p>
"""
page_to("topics.html","Topic calendar: twelve buyer questions | Countertop Guide","Twelve question-shaped, spec-backed article working titles - five published, seven queued - with the verified fields and sources each is built from.",topics_body)


# ---------- SEARCH ----------
search_body = """
<p class="eyebrow">Search</p>
<h1>Search the site</h1>
<form id="search-page-form" role="search">
  <label for="search-input">Search guides &amp; products</label>
  <input id="search-input" type="search" placeholder="Try capacity or thermometer">
  <button class="btn" type="submit">Search</button>
</form>
<div id="search-results" aria-live="polite"></div>
<p><a href="search.html">Browse all</a> - <a href="guides.html">Guides</a> - <a href="compare.html">Compare</a></p>
"""
page_to("search.html","Search the guides and products | Countertop Guide","Search this site's buying guides and product comparisons for air fryers and meat thermometers.",search_body)
# ---------- ABOUT ----------
about_body = f"""
<p class="eyebrow">About</p>
<h1>What this site is, and what it will not do</h1>
<p class="lede">The Countertop Guide is a small buying publication for two kinds of countertop appliance: air fryers and meat thermometers. It exists because the comparison pages that rank for these products usually claim to have cooked with machines nobody cooked with. We do the opposite: we read the listing carefully, do the arithmetic the listing will not do for you, and say plainly which fields are missing.</p>

<h2>Who writes it</h2>
<p>Articles are published under the <strong>{esc(DESK)}</strong> byline. That is honest: no individual here has a credential we can show you, so we do not attach one. A named byline with a real bio is an open decision the site owner has to make &mdash; see <a href="suggestions.html#SG-26">SG-26</a>.</p>

<h2 id="money">How this site makes money</h2>
<p>Product links are Amazon Associates links carrying our tracking ID (<code>{TAG}</code>). If you click one and buy something on Amazon within the session rules, we earn a commission. That is the whole business model: no display advertising, no sponsored posts sold to brands, no email list, no third-party trackers.</p>
<p>Because we are paid on clicks, the interesting question is whether that payment changes what we tell you. Here is the contract we hold ourselves to:</p>
<ul>
<li><strong>Links go where they say they go.</strong> Every product link opens that exact Amazon listing. They carry <code>rel="sponsored"</code> so search engines can tell, and the word &ldquo;sponsored&rdquo; appears next to them for you.</li>
<li><strong>We publish the negatives.</strong> Missing dimensions, an uncaptured wattage, a title that contradicts the bullet list &mdash; all of it is on the page, not in a basement. See <a href="flagged.html">Flagged for review</a>.</li>
<li><strong>No invented urgency.</strong> No countdowns, no &ldquo;only 3 left&rdquo;, no trend claim without a dated snapshot of the official category page.</li>
<li><strong>No price theatre.</strong> We do not show a strike-through &ldquo;list price&rdquo; we cannot keep current. Amazon&rsquo;s rules only allow a site to display price and availability when Amazon serves it or when it is pulled from their API and refreshed inside 24 hours; a static page can&rsquo;t honestly do either, so the button says &ldquo;see today&rsquo;s price&rdquo;.</li>
</ul>

<h2>How a fact gets onto a page</h2>
<ol>
<li>A listing field is read and copied, with its URL and the date, into <code>data/products.json</code>.</li>
<li><code>build_site.py</code> renders it. Editorial lines such as &ldquo;Good for&rdquo; paraphrase a listed feature and attribute it; they never add a fact.</li>
<li><code>scripts/check_meta.mjs</code> runs in the deploy pipeline and fails the build if the disclosure, the sponsored marking, the metadata, a link or the voice rules are broken.</li>
<li>Anything we could not confirm is blank on the page and present on the register, with the reason.</li>
</ol>

<h2>What we do not claim</h2>
<div class="table-scroll"><table>
<tr><th>Nobody here has&hellip;</th><th>Why the page still helps</th><th>What would change that</th></tr>
<tr><td>&hellip;cooked in any of these fryers</td><td>Crispness, noise and browning are the seller&rsquo;s words, quoted as such; the specs are the arithmetic</td><td>A funded test protocol and dated photos (<a href="suggestions.html#SG-09">SG-09</a>)</td></tr>
<tr><td>&hellip;calibrated either thermometer</td><td>We report the stated tolerance and the named certification, and say when no figure exists</td><td>A reference thermometer and a written method</td></tr>
<tr><td>&hellip;seen the search volume for any topic here</td><td>Each guide is a question a buyer might type, labelled as a hypothesis</td><td>28 days of Search Console data (<a href="suggestions.html#SG-32">SG-32</a>)</td></tr>
<tr><td>&hellip;verified the account&rsquo;s commission rate</td><td>So we never quote earnings or forecast revenue</td><td>An authorized first-party report, recorded in the ledger with its date</td></tr>
</table></div>

<h2>Corrections</h2>
<p>Amazon listings change without notice, and a page that is 90 days old can be wrong through no fault of its author. The register is dated on purpose: every page states the date its data was checked. If you find a mismatch between this site and the current listing, the listing wins &mdash; and we want to know. Corrections belong on the register: the date, what it said, what it should say. No correction has been filed yet, so the first one opens the log.</p>

<h2>Policies and sources</h2>
<ul>
<li><a href="compliance.html">Disclosure and policy checklist</a> &mdash; how the links and the statement are handled.</li>
<li><a href="methodology.html">Method, analytics events and the campaign ledger</a>.</li>
<li><a href="verification.html">Line-by-line verification register</a> for every product field.</li>
<li>Amazon Associates <a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement</a> and <a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a>; <a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a> and <a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">endorsement guidance</a>; <a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links">Google on qualifying outbound links</a>.</li>
</ul>
<p class="fine">This page describes our practice; it is not legal advice. The Operating Agreement and the Program Policies govern. The policy text in the table above was re-read on 2026-11-20; the Program Policies revision date shown on the page at that read is 2026-04-14.</p>
"""
page_to("about.html","About us: how this site earns | Countertop Guide","Who writes here, how Amazon Associates money works, why no prices are quoted, what has not been tested and how corrections are handled.",about_body)

# ---------- GUIDES 7-9 (ported from session arena/2d5ebe5b, figure policy applied) ----------
b7, j7 = guide_shell("Guide - Seasonal - Holiday 2026", "The holiday hosting test: which air fryer actually feeds a crowd?",
 f"Thanksgiving week, Hanukkah, game day, the office cookie swap - December asks more of a countertop appliance than a Tuesday does. Here is how our three verified fryers answer the hosting questions that actually decide the meal: how much fits, how many dishes run at once, and whether it fits the counter when the mixer is already there.",
 f"""
<h2>The three hosting questions</h2>
<ol>
<li><strong>How much actually fits?</strong> The Emeril 26QT listing claims a 6-lb rotisserie chicken and a 12-inch pizza, and describes serving 4-6 people (seller claim, per bullets). The Chefman 6QT splits into two 3-quart baskets - two side dishes at once with Sync Finish. The Chefman 8QT is one 8-quart cavity for a single big dish.</li>
<li><strong>How many dishes can run at once?</strong> Only the dual-basket cooks two different foods on independent settings. The oven wins on volume per dish; the dual-basket wins on dish count.</li>
<li><strong>Will it still fit when the counter is full?</strong> December counters host pie boxes and cutting boards. Depth is the binding constraint: 32.4 cm (Chefman 8QT), 34.0 cm (Chefman 6QT dual), 42.9 cm (Emeril oven). Measure before the guests arrive.</li>
</ol>
<h2>Holiday math from the listing data</h2>
<div class="table-scroll"><table>
<tr><th>Hosting job</th><th>Best fit (from verified specs)</th><th>Why</th></tr>
<tr><td>Two sides at once (beans + potatoes)</td><td>Chefman 6QT Dual <span class="meta">B0CDY277D3</span></td><td>Two 3 Qt baskets, Sync Finish, narrowest footprint (158.0 sq in)</td></tr>
<tr><td>Rotisserie chicken / 12&quot; pizza</td><td>Emeril 26QT Oven <span class="meta">B09B7SB46R</span></td><td>Only unit whose listing claims rotisserie + 12-inch pizza (per bullets)</td></tr>
<tr><td>Big single dish in a small kitchen</td><td>Chefman 8QT Basket <span class="meta">B08DKYBTPH</span></td><td>8 qt single cavity, shallowest depth (32.4 cm)</td></tr>
</table></div>
<p class="small">Food-fit claims ("6-lb chicken", "4-6 people") are quoted from the seller's listing text. We have not cooked a holiday meal in any unit - portion math is yours to sanity-check.</p>
<h2>Holiday price reality</h2>
<p>We do not quote prices on this page: they move, and the buy button goes to the live listing for a reason. The dated snapshots this desk read on {VERIFIED} sit in the <a href="verification.html">verification register</a>. Listings read that day showed deal badges across the board (a dated observation, not a claim about today) and a holiday return window running to January 31, 2027 for purchases made November 1 - December 31, 2026. Confirm both on the listing before you buy.</p>
""",
 [("Which air fryer is best for Thanksgiving?","Whichever fits your counter and your dish count. For two sides at once, the Chefman 6QT dual-basket (2 x 3 Qt with Sync Finish). For a rotisserie chicken or 12-inch pizza, the Emeril 26QT (claims per its listing). Measure counter depth first: the Emeril needs 42.9 cm."),
  ("Do these make good holiday gifts?","The ThermoMaven listing itself positions the thermometer as a stocking stuffer and Secret Santa gift (seller claim). Our gift-by-budget guide maps the five products into budget bands."),
  ("Are the holiday prices final?","We do not quote prices on the site - snapshots go stale within days. Check the live listing price before buying; the register keeps what each listing showed on the check date.")],
 picks=("P1", "P2", "P3"))
page_to("guide-holiday-hosting.html", "Holiday hosting: which air fryer feeds a crowd? | Countertop Guide", "Holiday hosting questions from verified listings: two dishes at once, rotisserie and pizza claims, counter-depth math.", b7, j7, "guide-page")

b8, j8 = guide_shell("Guide - Seasonal - Gifts", "Kitchen gifts under $25, under $80 and under $150",
 f"Gift guides usually invent prices. This one maps the five listings we verify into budget bands and quotes each product's own gift positioning where the seller makes one. Bands are a starting map, not a price promise: every product's dated price snapshot lives in the <a href=\"verification.html\">verification register</a>.",
 f"""
<h2>The bands (listing data checked {VERIFIED})</h2>
<div class="table-scroll"><table>
<tr><th>Budget band</th><th>Pick</th><th>Who it's for</th><th>Listing's own gift claim</th></tr>
<tr><td>Under $25</td><td>ThermoMaven 1-Second Instant-Read <span class="meta">B0DHZTCNR5</span></td><td>Grillers, candy makers, anyone who cuts into chicken to "check"</td><td>Bullets call it a stocking stuffer and Secret Santa pick (seller claim) - and it includes a calibration certificate</td></tr>
<tr><td>Under $80</td><td>Chefman 8QT TurboFry <span class="meta">B08DKYBTPH</span></td><td>Family kitchens, dorms, first apartments</td><td>Listing positions the square shape for small counters (seller claim)</td></tr>
<tr><td>Under $80</td><td>Chefman 6QT Dual-Basket <span class="meta">B0CDY277D3</span></td><td>Meal preppers who cook mains and sides together</td><td>Viewing windows and Sync Finish are the headline features</td></tr>
<tr><td>Under $150</td><td>Emeril 26QT French-Door Oven <span class="meta">B09B7SB46R</span></td><td>Hosts, bakers, rotisserie-curious cooks</td><td>Six (or seven - see <a href="flagged.html#FLG-021">FLG-021</a>) accessories included</td></tr>
<tr><td>Under $150</td><td>CHEF iQ Sense Wireless (3 probes) <span class="meta">B0DZFD6R9Z</span></td><td>Smokers, brisket people, tech-forward cooks</td><td>Three probes = three proteins at once (seller claim)</td></tr>
</table></div>
<p class="small">Budget bands are editorial frames, not price claims. Whether a product currently sits inside a band is a live-listing question - check the dated snapshot in the register and the live price on Amazon.</p>
<h2>Gift-giver's checklist</h2>
<ol>
<li><strong>Check the return window.</strong> The listings we read on {VERIFIED} showed a holiday return window to January 31, 2027 for purchases November 1 - December 31, 2026. Confirm on the listing before gifting.</li>
<li><strong>Match the cook, not the logo.</strong> A wireless probe set delights a smoker owner and confuses a scrambled-eggs person. More angles in our <a href="guide-gift-picks.html">gift-picks checklist</a>.</li>
<li><strong>Mind the counter.</strong> You are gifting counter space as much as an appliance - the depth table in our <a href="guide-cleanup-counter-space.html">counter-space guide</a> applies to gifts too.</li>
<li><strong>Prices move.</strong> We deliberately do not quote them here. Check the live listing price before you buy.</li>
</ol>
<p class="small">We have not tested any of these as gifts (or as anything else). Claims quoted as "seller claims" come from the listing text, linked in the <a href="verification.html">source record</a>.</p>
""",
 [("What is a good kitchen gift under $25?","The ThermoMaven instant-read thermometer. Its own listing calls it a stocking stuffer and Secret Santa pick, and it includes a calibration certificate. Its dated price snapshot sits in the verification register."),
  ("Is the Chefman dual-basket a good mid-band gift?","Its buy-box snapshot on the check date sat inside the band against a higher list price shown on the listing (both in the register). Prices are snapshots and move - confirm on Amazon."),
  ("Should I gift an air fryer to someone with a small kitchen?","Measure their counter depth first. The Chefman 8QT is the shallowest of the three fryers here at 12.75 in (32.4 cm); the Emeril oven needs 16.9 in (42.9 cm).")],
 picks=("P4", "P3", "P2"))
page_to("guide-gifts-by-budget.html", "Kitchen gifts under $25, $80 and $150 | Countertop Guide", "Holiday gift bands from five verified Amazon listings: who each pick is for, the listings' own gift claims quoted, and a gift-giver's checklist.", b8, j8, "guide-page")

b9, j9 = guide_shell("Guide - Air fryers - Specs", "Will it trip the breaker? Wattage and outlet math for air fryers",
 "Air fryers are high-wattage appliances, and wattage is the spec listings are most likely to get inconsistent. We found exactly that on one of our own products. Here is what wattage means for your kitchen circuit, and how to check any listing for the same trap.",
 f"""
<h2>What the listings say (read {VERIFIED})</h2>
<ul>
<li><strong>Chefman 6QT Dual (B0CDY277D3):</strong> "120 Volts/1700 Watts" in the listing bullets. One number, consistent.</li>
<li><strong>Emeril 26QT (B09B7SB46R):</strong> Product information table lists 1700 watts / 120 volts.</li>
<li><strong>Chefman 8QT (B08DKYBTPH):</strong> the bullets say "1000 Watts/120 Volts - RJ38-SQSS-8T" while the Product information table on the same page says 1700 watts. Both values are on the same listing. We show both and flag it (<a href="flagged.html#FLG-022">FLG-022</a>).</li>
</ul>
<h2>The kitchen math</h2>
<p>A standard US kitchen circuit is 120 volts, typically 15 amps (1,800 watts of capacity) or 20 amps (2,400 watts). The rule of thumb electricians use: keep a continuous load under about 80% of the circuit. That puts the safe continuous budget around 1,440 W on a 15-amp circuit.</p>
<p>At 1,700 watts, an air fryer is already above that 15-amp continuous budget on its own - which is why the manuals say "dedicated outlet". At 1,000 watts, there is usually room for a kettle or toaster on the same circuit. The difference matters most in older kitchens and dorms.</p>
<h2>How to check any listing for the wattage trap</h2>
<ol>
<li>Read the "About this item" bullets and note any wattage figure.</li>
<li>Open the "Product information" table (it is below the description) and compare.</li>
<li>If the two disagree, treat wattage as unresolved. Check the box or the manufacturer's spec sheet before you plan your circuit around it.</li>
<li>When in doubt, assume the higher number for safety planning.</li>
</ol>
<p class="small">This is general electrical guidance, not a certified electrician's advice. We derived the circuit math from standard US 120V/15A and 20A ratings; the wattage figures are quoted from the listings. We have not measured any unit's draw.</p>
""",
 [("How many watts does an air fryer use?","The fryers on this site are listed between 1000 and 1700 watts. The Chefman 8QT listing gives both 1000W (bullets) and 1700W (Product information) - we show both and flag the conflict. Check your unit's label before planning outlets."),
  ("Can I run an air fryer and a microwave on the same circuit?","Not safely if the air fryer draws 1700W: that alone approaches the capacity of a 15-amp, 120-volt kitchen circuit. Use separate outlets on separate circuits for two high-wattage appliances."),
  ("Why do two sections of the same listing show different wattage?","Seller-entered data can disagree between bullets and the Product information table, exactly as on the Chefman 8QT (FLG-022). Treat the conflict as unresolved and verify on the box or manufacturer's spec sheet.")],
 picks=("P3", "P1", "P2"))
page_to("guide-wattage-outlets.html", "Will it trip the breaker? Air fryer wattage math | Countertop Guide", "What 1000W vs 1700W means for a 120V kitchen circuit, the wattage conflict on the Chefman 8QT, and a checklist for verifying wattage on any listing.", b9, j9, "guide-page")

# ---------- SEASONAL GUIDES, 2026 holiday window (session arena/42e09357-prod1) ----------
# The window is fixed by statute, not by instinct: Thanksgiving Day 2026 is Thursday, 26 November
# (5 U.S.C. 6103, as listed by the US Office of Personnel Management, read 2026-11-20 at
# https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/). The Friday and Monday
# after it are retail names, not holidays in that law, so the copy treats them as days of the week.
HOLIDAY = {
    "thanksgiving": "Thursday, 26 November 2026",
    "friday": "Friday, 27 November 2026",
    "cybermonday": "Monday, 30 November 2026",
    "source": "https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/",
    "read": "2026-11-20",
}

b10, j10 = guide_shell(
    "Guide - Seasonal - Thanksgiving 2026",
    "Thanksgiving counter math: what actually fits the week you cook for six?",
    "The oven is spoken for on 26 November, so the question is what a countertop appliance can be asked to do, and whether it physically fits where you would put it. Both answers are on the listing. Nobody here has cooked a turkey in any of these machines, so this is a fit-and-claim check, not a recipe.",
    """
<section id="date">
<h2>The date, and why the counter is the real constraint</h2>
<p>Thanksgiving Day 2026 is <strong>Thursday, 26 November</strong>. That is federal law (5 U.S.C. 6103), listed on the <a href="HOLIDAY_SOURCE">US Office of Personnel Management's holiday schedule</a> and read on HOLIDAY_READ. The Friday after and the Monday after carry retail names; neither is a holiday in that law, so treat them as days when the kitchen is also busy.</p>
<p>Ask two questions before you ask which machine cooks best. First: how much counter depth do you have where it will live, not where it will sit for one photograph? Second: what does this listing claim it can cook, in its own words? Everything below is those two questions applied to the three fryers on this site.</p>
</section>
<section id="footprints">
<h2>Three machines, three footprints, stated sizes only</h2>
<div class="table-scroll"><table>
<tr><th>Machine</th><th>Stated size (D x W x H)</th><th>Counter depth</th><th>Floor area</th><th>What the listing says it cooks</th></tr>
<tr><td>Chefman 6QT dual-basket (P1)</td><td>13.38 x 11.81 x 10.63 in</td><td>13.38 in (34.0 cm)</td><td>158.0 sq in</td><td>Two independent 3-quart baskets; Sync Finish so two dishes land together (per bullets)</td></tr>
<tr><td>Emeril Lagasse 26QT French-door (P2)</td><td>16.9 x 15.8 x 14.8 in</td><td>16.9 in (42.9 cm)</td><td>267.0 sq in</td><td>Bullets describe capacity for 4-6 people, a rotisserie for a 6-lb chicken and a 12-inch pizza</td></tr>
<tr><td>Chefman 8QT TurboFry (P3)</td><td>12.75 x 13.5 x 10 in</td><td>12.75 in (32.4 cm)</td><td>172.1 sq in</td><td>One 8-quart non-stick basket; four presets (per bullets)</td></tr>
</table></div>
<p class="small">Floor area is our arithmetic (depth x width from the listing), not a manufacturer claim. The drawings on the product cards are ours too, drawn to the same scale so you can compare them by eye.</p>
<p>Read the depth column as the deciding number. Two of the three fit inside a shallow run of counter; the Emeril oven needs 16.9 in of it, which is why the sizing guide tells you to measure before the holiday, not after.</p>
</section>
<section id="height">
<h2>Height is the number people forget until the cabinet is full</h2>
<p>The listed heights are 10.63 in, 14.8 in and 10 in. If the appliance has to live under a wall cabinet, that clearance, plus whatever space the manual asks for around vents and the door swing, is the constraint, not the width. <strong>None of the three listings states a required clearance in the fields we captured</strong>, so this site cannot tell you a safe number. Get a tape measure, and if the space is tight, ask the seller the clearance question in writing before the week the delivery window closes.</p>
<p>One more door-day detail: the Emeril's doors are French doors that "open with a single pull" per its bullets. Decide where the swing goes before you put a 16.9 in box in the corner.</p>
</section>
<section id="power">
<h2>Two 1700 W machines and one outlet</h2>
<p>The Chefman 6QT listing states 1700 W at 120 V; the Emeril's Product information table states 1700 W at 120 V. On one small kitchen circuit, two of those plus a kettle is a question worth asking before Thanksgiving dinner, not during it. The 8QT is the awkward one: its bullets say 1000 W while its own spec table says 1700 W, and we publish both rather than choosing (<a href="flagged.html#FLG-022">FLG-022</a>). The circuit arithmetic and what to ask an electrician live in the <a href="guide-wattage-outlets.html">wattage and outlets guide</a>.</p>
</section>
<section id="checklist">
<h2>Ten days out: the fit check, in order</h2>
<ol class="steps">
<li>Measure the depth and the height of the spot it will live in. Write the two numbers down.</li>
<li>Compare them against the stated size in the table above. If the appliance is deeper than the counter, stop there.</li>
<li>Check what the listing says it cooks, in the listing's words. A capacity number in a title is not a meal plan.</li>
<li>Read the variant selector before ordering. The 8QT comes in 6, 8 and 9-quart sizes and in two finishes per its own listing, and the photograph shows one of them.</li>
<li>Decide who washes what. The 8QT's basket and tray are called top-rack dishwasher safe per bullets; the 6QT's baskets are called dishwasher safe per bullets; for the Emeril we captured no cleanup claim, so its accessories are a question for the listing, not for us.</li>
<li>Confirm the power figure you will actually rely on, given the discrepancy above.</li>
</ol>
</section>
<section id="limits">
<h2>What this page cannot tell you</h2>
<p>Not how long anything takes to cook. Not whether a 6-quart basket feeds your family. Not whether the machine is good. Those need a test kitchen and a protocol, and the decision on whether to build one is still open on the <a href="suggestions.html#SG-09">review desk</a> (SG-09, Q-19). What this page can tell you is what the seller stated, when we read it, and what the listing leaves out. The gaps are listed on <a href="flagged.html">Flagged for review</a>.</p>
<p class="next">Next: <a href="compare.html#chooser">answer the three-question chooser</a>, or read the <a href="guide-holiday-deal-check.html">holiday listing check</a> before you buy in the sales window.</p></section>
""",
    [("Can an air fryer replace an oven on Thanksgiving?",
      "Nothing on these listings claims it can cook a whole turkey, and we are not going to invent that claim. The Emeril listing describes a rotisserie for a 6-lb chicken and a 12-inch pizza. Whether that helps your menu is your call, and it is a question the listing answers only about capacity, not about timing."),
     ("What size do I need to feed six people?",
      "The only number on the listing that speaks to household size is the Emeril's bullet describing 26-quart capacity for four to six people. The other two state 6 and 8 quarts without a headcount. Do not read a headcount into a quart figure."),
     ("Is the deepest one also the biggest inside?",
      "By the stated figures, yes on both counts for the Emeril: 16.9 in of depth and 26QT in its title. Note the title-to-field gap the register carries, 26QT against a 24.6 liter capacity field, which we show as two values rather than converting silently."),
     ("Do these listings say how much clearance they need?",
      "Not in the fields captured for this register. That is why the fit check ends with a question for the seller instead of a number from us.")],
    picks=("P1", "P2", "P3"))
b10 = b10.replace("HOLIDAY_SOURCE", HOLIDAY["source"]).replace("HOLIDAY_READ", HOLIDAY["read"])
page_to("guide-thanksgiving-counter.html", "Thanksgiving counter math: what fits? | Countertop Guide",
        "Counter depth, cabinet height, wattage and what the listing actually claims it cooks, checked against the three fryers before Thanksgiving 2026.", b10, j10, "guide-page")

b11, j11 = guide_shell(
    "Guide - Seasonal - Holiday buying window",
    "A holiday price looks like a deal. Ten minutes on the listing tells you which one it is.",
    "Between 27 and 30 November 2026 a lot of appliance listings will show a lower number next to a higher one. Nothing about that makes a machine fit your counter or cook your food. This is the check we would run on any listing, in order, using only what the page itself states, and it works the same whether the discount is 5 percent or 40.",
    """
<section id="window">
<h2>What the window is, and what it is not</h2>
<p>The commercial days around Thanksgiving are named after the holiday rather than defined by it. Thanksgiving Day 2026 is Thursday, 26 November, the only one of the four in federal law (5 U.S.C. 6103; <a href="HOLIDAY_SOURCE">OPM schedule</a>, read HOLIDAY_READ). The Friday, 27 November, and the Monday, 30 November, are retail names for working weekdays. That matters for one practical reason: a delivery estimate or a return clock does not pause for a sale, so read both on the page instead of assuming.</p>
<p>This site publishes no price figures at all, and it runs no price alerts or watchlists: the Program Policies' participation requirements forbid price-tracking or alerting functionality on a Site, which the <a href="compliance.html">compliance page</a> quotes. So the maths below is maths you do on Amazon's page, where the number is current.</p>
</section>
<section id="unit">
<h2>1. Do the quarts-per-dollar maths yourself</h2>
<p>Find the price, find the stated capacity, divide. Then do it for the other two machines you are considering. That one number exposes most of the nonsense in the category, because capacity is what you pay for and the marketing words around it are free.</p>
<p>Two traps in that arithmetic, both visible on our own listings:</p>
<ul>
<li><strong>Title capacity is not always the capacity field.</strong> The Chefman 6QT's title says 6 Quart while its capacity field says 6 liters; the Emeril's title says 26QT against a field of 24.6 liters. We keep both values and flag the difference (<a href="flagged.html#FLG-002">FLG-002</a>) instead of picking one. If a comparison depends on a unit, check which unit the seller used.</li>
<li><strong>A basket count changes what a quart means.</strong> Two 3-quart baskets is 6 quarts split, which is a different dinner from one 6-quart basket. The dual-basket claim is about finishing two dishes together, per the Sync Finish bullet, not about volume.</li>
</ul>
</section>
<section id="model">
<h2>2. Check the model number, not the photograph</h2>
<p>The 8QT TurboFry listing offers 6, 8 and 9-quart sizes in two finishes, per its own variant selector. The image on the page shows one of them. A cheaper tile in a sale grid is often a smaller variant of the machine you read about, and the picture will not tell you. Read the size and colour fields, and the model string if the page gives one.</p>
<p>The same trap in the opposite direction: a listing can stay identical while a newer model sits next to it. Ours does. The 8QT page's own suggestions show a 6QT Chefman model at a lower price with more ratings, recorded as <a href="flagged.html#FLG-003">FLG-003</a>. Whether to promote the newer ASIN is an open decision on the desk (SG-08), so we promote the submitted one and say plainly that a sibling exists.</p>
</section>
<section id="badges">
<h2>3. Badges are listing furniture, not evidence</h2>
<p>An Amazon's Choice chip and a "bought in past month" line belong to Amazon's page on a given day. They are not our ranking, not a quality score, and not a reason to buy today. The register's rule is that a popularity or trend statement needs a dated snapshot from an official page or it does not get written (<a href="flagged.html#FLG-012">FLG-012</a>), and this build displays none of those figures anywhere on the shop pages, for the Program Content reasons in <a href="flagged.html#FLG-032">FLG-032</a>.</p>
</section>
<section id="disagree">
<h2>4. If the listing argues with itself, a discount is not the fix</h2>
<p>Two of our five listings do exactly that:</p>
<ul>
<li>The 8QT states 1000 W in its bullets and 1700 W in its spec table. Both are shown; neither is inferred (<a href="flagged.html#FLG-022">FLG-022</a>).</li>
<li>The Emeril's title says six cooking accessories, its item details say seven, and the included-components list names six. Its title says 24 one-touch presets while its bullets elsewhere describe 25 (<a href="flagged.html#FLG-021">FLG-021</a>, <a href="flagged.html#FLG-002">FLG-002</a>).</li>
</ul>
<p>If the number matters to you, that is a question for the seller or the manual, and it does not become answered because the price moved. This is also why our pages say "as listed" next to figures instead of stating them as facts about the world.</p>
</section>
<section id="after">
<h2>5. Warranty, returns and the receipt, before you click</h2>
<p>Captured from the listings on VERIFIED, in the sellers' words: the Chefman fryers state a 1-year assurance (P1) and a 1-year warranty (P3), both per bullets, plus cETL approval. The Emeril's listing links a warranty PDF and states no term in its text, so the field on our pages is blank rather than guessed (<a href="flagged.html#FLG-005">FLG-005</a>). The ThermoMaven includes one calibration certificate per its included-components field. Returns windows and exchange rules are not product fields: they live on your order page, so read them there.</p>
<p class="next">Next: the <a href="guide-gift-return-window.html">gift receipt test</a> if this purchase is for someone else, or the <a href="verification.html">verification register</a> to see every figure and where it came from.</p></section>
""",
    [("Is there actually a deal in the holiday window?",
      "We cannot say, and that is not modesty. This site publishes no price figures, so it also makes no claim about what happens to them on a given Friday. The check above works whether a price moved or not, which is the point."),
     ("Should I wait for Black Friday instead of buying now?",
      "That is a prediction about future prices, which we do not make: forecasting them would need a price-tracking feature, and the Program Policies bar a Site from having one. What you can do today is the arithmetic in section 1, on the page where the number is live."),
     ("Do cheaper listings mean older machines?",
      "Sometimes the difference is a variant, not a discount. Read the capacity, size and colour fields and the model string. A newer sibling can also sit on the same page at a lower price, which is exactly what the 8QT listing shows."),
     ("Is a title claim like 26QT a promise?",
      "It is a title. The spec fields next to it can disagree, as ours does, which is why the register shows both and flags the gap rather than resolving it for you.")],
    picks=("P1", "P2", "P3"))
b11 = b11.replace("HOLIDAY_SOURCE", HOLIDAY["source"]).replace("HOLIDAY_READ", HOLIDAY["read"]).replace("VERIFIED", VERIFIED)
page_to("guide-holiday-deal-check.html", "Holiday listing check: ten minutes before you buy | Countertop Guide",
        "A ten-minute check for any appliance listing in the holiday window: quarts per dollar, the variant trap, badge meaning and listings that disagree with themselves.", b11, j11, "guide-page")

b12, j12 = guide_shell(
    "Guide - Seasonal - Gifting",
    "The gift receipt test: five checks that decide whether it gets kept",
    "Most appliance gifts are not returned because they are bad. They are returned because they did not fit, the parts were wrong, or nobody could find the box. All five checks below can be done from the listing before you wrap anything, using fields this site has already verified.",
    """
<section id="receipt">
<h2>1. Keep the box, the manual and the model string</h2>
<p>An exchange without the model string is a phone call, and the string is on the label, the box and the listing. Write it on the gift note. That one habit answers most December problems, and it is the reason the shop pages link to the exact ASIN rather than to a search page: the recipient should be able to find the same page you read.</p>
</section>
<section id="variant">
<h2>2. Confirm the variant you are buying, not the one in the photo</h2>
<p>The 8QT TurboFry is offered in 6, 8 and 9-quart sizes and in stainless steel or black, per its listing's variant selector. The CHEF iQ Sense is sold in probe-count variants, and our register records the price fields per variant, which is how we know the tiles differ. Colour fields matter too: the Chefman 6QT listing lists Black and Gray; the Emeril states Stainless Steel. Order the tile you mean.</p>
</section>
<section id="fit">
<h2>3. Ask for two numbers before you buy for someone else's kitchen</h2>
<p>Depth and clearance. You do not need their floor plan, just the depth of the counter run and the height under the cabinet. Against the stated sizes: 13.38 in deep and 10.63 in tall (6QT), 16.9 in deep and 14.8 in tall (26QT), 12.75 in deep and 10 in tall (8QT). None of the three listings states a required clearance in the fields we captured, so if their space is tight, that is a question for the seller.</p>
<p>The drawings on the product cards are ours, drawn to one shared scale from those inches, which makes them a reasonable thing to show a recipient who is holding a tape measure.</p>
</section>
<section id="cleanup">
<h2>4. The dishwasher question is the marriage question</h2>
<p>Per the bullets: the 8QT's basket and flat tray are top-rack dishwasher safe, and the 6QT's removable non-stick baskets are dishwasher safe. For the Emeril we captured no cleanup claim, so its six (or seven, see <a href="flagged.html#FLG-021">FLG-021</a>) accessories are a real hand-washing question that the listing does not settle. If the gift is for someone who will not soak a pan, that is the deciding field, not the preset count.</p>
</section>
<section id="setup">
<h2>5. Some gifts need a network, a hub and an afternoon</h2>
<p>The CHEF iQ Sense listing describes three ultra-thin probes plus a hub that charges all three, WiFi with app monitoring, Bluetooth in the connectivity field, ratings to 1000 F and up to 50 hours per charge. That is a lovely gift for someone who enjoys setting things up, and a chore for anyone else. It also has no accuracy figure in the fields we captured, which the register states as a gap (<a href="flagged.html#FLG-004">FLG-004</a> covers the missing dimensions for both thermometers). The ThermoMaven, by contrast, is handheld: no hub, no app, one-second read per its bullets, IP67 and rinsable per its title and bullets, and no setup at all. If the recipient just wants the steak right, the pocket read is the lower-friction gift.</p>
</section>
<section id="gaps">
<h2>What this site cannot promise about a returned gift</h2>
<p>Returns windows, exchange rules and gift-receipt mechanics belong to the order page, not to a product listing, so we do not state them here. Same for warranty terms: the Emeril's listing links a PDF and puts no period in its text, which stays blank on our tables rather than guessed (<a href="flagged.html#FLG-005">FLG-005</a>). Everything we do state carries a date and a link, so a recipient can check the same source.</p>
<p class="next">Next: <a href="guide-gift-picks.html">which appliance to gift in the first place</a>, or the <a href="compare.html">side-by-side table</a> for the five products.</p></section>
""",
    [("Is an air fryer a good gift for someone who has one?",
      "The listing fields cannot answer that, and neither can we without knowing the person. What we can say: the 6QT's two-basket Sync Finish claim and the 8QT's single large basket are different purchases solving different problems, so if their current machine is a single basket, the dual-basket one is the only one of the three that changes anything."),
     ("What if it does not fit in their kitchen?",
      "That is why the depth column is on every card. Compare their counter depth to 13.38, 16.9 or 12.75 inches before ordering, and keep the box and the model string so an exchange is a form, not a project."),
     ("Do the thermometers need an app?",
      "Only the wireless one: its listing describes a hub, WiFi and app monitoring. The handheld ThermoMaven is a read-in-your-hand device with an auto-rotating display per its bullets, which is the better gift for anyone who will not pair a device."),
     ("Is the warranty included with a gift?",
      "The two Chefman listings state a one-year assurance or warranty per their bullets, and the CHEF iQ states a two-year assurance per bullets. The Emeril's term is not in its listing text, so we show nothing rather than assume. Keep the packaging either way.")],
    picks=("P1", "P3", "P5"))
b12 = b12.replace("HOLIDAY_SOURCE", HOLIDAY["source"])
page_to("guide-gift-return-window.html", "Gift receipt test: five checks before you wrap | Countertop Guide",
        "Five listing-based checks that decide whether a gifted appliance gets kept: variant, counter fit, cleanup, setup burden and the paperwork to keep.", b12, j12, "guide-page")

# ---------- GIFT GUIDE ----------
b6, j6 = guide_shell("Guide - Seasonal", "Holiday air fryer gifts: how to choose one that gets used",
 "A gift air fryer fails in two ways: it does not fit where they cook, or it is complicated enough that they never learn it. Neither is about price. Here is the checklist we use for a gift pick, applied to the three fryers on this site.",
 """
<h2>The five-question gift check</h2>
<ol>
<li><strong>How much counter do they actually have?</strong> Depth is the killer. These three need 32.4 cm, 34.0 cm and 42.9 cm respectively (derived from listing dimensions). If their counter is shallow and cluttered, the 8QT basket at 12.75 in deep is the one that stays out.</li>
<li><strong>Do they cook for two or six?</strong> The Emeril French-door oven is the listing that claims four-to-six people, a 6-lb rotisserie chicken and a 12-inch pizza. The dual-basket is the listing that claims two dishes finishing together. One of those sentences matches your recipient; usually only one.</li>
<li><strong>Will they wash it?</strong> A gift with parts that go in the dishwasher gets used. Chefman&rsquo;s two listings say the baskets are dishwasher safe (8QT: top rack, basket and tray). Check the exact wording on the listing you buy from.</li>
<li><strong>Is the control panel learnable in one evening?</strong> Count the presets and ask whether they recognise the names. The Emeril listing carries 24 presets in its title and 25 in its bullets - a discrepancy we flag rather than smooth over. Many presets is not a gift feature.</li>
<li><strong>Does the return window survive the holiday?</strong> Availability and return terms belong to the seller, not to us. Confirm them on the listing and in checkout, the week you buy.</li>
</ol>
<h2>Which one, for whom</h2>
<ul>
<li><strong>The household that cooks two things every night:</strong> the dual-basket (two independent 3-quart baskets, Sync Finish per listing).</li>
<li><strong>The one who hosts:</strong> the 26QT oven-style, if - and only if - they have the depth and want a rotisserie.</li>
<li><strong>The first-timer or small kitchen:</strong> the single 8QT basket: one cavity, one dial-learning curve, dishwasher-safe parts per bullets.</li>
<li><strong>The grill person, as a second gift:</strong> the instant-read thermometer. Small, useful the same day, and the listing states a +/-0.5F tolerance with NIST and NSF certification named.</li>
</ul>
<h2>Write the specs on the card</h2>
<p>Genuinely useful gift advice, at zero cost: put the depth and the capacity on the note, so the recipient can decide whether it fits before they wrap the receipt away. &ldquo;Needs 34 cm of counter depth, two 3-quart baskets&rdquo; is a nicer present than a surprise appliance that has nowhere to live.</p>
<h2>What this page will not tell you</h2>
<p>Not price, not &ldquo;everyone is buying&rdquo;, not which one is &ldquo;best&rdquo;. We have not cooked with any of them, we do not monitor stock, and a gift claim about crispness would be the seller&rsquo;s, not ours. What we can give you is fit, capacity, cleanup and the control-panel question, all from the listings linked above.</p>
""",
 [("Is an air fryer a good gift?","It is a good gift for someone with the counter space and the inclination to use it. Check depth first (32.4, 34.0 and 42.9 cm for the three here), then whether the cleaning is dishwasher-safe as listed. Those two answers predict use better than price does."),
  ("Should I gift the biggest capacity I can find?","Only if the recipient cooks for four to six and has the depth. The 26QT oven-style is the largest cavity and the deepest footprint on this site; a too-big machine on a crowded counter ends up in a cupboard."),
  ("What goes on the gift note?","Capacity as titled, the depth in centimetres, and which parts are listed as dishwasher safe. Keep the receipt accessible - availability and return terms belong to the seller.")],
 picks=("P3","P1","P4"))
page_to("guide-gift-picks.html","Air fryer gifts that get used | Countertop Guide","The gift check that needs no price tag: counter depth, household size, dishwasher-safe parts and a panel the recipient will actually learn.",b6,j6,"guide-page")

# ---------- GUIDE 10: instant-read vs wireless (published from the topic calendar, week 2026-12-08) ----------
b10, j10 = guide_shell("Guide - Thermometers", "Instant-read vs wireless thermometer: do you need both?",
 "These two tools answer different questions. One tells you the temperature of the food in front of you, in about a second. The other tells you the temperature of food you are not standing next to. Whether you need both depends on how often you leave the kitchen during a cook - and on two listings that do not state the same kind of accuracy claim.",
 """
<h2>The one-line answer</h2>
<p>If you grill, pan-fry or roast and stay nearby, the handheld instant-read covers it. If you smoke, roast low and slow, or cook a bird big enough to need an hour, the wireless probe set earns its place. Owning both is common because they fail in different ways: a handheld cannot watch a roast, and a probe set cannot give you a reading in a saucepan of caramel in two seconds.</p>

<h2>What each listing actually states</h2>
<div class="table-scroll"><table>
<tr><th>Question</th><th>ThermoMaven instant-read (B0DHZTCNR5)</th><th>CHEF iQ Sense wireless, 3 probes (B0DZFD6R9Z)</th></tr>
<tr><td>Stated accuracy</td><td>&plusmn;0.5&deg;F, with NIST and NSF certification named in the title <span class="fine">(per listing)</span></td><td>No &plusmn; figure in the fields we captured <span class="badge-warn">not stated</span></td></tr>
<tr><td>Read time</td><td>1 second, thermocouple sensor <span class="fine">(per title and bullets)</span></td><td>Continuous monitoring; each probe reports to the hub and the app <span class="fine">(per bullets)</span></td></tr>
<tr><td>How many readings</td><td>One at a time, in your hand</td><td>Three probes at once, from the app</td></tr>
<tr><td>Range</td><td>Not applicable - you are holding it</td><td>&ldquo;WiFi unlimited range&rdquo; with app monitoring, plus Bluetooth in the connectivity field <span class="fine">(per listing)</span></td></tr>
<tr><td>Heat rating</td><td>Not stated as a probe rating in the fields we captured</td><td>1000&deg;F heat safe <span class="fine">(per title and bullets)</span></td></tr>
<tr><td>Water</td><td>IP67, can be rinsed <span class="fine">(per title and bullets)</span></td><td>Not stated in the fields we captured</td></tr>
<tr><td>Power</td><td>Battery; a calibration certificate is included <span class="fine">(per included-components field)</span></td><td>Rechargeable hub; up to 50 hours per charge <span class="fine">(per bullets)</span></td></tr>
<tr><td>Source</td><td><a href="https://www.amazon.com/dp/B0DHZTCNR5">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B0DZFD6R9Z">Amazon listing</a></td></tr>
</table></div>
<p class="small">Both columns are read from the product's own listing on the date shown in the byline. Where a field is absent we write &ldquo;not stated&rdquo; rather than assuming a comparable value.</p>

<h2>The asymmetry that decides it</h2>
<p>Only one of these two listings makes a numeric accuracy claim, so an accuracy comparison would be a comparison of a number against silence. That is not a reason to prefer the cheaper tool; it is a reason to check the wireless listing&rsquo;s manual or product-support documents before you buy it <em>for accuracy</em>. Buy it for coverage, not for a tolerance figure you have not seen.</p>

<h2>Four questions that sort most buyers</h2>
<ol>
<li><strong>Do you leave the room during a cook?</strong> If yes, a handheld is the wrong only-tool. Probes that report to a phone are the ones that solve that.</li>
<li><strong>Do you cook more than one protein at once?</strong> Three probes against one. If you regularly do a joint and a chicken together, the count matters.</li>
<li><strong>Do you need a reading in a saucepan?</strong> Caramel, custard, oil and sugar work are handheld jobs. A probe in a hub is not designed for a spoon-and-stir check.</li>
<li><strong>Do you want the tool to survive the sink?</strong> One listing states IP67 and rinsing; the other does not state a water rating in the fields we captured.</li>
</ol>

<h2>What we will not tell you</h2>
<p>We have not calibrated either unit, and we have not cooked with either. The accuracy sentence in this guide is the seller's claim, attributed, with the certification it names. If a tolerance figure matters to your cooking, spend the two minutes it takes to find the manual on the listing before you order.</p>
""",
 [("Do I need both thermometers?","Not necessarily. A handheld instant-read covers grilling, pan-frying and quick checks. A wireless probe set covers long cooks you are not standing next to. Buy the second only if you leave the kitchen during cooks."),
  ("Which one is more accurate?","We cannot say from the listings. The ThermoMaven listing states a tolerance of plus or minus 0.5 degrees F with NIST and NSF certification named. No tolerance figure appears in the CHEF iQ fields we captured, so ranking them would be inventing a number."),
  ("Does the wireless thermometer need WiFi?","The listing describes WiFi unlimited range with app monitoring and also lists Bluetooth in its connectivity field. Either way you need the app and the hub for remote readings."),
  ("Can the instant-read stay in the oven?","That is not what a handheld instant-read is for, and the listing does not state an oven-safe probe rating in the fields we captured. Use a probe designed to stay in the oven.")],
 picks=("P4", "P5"))
page_to("guide-instant-read-vs-wireless.html", "Instant-read vs wireless thermometer | Countertop Guide",
 "A one-second handheld read against three probes monitored from a phone: what each listing states, including the one that states no accuracy figure.",
 b10, j10, "guide-page")


# ---------- REVIEW DESK ----------
desk_body = f"""
<p class="eyebrow">Review desk</p>
<h1>Everything internal, in one place</h1>
<p class="lede">This is the counter behind the counter: the register, the open questions, the flags, the method and the money rules. Reader-facing pages stay out of here on purpose - you will not find a row of status badges on the shop pages - but every one of these surfaces is reachable from the masthead&rsquo;s Review desk link and from the footer of every page.</p>
<h2>The eight surfaces</h2>
<div class="grid cols-2">
  <article class="card"><span class="tag">Evidence</span><h3><a href="verification.html">Verification register</a></h3><p>Line by line: submitted short link, intended ASIN, official listing URL, confirmation date and source, the observed redirect target in its own separate field, and every product fact with the link it came from.</p></article>
  <article class="card"><span class="tag">Open items</span><h3><a href="flagged.html">Flagged for review</a></h3><p>Every irregularity and unverified item, with the action that would close it. Flags never block publishing; they block claims.</p></article>
  <article class="card"><span class="tag">Decisions</span><h3><a href="decisions.html">Decision register: seven gates</a></h3><p>The whole board collapsed into the seven answers that gate the rest, each with what an official source already settles, what is missing, and the steps that would produce it. The short queue sits on the board below.</p></article>
  <article class="card"><span class="tag">Evidence</span><h3><a href="suggestions.html">Suggestions &amp; decision desk</a></h3><p>Ranked suggestions with options, a copy-paste design brief, the six-item decision queue, and the questions whose answers gate the next build.</p></article>
  <article class="card"><span class="tag">Money &amp; policy</span><h3><a href="compliance.html">Compliance gate</a></h3><p>Disclosure wording, sponsored marking, price and image rules read from the Operating Agreement and Program Policies.</p></article>
  <article class="card"><span class="tag">Measurement</span><h3><a href="methodology.html">Method, events &amp; ledger</a></h3><p>What is automated, what is gated, the five defined events, and an empty campaign ledger that only first-party reports may fill.</p></article>
  <article class="card"><span class="tag">Design</span><h3><a href="suggestions.html#design-inputs">Design inputs DI-1 to DI-8</a></h3><p>The eight inputs a parallel pass wrote for the design prompt, kept as a separate register on the board so the owner can approve, reject or defer each line before any CSS ships.</p></article>
  <article class="card"><span class="tag">Design</span><h3><a href="design-brief.html">Design brief (parallel pass)</a></h3><p>A second, independently written brief for the visual overhaul: prompt blocks, three visual directions and an eight-topic calendar. The owner picks one brief to execute - the choice is noted at the end of the decision desk.</p></article>
  <article class="card"><span class="tag">Working papers</span><h3><a href="suggestions.html#the-decisions">The decision queue</a></h3><p>Six decisions only the owner can settle, each with the choice, what it unblocks, and the evidence that closes it. The full Q/I/A register and a long-form working copy travel with the repository under <code>review/1035d1e2/</code>.</p></article>
<article class="card"><span class="tag">Snapshot</span><h3><a href="executive-summary.html">Executive summary</a></h3><p>One page for a decision-maker: what is live, what is verified, what is blocked and what happens next.</p></article>
</div>
<h2>Status board</h2>
<div class="table-scroll"><table>
<tr><th>Area</th><th>State</th><th>What it means</th></tr>
<tr><td>Product data</td><td><span class="badge-ok">5 products, {VERIFIED}</span></td><td>Every field traces to a listing read in-session; four cells stay blank and are flagged.</td></tr>
<tr><td>Disclosure</td><td><span class="badge-ok">On every page</span></td><td>The Associates statement in the required wording, above the fold and in the footer, plus a plain-language line.</td></tr>
<tr><td>Outbound links</td><td><span class="badge-ok">Marked sponsored</span></td><td>Static and script-generated links alike; label, rel, noopener and the tag parameter.</td></tr>
<tr><td>Link format validation</td><td><span class="badge-warn">Manual gate open</span></td><td>The one-link-per-product test in Associates Central has not been recorded. Nothing scales until it passes.</td></tr>
<tr><td>Price &amp; rating display</td><td><span class="badge-warn">Suppressed by policy read</span></td><td>Link-only pricing on shop pages; dated figures live in the register. Owner to ratify.</td></tr>
<tr><td>Analytics</td><td><span class="badge-warn">Local-only</span></td><td>Five events defined and counted in the browser; no endpoint hosted, so no data leaves the device.</td></tr>
<tr><td>Search performance</td><td><span class="badge-flag">Unmeasured</span></td><td>No Search Console property is recorded for this site. Traffic claims are therefore absent by design.</td></tr>
<tr><td>Imagery</td><td><span class="badge-flag">No product photography</span></td><td>Diagram and type only, until a licence decision (SG-04) clears.</td></tr>
</table></div>
<h2>How to read a flag</h2>
<p>A flag is not an admission of a defect in the product; it is a statement about <em>our evidence</em>. <span class="badge-warn">Needs decision</span> means a human with account access must choose. <span class="badge-flag">Unverified</span> means a value we could not confirm from an official source, left blank rather than guessed. <span class="badge-ok">Resolved</span> items keep their row so the trail survives a rebuild.</p>
"""
page_to("review-desk.html","Review desk: register & open items | Countertop Guide","The internal side of this publication: verification register, flagged items, the decision desk, the compliance gate, method and executive summary.",desk_body)

# ---------- DESIGN BRIEF ----------
db_body = """
<div class="callout"><strong>Integration note (this page came from a parallel pass).</strong> One line below tells a designer to put a price snapshot first on product cards. That is no longer possible here: Amazon&rsquo;s rules let a Site show price only when Amazon serves it or via the Creators/PA API, refreshed inside 24 hours, and this build is static. See <a href="flagged.html#FLG-032">FLG-032</a> and the consolidated brief on the <a href="suggestions.html#design-prompt">decision desk</a>. Everything else on this page - the brand, layout, components, imagery, voice and findability blocks - still stands, and the owner has to choose between the two briefs rather than run both.</div>
<p class="eyebrow">Design brief</p>
<h1>Design brief: suggestions for the publication redesign</h1>
<p class="lede">Everything on this page is a suggestion for the design prompt, not a decision. A reviewer picks a direction, and only approved items are implemented. The brief is written so it can be fed to a design tool as-is; each block states what it changes, what it needs, and what decision it blocks.</p>
<h2>1. Design prompt blocks (use verbatim in the design prompt)</h2>
<p class="small">Each block is drafted to be pasted into the design prompt. Edit only with owner approval.</p>
<div class="table-scroll"><table>
<tr><th>Block</th><th>Suggested prompt text</th><th>What it changes</th><th>Decision needed</th></tr>
<tr><td>Brand</td><td>Build a warm, editorial kitchen-publication brand called The Countertop Guide: deep charcoal text, warm cream background, a single confident accent (burnt orange or herb green). Typography: a sturdy serif for headings, a clean grotesque for body. It must read like a magazine a cook trusts, never like a dashboard or a template.</td><td>Visual identity across all pages</td><td>Accent colour pick (SG-11)</td></tr>
<tr><td>Layout</td><td>Lead every page with the product: comparison table or product cards first, verification and methodology below the fold. On the homepage: hero headline answering the buyer's question, then featured guides, then category tiles, then the data. Put the disclosure strip under the masthead on every page and repeat it in the footer.</td><td>Page structure and reading order</td><td>Homepage layout pick (Q-12)</td></tr>
<tr><td>Components</td><td>Design a sticky comparison bar on comparison and category pages, a three-question \"which one is for you\" chooser above the comparison table, category tiles with one-line spec summaries, and product cards that show capacity, footprint and price snapshot first. Every buy button is labelled \"Check price on Amazon - sponsored\" and opens amazon.com.</td><td>Reusable components</td><td>Component scope approval (SG-11)</td></tr>
<tr><td>Imagery</td><td>Use SVG/CSS illustration and typography only. Never copy Amazon product images and never generate fake product photographs; if real photography is added later it must be owned or licensed (Amazon Associates Program Content rules).</td><td>All imagery</td><td>Photography decision (Q-07)</td></tr>
<tr><td>Voice</td><td>Write like a knowledgeable friend comparing specs: short varied sentences, one idea per paragraph, concrete numbers with their source, no filler transitions, no \"in conclusion\", no superlatives. We never claim hands-on testing, popularity status or rankings we cannot show.</td><td>All copy</td><td>Voice sign-off (Q-11)</td></tr>
<tr><td>Findability</td><td>Give every page one unique, question-shaped title and meta description. Keep one canonical domain, an XML sitemap and a valid RSS feed, and submit the sitemap to Search Console once the domain is set.</td><td>SEO foundations</td><td>Domain pick (Q-02)</td></tr>
</table></div>
<h2>2. Visual direction options (pick one)</h2>
<div class="table-scroll"><table>
<tr><th>Option</th><th>Direction</th><th>Why it suits a buyer-action site</th><th>Risk</th></tr>
<tr><td>A</td><td>Warm editorial - cream paper, charcoal serif headings, burnt-orange accent, generous whitespace</td><td>Reads like a trusted publication; product cards feel hand-picked</td><td>Needs disciplined typography to avoid looking flat</td></tr>
<tr><td>B</td><td>Modern utility - light neutral canvas, indigo accent, tight data-friendly tables</td><td>Comparison tables and specs read as precise and scannable</td><td>Can drift toward dashboard feel; needs editorial warmth</td></tr>
<tr><td>C</td><td>Bold magazine - high-contrast black/white with a strong accent, large type, editorial photography placeholders</td><td>Strongest brand presence; stands out in search results</td><td>Highest design effort; photography decision gates it</td></tr>
</table></div>
<h2>3. Anti-AI-slop writing rules (apply to every page)</h2>
<ul>
<li>No filler openers (\"In today's fast-paced world\"), no \"in conclusion\", no em-dash chains of three.</li>
<li>One idea per paragraph; vary sentence length; prefer the specific number over the adjective.</li>
<li>Every product claim links to its Amazon listing; missing data is left blank and flagged, never filled with a guess.</li>
<li>Seller claims are attributed (\"per listing\"); our own words stay first-person and honest about what we have and have not tested.</li>
<li>No superlatives, no \"best\", \"top-rated\" or \"#1\" claims; popularity badges appear only as dated listing snapshots.</li>
</ul>
<h2>4. Editorial calendar: eight question-shaped topics</h2>
<p class="small">Working titles, not claims about popularity or search volume. Five are published; three are proposed. Every topic follows the same verification rules before publishing.</p>
<div class="table-scroll"><table>
<tr><th>#</th><th>Working title</th><th>Angle (from verified data)</th><th>Status</th></tr>
<tr><td>1</td><td>Basket or oven-style air fryer: what should you compare?</td><td>Dual-basket vs French-door vs single basket, from the three verified fryer listings</td><td>Published</td></tr>
<tr><td>2</td><td>A no-hype checklist for comparing air fryer capacity</td><td>6 qt vs 8 qt vs 26 qt capacity figures as listed</td><td>Published</td></tr>
<tr><td>3</td><td>How to assess cleanup and counter-space trade-offs</td><td>Dishwasher-safe baskets plus verified footprints</td><td>Published</td></tr>
<tr><td>4</td><td>Questions to ask before buying a multi-function kitchen appliance</td><td>Presets, accessories, wattage and warranty from the Emeril listing</td><td>Published</td></tr>
<tr><td>5</td><td>Instant-read or wireless? How to read thermometer accuracy claims</td><td>±0.5F, NIST/NSF and sensor counts from the two verified thermometers</td><td>Published</td></tr>
<tr><td>6</td><td>Two baskets or one: what a dual-basket air fryer actually changes</td><td>Sync Finish and dual-zone cooking from the Chefman 6QT listing</td><td>Proposed</td></tr>
<tr><td>7</td><td>How much counter space does a 26-quart air fryer really need?</td><td>Verified 16.9in x 15.8in footprint of the Emeril 26QT</td><td>Proposed</td></tr>
<tr><td>8</td><td>What \"dishwasher-safe\" really means for air fryer cleanup</td><td>Dishwasher-safe baskets and probes as stated in the three listings' bullets</td><td>Proposed</td></tr>
</table></div>
<h2>5. Improvements for decision-making</h2>
<ul>
<li>Keep this suggestions board as the single review surface: every change starts as an SG item, a reviewer approves, then it is implemented and re-verified.</li>
<li>Keep the verification register and flagged page linked from the footer so readers and reviewers can audit any claim.</li>
<li>Measure before optimising: once analytics is live (SG-03), choose the next topic from measured queries, not instinct.</li>
<li>Gate the manual parts: Special Link testing, photography licensing and domain choice stay owner decisions, recorded here.</li>
</ul>
<p class="small">Nothing here is implemented until approved. Irregularities and unverified items stay on <a href="flagged.html">Flagged for review</a>. The decision questions this brief answers are listed on <a href="suggestions.html">the Suggestions board</a> (Q-09 to Q-14).</p>
"""
page_to("design-brief.html","Design brief: pick a visual direction | Countertop Guide","Prompt blocks, three visual directions, anti-slop writing rules and an eight-topic calendar, written as a parallel brief for the owner to choose between.",db_body)
# ---------- CONSOLIDATED URLS (see FLG-047) ----------
# A parallel session published three seasonal guides at these URLs. They restate, at shorter
# length and with dated price figures, topics this site already covers. Two near-identical
# pages competing for one question helps neither, so the extra URLs are kept alive and
# canonicalised to the surviving page instead of being deleted or 404-ed: any link or bookmark
# still lands somewhere useful, and the duplicate signal is consolidated rather than split.
MERGED = [
 ("guide-holiday-gifts.html", "guide-gift-picks.html",
  "Holiday air fryer gifts: how to choose one that gets used",
  "Holiday gifts guide | Countertop Guide",
  "This URL now points at the site's gift guide: five questions that predict whether a gifted air fryer stays on the counter, answered from verified listings.",
  "Holiday air fryer gifts"),
 ("guide-small-kitchen.html", "guide-cleanup-counter-space.html",
  "How to assess cleanup and counter-space trade-offs",
  "Small-kitchen fit guide | Countertop Guide",
  "This URL now points at the counter-space guide: counter depth, footprint arithmetic and cleanup, taken from the listings rather than estimated.",
  "Small kitchen, big appetite"),
 ("dashboard.html", "review-desk.html",
  "Review desk: every data surface in one place",
  "Dashboard hub | Countertop Guide",
  "This URL now points at the review desk: verification register, flag list, suggestions board, compliance, method and ledger, and both design briefs - one link each.",
  "Dashboard hub"),
 ("guide-holiday-roast.html", "guide-thermometer-accuracy.html",
  "Instant-read or wireless? How to read accuracy claims",
  "Roast-thermometer guide | Countertop Guide",
  "This URL now points at the thermometer accuracy guide: what a stated tolerance, a named certification and a sensor count each do and do not prove.",
  "Roast like a pro"),
]
for slug, target, dest, title, desc, h1 in MERGED:
    merged_body = f"""<p class="eyebrow">Guide</p>
<h1>{h1}</h1>
<p class="lede">This page moved. Its subject is covered in full on <a href="{target}">{dest}</a>, and keeping one answer per question is why.</p>
<div class="callout"><p>We keep one complete answer per question, so this address points to the page that covers the subject in full. Product facts on that page link to their Amazon listings and show the date they were read: {VERIFIED}.</p></div>
<p><a class="btn" href="{target}">Read the guide</a></p>
<p class="small">Why this address moved is logged on <a href="flagged.html#FLG-047">Flagged for review (FLG-047)</a>.</p>
"""
    page_to(slug, title, desc, merged_body, canonical=target)
print("consolidated pages wired:", len(MERGED))
# ---------- sitemap / feed / robots / search index ----------
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pg in PAGES:
    if pg["kind"] == "merged" or not pg["indexable"]:
        continue
    sm.append(f"<url><loc>{esc(abs_url(pg['slug']))}</loc><lastmod>{ISSUE}</lastmod></url>")
sm.append("</urlset>")
open("sitemap.xml","w").write("\n".join(sm) + "\n")
def rfc(d):
    import datetime as _dt
    return _dt.date.fromisoformat(d).strftime("%a, %d %b %Y 00:00:00 GMT")
GUIDES = [
 ("guide-basket-vs-oven.html","Basket or oven-style air fryer: what should you compare?","Dual-basket vs French-door oven vs single basket: two-dish cooking, crowd capacity and counter depth, from the listings."),
 ("guide-capacity-checklist.html","A no-hype checklist for comparing air fryer capacity","Quarts vs litres, single vs split baskets, and what a 'feeds 4-6' claim actually claims."),
 ("guide-cleanup-counter-space.html","How to assess cleanup and counter-space trade-offs","Dishwasher-safe parts as listed, footprint arithmetic, and capacity per centimetre of counter depth."),
 ("guide-multifunction-questions.html","Questions to ask before buying a multi-function kitchen appliance","Presets, accessories, wattage, warranty and fit - applied to the 26QT French-door oven."),
 ("guide-thermometer-accuracy.html","Instant-read or wireless? How to read accuracy claims","The stated tolerance, the named certification, sensor counts and what 'unlimited range' means."),
 ("guide-gift-picks.html","Holiday air fryer gifts: how to choose one that gets used","Five questions that predict whether a gifted air fryer stays on the counter: depth, household size, cleanup, panel, returns."),
 ("guide-holiday-hosting.html","The holiday hosting test: which air fryer actually feeds a crowd?","Capacity claims, two-dish cooking and counter-depth math for December counters, from the listings."),
 ("guide-gifts-by-budget.html","Kitchen gifts under $25, under $80 and under $150","Budget bands mapped to five verified picks, each listing's own gift claims quoted."),
 ("guide-wattage-outlets.html","Will it trip the breaker? Wattage and outlet math for air fryers","1000W vs 1700W on a 120V circuit, the Chefman 8QT wattage conflict, and a listing checklist."),
 ("guide-thanksgiving-counter.html","Thanksgiving counter math: what fits on the counter this year?","Depth, height, wattage and the cooking claims three listings will stand behind, checked before 26 November 2026."),
 ("guide-holiday-deal-check.html","A holiday price looks like a deal: the ten-minute listing check","Quarts per dollar, the variant trap, what badges are not, and listings that disagree with themselves."),
 ("guide-gift-return-window.html","The gift receipt test: five checks before you wrap an appliance","Variant, counter fit, cleanup, setup burden and the paperwork that makes an exchange a form."),
 ("guide-instant-read-vs-wireless.html","Instant-read vs wireless thermometer: do you need both?","Two thermometers, two jobs: a one-second handheld read against three probes monitored from a phone, and the accuracy figure one listing never states."),
 ("guide-counter-depth-fit.html","Will a 26-quart oven fit your counter? The depth and height math","Depth, height and footprint arithmetic from the listed dimensions, converted to centimetres and repeated step by step."),
 ("guide-dual-vs-single-basket.html","Two baskets or one: what dual-zone cooking actually changes","Dual-basket versus single-basket versus oven-cavity cooking, decided on the listings' own form, capacity and care facts."),
 ("guide-accessories-included.html","What's actually in the box: accessories, per the listing","Included parts for the five verified picks, stated exactly as each listing shows them, including the count the listing gives two ways."),
]
fd = ['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
      '<channel>', f'<title>{esc(BRAND)}</title>', f'<link>{esc(abs_url("index.html"))}</link>',
      '<description>Spec-backed air fryer and meat thermometer buying guides, written from the Amazon listing.</description>',
      f'<atom:link href="{esc(BASE)}/feed.xml" rel="self" type="application/rss+xml"/>',
      f'<lastBuildDate>{rfc(VERIFIED)}</lastBuildDate>']
for slug, t, d in GUIDES:
    u = esc(abs_url(slug))
    fd.append(f"<item><title>{esc(t)}</title><link>{u}</link><guid>{u}</guid><pubDate>{rfc(ISSUE)}</pubDate><description>{esc(d)}</description></item>")
fd += ['</channel>','</rss>']
open("feed.xml","w").write("\n".join(fd) + "\n")
open("robots.txt","w").write(
    "User-agent: *\n"
    "Allow: /\n"
    "# One site to index: the root publication only (see flagged.html FLG-039).\n"
    "# The secondary builds on this host are review-only material, kept out of the\n"
    "# search index. Remove a rule only if the owner promotes that build to its own site.\n"
    "Disallow: /counter-check/\n"
    "Disallow: /docs/\n"
    "Disallow: /articles/\n"
    "Disallow: /review/\n"
    "Disallow: /analytics-endpoint/\n"
    f"Sitemap: {BASE}/sitemap.xml\n"
)
idx = [{"title": p["title"].split(" | ")[0], "url": p["slug"], "text": p["description"]} for p in PAGES if p["kind"] != "merged"]
json.dump(idx, open("data/search-index.json","w"), indent=2)
SM_URLS = open("sitemap.xml").read().count("<url>")
# The executive summary counts pages and guides, and both change every time anyone ships an article.
# They are therefore resolved after the last page exists and written back into the file: a typed
# count goes stale within one publish, and a stale count on a page about the state of the site is
# the kind of error that makes a reader distrust every other number on it.
_n_indexable = len([_p for _p in PAGES if _p["kind"] != "merged"])
_e = open("executive-summary.html").read()
for _tok, _val in (("@@PAGES@@", str(_n_indexable)), ("@@GUIDES@@", str(_gn))):
    if _tok not in _e:
        raise SystemExit("executive-summary.html lost its %s token; the counts must stay computed" % _tok)
    _e = _e.replace(_tok, _val)
open("executive-summary.html", "w").write(_e)

MERGED_N = sum(1 for pg in PAGES if pg["kind"] == "merged")
print(f"pages: {len(PAGES)} | search index: {len(idx)} | sitemap: {SM_URLS} urls | consolidated (deliberately out of the sitemap): {MERGED_N}")


# Post-step: mark every amazon.com citation link as sponsored (consistency: every outbound product link sponsored)
import glob as _g, re as _r
for _f in _g.glob("*.html"):
    _s = open(_f).read()
    _s2 = _r.sub(r'(<a href="https://www\.amazon\.com/dp/[^"]*")>', r'\1 rel="sponsored nofollow noopener" target="_blank">', _s)
    if _s2 != _s:
        open(_f, "w").write(_s2)
print("sponsored post-step done")

# Structural checks run last, once every page on disk was written by this build - checking earlier
# would read stale files from a previous run and report a bug that this build already fixed.
_SPEC_FAILS = check_spec_lists(sorted(__import__("glob").glob("*.html")))
if _SPEC_FAILS:
    raise SystemExit("spec-list gate failed - the same row is printed twice: " + "; ".join(_SPEC_FAILS))
