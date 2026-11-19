import json, html
D = json.load(open("data/products.json"))
SITE = D["site"]
PRODS = {p["id"]: p for p in D["products"]}
VERIFIED = SITE["verifiedDate"]
TAG = SITE["trackingId"]
# Canonical base for every page. Session arena/2ec8638e-prod1 (2026-11-19) replaced the
# placeholder https://example.com/ with the live GitHub Pages URL across all HTML; the
# generator must reproduce the committed pages, so the value lives here, not inline.
CANONICAL = "https://wingbangboozle1-lang.github.io/Prod1/"
def esc(s): return html.escape(str(s), quote=True)
def aff(p): return f"https://www.amazon.com/dp/{p['asin']}?tag={TAG}"
def product_card(pid, bullets_n=3):
    p = PRODS[pid]
    bl = "".join(f"<li>{esc(b)}</li>" for b in p["bullets"][:bullets_n])
    dims = esc(p["dimensions"]) if p["dimensions"] else '<span class="badge-flag">Dimensions not yet verified - see Flagged</span>'
    return f"""
<article class="card" id="{pid}">
  <span class="tag">{esc(p['category'])} - {esc(p['form'])}</span>
  <h3>{esc(p['shortName'])}</h3>
  <p><span class="stars">&#9733; {esc(p['rating'])}</span> <span class="meta">({esc(p['ratingCount'])} ratings on Amazon - snapshot {VERIFIED})</span></p>
  <p><span class="price">{esc(p['priceNew'])}</span> <span class="listprice">{esc(p['priceList'])}</span> <span class="meta">List price shown on listing - check live price on Amazon</span></p>
  <ul>
    <li><strong>Capacity (title):</strong> {esc(p['capacityTitle'])}</li>
    <li><strong>Dimensions (listing):</strong> {dims}</li>
    <li><strong>Special features:</strong> {esc(p['specialFeatures'])}</li>
  </ul>
  <ul>{bl}</ul>
  <p><a class="btn" href="{aff(p)}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{p['asin']}">Check price on Amazon - sponsored</a></p>
  <p class="sponsored-note">Sponsored link - Opens amazon.com - ASIN {p['asin']} - <a href="verification.html#{pid}">Verify this listing</a></p>
</article>"""
NAV = """<nav class="nav" aria-label="Main">
  <a href="index.html">Home</a>
  <a href="air-fryers.html">Air Fryers</a>
  <a href="thermometers.html">Thermometers</a>
  <a href="compare.html">Compare</a>
  <a href="guides.html">Guides</a>
  <a href="dashboard.html">Dashboard</a>
</nav>
<form class="searchbox" id="site-search-form" role="search">
  <label class="skip" for="site-search-input">Search the site</label>
  <input id="site-search-input" type="search" placeholder="Search guides &amp; products" aria-label="Search the site">
  <button class="btn small secondary" type="submit">Search</button>
</form>"""
FOOTER = f"""
<footer>
  <div class="disclosure-strip">Disclosure: As an Amazon Associate, The Countertop Guide earns from qualifying purchases. <a href="compliance.html">How we disclose</a></div>
  <div class="footer-inner">
    <div>
      <p><strong>The Countertop Guide</strong> - spec-backed comparisons from Amazon listings. We do not claim hands-on testing we have not done. Every product fact links to its Amazon listing and verification record.</p>
      <p class="small">Prices are snapshots from {VERIFIED} and change. Always confirm price, variant and fit on Amazon before buying.</p>
    </div>
    <nav aria-label="Shop"><p><strong>Shop</strong></p><p><a href="air-fryers.html">Air Fryers</a><br><a href="thermometers.html">Thermometers</a><br><a href="compare.html">Compare all five</a></p></nav>
    <nav aria-label="Guides"><p><strong>Guides</strong></p><p><a href="guides.html">All guides</a><br><a href="guide-basket-vs-oven.html">Basket or oven-style?</a><br><a href="guide-capacity-checklist.html">Capacity checklist</a><br><a href="guide-cleanup-counter-space.html">Cleanup &amp; counter space</a></p></nav>
    <nav aria-label="Trust"><p><strong>Trust &amp; data</strong></p><p><a href="dashboard.html">Dashboard hub</a><br><a href="verification.html">Verification register</a><br><a href="flagged.html">Flagged for review</a><br><a href="compliance.html">Compliance</a><br><a href="methodology.html">Method &amp; campaign ledger</a><br><a href="executive-summary.html">Executive summary</a><br><a href="design-brief.html">Design brief</a><br><a href="suggestions.html">Suggestions board</a></p></nav>
  </div>
</footer>"""
BASE = SITE["canonical"].rstrip("/") + "/"
def page(title, desc, body, extra_head="", body_class="", slug="index.html"):
    canonical = BASE + slug
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
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
<div class="disclosure-strip" role="note">Disclosure: As an Amazon Associate, The Countertop Guide earns from qualifying purchases. Prices are snapshots from {VERIFIED} - check Amazon for the live price. <a href="compliance.html">Learn more</a></div>
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
def guide_shell(kicker, h1, intro, sections_html, faqs):
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in faqs)
    body = f"""
<p class="eyebrow">{esc(kicker)}</p>
<h1>{esc(h1)}</h1>
<p class="meta">By The Countertop Guide editorial team - Spec-based guide (not hands-on tested) - Verified data {VERIFIED} - 4 min read</p>
<p class="lede">{intro}</p>
<div class="toc"><strong>On this page:</strong> <a href="#shortlist">Shortlist from verified listings</a> - <a href="#compare-link">Full comparison</a> - <a href="#faq">Questions</a></div>
{sections_html}
<h2 id="shortlist">Shortlist from verified listings</h2>
<div class="grid cols-2">{product_card('P1',2)}{product_card('P2',2)}{product_card('P3',2)}</div>
<p id="compare-link"><a class="btn secondary" href="compare.html">See the full side-by-side comparison</a></p>
<h2 id="faq">Questions</h2>
{faq_html}
<p class="small">Every product fact above comes from the Amazon listing linked on each card. If a fact is missing, we say so - see <a href="flagged.html">Flagged for review</a>. Prices are snapshots; confirm on Amazon before buying.</p>
"""
    return body, jsonld(faq_json)
# ---------- INDEX ----------
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
<p class="eyebrow">The Countertop Guide - independent buying guides</p>
<h1>Counter space in, confidence out: pick your next air fryer or thermometer</h1>
<p class="lede">Three air fryers and two meat thermometers, compared the honest way - every spec traced to its Amazon listing, every link labeled. Start with the products below, or answer three quick questions and we will shortlist what fits your counter.</p>
<p><a class="btn" href="#lineup">Shop the line-up</a> <a class="btn secondary" href="guides.html">Read the guides</a></p>
<p class="small"><span class="badge-ok">Listings verified {VERIFIED}</span> <span class="badge-ok">Sponsored links labeled</span> <span class="badge-warn">Prices are snapshots - check Amazon</span></p>
</section>
<h2 id="lineup">The line-up - five products, two categories</h2>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<div class="grid cols-2" style="margin-top:1rem">{product_card('P4')}{product_card('P5')}</div>
<h2>Shop by category</h2>
<div class="grid cols-2">
  <article class="card"><span class="tag">Air Fryers - 3 products</span><h3>Dual-basket, oven-style &amp; single-basket</h3><p>From a 6QT dual-basket to a 26QT French-door oven. Compare depth, footprint and capacity per centimetre of counter.</p><p><a class="btn small" href="air-fryers.html">Shop air fryers</a></p></article>
  <article class="card"><span class="tag">Thermometers - 2 products</span><h3>Instant-read vs wireless</h3><p>One-second instant reads vs WiFi probes you can watch from the next room. Accuracy claims are quoted from the listing, with the certification named.</p><p><a class="btn small" href="thermometers.html">Shop thermometers</a></p></article>
</div>
<h2>Not sure where to start? Answer three questions</h2>
<p>Our chooser uses only verified specs (form, depth, price snapshot). It does not replace reading the listing - but it gets you to a shortlist in 20 seconds.</p>
{CHOOSER}
<h2>Latest guides</h2>
<div class="grid cols-3">
  <article class="card"><span class="tag">Guide</span><h3>Basket or oven-style air fryer: what should you compare?</h3><p>Form factor first: baskets vs French-door ovens, with the three fryers on this site as worked examples.</p><p><a href="guide-basket-vs-oven.html">Read</a></p></article>
  <article class="card"><span class="tag">Guide</span><h3>A no-hype checklist for comparing air fryer capacity</h3><p>Quarts vs litres, single vs dual baskets, and the \"feeds 4-6\" claim - how to read it without being misled.</p><p><a href="guide-capacity-checklist.html">Read</a></p></article>
  <article class="card"><span class="tag">Guide</span><h3>How to assess cleanup and counter-space trade-offs</h3><p>Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.</p><p><a href="guide-cleanup-counter-space.html">Read</a></p></article>
</div>
<p><a href="guides.html">All guides</a> - <a href="compare.html">Full comparison</a> - <a href="suggestions.html">Suggest a topic</a></p>
<h2>How we keep this honest</h2>
<p class="small\">Every product fact links to its <a href=\"verification.html\">verification record</a>. Missing values are blank and <a href=\"flagged.html\">flagged</a>, never guessed. We do not claim hands-on testing we have not done. Disclosure: as an Amazon Associate we earn from qualifying purchases - <a href=\"compliance.html\">how we disclose</a>.</p>
"""
write_page("index.html", "Air Fryers & Meat Thermometers, Compared Honestly | The Countertop Guide","Shop 3 air fryers and 2 meat thermometers with specs traced to their Amazon listings: capacity, counter footprint, cleanup and dated price snapshots. Sponsored links labeled, every fact sourced.",index_body,jsonld({"@context":"https://schema.org","@type":"WebSite","name":"The Countertop Guide","url": BASE + "index.html"}))
# ---------- AIR FRYERS ----------
af_body = f"""
<p class="eyebrow">Category - Air Fryers</p>
<h1>Air fryers: dual-basket, oven-style &amp; single-basket</h1>
<p class="lede">Three verified fryers, three different jobs. The dual-basket cooks two dishes at once; the French-door oven is built for crowds and rotisserie; the single basket is the compact weeknight workhorse. Start with form, then capacity, then footprint.</p>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<h2>Air fryer comparison (verified fields only)</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>Chefman 6QT Dual-Basket<br>B0CDY277D3</th><th>Emeril 26QT French-Door<br>B09B7SB46R</th><th>Chefman 8QT TurboFry<br>B08DKYBTPH</th></tr>
<tr><td>Form</td><td>Dual basket (2 x 3 Qt)</td><td>Oven-style, French door</td><td>Single basket</td></tr>
<tr><td>Capacity (title)</td><td>6 Quart</td><td>26QT</td><td>8 quarts</td></tr>
<tr><td>Capacity field on listing</td><td>6 liters <span class="badge-warn">unit differs - see Flagged</span></td><td>24.6 liters <span class="badge-warn">unit differs - see Flagged</span></td><td>8 quarts</td></tr>
<tr><td>Dimensions (D x W x H)</td><td>13.38 x 11.81 x 10.63 in</td><td>16.9 x 15.8 x 14.8 in</td><td>12.75 x 13.5 x 10 in</td></tr>
<tr><td>Counter depth</td><td>13.38 in (34.0 cm)</td><td>16.9 in (42.9 cm)</td><td>12.75 in (32.4 cm)</td></tr>
<tr><td>Footprint (W x D)</td><td>158.0 sq in</td><td>267.0 sq in</td><td>172.1 sq in</td></tr>
<tr><td>Capacity per sq in footprint*</td><td>0.038 qt/sq in</td><td>0.097 qt/sq in</td><td>0.046 qt/sq in</td></tr>
<tr><td>Rating (snapshot)</td><td>4.2 (4,876)</td><td>4.3 (18,375)</td><td>4.4 (16,892)</td></tr>
<tr><td>Price snapshot (new)</td><td>$79.93 (list $99.99)</td><td>$149.99 (list $209.99)</td><td>$69.99 (list $119.99)</td></tr>
<tr><td>Wattage (listing bullets)</td><td>1700 W / 120 V</td><td><span class="badge-flag">Not captured - Flagged</span></td><td>1000 W / 120 V</td></tr>
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
write_page("air-fryers.html", "Air Fryers Compared: Dual-Basket, Oven-Style & Single-Basket | The Countertop Guide","Compare Chefman 6QT dual-basket, Emeril 26QT French-door oven and Chefman 8QT TurboFry from verified Amazon listings: capacity, footprint, cleanup, price snapshots.",af_body)
# ---------- THERMOMETERS ----------
th_body = f"""
<p class="eyebrow">Category - Thermometers</p>
<h1>Thermometers: instant-read vs wireless</h1>
<p class="lede">Two different tools for the same job - knowing when meat is done. The instant-read gives a 1-second answer in your hand. The wireless system watches three probes from your phone. Accuracy claims below are quoted from the listing with the certification named; we have not independently calibrated either unit.</p>
<div class="grid cols-2">{product_card('P4')}{product_card('P5')}</div>
<h2>Thermometer comparison (verified fields only)</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>ThermoMaven Instant-Read<br>B0DHZTCNR5</th><th>CHEF iQ Sense Wireless<br>B0DZFD6R9Z</th></tr>
<tr><td>Type</td><td>Handheld instant-read</td><td>Wireless probes + hub + app</td></tr>
<tr><td>Accuracy claim (listing)</td><td>+/-0.5F, NIST &amp; NSF certified</td><td>4 internal + 1 ambient sensor (listing bullets); no +/-F figure captured</td></tr>
<tr><td>Read / monitoring</td><td>1-second read (thermocouple, per bullets)</td><td>Real-time app updates, WiFi unlimited range, Bluetooth</td></tr>
<tr><td>Probes</td><td>Single probe (handheld)</td><td>3 probes included (1/2/4-probe variants exist)</td></tr>
<tr><td>Heat rating</td><td>- (not captured)</td><td>1000F heat-safe probes (per title/bullets)</td></tr>
<tr><td>Waterproof / care</td><td>IP67 waterproof; rinse under water</td><td>Waterproof, dishwasher-safe probes</td></tr>
<tr><td>Battery / charge</td><td>1x AAA battery included</td><td>Up to 50 hours per charge (per bullets)</td></tr>
<tr><td>Rating (snapshot)</td><td>4.6 (3,499)</td><td>4.2 (2,178)</td></tr>
<tr><td>Price snapshot</td><td>$16.99 (list $22.99)</td><td>$119.99 3-probe (list $219.99)</td></tr>
<tr><td>Dimensions</td><td><span class="badge-flag">Not captured - Flagged</span></td><td><span class="badge-flag">Not captured - Flagged</span></td></tr>
<tr><td>Source</td><td><a href="https://www.amazon.com/dp/B0DHZTCNR5">Amazon listing</a></td><td><a href="https://www.amazon.com/dp/B0DZFD6R9Z">Amazon listing</a></td></tr>
</table></div>
<h2>Guide</h2>
<ul><li><a href="guide-thermometer-accuracy.html">Instant-read or wireless? How to read accuracy claims without being misled</a></li></ul>
<p><a class="btn secondary" href="compare.html">Compare with air fryers</a></p>
"""
write_page("thermometers.html", "Meat Thermometers Compared: Instant-Read vs Wireless | The Countertop Guide","ThermoMaven 1-second instant-read vs CHEF iQ Sense wireless 3-probe system, compared from verified Amazon listings: accuracy claims, range, probes and price snapshots.",th_body)
# ---------- COMPARE ----------
compare_body = f"""
<p class="eyebrow">Comparison</p>
<h1>All five products, side by side</h1>
<p class="lede">Every cell is either quoted from the Amazon listing (with link) or marked missing. Derived rows (footprint, capacity per square inch) show their method. Prices are {VERIFIED} snapshots - the live price on Amazon is the only price that matters.</p>
<h2>Three-question chooser</h2>
{CHOOSER}
<h2>Full table</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>P1 Chefman 6QT Dual<br>B0CDY277D3</th><th>P2 Emeril 26QT Oven<br>B09B7SB46R</th><th>P3 Chefman 8QT Basket<br>B08DKYBTPH</th><th>P4 ThermoMaven Instant<br>B0DHZTCNR5</th><th>P5 CHEF iQ Wireless<br>B0DZFD6R9Z</th></tr>
<tr><td>Category / form</td><td>Air Fryers - Dual basket</td><td>Air Fryers - Oven-style</td><td>Air Fryers - Single basket</td><td>Thermometers - Instant-read</td><td>Thermometers - Wireless</td></tr>
<tr><td>Capacity</td><td>6 Quart (title) / 6 liters (field)</td><td>26QT (title) / 24.6 liters (field)</td><td>8 quarts</td><td>-</td><td>-</td></tr>
<tr><td>Dimensions</td><td>13.38D x 11.81W x 10.63H in</td><td>16.9D x 15.8W x 14.8H in</td><td>12.75D x 13.5W x 10H in</td><td>Not captured</td><td>Not captured</td></tr>
<tr><td>Rating snapshot</td><td>4.2 (4,876)</td><td>4.3 (18,375)</td><td>4.4 (16,892)</td><td>4.6 (3,499)</td><td>4.2 (2,178)</td></tr>
<tr><td>Price snapshot (new)</td><td>$79.93</td><td>$149.99</td><td>$69.99</td><td>$16.99</td><td>$119.99 (3-probe)</td></tr>
<tr><td>List price</td><td>$99.99</td><td>$209.99</td><td>$119.99</td><td>$22.99</td><td>$219.99</td></tr>
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
write_page("compare.html", "Compare 5 Air Fryers & Thermometers Side by Side | The Countertop Guide","Side-by-side comparison of 5 verified products: capacity, dimensions, footprint, ratings and price snapshots, plus a 3-question chooser and counter-space math.",compare_body)
# ---------- GUIDES INDEX ----------
guides_body = """
<p class="eyebrow">Guides</p>
<h1>Question-shaped guides, answered from the listing</h1>
<p class="lede">Each guide starts from a question a buyer actually types, then answers it with verified listing facts - and says plainly what the listing does not tell us. No popularity or "trending" claims without a dated snapshot.</p>
<div class="grid cols-2">
<article class="card"><span class="tag">Air fryers - Form</span><h3>Basket or oven-style air fryer: what should you compare?</h3><p>Dual-basket vs French-door oven vs single basket: cooking two dishes, crowd capacity, and counter depth.</p><p><a class="btn small" href="guide-basket-vs-oven.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Capacity</span><h3>A no-hype checklist for comparing air fryer capacity</h3><p>Quarts vs litres, "feeds 4-6", rotisserie and pizza claims - how to read capacity without being misled.</p><p><a class="btn small" href="guide-capacity-checklist.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Space &amp; cleanup</span><h3>How to assess cleanup and counter-space trade-offs</h3><p>Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.</p><p><a class="btn small" href="guide-cleanup-counter-space.html">Read guide</a></p></article>
<article class="card"><span class="tag">Multi-function</span><h3>Questions to ask before buying a multi-function kitchen appliance</h3><p>Presets, accessories, wattage and warranty - the pre-purchase checklist, applied to the Emeril oven.</p><p><a class="btn small" href="guide-multifunction-questions.html">Read guide</a></p></article>
<article class="card"><span class="tag">Thermometers - Accuracy</span><h3>Instant-read or wireless? How to read accuracy claims</h3><p>+/-0.5F, NIST/NSF, sensor counts and range - what each claim does and does not prove.</p><p><a class="btn small" href="guide-thermometer-accuracy.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal</span><h3>Holiday &amp; gift guides (coming next)</h3><p>Gift-ready picks by budget and cook type. We publish only after the gift angle is verified against the listing - see Suggestions board for the calendar.</p><p><a href="suggestions.html">See publishing plan</a></p></article>
</div>
"""
write_page("guides.html", "Buyer Guides: Air Fryers & Thermometers | The Countertop Guide","Question-shaped buying guides answered from verified Amazon listings: basket vs oven, capacity, cleanup and counter space, multi-function checklists, thermometer accuracy.",guides_body)
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
<p>We have not cooked in any of these units, so we do not claim crispness, noise, or "lived-with" durability. Those require hands-on testing we have not done - see <a href="flagged.html">Flagged for review</a>. What we can tell you is form, capacity, footprint, cleanup as listed, and price snapshot.</p>
""",
 [("Which is better, basket or oven-style air fryer?","Neither - they do different jobs. Dual-basket for two dishes at once, oven-style for crowds, rotisserie and pizza, single-basket for compact one-dish cooking. Use the three questions above."),
  ("How deep is the Emeril 26QT oven?","16.9 inches (42.9 cm) deep, per the Amazon listing dimensions (16.9D x 15.8W x 14.8H in). Measure your counter before buying."),
  ("Can the Chefman 6QT cook two dishes at once?","Yes, per the listing: two independent 3-quart baskets with Sync Finish so both can finish at the same time.")])
write_page("guide-basket-vs-oven.html", "Basket or Oven-Style Air Fryer: What Should You Compare? | The Countertop Guide","Dual-basket vs French-door oven vs single basket: two-dish cooking, crowd capacity, counter depth and cleanup, compared from verified Amazon listings.",b1,j1,"guide-page")
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
<li><strong>What is missing?</strong> Emeril wattage was not captured. If wattage matters for your circuit, check the listing's product details before buying.</li>
</ol>
<h2>Worked example</h2>
<p>Two baskets of 3 Qt each (Chefman 6QT dual) let you run chicken in one and vegetables in the other, finishing together. A single 8 Qt basket (Chefman 8QT) gives one large cavity for one dish. A 26QT oven (Emeril) gives a cavity for a whole chicken and pizza. Same word - "capacity" - three different cooking experiences.</p>
""",
 [("Is 6 quarts the same as 6 litres?","No. The Chefman 6QT listing title says 6 Quart while its capacity field says 6 liters. We report both exactly as shown and flag the difference rather than converting silently."),
  ("How many people does the Emeril 26QT feed?","The listing bullets describe it as suitable for 4-6 people. That is the seller's description, not our tested serving count."),
  ("What does capacity per square inch mean?","Title capacity divided by footprint (width x depth from listing dimensions). It shows how much capacity you get per unit of counter. Derived by us; see compare page for method.")])
write_page("guide-capacity-checklist.html", "A No-Hype Checklist for Comparing Air Fryer Capacity | The Countertop Guide","Quarts vs litres, single vs dual baskets, feeds 4-6 and pizza claims: a checklist for reading air fryer capacity honestly, applied to 3 verified listings.",b2,j2,"guide-page")
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
write_page("guide-cleanup-counter-space.html", "How to Assess Cleanup and Counter-Space Trade-Offs | The Countertop Guide","Dishwasher-safe baskets, footprint math and capacity per centimetre of counter depth for 3 verified air fryers. Measure your counter, then compare.",b3,j3,"guide-page")
# ---------- GUIDE 4 ----------
b4, j4 = guide_shell("Guide - Multi-function", "Questions to ask before buying a multi-function kitchen appliance",
 "Multi-function ovens promise everything. Before you pay for presets you will never use, ask these questions. We apply them to the Emeril 26QT French-door oven.",
 """
<h2>The pre-purchase questions</h2>
<ol>
<li><strong>How many presets, and do you recognise them?</strong> Emeril title says 24 One-Touch presets; bullets say 25 cooking pre-sets. That discrepancy is flagged - count on the listing, not the headline. Functions shown: Air Fry, Convection Bake, Rotisserie, Toast, Grill, Dehydrate, Roast, Slow Cook, Broil.</li>
<li><strong>What accessories are included?</strong> Title says six cooking accessories. List them on the listing before buying; replacements cost extra.</li>
<li><strong>What is the wattage?</strong> Not captured for the Emeril in our verification pass - flagged. Check product details for circuit planning.</li>
<li><strong>What does the warranty say?</strong> Chefman listings state 1-year assurance/warranty; CHEF iQ states 2-year assurance. Emeril warranty was not captured - check the listing.</li>
<li><strong>Does it fit?</strong> 16.9D x 15.8W x 14.8H in is the largest of the three fryers. French doors need swing clearance.</li>
</ol>
<p>Rule of thumb: pay for functions you will use weekly (air fry, bake, toast, rotisserie), not for the longest preset list.</p>
""",
 [("How many presets does the Emeril 26QT have?","The title says 24 One-Touch presets while the bullets say 25 cooking pre-sets. We flag the discrepancy and recommend verifying on the listing."),
  ("What accessories come with the Emeril oven?","The title says six cooking accessories are included. Check the listing for the exact list before buying."),
  ("What is the Emeril wattage?","Not captured in our verification pass. See the listing's product details section before buying.")])
write_page("guide-multifunction-questions.html", "Questions to Ask Before Buying a Multi-Function Kitchen Appliance | The Countertop Guide","Presets, accessories, wattage, warranty and fit: the pre-purchase checklist for multi-function ovens, applied to the Emeril 26QT from its verified listing.",b4,j4,"guide-page")
# ---------- GUIDE 5 ----------
b5, j5 = guide_shell("Guide - Thermometers", "Instant-read or wireless? How to read accuracy claims",
 "One tool answers in one second in your hand; the other watches from your phone. The right choice depends on how you cook - and on reading accuracy claims carefully.",
 """
<h2>Instant-read: ThermoMaven (B0DHZTCNR5)</h2>
<p>Listing claims +/-0.5F accuracy with NIST &amp; NSF certification, 1-second thermocouple read, IP67 waterproof, auto-rotating LED. Includes a calibration certificate. Price snapshot $16.99. Best for: quick checks, grilling, candy, everyday meals.</p>
<h2>Wireless: CHEF iQ Sense (B0DZFD6R9Z)</h2>
<p>Three ultra-thin probes plus hub, WiFi unlimited range with app, 1000F heat-safe probes, up to 50 hours per charge, flip reminders and rest timers. Listing bullets describe 4 internal + 1 ambient sensors (title: 5 sensors). No +/-F accuracy figure was captured - do not assume it matches the instant-read. Price snapshot $119.99 (3-probe). Best for: long cooks, multiple proteins, monitoring from another room.</p>
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
write_page("guide-thermometer-accuracy.html", "Instant-Read or Wireless? How to Read Thermometer Accuracy Claims | The Countertop Guide","Plus-minus 0.5F, NIST/NSF, sensor counts and WiFi range: how to read meat thermometer accuracy claims honestly, comparing 2 verified listings.",b5,j5,"guide-page")
# ---------- EXECUTIVE SUMMARY ----------
exec_body = f"""
<p class="eyebrow">Executive summary</p>
<h1>What this site is, what is verified, and what happens next</h1>
<p class="lede">The Countertop Guide is a spec-backed affiliate publication for two kitchen categories - air fryers and meat thermometers - built from five Amazon listings verified on {VERIFIED}. It leads with products and buyer questions, not with process. Every number links to its source.</p>
<h2>The five products</h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Product</th><th>ASIN</th><th>Category</th><th>Price snapshot</th><th>Rating snapshot</th></tr>
<tr><td>P1</td><td>Chefman 6QT Dual-Basket Air Fryer Oven</td><td>B0CDY277D3</td><td>Air Fryers</td><td>$79.93</td><td>4.2 (4,876)</td></tr>
<tr><td>P2</td><td>Emeril Lagasse 26QT French-Door Oven</td><td>B09B7SB46R</td><td>Air Fryers</td><td>$149.99</td><td>4.3 (18,375)</td></tr>
<tr><td>P3</td><td>Chefman 8QT TurboFry Basket</td><td>B08DKYBTPH</td><td>Air Fryers</td><td>$69.99</td><td>4.4 (16,892)</td></tr>
<tr><td>P4</td><td>ThermoMaven 1-Second Instant-Read</td><td>B0DHZTCNR5</td><td>Thermometers</td><td>$16.99</td><td>4.6 (3,499)</td></tr>
<tr><td>P5</td><td>CHEF iQ Sense Wireless (3 probes)</td><td>B0DZFD6R9Z</td><td>Thermometers</td><td>$119.99</td><td>4.2 (2,178)</td></tr>
</table></div>
<h2>What is verified</h2>
<ul>
<li>Each submitted short link resolves to the ASIN and official listing URL in <a href="verification.html">verification register</a> (intended ASIN kept separate from observed redirect target). All five links re-checked 2026-11-19.</li>
<li>A full line-by-line re-read of all five Amazon.com listings on 2026-11-19: titles, ratings, price snapshots, dimensions (air fryers), capacity, wattage, special features and bullets. Emeril wattage was captured on this pass (1700 watts per the listing's Product information table).</li>
<li>Compliance posture: disclosure above the fold on every page and in the footer; every outbound product link is rel="sponsored" and labeled; no "trending" or popularity claims without a dated snapshot; no hands-on testing claims.</li>
</ul>
<h2>What is not verified (and therefore not claimed)</h2>
<ul>
<li>Thermometer dimensions (not listed on their listing pages), Emeril warranty period (listing links a PDF only), and the Chefman 8QT wattage (listing bullets and spec table disagree) - blank or attributed and flagged.</li>
<li>Short-link compliance status (unresolved), Special Link test in Associates Central (manual gate), commission rates (not published here), search volume / popularity (not claimed).</li>
<li>Product photography (no Amazon images used; real photography needs a licence decision).</li>
</ul>
<h2>How money and measurement work</h2>
<p>Outbound links use tracking ID <code>{TAG}</code> and are marked sponsored. Click and conversion measurement is defined (five events) with a privacy-preserving local counter; the self-hosted endpoint is a documented stub, not yet deployed. The campaign ledger starts empty - orders and revenue are recorded only from authorized first-party reports. See <a href="methodology.html">Method &amp; campaign ledger</a>.</p>
<h2>Next gates (owner decisions)</h2>
<p>Canonical domain, Special Link validation, photography licence, analytics endpoint, the design-brief direction, and the Suggestions board priorities. Nothing scales until those gates pass. See <a href="design-brief.html">Design brief</a>, <a href="suggestions.html">Suggestions &amp; decision log</a> and <a href="flagged.html">Flagged for review</a>.</p>
"""
write_page("executive-summary.html", "Executive Summary: Products, Verification & Next Gates | The Countertop Guide","Executive summary for The Countertop Guide: 5 verified products in 2 categories, what is and is not verified, compliance posture, measurement plan and decision gates.",exec_body)
# ---------- SUGGESTIONS ----------
sugg_body = """
<p class="eyebrow">Suggestions board</p>
<h1>Suggestions &amp; decision log - review before anything is built</h1>
<p class="lede">Nothing on this board is implemented until a reviewer picks a path. Each suggestion states the evidence it needs, the effort, and what decision it blocks. Add your pick in the review; we implement only approved items.</p>
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
</table></div>
<p class="small">Reviewer: mark each SG item Approved / Rejected / Deferred with a date. Approved items move to COORDINATION.md as claimed tasks. The full design brief feeding the visual overhaul is on <a href="design-brief.html">design-brief.html</a>. Nothing here is a promise of traffic, ranking, or revenue.</p>
"""
write_page("suggestions.html", "Suggestions Board & Decision Log: Review Before Building | The Countertop Guide","Suggestions board and Q/I/A decision log for The Countertop Guide: what to build next, what evidence each needs, and which decisions are blocked until answers arrive.",sugg_body)
# ---------- VERIFICATION ----------
ver_rows = ""
for pid in ["P1","P2","P3","P4","P5"]:
    p = PRODS[pid]
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
<p class="small">Verification performed 2026-11-19 by fetching each Amazon listing and policy page. Second pass the same day re-read all five listings end-to-end: titles, buy-box prices and list prices, rating counts (P2 18,375; P3 16,892 - counts drift, snapshots re-dated), dimensions, capacity fields and bullets all confirmed; short links re-resolved to the same five ASINs. Prices/ratings are snapshots and will change. Manual Special Link test in Associates Central remains a gate (see <a href="flagged.html">Flagged</a>).</p>
"""
write_page("verification.html", "Verification Register: Line-by-Line Sources for Every Fact | The Countertop Guide","Verification register for 5 products: intended ASIN, official listing URL, confirmation date and source per product, plus official Amazon and FTC policy sources.",ver_body)
# ---------- FLAGGED ----------
flag_body = f"""
<p class="eyebrow">Flagged for review</p>
<h1>Flagged for review - irregularities &amp; unverified items</h1>
<p class="lede">Flagged items do not block publishing, but they block claims. Nothing below is presented as fact on product pages. Review after launch and request changes.</p>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Item</th><th>Detail</th><th>Action</th></tr>
<tr><td>FLG-001</td><td>Short-link compliance unresolved</td><td>Supplied link.amazon short links resolve to the ASINs, but their exact compliance status as Special Links is unresolved. We do not claim they are invalid. Site outbound buttons use official listing URLs + tag instead.</td><td>Manual test in Associates Central (SG-01)</td></tr>
<tr><td>FLG-002</td><td>Preset &amp; capacity discrepancies</td><td>Emeril: title 24 presets vs bullets 25; title 26QT vs field 24.6 liters. Chefman 6QT: title 6 Quart vs field 6 liters. Both values shown; no silent conversion.</td><td>Verify on listing; ask seller if needed</td></tr>
<tr><td>FLG-003</td><td>Newer models shown on listings</td><td>Chefman 8QT page shows newer 6QT B0CNY1YVDD ($59.99, 4.6/7,602); ThermoMaven page shows newer Orange B0GL7Z4KP4 ($16.99, 4.7/144). We promote the submitted ASINs only.</td><td>Decide lineup (SG-08)</td></tr>
<tr><td>FLG-004</td><td>Missing dimensions (thermometers)</td><td>ThermoMaven B0DHZTCNR5 and CHEF iQ B0DZFD6R9Z dimensions not in captured fields. Left blank in tables.</td><td>Re-fetch product-details; record date</td></tr>
<tr><td>FLG-005</td><td>Missing warranty (Emeril)</td><td>Emeril wattage captured 2026-11-19 (1700 watts / 120 volts per the listing's Product information table). Warranty period is not stated on the listing page; the listing links a warranty PDF only. Left blank.</td><td>Read warranty PDF if the term is needed</td></tr>
<tr><td>FLG-006</td><td>Price volatility</td><td>All prices are {VERIFIED} snapshots (Black Friday period). Live price on Amazon governs.</td><td>Re-snapshot on cadence; date every price</td></tr>
<tr><td>FLG-007</td><td>Canonical is the GitHub Pages URL, not a custom domain</td><td>Canonical/og URLs now point to https://wingbangboozle1-lang.github.io/Prod1/ on every page (set 2026-11-19; generator fixed so rebuilds reproduce it). A custom domain is still an owner decision, and Search Console is not yet connected.</td><td>Owner confirms the GitHub Pages URL is final, or picks a custom domain (SG-02)</td></tr>
<tr><td>FLG-008</td><td>Analytics endpoint not deployed</td><td>Five events defined; local counter only. No server endpoint yet.</td><td>Deploy endpoint (SG-03)</td></tr>
<tr><td>FLG-009</td><td>No product photography</td><td>No Amazon images used (IP/licence). SVG/CSS illustrations only.</td><td>Licence decision (SG-04)</td></tr>
<tr><td>FLG-010</td><td>No hands-on testing</td><td>We have not cooked with or calibrated any product. No "lived-with" claims made.</td><td>Testing programme if approved (SG-09)</td></tr>
<tr><td>FLG-011</td><td>No commission / revenue claims</td><td>Rates not published; ledger empty until authorized reports arrive.</td><td>Record only from Associates reports</td></tr>
<tr><td>FLG-012</td><td>No trending / popularity claims</td><td>"Bought in past month" badges are listing snapshots, not our ranking. We do not claim trending.</td><td>Evidence rule: dated snapshot or no claim</td></tr>
<tr><td>FLG-013</td><td>Submitted link codes are 9 characters</td><td>Each submitted link.amazon path code (e.g. B04G1MEwY) is 9 characters. Each code resolves to a listing whose ASIN differs from the code, so the code is not used as an intended ASIN. Intended ASIN fields stay blank pending submitter confirmation (session 9b748801, 2026-11-19).</td><td>Submitter confirms intended ASIN per link (Q-03)</td></tr>
<tr><td>FLG-014</td><td>ASIN 10-character rule: third-party sources only</td><td>The 10-character ASIN format was found on third-party guides, not on an Amazon page read in this session. The format is used only to flag the 9-character codes.</td><td>Find an official Amazon help page for the ASIN definition</td></tr>
<tr><td>FLG-015</td><td>Redirect targets carry no tag=</td><td>The final URLs of the five supplied links (read 2026-11-19) contain no tag= parameter. Attribution to shopnow047c-20 is therefore not observed on the redirect path. Site buttons use tagged listing URLs (FLG-001).</td><td>Associates tracking-report test per product (SG-01)</td></tr>
<tr><td>FLG-016</td><td>Listing pages carry widget data for other ASINs</td><td>Listing pages include Product summary links and Customers who viewed carousels with prices and ratings for other products. These are not used as data for the five products.</td><td>Use only each product's own fields; re-check on publication</td></tr>
<tr><td>FLG-017</td><td>External register: three links vs five</td><td>The external Zone4 decision log (D-13) refers to the three supplied links; this brief supplies five. Its statuses are not carried into this site. Only the first part of that log was read.</td><td>Reconcile the external register with the five links</td></tr>
<tr><td>FLG-018</td><td>Proposed Amazon content notice (not verified)</td><td>The external Zone4 decision log proposes an Amazon content notice citing IP License section 2(k). The IP License was not read, and the notice is not yet on the pages.</td><td>Read IP License 2(k); decide under SG-04</td></tr>
<tr><td>FLG-019</td><td>Creators API prerequisites not read</td><td>The external Zone4 decision log suggests the Creators API for prices and ratings. Its prerequisites were not read, and no API data is used on this site.</td><td>Read prerequisites before any price or rating source change</td></tr>
<tr><td>FLG-020</td><td>Main-product values not fully re-read in integration</td><td>The integration check confirmed the five ASINs and the ThermoMaven price ($16.99) against the listing pages. Other prices, ratings and dimensions in data/products.json were not re-read in full in this pass.</td><td>Full re-read of each listing's product details before publishing price claims</td></tr>
<tr><td>FLG-021</td><td>Accessory count discrepancy (Emeril)</td><td>Listing title says \"Six Cooking Accessories Included\"; the listing's item details say \"Air Fryer Toaster Oven Combo with 24 Functions and 7 Accessories\"; the included-components list names 6 items (Rack, Bake Pan, Drip Tray, Crisper Basket, Rotisserie Spit, Fetch Tool). All three values are listing-internal and disagree. We show the title value and flag it; no count is inferred. Observed 2026-11-19.</td><td>Ask seller / read product manual; show title value with flag until resolved</td></tr>
<tr><td>FLG-022</td><td>Wattage discrepancy (Chefman 8QT)</td><td>Chefman 8QT listing bullets state \"1000 Watts/120 Volts - RJ38-SQSS-8T\" while the listing's Product information table lists Output Wattage 1700 watts, 120 volts. Both values are listing-internal and disagree. We show the bullets value with attribution and flag it; no wattage is inferred. Observed 2026-11-19.</td><td>Ask seller / read user manual; resolve before any circuit-load claim</td></tr>
</table></div>
"""
write_page("flagged.html", "Flagged for Review: Irregularities & Unverified Items | The Countertop Guide","Flagged irregularities for The Countertop Guide: short-link compliance, preset/capacity discrepancies, newer models, missing fields, price volatility and launch gates.",flag_body)
# ---------- COMPLIANCE ----------
comp_body = f"""
<p class="eyebrow">Compliance gate</p>
<h1>Disclosures &amp; policy checks in the publishing workflow</h1>
<p class="lede">Disclosure above the fold on every page (and repeated in the footer). Every outbound product link is marked sponsored. Endorsement context is reviewed against the Operating Agreement and FTC guidance before publishing.</p>
<h2>Our disclosure (verbatim, every page)</h2>
<blockquote>As an Amazon Associate, The Countertop Guide earns from qualifying purchases. Prices and availability are snapshots from Amazon.com on the verification date and can change - always check the price on Amazon before you buy.</blockquote>
<h2>How each outbound link is marked</h2>
<ul>
<li>URL format: <code>https://www.amazon.com/dp/ASIN?tag={TAG}</code> (official listing URL + tracking ID).</li>
<li>Attributes: <code>rel="sponsored nofollow noopener"</code>, <code>target="_blank"</code>, visible "sponsored" label and "Opens amazon.com" text so destination is never obscured.</li>
<li>Short links are recorded in the <a href="verification.html">verification register</a> as submitted links with observed redirect targets in a separate field. They are not used as outbound buttons.</li>
</ul>
<h2>Policy checklist (reviewed 2026-11-19)</h2>
<div class="table-scroll"><table>
<tr><th>Check</th><th>Source</th><th>Our practice</th></tr>
<tr><td>Use proper tagged Special Link formats</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement S1</a></td><td>Official URL + tag; manual SiteStripe test is a gate (FLG-001)</td></tr>
<tr><td>Do not obscure link destination</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td><td>Button text + ASIN + "Opens amazon.com" on every card</td></tr>
<tr><td>Disclose material connection, hard to miss</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td><td>Strip under masthead on every page + footer; simple language ("earns from qualifying purchases")</td></tr>
<tr><td>Endorsement honesty; no unsubstantiated claims</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td><td>No testing/trending claims; seller claims attributed ("per listing")</td></tr>
<tr><td>Program Content / images</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement S1</a></td><td>No Amazon images copied; SVG/CSS only until licence decided</td></tr>
</table></div>
<p class="small">This page is a publishing checklist, not legal advice. Review disclosure placement and endorsement context against the current Agreement and FTC guidance at each publish. If in doubt, flag it.</p>
"""
write_page("compliance.html", "Compliance: Disclosures & Amazon/FTC Policy Checks | The Countertop Guide","Compliance gate for The Countertop Guide: disclosure wording, sponsored-link marking, and Amazon Associates + FTC policy checklist reviewed before publishing.",comp_body)
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
<p>Implementation: <code>assets/app.js</code> counts locally in <code>localStorage</code> and beacons to a configurable endpoint (<code>data-analytics-endpoint</code>, currently empty). No third-party trackers. Deploying the endpoint is SG-03; until then, counts are device-local and the ledger stays empty.</p>
<h2>Campaign ledger (empty by design)</h2>
<div class="table-scroll"><table>
<tr><th>Date</th><th>Source</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th><th>Reported orders</th><th>Provenance</th></tr>
<tr><td colspan="7"><em>No rows yet. Add timestamp, source, channel, eligible sessions, clicks and reported orders only when obtained from authorized first-party reports (Associates Central). No conversion score or revenue forecast is presented.</em></td></tr>
</table></div>
<h2>Publishing cadence</h2>
<p>New guides are added to <code>sitemap.xml</code> and <code>feed.xml</code> at publish. Next topic is chosen from measured Search Console queries (after SG-02), not instinct. RSS feed: <a href="feed.xml">feed.xml</a>. Sitemap: <a href="sitemap.xml">sitemap.xml</a>.</p>
"""
write_page("methodology.html", "Method: Verification, Analytics Events & Campaign Ledger | The Countertop Guide","Method page for The Countertop Guide: evidence rules, five privacy-preserving analytics events, empty campaign ledger with provenance rules, and publishing cadence.",meth_body)
# ---------- DASHBOARD HUB ----------
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
write_page("dashboard.html", "Dashboard: Verification, Flags, Compliance & Decisions | The Countertop Guide","One hub for every dashboard surface of The Countertop Guide: verification register, flagged items, compliance checklist, method and ledger, executive summary, and the suggestions board.",dash_body)# ---------- DESIGN BRIEF ----------
db_body = """
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
<tr><td>Voice</td><td>Write like a knowledgeable friend comparing specs: short varied sentences, one idea per paragraph, concrete numbers with their source, no filler transitions, no \"in conclusion\", no superlatives. We never claim hands-on testing, trending status or rankings we cannot show.</td><td>All copy</td><td>Voice sign-off (Q-11)</td></tr>
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
write_page("design-brief.html", "Design Brief: Suggestions for the Publication Redesign | The Countertop Guide","Design brief suggestions for The Countertop Guide redesign: design prompt blocks, three visual directions, anti-AI-slop rules, an eight-topic editorial calendar, and decision gates for review.",db_body)

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
write_page("search.html", "Search Guides & Products | The Countertop Guide","Search The Countertop Guide guides and product comparisons: air fryers, thermometers, capacity, cleanup, counter space and accuracy.",search_body)
idx = [
 {"title":"Dashboard hub","url":"dashboard.html","text":"Every dashboard surface in one place: verification register, flagged for review, compliance, method and campaign ledger, executive summary, suggestions board."},
 {"title":"Air fryers category","url":"air-fryers.html","text":"Chefman 6QT dual-basket, Emeril 26QT French-door oven, Chefman 8QT TurboFry. Capacity, footprint, cleanup, price snapshots."},
 {"title":"Thermometers category","url":"thermometers.html","text":"ThermoMaven 1-second instant-read vs CHEF iQ Sense wireless 3-probe. Accuracy claims, range, probes."},
 {"title":"Compare all five","url":"compare.html","text":"Side-by-side table, 3-question chooser, counter-space analysis, capacity per cm depth."},
 {"title":"Basket or oven-style air fryer: what should you compare?","url":"guide-basket-vs-oven.html","text":"Dual-basket vs French-door oven vs single basket. Two-dish cooking, crowd capacity, counter depth."},
 {"title":"A no-hype checklist for comparing air fryer capacity","url":"guide-capacity-checklist.html","text":"Quarts vs litres, single vs dual baskets, feeds 4-6, rotisserie and pizza claims."},
 {"title":"How to assess cleanup and counter-space trade-offs","url":"guide-cleanup-counter-space.html","text":"Dishwasher-safe baskets, footprint math, capacity per centimetre of counter depth."},
 {"title":"Questions to ask before buying a multi-function kitchen appliance","url":"guide-multifunction-questions.html","text":"Presets, accessories, wattage, warranty and fit checklist for multi-function ovens."},
 {"title":"Instant-read or wireless? How to read accuracy claims","url":"guide-thermometer-accuracy.html","text":"Plus-minus 0.5F, NIST NSF, sensor counts, WiFi range. How to read thermometer claims."},
 {"title":"Executive summary","url":"executive-summary.html","text":"What the site is, what is verified, compliance posture, measurement plan, decision gates."},
 {"title":"Suggestions board and decision log","url":"suggestions.html","text":"Suggestions SG-01 to SG-10, questions Q-01 to Q-08, evidence needed, decisions blocked."},
 {"title":"Verification register","url":"verification.html","text":"Line-by-line sources, intended ASIN vs observed redirect, confirmation dates, policy sources."},
 {"title":"Flagged for review","url":"flagged.html","text":"Irregularities: short-link compliance, discrepancies, newer models, missing fields, launch gates."},
 {"title":"Compliance","url":"compliance.html","text":"Disclosure wording, sponsored-link marking, Amazon and FTC policy checklist."},
 {"title":"Method and campaign ledger","url":"methodology.html","text":"Evidence rules, five analytics events, empty campaign ledger, publishing cadence."},
 {"title":"Design brief","url":"design-brief.html","text":"Design prompt blocks, three visual directions, anti-AI-slop rules, eight-topic editorial calendar, decision gates."},
]
json.dump(idx, open("data/search-index.json","w"), indent=2)
print("pages written")

# Post-step: mark every amazon.com citation link as sponsored (consistency: every outbound product link sponsored)
import glob as _g, re as _r
for _f in _g.glob("*.html"):
    _s = open(_f).read()
    _s2 = _r.sub(r'(<a href="https://www\.amazon\.com/dp/[^"]*")>', r'\1 rel="sponsored nofollow noopener" target="_blank">', _s)
    if _s2 != _s:
        open(_f, "w").write(_s2)
print("sponsored post-step done")

# Post-step: preserve the index-only footer review links added by session ab9cbcdc (P-21).
# They are kept in the generator so rebuilds reproduce the committed index.html instead of
# silently dropping the links to the docs/ review pages.
_idx = open("index.html").read()
_old_tail = '<a href="suggestions.html">Suggestions board</a></p></nav>'
_new_tail = ('<a href="suggestions.html">Suggestions board</a><br>'
             '<a href="docs/products.html">Product-intent register (blank fields)</a><br>'
             '<a href="docs/flagged.html">Additional review notes</a><br>'
             '<a href="docs/campaign-ledger.html">Empty campaign ledger</a></p></nav>')
if _old_tail in _idx:
    open("index.html", "w").write(_idx.replace(_old_tail, _new_tail, 1))
    print("index footer review links preserved")
