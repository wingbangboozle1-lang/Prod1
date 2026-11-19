# The Countertop Guide - static site generator.
# Source of truth: data/products.json. Run: python3 build_site.py
# Rules (do not break): disclosure above the fold + footer on every page (exact
# Associates Operating Agreement Section 5 sentence); every outbound product link
# rel="sponsored" + labeled; every product fact links to its Amazon listing;
# missing values stay blank + flagged; prices carry a snapshot date; intended ASIN
# and observed redirect target stay in separate fields; no testing/trending claims.
import json, html, os
D = json.load(open("data/products.json"))
SITE = D["site"]
PRODS = {p["id"]: p for p in D["products"]}
VERIFIED = SITE["verifiedDate"]
TAG = SITE["trackingId"]
CANON = SITE["canonical"].rstrip("/")
DISCLOSE = "As an Amazon Associate I earn from qualifying purchases."
def esc(s): return html.escape(str(s), quote=True)
def aff(p): return f"https://www.amazon.com/dp/{p['asin']}?tag={TAG}"
def stars(rating):
    full = int(float(rating))
    return "&#9733;" * full + "&#9734;" * (5 - full)
def product_card(pid, bullets_n=3, note=""):
    p = PRODS[pid]
    bl = "".join(f"<li>{esc(b)}</li>" for b in p["bullets"][:bullets_n])
    dims = esc(p["dimensions"]) if p["dimensions"] else '<span class="badge-flag">Dimensions not on listing fields - see Flagged</span>'
    return f"""
<article class="card product-card" id="{pid}">
  <span class="tag">{esc(p['category'])} &middot; {esc(p['form'])}</span>
  <h3>{esc(p['shortName'])}</h3>
  <p class="stars">{stars(p['rating'])} <strong>{esc(p['rating'])}</strong> <span class="meta">({esc(p['ratingCount'])} ratings on Amazon &middot; snapshot {VERIFIED})</span></p>
  <p class="price-row"><span class="price">{esc(p['priceNew'])}</span> <span class="listprice">{esc(p['priceList'])} list</span></p>
  <p class="meta">Price snapshot {VERIFIED} &mdash; check the live price on Amazon.</p>
  <ul class="spec-list">
    <li><strong>Capacity:</strong> {esc(p['capacityTitle'])}</li>
    <li><strong>Size (listing):</strong> {dims}</li>
    <li><strong>Features:</strong> {esc(p['specialFeatures'])}</li>
  </ul>
  <ul>{bl}</ul>
  <p><a class="btn buy" href="{aff(p)}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{p['asin']}">Check price on Amazon &middot; sponsored</a></p>
  <p class="sponsored-note">Sponsored link &middot; opens amazon.com &middot; ASIN {p['asin']} &middot; <a href="verification.html#{pid}">See the source record</a>{note}</p>
</article>"""
NAV = """<nav class="nav" aria-label="Main">
  <a href="index.html">Home</a>
  <a href="air-fryers.html">Air Fryers</a>
  <a href="thermometers.html">Thermometers</a>
  <a href="compare.html">Compare</a>
  <a href="guides.html">Guides</a>
  <details class="desk"><summary>The desk</summary>
    <div class="desk-panel">
      <a href="suggestions.html">Suggestions &amp; decisions</a>
      <a href="executive-summary.html">Executive summary</a>
      <a href="verification.html">Verification register</a>
      <a href="flagged.html">Flagged for review</a>
      <a href="compliance.html">Compliance</a>
      <a href="methodology.html">Method &amp; ledger</a>
      <a href="search.html">Search</a>
    </div>
  </details>
</nav>
<form class="searchbox" id="site-search-form" role="search">
  <label class="skip" for="site-search-input">Search the site</label>
  <input id="site-search-input" type="search" placeholder="Search guides &amp; products" aria-label="Search the site">
  <button class="btn small secondary" type="submit">Search</button>
</form>"""
FOOTER = f"""
<footer>
  <div class="disclosure-strip">Disclosure: {DISCLOSE} <a href="compliance.html">How we disclose</a></div>
  <div class="footer-inner">
    <div>
      <p class="footer-brand">The Countertop <span>Guide</span></p>
      <p>Spec-backed comparisons from Amazon listings for air fryers and meat thermometers. We show the source for every number and we say plainly what we have not verified. No fake testing.</p>
      <p class="small">Prices are snapshots from {VERIFIED} and change. Always confirm price, variant and fit on Amazon before buying.</p>
    </div>
    <nav aria-label="Shop"><p><strong>Shop</strong></p><p><a href="air-fryers.html">Air Fryers</a><br><a href="thermometers.html">Thermometers</a><br><a href="compare.html">Compare all five</a><br><a href="search.html">Search</a></p></nav>
    <nav aria-label="Guides"><p><strong>Guides</strong></p><p><a href="guides.html">All guides</a><br><a href="guide-basket-vs-oven.html">Basket or oven-style?</a><br><a href="guide-capacity-checklist.html">Capacity checklist</a><br><a href="guide-holiday-hosting.html">Holiday hosting</a><br><a href="guide-gifts-by-budget.html">Gifts by budget</a></p></nav>
    <nav aria-label="Review desk"><p><strong>Review desk</strong></p><p><a href="suggestions.html">Suggestions &amp; decisions</a><br><a href="executive-summary.html">Executive summary</a><br><a href="verification.html">Verification register</a><br><a href="flagged.html">Flagged for review</a><br><a href="compliance.html">Compliance</a><br><a href="methodology.html">Method &amp; campaign ledger</a></p></nav>
  </div>
</footer>"""
BASE = SITE["canonical"].rstrip("/") + "/"
def page(title, desc, body, extra_head="", body_class="", slug="index.html"):
    canonical = BASE if slug == "index.html" else BASE + slug
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{CANON}/assets/og-image.svg">
<meta property="og:site_name" content="The Countertop Guide">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700;9..144,900&amp;family=Inter:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="assets/style.css">
<link rel="alternate" type="application/rss+xml" title="The Countertop Guide feed" href="feed.xml">
{extra_head}
</head>
<body data-verified-date="{VERIFIED}" data-analytics-endpoint="" class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="masthead-inner">
<a class="brand" href="index.html">The Countertop <span>Guide</span></a>
{NAV}
</div></header>
<div class="disclosure-strip" role="note">Disclosure: {DISCLOSE} Prices are snapshots from {VERIFIED} &mdash; check Amazon for the live price. <a href="compliance.html">Learn more</a></div>
<main id="main" class="wrap">
{body}
</main>
{FOOTER}
<script src="assets/app.js"></script>
</body>
</html>
"""
def write_page(fname, title, desc, body, extra_head="", body_class=""):
    open(fname, "w").write(page(title, desc, body, extra_head, body_class, slug=fname))
def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj)}</script>'
def guide_shell(kicker, h1, intro, sections_html, faqs, readtime="4 min read", cluster=""):
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in faqs)
    body = f"""
<p class="eyebrow">{esc(kicker)}</p>
<h1 class="guide-title">{esc(h1)}</h1>
<p class="byline">By The Countertop Guide editors &middot; Spec-based guide (not hands-on tested) &middot; Listing data verified {VERIFIED} &middot; {readtime}</p>
<p class="lede">{intro}</p>
<div class="toc"><strong>On this page:</strong> <a href="#shortlist">Shortlist from verified listings</a> &middot; <a href="#compare-link">Full comparison</a> &middot; <a href="#faq">Questions</a></div>
{sections_html}
<h2 id="shortlist">Shortlist from verified listings</h2>
<div class="grid cols-3">{product_card('P1',2)}{product_card('P2',2)}{product_card('P3',2)}</div>
<p id="compare-link"><a class="btn secondary" href="compare.html">See the full side-by-side comparison</a> <a class="btn secondary" href="guides.html">All buying guides</a> <a class="btn secondary" href="air-fryers.html">Air fryer category</a></p>
<h2 id="faq">Questions readers ask</h2>
{faq_html}
<div class="trust-strip">
  <p><strong>How we work:</strong> every product fact above comes from the Amazon listing linked on each card &mdash; see the <a href="verification.html">source record</a>. If a fact is missing, we say so on <a href="flagged.html">Flagged for review</a>. Prices are snapshots from {VERIFIED}; confirm on Amazon before buying.</p>
</div>
"""
    return body, jsonld(faq_json)
# ---------- INDEX (publication front page) ----------
CHOOSER = """
<form id="chooser-form" class="chooser card">
  <fieldset><legend>1. What are you cooking most?</legend>
    <label><input type="radio" name="q1" value="snacks"> Crispy snacks &amp; weeknight sides</label>
    <label><input type="radio" name="q1" value="family"> Whole meals for a crowd</label>
    <label><input type="radio" name="q1" value="meat"> Meat &amp; grill &mdash; temperature matters</label>
  </fieldset>
  <fieldset><legend>2. How much counter depth do you have?</legend>
    <label><input type="radio" name="q2" value="compact"> Compact &mdash; under ~33 cm (13 in)</label>
    <label><input type="radio" name="q2" value="standard"> Standard &mdash; ~33&ndash;40 cm</label>
    <label><input type="radio" name="q2" value="plenty"> Plenty &mdash; 40 cm+</label>
  </fieldset>
  <fieldset><legend>3. Price snapshot comfort zone?</legend>
    <label><input type="radio" name="q3" value="budget"> Under $25 (thermometer territory)</label>
    <label><input type="radio" name="q3" value="mid"> Under $80</label>
    <label><input type="radio" name="q3" value="premium"> $100+ for the full setup</label>
  </fieldset>
  <button class="btn" type="submit">Show my shortlist</button>
  <div id="chooser-result" aria-live="polite"></div>
</form>"""
index_body = f"""
<section class="hero">
  <p class="eyebrow">Air fryers &amp; meat thermometers &middot; compared from the listing</p>
  <h1>Five real products. Every number sourced. Zero hype.</h1>
  <p class="lede">We read the listings so you don't have to squint at them. Capacity, counter footprint, cleanup, wattage and price &mdash; <em>exactly as shown on Amazon</em>, with the source linked for every fact and the live price one click away. Sponsored links are labeled. Snapshots are dated.</p>
  <p class="hero-cta"><a class="btn" href="compare.html">Compare all five</a> <a class="btn secondary" href="guides.html">Read the buying guides</a></p>
  <p class="small hero-chips"><span class="badge-ok">Verified {VERIFIED}</span> <span class="badge-ok">Sponsored links labeled</span> <span class="badge-warn">Prices are snapshots &mdash; check Amazon</span></p>
</section>

<h2 class="section-head">Shop by category</h2>
<div class="grid cols-2 tiles">
  <article class="card tile tile-fryers"><span class="tag">Air Fryers &middot; 3 products</span>
    <h3><a href="air-fryers.html">Dual-basket, oven-style &amp; single-basket</a></h3>
    <p>From a 6QT dual-basket that finishes two dishes together to a 26QT French-door oven built for holiday crowds. Compare depth, footprint and capacity per centimetre of counter.</p>
    <p><a class="btn small" href="air-fryers.html">Shop air fryers</a></p></article>
  <article class="card tile tile-thermos"><span class="tag">Thermometers &middot; 2 products</span>
    <h3><a href="thermometers.html">Instant-read vs wireless probes</a></h3>
    <p>One-second reads from your hand, or three WiFi probes you can watch from the couch. Accuracy claims are quoted from the listing with the certification named.</p>
    <p><a class="btn small" href="thermometers.html">Shop thermometers</a></p></article>
</div>

<h2 class="section-head">Our five picks <span class="section-note">snapshot {VERIFIED}</span></h2>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<div class="grid cols-2" style="margin-top:1rem">{product_card('P4')}{product_card('P5')}</div>
<p class="small">Every card links to its Amazon listing and its <a href="verification.html">source record</a>. Prices and ratings are {VERIFIED} snapshots and will change.</p>

<h2 class="section-head">Fresh off the desk</h2>
<div class="grid cols-3 guide-cards">
  <article class="card"><span class="tag">Seasonal &middot; Air fryers</span><h3><a href="guide-holiday-hosting.html">The holiday hosting test: which air fryer actually feeds a crowd?</a></h3><p>Capacity claims, turkeys, sides and the one measurement that decides whether it fits your counter in December.</p><p class="meta">6 min read</p></article>
  <article class="card"><span class="tag">Seasonal &middot; Gifts</span><h3><a href="guide-gifts-by-budget.html">Kitchen gifts under $25, under $80 and under $150</a></h3><p>Verified-price gift tiers for cooks, grillers and hosts &mdash; with the listing's own gift claims quoted, not invented.</p><p class="meta">5 min read</p></article>
  <article class="card"><span class="tag">Air fryers &middot; Specs</span><h3><a href="guide-wattage-outlets.html">Will it trip the breaker? Wattage and outlet math for air fryers</a></h3><p>1000W or 1700W? One of our listings answers that question two different ways &mdash; here's how to check yours.</p><p class="meta">5 min read</p></article>
  <article class="card"><span class="tag">Seasonal &middot; Gifts</span><h3><a href="guide-holiday-gifts.html">Holiday air fryer gifts: what to buy for every kind of cook</a></h3><p>Match the fryer to the cook &mdash; couples, crowds, small kitchens, stocking stuffers.</p><p class="meta">4 min read</p></article>
  <article class="card"><span class="tag">Seasonal &middot; Roasts</span><h3><a href="guide-holiday-roast.html">Roast like a pro: instant-read or wireless for holiday roasts?</a></h3><p>Read the accuracy claims on both thermometers before the holiday cook.</p><p class="meta">4 min read</p></article>
  <article class="card"><span class="tag">Air fryers &middot; Space</span><h3><a href="guide-small-kitchen.html">Small kitchen, big appetite: air fryers under 34 cm of depth</a></h3><p>Counter-depth math for tight kitchens, derived from listing dimensions.</p><p class="meta">4 min read</p></article>
</div>
<p><a class="btn secondary small" href="guides.html">All 11 buying guides</a></p>

<section class="chooser-block">
<h2 class="section-head">Not sure where to start? Answer three questions.</h2>
<p>Our chooser uses only verified specs (form, depth, price snapshot). It does not replace reading the listing &mdash; but it gets you to a shortlist in 20 seconds.</p>
{CHOOSER}
</section>

<section class="trust-strip">
<h2 class="section-head">Why this page is worth your time</h2>
<div class="grid cols-3">
  <div><h3>Every number has a source</h3><p>Product facts link to the exact Amazon listing they came from. If we couldn't confirm a value, it's blank and flagged &mdash; never guessed.</p></div>
  <div><h3>Snapshots are dated</h3><p>Prices and ratings say when they were read ({VERIFIED}). The live listing governs &mdash; that's why every buy button goes straight to Amazon.</p></div>
  <div><h3>We don't fake testing</h3><p>No hands-on claims, no invented rankings, no "trending" without a dated snapshot. What the listing says, we quote; what it doesn't, we say.</p></div>
</div>
</section>

<p class="center"><a class="btn secondary" href="suggestions.html">Suggest a topic or review our next steps</a></p>
"""
dash_body = f"""
<p class="eyebrow">Dashboard</p>
<h1>Every dashboard surface, one place</h1>
<p class="lede">The shop lives on the front page; the machinery lives here. Pick a surface below - nothing on this hub is hidden, and every page it links to carries its own sources.</p>
<div class="grid cols-3">
  <article class="card"><span class="tag">Products</span><h3><a href="verification.html">Verification register</a></h3><p>Line-by-line sources for every fact: intended ASIN, official listing URL, confirmation date and source - with observed redirect targets kept in a separate field.</p></article>
  <article class="card"><span class="tag">Review</span><h3><a href="flagged.html">Flagged for review</a></h3><p>Irregularities and unverified items (FLG-001..FLG-022), each with what is known, what is not, and how to resolve it. Flagged items do not block publishing; they block claims.</p></article>
  <article class="card"><span class="tag">Policy</span><h3><a href="compliance.html">Compliance</a></h3><p>Disclosure wording, sponsored-link marking, and the Amazon Associates + FTC checklist reviewed before each publish.</p></article>
  <article class="card"><span class="tag">Method</span><h3><a href="methodology.html">Method &amp; campaign ledger</a></h3><p>Evidence rules, the five defined analytics events, and the empty campaign ledger that fills only from authorized first-party reports.</p></article>
  <article class="card"><span class="tag">Summary</span><h3><a href="executive-summary.html">Executive summary</a></h3><p>What the site is, what is verified, what is not, how money and measurement work, and the next owner gates.</p></article>
  <article class="card"><span class="tag">Decisions</span><h3><a href="suggestions.html">Suggestions board</a></h3><p>Suggestions SG-01..SG-26 with evidence needed and effort, plus the Q/I/A decision log (Q-01..Q-19) for questions that must be answered before a reasonable choice.</p></article>
</div>
<p class="small">Also on this hub: <a href="search.html">site search</a> - <a href="sitemap.xml">sitemap</a> - <a href="feed.xml">RSS feed</a>.</p>
"""
write_page("dashboard.html", "Dashboard: Verification, Flags, Compliance & Decisions | The Countertop Guide","One hub for every dashboard surface of The Countertop Guide: verification register, flagged items, compliance checklist, method and ledger, executive summary, and the suggestions board.", dash_body)
write_page("index.html",
 "The Countertop Guide: Air Fryers &amp; Thermometers Compared From the Listing",
 "Five kitchen products compared from verified Amazon listings: air fryers and meat thermometers with sourced capacity, footprint, cleanup and dated price snapshots. Sponsored links labeled.",
 index_body,
 jsonld({"@context":"https://schema.org","@type":"WebSite","name":"The Countertop Guide","url":CANON+"/","potentialAction":{"@type":"SearchAction","target":CANON+"/search.html?q={search_term_string}","query-input":"required name=search_term_string"}}))
# ---------- AIR FRYERS ----------
af_body = f"""
<p class="eyebrow">Category &middot; Air Fryers</p>
<h1>Air fryers: dual-basket, oven-style &amp; single-basket</h1>
<p class="lede">Three verified fryers, three different jobs. The dual-basket cooks two dishes at once; the French-door oven is built for crowds and rotisserie; the single basket is the compact weeknight workhorse. Start with form, then capacity, then footprint.</p>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<h2>Air fryer comparison <span class="section-note">verified fields only &middot; snapshot {VERIFIED}</span></h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>Chefman 6QT Dual-Basket<br><span class="meta">B0CDY277D3</span></th><th>Emeril 26QT French-Door<br><span class="meta">B09B7SB46R</span></th><th>Chefman 8QT TurboFry<br><span class="meta">B08DKYBTPH</span></th></tr>
<tr><td>Form</td><td>Dual basket (2 &times; 3 Qt)</td><td>Oven-style, French door</td><td>Single basket</td></tr>
<tr><td>Capacity (title)</td><td>6 Quart</td><td>26QT</td><td>8 quarts</td></tr>
<tr><td>Capacity field on listing</td><td>6 liters <span class="badge-warn">unit differs &mdash; FLG-002</span></td><td>24.6 liters <span class="badge-warn">unit differs &mdash; FLG-002</span></td><td>8 quarts</td></tr>
<tr><td>Dimensions (D &times; W &times; H)</td><td>13.38 &times; 11.81 &times; 10.63 in</td><td>16.9 &times; 15.8 &times; 14.8 in</td><td>12.75 &times; 13.5 &times; 10 in</td></tr>
<tr><td>Counter depth</td><td>13.38 in (34.0 cm)</td><td>16.9 in (42.9 cm)</td><td>12.75 in (32.4 cm)</td></tr>
<tr><td>Footprint (W &times; D)*</td><td>158.0 sq in</td><td>267.0 sq in</td><td>172.1 sq in</td></tr>
<tr><td>Capacity per sq in footprint*</td><td>0.038 qt/sq in</td><td>0.097 qt/sq in</td><td>0.046 qt/sq in</td></tr>
<tr><td>Rating (snapshot)</td><td>4.2 (4,876)</td><td>4.3 (18,375)</td><td>4.4 (16,892)</td></tr>
<tr><td>Price snapshot (new)</td><td>$79.93 (list $99.99)</td><td>$149.99 (list $209.99)</td><td>$69.99 (list $119.99)</td></tr>
<tr><td>Wattage (listing)</td><td>1700 W / 120 V <span class="meta">(bullets)</span></td><td>1700 W / 120 V <span class="meta">(Product information)</span></td><td>1000 W <span class="meta">(bullets)</span> vs 1700 W <span class="meta">(Product information)</span> <span class="badge-flag">discrepancy &mdash; FLG-022</span></td></tr>
<tr><td>Warranty (listing)</td><td>1-year Chefman assurance</td><td>Warranty PDF linked; no term in listing text</td><td>1-year Chefman warranty</td></tr>
<tr><td>Cleanup (listing)</td><td>Non-stick baskets dishwasher safe</td><td>See listing for accessory care</td><td>Basket + tray top-rack dishwasher safe</td></tr>
<tr><td>Source</td><td><a href="https://www.amazon.com/dp/B0CDY277D3" rel="sponsored nofollow noopener" target="_blank">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B09B7SB46R" rel="sponsored nofollow noopener" target="_blank">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B08DKYBTPH" rel="sponsored nofollow noopener" target="_blank">Amazon listing</a></td></tr>
</table></div>
<p class="small">* Derived by us from listing dimensions and title capacity (1 in = 2.54 cm). Not a manufacturer claim &mdash; see the <a href="guide-cleanup-counter-space.html">counter-space guide</a> for method and limits. Where the listing gives two values for one field, we show both and flag the difference (<a href="flagged.html">Flagged</a>).</p>
<h2>Guides for air fryer buyers</h2>
<ul class="link-list">
<li><a href="guide-basket-vs-oven.html">Basket or oven-style air fryer: what should you compare?</a></li>
<li><a href="guide-capacity-checklist.html">A no-hype checklist for comparing air fryer capacity</a></li>
<li><a href="guide-cleanup-counter-space.html">How to assess cleanup and counter-space trade-offs</a></li>
<li><a href="guide-multifunction-questions.html">Questions to ask before buying a multi-function kitchen appliance</a></li>
<li><a href="guide-holiday-hosting.html">The holiday hosting test: which air fryer actually feeds a crowd?</a></li>
<li><a href="guide-wattage-outlets.html">Will it trip the breaker? Wattage and outlet math</a></li>
</ul>
<p><a class="btn secondary" href="compare.html">Compare with thermometers</a></p>
"""
write_page("air-fryers.html",
 "Air Fryers Compared: Dual-Basket, Oven-Style &amp; Single-Basket | The Countertop Guide",
 "Compare the Chefman 6QT dual-basket, Emeril 26QT French-door oven and Chefman 8QT TurboFry from verified Amazon listings: capacity, footprint, wattage, cleanup and dated price snapshots.",
 af_body)
# ---------- THERMOMETERS ----------
th_body = f"""
<p class="eyebrow">Category &middot; Thermometers</p>
<h1>Thermometers: instant-read vs wireless</h1>
<p class="lede">Two different tools for the same job &mdash; knowing when meat is done. The instant-read gives a 1-second answer in your hand. The wireless system watches three probes from your phone. Accuracy claims below are quoted from the listing with the certification named; we have not independently calibrated either unit.</p>
<div class="grid cols-2">{product_card('P4')}{product_card('P5')}</div>
<h2>Thermometer comparison <span class="section-note">verified fields only &middot; snapshot {VERIFIED}</span></h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>ThermoMaven Instant-Read<br><span class="meta">B0DHZTCNR5</span></th><th>CHEF iQ Sense Wireless<br><span class="meta">B0DZFD6R9Z</span></th></tr>
<tr><td>Type</td><td>Handheld instant-read</td><td>Wireless probes + hub + app</td></tr>
<tr><td>Accuracy claim (listing)</td><td>&plusmn;0.5&deg;F, NIST &amp; NSF certified <span class="meta">(spec field "Specification Met: NIST, NSF"; bullets)</span></td><td>4 internal + 1 ambient sensor (listing bullets); no &plusmn;&deg;F figure shown</td></tr>
<tr><td>Read / monitoring</td><td>1-second read (thermocouple, per bullets)</td><td>Real-time app updates, WiFi unlimited range, Bluetooth</td></tr>
<tr><td>Probes</td><td>Single probe (handheld)</td><td>3 probes included (1/2/4-probe variants priced on listing)</td></tr>
<tr><td>Heat rating</td><td>&mdash; (not shown)</td><td>1000&deg;F heat-safe probes (per title/bullets)</td></tr>
<tr><td>Waterproof / care</td><td>IP67 waterproof; rinse under water</td><td>Waterproof, dishwasher-safe probes</td></tr>
<tr><td>Battery / charge</td><td>1&times; AAA battery included</td><td>Up to 50 hours per charge (per bullets)</td></tr>
<tr><td>Warranty (listing)</td><td>Includes 1&times; calibration certificate</td><td>Two-year assurance (per bullets)</td></tr>
<tr><td>Rating (snapshot)</td><td>4.6 (3,499)</td><td>4.2 (2,178)</td></tr>
<tr><td>Price snapshot</td><td>$16.99 (list $22.99)</td><td>$119.99 3-probe (list $219.99)</td></tr>
<tr><td>Dimensions</td><td><span class="badge-flag">Not on listing fields &mdash; FLG-004</span></td><td><span class="badge-flag">Not on listing fields &mdash; FLG-004</span></td></tr>
<tr><td>Source</td><td><a href="https://www.amazon.com/dp/B0DHZTCNR5" rel="sponsored nofollow noopener" target="_blank">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B0DZFD6R9Z" rel="sponsored nofollow noopener" target="_blank">Amazon listing</a></td></tr>
</table></div>
<p class="small">A newer ThermoMaven variant (B0GL7Z4KP4, Orange) is shown on the listing &mdash; we promote the submitted ASIN only (<a href="flagged.html#FLG-003">FLG-003</a>).</p>
<h2>Guide</h2>
<ul class="link-list"><li><a href="guide-thermometer-accuracy.html">Instant-read or wireless? How to read accuracy claims without being misled</a></li>
<li><a href="guide-gifts-by-budget.html">The ThermoMaven is listed as a stocking stuffer &mdash; see our gift tiers</a></li></ul>
<p><a class="btn secondary" href="compare.html">Compare with air fryers</a></p>
"""
write_page("thermometers.html",
 "Meat Thermometers Compared: Instant-Read vs Wireless | The Countertop Guide",
 "ThermoMaven 1-second instant-read vs CHEF iQ Sense wireless 3-probe system, compared from verified Amazon listings: accuracy claims, certification fields, range, probes and dated price snapshots.",
 th_body)
# ---------- COMPARE ----------
compare_body = f"""
<p class="eyebrow">Comparison</p>
<h1>All five products, side by side</h1>
<p class="lede">Every cell is either quoted from the Amazon listing (with link) or marked missing. Derived rows (footprint, capacity per square inch) show their method. Prices are {VERIFIED} snapshots &mdash; the live price on Amazon is the only price that matters.</p>
<h2>Three-question chooser</h2>
{CHOOSER}
<h2>Full table</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>P1 Chefman 6QT Dual<br><span class="meta">B0CDY277D3</span></th><th>P2 Emeril 26QT Oven<br><span class="meta">B09B7SB46R</span></th><th>P3 Chefman 8QT Basket<br><span class="meta">B08DKYBTPH</span></th><th>P4 ThermoMaven Instant<br><span class="meta">B0DHZTCNR5</span></th><th>P5 CHEF iQ Wireless<br><span class="meta">B0DZFD6R9Z</span></th></tr>
<tr><td>Category / form</td><td>Air Fryers &middot; Dual basket</td><td>Air Fryers &middot; Oven-style</td><td>Air Fryers &middot; Single basket</td><td>Thermometers &middot; Instant-read</td><td>Thermometers &middot; Wireless</td></tr>
<tr><td>Capacity</td><td>6 Quart (title) / 6 liters (field)</td><td>26QT (title) / 24.6 liters (field)</td><td>8 quarts</td><td>&mdash;</td><td>&mdash;</td></tr>
<tr><td>Dimensions</td><td>13.38D &times; 11.81W &times; 10.63H in</td><td>16.9D &times; 15.8W &times; 14.8H in</td><td>12.75D &times; 13.5W &times; 10H in</td><td>Not shown</td><td>Not shown</td></tr>
<tr><td>Rating snapshot</td><td>4.2 (4,876)</td><td>4.3 (18,375)</td><td>4.4 (16,892)</td><td>4.6 (3,499)</td><td>4.2 (2,178)</td></tr>
<tr><td>Price snapshot (new)</td><td>$79.93</td><td>$149.99</td><td>$69.99</td><td>$16.99</td><td>$119.99 (3-probe)</td></tr>
<tr><td>List price</td><td>$99.99</td><td>$209.99</td><td>$119.99</td><td>$22.99</td><td>$219.99</td></tr>
<tr><td>Wattage</td><td>1700 W</td><td>1700 W</td><td>1000 W vs 1700 W <span class="badge-flag">FLG-022</span></td><td>&mdash;</td><td>&mdash;</td></tr>
<tr><td>Key differentiator (listing)</td><td>Sync Finish, 2&times;3 Qt baskets</td><td>French door, rotisserie, 12 in pizza</td><td>450&deg;F Hi-Fry, dishwasher-safe basket</td><td>1-sec, &plusmn;0.5&deg;F NIST</td><td>WiFi, 3 probes, 1000&deg;F-safe</td></tr>
<tr><td>Buy (sponsored)</td>
<td><a class="btn small buy" href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0CDY277D3">Amazon</a></td>
<td><a class="btn small buy" href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B09B7SB46R">Amazon</a></td>
<td><a class="btn small buy" href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B08DKYBTPH">Amazon</a></td>
<td><a class="btn small buy" href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">Amazon</a></td>
<td><a class="btn small buy" href="{aff(PRODS['P5'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">Amazon</a></td></tr>
<tr><td>Source record</td><td><a href="verification.html#P1">P1</a></td><td><a href="verification.html#P2">P2</a></td><td><a href="verification.html#P3">P3</a></td><td><a href="verification.html#P4">P4</a></td><td><a href="verification.html#P5">P5</a></td></tr>
</table></div>
<p class="small">All outbound links are sponsored (rel="sponsored") and open amazon.com. Ratings and prices are {VERIFIED} snapshots and will change. See the <a href="verification.html">verification register</a> for line-by-line sources.</p>
<h2>Counter-space analysis <span class="section-note">air fryers only</span></h2>
<div class="table-scroll"><table>
<tr><th>Air fryer</th><th>Depth</th><th>Footprint</th><th>Capacity (title)</th><th>Capacity per cm depth*</th><th>Capacity per sq in*</th></tr>
<tr><td>Chefman 6QT Dual (B0CDY277D3)</td><td>34.0 cm</td><td>158.0 sq in</td><td>6 qt</td><td>0.18 qt/cm</td><td>0.038 qt/sq in</td></tr>
<tr><td>Emeril 26QT Oven (B09B7SB46R)</td><td>42.9 cm</td><td>267.0 sq in</td><td>26 qt</td><td>0.61 qt/cm</td><td>0.097 qt/sq in</td></tr>
<tr><td>Chefman 8QT Basket (B08DKYBTPH)</td><td>32.4 cm</td><td>172.1 sq in</td><td>8 qt</td><td>0.25 qt/cm</td><td>0.046 qt/sq in</td></tr>
</table></div>
<p class="small">* Derived by us: depth in cm = inches &times; 2.54; footprint = width &times; depth; ratios use title capacity. Thermometers excluded (dimensions not shown on listing fields). Method and limits in the <a href="guide-cleanup-counter-space.html">cleanup &amp; counter-space guide</a>.</p>
<div class="sticky-bar" id="sticky-bar" style="display:none">
  <span><strong>Snapshot {VERIFIED}:</strong> cheapest pick on this page is the ThermoMaven at $16.99</span>
  <a class="btn small buy" href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">Check live price &middot; sponsored</a>
</div>
"""
write_page("compare.html",
 "Compare 5 Air Fryers &amp; Thermometers Side by Side | The Countertop Guide",
 "Side-by-side comparison of five verified products: capacity, dimensions, footprint, wattage, ratings and dated price snapshots, plus a 3-question chooser and counter-space math.",
 compare_body)
# ---------- GUIDES INDEX (clusters) ----------
guides_body = f"""
<p class="eyebrow">Guides</p>
<h1>Buying guides that start from a real question</h1>
<p class="lede">Each guide starts from a question a buyer actually types, then answers it with verified listing facts &mdash; and says plainly what the listing does not tell us. Eleven guides, three clusters, one evidence rule: no popularity or "trending" claims without a dated snapshot.</p>

<h2 class="cluster-head">Cluster 1 &middot; Choosing an air fryer</h2>
<div class="grid cols-2 guide-cards">
<article class="card"><span class="tag">Form</span><h3><a href="guide-basket-vs-oven.html">Basket or oven-style air fryer: what should you compare?</a></h3><p>Dual-basket vs French-door oven vs single basket: cooking two dishes, crowd capacity, and counter depth &mdash; with our three fryers as worked examples.</p><p class="meta">4 min read</p></article>
<article class="card"><span class="tag">Capacity</span><h3><a href="guide-capacity-checklist.html">A no-hype checklist for comparing air fryer capacity</a></h3><p>Quarts vs litres, "feeds 4&ndash;6", rotisserie and pizza claims &mdash; how to read capacity numbers without being misled.</p><p class="meta">4 min read</p></article>
<article class="card"><span class="tag">Space &amp; cleanup</span><h3><a href="guide-cleanup-counter-space.html">How to assess cleanup and counter-space trade-offs</a></h3><p>Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.</p><p class="meta">4 min read</p></article>
<article class="card"><span class="tag">Multi-function</span><h3><a href="guide-multifunction-questions.html">Questions to ask before buying a multi-function kitchen appliance</a></h3><p>Presets, accessories, wattage and warranty &mdash; the pre-purchase checklist, applied to the Emeril 26QT oven.</p><p class="meta">4 min read</p></article>
<article class="card"><span class="tag">Wattage</span><h3><a href="guide-wattage-outlets.html">Will it trip the breaker? Wattage and outlet math for air fryers</a></h3><p>What 1000W vs 1700W means for your kitchen circuit &mdash; and why one listing on this site gives both numbers.</p><p class="meta">5 min read</p></article>
<article class="card"><span class="tag">Space</span><h3><a href="guide-small-kitchen.html">Small kitchen, big appetite: which air fryer fits under 34 cm of counter depth?</a></h3><p>Depth, footprint and the derived capacity-per-centimetre math &mdash; for counters where every centimetre counts.</p><p class="meta">4 min read</p></article>
</div>

<h2 class="cluster-head">Cluster 2 &middot; Meat thermometers</h2>
<div class="grid cols-2 guide-cards">
<article class="card"><span class="tag">Accuracy</span><h3><a href="guide-thermometer-accuracy.html">Instant-read or wireless? How to read accuracy claims</a></h3><p>&plusmn;0.5&deg;F, NIST/NSF, sensor counts and range &mdash; what each claim does and does not prove.</p><p class="meta">4 min read</p></article>
<article class="card"><span class="tag">Seasonal</span><h3><a href="guide-holiday-roast.html">Roast like a pro: instant-read or wireless for holiday roasts?</a></h3><p>The accuracy claims on both thermometers, read before the holiday cook.</p><p class="meta">4 min read</p></article>
</div>

<h2 class="cluster-head">Cluster 3 &middot; Seasonal (holiday 2026)</h2>
<div class="grid cols-2 guide-cards">
<article class="card"><span class="tag">Hosting</span><h3><a href="guide-holiday-hosting.html">The holiday hosting test: which air fryer actually feeds a crowd?</a></h3><p>Capacity claims, a 6-lb rotisserie chicken, 12-inch pizzas &mdash; and the counter-depth number that decides fit in December.</p><p class="meta">6 min read</p></article>
<article class="card"><span class="tag">Gifts</span><h3><a href="guide-gifts-by-budget.html">Kitchen gifts under $25, under $80 and under $150</a></h3><p>Verified-price gift tiers for cooks, grillers and hosts. The listing's own gift claims are quoted, not invented.</p><p class="meta">5 min read</p></article>
<article class="card"><span class="tag">Gifts</span><h3><a href="guide-holiday-gifts.html">Holiday air fryer gifts: what to buy for every kind of cook</a></h3><p>Match the fryer to the cook: couples, crowds, small kitchens and stocking stuffers.</p><p class="meta">4 min read</p></article>
</div>

<h2 class="cluster-head">Pillar pages</h2>
<p><a class="btn secondary small" href="air-fryers.html">Air fryers category</a> <a class="btn secondary small" href="thermometers.html">Thermometers category</a> <a class="btn secondary small" href="compare.html">Full comparison</a></p>
<p class="small">Publishing cadence: new guides are added to the <a href="sitemap.xml">sitemap</a> and <a href="feed.xml">RSS feed</a> at publish. The next topic is chosen from measured Search Console queries once measurement is on &mdash; see the <a href="suggestions.html">review desk</a>.</p>
"""
write_page("guides.html",
 "Buying Guides: Air Fryers &amp; Thermometers | The Countertop Guide",
 "Eight question-shaped buying guides in three clusters - choosing an air fryer, meat thermometers, and holiday 2026 seasonal guides - answered from verified Amazon listings.",
 guides_body)
# ---------- GUIDE 1 ----------
b1, j1 = guide_shell("Guide &middot; Air fryers &middot; Form", "Basket or oven-style air fryer: what should you compare?",
 "If you cook two different dishes at the same time, a dual-basket wins. If you cook for a crowd or want rotisserie and a 12-inch pizza, an oven-style unit wins. Everything else is footprint and cleanup. Here is how to decide, using the three fryers on this site.",
 """
<h2>Start with the job, not the brand</h2>
<p><strong>Dual-basket (Chefman 6QT, B0CDY277D3).</strong> Two independent 3-quart baskets with Sync Finish, so two dishes can finish together. The listing describes dual-zone cooking for different dishes simultaneously. Depth is 13.38 inches (34.0 cm) &mdash; the middle of the three.</p>
<p><strong>Oven-style French-door (Emeril 26QT, B09B7SB46R).</strong> Built for volume: the listing describes 26-quart capacity for 4&ndash;6 people, rotisserie for a 6-lb chicken, and baking a 12-inch pizza. It is also the deepest at 16.9 inches (42.9 cm) and the largest footprint (267.0 sq in). French doors open with a single pull.</p>
<p><strong>Single-basket (Chefman 8QT, B08DKYBTPH).</strong> One large basket with a 450&deg;F Hi-Fry option and a top-rack dishwasher-safe basket and tray. Shallowest at 12.75 inches (32.4 cm). Best when counter depth is the constraint and you cook one dish at a time.</p>
<h2>Three questions that decide it</h2>
<ol>
<li><strong>Do you cook two things at once?</strong> If yes, dual-basket. If no, single-basket or oven-style.</li>
<li><strong>Do you cook for 4&ndash;6 or want rotisserie/pizza?</strong> If yes, oven-style. The Emeril listing makes those specific claims; verify them on the listing before buying.</li>
<li><strong>What is your counter depth?</strong> Measure it. The Emeril needs 42.9 cm; the Chefman 8QT needs 32.4 cm. A 10 cm difference decides fit.</li>
</ol>
<h2>What the listing cannot tell you</h2>
<p>We have not cooked in any of these units, so we do not claim crispness, noise, or "lived-with" durability. Those require hands-on testing we have not done &mdash; see <a href="flagged.html">Flagged for review</a>. What we can tell you is form, capacity, footprint, cleanup as listed, and price snapshot.</p>
""",
 [("Which is better, basket or oven-style air fryer?","Neither - they do different jobs. Dual-basket for two dishes at once, oven-style for crowds, rotisserie and pizza, single-basket for compact one-dish cooking. Use the three questions above."),
  ("How deep is the Emeril 26QT oven?","16.9 inches (42.9 cm) deep, per the Amazon listing dimensions (16.9D x 15.8W x 14.8H in). Measure your counter before buying."),
  ("Can the Chefman 6QT cook two dishes at once?","Yes, per the listing: two independent 3-quart baskets with Sync Finish so both can finish at the same time.")])
write_page("guide-basket-vs-oven.html", "Basket or Oven-Style Air Fryer: What Should You Compare? | The Countertop Guide","Dual-basket vs French-door oven vs single basket: two-dish cooking, crowd capacity, counter depth and cleanup, compared from verified Amazon listings.",b1,j1,"guide-page")
# ---------- GUIDE 2 ----------
b2, j2 = guide_shell("Guide &middot; Air fryers &middot; Capacity", "A no-hype checklist for comparing air fryer capacity",
 "Capacity numbers are the easiest place to be misled. Quarts vs litres, single vs dual baskets, and 'feeds 4-6' all mean different things. Use this checklist on any listing - we apply it to the three fryers here.",
 """
<h2>The checklist</h2>
<ol>
<li><strong>Which number is the title, which is the field?</strong> Chefman 6QT title vs "6 liters" field; Emeril 26QT title vs "24.6 liters" field. Note both; do not silently convert. See <a href="flagged.html">Flagged FLG-002</a>.</li>
<li><strong>Single or split?</strong> "6 Quart" that is 2 x 3 Qt behaves differently from a single 6 Qt basket. The Chefman dual-basket is explicitly 2 x 3 Qt.</li>
<li><strong>What food claim backs the number?</strong> Emeril: 4-6 people, 6-lb rotisserie chicken, 12-inch pizza (per bullets). Chefman 8QT: family-size single basket (per bullets). Ask: what food, what portion?</li>
<li><strong>What is the footprint cost?</strong> Capacity per square inch: Emeril 0.097, Chefman 8QT 0.046, Chefman 6QT dual 0.038 qt/sq in (derived from listing dims). Bigger is not automatically better if it does not fit.</li>
<li><strong>What is missing?</strong> Ask the same question of every spec. If a listing gives two values for one field (like wattage on the Chefman 8QT - see <a href="flagged.html">FLG-022</a>), treat it as unresolved until you confirm it.</li>
</ol>
<h2>Worked example</h2>
<p>Two baskets of 3 Qt each (Chefman 6QT dual) let you run chicken in one and vegetables in the other, finishing together. A single 8 Qt basket (Chefman 8QT) gives one large cavity for one dish. A 26QT oven (Emeril) gives a cavity for a whole chicken and pizza. Same word - "capacity" - three different cooking experiences.</p>
""",
 [("Is 6 quarts the same as 6 litres?","No. The Chefman 6QT listing title says 6 Quart while its capacity field says 6 liters. We report both exactly as shown and flag the difference rather than converting silently."),
  ("How many people does the Emeril 26QT feed?","The listing bullets describe it as suitable for 4-6 people. That is the seller's description, not our tested serving count."),
  ("What does capacity per square inch mean?","Title capacity divided by footprint (width x depth from listing dimensions). It shows how much capacity you get per unit of counter. Derived by us; see the compare page for method.")])
write_page("guide-capacity-checklist.html", "A No-Hype Checklist for Comparing Air Fryer Capacity | The Countertop Guide","Quarts vs litres, single vs dual baskets, feeds 4-6 and pizza claims: a checklist for reading air fryer capacity honestly, applied to three verified listings.",b2,j2,"guide-page")
# ---------- GUIDE 3 ----------
b3, j3 = guide_shell("Guide &middot; Air fryers &middot; Space &amp; cleanup", "How to assess cleanup and counter-space trade-offs",
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
<li>Emeril 26QT: six accessories included per the title (the listing description says seven - see <a href="flagged.html">FLG-021</a>); check the listing for each accessory's care instructions before buying.</li>
</ul>
<p>"Dishwasher safe" in a bullet is the seller's claim. We have not washed any of these baskets. If dishwasher care is decisive, confirm the exact wording on the listing.</p>
""",
 [("Which air fryer takes the least counter space?","By footprint, the Chefman 6QT dual-basket (158.0 sq in). By depth, the Chefman 8QT (32.4 cm). Measure both depth and width."),
  ("Are the baskets dishwasher safe?","Chefman 6QT: baskets dishwasher safe per bullets. Chefman 8QT: basket and tray top-rack dishwasher safe per bullets. Confirm on the listing."),
  ("How is capacity per cm calculated?","Title capacity (quarts) divided by depth in centimetres (inches x 2.54). Derived by us from listing dimensions; not a manufacturer claim.")])
write_page("guide-cleanup-counter-space.html", "How to Assess Cleanup and Counter-Space Trade-Offs | The Countertop Guide","Dishwasher-safe baskets, footprint math and capacity per centimetre of counter depth for three verified air fryers. Measure your counter, then compare.",b3,j3,"guide-page")
# ---------- GUIDE 4 ----------
b4, j4 = guide_shell("Guide &middot; Multi-function", "Questions to ask before buying a multi-function kitchen appliance",
 "Multi-function ovens promise everything. Before you pay for presets you will never use, ask these questions. We apply them to the Emeril 26QT French-door oven.",
 """
<h2>The pre-purchase questions</h2>
<ol>
<li><strong>How many presets, and do you recognise them?</strong> Emeril title says 24 One-Touch presets; bullets say 25 cooking pre-sets. That discrepancy is flagged - count on the listing, not the headline. Functions shown: Air Fry, Convection Bake, Rotisserie, Toast, Grill, Dehydrate, Roast, Slow Cook, Broil.</li>
<li><strong>What accessories are included?</strong> The title says six cooking accessories and the item-details field lists six (rack, bake pan, drip tray, crisper basket, rotisserie spit, fetch tool) - but the product description says seven. Flagged as <a href="flagged.html">FLG-021</a>. List them on the listing before buying; replacements cost extra.</li>
<li><strong>What is the wattage?</strong> The Emeril's Product information table lists 1700 watts / 120 volts (read 2026-11-19). Note that the Chefman 8QT listing on this site gives two different wattage figures - see <a href="guide-wattage-outlets.html">the wattage guide</a> and check yours.</li>
<li><strong>What does the warranty say?</strong> Chefman listings state 1-year assurance/warranty; CHEF iQ states 2-year assurance. For the Emeril, the listing links a warranty PDF without stating a term in the page text - open the PDF before buying.</li>
<li><strong>Does it fit?</strong> 16.9D x 15.8W x 14.8H in is the largest of the three fryers. French doors need swing clearance.</li>
</ol>
<p>Rule of thumb: pay for functions you will use weekly (air fry, bake, toast, rotisserie), not for the longest preset list.</p>
""",
 [("How many presets does the Emeril 26QT have?","The title says 24 One-Touch presets while the bullets say 25 cooking pre-sets. We flag the discrepancy and recommend verifying on the listing."),
  ("What accessories come with the Emeril oven?","The title and item-details field say six cooking accessories; the description says seven. Check the listing for the exact list before buying."),
  ("What is the Emeril wattage?","1700 watts / 120 volts per the Product information table on the listing (read 2026-11-19).")])
write_page("guide-multifunction-questions.html", "Questions to Ask Before Buying a Multi-Function Kitchen Appliance | The Countertop Guide","Presets, accessories, wattage, warranty and fit: the pre-purchase checklist for multi-function ovens, applied to the Emeril 26QT from its verified listing.",b4,j4,"guide-page")
# ---------- GUIDE 5 ----------
b5, j5 = guide_shell("Guide &middot; Thermometers &middot; Accuracy", "Instant-read or wireless? How to read accuracy claims",
 "One tool answers in one second in your hand; the other watches from your phone. The right choice depends on how you cook - and on reading accuracy claims carefully.",
 """
<h2>Instant-read: ThermoMaven (B0DHZTCNR5)</h2>
<p>Listing claims &plusmn;0.5&deg;F accuracy with NIST &amp; NSF certification (the spec field literally reads "Specification Met: NIST, NSF"), 1-second thermocouple read, IP67 waterproof, auto-rotating LED. Includes a calibration certificate. Price snapshot $16.99 (list $22.99). Best for: quick checks, grilling, candy, everyday meals.</p>
<h2>Wireless: CHEF iQ Sense (B0DZFD6R9Z)</h2>
<p>Three ultra-thin probes plus hub, WiFi unlimited range with app, 1000&deg;F heat-safe probes, up to 50 hours per charge, flip reminders and rest timers. Listing bullets describe 4 internal + 1 ambient sensors (title: 5 sensors). No &plusmn;&deg;F accuracy figure appears in the fields or bullets we read - do not assume it matches the instant-read. Price snapshot $119.99 (3-probe, list $219.99; 1/2/4-probe variants are priced on the listing). Best for: long cooks, multiple proteins, monitoring from another room.</p>
<h2>How to read "accuracy"</h2>
<ul>
<li>Ask for the &plusmn; figure and the certification name. "NIST certified" without a figure is incomplete.</li>
<li>Ask what the sensor count means. CHEF iQ's 5 = 4 internal + 1 ambient (per bullets).</li>
<li>Ask about range honestly. "Unlimited" via WiFi means app monitoring over your network, not magic - you still need WiFi and the app.</li>
<li>We have not calibrated either unit. Certification claims are the seller's; verify the certificate on the listing.</li>
</ul>
""",
 [("Which thermometer is more accurate?","The ThermoMaven listing states plus-minus 0.5 degrees F with NIST and NSF certification. No plus-minus figure appears for the CHEF iQ in the fields we read, so we do not rank them on accuracy."),
  ("What does 5 sensors mean on the CHEF iQ?","Per the listing bullets: 4 internal temperature sensors plus 1 ambient sensor that tracks cooking-environment temperature."),
  ("Do I need WiFi for the CHEF iQ?","WiFi enables unlimited-range app monitoring per the listing; Bluetooth is also listed in connectivity. You need the CHEF iQ app for remote monitoring.")])
write_page("guide-thermometer-accuracy.html", "Instant-Read or Wireless? How to Read Thermometer Accuracy Claims | The Countertop Guide","Plus-minus 0.5F, NIST/NSF, sensor counts and WiFi range: how to read meat thermometer accuracy claims honestly, comparing two verified listings.",b5,j5,"guide-page")
# ---------- GUIDE 6 (NEW - seasonal) ----------
b6, j6 = guide_shell("Guide &middot; Seasonal &middot; Holiday 2026", "The holiday hosting test: which air fryer actually feeds a crowd?",
 "Thanksgiving week, Hanukkah, game day, the office cookie swap - December asks more of a countertop appliance than a Tuesday does. Here is how our three verified fryers answer the hosting questions that actually decide the meal: how much fits, how many dishes run at once, and whether it fits the counter when the mixer is already there.",
 """
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
<p>These snapshots ({VERIFIED}) sit inside the Black Friday window - listings showed deal badges on every product we read. Treat any price as a moving target: the buy button goes to the live listing for a reason. Amazon's holiday return window on the listings we read runs to January 31, 2027 for purchases made November 1 - December 31, 2026 (as shown on the listings, read {VERIFIED}).</p>
""",
 [("Which air fryer is best for Thanksgiving?","Whichever fits your counter and your dish count. For two sides at once, the Chefman 6QT dual-basket (2 x 3 Qt with Sync Finish). For a rotisserie chicken or 12-inch pizza, the Emeril 26QT (claims per its listing). Measure counter depth first: the Emeril needs 42.9 cm."),
  ("Do these make good holiday gifts?","The ThermoMaven listing itself positions the thermometer as a stocking stuffer and Secret Santa gift (seller claim). See our gift-by-budget guide for verified-price tiers."),
  ("Are the holiday prices final?","No. All prices on this site are dated snapshots from 2026-11-19 during the Black Friday window. Confirm the live price on Amazon before buying.")],
 readtime="6 min read")
write_page("guide-holiday-hosting.html", "The Holiday Hosting Test: Which Air Fryer Feeds a Crowd? | The Countertop Guide","Holiday hosting questions answered from verified Amazon listings: two dishes at once, rotisserie and pizza claims, counter-depth math and Black Friday price-snapshot caveats.",b6,j6,"guide-page")
# ---------- GUIDE 7 (NEW - seasonal gifts) ----------
b7, j7 = guide_shell("Guide &middot; Seasonal &middot; Gifts", "Kitchen gifts under $25, under $80 and under $150",
 "Gift guides usually invent prices. This one uses dated snapshots from the five listings we verify ({VERIFIED}) and quotes each product's own gift positioning where the seller makes one. Prices move; the tiers are a starting map, not a promise.",
 """
<h2>The tiers (snapshot {VERIFIED})</h2>
<div class="table-scroll"><table>
<tr><th>Budget tier</th><th>Pick</th><th>Snapshot price</th><th>Who it's for</th><th>Listing's own gift claim</th></tr>
<tr><td>Under $25</td><td>ThermoMaven 1-Second Instant-Read <span class="meta">B0DHZTCNR5</span></td><td>$16.99 (list $22.99)</td><td>Grillers, candy makers, anyone who cuts into chicken to "check"</td><td>Bullets call it a stocking stuffer and Secret Santa pick (seller claim) &mdash; and it includes a calibration certificate</td></tr>
<tr><td>Under $80</td><td>Chefman 8QT TurboFry <span class="meta">B08DKYBTPH</span></td><td>$69.99 (list $119.99)</td><td>Family kitchens, dorms, first apartments</td><td>Listing positions the square shape for small counters (seller claim)</td></tr>
<tr><td>Under $80</td><td>Chefman 6QT Dual-Basket <span class="meta">B0CDY277D3</span></td><td>$79.93 (list $99.99)</td><td>Meal preppers who cook mains and sides together</td><td>Viewing windows and Sync Finish are the headline features</td></tr>
<tr><td>Under $150</td><td>Emeril 26QT French-Door Oven <span class="meta">B09B7SB46R</span></td><td>$149.99 (list $209.99)</td><td>Hosts, bakers, rotisserie-curious cooks</td><td>Six (or seven - see <a href="flagged.html">FLG-021</a>) accessories included</td></tr>
<tr><td>Under $150</td><td>CHEF iQ Sense Wireless (3 probes) <span class="meta">B0DZFD6R9Z</span></td><td>$119.99 (list $219.99)</td><td>Smokers, brisket people, tech-forward cooks</td><td>Three probes = three proteins at once (seller claim)</td></tr>
</table></div>
<h2>Gift-giver's checklist</h2>
<ol>
<li><strong>Check the return window.</strong> The listings we read ({VERIFIED}) show a holiday return window to January 31, 2027 for purchases November 1 - December 31, 2026. Confirm on the listing before gifting.</li>
<li><strong>Match the cook, not the logo.</strong> A wireless probe set delights a smoker owner and confuses a scrambled-eggs person.</li>
<li><strong>Mind the counter.</strong> You are gifting counter space as much as an appliance - the depth table in our <a href="guide-cleanup-counter-space.html">counter-space guide</a> applies to gifts too.</li>
<li><strong>Prices move.</strong> Every figure above is a snapshot from {VERIFIED} inside the Black Friday window. Check the live price before you buy.</li>
</ol>
<p class="small">We have not tested any of these as gifts (or as anything else). Claims quoted as "seller claims" come from the listing text, linked in the <a href="verification.html">source record</a>.</p>
""",
 [("What is a good kitchen gift under $25?","The ThermoMaven instant-read thermometer at a $16.99 snapshot price (2026-11-19). Its own listing calls it a stocking stuffer and Secret Santa pick, and it includes a calibration certificate."),
  ("Is $79.93 a good gift price for the Chefman dual-basket?","It is the buy-box snapshot from 2026-11-19 against a $99.99 list price shown on the listing. Prices are snapshots during the Black Friday window and can change - confirm on Amazon."),
  ("Should I gift an air fryer to someone with a small kitchen?","Measure their counter depth first. The Chefman 8QT is the shallowest of the three fryers here at 12.75 in (32.4 cm); the Emeril oven needs 16.9 in (42.9 cm).")],
 readtime="5 min read")
write_page("guide-gifts-by-budget.html", "Kitchen Gifts Under $25, $80 and $150 (Verified-Price Tiers) | The Countertop Guide","Holiday 2026 gift tiers from five verified Amazon listings: dated price snapshots, each product's own gift claims quoted, and a gift-giver's checklist.",b7,j7,"guide-page")
# ---------- GUIDE 8 (NEW - wattage) ----------
b8, j8 = guide_shell("Guide &middot; Air fryers &middot; Specs", "Will it trip the breaker? Wattage and outlet math for air fryers",
 "Air fryers are high-wattage appliances, and wattage is the spec listings are most likely to get inconsistent. We found exactly that on one of our own products. Here is what wattage means for your kitchen circuit, and how to check any listing for the same trap.",
 """
<h2>What the listings say (read {VERIFIED})</h2>
<ul>
<li><strong>Chefman 6QT Dual (B0CDY277D3):</strong> "120 Volts/1700 Watts" in the listing bullets. One number, consistent.</li>
<li><strong>Emeril 26QT (B09B7SB46R):</strong> Product information table lists 1700 watts / 120 volts.</li>
<li><strong>Chefman 8QT (B08DKYBTPH):</strong> the bullets say "1000 Watts/120 Volts - RJ38-SQSS-8T" while the Product information table on the same page says 1700 watts. Both values are on the same listing. We show both and flag it (<a href="flagged.html">FLG-022</a>).</li>
</ul>
<h2>The kitchen math</h2>
<p>A standard US kitchen circuit is 120 volts, typically 15 amps (1,800 watts of capacity) or 20 amps (2,400 watts). The rule of thumb electricians use: keep a continuous load under about 80% of the circuit. That puts the safe continuous budget around 1,440 W on a 15-amp circuit.</p>
<p>At 1,700 watts, an air fryer is already above that 15-amp continuous budget on its own - which is why the manuals say "dedicated outlet". At 1,000 watts, there is usually room for a kettle or toaster on the same circuit. The difference matters most in older kitchens and dorms.</p>
<h2>How to check any listing for the wattage trap</h2>
<ol>
<li>Read the "About this item" bullets and note any wattage figure.</li>
<li>Open the "Product information" table (it's below the description) and compare.</li>
<li>If the two disagree, treat wattage as unresolved. Check the box or the manufacturer's spec sheet before you plan your circuit around it.</li>
<li>When in doubt, assume the higher number for safety planning.</li>
</ol>
<p class="small">This is general electrical guidance, not a certified electrician's advice. We derived the circuit math from standard US 120V/15A and 20A ratings; the wattage figures are quoted from the listings. We have not measured any unit's draw.</p>
""",
 [("How many watts does an air fryer use?","The fryers on this site are listed between 1000 and 1700 watts. The Chefman 8QT listing gives both 1000W (bullets) and 1700W (Product information) - we show both and flag the conflict. Check your unit's label before planning outlets."),
  ("Can I run an air fryer and a microwave on the same circuit?","Not safely if the air fryer draws 1700W: that alone approaches the capacity of a 15-amp, 120-volt kitchen circuit. Use separate outlets on separate circuits for two high-wattage appliances."),
  ("Why do two sections of the same listing show different wattage?","Seller-entered data can disagree between bullets and the Product information table, exactly as on the Chefman 8QT (FLG-022). Treat the conflict as unresolved and verify on the box or manufacturer's spec sheet.")],
 readtime="5 min read")
write_page("guide-wattage-outlets.html", "Will It Trip the Breaker? Air Fryer Wattage and Outlet Math | The Countertop Guide","What 1000W vs 1700W means for a 120V kitchen circuit, the wattage-listing conflict on the Chefman 8QT, and a checklist for verifying wattage on any listing.",b8,j8,"guide-page")
# ---------- GUIDE 9 (merged from session arena/8e82d03c - recipient-angle gifts) ----------
b9, j9 = guide_shell("Guide &middot; Seasonal &middot; Gifts", "Holiday air fryer gifts: what to buy for every kind of cook",
 "Match the fryer to the cook, not the wish list. These picks come only from the verified listings on this site, each with its snapshot price and a link to its source. (Shopping by budget instead? See <a href=\"guide-gifts-by-budget.html\">gifts under $25, $80 and $150</a>.)",
 f"""
<h2>For couples and side-dish cooks: Chefman 6QT dual-basket</h2>
<p>Two independent 3-quart baskets with Sync Finish, so two dishes can finish at the same time - good for a main and a side together. Listing shows dual-zone cooking, viewing windows, and dishwasher-safe baskets. Depth 13.38 inches (34.0 cm). Price snapshot 2026-11-19: $79.93 (list $99.99). <a href="https://www.amazon.com/dp/B0CDY277D3?tag={TAG}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0CDY277D3">See Chefman 6QT listing &middot; sponsored</a></p>
<h2>For crowds and weekend roasts: Emeril 26QT French-door oven</h2>
<p>The listing describes 26-quart capacity for 4-6 people, rotisserie for a 6-lb chicken, and baking a 12-inch pizza. Deepest of the three at 16.9 inches (42.9 cm) - it needs real counter depth. Price snapshot 2026-11-19: $149.99 (list $209.99). Preset count differs between title (24) and bullets (25) - see Flagged FLG-002. <a href="https://www.amazon.com/dp/B09B7SB46R?tag={TAG}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B09B7SB46R">See Emeril 26QT listing &middot; sponsored</a></p>
<h2>For small kitchens: Chefman 8QT single basket</h2>
<p>Shallowest of the three at 12.75 inches (32.4 cm) deep, with an 8-quart single basket, 450&deg;F Hi-Fry option, and a top-rack dishwasher-safe basket and tray. Price snapshot 2026-11-19: $69.99 (list $119.99). <a href="https://www.amazon.com/dp/B08DKYBTPH?tag={TAG}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B08DKYBTPH">See Chefman 8QT listing &middot; sponsored</a></p>
<h2>Thermometer stocking stuffers</h2>
<ul>
<li><strong>ThermoMaven instant-read:</strong> 1-second read, &plusmn;0.5&deg;F accuracy with NIST &amp; NSF certification claimed, IP67 waterproof, includes a calibration certificate. Price snapshot 2026-11-19: $16.99 (list $22.99). Rating snapshot: 4.6 (3,499). Dimensions not captured - see Flagged FLG-004. <a href="https://www.amazon.com/dp/B0DHZTCNR5?tag={TAG}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">See ThermoMaven listing &middot; sponsored</a></li>
<li><strong>CHEF iQ Sense wireless:</strong> 3 ultra-thin probes plus hub, WiFi app monitoring, 1000&deg;F heat-safe probes claimed, up to 50 hours per charge claimed. Bullets describe 4 internal + 1 ambient sensors (title says 5); no &plusmn;&deg;F accuracy figure captured. Price snapshot 2026-11-19: $119.99 (list $219.99, 3-probe). Rating snapshot: 4.2 (2,178). <a href="https://www.amazon.com/dp/B0DZFD6R9Z?tag={TAG}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">See CHEF iQ listing &middot; sponsored</a></li>
</ul>
<p class="small">Snapshot prices and ratings are from Amazon.com on 2026-11-19 and will change. Confirm price, variant and fit on the listing before buying. No hands-on testing - these are spec-based suggestions, not recommendations of use.</p>
""",
 [("Which air fryer makes the best gift?","The one that fits the recipient's counter and cooking: dual-basket for two dishes at once, oven-style for crowds and roasts, single basket for compact counters. Match counter depth first."),
  ("Are these gift picks hands-on tested?","No. We have not cooked with any of these units. Picks are based only on verified listing specs and snapshot prices."),
  ("Do the prices include shipping?","Prices shown are the listing's new-item snapshot; shipping depends on the buyer's location and Prime status at checkout. Confirm on Amazon before buying.")],
 readtime="4 min read")
write_page("guide-holiday-gifts.html", "Holiday Air Fryer Gifts: What to Buy for Every Kind of Cook | The Countertop Guide","Spec-based holiday gift picks matched to the cook: dual-basket for couples, French-door oven for crowds, single basket for small kitchens, thermometer stocking stuffers. Verified snapshots only.",b9,j9,"guide-page")
# ---------- GUIDE 10 (merged from session arena/8e82d03c - holiday roasts) ----------
b10, j10 = guide_shell("Guide &middot; Seasonal &middot; Thermometers", "Roast like a pro: instant-read or wireless thermometer for holiday roasts?",
 "A roast is only as good as knowing when it's done. This guide reads the accuracy claims on two verified thermometers - what each claim does and does not prove - so you can choose before the holiday.",
 f"""
<h2>Instant-read: ThermoMaven 1-Second</h2>
<p>Listing claims &plusmn;0.5&deg;F accuracy with NIST &amp; NSF certification, 1-second thermocouple read, IP67 waterproof, auto-rotating LED, includes a calibration certificate. Best for: quick checks, grilling, candy, everyday meals. Price snapshot 2026-11-19: $16.99 (list $22.99). Rating snapshot: 4.6 (3,499). <a href="https://www.amazon.com/dp/B0DHZTCNR5?tag={TAG}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">See ThermoMaven listing &middot; sponsored</a></p>
<h2>Wireless: CHEF iQ Sense (3 probes)</h2>
<p>Three ultra-thin probes plus hub, WiFi unlimited range with app, 1000&deg;F heat-safe probes claimed, up to 50 hours per charge claimed, flip reminders and rest timers. Listing bullets describe 4 internal + 1 ambient sensors (title says 5). No &plusmn;&deg;F accuracy figure was captured - do not assume it matches the instant-read. Price snapshot 2026-11-19: $119.99 (list $219.99, 3-probe). Rating snapshot: 4.2 (2,178). <a href="https://www.amazon.com/dp/B0DZFD6R9Z?tag={TAG}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">See CHEF iQ listing &middot; sponsored</a></p>
<h2>How to read accuracy claims</h2>
<ul>
<li>Ask for the &plusmn; figure and the certification name. "NIST certified" without a figure is incomplete.</li>
<li>Ask what the sensor count means. CHEF iQ's 5 = 4 internal + 1 ambient (per bullets).</li>
<li>"Unlimited" WiFi range means app monitoring over your network - you still need WiFi and the app.</li>
<li>We have not calibrated either unit. Certification claims are the seller's; verify the certificate on the listing.</li>
</ul>
<p class="small">Accuracy figures and ratings are listing snapshots from 2026-11-19 and will change. We have not cooked with or calibrated either thermometer. Confirm claims on the listing before buying.</p>
""",
 [("Instant-read or wireless for a holiday roast?","Instant-read for a fast answer in your hand (ThermoMaven, 1-second). Wireless for monitoring from another room across a long cook (CHEF iQ Sense, 3 probes). Match the tool to how you cook."),
  ("Are the accuracy claims verified by the site?","No. Claims are quoted from the listings with the certification named. We have not calibrated either unit; verify certificates on the listing.")],
 readtime="4 min read")
write_page("guide-holiday-roast.html", "Instant-Read or Wireless for Holiday Roasts? | The Countertop Guide","Thermometer accuracy claims read before the holiday: ThermoMaven instant-read vs CHEF iQ wireless for roasts, with certification claims quoted from verified listings.",b10,j10,"guide-page")
# ---------- GUIDE 11 (merged from session arena/8e82d03c - small kitchens) ----------
b11, j11 = guide_shell("Guide &middot; Air fryers &middot; Space", "Small kitchen, big appetite: which air fryer fits under 34 cm of counter depth?",
 "Measure before you buy. This guide compares the three verified fryers by counter depth and footprint, with the derived capacity-per-centimetre math shown and its limits stated.",
 f"""
<h2>Measure your counter first</h2>
<p>Depth decides whether it fits under cabinets; width decides whether it crowds the sink. From listing dimensions:</p>
<ul>
<li>Chefman 8QT basket: 12.75D x 13.5W in - shallowest at 32.4 cm depth, 172.1 sq in footprint.</li>
<li>Chefman 6QT dual: 13.38D x 11.81W in - narrowest at 34.0 cm depth, 158.0 sq in footprint.</li>
<li>Emeril 26QT oven: 16.9D x 15.8W in - deepest at 42.9 cm depth, 267.0 sq in footprint.</li>
</ul>
<p class="small">Dimensions as shown on each Amazon listing on 2026-11-19. Footprint = width x depth; derived by us, not a manufacturer claim. Method and limits in the <a href="guide-cleanup-counter-space.html">cleanup &amp; counter-space guide</a>.</p>
<h2>Depth and footprint table (verified fields only)</h2>
<div class="table-scroll"><table>
<tr><th>Air fryer (ASIN)</th><th>Depth</th><th>Width</th><th>Height</th><th>Footprint</th><th>Capacity (title)</th><th>Price snapshot</th></tr>
<tr><td>Chefman 8QT single basket <span class="meta">B08DKYBTPH</span></td><td>12.75 in (32.4 cm)</td><td>13.5 in</td><td>10 in</td><td>172.1 sq in</td><td>8 quarts</td><td>$69.99 (list $119.99)</td></tr>
<tr><td>Chefman 6QT dual-basket <span class="meta">B0CDY277D3</span></td><td>13.38 in (34.0 cm)</td><td>11.81 in</td><td>10.63 in</td><td>158.0 sq in</td><td>6 Quart (2 x 3 Qt)</td><td>$79.93 (list $99.99)</td></tr>
<tr><td>Emeril 26QT French-door oven <span class="meta">B09B7SB46R</span></td><td>16.9 in (42.9 cm)</td><td>15.8 in</td><td>14.8 in</td><td>267.0 sq in</td><td>26QT</td><td>$149.99 (list $209.99)</td></tr>
</table></div>
<h2>Capacity per centimetre of counter depth (derived)</h2>
<p>Emeril 0.61 qt/cm, Chefman 8QT 0.25 qt/cm, Chefman 6QT dual 0.18 qt/cm. The oven gives the most capacity per centimetre of depth - if you have the depth to spare. Not a manufacturer claim; derived from listing dimensions and title capacity.</p>
""",
 [("Which air fryer fits the smallest counter?","By depth, the Chefman 8QT (32.4 cm). By footprint, the Chefman 6QT dual-basket (158.0 sq in). Measure both depth and width before buying."),
  ("Is capacity per centimetre a manufacturer claim?","No. It is derived by us from listing dimensions (inches x 2.54 = cm) and title capacity. Treat it as a planning aid, verify fit on the listing.")],
 readtime="4 min read")
write_page("guide-small-kitchen.html", "Small Kitchen, Big Appetite: Air Fryers Under 34 cm of Depth | The Countertop Guide","Counter-depth comparison of three verified air fryers: depth, footprint and derived capacity-per-centimetre math with its limits stated. Measure before you buy.",b11,j11,"guide-page")
# ---------- EXECUTIVE SUMMARY ----------
exec_body = f"""
<p class="eyebrow">Executive summary</p>
<h1>What this site is, what is verified, and what happens next</h1>
<p class="lede">The Countertop Guide is a spec-backed affiliate publication for two kitchen categories - air fryers and meat thermometers - built from five Amazon listings and re-verified line by line on {VERIFIED}. It leads with products and buyer questions, not with process. Every number links to its source; the review desk holds the decisions.</p>
<h2>The five products <span class="section-note">re-verified {VERIFIED}</span></h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Product</th><th>ASIN</th><th>Category</th><th>Price snapshot</th><th>Rating snapshot</th></tr>
<tr><td>P1</td><td>Chefman 6QT Dual-Basket Air Fryer Oven</td><td>B0CDY277D3</td><td>Air Fryers</td><td>$79.93 <span class="meta">(list $99.99)</span></td><td>4.2 (4,876)</td></tr>
<tr><td>P2</td><td>Emeril Lagasse 26QT French-Door Oven</td><td>B09B7SB46R</td><td>Air Fryers</td><td>$149.99 <span class="meta">(list $209.99)</span></td><td>4.3 (18,375)</td></tr>
<tr><td>P3</td><td>Chefman 8QT TurboFry Basket</td><td>B08DKYBTPH</td><td>Air Fryers</td><td>$69.99 <span class="meta">(list $119.99)</span></td><td>4.4 (16,892)</td></tr>
<tr><td>P4</td><td>ThermoMaven 1-Second Instant-Read</td><td>B0DHZTCNR5</td><td>Thermometers</td><td>$16.99 <span class="meta">(list $22.99)</span></td><td>4.6 (3,499)</td></tr>
<tr><td>P5</td><td>CHEF iQ Sense Wireless (3 probes)</td><td>B0DZFD6R9Z</td><td>Thermometers</td><td>$119.99 <span class="meta">(list $219.99)</span></td><td>4.2 (2,178)</td></tr>
</table></div>
<h2>What is verified</h2>
<ul>
<li>Each submitted short link resolves to the ASIN and official listing URL in the <a href="verification.html">verification register</a>; intended ASIN and observed redirect target are kept in separate fields and never merged.</li>
<li>Titles, ratings, price snapshots (buy box and list price), dimensions (air fryers), capacity fields, special features, bullets and policy text re-read against the live Amazon listings and the Associates Operating Agreement on {VERIFIED} (integration pass).</li>
<li>Compliance posture: the exact Operating Agreement Section 5 disclosure sentence above the fold on every page and in the footer; every outbound product link rel="sponsored" and labeled; no "trending" or popularity claims without a dated snapshot; no hands-on testing claims.</li>
<li>Trust machinery: a publishing gate (<code>scripts/check_site.mjs</code>) runs in the Pages workflow before deploy; five privacy-preserving analytics events are defined and counted locally.</li>
</ul>
<h2>What is not verified (and therefore not claimed)</h2>
<ul>
<li>Thermometer dimensions and any field not shown on the listing - blank and flagged (<a href="flagged.html">FLG-004</a>).</li>
<li>Short-link compliance status (unresolved, <a href="flagged.html">FLG-001</a>), the Special Link test in Associates Central (manual gate), commission rates, search volume / popularity.</li>
<li>One on-listing conflict: Chefman 8QT wattage shows 1000W (bullets) and 1700W (Product information) on the same page - both shown, flagged (<a href="flagged.html">FLG-022</a>).</li>
<li>Product photography (no Amazon images used; real photography needs a licence decision - <a href="flagged.html">FLG-009</a>).</li>
</ul>
<h2>How money and measurement work</h2>
<p>Outbound links use tracking ID <code>{TAG}</code> and are marked sponsored. Click and conversion measurement is defined (five events: page_view, outbound_click, search, chooser_complete, guide_read) with a privacy-preserving local counter; the self-hosted endpoint ships as code in <code>analytics-endpoint/</code> and needs a hosting decision before data flows. The campaign ledger starts empty - orders and revenue are recorded only from authorized first-party reports. See <a href="methodology.html">Method &amp; campaign ledger</a>.</p>
<h2>Next gates (owner decisions at the review desk)</h2>
<p><strong>First: the price and star-rating display condition (FLG-023).</strong> The Program Policies require prices and ratings to come from Amazon-served links or the Creators/PA API; our dated manual snapshots do not meet that condition as written. Three remediation options are laid out at the review desk &mdash; do not scale traffic until one is chosen. Then: Special Link validation, analytics hosting, photography licence, Search Console verification, and the ranked suggestions. Nothing scales until those gates pass. Start at the <a href="suggestions.html">review desk</a>; the design direction is captured in <a href="https://github.com/wingbangboozle1-lang/Prod1/blob/main/DESIGN_PROMPT.md">DESIGN_PROMPT.md</a>; open items live on <a href="flagged.html">Flagged for review</a>.</p>
"""
write_page("executive-summary.html", "Executive Summary: Products, Verification &amp; Next Gates | The Countertop Guide","Executive summary for The Countertop Guide: five re-verified products in two categories, compliance posture, measurement plan and the ranked decisions at the review desk.",exec_body)
# ---------- SUGGESTIONS (review desk) ----------
sugg_body = f"""
<p class="eyebrow">Review desk</p>
<h1>Suggestions &amp; decisions &mdash; choose the path before anything is built</h1>
<p class="lede">This is the site's decision room. Every suggestion below states the recommended path, the alternative, the evidence it needs and what it unblocks. Nothing is implemented until a reviewer marks it Approved. The visual direction these suggestions feed is written up in <a href="https://github.com/wingbangboozle1-lang/Prod1/blob/main/DESIGN_PROMPT.md">DESIGN_PROMPT.md</a>.</p>

<h2>Recommended path (if you only read one block)</h2>
<div class="table-scroll"><table>
<tr><th>Order</th><th>Decision</th><th>Recommended path</th><th>Effort</th><th>What it unblocks</th></tr>
<tr><td>1 <span class="badge-flag">P0</span></td><td>Price &amp; star-rating display vs API policy (FLG-023)</td><td>Apply for Creators/PA API and serve prices + ratings through it; until approved, either remove displayed prices/ratings (option B) or accept the documented risk (option C)</td><td>Low&ndash;Medium</td><td>Account-level compliance; unblocks scaling traffic</td></tr>
<tr><td>2</td><td>Outbound link validation (SG-01)</td><td>Test one Special Link per product in Associates Central; confirm destination + tracking report before scaling</td><td>Low (manual, ~30 min)</td><td>Confirms revenue attribution; closes FLG-001/FLG-015</td></tr>
<tr><td>3</td><td>Measurement activation (SG-03)</td><td>Deploy <code>analytics-endpoint/server.py</code> on any HTTPS host; set <code>data-analytics-endpoint</code>; publish retention policy</td><td>Medium</td><td>Real clicks/queries data; data-driven topic picks; fills the ledger</td></tr>
<tr><td>4</td><td>Search Console (SG-02)</td><td>Verify the github.io property, submit <code>sitemap.xml</code>, review queries weekly</td><td>Low</td><td>Measured queries for the topic calendar; SEO baseline</td></tr>
<tr><td>5</td><td>Photography (SG-04)</td><td>Owner-shot photography or manufacturer permission; never copied/generated product images (S-18)</td><td>Medium</td><td>Visual conversion lift without IP exposure</td></tr>
<tr><td>6</td><td>Seasonal calendar (SG-05)</td><td>Keep shipping one question-shaped guide per week through the holiday window; each goes to sitemap + feed at publish</td><td>Low</td><td>Seasonal organic traffic while intent is high</td></tr>
</table></div>

<h2>Full suggestions board</h2>
<div class="table-scroll"><table>
<tr><th>#</th><th>Suggestion</th><th>Recommended path</th><th>Alternative</th><th>Evidence needed</th><th>Effort</th><th>Status</th></tr>
<tr><td>SG-01</td><td>Validate one Special Link per product in Associates Central and confirm destination + tracking report</td><td>SiteStripe/Tools test on all 5 ASINs with <code>shopnow047c-20</code>; screenshot the tracking report</td><td>Keep outbound buttons as-is but do not scale traffic until tested</td><td>Associates Central test clicks + report</td><td>Low</td><td><span class="badge-warn">Needs decision &mdash; gate</span></td></tr>
<tr><td>SG-02</td><td>Search Console + sitemap submission</td><td>Verify the github.io property now; custom domain later if ever</td><td>Wait for a custom domain (delays all measurement)</td><td>Domain/property choice</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-03</td><td>Deploy the self-hosted analytics endpoint (5 events)</td><td>Any small HTTPS host + the shipped <code>analytics-endpoint/server.py</code>; 30-day retention, no IPs</td><td>Keep local-only counts (device-local, no aggregation)</td><td>Hosting choice; retention policy text</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-04</td><td>Real product photography (owner-shot or licensed)</td><td>Shoot the five products yourself; store in <code>assets/photos/</code></td><td>Manufacturer written permission for press images</td><td>Licence/permission record</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-05</td><td>Weekly question-shaped guide cadence through the holidays</td><td>Ship from the approved topic list; publish to sitemap + feed same day</td><td>Pause until measurement runs (loses seasonal window)</td><td>Editorial time</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-06</td><td>Chooser expansion (budget slider, counter-depth input in cm/in)</td><td>Add depth input + unit toggle to the 3-question chooser</td><td>Keep 3-question version</td><td>Usability feedback</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-07</td><td>Reader capture (email of new guides)</td><td>Double-opt-in form, privacy notice, no tracking pixels</td><td>RSS-only (already shipped)</td><td>Provider + consent copy + FTC review</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-08</td><td>Newer-model watch (B0CNY1YVDD, B0GL7Z4KP4 seen on listings)</td><td>Keep promoting submitted ASINs; compare variants before any switch</td><td>Add variants to comparison as "also consider" rows</td><td>Variant comparison + margin check</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-09</td><td>Hands-on testing programme</td><td>Buy units, publish a protocol first, disclose bought-vs-free per FTC</td><td>Stay spec-only (current honest posture)</td><td>Budget, protocol, photo workflow</td><td>High</td><td>Proposed &mdash; do not claim until done</td></tr>
<tr><td>SG-10</td><td>Expand categories (more brands per category)</td><td>Add 2-3 ASINs per category via a fresh verification pass</td><td>Deepen existing five with the new guides</td><td>New ASIN verification</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-11</td><td>Resolve the Chefman 8QT wattage conflict (FLG-022)</td><td>Ask the seller/support which figure is right; update data + guides</td><td>Keep both values + flag (current state)</td><td>Manufacturer confirmation</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-12</td><td>Price-snapshot cadence (weekly during holidays)</td><td>Re-run the verification pass weekly; every price carries its date</td><td>Snapshot monthly</td><td>Editorial time</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-13</td><td>Custom domain</td><td>Stay on github.io until traffic proves the concept</td><td>Buy a domain now + set canonical</td><td>Domain purchase</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-14</td><td>Newsletter/seasonal gift guide refresh in December</td><td>Update gift tiers with fresh snapshots Dec 1 and Dec 15</td><td>One December refresh</td><td>Price snapshots</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-15</td><td>Accessibility + performance pass (fonts, CLS, contrast)</td><td>Audit after photography lands; keep text-first layout meanwhile</td><td>Do it now (premature before design settles)</td><td>Lighthouse run</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-17 <span class="badge-flag">P0</span></td><td>Resolve price/star-rating display vs API policy (FLG-023)</td><td>Apply for Creators/PA API; source prices + ratings through it (or Amazon-served links)</td><td>Remove displayed prices/ratings, keep "Check price on Amazon" CTAs</td><td>API approval (or owner risk acceptance)</td><td>Low</td><td><span class="badge-flag">Needs decision &mdash; compliance gate</span></td></tr>
<tr><td>SG-16</td><td>Campaign ledger review ritual</td><td>Weekly 15-minute review of <a href="methodology.html">the ledger</a> once reports exist</td><td>Monthly</td><td>First Associates report</td><td>Low</td><td>Proposed</td></tr>
</table></div>

<h2>Questions, information &amp; answers &mdash; what must be known before a reasonable decision</h2>
<p class="lede small">Each row: the question, what we know (with source), what is missing, exactly how to discover it, and which decision it blocks. This is the missing-information map.</p>
<div class="table-scroll"><table>
<tr><th>#</th><th>Question</th><th>What we know</th><th>What we do not know</th><th>How to discover it</th><th>Decision blocked</th></tr>
<tr><td>Q-01</td><td>Are the supplied short links compliant Special Links?</td><td>They resolve to the ASINs in the register (observed 2026-11-19); their redirect targets carry no tag= parameter (FLG-015)</td><td>Exact compliance status is unresolved &mdash; we do not claim they are invalid</td><td>Test in Associates Central; read <a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a> Participation Requirements</td><td>Scaling outbound links (SG-01)</td></tr>
<tr><td>Q-02</td><td>Is the tracking ID earning correctly?</td><td>Outbound URLs use <code>{TAG}</code>; constructed from official listing URLs</td><td>No clicks/orders attributed yet (no reports read)</td><td>Associates Central Earnings Report after the SG-01 test</td><td>Any revenue claim; campaign ledger rows</td></tr>
<tr><td>Q-03</td><td>What are thermometer dimensions &amp; remaining spec gaps?</td><td>Air fryer dims verified on all three listings; thermometer fields captured do not include dimensions (FLG-004)</td><td>Thermometer dimensions; any field behind "See more"</td><td>Re-fetch listing product-details sections; record date</td><td>Counter-space rows for thermometers</td></tr>
<tr><td>Q-04</td><td>Which wattage is right for the Chefman 8QT?</td><td>Listing bullets: 1000W (model RJ38-SQSS-8T). Listing Product information: 1700W (FLG-022)</td><td>Which figure is authoritative</td><td>Manufacturer spec sheet or seller support; check the box label</td><td>Wattage-based advice; SG-11</td></tr>
<tr><td>Q-05</td><td>Should we promote newer models instead?</td><td>Listings show newer variants (B0CNY1YVDD $59.99 4.6/7,602; B0GL7Z4KP4 $16.99 4.7/144 &mdash; snapshots 2026-11-19, FLG-003)</td><td>Margin, trajectory, whether the submitted ASINs stay available</td><td>Compare variant listings; Associates reports by ASIN</td><td>Product lineup (SG-08)</td></tr>
<tr><td>Q-06</td><td>What commission rates apply?</td><td>Tracking ID registered; session rules in <a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td><td>Category rates (not published here)</td><td>Associates Central Commission Income Statement (authorized report only)</td><td>Revenue forecasting (not done by design)</td></tr>
<tr><td>Q-07</td><td>Is there search demand for these topics?</td><td>Eight guides are question-shaped hypotheses; no volume claims made</td><td>Measured queries (Search Console not yet verified)</td><td>Verify property + submit sitemap (SG-02); then choose topics from queries</td><td>Publishing cadence priorities</td></tr>
<tr><td>Q-08</td><td>Can we use product photos?</td><td>No Amazon images used; SVG/CSS graphics only; Operating Agreement treats Program Content (incl. images) as licensed, not owned</td><td>Whether owner-shot or manufacturer-permitted photos are feasible</td><td>SG-04 decision; read <a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement</a> Program Content definition</td><td>Visual conversion work (SG-04)</td></tr>
<tr><td>Q-09</td><td>Where does analytics data live?</td><td>Client ships 5 events with local-only counts; endpoint code ready in <code>analytics-endpoint/</code></td><td>Hosting, retention window, privacy notice wording</td><td>Pick host (SG-03); publish retention policy on the compliance page</td><td>Measurement &amp; optimization loop</td></tr>
<tr><td>Q-10</td><td>How volatile are these prices?</td><td>Five snapshots on 2026-11-19 (Black Friday window) reproduced against live buy boxes in the integration pass</td><td>Price history beyond snapshot dates</td><td>Weekly snapshots (SG-12); Associates SiteStripe price display</td><td>Any "deal" framing beyond dated snapshots</td></tr>
<tr><td>Q-11</td><td>What converts visitors into buyers?</td><td>Design + content hypotheses only (DESIGN_PROMPT.md); zero measured behavior</td><td>Click-through and conversion by page/pick</td><td>Endpoint + ledger (SG-03, SG-16); Associates reports</td><td>Any optimization claim; layout prioritization</td></tr>
<tr><td>Q-12</td><td>Is the disclosure wording compliant?</td><td>Site now uses the exact Section 5 sentence (verified against the Operating Agreement 2026-11-19)</td><td>Nothing outstanding &mdash; keep it under review at each publish</td><td>Re-read Section 5 at each publish (compliance gate)</td><td>None currently</td></tr>
</table></div>
<p class="small">Reviewer: mark each SG item Approved / Rejected / Deferred with a date. Approved items move to COORDINATION.md as claimed tasks. Nothing here is a promise of traffic, ranking, or revenue. Irregularities found in the data are not fixed silently &mdash; they are listed on <a href="flagged.html">Flagged for review</a>.</p>
"""
UPSTREAM_SUGG = """
<section class="section">
<h2>Merged suggestion log from upstream sessions (kept verbatim)</h2>
<p class="lede">Sessions 2ec8638e, 8e82d03c and f0db58ea recorded their own boards before this review desk was rebuilt. Nothing here is dropped: IDs are kept exactly as those sessions wrote them, so design-brief.html and their records keep working. Some IDs overlap with the recommended-path board above (SG-11..17) but carry different text - treat each board as its own numbering space.</p>
<h2>Suggestions for review</h2>
<div class="table-scroll"><table>
<tr><th>#</th><th>Suggestion</th><th>Why it matters</th><th>Evidence needed</th><th>Effort</th><th>Status</th></tr>
<tr><td>SG-01</td><td>Validate one Special Link per product in Associates Central (SiteStripe) and confirm destination + tracking report</td><td>Proves outbound links earn correctly before scaling</td><td>Associates Central test clicks + report screenshots</td><td>Low (manual)</td><td><span class="badge-warn">Needs decision - gate</span></td></tr>
<tr><td>SG-02</td><td>Set canonical domain + Search Console + sitemap submission</td><td>One site to index; measured queries drive next topics</td><td>Domain choice; Search Console property</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-03</td><td>Deploy self-hosted analytics endpoint (5 events) + weekly ledger review</td><td>Turns clicks into decisions without third-party trackers</td><td>Hosting choice; retention policy</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-04</td><td>Licensed product photography (own photos or manufacturer permission)</td><td>Real photos convert; copied Amazon images risk IP breach</td><td>Licence / permission letters</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-05</td><td>Holiday gift guides (air fryer gifts, grill gifts) with dated price snapshots</td><td>Seasonal organic traffic; gift intent converts</td><td>Gift-angle verification per listing</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-06</td><td>"Which one is for you" chooser expansion (budget slider, counter-depth input)</td><td>Better decision support without fake testing</td><td>Usability feedback</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-07</td><td>Reader capture (email signup) with explicit consent</td><td>Owns audience beyond search</td><td>Provider + consent copy + FTC review</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-08</td><td>Newer-model watch (Chefman B0CNY1YVDD, ThermoMaven B0GL7Z4KP4)</td><td>Decide whether to promote newer variants or keep current ASINs</td><td>Variant comparison + margin check</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-09</td><td>Hands-on testing programme (buy, cook, photograph, publish)</td><td>Unlocks "lived-with" content competitors cannot copy</td><td>Budget, protocol, disclosure of free vs bought units</td><td>High</td><td>Proposed - do not claim until done</td></tr>
<tr><td>SG-10</td><td>Expand categories (second air fryer brand, second thermometer brand)</td><td>More comparison depth; better internal linking</td><td>New ASIN verification pass</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-11</td><td>Run the design brief (design-brief.html) as the brief for the visual overhaul: warm editorial brand, product-first hero, category tiles, sticky comparison bar</td><td>Turns the site from a register into a publication a buyer can act on; cuts the generated-template feel</td><td>Owner picks the visual direction from the brief's options; photography decision (SG-04) gates imagery</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-12</td><td>Adopt the eight-topic editorial calendar in the design brief as the publishing cadence (question-shaped titles tied to the verified products)</td><td>Catchy, spec-backed topics feed organic search; every title is a question a buyer types</td><td>Owner approves titles; each topic needs the same line-by-line verification before publishing</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-13</td><td>Anti-AI-slop writing rules in the CMS checklist: no filler transitions, no \"in conclusion\", varied sentence length, one idea per paragraph, first-person editorial voice where honest</td><td>Readers and reviewers can tell template text; signal-rich writing ranks and converts better</td><td>Style guide decision; editor review on every page</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-14</td><td>Editorial voice decision: who is \"we\" (The Countertop Guide editorial team) and what we will never claim (no testing, no trending, no superlatives)</td><td>A defined voice is the strongest anti-slop lever and keeps FTC honesty intact</td><td>Owner sign-off on voice statement</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr><td>SG-15</td><td>Reader-facing seasonal clusters (holiday gift, New Year cooking reset) built from the verified products with dated price snapshots</td><td>Seasonal intent searches; reuses verified data instead of new claims</td><td>Season calendar decision; re-snapshot prices at publish</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-16</td><td>Comparison-first homepage: lead with the side-by-side table and the three-question chooser above the fold, verification below</td><td>Buyers act on comparisons; the verification register moves below the products</td><td>Layout decision in the design brief</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-17</td><td>Add author bylines and an \"updated\" date to every article and comparison</td><td>Authorship and freshness signals; reads like a publication, not a template</td><td>Author name/bio decision; date source from verification log</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-18</td><td>Internal-link cluster pages: one pillar per category linking every guide to the comparison and buying guide</td><td>Cluster structure helps search engines and keeps readers on-site longer</td><td>Topic approval (SG-12); link audit at publish</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-19</td><td>Design-prompt pass: feed this board into a visual design prompt (publication layout, type scale, product-card anatomy, seasonal skins) and review mockups before shipping</td><td>Turns \"make it look like a shop\" into a reviewable artifact instead of ad-hoc CSS edits</td><td>Owner picks a direction from mockups</td><td>Medium</td><td><span class="badge-warn\">Needs decision</span></td></tr>
<tr><td>SG-20</td><td>Product-card redesign: photo slot (once licensed), price snapshot date on the card, one primary CTA, spec chips instead of prose bullets</td><td>Shoppers scan cards, they do not read audits; cards are the conversion surface</td><td>Photography decision (SG-04) or approved placeholder art</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-21</td><td>Editorial homepage modules: hero story, \"featured guide\" slot, category tiles, then the product line-up - ordered by reader intent, not by data pipeline</td><td>Publication feel; leads with products and questions, not verification process</td><td>None - content exists</td><td>Low</td><td><span class="badge-ok\">Shipped in this pass (front page rebuilt)</span></td></tr>
<tr><td>SG-22</td><td>Seasonal skins: holiday gift-guide banner and dated price-snapshot badge (e.g. Black Friday) that auto-expires</td><td>Seasonal relevance lifts click-through without inventing claims</td><td>Dated snapshot rule already approved (D-19)</td><td>Low</td><td>Proposed</td></tr>
<tr><td>SG-23</td><td>Article template upgrade: key-takeaways box, at-a-glance spec table, \"what the listing cannot tell you\" callout, related-products rail</td><td>Consistent reader-facing polish across guides; reduces AI-slop look</td><td>Voice guide already approved (D-12)</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-24</td><td>Comparison-table UX: sticky first column, mobile card stack, \"share comparison\" link, print stylesheet</td><td>Tables are the most-used dashboard surface; mobile is most traffic</td><td>Usability feedback after launch</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-25</td><td>Topic cluster plan: 8 spec-backed articles mapped to the 5 products (titles already drafted as hypotheses), each added to sitemap + feed at publish</td><td>Cluster internal linking is the organic-traffic engine; cadence keeps it measurable</td><td>Search Console data after SG-02 to re-rank priority</td><td>Medium</td><td>Proposed</td></tr>
<tr><td>SG-26</td><td>Trust bar under masthead: \"every fact sourced - see the register\" one-liner linking to verification.html on all pages</td><td>Turns the audit strength into a shopper-facing promise without leading with process</td><td>None</td><td>Low</td><td><span class="badge-ok\">Shipped in this pass</span></td></tr>
<tr><td>SG-27</td><td>Decide disclosure wording: verbatim Operating Agreement §5 or site-named variant</td><td>§5 requires "As an Amazon Associate I earn from qualifying purchases." or a substantially similar previously allowed statement</td><td>Compliance review of current variant</td><td>Low</td><td>Resolved 2026-11-19: verbatim wording adopted</td></tr>
<tr><td>SG-12</td><td>Resolve star-rating display path under Participation Requirement 6(t)</td><td>Displaying customer reviews/star ratings conditions on Creators API or PA API; site shows snapshots without either</td><td>Policy decision; API access check</td><td>Medium</td><td>Needs decision</td></tr>
</table></div>
<h2>Design suggestions - feed these into the visual design prompt</h2>
<p>These are the concrete art-direction inputs for SG-11. They describe what \"a polished marketing affiliate site, not AI slop\" means for this repository, so a design pass can be reviewed against them before any CSS ships.</p>
<div class="table-scroll"><table>
<tr><th>#</th><th>Design input</th><th>Why it counters the \"generated\" look</th><th>Constraint</th></tr>
<tr><td>DI-1</td><td>Publication masthead with wordmark, tagline and issue date (verification date), not a generic app bar</td><td>Real shops and magazines have a masthead; app bars read as scaffolding</td><td>Must keep disclosure strip directly beneath</td></tr>
<tr><td>DI-2</td><td>Editorial hero: one strong headline, one lede, two CTAs (shop / read) - no badge soup</td><td>Audits open with process; shops open with the offer</td><td>Badges limited to three: verified date, sponsored labeled, price-snapshot warning</td></tr>
<tr><td>DI-3</td><td>Product-card anatomy: image slot, name, star+count, price with list-price strike and snapshot date, 3 spec chips, one CTA, sponsored microcopy</td><td>Card = conversion unit; prose bullets inside cards are the biggest AI-slop tell</td><td>No product photo until SG-04 decides; use licensed placeholder or typographic tile</td></tr>
<tr><td>DI-4</td><td>Type scale: display serif for headlines, grotesque for UI, mono for ASINs and spec tables</td><td>Three-role type system is what separates publications from templates</td><td>Ship webfonts self-hosted or system stack - no render-blocking third party</td></tr>
<tr><td>DI-5</td><td>Color: warm paper background, one accent for CTAs, one for trust/verification, muted ink - not the default blue/purple gradient</td><td>Gradients + glow = generated; flat warm palette = printed catalogue</td><td>Contrast AA on all text (WCAG)</td></tr>
<tr><td>DI-6</td><td>Guide layout: key-takeaways box above the fold, at-a-glance table, honest \"what we cannot tell you\" callout, related-product rail at the end</td><td>Opinionated structure reads as edited; wall-of-text reads as generated</td><td>Every spec cell links to its listing (existing rule)</td></tr>
<tr><td>DI-7</td><td>Seasonal skin layer (holiday gift-guide banner) that sits on top of the base design and can be switched off</td><td>Shows the site is maintained on a calendar, like a real publication</td><td>Dated price snapshots only (D-19); no \"trending\" without a source</td></tr>
<tr><td>DI-8</td><td>Dashboard surfaces restyled as \"the back office\": denser type, tabular numbers, source links on every row - visually distinct from the shop</td><td>Keeps the audit machinery available without letting it set the tone</td><td>Same disclosure and sponsored rules as shopper pages</td></tr>
</table></div>
<p class="small\">Review flow: pick a direction from DI-1..DI-8 (approve / reject / defer each), then SG-11 turns the approved set into a design prompt and mockups. No CSS changes ship before that review.</p>
<h2>Questions, information &amp; answers needed before a reasonable decision</h2>
<div class="table-scroll"><table>
<tr><th>#</th><th>Question</th><th>What we know</th><th>What we do not know</th><th>How to discover it</th><th>Decision blocked</th></tr>
<tr><td>Q-01</td><td>Are the supplied short links compliant Special Links?</td><td>They resolve to the ASINs in the register (observed 2026-11-19)</td><td>Exact compliance status is unresolved</td><td>Test in Associates Central; read Operating Agreement + Policies</td><td>Scaling outbound links</td></tr>
<tr><td>Q-02</td><td>What is the canonical domain?</td><td>Canonical set to the GitHub Pages URL (<code>https://wingbangboozle1-lang.github.io/Prod1/</code>) across HTML, sitemap, robots and feed on 2026-11-19</td><td>Whether to move to a custom domain later</td><td>Owner decision; if custom domain chosen, update canonical + re-submit sitemap</td><td>Custom-domain SEO; Search Console property still not created</td></tr>
<tr><td>Q-03</td><td>What are thermometer dimensions &amp; Emeril wattage?</td><td>Air fryer dims verified; thermometer dims + Emeril wattage not captured</td><td>Missing fields (blank in tables)</td><td>Re-fetch listing product-details sections; record date</td><td>Counter-space table for thermometers; circuit advice</td></tr>
<tr><td>Q-04</td><td>Should we promote newer models instead?</td><td>Listings show newer variants (see Flagged)</td><td>Margin, rating trajectory, variant fit</td><td>Compare variant listings; check Associates reports</td><td>Product lineup</td></tr>
<tr><td>Q-05</td><td>What commission rates apply?</td><td>Tracking ID shopnow047c-20; session rules in Policies</td><td>Category rates (not published here)</td><td>Associates Central commission statement (authorized report only)</td><td>Revenue forecasting (not done)</td></tr>
<tr><td>Q-06</td><td>Is there search demand for these topics?</td><td>Guides are question-shaped hypotheses, not volume claims</td><td>Measured queries (no analytics yet)</td><td>Search Console after launch; choose next topics from data</td><td>Publishing cadence</td></tr>
<tr><td>Q-07</td><td>Can we use product photos?</td><td>No Amazon images used; SVG/CSS only</td><td>Licence / permission status</td><td>Manufacturer permission or own photography</td><td>Visual overhaul</td></tr>
<tr><td>Q-08</td><td>Where does analytics data live?</td><td>Local-only counter; endpoint stub documented</td><td>Hosting, retention, consent</td><td>Pick host; publish retention policy</td><td>Measurement &amp; optimisation</td></tr>
<tr><td>Q-09</td><td>Which visual direction from the design brief do we adopt?</td><td>Brief offers a warm editorial direction with three named options and anti-slop rules</td><td>Owner's pick; photography decision (Q-07) gates imagery</td><td>Review design-brief.html; choose one direction</td><td>Visual overhaul (SG-11)</td></tr>
<tr><td>Q-10</td><td>Do we approve the eight-topic editorial calendar?</td><td>Titles are working hypotheses tied to verified products; none is a popularity claim</td><td>Owner approval; per-topic verification still required</td><td>Review calendar on design-brief.html</td><td>Publishing cadence (SG-12)</td></tr>
<tr><td>Q-11</td><td>What is the site's editorial voice, and what will it never claim?</td><td>No testing / trending / superlative claims today; voice statement is proposed</td><td>Owner sign-off on the voice statement</td><td>Review voice rules on design-brief.html</td><td>All content (SG-13, SG-14)</td></tr>
<tr><td>Q-12</td><td>Should the homepage lead with the comparison and chooser?</td><td>Current homepage leads with categories then data</td><td>Layout preference; impact on conversion vs. trust</td><td>Review homepage layout option in the brief</td><td>Homepage redesign (SG-16)</td></tr>
<tr><td>Q-13</td><td>Who are the named authors, and what bios go with them?</td><td>Guides currently say \"The Countertop Guide editorial team\"</td><td>Author identity and bio wording</td><td>Owner provides names/bios or keeps the team credit</td><td>Authorship (SG-17)</td></tr>
<tr><td>Q-14</td><td>What is the review SLA for this suggestions board?</td><td>26 suggestions and 19 questions wait on owner choices</td><td>Review cadence and who approves</td><td>Owner sets a review rhythm; approved items become tasks</td><td>All pending suggestions</td></tr>
<tr><td>Q-15</td><td>Which design direction does the owner want?</td><td>Design inputs DI-1..DI-8 written; front page rebuilt editorial-first in this pass</td><td>Approved visual direction (type, color, card anatomy)</td><td>Review DI-1..DI-8 on this board plus design-brief.html; approve/reject/defer each; then SG-19 mockups</td><td>Full visual overhaul (SG-11, SG-19, SG-20)</td></tr>
<tr><td>Q-16</td><td>What imagery may we legally ship?</td><td>No Amazon images used; SVG/CSS only; og-image is a typographic SVG</td><td>Licensed photography or manufacturer permission status; whether placeholder tiles are acceptable long-term</td><td>Decide SG-04; if placeholders approved, specify style in design prompt</td><td>Product cards, social previews, conversion polish</td></tr>
<tr><td>Q-17</td><td>What is the publishing cadence and who approves topics?</td><td>Five guides exist; 8 topic hypotheses drafted; sitemap/feed updated at publish</td><td>Owner approval of calendar; reviewer for each article</td><td>Owner sets cadence (e.g. 2/week) and names reviewer in COORDINATION.md</td><td>SG-25 cluster build-out</td></tr>
<tr><td>Q-18</td><td>Which success metrics decide iteration?</td><td>Five events defined; campaign ledger empty by design; Search Console not yet connected</td><td>Owner's thresholds (e.g. N eligible sessions before topic re-rank; CTR target)</td><td>Owner sets thresholds after first month of Search Console + ledger data</td><td>Evidence-based iteration (Priority 4)</td></tr>
<tr><td>Q-19</td><td>Are the five short links the only promotion surface, or will more ASINs be added?</td><td>Five ASINs verified and shippable; newer variants noted (FLG-003, SG-08)</td><td>Scope of catalogue growth; margin/commission data per category</td><td>Owner sets catalogue scope; commission data only from Associates reports (Q-05)</td><td>SG-10 expansion; revenue planning</td></tr>
<tr><td>Q-20</td><td>Should the disclosure use the verbatim §5 wording?</td><td>Current variant names the site instead of \"I\"; check script flagged it for owner review</td><td>— (resolved)</td><td>Resolved 2026-11-19 against Operating Agreement §5: verbatim wording adopted on all pages</td><td>Disclosure wording</td></tr>
<tr><td>Q-10</td><td>May we display star ratings without Creators API / PA API?</td><td>Participation Requirement 6(t) conditions ratings display on those APIs; site shows listing snapshots</td><td>API access and eligibility</td><td>Policy decision (SG-12)</td><td>Ratings on product cards</td></tr>
<tr><td>Q-11</td><td>What cadence for re-snapshotting prices and ratings?</td><td>Last snapshot 2026-11-19; live values have since drifted</td><td>Re-fetch listings on a schedule; record each date</td><td>Owner sets cadence</td><td>Price/rating freshness</td></tr>
</table></div>
<p class="small">Reviewer: mark each SG item Approved / Rejected / Deferred with a date. Approved items move to COORDINATION.md as claimed tasks. Nothing here is a promise of traffic, ranking, or revenue.</p>
"""
sugg_body += "\n" + UPSTREAM_SUGG
write_page("suggestions.html", "Review Desk: Suggestions, Recommended Paths &amp; Open Questions | The Countertop Guide","The review desk: ranked suggestions with recommended paths and alternatives, plus the Q/I/A map of what must be discovered before each decision.",sugg_body)
# ---------- VERIFICATION ----------
ver_rows = ""
for pid in ["P1","P2","P3","P4","P5"]:
    p = PRODS[pid]
    dims_cell = esc(p["dimensions"]) if p["dimensions"] else '<span class="badge-flag">Blank &mdash; not shown in listing fields (FLG-004)</span>'
    ver_rows += f"""
<article class="card" id="{pid}">
<h3>{pid} &middot; {esc(p['shortName'])} &middot; ASIN {p['asin']}</h3>
<div class="table-scroll"><table>
<tr><th>Field</th><th>Value</th><th>Source</th></tr>
<tr><td>Submitted short link (as supplied)</td><td>{esc(p['submittedShortLink'])}</td><td>Owner brief</td></tr>
<tr><td>Intended ASIN <span class="meta">(kept separate from observed target)</span></td><td>{p['asin']}</td><td><a href="{p['officialListingUrl']}" rel="sponsored nofollow noopener" target="_blank">Official listing</a></td></tr>
<tr><td>Official listing URL</td><td>{esc(p['officialListingUrl'])}</td><td>Amazon.com</td></tr>
<tr><td>Observed redirect target <span class="meta">(separate field &mdash; do not merge)</span></td><td>{esc(p['observedRedirectTarget'])}</td><td>Observed 2026-11-19</td></tr>
<tr><td>Confirmation date / source</td><td>{p['confirmationDate']}</td><td>{esc(p['confirmationSource'])}</td></tr>
<tr><td>Title (as listed)</td><td>{esc(p['title'])}</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>Rating / count (snapshot)</td><td>{esc(p['rating'])} ({esc(p['ratingCount'])})</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing</a> &middot; re-read 2026-11-19</td></tr>
<tr><td>Price snapshot (new / list)</td><td>{esc(p['priceNew'])} / {esc(p['priceList'])}</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing buy box</a> &middot; re-read 2026-11-19</td></tr>
<tr><td>Dimensions</td><td>{dims_cell}</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing spec table</a></td></tr>
<tr><td>Capacity (title / field)</td><td>{esc(p['capacityTitle'])} / {esc(p['capacityField'])}</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>Wattage</td><td>{esc(p['wattage']) if p['wattage'] else '<span class="badge-flag">Blank &mdash; not captured</span>'}</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>Warranty</td><td>{esc(p['warranty']) if p['warranty'] else '<span class="badge-flag">Blank &mdash; not captured</span>'}</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>Special features</td><td>{esc(p['specialFeatures'])}</td><td><a href="{p['sourceUrl']}" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>Affiliate URL used on site</td><td>{esc(aff(p))} (rel="sponsored")</td><td>Constructed: official URL + tag {TAG}</td></tr>
</table></div>
<p class="small">{esc(p['sourceNote'])}</p>
</article>"""
ver_body = f"""
<p class="eyebrow">Verification register</p>
<h1>Line-by-line verification: every fact, its source</h1>
<p class="lede">Rule: every table row has a source link to an official site. If a value cannot be confirmed, it is left blank and flagged &mdash; never inferred. Intended ASIN and observed redirect target are stored in separate fields and never merged. Integration re-verification pass: {VERIFIED} (this session's review log: <a href="https://github.com/wingbangboozle1-lang/Prod1/tree/main/review/2d5ebe5b">review/2d5ebe5b</a>).</p>
<h2>Product-intent confirmation record</h2>
{ver_rows}
<h2>Integration re-verification summary ({VERIFIED})</h2>
<div class="table-scroll"><table>
<tr><th>Check</th><th>Result</th><th>Source</th></tr>
<tr><td>Associates disclosure sentence (Operating Agreement &sect;5)</td><td>Exact sentence confirmed and now used verbatim on every page</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement</a> (updated 2025-10-15)</td></tr>
<tr><td>P1 buy box + list price ($79.93 / $99.99)</td><td>Reproduced twice on the live listing &mdash; resolves the earlier price doubt</td><td><a href="https://www.amazon.com/dp/B0CDY277D3" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>All five buy boxes and list prices</td><td>Match the register (P2 rating count updated 18,371&rarr;18,375; P3 16,890&rarr;16,892 &mdash; snapshot drift)</td><td>Each listing above</td></tr>
<tr><td>Air fryer dimensions</td><td>Match the register on all three listings</td><td>Each listing's spec table</td></tr>
<tr><td>P2 wattage (previously blank)</td><td>Found: 1700 W / 120 V in Product information &mdash; field filled</td><td><a href="https://www.amazon.com/dp/B09B7SB46R" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>P3 wattage</td><td>On-listing conflict: bullets 1000 W vs Product information 1700 W &mdash; both shown, FLG-022</td><td><a href="https://www.amazon.com/dp/B08DKYBTPH" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>P2 accessory count</td><td>On-listing conflict: title/item-details 6 vs description 7 &mdash; FLG-021</td><td><a href="https://www.amazon.com/dp/B09B7SB46R" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>Preset count P2 (24 vs 25)</td><td>Conflict re-confirmed on the live listing (FLG-002)</td><td><a href="https://www.amazon.com/dp/B09B7SB46R" rel="sponsored nofollow noopener" target="_blank">Listing</a></td></tr>
<tr><td>Thermometer dimensions</td><td>Not present in listing fields captured &mdash; remain blank (FLG-004)</td><td>Each listing above</td></tr>
</table></div>
<h2>Policy sources (official)</h2>
<div class="table-scroll"><table>
<tr><th>Source</th><th>What it governs</th><th>Link</th></tr>
<tr><td>Amazon Associates Operating Agreement (updated 2025-10-15)</td><td>Special Links must properly use tagged link formats; Program Content definition; &sect;5 disclosure sentence</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement</a></td></tr>
<tr><td>Amazon Associates Program Policies</td><td>Commission session rules; participation requirements (link destination transparency)</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td></tr>
<tr><td>FTC Disclosures 101 for Social Media Influencers (Nov 2019)</td><td>Material-connection disclosure: hard to miss, simple clear language</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td></tr>
<tr><td>FTC Endorsements, Influencers &amp; Reviews guidance</td><td>Endorsement context and review integrity</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td></tr>
</table></div>
<p class="small">Prices and ratings are snapshots and will change. The manual Special Link test in Associates Central remains an open gate (<a href="flagged.html">FLG-001</a>); it is a manual owner step and is not claimed as done.</p>
"""
write_page("verification.html", "Verification Register: Line-by-Line Sources for Every Fact | The Countertop Guide","Verification register for five products: intended ASIN, listing URL, confirmation date and source per product, integration re-verification results, and official Amazon/FTC policy sources.",ver_body)
# ---------- FLAGGED ----------
flag_body = f"""
<p class="eyebrow">Flagged for review</p>
<h1>Flagged for review &mdash; irregularities &amp; unverified items</h1>
<p class="lede">Flagged items do not block publishing, but they block claims. Nothing below is presented as fact on product pages. Review after launch and request changes. (Updated {VERIFIED}: FLG-005 partially resolved, FLG-021 and FLG-022 added from the integration re-verification.)</p>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Item</th><th>Detail</th><th>Action</th></tr>
<tr><td>FLG-001</td><td>Short-link compliance unresolved</td><td>Supplied link.amazon short links resolve to the ASINs, but their exact compliance status as Special Links is unresolved. We do not claim they are invalid. Site outbound buttons use official listing URLs + tag instead.</td><td>Manual test in Associates Central (SG-01)</td></tr>
<tr><td>FLG-002</td><td>Preset &amp; capacity discrepancies</td><td>Emeril: title 24 presets vs bullets 25 (re-confirmed {VERIFIED}); title 26QT vs field 24.6 liters. Chefman 6QT: title 6 Quart vs field 6 liters. Both values shown; no silent conversion.</td><td>Verify on listing; ask seller if needed</td></tr>
<tr><td>FLG-003</td><td>Newer models shown on listings</td><td>Chefman 8QT page shows newer 6QT B0CNY1YVDD ($59.99, 4.6/7,602); ThermoMaven page shows newer Orange B0GL7Z4KP4 ($16.99, 4.7/144) - snapshots {VERIFIED}. We promote the submitted ASINs only.</td><td>Decide lineup (SG-08)</td></tr>
<tr><td>FLG-004</td><td>Missing dimensions (thermometers)</td><td>ThermoMaven B0DHZTCNR5 and CHEF iQ B0DZFD6R9Z dimensions are not present in the listing fields captured ({VERIFIED} re-read). Left blank in tables.</td><td>Re-fetch product-details "See more"; record date</td></tr>
<tr><td>FLG-005</td><td>P2 wattage/warranty gap &mdash; partially resolved</td><td>Wattage found {VERIFIED}: 1700 W / 120 V (Product information) - now in the register. Warranty: the listing links a warranty PDF but states no term in the page text.</td><td>Open the warranty PDF for the term</td></tr>
<tr><td>FLG-006</td><td>Price volatility</td><td>All prices are {VERIFIED} snapshots (Black Friday window). Every one was reproduced against its live buy box in the integration pass. Live price on Amazon governs.</td><td>Weekly re-snapshot (SG-12); date every price</td></tr>
<tr><td>FLG-007</td><td>Canonical domain &mdash; resolved to Pages URL</td><td>Canonical/og URLs now use https://wingbangboozle1-lang.github.io/Prod1/ in the generator and data (the earlier placeholder regressed via <code>build_site.py</code>; fixed at the source {VERIFIED}). A custom domain remains optional (SG-13).</td><td>Optional: custom domain later</td></tr>
<tr><td>FLG-008</td><td>Analytics endpoint not deployed</td><td>Five events defined; local counter only. The self-hosted endpoint ships as code (<code>analytics-endpoint/server.py</code>) but needs an HTTPS host.</td><td>Deploy endpoint (SG-03)</td></tr>
<tr><td>FLG-009</td><td>No product photography</td><td>No Amazon images used (Program Content is licensed, not owned - Operating Agreement &sect;1). SVG/CSS illustrations only; generated or copied product photography is not used (S-18).</td><td>Licence decision (SG-04)</td></tr>
<tr><td>FLG-010</td><td>No hands-on testing</td><td>We have not cooked with or calibrated any product. No "lived-with" claims made.</td><td>Testing programme if approved (SG-09)</td></tr>
<tr><td>FLG-011</td><td>No commission / revenue claims</td><td>Rates not published; ledger empty until authorized reports arrive.</td><td>Record only from Associates reports</td></tr>
<tr><td>FLG-012</td><td>No trending / popularity claims</td><td>"Bought in past month" badges are listing snapshots, not our ranking. We do not claim trending.</td><td>Evidence rule: dated snapshot or no claim</td></tr>
<tr><td>FLG-013</td><td>Submitted link codes are 9 characters</td><td>Each submitted link.amazon path code (e.g. B04G1MEwY) is 9 characters. Each code resolves to a listing whose ASIN differs from the code, so the code is not used as an intended ASIN. Intended ASIN fields carry the confirmed listing ASIN with date and source in the register (session 9b748801, 2026-11-19).</td><td>Submitter confirms intended ASIN per link</td></tr>
<tr><td>FLG-014</td><td>ASIN 10-character rule: third-party sources only</td><td>The 10-character ASIN format was found on third-party guides, not on an Amazon help page. Used only to flag the 9-character codes.</td><td>Find an official Amazon help page for the ASIN definition</td></tr>
<tr><td>FLG-015</td><td>Redirect targets carry no tag=</td><td>The final URLs of the five supplied links (read 2026-11-19) contain no tag= parameter. Attribution to {TAG} is not observed on the redirect path. Site buttons use tagged listing URLs (FLG-001).</td><td>Associates tracking-report test per product (SG-01)</td></tr>
<tr><td>FLG-016</td><td>Listing pages carry widget data for other ASINs</td><td>Listing pages include "Customers who viewed" carousels and sponsored blocks with prices and ratings for other products (e.g. $74.99 for a different Chefman). Not used as data for the five products.</td><td>Use only each product's own fields</td></tr>
<tr><td>FLG-017</td><td>External register: three links vs five</td><td>The external Zone4 decision log (D-13) refers to three supplied links; this brief supplies five. Its statuses are not carried into this site.</td><td>Reconcile external register with the five links</td></tr>
<tr><td>FLG-018</td><td>Proposed Amazon content notice (not verified)</td><td>An external decision log proposes a notice citing IP License 2(k). The IP License text was not read in full; the notice is not on the pages.</td><td>Read IP License 2(k); decide under SG-04</td></tr>
<tr><td>FLG-019</td><td>Creators API prerequisites not read</td><td>An external log suggests the Creators API for prices/ratings. Prerequisites were not read; no API data is used on this site.</td><td>Read prerequisites before any source change</td></tr>
<tr><td>FLG-020</td><td>Main-product values re-read &mdash; resolved {VERIFIED}</td><td>The integration pass re-read all five listings: buy boxes, list prices, ratings, dimensions, capacity fields, wattage and bullets. Two rating counts drifted (P2 18,371&rarr;18,375; P3 16,890&rarr;16,892) and were updated with the date. P1's previously doubted price ($79.93/$99.99) reproduced twice.</td><td>Close; keep weekly cadence (SG-12)</td></tr>
<tr><td>FLG-021</td><td>Emeril accessory count conflict (new {VERIFIED})</td><td>The B09B7SB46R listing says "Six Cooking Accessories Included" (title) and lists six in item details (rack, bake pan, drip tray, crisper basket, rotisserie spit, fetch tool), but its product description says "7 premium accessories" and configuration says "7 Accessories".</td><td>Ask seller; show six with the conflict noted</td></tr>
<tr><td>FLG-022</td><td>Chefman 8QT wattage conflict (new {VERIFIED})</td><td>The B08DKYBTPH listing bullets say "1000 Watts/120 Volts - RJ38-SQSS-8T" while the same page's Product information table says 1700 watts. Both values are published side by side; neither is silently dropped.</td><td>Confirm with manufacturer (SG-11)</td></tr>
<tr><td>FLG-023 <span class="badge-flag">P0</span></td><td>Price and star-rating display vs API policy (new {VERIFIED} - read verbatim in the Program Policies)</td><td>Participation Requirements &sect;2: "your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API". &sect;6(t): "You will not display or otherwise use any of our customer reviews or star ratings ... unless you have obtained a link to that customer review or star rating through Creators API or PA API". This site currently shows dated manual snapshots of prices and ratings - neither Amazon-served nor API-sourced. The brief's evidence rule (dated snapshots, sourced rows) is satisfied, but the Program Policies condition is NOT satisfied as written. Remediation options: (1) apply for Creators/PA API and source prices+ratings through it (recommended); (2) remove displayed prices and star ratings and keep only "Check price on Amazon" CTAs; (3) owner accepts the risk while the application is pending. Owner decision - see Review desk.</td><td>Owner picks 1-3 (SG-17); do not scale traffic until resolved</td></tr>
<tr><td>FLG-024</td><td>Price-tracking functionality check (&sect;6(y))</td><td>Participation Requirements &sect;6(y): "your Site must not have price tracking and/or price alerting functionality" (unless otherwise agreed). Checked {VERIFIED}: the site has no user-facing price tracking or alerting; dated snapshots are static editorial records. No action needed unless a tracker/alert feature is ever added.</td><td>Keep under review at each publish</td></tr>
<tr><td>FLG-025</td><td>Flag numbering note (merge with session 8e82d03c)</td><td>Session 8e82d03c's register used different numbers for different items: its FLG-021 = disclosure variant (now closed - exact &sect;5 sentence on every page), its FLG-022 = price/star display vs API policy (carried here as FLG-023 with the verbatim text read {VERIFIED}), its FLG-024 = rating snapshot drift (covered by FLG-020). This register's FLG-021 = accessory-count conflict, FLG-022 = wattage conflict. Numbers are unique within this register only.</td><td>Reference note</td></tr>
</table></div>
"""
write_page("flagged.html", "Flagged for Review: Irregularities &amp; Unverified Items | The Countertop Guide","Flagged irregularities: short-link compliance, listing discrepancies (presets, accessories, wattage), newer models, missing fields, and launch gates - updated after line-by-line re-verification.",flag_body)
# ---------- COMPLIANCE ----------
comp_body = f"""
<p class="eyebrow">Compliance gate</p>
<h1>Disclosures &amp; policy checks in the publishing workflow</h1>
<p class="lede">Disclosure above the fold on every page (and repeated in the footer), using the exact sentence the Operating Agreement specifies. Every outbound product link is marked sponsored. Endorsement context is reviewed against the Operating Agreement and FTC guidance before publishing.</p>
<h2>Our disclosure (verbatim, every page)</h2>
<blockquote>{DISCLOSE}</blockquote>
<p class="small">Source: <a href="https://affiliate-program.amazon.com/help/operating/agreement">Associates Program Operating Agreement</a>, Section 5 ("Identifying Yourself as an Associate"), which requires: &ldquo;{DISCLOSE}&rdquo; &mdash; or any substantially similar statement previously allowed. We use the exact sentence. Verified {VERIFIED}.</p>
<h2>How each outbound link is marked</h2>
<ul>
<li>URL format: <code>https://www.amazon.com/dp/ASIN?tag={TAG}</code> (official listing URL + tracking ID).</li>
<li>Attributes: <code>rel="sponsored nofollow noopener"</code>, <code>target="_blank"</code>, visible "sponsored" label and "opens amazon.com" text so destination is never obscured.</li>
<li>Short links are recorded in the <a href="verification.html">verification register</a> as submitted links with observed redirect targets in a separate field. They are not used as outbound buttons.</li>
</ul>
<h2>Policy checklist (reviewed {VERIFIED})</h2>
<div class="table-scroll"><table>
<tr><th>Check</th><th>Source</th><th>Our practice</th></tr>
<tr><td>Use proper tagged Special Link formats</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement &sect;1</a></td><td>Official URL + tag; manual SiteStripe test is an open gate (FLG-001)</td></tr>
<tr><td>State the Section 5 disclosure clearly and prominently</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement &sect;5</a></td><td>Exact sentence above the fold on every page + footer</td></tr>
<tr><td>Do not obscure link destination</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td><td>Button text + ASIN + "opens amazon.com" on every card</td></tr>
<tr><td>Disclose material connection, hard to miss</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td><td>Strip under masthead on every page + footer; simple language</td></tr>
<tr><td>Endorsement honesty; no unsubstantiated claims</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td><td>No testing/trending claims; seller claims attributed ("per listing")</td></tr>
<tr><td>Program Content / images</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement &sect;1</a></td><td>No Amazon images copied; SVG/CSS graphics only until a licence decision (SG-04)</td></tr>
<tr><td>Publishing gate in the deploy workflow</td><td><code>scripts/check_site.mjs</code></td><td>Disclosure, sponsored links, internal links, unique titles/descriptions, claim wording &mdash; runs before Pages upload</td></tr>
<tr><td><strong>Price &amp; rating display must come from Amazon-served links or the Creators/PA API</strong></td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Participation Requirements &sect;2</a></td><td><span class="badge-flag">Open &mdash; FLG-023</span> currently dated manual snapshots; owner decision required (API application or removal)</td></tr>
<tr><td><strong>Customer reviews / star ratings only via Creators/PA API</strong></td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Participation Requirements &sect;6(t)</a></td><td><span class="badge-flag">Open &mdash; FLG-023</span> same decision as above</td></tr>
<tr><td>No price tracking or price-alerting functionality</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Participation Requirements &sect;6(y)</a></td><td>Checked &mdash; none present (FLG-024)</td></tr>
</table></div>
<h2>API policy check (run {VERIFIED})</h2>
<p>The Program Policies condition price and star-rating display on Amazon-served links or Creators/PA API data. This site's snapshots were read manually from the listings, so that condition is <strong>not</strong> met as written &mdash; recorded as <a href="flagged.html">FLG-023</a> with the verbatim text and three remediation options at the <a href="suggestions.html">review desk</a>. Until it is resolved, do not scale traffic to the site.</p>
<p class="small">This page is a publishing checklist, not legal advice. Review disclosure placement and endorsement context against the current Agreement and FTC guidance at each publish. If in doubt, flag it.</p>
"""
write_page("compliance.html", "Compliance: Disclosures &amp; Amazon/FTC Policy Checks | The Countertop Guide","Compliance gate: exact Section 5 disclosure wording, sponsored-link marking, and the Amazon Associates + FTC policy checklist reviewed before publishing.",comp_body)
# ---------- METHODOLOGY ----------
meth_body = f"""
<p class="eyebrow">Method</p>
<h1>How we verify, measure, and decide &mdash; without hallucinating</h1>
<p class="lede">Automate what can be automated; put a gate in front of what cannot. This page is the machinery: evidence rules, analytics events, the empty campaign ledger, and the publishing cadence.</p>
<h2>Evidence rule</h2>
<ul>
<li>Every product fact links to its Amazon listing and <a href="verification.html">verification record</a>. Missing = blank + flagged.</li>
<li>"Trending" / popularity claims require a dated snapshot from an official source. We make none; listing badges ("N bought in past month") are quoted only as dated listing snapshots.</li>
<li>Seller claims are attributed ("per listing"). Derived math shows its method. Prices always carry a snapshot date.</li>
<li>Where a listing contradicts itself, both values are published with the conflict flagged &mdash; never silently resolved (FLG-002, FLG-021, FLG-022).</li>
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
<p>Implementation: <code>assets/app.js</code> counts locally in <code>localStorage</code> and beacons to a configurable endpoint (<code>data-analytics-endpoint</code> on each page, currently empty). No third-party trackers, no cookies, no IPs stored. The self-hosted endpoint ships as code in <code>analytics-endpoint/server.py</code> (privacy notes in <code>analytics-endpoint/README.md</code>); deploying it is SG-03 at the <a href="suggestions.html">review desk</a>. Until then, counts are device-local and the ledger stays empty.</p>
<h2>Campaign ledger (empty by design)</h2>
<div class="table-scroll"><table>
<tr><th>Date</th><th>Source</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th><th>Reported orders</th><th>Provenance</th></tr>
<tr><td colspan="7"><em>No rows yet. Add timestamp, source, channel, eligible sessions, clicks and reported orders only when obtained from authorized first-party reports (Associates Central). No conversion score or revenue forecast is presented.</em></td></tr>
</table></div>
<h2>Publishing cadence &amp; topic calendar</h2>
<p>New guides are added to <code>sitemap.xml</code> and <code>feed.xml</code> at publish (both are generated by <code>build_site.py</code> with deterministic dates). The calendar: one question-shaped guide per week through the holiday window (SG-05), chosen from the approved clusters &mdash; air fryer choosing, thermometers, seasonal. The next topic after measurement starts comes from measured Search Console queries, not instinct. RSS feed: <a href="feed.xml">feed.xml</a>. Sitemap: <a href="sitemap.xml">sitemap.xml</a>.</p>
<h2>Publishing gate</h2>
<p><code>scripts/check_site.mjs</code> runs in the Pages workflow before deploy and fails the build on: missing/disclosure-below-fold, Amazon links without rel="sponsored", broken internal links, duplicate or missing titles/descriptions, and banned claim wording ("bestseller", "top rated", "#1", "guaranteed", "most popular"). Automate the mechanical; gate the judgment.</p>
"""
write_page("methodology.html", "Method: Verification, Analytics Events &amp; Campaign Ledger | The Countertop Guide","Method page: evidence rules, five privacy-preserving analytics events, the empty campaign ledger with provenance rules, publishing cadence and the automated publishing gate.",meth_body)
# ---------- SEARCH ----------
search_body = """
<p class="eyebrow">Search</p>
<h1>Search the site</h1>
<form id="search-page-form" role="search">
  <label for="search-input">Search guides &amp; products</label>
  <input id="search-input" type="search" placeholder="Try capacity, thermometer, wattage or gifts">
  <button class="btn" type="submit">Search</button>
</form>
<div id="search-results" aria-live="polite"></div>
<p><a href="guides.html">Guides</a> &middot; <a href="compare.html">Compare</a> &middot; <a href="air-fryers.html">Air fryers</a> &middot; <a href="thermometers.html">Thermometers</a></p>
"""
write_page("search.html", "Search Guides &amp; Products | The Countertop Guide","Search The Countertop Guide: air fryers, thermometers, capacity, cleanup, counter space, wattage, accuracy and holiday gift guides.",search_body)
idx = [
 {"title":"Home: air fryers & thermometers compared","url":"index.html","text":"Five verified products, two categories, sourced numbers, dated price snapshots. Compare all five, read the guides, use the chooser."},
 {"title":"Air fryers category","url":"air-fryers.html","text":"Chefman 6QT dual-basket, Emeril 26QT French-door oven, Chefman 8QT TurboFry. Capacity, footprint, wattage, cleanup, price snapshots."},
 {"title":"Thermometers category","url":"thermometers.html","text":"ThermoMaven 1-second instant-read vs CHEF iQ Sense wireless 3-probe. Accuracy claims, NIST NSF, range, probes."},
 {"title":"Compare all five","url":"compare.html","text":"Side-by-side table, 3-question chooser, counter-space analysis, capacity per cm depth, sticky price bar."},
 {"title":"Basket or oven-style air fryer: what should you compare?","url":"guide-basket-vs-oven.html","text":"Dual-basket vs French-door oven vs single basket. Two-dish cooking, crowd capacity, counter depth."},
 {"title":"A no-hype checklist for comparing air fryer capacity","url":"guide-capacity-checklist.html","text":"Quarts vs litres, single vs dual baskets, feeds 4-6, rotisserie and pizza claims."},
 {"title":"How to assess cleanup and counter-space trade-offs","url":"guide-cleanup-counter-space.html","text":"Dishwasher-safe baskets, footprint math, capacity per centimetre of counter depth."},
 {"title":"Questions to ask before buying a multi-function kitchen appliance","url":"guide-multifunction-questions.html","text":"Presets, accessories, wattage, warranty and fit checklist for multi-function ovens."},
 {"title":"Instant-read or wireless? How to read accuracy claims","url":"guide-thermometer-accuracy.html","text":"Plus-minus 0.5F, NIST NSF, sensor counts, WiFi range. How to read thermometer claims."},
 {"title":"The holiday hosting test: which air fryer feeds a crowd?","url":"guide-holiday-hosting.html","text":"Holiday hosting, two dishes at once, rotisserie and pizza claims, counter-depth math, return windows."},
 {"title":"Kitchen gifts under $25, $80 and $150","url":"guide-gifts-by-budget.html","text":"Holiday gift tiers from verified price snapshots. Stocking stuffer to showstopper."},
 {"title":"Will it trip the breaker? Wattage and outlet math","url":"guide-wattage-outlets.html","text":"Air fryer wattage, 120V circuits, the Chefman 8QT wattage conflict, how to verify any listing."},
 {"title":"Holiday air fryer gifts: what to buy for every kind of cook","url":"guide-holiday-gifts.html","text":"Gift picks matched to the cook: couples, crowds, small kitchens, thermometer stocking stuffers."},
 {"title":"Roast like a pro: instant-read or wireless for holiday roasts?","url":"guide-holiday-roast.html","text":"Thermometer accuracy claims read before the holiday roast."},
 {"title":"Small kitchen, big appetite: air fryers under 34 cm of counter depth","url":"guide-small-kitchen.html","text":"Depth and footprint comparison for tight counters, capacity per centimetre derived."},
 {"title":"All buying guides","url":"guides.html","text":"Eleven question-shaped guides in three clusters: air fryers, thermometers, seasonal."},
 {"title":"Dashboard hub","url":"dashboard.html","text":"Every dashboard surface in one place: verification register, flagged for review, compliance, method and campaign ledger, executive summary, suggestions board."},
 {"title":"Executive summary","url":"executive-summary.html","text":"What the site is, what is verified, compliance posture, measurement plan, decision gates."},
 {"title":"Review desk: suggestions and decisions","url":"suggestions.html","text":"Ranked suggestions SG-01 to SG-16 with recommended paths; Q-01 to Q-12 missing-information map."},
 {"title":"Verification register","url":"verification.html","text":"Line-by-line sources, intended ASIN vs observed redirect, confirmation dates, integration re-verification."},
 {"title":"Flagged for review","url":"flagged.html","text":"Irregularities FLG-001 to FLG-022: short-link compliance, listing conflicts, missing fields, launch gates."},
 {"title":"Compliance","url":"compliance.html","text":"Exact Section 5 disclosure, sponsored-link marking, Amazon and FTC policy checklist."},
 {"title":"Method and campaign ledger","url":"methodology.html","text":"Evidence rules, five analytics events, empty campaign ledger, publishing cadence, publishing gate."},
]
json.dump(idx, open("data/search-index.json","w"), indent=2)
# ---------- SITEMAP + FEED (deterministic) ----------
pages = [x["url"] for x in idx]
lastmod = VERIFIED
urls = "\n".join(f"  <url><loc>{CANON}/{u}</loc><lastmod>{lastmod}</lastmod></url>" for u in pages)
open("sitemap.xml","w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")
feed_items = ""
for u in ["guide-holiday-hosting.html","guide-gifts-by-budget.html","guide-holiday-gifts.html","guide-holiday-roast.html","guide-wattage-outlets.html","guide-small-kitchen.html","guide-basket-vs-oven.html","guide-capacity-checklist.html","guide-cleanup-counter-space.html","guide-multifunction-questions.html","guide-thermometer-accuracy.html"]:
    t = next(x["title"] for x in idx if x["url"] == u)
    dsc = next(x["text"] for x in idx if x["url"] == u)
    feed_items += f"""    <item>
      <title>{esc(t)}</title>
      <link>{CANON}/{u}</link>
      <guid isPermaLink="true">{CANON}/{u}</guid>
      <description>{esc(dsc)}</description>
      <pubDate>Thu, 19 Nov 2026 00:00:00 +0000</pubDate>
    </item>
"""
open("feed.xml","w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>The Countertop Guide</title>
    <link>{CANON}/</link>
    <description>Spec-backed comparisons from Amazon listings: air fryers and meat thermometers. Sponsored links labeled; snapshots dated.</description>
    <language>en-us</language>
    <lastBuildDate>Thu, 19 Nov 2026 00:00:00 +0000</lastBuildDate>
{feed_items}  </channel>
</rss>
""")
open("robots.txt","w").write(f"""User-agent: *
Allow: /
Sitemap: {CANON}/sitemap.xml
""")
print("pages written")
# Post-step: mark every amazon.com citation link as sponsored (consistency: every outbound product link sponsored)
import glob as _g, re as _r
for _f in _g.glob("*.html"):
    _s = open(_f).read()
    _s2 = _r.sub(r'(<a href="https://www\.amazon\.com/dp/[^"]*")>', r'\1 rel="sponsored nofollow noopener" target="_blank">', _s)
    if _s2 != _s:
        open(_f, "w").write(_s2)
print("sponsored post-step done")
