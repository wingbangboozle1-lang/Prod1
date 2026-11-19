import json, html, re
D = json.load(open("data/products.json"))
SITE = D["site"]
PRODS = {p["id"]: p for p in D["products"]}
VERIFIED = SITE["verifiedDate"]
TAG = SITE["trackingId"]
def esc(s): return html.escape(str(s), quote=True)
def aff(p): return p["candidateAffiliateUrl"]
def source_links(pids):
    return " · ".join(f'<a href="{esc(PRODS[pid]["observedListingUrl"])}">{pid} listing</a>' for pid in pids)
def product_card(pid, bullets_n=3):
    p = PRODS[pid]
    bl = "".join(f"<li>{esc(b)}</li>" for b in p["bullets"][:bullets_n])
    capacity = esc(p["capacityTitle"]) if p["capacityTitle"] not in ("", "—", "-") else "Not applicable"
    dims = esc(p["dimensions"]) if p["dimensions"] else '<span class="badge-flag">Dimensions not captured - see Flagged</span>'
    return f"""
<article class="card product-card" id="{pid}">
  <span class="tag">{esc(p['category'])} - {esc(p['form'])}</span>
  <h3>{esc(p['shortName'])}</h3>
  <p class="product-context">Observed listing target · {esc(p['observedAsin'])} · listing snapshot {VERIFIED}</p>
  <p><span class="stars">&#9733; {esc(p['rating'])}</span> <span class="meta">({esc(p['ratingCount'])} ratings shown on the listing at capture)</span></p>
  <p><span class="price">{esc(p['priceNew'])}</span> <span class="listprice">{esc(p['priceList'])}</span> <span class="meta">Recorded price snapshot · {VERIFIED}; confirm the live price and variant</span></p>
  <ul>
    <li><strong>Capacity:</strong> {capacity}</li>
    <li><strong>Dimensions (listing):</strong> {dims}</li>
    <li><strong>Listing features:</strong> {esc(p['specialFeatures'])}</li>
  </ul>
  <p class="meta">Selected listing statements; not independently tested</p>
  <ul>{bl}</ul>
  <p><a class="btn" href="{aff(p)}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{p['observedAsin']}">See listing on Amazon - sponsored</a></p>
  <p class="sponsored-note">Affiliate tracking test pending · Opens amazon.com · <a href="verification.html#{pid}">See source and intent record</a></p>
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
  <div class="disclosure-strip">As an Amazon Associate I earn from qualifying purchases. <a href="compliance.html">How we disclose</a></div>
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
<link rel="canonical" href="{esc(SITE['canonical'])}">
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
<div class="disclosure-strip" role="note">As an Amazon Associate I earn from qualifying purchases. Prices shown are recorded snapshots from {VERIFIED}; check Amazon for the live price. <a href="compliance.html">Disclosure details</a></div>
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
def guide_shell(kicker, h1, intro, sections_html, faqs, shortlist_pids=("P1", "P2", "P3")):
    sections_html = sections_html.replace("{VERIFIED}", VERIFIED)
    sections_html = re.sub(
        r"\{source_links\(\[([^\]]*)\]\)\}",
        lambda match: source_links(re.findall(r"['\"](P[1-5])['\"]", match.group(1))),
        sections_html,
    )
    if "{source_links(" in sections_html or "{VERIFIED}" in sections_html:
        raise ValueError("unresolved placeholder in guide sections")
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in faqs)
    shortlist_html = "".join(product_card(pid, 2) for pid in shortlist_pids)
    body = f"""
<p class="eyebrow">{esc(kicker)}</p>
<h1>{esc(h1)}</h1>
<p class="meta">By The Countertop Guide editorial team · Listing-based guide · Listing capture date {VERIFIED} · No hands-on testing claimed</p>
<p class="lede">{intro}</p>
<div class="toc"><strong>On this page:</strong> <a href="#shortlist">Products in this guide</a> · <a href="#compare-link">Full comparison</a> · <a href="#faq">Questions</a></div>
{sections_html}
<h2 id="shortlist">Products in this guide</h2>
<div class="grid cols-2">{shortlist_html}</div>
<p id="compare-link"><a class="btn secondary" href="compare.html">See the full side-by-side comparison</a></p>
<h2 id="faq">Questions</h2>
{faq_html}
<p class="small">Product claims are attributed to the linked observed listings and their historical captures. Missing values stay blank and appear on <a href="flagged.html">Flagged for review</a>. Check the current listing and variant before buying.</p>
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
<section class="hero hero-shop">
<div>
<p class="eyebrow">The Countertop Guide · kitchen gear, clearly compared</p>
<h1>Find the appliance that fits how you cook.</h1>
<p class="lede">Compare air fryers and meat thermometers by cooking style, capacity, counter space, and cleanup. Start with the setup you have in mind; use the listing links to check current details before buying.</p>
<p><a class="btn" href="air-fryers.html">Shop air fryers</a> <a class="btn secondary" href="thermometers.html">Shop thermometers</a></p>
<p class="small">Listing details and price snapshots recorded {VERIFIED}; prices and availability can change.</p>
</div>
<aside class="hero-aside" aria-label="Quick ways to compare">
<p class="eyebrow">Start with what matters</p>
<ul><li>Two baskets or one larger cooking area?</li><li>How much counter depth can you spare?</li><li>Instant-read or leave-in temperature monitoring?</li></ul>
<a href="compare.html">See all five side by side →</a>
</aside>
</section>
<p class="shop-note"><strong>Product note:</strong> these candidate listings reflect previously recorded destinations for the five supplied short links. The intended products and the Associates tracking report are not yet confirmed. See each listing's record for the distinction.</p>
<h2>Shop by category</h2>
<div class="grid cols-2">
  <article class="card category-card"><span class="tag">Air fryers · 3 listings</span><h3>Dual basket, oven-style, or single basket?</h3><p>Compare the cooking layouts, listed capacity, footprint, and cleanup details across three air fryer formats.</p><p><a class="btn small" href="air-fryers.html">Explore air fryers</a></p></article>
  <article class="card category-card"><span class="tag">Meat thermometers · 2 listings</span><h3>Instant-read or wireless probes?</h3><p>Compare handheld and leave-in styles, including the accuracy and range claims stated on each listing.</p><p><a class="btn small" href="thermometers.html">Explore thermometers</a></p></article>
</div>
<h2>Air fryers to compare</h2>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<h2>Meat thermometers to compare</h2>
<div class="grid cols-2">{product_card('P4')}{product_card('P5')}</div>
<h2>Not sure where to start?</h2>
<p>Answer three questions to get a shortlist based on the recorded listing fields. It is a starting point, not a hands-on recommendation.</p>
{CHOOSER}
<h2>Buying guides</h2>
<div class="grid cols-3">
  <article class="card"><span class="tag">Air fryer · form</span><h3>Basket or oven-style air fryer: what should you compare?</h3><p>Think through layout, cooking tasks, and the space each style needs.</p><p><a href="guide-basket-vs-oven.html">Read the guide</a></p></article>
  <article class="card"><span class="tag">Air fryer · capacity</span><h3>A no-hype checklist for comparing air fryer capacity</h3><p>What a quart count can and cannot tell you about usable cooking space.</p><p><a href="guide-capacity-checklist.html">Read the guide</a></p></article>
  <article class="card"><span class="tag">Counter space · cleanup</span><h3>How to assess cleanup and counter-space trade-offs</h3><p>Measure before you buy, and compare removable parts and care instructions.</p><p><a href="guide-cleanup-counter-space.html">Read the guide</a></p></article>
</div>
<p><a href="guides.html">Browse all guides</a> · <a href="suggestions.html">Explore the editorial plan</a></p>
"""
open("index.html","w").write(page("Air Fryers & Thermometers Compared | The Countertop Guide","Compare air fryers and meat thermometers by cooking style, capacity, counter space and cleanup. Browse question-led buying guides and check current listing details before you buy.",index_body,jsonld({"@context":"https://schema.org","@type":"WebSite","name":"The Countertop Guide","url":SITE["canonical"]})))
# ---------- AIR FRYERS ----------
af_body = f"""
<p class="eyebrow">Category - Air Fryers</p>
<h1>Air fryers: dual-basket, oven-style &amp; single-basket</h1>
<p class="lede">Compare the layouts first, then check capacity, counter depth, and cleanup. The notes below are listing-derived; no hands-on comparison is claimed.</p>
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<h2>Air fryer comparison</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>Chefman 6QT Dual-Basket<br>B0CDY277D3</th><th>Emeril 26QT French-Door<br>B09B7SB46R</th><th>Chefman 8QT TurboFry<br>B08DKYBTPH</th><th>Official listing sources</th></tr>
<tr><td>Form</td><td>Dual basket (2 x 3 Qt)</td><td>Oven-style, French door</td><td>Single basket</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Capacity (title)</td><td>6 Quart</td><td>26QT</td><td>8 quarts</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Capacity field on listing</td><td>6 liters <span class="badge-warn">unit differs - see Flagged</span></td><td>24.6 liters <span class="badge-warn">unit differs - see Flagged</span></td><td>8 quarts</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Dimensions (D x W x H)</td><td>13.38 x 11.81 x 10.63 in</td><td>16.9 x 15.8 x 14.8 in</td><td>12.75 x 13.5 x 10 in</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Counter depth</td><td>13.38 in (34.0 cm)</td><td>16.9 in (42.9 cm)</td><td>12.75 in (32.4 cm)</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Footprint (W x D)</td><td>158.0 sq in</td><td>267.0 sq in</td><td>172.1 sq in</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Capacity per sq in footprint*</td><td>0.038 qt/sq in</td><td>0.097 qt/sq in</td><td>0.046 qt/sq in</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Rating (historical snapshot)</td><td>4.2 (4,876)</td><td>4.3 (18,371)</td><td>4.4 (16,890)</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Price snapshot (new)</td><td>$79.93 (list $99.99)</td><td>$149.99 (list $209.99)</td><td>$69.99 (list $119.99)</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Wattage (listing bullets)</td><td>1700 W / 120 V</td><td><span class="badge-flag">Not captured - Flagged</span></td><td>1000 W / 120 V</td><td>{source_links(['P1','P2','P3'])}</td></tr>
<tr><td>Cleanup (listing)</td><td>Non-stick baskets dishwasher safe</td><td>See listing for accessory care</td><td>Basket + tray top-rack dishwasher safe</td><td>{source_links(['P1','P2','P3'])}</td></tr>
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
open("air-fryers.html","w").write(page("Air Fryers Compared: Dual-Basket, Oven-Style & Single-Basket | The Countertop Guide","Compare three air fryer listing profiles by layout, capacity, counter footprint, cleanup claims, and historical price snapshots. Check current details before buying.",af_body))
# ---------- THERMOMETERS ----------
th_body = f"""
<p class="eyebrow">Category - Thermometers</p>
<h1>Thermometers: instant-read vs wireless</h1>
<p class="lede">Instant-read and leave-in wireless thermometers answer different kitchen questions. Compare the listing claims below; accuracy has not been independently tested here.</p>
<div class="grid cols-2">{product_card('P4')}{product_card('P5')}</div>
<h2>Instant-read vs wireless</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>ThermoMaven Instant-Read<br>B0DHZTCNR5</th><th>CHEF iQ Sense Wireless<br>B0DZFD6R9Z</th><th>Official listing sources</th></tr>
<tr><td>Type</td><td>Handheld instant-read</td><td>Wireless probes + hub + app</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Accuracy claim (listing)</td><td>+/-0.5F, NIST &amp; NSF certified</td><td>4 internal + 1 ambient sensor (listing bullets); no +/-F figure captured</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Read / monitoring</td><td>1-second read (thermocouple, per bullets)</td><td>Real-time app updates, WiFi unlimited range, Bluetooth</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Probes</td><td>Single probe (handheld)</td><td>3 probes included (1/2/4-probe variants exist)</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Heat rating</td><td>- (not captured)</td><td>1000F heat-safe probes (per title/bullets)</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Waterproof / care</td><td>IP67; rinse under water (per title/bullets)</td><td>Care instructions not captured - see FLG-004</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Battery / charge</td><td>Not captured in this record - see FLG-004</td><td>Up to 50 hours per charge (per bullets)</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Rating (historical snapshot)</td><td>4.6 (3,499)</td><td>4.2 (2,178)</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Price snapshot</td><td>$16.99 (list $22.99)</td><td>$119.99 3-probe (list $219.99)</td><td>{source_links(['P4','P5'])}</td></tr>
<tr><td>Dimensions</td><td><span class="badge-flag">Not captured - see Flagged</span></td><td><span class="badge-flag">Not captured - see Flagged</span></td><td>{source_links(['P4','P5'])}</td></tr>
</table></div>
<h2>Guide</h2>
<ul><li><a href="guide-thermometer-accuracy.html">Instant-read or wireless? How to read accuracy claims without being misled</a></li></ul>
<p><a class="btn secondary" href="compare.html">Compare with air fryers</a></p>
"""
open("thermometers.html","w").write(page("Meat Thermometers Compared: Instant-Read vs Wireless | The Countertop Guide","Compare two meat thermometer listing profiles: instant-read and wireless probes, with historical accuracy claims, sensor details, and price snapshots.",th_body))
# ---------- COMPARE ----------
compare_body = f"""
<p class="eyebrow">Comparison</p>
<h1>All five products, side by side</h1>
<p class="lede">Compare the recorded listing fields side by side. Each product row includes a direct official listing source; derived footprint ratios include their calculation method. Price and rating figures are historical snapshots dated {VERIFIED}.</p>
<h2>Three-question chooser</h2>
{CHOOSER}
<h2>Full comparison</h2>
<div class="table-scroll"><table>
<tr><th>Field</th><th>P1 Chefman 6QT Dual<br>B0CDY277D3</th><th>P2 Emeril 26QT Oven<br>B09B7SB46R</th><th>P3 Chefman 8QT Basket<br>B08DKYBTPH</th><th>P4 ThermoMaven Instant<br>B0DHZTCNR5</th><th>P5 CHEF iQ Wireless<br>B0DZFD6R9Z</th><th>Official listing sources</th></tr>
<tr><td>Category / form</td><td>Air Fryers - Dual basket</td><td>Air Fryers - Oven-style</td><td>Air Fryers - Single basket</td><td>Thermometers - Instant-read</td><td>Thermometers - Wireless</td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
<tr><td>Capacity</td><td>6 Quart (title) / 6 liters (field)</td><td>26QT (title) / 24.6 liters (field)</td><td>8 quarts</td><td>-</td><td>-</td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
<tr><td>Dimensions</td><td>13.38D x 11.81W x 10.63H in</td><td>16.9D x 15.8W x 14.8H in</td><td>12.75D x 13.5W x 10H in</td><td>Not captured</td><td>Not captured</td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
<tr><td>Rating snapshot</td><td>4.2 (4,876)</td><td>4.3 (18,371)</td><td>4.4 (16,890)</td><td>4.6 (3,499)</td><td>4.2 (2,178)</td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
<tr><td>Price snapshot (new)</td><td>$79.93</td><td>$149.99</td><td>$69.99</td><td>$16.99</td><td>$119.99 (3-probe)</td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
<tr><td>List price snapshot</td><td>$99.99</td><td>$209.99</td><td>$119.99</td><td>$22.99</td><td>$219.99</td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
<tr><td>Key differentiator (listing)</td><td>Sync Finish, 2x3 Qt baskets</td><td>French door, rotisserie, 12 in pizza</td><td>450F Hi-Fry, dishwasher-safe basket</td><td>1-sec, +/-0.5F NIST</td><td>WiFi, 3 probes, 1000F-safe</td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
<tr><td>Sponsored listing links</td>
<td><a href="{aff(PRODS['P1'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P1']['observedAsin']}">Amazon · sponsored</a></td>
<td><a href="{aff(PRODS['P2'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P2']['observedAsin']}">Amazon · sponsored</a></td>
<td><a href="{aff(PRODS['P3'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P3']['observedAsin']}">Amazon · sponsored</a></td>
<td><a href="{aff(PRODS['P4'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P4']['observedAsin']}">Amazon · sponsored</a></td>
<td><a href="{aff(PRODS['P5'])}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{PRODS['P5']['observedAsin']}">Amazon · sponsored</a></td>
<td>Tracking tests not recorded; see <a href="verification.html">intent register</a>.</td></tr>
<tr><td>Verification record</td><td><a href="verification.html#P1">P1 record</a></td><td><a href="verification.html#P2">P2 record</a></td><td><a href="verification.html#P3">P3 record</a></td><td><a href="verification.html#P4">P4 record</a></td><td><a href="verification.html#P5">P5 record</a></td><td>{source_links(['P1','P2','P3','P4','P5'])}</td></tr>
</table></div>
<p class="small">Every Amazon-bound product link is marked sponsored. Price and rating snapshots are dated {VERIFIED}; always check the current listing and variant.</p>
<h2>Counter-space analysis (air fryers only)</h2>
<div class="table-scroll"><table>
<tr><th>Air fryer</th><th>Depth</th><th>Footprint</th><th>Capacity</th><th>Capacity per cm depth*</th><th>Capacity per sq in*</th><th>Official listing source</th></tr>
<tr><td>Chefman 6QT Dual (B0CDY277D3)</td><td>34.0 cm</td><td>158.0 sq in</td><td>6 qt</td><td>0.18 qt/cm</td><td>0.038 qt/sq in</td><td>{source_links(['P1'])}</td></tr>
<tr><td>Emeril 26QT Oven (B09B7SB46R)</td><td>42.9 cm</td><td>267.0 sq in</td><td>26 qt</td><td>0.61 qt/cm</td><td>0.097 qt/sq in</td><td>{source_links(['P2'])}</td></tr>
<tr><td>Chefman 8QT Basket (B08DKYBTPH)</td><td>32.4 cm</td><td>172.1 sq in</td><td>8 qt</td><td>0.25 qt/cm</td><td>0.046 qt/sq in</td><td>{source_links(['P3'])}</td></tr>
</table></div>
<p class="small">* Derived by us: depth in cm = inches x 2.54; footprint = width x depth; ratios use title capacity. Thermometers excluded (dimensions not captured). Method and limits in <a href="guide-cleanup-counter-space.html">cleanup &amp; counter-space guide</a>.</p>
"""
open("compare.html","w").write(page("Compare Air Fryers & Thermometers Side by Side | The Countertop Guide","Compare five historical candidate listings by capacity, dimensions, footprint, recorded ratings and prices, with source links and a three-question shortlist tool.",compare_body))
# ---------- GUIDES INDEX ----------
guides_body = """
<p class="eyebrow">Buyer guides</p>
<h1>Questions to ask before you buy</h1>
<p class="lede">Each guide starts with a real product decision and works from the listing details that were captured. We separate seller wording from our calculations and say where the listings leave a gap. Titles are editorial hypotheses, not measured search-demand claims.</p>
<div class="grid cols-2">
<article class="card"><span class="tag">Air fryers · format</span><h3>Basket or oven-style air fryer: what should you compare?</h3><p>Compare layout, dimensions, food examples, and the questions a product listing cannot answer.</p><p><a class="btn small" href="guide-basket-vs-oven.html">Read the guide</a></p></article>
<article class="card"><span class="tag">Air fryers · capacity</span><h3>A no-hype checklist for comparing air fryer capacity</h3><p>Separate title capacity from product fields, basket layout, and seller serving examples.</p><p><a class="btn small" href="guide-capacity-checklist.html">Read the guide</a></p></article>
<article class="card"><span class="tag">Counter space · cleanup</span><h3>How to assess cleanup and counter-space trade-offs</h3><p>Measure width and depth, compare removable parts, and check the current care instructions.</p><p><a class="btn small" href="guide-cleanup-counter-space.html">Read the guide</a></p></article>
<article class="card"><span class="tag">Multi-function ovens</span><h3>Questions to ask before buying a multi-function kitchen appliance</h3><p>Presets, accessories, wattage, fit, and the fields still missing from the captured listing.</p><p><a class="btn small" href="guide-multifunction-questions.html">Read the guide</a></p></article>
<article class="card"><span class="tag">Meat thermometers</span><h3>Instant-read or wireless? How to read accuracy claims</h3><p>Compare what the listings say about tolerance, sensors, connectivity, and what has not been tested.</p><p><a class="btn small" href="guide-thermometer-accuracy.html">Read the guide</a></p></article>
</div>
<p class="small">Next-topic ideas—including seasonal cooking and gift questions—are listed separately on the <a href="suggestions.html">editorial decision board</a>. They are not published as demand or popularity claims.</p>
"""
open("guides.html","w").write(page("Buyer Guides: Air Fryers & Meat Thermometers | The Countertop Guide","Question-led guides for comparing air fryer formats, capacity, cleanup, counter space, multi-function features, and meat thermometer claims.",guides_body))
# ---------- GUIDE 1 ----------
b1, j1 = guide_shell("Guide · Air fryer formats", "Basket or oven-style air fryer: what should you compare?",
 "There is no universal winner in the product title. Compare the cooking layout, the outside dimensions, the listing's capacity wording, and the parts you will need to clean. The examples here are listing-based, not a cooking test.",
 """
<h2>Three formats, three different layouts</h2>
<p><strong>Dual basket.</strong> The historical Chefman 6-quart listing describes two 3-quart baskets and a Sync Finish feature. That tells you how the compartments are arranged; it does not tell us whether two dishes cook evenly or finish at the same quality. <a href="https://www.amazon.com/dp/B0CDY277D3">Check the listing</a>.</p>
<p><strong>French-door oven style.</strong> The Emeril listing describes a 26-quart capacity, rotisserie, and a 12-inch pizza. It also lists a 16.9-inch depth. Treat “feeds 4–6” and food-size examples as seller claims, then check the current listing and accessories. <a href="https://www.amazon.com/dp/B09B7SB46R">Check the listing</a>.</p>
<p><strong>Single basket.</strong> The Chefman 8-quart listing describes a single non-stick basket and a flat tray; its listing capture gives a 12.75-inch depth. A single cavity and a split pair of baskets are not interchangeable measures of usable cooking area. <a href="https://www.amazon.com/dp/B08DKYBTPH">Check the listing</a>.</p>
<h2>Put the footprint next to the capacity</h2>
<p>Measure the counter depth and width you can actually spare. These historical outside dimensions do not include the clearance needed for doors, vents, cords, or manufacturer installation instructions.</p>
<div class="table-scroll"><table><tr><th>Observed listing</th><th>Listed depth</th><th>Listed width</th><th>Questions to check</th><th>Official source</th></tr>
<tr><td>Chefman dual basket · 6 qt title</td><td>13.38 in</td><td>11.81 in</td><td>Will the baskets and handles be easy to access?</td><td>{source_links(['P1'])}</td></tr>
<tr><td>Emeril French-door · 26 qt title</td><td>16.9 in</td><td>15.8 in</td><td>Is there room to open the doors and follow the manual's clearance guidance?</td><td>{source_links(['P2'])}</td></tr>
<tr><td>Chefman single basket · 8 qt title</td><td>12.75 in</td><td>13.5 in</td><td>Does the wider single-basket layout work on your counter?</td><td>{source_links(['P3'])}</td></tr></table></div>
<h2>A practical short list of questions</h2>
<ol><li>Do you want two independently controlled compartments, or one cavity?</li><li>Which foods and portions matter to you? Compare those examples to what the current listing actually states.</li><li>Measure width and depth, then verify clearance in the manual. Product dimensions alone do not answer ventilation or door-swing questions.</li><li>Check which removable parts are dishwasher-safe, and confirm the exact care directions on the listing or manual.</li></ol>
<p>We have not cooked in these appliances. Crispness, noise, evenness, durability, and real-world cleanup remain unknown; see <a href="flagged.html#FLG-010">the testing flag</a>. The full listing comparison is on the <a href="air-fryers.html">air-fryer page</a>.</p>
""",
 [("Which is better, basket or oven-style air fryer?","The listings describe different layouts; they do not establish a universal winner. Choose by cooking needs, counter fit, and the current care/clearance instructions."),
  ("How deep is the Emeril listing?","The historical listing capture records 16.9 inches (42.9 cm) depth. Re-check the current product page and manual before measuring for fit."),
  ("Does a dual basket prove two foods finish equally?","No. The listing describes separate baskets and Sync Finish; we have not tested cooking results.")])
open("guide-basket-vs-oven.html","w").write(page("Basket or Oven-Style Air Fryer: What Should You Compare? | The Countertop Guide","Compare air fryer layout, listed capacity wording, exterior dimensions, and care questions without assuming one format is best.",b1,j1,"guide-page"))
# ---------- GUIDE 2 ----------
b2, j2 = guide_shell("Guide · Capacity", "A no-hype checklist for comparing air fryer capacity",
 "A quart figure is a starting point, not a serving-size guarantee. Before comparing numbers, check whether they describe a single cavity, split baskets, or a seller's food example.",
 """
<h2>1. Keep the title and product-detail fields separate</h2>
<p>Two historical listing captures show different capacity wording in the title and the product field. Do not silently convert or choose the number that looks more favorable: the Chefman dual-basket title says 6 quart while its field says 6 liters; the Emeril title says 26QT while its field says 24.6 liters. Both rows are flagged for re-check. <a href="flagged.html#FLG-002">See the discrepancy note</a>.</p>
<div class="table-scroll"><table><tr><th>Observed listing</th><th>Title wording in capture</th><th>Product field in capture</th><th>Source</th></tr>
<tr><td>Chefman dual basket</td><td>6 Quart (2 × 3 Qt)</td><td>6 liters</td><td>{source_links(['P1'])}</td></tr>
<tr><td>Emeril French-door oven</td><td>26QT</td><td>24.6 liters</td><td>{source_links(['P2'])}</td></tr>
<tr><td>Chefman single basket</td><td>8 quarts</td><td>8 quarts</td><td>{source_links(['P3'])}</td></tr></table></div>
<h2>2. Ask what the capacity describes</h2>
<p>Two 3-quart baskets are split cooking zones. An 8-quart single basket is one cavity. A French-door oven has a different shape again. A total volume does not tell you the size of a tray, how much food fits in one layer, or whether two foods can be cooked together.</p>
<h2>3. Treat serving and food-size examples as listing claims</h2>
<p>The Emeril listing capture mentions 4–6 people, a 6-pound rotisserie chicken, and a 12-inch pizza. Those are seller examples, not a tested serving count. If one of those tasks matters to you, check the live listing, included accessories, and any current manual before buying.</p>
<h2>4. Measure the outside and leave room for use</h2>
<p>Compare the stated exterior dimensions with your counter, then check door swing, handles, ventilation, and the manufacturer's clearance instructions. Those practical constraints are not answered by the quart number. For dimension and footprint notes, see the <a href="compare.html">side-by-side comparison</a>.</p>
<h2>5. Write down what is missing</h2>
<p>For these captured listings, the Emeril wattage and two thermometer dimensions were not recorded. Missing details stay blank rather than being estimated. See <a href="flagged.html">the open evidence list</a>.</p>
""",
 [("Is 6 quarts the same as 6 litres?","No. The historical Chefman listing capture uses 6 Quart in the title and 6 liters in a product field. We preserve both labels and flag the discrepancy; check the current listing."),
  ("Does a quart count tell me how many people an appliance feeds?","Not by itself. The Emeril listing makes a 4–6 people claim, but serving size and cooking method vary; we have not tested portions."),
  ("Can I compare two baskets with one larger basket by total capacity?","You can compare the stated totals, but basket layout and usable cooking area differ. Check compartment size and food examples rather than treating the totals as equivalent.")])
open("guide-capacity-checklist.html","w").write(page("A No-Hype Checklist for Comparing Air Fryer Capacity | The Countertop Guide","A careful guide to air fryer capacity labels, split baskets, seller serving examples, exterior dimensions, and missing fields.",b2,j2,"guide-page"))
# ---------- GUIDE 3 ----------
b3, j3 = guide_shell("Guide · Space and cleanup", "How to assess cleanup and counter-space trade-offs",
 "A product's outside dimensions, removable parts, and care instructions are more useful than a vague promise that it is “compact” or “easy to clean.” Here is a simple way to compare them before you order.",
 """
<h2>Measure the actual counter area</h2>
<p>Write down usable width and depth, including any nearby wall or cabinet constraints. The table uses the listing dimensions captured on {VERIFIED}; footprint is our calculation of listed width × depth, not a manufacturer measurement of required clearance.</p>
<div class="table-scroll"><table><tr><th>Observed listing</th><th>Depth × width</th><th>Footprint calculation</th><th>Official source</th></tr>
<tr><td>Chefman 6QT dual basket</td><td>13.38 × 11.81 in</td><td>158.0 sq in</td><td>{source_links(['P1'])}</td></tr>
<tr><td>Emeril 26QT French-door oven</td><td>16.9 × 15.8 in</td><td>267.0 sq in</td><td>{source_links(['P2'])}</td></tr>
<tr><td>Chefman 8QT single basket</td><td>12.75 × 13.5 in</td><td>172.1 sq in</td><td>{source_links(['P3'])}</td></tr></table></div>
<p>Footprint = depth × width. It does not include space for door swing, handles, heat, vents, or cord routing. Check the current manual for safe clearances; those are not inferred from this calculation.</p>
<h2>Compare cleanup claims without pretending to have tested</h2>
<ul>
<li>Chefman 6QT listing capture: removable non-stick baskets described as dishwasher-safe. <a href="https://www.amazon.com/dp/B0CDY277D3">Check the current listing</a>.</li>
<li>Chefman 8QT listing capture: basket and flat tray described as top-rack dishwasher-safe. <a href="https://www.amazon.com/dp/B08DKYBTPH">Check the current listing</a>.</li>
<li>Emeril 26QT title lists six accessories; their individual care instructions were not captured. <a href="https://www.amazon.com/dp/B09B7SB46R">Check the current listing</a>.</li>
</ul>
<p>Before ordering, confirm which pieces are removable, which are dishwasher-safe, and whether the current manual adds care or clearance requirements. We have not washed or measured these appliances ourselves.</p>
<h2>Turn it into your own checklist</h2>
<ol><li>Measure counter width and depth.</li><li>Compare the dimensions—not only the listed capacity.</li><li>Check door/basket access and the manual's clearance directions.</li><li>Confirm care directions for each removable part.</li></ol>
""",
 [("Which listing has the smallest calculated footprint?","The historical dimensions calculate to 158.0 square inches for the Chefman 6QT dual basket, 172.1 for the Chefman 8QT, and 267.0 for the Emeril oven. This is an outside-dimension calculation, not a space-clearance recommendation."),
  ("Are the baskets dishwasher-safe?","The captured listings describe dishwasher-safe parts for the two Chefman models. Check the current listing/manual for exact parts and care instructions; we have not tested cleaning."),
  ("How do you calculate footprint?","Multiply the listed outside width by depth. It is a derived estimate from the historical listing dimensions and excludes door swing, ventilation, cord routing, and other clearance needs.")])
open("guide-cleanup-counter-space.html","w").write(page("How to Assess Cleanup and Counter-Space Trade-Offs | The Countertop Guide","A practical checklist for measuring appliance width and depth, comparing calculated footprints, and checking listed care instructions.",b3,j3,"guide-page"))
# ---------- GUIDE 4 ----------
b4, j4 = guide_shell("Guide · Multi-function", "Questions to ask before buying a multi-function kitchen appliance",
 "A long feature list is not a use case. Before comparing a multi-function oven, match the tasks you expect to do with the accessories, dimensions, care instructions, and electrical details the seller actually publishes.",
 """
<h2>Use the listing as a checklist, not a verdict</h2>
<div class="table-scroll"><table><tr><th>Question</th><th>What the historical listing capture says</th><th>What still needs checking</th><th>Official source</th></tr>
<tr><td>How many presets?</td><td>Emeril title says 24; bullets say 25. The count conflicts in the capture.</td><td>Confirm the current wording; do not choose one number silently.</td><td>{source_links(['P2'])}</td></tr>
<tr><td>Which functions are listed?</td><td>Air Fry, Convection Bake, Rotisserie, Toast, Grill, Dehydrate, Roast, Slow Cook, Broil.</td><td>Whether each mode suits your recipes and how it performs were not tested here.</td><td>{source_links(['P2'])}</td></tr>
<tr><td>What accessories are included?</td><td>The title says six cooking accessories.</td><td>The exact list, care instructions, and what fits the appliance.</td><td>{source_links(['P2'])}</td></tr>
<tr><td>What electrical details matter?</td><td>Wattage was not captured in this record.</td><td>Check the current product details and manual for your kitchen setup.</td><td>{source_links(['P2'])}</td></tr>
<tr><td>Does the appliance fit?</td><td>Recorded dimensions: 16.9D × 15.8W × 14.8H inches.</td><td>Allow for doors, handles, ventilation, and manual clearances.</td><td>{source_links(['P2'])}</td></tr></table></div>
<h2>Before you compare models</h2>
<ol><li>List the cooking tasks you actually expect to use.</li><li>Check the current listing and manual for accessory names and care.</li><li>Measure the counter and verify electrical and clearance requirements from the manufacturer.</li><li>Separate listing claims from tested performance. This publication has not tested the Emeril oven.</li></ol>
<p>The listing capture also contains a preset-count discrepancy and missing wattage/warranty fields; see <a href="flagged.html#FLG-002">the flagged record</a>. A feature list cannot tell you how well a function cooks.</p>
""",
 [("How many presets does the Emeril 26QT list?","The capture says 24 one-touch presets in the title and 25 presets in bullets. The count discrepancy is flagged; check the current listing."),
  ("Which accessories come with the oven?","The title says six accessories, but the exact list was not captured here. Check the current listing before making a purchase decision."),
  ("What is the Emeril wattage?","It was not captured in the historical record. Use the current product details and manufacturer manual rather than guessing.")], shortlist_pids=("P2",))
open("guide-multifunction-questions.html","w").write(page("Questions to Ask Before Buying a Multi-Function Kitchen Appliance | The Countertop Guide","A pre-purchase checklist for multi-function appliance presets, accessories, fit, electrical details, and information not captured in a product listing.",b4,j4,"guide-page"))
# ---------- GUIDE 5 ----------
b5, j5 = guide_shell("Guide · Meat thermometers", "Instant-read or wireless? How to read accuracy claims",
 "“One second,” “±0.5°F,” and “unlimited range” are different claims. Here is how to compare what the listings actually say—without treating marketing language as an independent test.",
 """
<h2>Instant-read listing: ThermoMaven</h2>
<p>The historical title and bullet capture states ±0.5°F accuracy, NIST/NSF certification, a one-second thermocouple read, IP67 waterproofing, and an auto-rotating display. Those are listing claims; we have not calibrated the thermometer or checked a certificate. <a href="https://www.amazon.com/dp/B0DHZTCNR5">Review the current listing</a>.</p>
<h2>Wireless listing: CHEF iQ Sense</h2>
<p>The capture describes three probes, a hub, WiFi and Bluetooth connectivity, and a five-sensor arrangement: four internal sensors plus one ambient sensor according to the bullets. A numeric ± accuracy figure was not captured. “Unlimited range” is the listing's phrase, not an independent range test. <a href="https://www.amazon.com/dp/B0DZFD6R9Z">Review the current listing</a>.</p>
<h2>Questions worth asking</h2>
<ol><li><strong>What does the number measure?</strong> Look for a stated accuracy tolerance and its conditions; do not infer one from sensor count or reading speed.</li><li><strong>What is included?</strong> Probe count, hub, charging method, and app requirements can vary by selected variant.</li><li><strong>How will you use it?</strong> A handheld instant-read and a leave-in probe are different workflows. The listings do not tell us which routine will suit you better.</li><li><strong>What remains untested?</strong> Real reading speed, calibration, app reliability, connectivity through your kitchen, and long-term durability.</li></ol>
<p>We have not independently tested either thermometer. Compare the recorded product details on the <a href="thermometers.html">thermometer page</a> and verify the selected variant before ordering.</p>
""",
 [("Which thermometer is more accurate?","The ThermoMaven listing capture states ±0.5°F; no numeric ± figure was captured for the CHEF iQ. We have not tested either unit, so this is not an independent accuracy ranking."),
  ("What does five sensors mean on the CHEF iQ?","The historical listing bullets describe four internal temperature sensors and one ambient sensor. Check the current product page and selected variant."),
  ("Does ‘unlimited range’ guarantee connection anywhere?","No independent range result is available here. The phrase appears in the listing; actual connectivity depends on the product setup and conditions, which were not tested by this publication.")], shortlist_pids=("P4", "P5"))
open("guide-thermometer-accuracy.html","w").write(page("Instant-Read or Wireless? How to Read Thermometer Claims | The Countertop Guide","Compare historical listing claims about meat thermometer accuracy, reading speed, sensor counts, connectivity, and what still needs hands-on testing.",b5,j5,"guide-page"))
# ---------- EXECUTIVE SUMMARY ----------
exec_body = f"""
<p class="eyebrow">Executive summary</p>
<h1>What is ready, what is provisional, and what cannot be guessed</h1>
<p class="lede">The Countertop Guide is a product-led publication for air fryers and meat thermometers. It includes five candidate listing profiles, category comparisons, a chooser, and question-led buyer guides. The listing values are historical captures dated {VERIFIED}; this integration did not fetch Amazon pages or policy pages again.</p>
<h2>Five candidate listings in the current comparison</h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Listing profile</th><th>Observed ASIN</th><th>Category</th><th>Recorded price</th><th>Recorded rating</th><th>Official listing source</th></tr>
<tr><td>P1</td><td>Chefman 6QT Dual-Basket Air Fryer Oven</td><td>B0CDY277D3</td><td>Air Fryers</td><td>$79.93 · {VERIFIED}</td><td>4.2 (4,876) · {VERIFIED}</td><td>{source_links(['P1'])}</td></tr>
<tr><td>P2</td><td>Emeril Lagasse 26QT French-Door Oven</td><td>B09B7SB46R</td><td>Air Fryers</td><td>$149.99 · {VERIFIED}</td><td>4.3 (18,371) · {VERIFIED}</td><td>{source_links(['P2'])}</td></tr>
<tr><td>P3</td><td>Chefman 8QT TurboFry Basket</td><td>B08DKYBTPH</td><td>Air Fryers</td><td>$69.99 · {VERIFIED}</td><td>4.4 (16,890) · {VERIFIED}</td><td>{source_links(['P3'])}</td></tr>
<tr><td>P4</td><td>ThermoMaven 1-Second Instant-Read</td><td>B0DHZTCNR5</td><td>Thermometers</td><td>$16.99 · {VERIFIED}</td><td>4.6 (3,499) · {VERIFIED}</td><td>{source_links(['P4'])}</td></tr>
<tr><td>P5</td><td>CHEF iQ Sense Wireless (3 probes)</td><td>B0DZFD6R9Z</td><td>Thermometers</td><td>$119.99 · {VERIFIED}</td><td>4.2 (2,178) · {VERIFIED}</td><td>{source_links(['P5'])}</td></tr>
</table></div>
<h2>What the record supports</h2>
<ul>
<li>Earlier repository notes record five submitted short-link destinations and Amazon listing captures dated {VERIFIED}. The observed ASINs and listing URLs are kept as observations; they do not establish the intended product.</li>
<li>Each product-intent record now has separate fields for intended ASIN, official intended listing URL, confirmation date, and confirmation source. Those fields are blank pending confirmation; see <a href="verification.html">the register</a> and <a href="flagged.html#FLG-013">FLG-013</a>.</li>
<li>The root publication has unique page titles/descriptions and self-canonical URLs. The published sitemap lists buyer-facing pages; RSS is generated from the guide manifest. Internal decision pages remain reachable from the footer but are not submitted for indexing.</li>
<li>Every outbound Amazon product link carries <code>rel="sponsored"</code>. The client/server event contract and local endpoint tests are aligned; the endpoint is not hosted, so no site-wide event data is being collected.</li>
</ul>
<h2>Open verification and compliance gates</h2>
<ul>
<li>Associates Central: the exact compliance/attribution status of the submitted short links is unresolved. A tagged link per confirmed product still needs a destination check and a tracking-report check. We do not claim the supplied links are invalid.</li>
<li>Product data: prices and ratings are time-sensitive historical snapshots; thermometer dimensions and some appliance fields are missing. Re-check official sources before keeping or refreshing these values. API/content permissions were not freshly reviewed here.</li>
<li>Search Console: the public site URL and sitemap are defined, but account ownership, indexing, and query reports are not confirmed.</li>
<li>Measurement: only browser-local aggregate counts work while the endpoint URL is blank. A separate HTTPS host and a final hosting/privacy decision are required; conversions and revenue must come from authorized first-party reports.</li>
<li>Photography and testing: no product photos or hands-on test claims are used. Use original photography only after rights and permissions are documented; publish testing claims only after the test is actually done.</li>
</ul>
<h2>Editorial path</h2>
<p>Proposed four-week pilot: publish one sourced, question-led guide per week, then review aggregated Search Console queries monthly once the property is verified. Current titles are editorial hypotheses, not measured demand or popularity claims. The campaign ledger starts empty; no orders, conversion score, or revenue forecast is shown.</p>
<p>See the <a href="suggestions.html">suggestion and decision board</a>, <a href="methodology.html">method and empty ledger</a>, and <a href="compliance.html">publishing checklist</a>.</p>
"""
open("executive-summary.html","w").write(page("Executive Summary: Publication Readiness & Open Gates | The Countertop Guide","Executive summary of the buyer publication, five historical candidate listings, blank product-intent confirmations, search and analytics readiness, and remaining compliance gates.",exec_body))
# ---------- SUGGESTIONS ----------
sugg_body = f"""
<p class="eyebrow">Editorial desk</p>
<h1>Ideas, evidence gaps, and a path to the next release</h1>
<p class="lede">This page separates work already in place from choices that need account access, rights, or real audience evidence. Titles below are editorial hypotheses, not search-volume claims. Nothing is implemented just because it appears on this board.</p>
<div class="callout decision-callout"><strong>Recommended order</strong><ol><li>Confirm intended products, then test one Associates Special Link per product and its report.</li><li>Verify the Search Console property and submit the single root sitemap.</li><li>Keep the self-hosted event collector off until an HTTPS host, privacy notice, and retention choice are approved.</li><li>Use licensed original photos and hands-on testing only after rights, budget, and a protocol are documented.</li></ol><p>This path avoids spending on content or measurement before product identity and attribution are checked.</p></div>
<h2>Suggestions to review</h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Suggestion / path</th><th>Why it may help</th><th>What is missing / how to discover it</th><th>Effort</th><th>Current status</th><th>Your local choice</th></tr>
<tr><td>SG-01</td><td>Test one Special Link per confirmed product in Associates Central; verify destination and tracking report.</td><td>Checks the attribution path before any broader promotion; it does not guarantee earnings.</td><td>Product intent, enrolled workflow result, report reference. Record a dated result for each link.</td><td>Low; account access</td><td><span class="badge-warn">Open gate</span></td><td><select data-decision-id="SG-01" aria-label="Review SG-01"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-02</td><td>Verify the canonical GitHub Pages property in Search Console and submit the root sitemap.</td><td>Creates a route to inspect indexing and measured search queries.</td><td>Verified account ownership and Search Console reports; neither is available in this repository.</td><td>Low; account access</td><td><span class="badge-warn">Awaiting verification</span></td><td><select data-decision-id="SG-02" aria-label="Review SG-02"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-03</td><td>Host the self-hosted five-event collector and review aggregate counts weekly.</td><td>Could provide site-wide outbound-click counts without raw query or per-user records.</td><td>HTTPS host, access controls, host log policy, retention and privacy notice. Code is tested; service is not hosted.</td><td>Medium; separate service</td><td><span class="badge-warn">Code ready; host undecided</span></td><td><select data-decision-id="SG-03" aria-label="Review SG-03"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-04</td><td>Add real product photography only from original shoots or documented manufacturer permission.</td><td>Could make product differences easier to see; impact is unmeasured.</td><td>Rights/permission record, photo source, accurate model match. Do not use copied or generated product photos.</td><td>Medium</td><td><span class="badge-warn">Rights decision needed</span></td><td><select data-decision-id="SG-04" aria-label="Review SG-04"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-05</td><td>Draft seasonal kitchen-gift guides as working-title experiments.</td><td>Creates useful seasonal coverage if reader needs and product fit support it; traffic/conversion impact is unknown.</td><td>Confirm each use case and item detail from an official source; review Search Console after launch.</td><td>Low–medium</td><td><span class="badge-warn">Hypothesis only</span></td><td><select data-decision-id="SG-05" aria-label="Review SG-05"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-06</td><td>Expand the three-question chooser after usability feedback.</td><td>Could help readers narrow choices by cooking style, available counter depth, and budget.</td><td>Reader feedback or a small usability test; do not infer a winner from the chooser.</td><td>Low</td><td><span class="badge-warn">Proposed</span></td><td><select data-decision-id="SG-06" aria-label="Review SG-06"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-07</td><td>Offer an optional reader email signup only after provider and consent review.</td><td>Gives readers a way to request new guides; no list is collected now.</td><td>Provider, explicit consent wording, unsubscribe/deletion path, retention, privacy review.</td><td>Medium</td><td><span class="badge-warn">Deferred; no capture</span></td><td><select data-decision-id="SG-07" aria-label="Review SG-07"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-08</td><td>Revisit alternative product models only after a fresh official listing and variant check.</td><td>Could reveal whether a different submitted variant better matches the intended item.</td><td>Intended ASIN, variant, current official product details and authorized commission report; no margin is assumed.</td><td>Low–medium</td><td><span class="badge-warn">Needs evidence</span></td><td><select data-decision-id="SG-08" aria-label="Review SG-08"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-09</td><td>Run a hands-on testing programme with a published protocol.</td><td>Can support lived-with observations that listing specs cannot answer.</td><td>Budget, owned/loaned sample status, test methods, repeatability, disclosure context, and original photos.</td><td>High</td><td><span class="badge-warn">Not done; no test claims</span></td><td><select data-decision-id="SG-09" aria-label="Review SG-09"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-10</td><td>Expand to another appliance category only after the current cluster has sourced coverage.</td><td>Could deepen comparisons and internal links without spreading thin.</td><td>Editorial capacity, intended products, authoritative source records, and query evidence.</td><td>Medium</td><td><span class="badge-warn">Proposed</span></td><td><select data-decision-id="SG-10" aria-label="Review SG-10"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-27</td><td>Keep the masthead buyer-first; group verification, compliance, measurement, and suggestions together in the footer.</td><td>Helps the front page read like a publication while keeping every dashboard surface reachable.</td><td>Navigation and footer link check; implemented in the root site.</td><td>Done</td><td><span class="badge-ok">Implemented</span></td><td><select data-decision-id="SG-27" aria-label="Review SG-27"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-28</td><td>Ship and maintain the RSS feed; add each new guide from the publication manifest.</td><td>Provides a reader-facing update channel and a reproducible publishing workflow.</td><td>Feed and sitemap are generated from the same guide manifest; verify build output on every release.</td><td>Done + ongoing</td><td><span class="badge-ok">Implemented</span></td><td><select data-decision-id="SG-28" aria-label="Review SG-28"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-29</td><td>Set up Search Console and use measured queries for the next topic review.</td><td>Replaces guesses about demand with first-party search reports after indexing.</td><td>Account verification and query data; this task cannot be completed without account access.</td><td>Low; account access</td><td><span class="badge-warn">Awaiting verification</span></td><td><select data-decision-id="SG-29" aria-label="Review SG-29"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-30</td><td>Consider a permission-based reader-capture option only after the privacy and consent questions are answered.</td><td>Lets readers opt in to future guides without silently collecting addresses.</td><td>Provider, data controller, consent, unsubscribe, retention, deletion, and privacy copy.</td><td>Medium</td><td><span class="badge-warn">Deferred; no capture</span></td><td><select data-decision-id="SG-30" aria-label="Review SG-30"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
<tr><td>SG-31</td><td>Run a four-week pilot at one original question-led guide per week, then review queries monthly.</td><td>Creates a manageable publishing rhythm without making unsupported popularity claims.</td><td>Editorial hours, fact-checking time, and Search Console access for later measurement.</td><td>Low–medium</td><td><span class="badge-warn">Proposed pilot</span></td><td><select data-decision-id="SG-31" aria-label="Review SG-31"><option value="">Choose…</option><option value="approve">Approve</option><option value="defer">Defer</option><option value="reject">Reject</option></select></td></tr>
</table></div>
<h2>Review choices (saved only in this browser)</h2>
<div class="card decision-tools"><p>Choose Approve, Defer, or Reject per suggestion. Your selections stay on this device; they are not sent to the site, do not change published pages, and do not create work automatically.</p><p><button type="button" class="btn small" id="download-decision-record">Download decision record</button> <button type="button" class="btn small secondary" id="clear-decision-record">Clear local choices</button></p><p id="decision-save-status" class="small" aria-live="polite">No changes saved in this browser.</p></div>
<h2>Questions, current information, and how to close the gaps</h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Question</th><th>What is known</th><th>What is unknown</th><th>How to discover it</th><th>Decision blocked</th></tr>
<tr><td>Q-01</td><td>Which exact product did each submitted short link intend?</td><td>Five short URLs were supplied; prior repository notes record observed destinations.</td><td>The intended ASIN, official intended listing URL, confirmation date, and source are blank.</td><td>Confirm each intended item independently in the enrolled Associates workflow; store the intended record separately from the redirect observation.</td><td>Product selection and final outbound destination</td></tr>
<tr><td>Q-02</td><td>Do the candidate outbound links attribute correctly?</td><td>Tracking ID text is <code>shopnow047c-20</code>; candidate tagged URLs are in the site.</td><td>Associates enrollment, Special Link status, destination behavior, and tracking-report result.</td><td>Test one link per confirmed product in Associates Central; preserve the dated report reference. Do not infer validity from URL shape.</td><td>Scaling affiliate promotion</td></tr>
<tr><td>Q-03</td><td>Is the site indexed, and what queries reach it?</td><td>Canonical site URL is <code>https://wingbangboozle1-lang.github.io/Prod1/</code>; one root sitemap is generated.</td><td>Search Console ownership, indexing state, query/click reports.</td><td>Verify the URL-prefix property in Search Console, submit the sitemap, and review page/query data after it accrues.</td><td>Measured topic choices</td></tr>
<tr><td>Q-04</td><td>Can the site collect aggregate click events?</td><td>The five-event browser/server contract is tested; the published endpoint setting is blank.</td><td>HTTPS host, access policy, retention, privacy notice, and external host logs.</td><td>Select a separate service host; test CORS/origin, payloads, retention and deletion before enabling the endpoint.</td><td>Site-wide click measurement</td></tr>
<tr><td>Q-05</td><td>May the historical price/rating data and any future product content be used this way?</td><td>Prior records show listing snapshots dated {VERIFIED}; this integration did not refresh them.</td><td>Current listing values, eligible data-source/API prerequisites, and current program terms.</td><td>Re-read official listing and current Associates/API terms; record each source/date and leave unconfirmed values blank.</td><td>Keeping or refreshing time-sensitive product facts</td></tr>
<tr><td>Q-06</td><td>What commissions and orders are actually reported?</td><td>No authorized performance report is in the repository; campaign ledger is empty.</td><td>Category rates, eligible sessions, clicks, reported orders, and attribution window.</td><td>Use authorized first-party Associates reports only; add date, report/source, channel, metrics, and provenance.</td><td>Revenue analysis and optimization</td></tr>
<tr><td>Q-07</td><td>Are these topics being searched for by the target audience?</td><td>Current guide titles are working hypotheses based on buyer questions, not demand evidence.</td><td>Real query, audience, and intent data.</td><td>Use Search Console query reports after verification; keep an editorial log that distinguishes observation from hypothesis.</td><td>Which guide to write next</td></tr>
<tr><td>Q-08</td><td>What would make a useful original product photo or hands-on review?</td><td>No product photography or hands-on test is claimed here.</td><td>Rights, budget, unit provenance, test protocol, and reviewer capacity.</td><td>Use original photos with rights records; write a reproducible protocol and disclose sample source before testing.</td><td>Photo and first-hand review work</td></tr>
<tr><td>Q-09</td><td>Should readers be able to subscribe for new guides?</td><td>No email addresses are collected.</td><td>Provider, consent text, unsubscribe, retention, deletion, privacy notice, and cost.</td><td>Compare providers and complete a privacy/consent review before adding any form.</td><td>Reader capture</td></tr>
<tr><td>Q-10</td><td>Can the proposed weekly cadence be sustained?</td><td>A four-week pilot and monthly query review are proposed, not yet a commitment.</td><td>Editorial hours, fact-checking capacity, and ongoing report access.</td><td>Track actual publication dates and review capacity at the end of the pilot.</td><td>Long-term publishing schedule</td></tr>
</table></div>
<p class="small">Working-title examples: “Basket or oven-style air fryer: what should you compare?”, “A no-hype checklist for comparing air fryer capacity”, “How to assess cleanup and counter-space trade-offs”, and “Questions to ask before buying a multi-function kitchen appliance.” These are not popularity or search-volume claims. Additional buyer-question hypotheses can be reviewed here after source and intent checks.</p>
"""
open("suggestions.html","w").write(page("Suggestions & Decision Log: Ideas, Evidence Gaps, and Next Steps | The Countertop Guide","A decision desk with recommendations, local reviewer choices, known answers, missing information, discovery paths, and implementation gates for The Countertop Guide.",sugg_body))
open("suggestions.html","w").write(page("Suggestions Board & Decision Log: Review Before Building | The Countertop Guide","Suggestions board and Q/I/A decision log for The Countertop Guide: what to build next, what evidence each needs, and which decisions are blocked until answers arrive.",sugg_body))
# ---------- VERIFICATION ----------
ver_rows = ""
for pid in ["P1","P2","P3","P4","P5"]:
    p = PRODS[pid]
    intent = p["productIntent"]
    listing = esc(p["observedListingUrl"])
    observed_asin = esc(p["observedAsin"])
    listing_link = f'<a href="{listing}">Observed Amazon listing</a>'
    intent_unknown = '<span class="badge-flag">Unverified - see FLG-013</span>'
    dims_cell = esc(p["dimensions"]) if p["dimensions"] else '<span class="badge-flag">Not captured - see FLG-004</span>'
    ver_rows += f"""
<article class="card" id="{pid}">
<h3>{pid} · {esc(p['shortName'])} <span class="meta">(observed listing ASIN {observed_asin})</span></h3>
<div class="table-scroll"><table>
<tr><th>Field</th><th>Value</th><th>Source / status</th></tr>
<tr><td>Submitted short link</td><td>{esc(p['submittedShortLink'])}</td><td>Supplied in project brief</td></tr>
<tr><td>Intended ASIN</td><td>{esc(intent['intendedAsin'])}</td><td>{intent_unknown} Confirmation is not in the repository.</td></tr>
<tr><td>Official listing URL for intended product</td><td>{esc(intent['officialListingUrl'])}</td><td>{intent_unknown}</td></tr>
<tr><td>Intent confirmation date</td><td>{esc(intent['confirmationDate'])}</td><td>{intent_unknown}</td></tr>
<tr><td>Intent confirmation source</td><td>{esc(intent['source'])}</td><td>{intent_unknown}</td></tr>
<tr><td>Observed redirect target (separate from intent)</td><td><a href="{esc(p['observedRedirectUrl'])}">{esc(p['observedRedirectUrl'])}</a></td><td>Historical observation {esc(p['observedRedirectDate'])}; not re-followed in this integration.</td></tr>
<tr><td>Observed ASIN</td><td>{observed_asin}</td><td>{listing_link}</td></tr>
<tr><td>Observed listing title</td><td>{esc(p['title'])}</td><td>{listing_link}</td></tr>
<tr><td>Rating / count snapshot</td><td>{esc(p['rating'])} ({esc(p['ratingCount'])}) · {VERIFIED}</td><td>{listing_link}</td></tr>
<tr><td>Price snapshot (new / list)</td><td>{esc(p['priceNew'])} / {esc(p['priceList'])} · {VERIFIED}</td><td>{listing_link}</td></tr>
<tr><td>Dimensions</td><td>{dims_cell}</td><td>{listing_link}</td></tr>
<tr><td>Capacity (title / field)</td><td>{esc(p['capacityTitle'])} / {esc(p['capacityField'])}</td><td>{listing_link}</td></tr>
<tr><td>Special features</td><td>{esc(p['specialFeatures'])}</td><td>{listing_link}</td></tr>
<tr><td>Candidate tagged URL used on the publication</td><td><a href="{esc(aff(p))}">Open observed listing with tag {TAG}</a></td><td><span class="badge-flag">Associates Central destination/report test not recorded (FLG-001)</span></td></tr>
</table></div>
<p class="small">{esc(p['sourceNote'])} These are historical listing snapshots, not a fresh verification from this integration. Intended-product fields remain blank until confirmed independently.</p>
</article>"""
ver_body = f"""
<p class="eyebrow">Verification register</p>
<h1>Source register and product-intent record</h1>
<p class="lede">The intended item and the observed redirect are different records. Intended ASIN, official intended listing URL, confirmation date, and confirmation source are blank until confirmed; the observed destination is shown separately. Product listing facts below refer only to the historical observed destination.</p>
<p class="shop-note">For each submitted link, run the Associates workflow, confirm the product identity, then test one tagged Special Link and check its tracking report before scaling. The submitted short links are not described as invalid; their exact Special Link status is unresolved.</p>
{ver_rows}
<h2>Official policy references</h2>
<div class="table-scroll"><table>
<tr><th>Reference</th><th>Why it is listed</th><th>Source</th></tr>
<tr><td>Amazon Associates Operating Agreement</td><td>Special Links, disclosure, and Program Content requirements; re-check the current terms before publishing.</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Amazon Associates</a></td></tr>
<tr><td>Amazon Associates Program Policies</td><td>Program and link requirements; re-check the current policy and any API prerequisites.</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Amazon Associates</a></td></tr>
<tr><td>FTC Disclosures 101</td><td>Disclosure review reference; the site's specific legal obligations need review.</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC</a></td></tr>
<tr><td>FTC Endorsements, Influencers &amp; Reviews</td><td>Endorsement-context review reference.</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC</a></td></tr>
</table></div>
<p class="small">Historical listing capture date: {VERIFIED}. This integration did not fetch Amazon or policy pages, and the Associates Central Special Link test remains uncompleted in the record. See <a href="flagged.html">Flagged for review</a> before treating a candidate as confirmed.</p>
"""
open("verification.html","w").write(page("Product Intent & Source Register | The Countertop Guide","Separate intended products from historical observed redirect destinations. Review the five submitted links, blank confirmation records, source snapshots, and the untested affiliate-link gate.",ver_body))
# ---------- FLAGGED ----------
flag_body = f"""
<p class="eyebrow">Flagged for review</p>
<h1>Flagged for review - irregularities &amp; unverified items</h1>
<p class="lede">These are open evidence and account-access gaps, not findings that a link or product is invalid. Historical notes remain labeled as historical; unresolved fields are blank until an official source or authorized report is available.</p>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Item</th><th>Detail</th><th>Action</th><th>Source / record</th></tr>
<tr><td>FLG-001</td><td>Special Link destination/report not tested</td><td>Prior repository notes record observed short-link destinations. Their exact Special Link compliance status is unresolved; we do not claim the supplied links are invalid. Candidate tagged listing URLs have not been confirmed in Associates Central.</td><td>Confirm intent, test one per item, and save dated tracking-report evidence (SG-01).</td></tr>
<tr><td>FLG-002</td><td>Preset &amp; capacity discrepancies</td><td>Emeril: title 24 presets vs bullets 25; title 26QT vs field 24.6 liters. Chefman 6QT: title 6 Quart vs field 6 liters. Both values shown; no silent conversion.</td><td>Verify on listing; ask seller if needed</td></tr>
<tr><td>FLG-003</td><td>Alternative variants need a fresh review</td><td>Prior repository notes mention alternative models/variants. Their current identity, availability, and listing fields have not been rechecked in this integration; no alternative price or rating is presented here.</td><td>Compare current official listings only after intended products are confirmed (SG-08).</td></tr>
<tr><td>FLG-004</td><td>Missing thermometer fields</td><td>ThermoMaven and CHEF iQ dimensions were not in captured fields. ThermoMaven battery type and CHEF iQ probe-care instructions were also not captured; no values are inferred.</td><td>Check the current official listings/manuals; record each source and date.</td></tr>
<tr><td>FLG-005</td><td>Missing wattage/warranty (Emeril)</td><td>Emeril wattage and warranty not captured. Left blank.</td><td>Check listing product details</td></tr>
<tr><td>FLG-006</td><td>Price volatility</td><td>Prices are dated snapshots from {VERIFIED}; they may no longer match the listing. No fresh price check was made in this integration.</td><td>Recheck from an authorized source before updating; keep date and provenance.</td></tr>
<tr id="FLG-007"><td>FLG-007</td><td>Search Console not verified</td><td>The GitHub Pages canonical site and root sitemap are set; Search Console ownership, indexing, and query data are not confirmed.</td><td>Verify property and submit the sitemap (SG-02 / SG-29).</td></tr>
<tr id="FLG-008"><td>FLG-008</td><td>Analytics endpoint not hosted</td><td>Five-event client/server contract and local tests are in place. The deployed page endpoint is blank; only device-local counts run, not site-wide analytics.</td><td>Choose a separate HTTPS host, privacy notice, host-log policy, and retention before enabling (SG-03).</td></tr>
<tr><td>FLG-009</td><td>No product photography</td><td>No Amazon images used (IP/licence). SVG/CSS illustrations only.</td><td>Licence decision (SG-04)</td></tr>
<tr><td>FLG-010</td><td>No hands-on testing</td><td>We have not cooked with or calibrated any product. No "lived-with" claims made.</td><td>Testing programme if approved (SG-09)</td></tr>
<tr><td>FLG-011</td><td>No commission / revenue claims</td><td>Rates not published; ledger empty until authorized reports arrive.</td><td>Record only from Associates reports</td></tr>
<tr><td>FLG-012</td><td>No unsupported popularity or ranking claims</td><td>"Bought in past month" badges are listing snapshots; we do not rank products based on them.</td><td>Evidence rule: dated snapshot or no claim</td></tr>
<tr id="FLG-013"><td>FLG-013</td><td>Intended ASIN not confirmed</td><td>The short-link observations and candidate listing ASINs are recorded separately. The intended ASIN, official intended listing URL, confirmation date, and source are blank for all five items; the redirect destination does not establish intent.</td><td>Confirm each intended product independently; keep the observed target in its separate field (Q-01).</td></tr>
<tr><td>FLG-014</td><td>Identifier format not independently sourced</td><td>A prior note cited a third-party explanation of ASIN length. This integration records the identifiers already present in observed listing URLs; it does not independently state Amazon's formal format rule.</td><td>Find an official Amazon reference before asserting a format rule</td></tr>
<tr><td>FLG-015</td><td>Attribution is unconfirmed</td><td>Prior repository notes say the observed short-link targets did not show a <code>tag=</code> parameter. This is not a finding that the links are invalid. Candidate tagged URLs also lack a recorded Associates tracking-report test.</td><td>Run and record the enrolled-workflow test per confirmed product (SG-01).</td></tr>
<tr><td>FLG-016</td><td>Listing pages carry widget data for other ASINs</td><td>Listing pages include Product summary links and Customers who viewed carousels with prices and ratings for other products. These are not used as data for the five products.</td><td>Use only each product's own fields; re-check on publication</td></tr>
<tr><td>FLG-017</td><td>External register: three links vs five</td><td>The external Zone4 decision log (D-13) refers to the three supplied links; this brief supplies five. Its statuses are not carried into this site. Only the first part of that log was read.</td><td>Reconcile the external register with the five links</td></tr>
<tr><td>FLG-018</td><td>Proposed Amazon content notice (not verified)</td><td>The external Zone4 decision log proposes an Amazon content notice citing IP License section 2(k). The IP License was not read, and the notice is not yet on the pages.</td><td>Read IP License 2(k); decide under SG-04</td></tr>
<tr><td>FLG-019</td><td>Creators API prerequisites not read</td><td>The external Zone4 decision log suggests the Creators API for prices and ratings. Its prerequisites were not read, and no API data is used on this site.</td><td>Read prerequisites before any price or rating source change</td></tr>
<tr><td>FLG-020</td><td>Historical product values not refreshed in this integration</td><td>Product attributes, prices, and ratings in the repository retain their prior capture date {VERIFIED}; this integration did not re-fetch those pages. Treat them as historical snapshots, not a current verification.</td><td>Recheck each fact from the official listing or an authorized data source before refresh or reliance.</td></tr>
</table></div>
"""
flag_sources = {
    "FLG-001": '<a href="verification.html">Verification register</a>',
    "FLG-002": source_links(["P1", "P2"]),
    "FLG-003": source_links(["P3"]),
    "FLG-004": source_links(["P4", "P5"]),
    "FLG-005": source_links(["P2"]),
    "FLG-006": source_links(["P1", "P2", "P3", "P4", "P5"]),
    "FLG-007": '<a href="suggestions.html">Search Console question</a> · <a href="sitemap.xml">Root sitemap</a>',
    "FLG-008": '<a href="methodology.html">Measurement method</a>',
    "FLG-009": '<a href="compliance.html">Photography note</a>',
    "FLG-010": '<a href="methodology.html">Evidence rules</a>',
    "FLG-011": '<a href="methodology.html">Empty campaign ledger</a>',
    "FLG-012": source_links(["P1", "P2", "P3", "P4", "P5"]),
    "FLG-013": '<a href="verification.html">Product-intent register</a>',
    "FLG-014": '<a href="verification.html">Observed ASIN register</a>',
    "FLG-015": '<a href="verification.html">Link-status register</a>',
    "FLG-016": source_links(["P1", "P2", "P3", "P4", "P5"]),
    "FLG-017": '<span>Prior repository note; external log not re-read</span>',
    "FLG-018": '<span>Prior repository note; license not reviewed</span>',
    "FLG-019": '<span>Prior repository note; API prerequisites not reviewed</span>',
    "FLG-020": source_links(["P1", "P2", "P3", "P4", "P5"]),
}
for _flag_id, _source in flag_sources.items():
    _pattern = rf'(<tr(?: id="{_flag_id}")?><td>{_flag_id}</td>.*?</tr>)'
    flag_body, _count = re.subn(
        _pattern,
        lambda match: match.group(1).replace("</tr>", f"<td>{_source}</td></tr>", 1),
        flag_body,
        count=1,
        flags=re.S,
    )
    if _count != 1:
        raise ValueError(f"could not add source column to {_flag_id}")
open("flagged.html","w").write(page("Flagged for Review: Irregularities & Unverified Items | The Countertop Guide","Flagged irregularities for The Countertop Guide: short-link compliance, preset/capacity discrepancies, newer models, missing fields, price volatility and launch gates.",flag_body))
# ---------- COMPLIANCE ----------
comp_body = f"""
<p class="eyebrow">Compliance gate</p>
<h1>Disclosures &amp; policy checks in the publishing workflow</h1>
<p class="lede">The Associates statement is immediately below the masthead on every page and repeated in the footer. Every Amazon-bound product link carries <code>rel="sponsored"</code>. This is a publishing control, not a compliance certification.</p>
<h2>Disclosure displayed on every page</h2>
<blockquote>As an Amazon Associate I earn from qualifying purchases.</blockquote>
<p>Price snapshots can change; check the live listing before buying. Source links below are provided for review; current policy text was not re-fetched during this integration.</p>
<h2>Outbound link controls</h2>
<ul>
<li>The site contains candidate Amazon listing URLs with tracking ID <code>{TAG}</code>; they are explicitly marked sponsored and identify the retailer.</li>
<li>The candidate URLs are not described as validated Special Links. The Associates Central destination and tracking-report test remains open for each intended product.</li>
<li>The supplied short links remain in the register as submitted links. Their observed destinations are kept separate from the blank intended-product fields; their exact compliance status is unresolved.</li>
</ul>
<h2>Publishing checklist and official sources</h2>
<div class="table-scroll"><table>
<tr><th>Check</th><th>Source</th><th>Our practice</th></tr>
<tr><td>Use proper tagged Special Link formats</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement S1</a></td><td>Official URL + tag; manual SiteStripe test is a gate (FLG-001)</td></tr>
<tr><td>Do not obscure link destination</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td><td>Button text + ASIN + "Opens amazon.com" on every card</td></tr>
<tr><td>Disclose material connection, hard to miss</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td><td>Strip under masthead on every page + footer; simple language ("earns from qualifying purchases")</td></tr>
<tr><td>Endorsement honesty; no unsubstantiated claims</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td><td>No performance or popularity claims without evidence; seller claims attributed ("per listing")</td></tr>
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
<li>Popularity or ranking claims require a dated, relevant source. We make none.</li>
<li>Seller claims are attributed ("per listing"). Derived math shows its method. Prices always carry a snapshot date.</li>
<li>Hands-on testing claims require a published protocol and photos. We make none.</li>
</ul>
<h2>Analytics: five defined events</h2>
<div class="table-scroll"><table>
<tr><th>Event</th><th>When it fires</th><th>Payload / aggregate retained</th></tr>
<tr><td>page_view</td><td>Page load</td><td>Path only; daily count</td></tr>
<tr><td>outbound_click</td><td>Sponsored Amazon click</td><td>Path + observed product ASIN; daily count by path and ASIN</td></tr>
<tr><td>search</td><td>Site search submitted</td><td>Path only; no query text</td></tr>
<tr><td>chooser_complete</td><td>3-question chooser finished</td><td>Path only; no selected answers</td></tr>
<tr><td>guide_read</td><td>Guide scrolled 75%</td><td>Path only; daily count</td></tr>
</table></div>
<p>The event payload excludes search terms, full outbound URLs, chooser answers, referrers, cookies, user agents, and client timestamps. The browser keeps device-local daily counts for up to 30 days; the self-hosted endpoint, when deployed, keeps aggregate daily counts for 90 days and does not log request details. Hosting-provider logging remains a hosting decision.</p>
<p>Implementation: <code>assets/app.js</code> and <code>analytics-endpoint/server.py</code> share the same five-event contract. The endpoint URL is blank in the published pages, so only device-local counters run today; no site-wide click totals are collected. GitHub Pages is static and cannot run this Python service. The host decision and deployment status are recorded under <a href="flagged.html#FLG-008">FLG-008</a>. Affiliate orders/conversions are not browser events; use only authorized Associates reports.</p>
<h2>Campaign ledger (empty by design)</h2>
<div class="table-scroll"><table>
<tr><th>Date</th><th>Source</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th><th>Reported orders</th><th>Provenance</th></tr>
<tr><td colspan="7"><em>No rows yet. Add timestamp, source, channel, eligible sessions, clicks and reported orders only when obtained from authorized first-party reports (Associates Central). No conversion score or revenue forecast is presented.</em></td></tr>
</table></div>
<h2>Publishing cadence</h2>
<p>Editorial pilot: one sourced, question-led guide per week for four weeks, then a monthly topic review. This is a proposed operating cadence, not a claim that future articles are already commissioned. Until Search Console is verified and query data is available, article titles remain buyer-question hypotheses, not search-volume claims. Add each published guide to <code>data/guides.json</code>; the build generates the root sitemap and RSS feed from that manifest. RSS: <a href="feed.xml">feed.xml</a>. Sitemap: <a href="sitemap.xml">sitemap.xml</a>.</p>
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
 {"title":"Air fryers category","url":"air-fryers.html","text":"Compare three historical air fryer listing profiles: dual basket, French-door oven, and single basket. Capacity labels, dimensions, footprint, cleanup claims, and dated prices."},
 {"title":"Meat thermometers category","url":"thermometers.html","text":"Compare historical instant-read and wireless thermometer listing claims, probe count, sensor details, connectivity, and missing dimensions."},
 {"title":"Compare five candidate listings","url":"compare.html","text":"Source-linked comparison of five historical candidate listings, with recorded dimensions, prices, ratings, a three-question spec-based shortlist, and calculated footprint."},
 {"title":"Basket or oven-style air fryer: what should you compare?","url":"guide-basket-vs-oven.html","text":"Compare air fryer layouts, listing capacity wording, exterior dimensions, food examples, cleaning questions, and unknown hands-on performance."},
 {"title":"A no-hype checklist for comparing air fryer capacity","url":"guide-capacity-checklist.html","text":"Separate title capacity from product fields, split baskets, seller serving examples, outside dimensions, and missing details."},
 {"title":"How to assess cleanup and counter-space trade-offs","url":"guide-cleanup-counter-space.html","text":"Measure width and depth, compare calculated footprints, check listed dishwasher-care claims, and consult the current manual."},
 {"title":"Questions to ask before buying a multi-function kitchen appliance","url":"guide-multifunction-questions.html","text":"A checklist for presets, accessories, fit, electrical details, and information that was not captured from the product listing."},
 {"title":"Instant-read or wireless? How to read accuracy claims","url":"guide-thermometer-accuracy.html","text":"Compare listing claims about thermometer accuracy, reading speed, sensor counts, connectivity, and what remains untested."},
 {"title":"Executive summary","url":"executive-summary.html","text":"Publication overview, historical candidate listings, product-intent fields awaiting confirmation, account-dependent launch gates, and measurement limits."},
 {"title":"Suggestions board and decision log","url":"suggestions.html","text":"Reviewable editorial suggestions, local-only approve/defer/reject choices, knowns, unknowns, evidence gaps, and ways to discover missing information."},
 {"title":"Verification register","url":"verification.html","text":"Separate intended products from historical observed redirect destinations; see listing sources, blank confirmations, and the unresolved Special Link test."},
 {"title":"Flagged for review","url":"flagged.html","text":"Open product-record discrepancies, missing fields, unconfirmed intent, historical price data, account gates, and the unhosted analytics endpoint."},
 {"title":"Compliance","url":"compliance.html","text":"Disclosure placement, sponsored-link marking, candidate tracking status, and links to Amazon Associates and FTC review material."},
 {"title":"Method and campaign ledger","url":"methodology.html","text":"Evidence rules, five event names and payload limits, local and endpoint retention, an empty campaign ledger, and the proposed editorial cadence."},
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
