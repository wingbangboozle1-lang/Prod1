import json, html
D = json.load(open("data/products.json"))
SITE = D["site"]
PRODS = {p["id"]: p for p in D["products"]}
VERIFIED = SITE["verifiedDate"]
TAG = SITE["trackingId"]
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
  <a href="suggestions.html">Suggestions</a>
</nav>
<form class="searchbox" id="site-search-form" role="search">
  <label class="skip" for="site-search-input">Search the site</label>
  <input id="site-search-input" type="search" placeholder="Search guides &amp; products" aria-label="Search the site">
  <button class="btn small secondary" type="submit">Search</button>
</form>"""
FOOTER = f"""
<footer>
  <div class="disclosure-strip">Disclosure: As an Amazon Associate I earn from qualifying purchases. <a href="compliance.html">How we disclose</a></div>
  <div class="footer-inner">
    <div>
      <p><strong>The Countertop Guide</strong> - spec-backed comparisons from Amazon listings. We do not claim hands-on testing we have not done. Every product fact links to its Amazon listing and verification record.</p>
      <p class="small">Prices are snapshots from {VERIFIED} and change. Always confirm price, variant and fit on Amazon before buying.</p>
    </div>
    <nav aria-label="Shop"><p><strong>Shop</strong></p><p><a href="air-fryers.html">Air Fryers</a><br><a href="thermometers.html">Thermometers</a><br><a href="compare.html">Compare all five</a></p></nav>
    <nav aria-label="Guides"><p><strong>Guides</strong></p><p><a href="guides.html">All guides</a><br><a href="guide-basket-vs-oven.html">Basket or oven-style?</a><br><a href="guide-capacity-checklist.html">Capacity checklist</a><br><a href="guide-cleanup-counter-space.html">Cleanup &amp; counter space</a></p></nav>
    <nav aria-label="Trust"><p><strong>Trust &amp; data</strong></p><p><a href="verification.html">Verification register</a><br><a href="flagged.html">Flagged for review</a><br><a href="compliance.html">Compliance</a><br><a href="methodology.html">Method &amp; campaign ledger</a><br><a href="executive-summary.html">Executive summary</a><br><a href="suggestions.html">Suggestions board</a></p></nav>
  </div>
</footer>"""
def page(title, desc, body, extra_head="", body_class=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://wingbangboozle1-lang.github.io/Prod1/">
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
<div class="disclosure-strip" role="note">Disclosure: As an Amazon Associate I earn from qualifying purchases. Prices are snapshots from {VERIFIED} - check Amazon for the live price. <a href="compliance.html">Learn more</a></div>
<main id="main" class="wrap">
{body}
</main>
{FOOTER}
<script src="assets/app.js"></script>
</body>
</html>
"""
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
<p class="eyebrow">Air fryers &amp; thermometers - compared from the listing</p>
<h1>Basket or oven-style air fryer: what should you compare?</h1>
<p class="lede">Five real products, two categories, zero hype. We compare capacity, counter footprint, cleanup and price <em>exactly as listed on Amazon</em> - and we show the source for every number. No fake "we tested it" claims. No "trending" without a dated snapshot.</p>
<p><a class="btn" href="compare.html">Compare all five</a> <a class="btn secondary" href="guides.html">Read the guides</a></p>
<p class="small"><span class="badge-ok">Verified {VERIFIED}</span> <span class="badge-ok">Sponsored links labeled</span> <span class="badge-warn">Prices are snapshots - check Amazon</span></p>
</section>
<h2>Shop by category</h2>
<div class="grid cols-2">
  <article class="card"><span class="tag">Air Fryers - 3 products</span><h3>Air fryers: dual-basket, oven-style &amp; single-basket</h3><p>From a 6QT dual-basket to a 26QT French-door oven. Compare depth, footprint and capacity per centimetre of counter.</p><p><a class="btn small" href="air-fryers.html">Shop air fryers</a></p></article>
  <article class="card"><span class="tag">Thermometers - 2 products</span><h3>Thermometers: instant-read vs wireless</h3><p>One-second instant reads vs WiFi probes you can watch from the next room. Accuracy claims are quoted from the listing, with the certification named.</p><p><a class="btn small" href="thermometers.html">Shop thermometers</a></p></article>
</div>
<h2>Featured products - verified {VERIFIED}</h2>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<div class="grid cols-2" style="margin-top:1rem">{product_card('P4')}{product_card('P5')}</div>
<h2>Not sure where to start? Answer three questions</h2>
<p>Our chooser uses only verified specs (form, depth, price snapshot). It does not replace reading the listing - but it gets you to a shortlist in 20 seconds.</p>
{CHOOSER}
<h2>Latest guides</h2>
<div class="grid cols-3">
  <article class="card"><span class="tag">Guide</span><h3>Basket or oven-style air fryer: what should you compare?</h3><p>Form factor first: baskets vs French-door ovens, with the three fryers on this site as worked examples.</p><p><a href="guide-basket-vs-oven.html">Read</a></p></article>
  <article class="card"><span class="tag">Guide</span><h3>A no-hype checklist for comparing air fryer capacity</h3><p>Quarts vs litres, single vs dual baskets, and the "feeds 4-6" claim - how to read it without being misled.</p><p><a href="guide-capacity-checklist.html">Read</a></p></article>
  <article class="card"><span class="tag">Guide</span><h3>How to assess cleanup and counter-space trade-offs</h3><p>Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.</p><p><a href="guide-cleanup-counter-space.html">Read</a></p></article>
</div>
<p><a href="guides.html">All guides</a> - <a href="suggestions.html">Suggest a topic</a></p>
"""
open("index.html","w").write(page("Air Fryers & Thermometers Compared From the Listing | The Countertop Guide","Compare 3 air fryers and 2 thermometers from verified Amazon listings: capacity, footprint, cleanup and price snapshots. No fake testing, sponsored links labeled.",index_body,jsonld({"@context":"https://schema.org","@type":"WebSite","name":"The Countertop Guide","url":"https://wingbangboozle1-lang.github.io/Prod1/"})))
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
<tr><td>Rating (snapshot)</td><td>4.2 (4,876)</td><td>4.3 (18,371)</td><td>4.4 (16,890)</td></tr>
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
open("air-fryers.html","w").write(page("Air Fryers Compared: Dual-Basket, Oven-Style & Single-Basket | The Countertop Guide","Compare Chefman 6QT dual-basket, Emeril 26QT French-door oven and Chefman 8QT TurboFry from verified Amazon listings: capacity, footprint, cleanup, price snapshots.",af_body))
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
open("thermometers.html","w").write(page("Meat Thermometers Compared: Instant-Read vs Wireless | The Countertop Guide","ThermoMaven 1-second instant-read vs CHEF iQ Sense wireless 3-probe system, compared from verified Amazon listings: accuracy claims, range, probes and price snapshots.",th_body))
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
<tr><td>Rating snapshot</td><td>4.2 (4,876)</td><td>4.3 (18,371)</td><td>4.4 (16,890)</td><td>4.6 (3,499)</td><td>4.2 (2,178)</td></tr>
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
open("compare.html","w").write(page("Compare 5 Air Fryers & Thermometers Side by Side | The Countertop Guide","Side-by-side comparison of 5 verified products: capacity, dimensions, footprint, ratings and price snapshots, plus a 3-question chooser and counter-space math.",compare_body))
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
<article class="card"><span class="tag">Seasonal - Gifts</span><h3>Holiday air fryer gifts: what to buy for every kind of cook</h3><p>Match the fryer to the cook: dual-basket, oven-style, single basket, plus thermometer stocking stuffers - each from a verified listing.</p><p><a class="btn small" href="guide-holiday-gifts.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Small kitchens</span><h3>Small kitchen, big appetite: under 34 cm of counter depth</h3><p>Depth and footprint compared for the three verified fryers, with derived capacity-per-centimetre math.</p><p><a class="btn small" href="guide-small-kitchen.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Roasts</span><h3>Roast like a pro: instant-read or wireless thermometer?</h3><p>Reading accuracy claims on two verified thermometers before the holiday.</p><p><a class="btn small" href="guide-holiday-roast.html">Read guide</a></p></article>
</div>
"""
open("guides.html","w").write(page("Buyer Guides: Air Fryers & Thermometers | The Countertop Guide","Question-shaped buying guides answered from verified Amazon listings: basket vs oven, capacity, cleanup and counter space, multi-function checklists, thermometer accuracy, holiday gifts and holiday roasts.",guides_body))
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
open("guide-basket-vs-oven.html","w").write(page("Basket or Oven-Style Air Fryer: What Should You Compare? | The Countertop Guide","Dual-basket vs French-door oven vs single basket: two-dish cooking, crowd capacity, counter depth and cleanup, compared from verified Amazon listings.",b1,j1,"guide-page"))
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
open("guide-capacity-checklist.html","w").write(page("A No-Hype Checklist for Comparing Air Fryer Capacity | The Countertop Guide","Quarts vs litres, single vs dual baskets, feeds 4-6 and pizza claims: a checklist for reading air fryer capacity honestly, applied to 3 verified listings.",b2,j2,"guide-page"))
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
open("guide-cleanup-counter-space.html","w").write(page("How to Assess Cleanup and Counter-Space Trade-Offs | The Countertop Guide","Dishwasher-safe baskets, footprint math and capacity per centimetre of counter depth for 3 verified air fryers. Measure your counter, then compare.",b3,j3,"guide-page"))
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
open("guide-multifunction-questions.html","w").write(page("Questions to Ask Before Buying a Multi-Function Kitchen Appliance | The Countertop Guide","Presets, accessories, wattage, warranty and fit: the pre-purchase checklist for multi-function ovens, applied to the Emeril 26QT from its verified listing.",b4,j4,"guide-page"))
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
open("guide-thermometer-accuracy.html","w").write(page("Instant-Read or Wireless? How to Read Thermometer Accuracy Claims | The Countertop Guide","Plus-minus 0.5F, NIST/NSF, sensor counts and WiFi range: how to read meat thermometer accuracy claims honestly, comparing 2 verified listings.",b5,j5,"guide-page"))
# ---------- GUIDE 6: holiday gifts ----------
g6_body = f"""<p class="eyebrow">Seasonal guide - Air fryer &amp; thermometer gifts</p>
<h1>Holiday air fryer gifts: what to buy for every kind of cook</h1>
<p class="meta">By The Countertop Guide editorial team - Spec-based gift guide (not hands-on tested) - Verified data {VERIFIED} - 4 min read</p>
<p class="lede">Match the fryer to the cook, not the wish list. These picks come only from the verified listings on this site, each with its snapshot price and a link to its source.</p>
<div class="toc"><strong>On this page:</strong> <a href="#for-couples">For couples &amp; side-dish cooks</a> - <a href="#for-crowds">For crowds &amp; weekend roasts</a> - <a href="#for-small-kitchens">For small kitchens</a> - <a href="#for-thermometer-gifts">Thermometer stocking stuffers</a> - <a href="#faq">Questions</a></div>
<h2 id="for-couples">For couples and side-dish cooks: Chefman 6QT dual-basket</h2>
<p>Two independent 3-quart baskets with Sync Finish, so two dishes can finish at the same time - good for a main and a side together. Listing shows dual-zone cooking, viewing windows, and dishwasher-safe baskets. Depth 13.38 inches (34.0 cm). Price snapshot {VERIFIED}: $79.93 (list $99.99).</p>
<p><a class="btn" href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0CDY277D3">See Chefman 6QT listing - sponsored</a></p>
<h2 id="for-crowds">For crowds and weekend roasts: Emeril 26QT French-door oven</h2>
<p>The listing describes 26-quart capacity for 4-6 people, rotisserie for a 6-lb chicken, and baking a 12-inch pizza. Deepest of the three at 16.9 inches (42.9 cm) - it needs real counter depth. Price snapshot {VERIFIED}: $149.99 (list $209.99). Preset count differs between title (24) and bullets (25) - see <a href="flagged.html">Flagged FLG-002</a>.</p>
<p><a class="btn" href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B09B7SB46R">See Emeril 26QT listing - sponsored</a></p>
<h2 id="for-small-kitchens">For small kitchens: Chefman 8QT single basket</h2>
<p>Shallowest of the three at 12.75 inches (32.4 cm) deep, with an 8-quart single basket, 450F Hi-Fry option, and a top-rack dishwasher-safe basket and tray. Price snapshot {VERIFIED}: $69.99 (list $119.99).</p>
<p><a class="btn" href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B08DKYBTPH">See Chefman 8QT listing - sponsored</a></p>
<h2 id="for-thermometer-gifts">Thermometer stocking stuffers</h2>
<p>ThermoMaven instant-read: 1-second read, +/-0.5F accuracy with NIST &amp; NSF certification claimed, IP67 waterproof, includes a calibration certificate. Best for quick checks, grilling, candy, everyday meals. Price snapshot {VERIFIED}: $16.99 (list $22.99). Rating snapshot {VERIFIED}: 4.6 (3,499). Dimensions not yet captured - see <a href="flagged.html">Flagged FLG-004</a>. <a class="btn" href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">See ThermoMaven listing - sponsored</a></p>
<p>CHEF iQ Sense wireless: 3 ultra-thin probes plus hub, WiFi app monitoring, 1000F heat-safe probes claimed, up to 50 hours per charge claimed, flip reminders and rest timers. Listing bullets describe 4 internal + 1 ambient sensors (title says 5); no +/-F accuracy figure captured - do not assume it matches the instant-read. Price snapshot {VERIFIED}: $119.99 (list $219.99, 3-probe). Rating snapshot {VERIFIED}: 4.2 (2,178). <a class="btn" href="{aff(PRODS['P5'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">See CHEF iQ listing - sponsored</a></p>
<p class="small">Snapshot prices and ratings are from Amazon.com on {VERIFIED} and will change. Confirm price, variant and fit on the listing before buying. No hands-on testing - these are spec-based suggestions, not recommendations of use.</p>
<h2 id="faq">Questions</h2>
<details><summary>Which air fryer makes the best gift?</summary><p>The one that fits the recipient's counter and cooking: dual-basket for two dishes at once, oven-style for crowds and roasts, single basket for compact counters. Match counter depth first.</p></details>
<details><summary>Are these gift picks hands-on tested?</summary><p>No. We have not cooked with any of these units. Picks are based only on verified listing specs and snapshot prices.</p></details>
<details><summary>Do the prices include shipping?</summary><p>Prices shown are the listing's new-item snapshot; shipping depends on the buyer's location and Prime status at checkout. Confirm on Amazon before buying.</p></details>
"""
j6 = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Which air fryer makes the best gift?","acceptedAnswer":{"@type":"Answer","text":"The one that fits the recipient's counter and cooking: dual-basket for two dishes at once, oven-style for crowds and roasts, single basket for compact counters. Match counter depth first."}},{"@type":"Question","name":"Are these gift picks hands-on tested?","acceptedAnswer":{"@type":"Answer","text":"No. We have not cooked with any of these units. Picks are based only on verified listing specs and snapshot prices."}}]}
open("guide-holiday-gifts.html","w").write(page("Holiday Air Fryer Gifts: What to Buy for Every Kind of Cook | The Countertop Guide","Spec-based holiday gift picks drawn from verified Amazon listings: Chefman 6QT dual-basket, Emeril 26QT oven, Chefman 8QT basket, plus thermometer stocking stuffers.",g6_body,jsonld(j6)))
# ---------- GUIDE 7: small kitchen ----------
g7_body = f"""<p class="eyebrow">Seasonal guide - Small kitchens</p>
<h1>Small kitchen, big appetite: which air fryer fits under 34 cm of counter depth?</h1>
<p class="meta">By The Countertop Guide editorial team - Spec-based guide (not hands-on tested) - Verified data {VERIFIED} - 4 min read</p>
<p class="lede">Measure before you buy. This guide compares the three verified fryers by counter depth and footprint, with the derived capacity-per-centimetre math shown and its limits stated.</p>
<div class="toc"><strong>On this page:</strong> <a href="#measure">Measure your counter</a> - <a href="#depth-table">Depth and footprint table</a> - <a href="#capacity-per-cm">Capacity per centimetre of depth</a> - <a href="#faq">Questions</a></div>
<h2 id="measure">Measure your counter first</h2>
<p>Depth decides whether it fits under cabinets; width decides whether it crowds the sink. From listing dimensions:</p>
<ul>
<li>Chefman 8QT basket: 12.75D x 13.5W in - shallowest at 32.4 cm depth, 172.1 sq in footprint.</li>
<li>Chefman 6QT dual: 13.38D x 11.81W in - narrowest at 34.0 cm depth, 158.0 sq in footprint.</li>
<li>Emeril 26QT oven: 16.9D x 15.8W in - deepest at 42.9 cm depth, 267.0 sq in footprint.</li>
</ul>
<p class="small">Dimensions as shown on each Amazon listing on {VERIFIED}. Footprint = width x depth; derived by us, not a manufacturer claim. Method and limits in <a href="guide-cleanup-counter-space.html">cleanup &amp; counter-space guide</a>.</p>
<h2 id="depth-table">Depth and footprint table (verified fields only)</h2>
<div class="table-scroll"><table>
<tr><th>Air fryer (ASIN)</th><th>Depth</th><th>Width</th><th>Height</th><th>Footprint</th><th>Capacity (title)</th><th>Price snapshot {VERIFIED}</th></tr>
<tr><td><a href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B08DKYBTPH">Chefman 8QT single basket - sponsored</a> B08DKYBTPH</td><td>12.75 in (32.4 cm)</td><td>13.5 in</td><td>10 in</td><td>172.1 sq in</td><td>8 quarts</td><td>$69.99 (list $119.99)</td></tr>
<tr><td><a href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0CDY277D3">Chefman 6QT dual-basket - sponsored</a> B0CDY277D3</td><td>13.38 in (34.0 cm)</td><td>11.81 in</td><td>10.63 in</td><td>158.0 sq in</td><td>6 Quart (2 x 3 Qt)</td><td>$79.93 (list $99.99)</td></tr>
<tr><td><a href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B09B7SB46R">Emeril 26QT French-door oven - sponsored</a> B09B7SB46R</td><td>16.9 in (42.9 cm)</td><td>15.8 in</td><td>14.8 in</td><td>267.0 sq in</td><td>26QT</td><td>$149.99 (list $209.99)</td></tr>
</table></div>
<h2 id="capacity-per-cm">Capacity per centimetre of counter depth (derived)</h2>
<p>Emeril 0.61 qt/cm, Chefman 8QT 0.25 qt/cm, Chefman 6QT dual 0.18 qt/cm. The oven gives the most capacity per centimetre of depth - if you have the depth to spare. Not a manufacturer claim; derived from listing dimensions and title capacity.</p>
<h2 id="faq">Questions</h2>
<details><summary>Which air fryer fits the smallest counter?</summary><p>By depth, the Chefman 8QT (32.4 cm). By footprint, the Chefman 6QT dual-basket (158.0 sq in). Measure both depth and width before buying.</p></details>
<details><summary>Is capacity per centimetre a manufacturer claim?</summary><p>No. It is derived by us from listing dimensions (inches x 2.54 = cm) and title capacity. Treat it as a planning aid, verify fit on the listing.</p></details>
"""
j7 = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Which air fryer fits the smallest counter?","acceptedAnswer":{"@type":"Answer","text":"By depth, the Chefman 8QT (32.4 cm). By footprint, the Chefman 6QT dual-basket (158.0 sq in). Measure both depth and width before buying."}},{"@type":"Question","name":"Is capacity per centimetre a manufacturer claim?","acceptedAnswer":{"@type":"Answer","text":"No. It is derived by us from listing dimensions and title capacity. Treat it as a planning aid, verify fit on the listing."}}]}
open("guide-small-kitchen.html","w").write(page("Small Kitchen Air Fryers: Which Fits Under 34 cm of Counter Depth? | The Countertop Guide","Counter depth and footprint compared for 3 verified air fryers, with derived capacity-per-centimetre math and measure-first advice.",g7_body,jsonld(j7)))
# ---------- GUIDE 8: holiday roast thermometers ----------
g8_body = f"""<p class="eyebrow">Seasonal guide - Holiday roasts</p>
<h1>Roast like a pro: instant-read or wireless thermometer for holiday roasts?</h1>
<p class="meta">By The Countertop Guide editorial team - Spec-based guide (not hands-on tested) - Verified data {VERIFIED} - 4 min read</p>
<p class="lede">A roast is only as good as knowing when it's done. This guide reads the accuracy claims on two verified thermometers - what each claim does and does not prove - so you can choose before the holiday.</p>
<div class="toc"><strong>On this page:</strong> <a href="#instant-read">Instant-read: ThermoMaven</a> - <a href="#wireless">Wireless: CHEF iQ Sense</a> - <a href="#reading-accuracy">How to read accuracy claims</a> - <a href="#faq">Questions</a></div>
<h2 id="instant-read">Instant-read: ThermoMaven 1-Second</h2>
<p>Listing claims +/-0.5F accuracy with NIST &amp; NSF certification, 1-second thermocouple read, IP67 waterproof, auto-rotating LED, includes a calibration certificate. Best for: quick checks, grilling, candy, everyday meals. Price snapshot {VERIFIED}: $16.99 (list $22.99). Rating snapshot {VERIFIED}: 4.6 (3,499).</p>
<p><a class="btn" href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DHZTCNR5">See ThermoMaven listing - sponsored</a></p>
<h2 id="wireless">Wireless: CHEF iQ Sense (3 probes)</h2>
<p>Three ultra-thin probes plus hub, WiFi unlimited range with app, 1000F heat-safe probes claimed, up to 50 hours per charge claimed, flip reminders and rest timers. Listing bullets describe 4 internal + 1 ambient sensors (title says 5). No +/-F accuracy figure was captured - do not assume it matches the instant-read. Price snapshot {VERIFIED}: $119.99 (list $219.99, 3-probe). Rating snapshot {VERIFIED}: 4.2 (2,178).</p>
<p><a class="btn" href="{aff(PRODS['P5'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="B0DZFD6R9Z">See CHEF iQ listing - sponsored</a></p>
<h2 id="reading-accuracy">How to read accuracy claims</h2>
<ul>
<li>Ask for the +/- figure <em>and</em> the certification name. "NIST certified" without a figure is incomplete.</li>
<li>Ask what the sensor count means. CHEF iQ's 5 = 4 internal + 1 ambient (per bullets).</li>
<li>"Unlimited" WiFi range means app monitoring over your network - you still need WiFi and the app.</li>
<li>We have not calibrated either unit. Certification claims are the seller's; verify the certificate on the listing.</li>
</ul>
<p class="small">Accuracy figures and ratings are listing snapshots from {VERIFIED} and will change. We have not cooked with or calibrated either thermometer. Confirm claims on the listing before buying.</p>
<h2 id="faq">Questions</h2>
<details><summary>Instant-read or wireless for a holiday roast?</summary><p>Instant-read for a fast answer in your hand (ThermoMaven, 1-second). Wireless for monitoring from another room across a long cook (CHEF iQ Sense, 3 probes). Match the tool to how you cook.</p></details>
<details><summary>Are the accuracy claims verified by the site?</summary><p>No. Claims are quoted from the listings with the certification named. We have not calibrated either unit; verify certificates on the listing.</p></details>
"""
j8 = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Instant-read or wireless for a holiday roast?","acceptedAnswer":{"@type":"Answer","text":"Instant-read for a fast answer in your hand (ThermoMaven, 1-second). Wireless for monitoring from another room across a long cook (CHEF iQ Sense, 3 probes). Match the tool to how you cook."}},{"@type":"Question","name":"Are the accuracy claims verified by the site?","acceptedAnswer":{"@type":"Answer","text":"No. Claims are quoted from the listings with the certification named. We have not calibrated either unit; verify certificates on the listing."}}]}
open("guide-holiday-roast.html","w").write(page("Roast Like a Pro: Instant-Read or Wireless Thermometer for Holiday Roasts? | The Countertop Guide","Reading meat thermometer accuracy claims on 2 verified listings - instant-read vs wireless - with snapshot prices and ratings.",g8_body,jsonld(j8)))
# ---------- EXECUTIVE SUMMARY ----------
exec_body = f"""
<p class="eyebrow">Executive summary</p>
<h1>What this site is, what is verified, and what happens next</h1>
<p class="lede">The Countertop Guide is a spec-backed affiliate publication for two kitchen categories - air fryers and meat thermometers - built from five Amazon listings verified on {VERIFIED}. It leads with products and buyer questions, not with process. Every number links to its source.</p>
<h2>The five products</h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Product</th><th>ASIN</th><th>Category</th><th>Price snapshot</th><th>Rating snapshot</th></tr>
<tr><td>P1</td><td>Chefman 6QT Dual-Basket Air Fryer Oven</td><td>B0CDY277D3</td><td>Air Fryers</td><td>$79.93</td><td>4.2 (4,876)</td></tr>
<tr><td>P2</td><td>Emeril Lagasse 26QT French-Door Oven</td><td>B09B7SB46R</td><td>Air Fryers</td><td>$149.99</td><td>4.3 (18,371)</td></tr>
<tr><td>P3</td><td>Chefman 8QT TurboFry Basket</td><td>B08DKYBTPH</td><td>Air Fryers</td><td>$69.99</td><td>4.4 (16,890)</td></tr>
<tr><td>P4</td><td>ThermoMaven 1-Second Instant-Read</td><td>B0DHZTCNR5</td><td>Thermometers</td><td>$16.99</td><td>4.6 (3,499)</td></tr>
<tr><td>P5</td><td>CHEF iQ Sense Wireless (3 probes)</td><td>B0DZFD6R9Z</td><td>Thermometers</td><td>$119.99</td><td>4.2 (2,178)</td></tr>
</table></div>
<h2>What is verified</h2>
<ul>
<li>Each submitted short link resolves to the ASIN and official listing URL in <a href="verification.html">verification register</a> (intended ASIN kept separate from observed redirect target).</li>
<li>Titles, ratings, price snapshots, dimensions (air fryers), capacity, special features and bullets as shown on Amazon.com on {VERIFIED}.</li>
<li>Compliance posture: disclosure above the fold on every page and in the footer; every outbound product link is rel="sponsored" and labeled; no "trending" or popularity claims without a dated snapshot; no hands-on testing claims.</li>
</ul>
<h2>What is not verified (and therefore not claimed)</h2>
<ul>
<li>Thermometer dimensions, Emeril wattage/warranty, CHEF iQ +/-F accuracy figure - blank and flagged.</li>
<li>Short-link compliance status (unresolved), Special Link test in Associates Central (manual gate), commission rates (not published here), search volume / popularity (not claimed).</li>
<li>Product photography (no Amazon images used; real photography needs a licence decision).</li>
</ul>
<h2>How money and measurement work</h2>
<p>Outbound links use tracking ID <code>{TAG}</code> and are marked sponsored. Click and conversion measurement is defined (five events) with a privacy-preserving local counter; the self-hosted endpoint is a documented stub, not yet deployed. The campaign ledger starts empty - orders and revenue are recorded only from authorized first-party reports. See <a href="methodology.html">Method &amp; campaign ledger</a>.</p>
<h2>Next gates (owner decisions)</h2>
<p>Canonical domain, Special Link validation, photography licence, analytics endpoint, and the Suggestions board priorities. Nothing scales until those gates pass. See <a href="suggestions.html">Suggestions &amp; decision log</a> and <a href="flagged.html">Flagged for review</a>.</p>
"""
open("executive-summary.html","w").write(page("Executive Summary: Products, Verification & Next Gates | The Countertop Guide","Executive summary for The Countertop Guide: 5 verified products in 2 categories, what is and is not verified, compliance posture, measurement plan and decision gates.",exec_body))
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
<tr><td>SG-11</td><td>Decide disclosure wording: verbatim Operating Agreement §5 or site-named variant</td><td>§5 requires "As an Amazon Associate I earn from qualifying purchases." or a substantially similar previously allowed statement</td><td>Compliance review of current variant</td><td>Low</td><td>Resolved 2026-11-19: verbatim wording adopted</td></tr>
<tr><td>SG-12</td><td>Resolve star-rating display path under Participation Requirement 6(t)</td><td>Displaying customer reviews/star ratings conditions on Creators API or PA API; site shows snapshots without either</td><td>Policy decision; API access check</td><td>Medium</td><td>Needs decision</td></tr>
</table></div>
<h2>Questions, information &amp; answers needed before a reasonable decision</h2>
<div class="table-scroll"><table>
<tr><th>#</th><th>Question</th><th>What we know</th><th>What we do not know</th><th>How to discover it</th><th>Decision blocked</th></tr>
<tr><td>Q-01</td><td>Are the supplied short links compliant Special Links?</td><td>They resolve to the ASINs in the register (observed 2026-11-19)</td><td>Exact compliance status is unresolved</td><td>Test in Associates Central; read Operating Agreement + Policies</td><td>Scaling outbound links</td></tr>
<tr><td>Q-02</td><td>What is the canonical domain?</td><td>Site builds as static GitHub Pages; canonical currently placeholder</td><td>Final domain / custom domain</td><td>Owner picks domain; set canonical + Search Console</td><td>SEO launch, og:image, sitemap</td></tr>
<tr><td>Q-03</td><td>What are thermometer dimensions &amp; Emeril wattage?</td><td>Air fryer dims verified; thermometer dims + Emeril wattage not captured</td><td>Missing fields (blank in tables)</td><td>Re-fetch listing product-details sections; record date</td><td>Counter-space table for thermometers; circuit advice</td></tr>
<tr><td>Q-04</td><td>Should we promote newer models instead?</td><td>Listings show newer variants (see Flagged)</td><td>Margin, rating trajectory, variant fit</td><td>Compare variant listings; check Associates reports</td><td>Product lineup</td></tr>
<tr><td>Q-05</td><td>What commission rates apply?</td><td>Tracking ID shopnow047c-20; session rules in Policies</td><td>Category rates (not published here)</td><td>Associates Central commission statement (authorized report only)</td><td>Revenue forecasting (not done)</td></tr>
<tr><td>Q-06</td><td>Is there search demand for these topics?</td><td>Guides are question-shaped hypotheses, not volume claims</td><td>Measured queries (no analytics yet)</td><td>Search Console after launch; choose next topics from data</td><td>Publishing cadence</td></tr>
<tr><td>Q-07</td><td>Can we use product photos?</td><td>No Amazon images used; SVG/CSS only</td><td>Licence / permission status</td><td>Manufacturer permission or own photography</td><td>Visual overhaul</td></tr>
<tr><td>Q-08</td><td>Where does analytics data live?</td><td>Local-only counter; endpoint stub documented</td><td>Hosting, retention, consent</td><td>Pick host; publish retention policy</td><td>Measurement &amp; optimisation</td></tr>
<tr><td>Q-09</td><td>Should the disclosure use the verbatim §5 wording?</td><td>Current variant names the site instead of \"I\"; check script flagged it for owner review</td><td>— (resolved)</td><td>Resolved 2026-11-19 against Operating Agreement §5: verbatim wording adopted on all pages</td><td>Disclosure wording</td></tr>
<tr><td>Q-10</td><td>May we display star ratings without Creators API / PA API?</td><td>Participation Requirement 6(t) conditions ratings display on those APIs; site shows listing snapshots</td><td>API access and eligibility</td><td>Policy decision (SG-12)</td><td>Ratings on product cards</td></tr>
<tr><td>Q-11</td><td>What cadence for re-snapshotting prices and ratings?</td><td>Last snapshot 2026-11-19; live values have since drifted</td><td>Re-fetch listings on a schedule; record each date</td><td>Owner sets cadence</td><td>Price/rating freshness</td></tr>
</table></div>
<p class="small">Reviewer: mark each SG item Approved / Rejected / Deferred with a date. Approved items move to COORDINATION.md as claimed tasks. Nothing here is a promise of traffic, ranking, or revenue.</p>
"""
open("suggestions.html","w").write(page("Suggestions Board & Decision Log: Review Before Building | The Countertop Guide","Suggestions board and Q/I/A decision log for The Countertop Guide: what to build next, what evidence each needs, and which decisions are blocked until answers arrive.",sugg_body))
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
<p class="small">Verification performed 2026-11-19 by fetching each Amazon listing and policy page. Prices/ratings are snapshots and will change. Manual Special Link test in Associates Central remains a gate (see <a href="flagged.html">Flagged</a>).</p>
"""
open("verification.html","w").write(page("Verification Register: Line-by-Line Sources for Every Fact | The Countertop Guide","Verification register for 5 products: intended ASIN, official listing URL, confirmation date and source per product, plus official Amazon and FTC policy sources.",ver_body))
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
<tr><td>FLG-005</td><td>Missing wattage/warranty (Emeril)</td><td>Emeril wattage and warranty not captured. Left blank.</td><td>Check listing product details</td></tr>
<tr><td>FLG-006</td><td>Price and rating volatility</td><td>All prices and rating counts are {VERIFIED} snapshots (Black Friday period). Re-read of listings shows rating counts have since moved (P2 18,371 recorded vs 18,375 live; P3 16,890 recorded vs 16,892 live). Live price/rating on Amazon governs.</td><td>Re-snapshot on cadence; date every price and rating</td></tr>
<tr><td>FLG-007</td><td>Canonical domain unset</td><td>Canonical/og URLs use placeholder until owner picks domain. SEO cannot fully launch without it.</td><td>Pick domain (SG-02)</td></tr>
<tr><td>FLG-008</td><td>Analytics endpoint not deployed</td><td>Five events defined; local counter only. No server endpoint yet.</td><td>Deploy endpoint (SG-03)</td></tr>
<tr><td>FLG-009</td><td>No product photography</td><td>No Amazon images used (IP/licence). SVG/CSS illustrations only.</td><td>Licence decision (SG-04)</td></tr>
<tr><td>FLG-010</td><td>No hands-on testing</td><td>We have not cooked with or calibrated any product. No "lived-with" claims made.</td><td>Testing programme if approved (SG-09)</td></tr>
<tr><td>FLG-011</td><td>No commission / revenue claims</td><td>Rates not published; ledger empty until authorized reports arrive.</td><td>Record only from Associates reports</td></tr>
<tr><td>FLG-012</td><td>No unverified popularity claims</td><td>"Bought in past month" badges are listing snapshots, not our ranking. We make no popularity claims.</td><td>Evidence rule: dated snapshot or no claim</td></tr>
<tr><td>FLG-013</td><td>Submitted link codes are 9 characters</td><td>Each submitted link.amazon path code (e.g. B04G1MEwY) is 9 characters. Each code resolves to a listing whose ASIN differs from the code, so the code is not used as an intended ASIN. Intended ASIN fields stay blank pending submitter confirmation (session 9b748801, 2026-11-19).</td><td>Submitter confirms intended ASIN per link (Q-03)</td></tr>
<tr><td>FLG-014</td><td>ASIN 10-character rule: third-party sources only</td><td>The 10-character ASIN format was found on third-party guides, not on an Amazon page read in this session. The format is used only to flag the 9-character codes.</td><td>Find an official Amazon help page for the ASIN definition</td></tr>
<tr><td>FLG-015</td><td>Redirect targets carry no tag=</td><td>The final URLs of the five supplied links (read 2026-11-19) contain no tag= parameter. Attribution to shopnow047c-20 is therefore not observed on the redirect path. Site buttons use tagged listing URLs (FLG-001).</td><td>Associates tracking-report test per product (SG-01)</td></tr>
<tr><td>FLG-016</td><td>Listing pages carry widget data for other ASINs</td><td>Listing pages include Product summary links and Customers who viewed carousels with prices and ratings for other products. These are not used as data for the five products.</td><td>Use only each product's own fields; re-check on publication</td></tr>
<tr><td>FLG-017</td><td>External register: three links vs five</td><td>The external Zone4 decision log (D-13) refers to the three supplied links; this brief supplies five. Its statuses are not carried into this site. Only the first part of that log was read.</td><td>Reconcile the external register with the five links</td></tr>
<tr><td>FLG-018</td><td>Proposed Amazon content notice (not verified)</td><td>The external Zone4 decision log proposes an Amazon content notice citing IP License section 2(k). The IP License was not read, and the notice is not yet on the pages.</td><td>Read IP License 2(k); decide under SG-04</td></tr>
<tr><td>FLG-019</td><td>Creators API prerequisites not read</td><td>The external Zone4 decision log suggests the Creators API for prices and ratings. Its prerequisites were not read, and no API data is used on this site.</td><td>Read prerequisites before any price or rating source change</td></tr>
<tr><td>FLG-020</td><td>Main-product values not fully re-read in integration</td><td>The integration check confirmed the five ASINs and the ThermoMaven price ($16.99) against the listing pages. Other prices, ratings and dimensions in data/products.json were not re-read in full in this pass.</td><td>Full re-read of each listing's product details before publishing price claims</td></tr>
<tr><td>FLG-021</td><td>Disclosure wording variant vs Operating Agreement §5</td><td>Operating Agreement Section 5 requires the disclosure in its verbatim form (the sentence naming \"I\") or any substantially similar statement previously allowed under the Agreement. The site strip previously named the site instead of \"I\"; whether that variant is \"substantially similar\" was an owner compliance decision.</td><td>Resolved 2026-11-19: verbatim §5 wording adopted on all pages (SG-11 closed).</td></tr>
<tr><td>FLG-022</td><td>Star ratings displayed without Creators API / PA API</td><td>Participation Requirement 6(t) conditions display of customer reviews or star ratings on obtaining them via Creators API or PA API. The site shows rating snapshots without those APIs.</td><td>Remove ratings or source via Creators/PA API; decision needed (SG-12)</td></tr>
<tr><td>FLG-023</td><td>Intended ASIN inconsistency</td><td>data/products.json sets the intended ASIN equal to the verified/observed ASIN. FLG-013 states intended ASIN fields stay blank pending submitter confirmation, and the brief requires intended and observed fields stay separate and unmerged.</td><td>Owner confirms each intended ASIN or blanks the field (R-02, Q-03)</td></tr>
<tr><td>FLG-024</td><td>Rating-count snapshot drift</td><td>Re-read of listings 2026-11-19 shows P2 rating count 18,375 (recorded 18,371) and P3 16,892 (recorded 16,890). Ratings, like prices, are snapshots that change.</td><td>Re-snapshot ratings on cadence; treat recorded counts as unverified until re-confirmed</td></tr>
</table></div>
"""
open("flagged.html","w").write(page("Flagged for Review: Irregularities & Unverified Items | The Countertop Guide","Flagged irregularities for The Countertop Guide: short-link compliance, preset/capacity discrepancies, newer models, missing fields, price volatility and launch gates.",flag_body))
# ---------- COMPLIANCE ----------
comp_body = f"""
<p class="eyebrow">Compliance gate</p>
<h1>Disclosures &amp; policy checks in the publishing workflow</h1>
<p class="lede">Disclosure above the fold on every page (and repeated in the footer). Every outbound product link is marked sponsored. Endorsement context is reviewed against the Operating Agreement and FTC guidance before publishing.</p>
<h2>Our disclosure (verbatim, every page)</h2>
<blockquote>As an Amazon Associate I earn from qualifying purchases. Prices and availability are snapshots from Amazon.com on the verification date and can change - always check the price on Amazon before you buy.</blockquote>
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
<tr><td>Endorsement honesty; no unsubstantiated claims</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td><td>No unverified testing or sales claims; seller claims attributed ("per listing")</td></tr>
<tr><td>Program Content / images</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement S1</a></td><td>No Amazon images copied; SVG/CSS only until licence decided</td></tr>
</table></div>
<p class="small">This page is a publishing checklist, not legal advice. Review disclosure placement and endorsement context against the current Agreement and FTC guidance at each publish. If in doubt, flag it.</p>
"""
open("compliance.html","w").write(page("Compliance: Disclosures & Amazon/FTC Policy Checks | The Countertop Guide","Compliance gate for The Countertop Guide: disclosure wording, sponsored-link marking, and Amazon Associates + FTC policy checklist reviewed before publishing.",comp_body))
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
open("methodology.html","w").write(page("Method: Verification, Analytics Events & Campaign Ledger | The Countertop Guide","Method page for The Countertop Guide: evidence rules, five privacy-preserving analytics events, empty campaign ledger with provenance rules, and publishing cadence.",meth_body))
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
open("search.html","w").write(page("Search Guides & Products | The Countertop Guide","Search The Countertop Guide guides and product comparisons: air fryers, thermometers, capacity, cleanup, counter space and accuracy.",search_body))
idx = [
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
