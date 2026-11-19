import json, html
D = json.load(open("data/products.json"))
SITE = D["site"]
PRODS = {p["id"]: p for p in D["products"]}
VERIFIED = SITE["verifiedDate"]
TAG = SITE["trackingId"]
SITE_URL = "https://wingbangboozle1-lang.github.io/Prod1/"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

def esc(s): return html.escape(str(s), quote=True)
def aff(p): return f"https://www.amazon.com/dp/{p['asin']}?tag={TAG}"
def canon(fname): return SITE_URL if fname == "index.html" else SITE_URL + fname

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

def story_card(href, kicker, section, title, deck, read, img, art):
    return f"""
<a class="story-card" href="{href}">
  <div class="story-image {img}"><span class="image-tag">{esc(kicker)}</span>{art}</div>
  <div class="card-meta"><span>{esc(section)}</span><span>GUIDE</span></div>
  <h3>{esc(title)}</h3>
  <p>{esc(deck)}</p>
  <span class="read-link">{esc(read)}</span>
</a>"""

NAV = """<nav class="nav" aria-label="Main">
  <a href="index.html">Home</a>
  <a href="air-fryers.html">Air Fryers</a>
  <a href="thermometers.html">Thermometers</a>
  <a href="compare.html">Compare</a>
  <a href="guides.html">Guides</a>
  <a href="topics.html">Topics</a>
  <a href="suggestions.html">Suggestions</a>
</nav>
<form class="searchbox" id="site-search-form" role="search">
  <label class="skip" for="site-search-input">Search the site</label>
  <input id="site-search-input" type="search" placeholder="Search guides &amp; products" aria-label="Search the site">
  <button class="btn small" type="submit">Search</button>
</form>"""

FOOTER = f"""
<footer>
  <div class="wrap">
  <div class="footer-top">
    <a class="brand brand-footer" href="index.html"><span class="brand-mark">T<span>G</span></span><span>The Countertop <b>Guide</b><small>KITCHEN BUYER&apos;S DESK</small></span></a>
    <div class="footer-links">
      <div><b>SHOP</b><a href="air-fryers.html">Air Fryers</a><a href="thermometers.html">Thermometers</a><a href="compare.html">Compare all five</a></div>
      <div><b>READ</b><a href="guides.html">All guides</a><a href="topics.html">Topic calendar</a><a href="feed.xml">RSS feed</a></div>
      <div><b>TRUST &amp; DATA</b><a href="verification.html">Verification register</a><a href="flagged.html">Flagged for review</a><a href="compliance.html">Compliance</a><a href="methodology.html">Method &amp; campaign ledger</a><a href="executive-summary.html">Executive summary</a><a href="design-brief.html">Design brief</a><a href="suggestions.html">Suggestions board</a><a href="docs/products.html">Product-intent register</a></div>
    </div>
  </div>
  <div class="footer-disclosure">{DISCLOSURE} Prices are snapshots from {VERIFIED} and change - always confirm on Amazon. <a href="compliance.html">How we disclose</a></div>
  <div class="footer-bottom"><span>&copy; 2026 The Countertop Guide - spec-backed comparisons from Amazon listings. We do not claim hands-on testing we have not done.</span><span>Some links are sponsored; they may earn a commission at no extra cost to you.</span></div>
  </div>
</footer>"""

def page(fname, title, desc, body, extra_head="", body_class=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon(fname)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon(fname)}">
<meta property="og:image" content="assets/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="styles.css">
<link rel="alternate" type="application/rss+xml" title="The Countertop Guide feed" href="feed.xml">
{extra_head}
</head>
<body data-verified-date="{VERIFIED}" data-analytics-endpoint="" class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead wrap">
<a class="brand" href="index.html"><span class="brand-mark">T<span>G</span></span><span>The Countertop <b>Guide</b><small>KITCHEN BUYER&apos;S DESK</small></span></a>
{NAV}
</header>
<div class="disclosure" role="note">{DISCLOSURE} Prices are snapshots from {VERIFIED} - check Amazon for the live price. <a href="compliance.html">Learn more</a></div>
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

# ---------- shared blocks ----------
HERO_ART = """<div class="hero-art">
<div class="sun"></div><div class="shelf"></div>
<div class="plant"><i></i><i></i><i></i><b></b></div>
<div class="counter"></div>
<div class="appliance">
  <div class="appliance-top"></div>
  <div class="appliance-window"><span></span></div>
  <div class="knob"></div>
  <div class="appliance-foot"></div>
</div>
<div class="art-caption">SPEC-BACKED &middot; SOURCED &middot; NO FAKE TESTING</div>
</div>"""

TICK_ITEM = f"<span>VERIFIED {VERIFIED}</span><span>SOURCED FROM AMAZON LISTINGS</span><span>NO FAKE TESTING</span><span>SPONSORED LINKS LABELED</span><span>EVERY NUMBER HAS A SOURCE</span>"
TICKER = '<div class="ticker"><div>' + TICK_ITEM * 5 + '</div></div>'

CHOOSER = """
<form id="chooser-form" class="chooser">
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

# Topic calendar (shared by the front page band and topics.html)
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
     "status": "Planned", "href": "topics.html#t06",
     "angle": "A tape-measure walkthrough: depth, width, footprint and the capacity you get per centimetre of counter - using only listed dimensions.",
     "hooks": "Listed dimensions (P2: 16.9D x 15.8W x 14.8H in); derived footprint and capacity-per-cm math",
     "sources": [("P2 listing", PRODS["P2"]["sourceUrl"]), ("Counter-space math", "compare.html")]},
    {"n": "07", "title": "Two baskets or one: what dual-zone cooking actually changes", "cat": "Air fryers - Form",
     "status": "Planned", "href": "topics.html#t07",
     "angle": "When two independent baskets earn their extra depth - and when a single large basket is the simpler buy.",
     "hooks": "P1 dual-basket listing claims (Sync Finish, 2 x 3 Qt); P3 single-basket listing claims",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"])]},
    {"n": "08", "title": "How to read the badges on a listing - without overreading them", "cat": "Trust",
     "status": "Planned", "href": "topics.html#t08",
     "angle": "What an 'Amazon's Choice' badge and a rating snapshot can and cannot tell a buyer, with the snapshot date kept visible.",
     "hooks": "Badge and rating fields as shown on listings (P1, P3, P4); dated-snapshot rule",
     "sources": [("P1 listing", PRODS["P1"]["sourceUrl"]), ("P3 listing", PRODS["P3"]["sourceUrl"]), ("P4 listing", PRODS["P4"]["sourceUrl"])]},
]

def topic_band():
    rows = "".join(
        f'<a href="{t["href"]}"><span>{t["n"]}</span>{esc(t["title"])}<b class="{"status-published" if t["status"]=="Published" else "status-planned"}">{t["status"]}</b></a>'
        for t in TOPICS)
    return f"""
<div class="topic-band">
  <div class="wrap topic-inner">
    <div>
      <h2>The topic calendar</h2>
      <p>Eight question-shaped topics, five published and three queued. Every queued title is an editorial hypothesis backed by verified listing fields - not a claim about search volume or popularity. The next topic is chosen from measured queries, not instinct.</p>
      <p><a class="btn secondary" href="topics.html">Open the full calendar</a></p>
    </div>
    <div class="topic-list">{rows}</div>
  </div>
</div>"""

# ---------- INDEX ----------
index_stories = "".join([
    story_card("guide-basket-vs-oven.html", "Form", "Latest stories", "Basket or oven-style air fryer: what should you compare?",
               "Dual-basket vs French-door oven vs single basket: two-dish cooking, crowd capacity and counter depth.", "Read the guide", "image-one", '<span class="shape shape-a"></span>'),
    story_card("guide-capacity-checklist.html", "Capacity", "Latest stories", "A no-hype checklist for comparing air fryer capacity",
               "Quarts vs litres, single vs dual baskets, and the 'feeds 4-6' claim - how to read it without being misled.", "Read the guide", "image-two", '<span class="plate"></span>'),
    story_card("guide-cleanup-counter-space.html", "Space", "Latest stories", "How to assess cleanup and counter-space trade-offs",
               "Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.", "Read the guide", "image-three", '<span class="spark">&#10022;</span>'),
    story_card("guide-multifunction-questions.html", "Multi-function", "Latest stories", "Questions to ask before buying a multi-function kitchen appliance",
               "Presets, accessories, wattage and warranty - the pre-purchase checklist, applied to the Emeril oven.", "Read the guide", "image-one", '<span class="shape shape-b"></span>'),
    story_card("guide-thermometer-accuracy.html", "Thermometers", "Latest stories", "Instant-read or wireless? How to read accuracy claims",
               "Plus-minus 0.5F, NIST/NSF, sensor counts and WiFi range - what each claim does and does not prove.", "Read the guide", "image-two", '<span class="plate"></span>'),
])

index_body = f"""
<section class="hero">
<p class="eyebrow">The Countertop Guide &middot; compared from the listing</p>
<h1>Basket or oven-style air fryer: what should you compare?</h1>
<p class="hero-text">Five real products, two categories, zero hype. We compare capacity, counter footprint, cleanup and price <em>exactly as listed on Amazon</em> - and we show the source for every number. No fake "we tested it" claims. No popularity claims without a dated snapshot.</p>
<p><a class="btn" href="compare.html">Compare all five</a> <a class="btn secondary" href="guides.html">Read the guides</a></p>
<p class="small"><span class="badge-ok">Verified {VERIFIED}</span> <span class="badge-ok">Sponsored links labeled</span> <span class="badge-warn">Prices are snapshots - check Amazon</span></p>
{HERO_ART}
</section>
{TICKER}
<section class="section">
  <div class="section-head">
    <div><p class="eyebrow">The desk</p><h2>Latest stories</h2></div>
    <p>Question-shaped guides, answered from verified listings. Each one says plainly what the listing does not tell you.</p>
  </div>
  <div class="cards">{index_stories}</div>
  <p><a href="guides.html">All guides</a> &middot; <a href="topics.html">The topic calendar</a></p>
</section>
{topic_band()}
<section class="section">
  <div class="section-head">
    <div><p class="eyebrow">The shop</p><h2>The five verified picks</h2></div>
    <p>Every fact below links to its Amazon listing. Missing values are blank and flagged - never inferred.</p>
  </div>
  <div class="cards">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
  <div class="cards" style="margin-top:1.1rem">{product_card('P4')}{product_card('P5')}</div>
</section>
<section class="section">
  <div class="section-head">
    <div><p class="eyebrow">Not sure</p><h2>Answer three questions, get a shortlist</h2></div>
    <p>The chooser uses only verified specs (form, depth, price snapshot). It does not replace reading the listing - but it gets you to a shortlist in 20 seconds.</p>
  </div>
{CHOOSER}
</section>
<div class="newsletter">
  <div class="wrap newsletter-inner">
    <div>
      <p class="eyebrow">New guides, in your feed</p>
      <h2>Follow the topic calendar via RSS</h2>
      <p>Each new guide is added to the feed and the sitemap at publish. No email capture yet - email signup is proposed on the decision desk (SG-07) and stays off until a provider, consent copy and FTC review are approved.</p>
    </div>
    <a class="button-light" href="feed.xml"><span>&#9654;</span> Subscribe via RSS</a>
  </div>
</div>
"""
open("index.html","w").write(page("index.html","Air Fryers & Thermometers Compared From the Listing | The Countertop Guide","Compare 3 air fryers and 2 thermometers from verified Amazon listings: capacity, footprint, cleanup and price snapshots. No fake testing, sponsored links labeled.",index_body,
    jsonld({"@context":"https://schema.org","@type":"WebSite","name":"The Countertop Guide","url":SITE_URL})))

# ---------- AIR FRYERS ----------
af_body = f"""
<section class="doc-hero">
<p class="eyebrow">Category &middot; Air Fryers</p>
<h1>Air fryers: dual-basket, oven-style &amp; single-basket</h1>
<p>Three verified fryers, three different jobs. The dual-basket cooks two dishes at once; the French-door oven is built for crowds and rotisserie; the single basket is the compact weeknight workhorse. Start with form, then capacity, then footprint.</p>
</section>
<article class="doc-main">
<div class="cards" style="grid-template-columns:repeat(3,1fr)">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
<h2>Air fryer comparison (verified fields only)</h2>
<div class="table-wrap"><table class="data-table">
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
</article>
"""
open("air-fryers.html","w").write(page("air-fryers.html","Air Fryers Compared: Dual-Basket, Oven-Style & Single-Basket | The Countertop Guide","Compare Chefman 6QT dual-basket, Emeril 26QT French-door oven and Chefman 8QT TurboFry from verified Amazon listings: capacity, footprint, cleanup, price snapshots.",af_body))

# ---------- THERMOMETERS ----------
th_body = f"""
<section class="doc-hero">
<p class="eyebrow">Category &middot; Thermometers</p>
<h1>Thermometers: instant-read vs wireless</h1>
<p>Two different tools for the same job - knowing when meat is done. The instant-read gives a 1-second answer in your hand. The wireless system watches three probes from your phone. Accuracy claims below are quoted from the listing with the certification named; we have not independently calibrated either unit.</p>
</section>
<article class="doc-main">
<div class="cards" style="grid-template-columns:repeat(2,1fr)">{product_card('P4')}{product_card('P5')}</div>
<h2>Thermometer comparison (verified fields only)</h2>
<div class="table-wrap"><table class="data-table">
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
</article>
"""
open("thermometers.html","w").write(page("thermometers.html","Meat Thermometers Compared: Instant-Read vs Wireless | The Countertop Guide","ThermoMaven 1-second instant-read vs CHEF iQ Sense wireless 3-probe system, compared from verified Amazon listings: accuracy claims, range, probes and price snapshots.",th_body))

# ---------- COMPARE ----------
compare_body = f"""
<section class="doc-hero">
<p class="eyebrow">Comparison</p>
<h1>All five products, side by side</h1>
<p>Every cell is either quoted from the Amazon listing (with link) or marked missing. Derived rows (footprint, capacity per square inch) show their method. Prices are {VERIFIED} snapshots - the live price on Amazon is the only price that matters.</p>
</section>
<article class="doc-main">
<h2>Three-question chooser</h2>
{CHOOSER}
<h2>Full table</h2>
<div class="table-wrap"><table class="data-table">
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
<div class="table-wrap"><table class="data-table">
<tr><th>Air fryer</th><th>Depth</th><th>Footprint</th><th>Capacity</th><th>Capacity per cm depth*</th><th>Capacity per sq in*</th></tr>
<tr><td>Chefman 6QT Dual (B0CDY277D3)</td><td>34.0 cm</td><td>158.0 sq in</td><td>6 qt</td><td>0.18 qt/cm</td><td>0.038 qt/sq in</td></tr>
<tr><td>Emeril 26QT Oven (B09B7SB46R)</td><td>42.9 cm</td><td>267.0 sq in</td><td>26 qt</td><td>0.61 qt/cm</td><td>0.097 qt/sq in</td></tr>
<tr><td>Chefman 8QT Basket (B08DKYBTPH)</td><td>32.4 cm</td><td>172.1 sq in</td><td>8 qt</td><td>0.25 qt/cm</td><td>0.046 qt/sq in</td></tr>
</table></div>
<p class="small">* Derived by us: depth in cm = inches x 2.54; footprint = width x depth; ratios use title capacity. Thermometers excluded (dimensions not captured). Method and limits in <a href="guide-cleanup-counter-space.html">cleanup &amp; counter-space guide</a>.</p>
<div class="sticky-bar" id="sticky-bar">
  <span>Compare all five &middot; prices are {VERIFIED} snapshots &middot; sponsored links labeled</span>
  <a href="#full-table">Back to the table</a>
</div>
</article>
"""
open("compare.html","w").write(page("compare.html","Compare 5 Air Fryers & Thermometers Side by Side | The Countertop Guide","Side-by-side comparison of 5 verified products: capacity, dimensions, footprint, ratings and price snapshots, plus a 3-question chooser and counter-space math.",compare_body))

# ---------- GUIDES INDEX ----------
guides_stories = "".join([
    story_card("guide-basket-vs-oven.html", "Form", "Guides", "Basket or oven-style air fryer: what should you compare?",
               "Dual-basket vs French-door oven vs single basket: cooking two dishes, crowd capacity, and counter depth.", "Read guide", "image-one", '<span class="shape shape-a"></span>'),
    story_card("guide-capacity-checklist.html", "Capacity", "Guides", "A no-hype checklist for comparing air fryer capacity",
               "Quarts vs litres, single vs dual baskets, and the 'feeds 4-6' claim - how to read capacity without being misled.", "Read guide", "image-two", '<span class="plate"></span>'),
    story_card("guide-cleanup-counter-space.html", "Space", "Guides", "How to assess cleanup and counter-space trade-offs",
               "Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.", "Read guide", "image-three", '<span class="spark">&#10022;</span>'),
    story_card("guide-multifunction-questions.html", "Multi-function", "Guides", "Questions to ask before buying a multi-function kitchen appliance",
               "Presets, accessories, wattage and warranty - the pre-purchase checklist, applied to the Emeril oven.", "Read guide", "image-one", '<span class="shape shape-b"></span>'),
    story_card("guide-thermometer-accuracy.html", "Accuracy", "Guides", "Instant-read or wireless? How to read accuracy claims",
               "Plus-minus 0.5F, NIST/NSF, sensor counts and range - what each claim does and does not prove.", "Read guide", "image-two", '<span class="plate"></span>'),
    story_card("topics.html", "Calendar", "Guides", "The topic calendar: what we publish next",
               "Eight spec-backed working titles, five published and three queued - with the fields each one is built from.", "Open calendar", "image-three", '<span class="shape shape-a"></span>'),
])
guides_body = f"""
<section class="doc-hero">
<p class="eyebrow">Guides</p>
<h1>Question-shaped guides, answered from the listing</h1>
<p>Each guide starts from a question a buyer actually types, then answers it with verified listing facts - and says plainly what the listing does not tell us. No popularity claims without a dated snapshot.</p>
</section>
<article class="doc-main">
<div class="cards">{guides_stories}</div>
<p class="small">New guides join the <a href="feed.xml">RSS feed</a> and the <a href="sitemap.xml">sitemap</a> at publish. Topics are chosen from measured queries after launch (SG-02), not instinct.</p>
</article>
"""
open("guides.html","w").write(page("guides.html","Buyer Guides: Air Fryers & Thermometers | The Countertop Guide","Question-shaped buying guides answered from verified Amazon listings: basket vs oven, capacity, cleanup and counter space, multi-function checklists, thermometer accuracy.",guides_body))

# ---------- TOPICS (topic calendar) ----------
topic_rows = ""
for t in TOPICS:
    src = " &middot; ".join(f'<a href="{u}">{esc(l)}</a>' for l, u in t["sources"])
    status = f'<span class="status-published">{t["status"]}</span>' if t["status"] == "Published" else f'<span class="status-planned">{t["status"]} - editorial hypothesis</span>'
    title_cell = f'<a href="{t["href"]}">{esc(t["title"])}</a>' if t["status"] == "Published" else esc(t["title"])
    topic_rows += f"""
<tr id="t{t['n'].replace('0','')}"><td>{t['n']}</td><td>{title_cell}</td><td>{esc(t['cat'])}</td><td>{status}</td><td>{esc(t['angle'])}</td><td>{esc(t['hooks'])}</td><td>{src}</td></tr>"""

topics_body = f"""
<section class="doc-hero">
<p class="eyebrow">The desk &middot; Topic calendar</p>
<h1>The topic calendar: eight questions, eight spec-backed answers</h1>
<p>Five guides are published; three are queued as working titles. Every title is an editorial hypothesis backed by verified listing fields - not a claim about search volume, popularity or product superiority. The next topic is chosen from measured queries, not instinct.</p>
</section>
<article class="doc-main">
<div class="callout"><b>How this calendar works</b>
<p>Each topic states the buyer question it answers, the verified fields it will be built from, and its sources. Queued titles publish only after their fields are verified against the listing and the guide is added to the <a href="sitemap.xml">sitemap</a> and <a href="feed.xml">feed</a>. Working titles may change at edit stage.</p></div>
<h2>The calendar</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>#</th><th>Working title</th><th>Category</th><th>Status</th><th>What it answers</th><th>Verified fields it uses</th><th>Sources</th></tr>
{topic_rows}
</table></div>
<h2>Publishing cadence</h2>
<p>One thoroughly checked guide per publishing slot, with a reassessment after the first batch of measured data. This is an operational plan, not a traffic promise. Every new guide is added to <a href="sitemap.xml">sitemap.xml</a> and <a href="feed.xml">feed.xml</a> at publish time.</p>
<p class="small">No topic here is a claim that the subject is popular or in demand. If a popularity claim is ever made, it carries a dated snapshot from an official source (see <a href="methodology.html">Method</a>).</p>
</article>
"""
open("topics.html","w").write(page("topics.html","Topic Calendar: Eight Spec-Backed Buyer Questions | The Countertop Guide","The Countertop Guide topic calendar: eight question-shaped, spec-backed article working titles - five published, three queued - with the verified fields and sources each is built from.",topics_body))

# ---------- GUIDE SHELL ----------
def guide_shell(kicker, h1, intro, sections_html, faqs, desc):
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    article_json = {"@context":"https://schema.org","@type":"Article","headline":h1,"description":desc,"datePublished":"2026-11-19","author":{"@type":"Organization","name":"The Countertop Guide editorial team"},"publisher":{"@type":"Organization","name":"The Countertop Guide"}}
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in faqs)
    body = f"""
<section class="doc-hero">
<p class="eyebrow">{esc(kicker)}</p>
<h1>{esc(h1)}</h1>
<p class="meta">By The Countertop Guide editorial team &middot; Spec-based guide (not hands-on tested) &middot; Verified data {VERIFIED} &middot; 4 min read</p>
<p class="lede">{intro}</p>
<div class="toc"><strong>On this page:</strong> <a href="#shortlist">Shortlist from verified listings</a> &middot; <a href="#compare-link">Full comparison</a> &middot; <a href="#faq">Questions</a></div>
</section>
<article class="doc-main article-body">
{sections_html}
<h2 id="shortlist">Shortlist from verified listings</h2>
<div class="cards" style="grid-template-columns:repeat(2,1fr)">{product_card('P1',2)}{product_card('P2',2)}{product_card('P3',2)}</div>
<p id="compare-link"><a class="btn secondary" href="compare.html">See the full side-by-side comparison</a></p>
<h2 id="faq">Questions</h2>
{faq_html}
<p class="small">Every product fact above comes from the Amazon listing linked on each card. If a fact is missing, we say so - see <a href="flagged.html">Flagged for review</a>. Prices are snapshots; confirm on Amazon before buying.</p>
<div class="sticky-bar" id="sticky-bar">
  <span>Spec-based guide &middot; verified {VERIFIED} &middot; no hands-on testing claimed</span>
  <a href="compare.html">Compare all five</a>
</div>
</article>
"""
    return body, jsonld(faq_json) + jsonld(article_json)

# ---------- GUIDE 1 ----------
b1, j1 = guide_shell("Guide &middot; Air fryers", "Basket or oven-style air fryer: what should you compare?",
 "If you cook two different dishes at the same time, a dual-basket wins. If you cook for a crowd or want rotisserie and a 12-inch pizza, an oven-style unit wins. Everything else is footprint and cleanup. Here is how to decide, using the three fryers on this site.",
 f"""
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
  ("Can the Chefman 6QT cook two dishes at once?","Yes, per the listing: two independent 3-quart baskets with Sync Finish so both can finish at the same time.")],
 "Dual-basket vs French-door oven vs single basket: two-dish cooking, crowd capacity, counter depth and cleanup, compared from verified Amazon listings.")
open("guide-basket-vs-oven.html","w").write(page("guide-basket-vs-oven.html","Basket or Oven-Style Air Fryer: What Should You Compare? | The Countertop Guide","Dual-basket vs French-door oven vs single basket: two-dish cooking, crowd capacity, counter depth and cleanup, compared from verified Amazon listings.",b1,j1,"guide-page"))

# ---------- GUIDE 2 ----------
b2, j2 = guide_shell("Guide &middot; Capacity", "A no-hype checklist for comparing air fryer capacity",
 "Capacity numbers are the easiest place to be misled. Quarts vs litres, single vs dual baskets, and 'feeds 4-6' all mean different things. Use this checklist on any listing - we apply it to the three fryers here.",
 f"""
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
  ("What does capacity per square inch mean?","Title capacity divided by footprint (width x depth from listing dimensions). It shows how much capacity you get per unit of counter. Derived by us; see compare page for method.")],
 "Quarts vs litres, single vs dual baskets, feeds 4-6 and pizza claims: a checklist for reading air fryer capacity honestly, applied to 3 verified listings.")
open("guide-capacity-checklist.html","w").write(page("guide-capacity-checklist.html","A No-Hype Checklist for Comparing Air Fryer Capacity | The Countertop Guide","Quarts vs litres, single vs dual baskets, feeds 4-6 and pizza claims: a checklist for reading air fryer capacity honestly, applied to 3 verified listings.",b2,j2,"guide-page"))

# ---------- GUIDE 3 ----------
b3, j3 = guide_shell("Guide &middot; Space &amp; cleanup", "How to assess cleanup and counter-space trade-offs",
 "The best air fryer is the one that fits your counter and that you will actually wash. Here is the footprint math and the cleanup facts as listed - nothing more.",
 f"""
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
  ("How is capacity per cm calculated?","Title capacity (quarts) divided by depth in centimetres (inches x 2.54). Derived by us from listing dimensions; not a manufacturer claim.")],
 "Dishwasher-safe baskets, footprint math and capacity per centimetre of counter depth for 3 verified air fryers. Measure your counter, then compare.")
open("guide-cleanup-counter-space.html","w").write(page("guide-cleanup-counter-space.html","How to Assess Cleanup and Counter-Space Trade-Offs | The Countertop Guide","Dishwasher-safe baskets, footprint math and capacity per centimetre of counter depth for 3 verified air fryers. Measure your counter, then compare.",b3,j3,"guide-page"))

# ---------- GUIDE 4 ----------
b4, j4 = guide_shell("Guide &middot; Multi-function", "Questions to ask before buying a multi-function kitchen appliance",
 "Multi-function ovens promise everything. Before you pay for presets you will never use, ask these questions. We apply them to the Emeril 26QT French-door oven.",
 f"""
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
  ("What is the Emeril wattage?","Not captured in our verification pass. See the listing's product details section before buying.")],
 "Presets, accessories, wattage, warranty and fit: the pre-purchase checklist for multi-function ovens, applied to the Emeril 26QT from its verified listing.")
open("guide-multifunction-questions.html","w").write(page("guide-multifunction-questions.html","Questions to Ask Before Buying a Multi-Function Kitchen Appliance | The Countertop Guide","Presets, accessories, wattage, warranty and fit: the pre-purchase checklist for multi-function ovens, applied to the Emeril 26QT from its verified listing.",b4,j4,"guide-page"))

# ---------- GUIDE 5 ----------
b5, j5 = guide_shell("Guide &middot; Thermometers", "Instant-read or wireless? How to read accuracy claims",
 "One tool answers in one second in your hand; the other watches from your phone. The right choice depends on how you cook - and on reading accuracy claims carefully.",
 f"""
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
  ("Do I need WiFi for the CHEF iQ?","WiFi enables unlimited-range app monitoring per the listing; Bluetooth is also listed in connectivity. You need the CHEF iQ app for remote monitoring.")],
 "Plus-minus 0.5F, NIST/NSF, sensor counts and WiFi range: how to read meat thermometer accuracy claims honestly, comparing 2 verified listings.")
open("guide-thermometer-accuracy.html","w").write(page("guide-thermometer-accuracy.html","Instant-Read or Wireless? How to Read Thermometer Accuracy Claims | The Countertop Guide","Plus-minus 0.5F, NIST/NSF, sensor counts and WiFi range: how to read meat thermometer accuracy claims honestly, comparing 2 verified listings.",b5,j5,"guide-page"))

# ---------- SEASONAL GUIDES ----------
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
<section class="doc-hero">
<p class="eyebrow">Executive summary</p>
<h1>What this site is, what is verified, and what happens next</h1>
<p>The Countertop Guide is a spec-backed affiliate publication for two kitchen categories - air fryers and meat thermometers - built from five Amazon listings verified on {VERIFIED}. It leads with products and buyer questions, not with process. Every number links to its source.</p>
</section>
<article class="doc-main">
<h2>The five products</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>ID</th><th>Product</th><th>ASIN</th><th>Category</th><th>Price snapshot</th><th>Rating snapshot</th></tr>
<tr><td>P1</td><td>Chefman 6QT Dual-Basket Air Fryer Oven</td><td>B0CDY277D3</td><td>Air Fryers</td><td>$79.93</td><td>4.2 ({PRODS['P1']['ratingCount']})</td></tr>
<tr><td>P2</td><td>Emeril Lagasse 26QT French-Door Oven</td><td>B09B7SB46R</td><td>Air Fryers</td><td>$149.99</td><td>4.3 ({PRODS['P2']['ratingCount']})</td></tr>
<tr><td>P3</td><td>Chefman 8QT TurboFry Basket</td><td>B08DKYBTPH</td><td>Air Fryers</td><td>$69.99</td><td>4.4 ({PRODS['P3']['ratingCount']})</td></tr>
<tr><td>P4</td><td>ThermoMaven 1-Second Instant-Read</td><td>B0DHZTCNR5</td><td>Thermometers</td><td>$16.99</td><td>4.6 ({PRODS['P4']['ratingCount']})</td></tr>
<tr><td>P5</td><td>CHEF iQ Sense Wireless (3 probes)</td><td>B0DZFD6R9Z</td><td>Thermometers</td><td>$119.99</td><td>4.2 ({PRODS['P5']['ratingCount']})</td></tr>
</table></div>
<h2>What is verified</h2>
<ul>
<li>Each submitted short link resolves to the ASIN and official listing URL in <a href="verification.html">verification register</a> (intended ASIN kept separate from observed redirect target). All five links re-checked 2026-11-19.</li>
<li>A full line-by-line re-read of all five Amazon.com listings on {VERIFIED}: titles, ratings, price snapshots, dimensions (air fryers), capacity, wattage, special features and bullets. Emeril wattage was captured on this pass (1700 watts per the listing's Product information table).</li>
<li>Compliance posture: disclosure above the fold on every page and in the footer (Operating Agreement Section 5 wording); every outbound product link is rel="sponsored" and labeled; no popularity claims without a dated snapshot; no hands-on testing claims.</li>
</ul>
<h2>What is not verified (and therefore not claimed)</h2>
<ul>
<li>Thermometer dimensions (not listed on their listing pages), Emeril warranty period (listing links a PDF only), and the Chefman 8QT wattage (listing bullets and spec table disagree) - blank or attributed and flagged.</li>
<li>Short-link compliance status (unresolved), Special Link test in Associates Central (manual gate), commission rates (not published here), search volume / popularity (not claimed).</li>
<li>Product photography (no Amazon images used; real photography needs a licence decision - SG-04).</li>
</ul>
<h2>How money and measurement work</h2>
<p>Outbound links use tracking ID <code>{TAG}</code> and are marked sponsored. Click and conversion measurement is defined (five events) with a privacy-preserving local counter; the self-hosted endpoint is a documented stub, not yet deployed (SG-03). The campaign ledger starts empty - orders and revenue are recorded only from authorized first-party reports. See <a href="methodology.html">Method &amp; campaign ledger</a>.</p>
<h2>What changed in this build (2026-11-19)</h2>
<ul>
<li>Front page rebuilt as a publication front page: hero, ticker, story cards, topic band, product panel, chooser and an RSS band.</li>
<li>New <a href="topics.html">topic calendar</a>: eight spec-backed working titles, five published and three queued, each with its verified fields and sources.</li>
<li><a href="suggestions.html">Suggestions page</a> rebuilt as an interactive decision desk: pick a path per suggestion, export a review sheet.</li>
<li>Generator now emits per-page canonical URLs on the live GitHub Pages address (the earlier placeholder bug is fixed - see <a href="flagged.html">FLG-007</a>).</li>
<li>Disclosure wording is now the exact Operating Agreement Section 5 sentence (see <a href="compliance.html">Compliance</a>).</li>
<li>No product values were changed in this build.</li>
</ul>
<h2>Next gates (owner decisions)</h2>
<p>Special Link validation (SG-01), canonical/Search Console (SG-02), analytics endpoint hosting (SG-03), photography licence (SG-04), the design-brief direction (SG-11), the editorial calendar (SG-12) and brand unification (SG-19). Nothing scales until those gates pass. See <a href="design-brief.html">Design brief</a>, <a href="suggestions.html">Suggestions &amp; decision log</a> and <a href="flagged.html">Flagged for review</a>.</p>
</article>
"""
open("executive-summary.html","w").write(page("executive-summary.html","Executive Summary: Products, Verification & Next Gates | The Countertop Guide","Executive summary for The Countertop Guide: 5 verified products in 2 categories, what is and is not verified, compliance posture, measurement plan and decision gates.",exec_body))

# ---------- SUGGESTIONS (decision desk) ----------
def pick_select(pid, options):
    opts = "".join(f'<option value="{esc(o)}">{esc(o)}</option>' for o in options)
    return f'<select data-pick="{pid}" aria-label="Pick a path for {esc(pid)}">{opts}</select>'

def sg_row(sid, suggestion, why, evidence, effort, options, note=""):
    return f"""
<tr><td>{sid}</td><td>{suggestion}</td><td>{why}</td><td>{evidence}</td><td>{effort}</td>
<td>{pick_select(sid, options)}<div class="pick-status small">{note or "Not picked yet"}</div></td></tr>"""

des_rows = (
 sg_row("DES-01", "Editorial typography and palette: Playfair Display + DM Sans on a warm paper background",
        "Reads like a publication, not a template; the design system already shipped in styles.css",
        "Design review by owner", "Done in this build", ["Approve", "Approve with changes", "Reject"]) +
 sg_row("DES-02", "Front page as a publication: hero art, ticker, story cards, topic band, product panel, RSS band",
        "Leads with products and stories; keeps every dashboard surface reachable from the footer",
        "Owner visual review", "Done in this build", ["Approve", "Approve with changes", "Reject"]) +
 sg_row("DES-03", "Topic calendar page with eight spec-backed working titles",
        "Gives readers and search engines a reason to return; titles are hypotheses, not demand claims",
        "Owner review of the eight titles", "Done in this build", ["Approve", "Approve with changes", "Reject"]) +
 sg_row("DES-04", "Interactive decision desk: pick a path per suggestion and export a review sheet",
        "Decisions get made deliberately, with evidence, before anything is implemented",
        "Usability check of the export", "Done in this build", ["Approve", "Approve with changes", "Reject"])
)

sg_rows = (
 sg_row("SG-01", "Validate one Special Link per product in Associates Central (SiteStripe) and confirm destination + tracking report",
        "Proves outbound links earn correctly before scaling", "Associates Central test clicks + report screenshots", "Low (manual)",
        ["Approve", "Reject", "Defer", "Needs more info"], "Gate - do not scale outbound links without it") +
 sg_row("SG-02", "Set canonical domain + Search Console + sitemap submission",
        "One site to index; measured queries drive next topics", "Domain choice; Search Console property", "Low",
        ["Approve", "Reject", "Defer", "Needs more info"]) +
 sg_row("SG-03", "Deploy self-hosted analytics endpoint (5 events) + weekly ledger review",
        "Turns clicks into decisions without third-party trackers", "Hosting choice; retention policy", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"]) +
 sg_row("SG-04", "Licensed product photography (own photos or manufacturer permission)",
        "Real photos convert; copied Amazon images risk IP breach", "Licence / permission letters", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"]) +
 sg_row("SG-05", "Holiday gift guides (air fryer gifts, grill gifts) with dated price snapshots",
        "Seasonal intent; gift guides convert when the gift angle is verified per listing", "Gift-angle verification per listing", "Low",
        ["Approve", "Reject", "Defer", "Needs more info"], "Queue behind the topic calendar") +
 sg_row("SG-06", "\"Which one is for you\" chooser expansion (budget slider, counter-depth input)",
        "Better decision support without fake testing", "Usability feedback", "Low",
        ["Approve", "Reject", "Defer", "Needs more info"]) +
 sg_row("SG-07", "Reader capture (email signup) with explicit consent",
        "Owns audience beyond search", "Provider + consent copy + FTC review", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"], "RSS feed ships first; email stays off until approved") +
 sg_row("SG-08", "Newer-model watch (Chefman B0CNY1YVDD, ThermoMaven B0GL7Z4KP4)",
        "Decide whether to promote newer variants or keep current ASINs", "Variant comparison + margin check", "Low",
        ["Approve", "Reject", "Defer", "Needs more info"]) +
 sg_row("SG-09", "Hands-on testing programme (buy, cook, photograph, publish)",
        "Unlocks \"lived-with\" content competitors cannot copy", "Budget, protocol, disclosure of free vs bought units", "High",
        ["Approve", "Reject", "Defer", "Needs more info"], "Do not claim until done") +
 sg_row("SG-10", "Expand categories (second air fryer brand, second thermometer brand)",
        "More comparison depth; better internal linking", "New ASIN verification pass", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"]) +
 sg_row("SG-11", "Run the design brief (design-brief.html) as the brief for the visual overhaul: warm editorial brand, product-first hero, category tiles, sticky comparison bar",
        "Turns the site from a register into a publication a buyer can act on; cuts the generated-template feel",
        "Owner picks the visual direction from the brief's options; photography decision (SG-04) gates imagery", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"], "Needs decision") +
 sg_row("SG-12", "Adopt the eight-topic editorial calendar in the design brief as the publishing cadence (question-shaped titles tied to the verified products)",
        "Catchy, spec-backed topics feed organic search; every title is a question a buyer types",
        "Owner approves titles; each topic needs the same line-by-line verification before publishing", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"], "Needs decision") +
 sg_row("SG-13", "Anti-AI-slop writing rules in the CMS checklist: no filler transitions, no \"in conclusion\", varied sentence length, one idea per paragraph",
        "Readers and reviewers can tell template text; signal-rich writing ranks and converts better",
        "Style guide decision; editor review on every page", "Low",
        ["Approve", "Reject", "Defer", "Needs more info"], "Needs decision") +
 sg_row("SG-14", "Editorial voice decision: who is \"we\" (The Countertop Guide editorial team) and what we will never claim (no testing, no popularity, no superlatives)",
        "A defined voice is the strongest anti-slop lever and keeps FTC honesty intact",
        "Owner sign-off on voice statement", "Low",
        ["Approve", "Reject", "Defer", "Needs more info"], "Needs decision") +
 sg_row("SG-15", "Reader-facing seasonal clusters (holiday gift, New Year cooking reset) built from the verified products with dated price snapshots",
        "Seasonal intent searches; reuses verified data instead of new claims",
        "Season calendar decision; re-snapshot prices at publish", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"], "Proposed") +
 sg_row("SG-16", "Comparison-first homepage: lead with the side-by-side table and the three-question chooser above the fold, verification below",
        "Buyers act on comparisons; the verification register moves below the products",
        "Layout decision in the design brief", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"], "Proposed") +
 sg_row("SG-17", "Add author bylines and an \"updated\" date to every article and comparison",
        "Authorship and freshness signals; reads like a publication, not a template",
        "Author name/bio decision; date source from verification log", "Low",
        ["Approve", "Reject", "Defer", "Needs more info"], "Proposed") +
 sg_row("SG-18", "Internal-link cluster pages: one pillar per category linking every guide to the comparison and buying guide",
        "Cluster structure helps search engines and keeps readers on-site longer",
        "Topic approval (SG-12); link audit at publish", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"], "Proposed") +
 sg_row("SG-19", "Unify the site's brand (root site vs the Counter &amp; Crumb docs/articles pages)",
        "One brand on one domain is easier to index, remember and trust", "Owner review of both editorial sets", "Medium",
        ["Approve", "Reject", "Defer", "Needs more info"], "Flagged for owner decision - see FLG-025")
)

def q_row(qid, question, know, lack, discover, blocked, options=("Open", "Answered", "Blocked - owner needed")):
    return f"""
<tr><td>{qid}</td><td>{question}</td><td>{know}</td><td>{lack}</td><td>{discover}</td><td>{blocked}</td>
<td>{pick_select(qid, options)}<div class="pick-status small">Not picked yet</div></td></tr>"""

q_rows = (
 q_row("Q-01", "Are the supplied short links compliant Special Links?",
       "They resolve to the ASINs in the register (observed 2026-11-19)", "Exact compliance status is unresolved",
       "Test in Associates Central; read Operating Agreement + Policies", "Scaling outbound links") +
 q_row("Q-02", "What is the canonical domain?",
       "Site builds as static GitHub Pages; generator now emits per-page canonicals on the live pages URL", "Final domain / custom domain",
       "Owner picks domain; set canonical + Search Console", "SEO launch, og:image, sitemap") +
 q_row("Q-03", "What are thermometer dimensions &amp; Emeril wattage?",
       "Air fryer dims verified; thermometer dims + Emeril wattage not captured", "Missing fields (blank in tables)",
       "Re-fetch listing product-details sections; record date", "Counter-space table for thermometers; circuit advice") +
 q_row("Q-04", "Should we promote newer models instead?",
       "Listings show newer variants (see Flagged)", "Margin, rating trajectory, variant fit",
       "Compare variant listings; check Associates reports", "Product lineup") +
 q_row("Q-05", "What commission rates apply?",
       "Tracking ID shopnow047c-20; session rules in Policies", "Category rates (not published here)",
       "Associates Central commission statement (authorized report only)", "Revenue forecasting (not done)") +
 q_row("Q-06", "Is there search demand for these topics?",
       "Guides are question-shaped hypotheses, not volume claims", "Measured queries (no analytics yet)",
       "Search Console after launch; choose next topics from data", "Publishing cadence") +
 q_row("Q-07", "Can we use product photos?",
       "No Amazon images used; SVG/CSS only", "Licence / permission status",
       "Manufacturer permission or own photography", "Visual overhaul (SG-04)") +
 q_row("Q-08", "Where does analytics data live?",
       "Local-only counter; endpoint stub documented", "Hosting, retention, consent",
       "Pick host; publish retention policy", "Measurement &amp; optimisation (SG-03)") +
 q_row("Q-09", "Which visual direction from the design brief do we adopt?",
       "Brief offers a warm editorial direction with three named options and anti-slop rules",
       "Owner's pick; photography decision (Q-07) gates imagery",
       "Review design-brief.html; choose one direction", "Visual overhaul (SG-11)") +
 q_row("Q-10", "Do we approve the eight-topic editorial calendar?",
       "Titles are working hypotheses tied to verified products; none is a popularity claim",
       "Owner approval; per-topic verification still required",
       "Review calendar on design-brief.html", "Publishing cadence (SG-12)") +
 q_row("Q-11", "What is the site's editorial voice, and what will it never claim?",
       "No testing / popularity / superlative claims today; voice statement is proposed",
       "Owner sign-off on the voice statement",
       "Review voice rules on design-brief.html", "All content (SG-13, SG-14)") +
 q_row("Q-12", "Should the homepage lead with the comparison and chooser?",
       "Current homepage leads with categories then data",
       "Layout preference; impact on conversion vs. trust",
       "Review homepage layout option in the brief", "Homepage redesign (SG-16)") +
 q_row("Q-13", "Who are the named authors, and what bios go with them?",
       "Guides currently say \"The Countertop Guide editorial team\"",
       "Author identity and bio wording",
       "Owner provides names/bios or keeps the team credit", "Authorship (SG-17)") +
 q_row("Q-14", "What is the review SLA for this suggestions board?",
       "19 suggestions and 16 questions wait on owner choices",
       "Review cadence and who approves",
       "Owner sets a review rhythm; approved items become tasks", "All pending suggestions") +
 q_row("Q-15", "Which brand should the whole site use?",
       "Two editorial sets ship on one domain: The Countertop Guide (root) and Counter &amp; Crumb (docs/articles)",
       "Owner choice of one brand, or a decision to keep the docs set clearly internal",
       "Owner review of both sets; then update nav, footer and metadata once", "Brand unification (SG-19)") +
 q_row("Q-16", "Can the 2026-11-19 listing values be re-confirmed?",
       "Register with per-field sources and confirmation dates is recorded in verification.html",
       "Fresh fetch of listing product-details (this session's sandbox could not reach Amazon.com or link.amazon)",
       "Owner re-fetch of each listing, or an authorized channel per the Operating Agreement; record the date",
       "Price/rating freshness; FLG-004, FLG-005, FLG-020")
)

sugg_body = f"""
<section class="doc-hero">
<p class="eyebrow">Suggestions board &middot; Decision desk</p>
<h1>Suggestions &amp; decision log - review before anything is built</h1>
<p>Nothing on this board is implemented until a reviewer picks a path. Each suggestion states the evidence it needs, the effort, and what decision it blocks. Pick a path below; the pick stays in your browser and you can export a review sheet to hand over. We implement only approved items.</p>
</section>
<article class="doc-main" id="suggestion-board">
<div class="callout"><b>How to use this desk</b>
<p>Use the select on each row to choose a path (Approve / Reject / Defer / Needs more info). Picks are stored in your browser only - nothing is sent anywhere. Export a JSON review sheet when you are done; approved items move to COORDINATION.md as claimed tasks. Nothing here is a promise of traffic, ranking, or revenue.</p>
<div class="review-panel">
  <button class="btn" id="sg-export" type="button">Export review sheet (JSON)</button>
  <button class="btn secondary" id="sg-print" type="button">Print this page</button>
  <button class="btn secondary" id="sg-reset" type="button">Clear my picks</button>
</div></div>
<h2>Design &amp; content suggestions (this build)</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>#</th><th>Suggestion</th><th>Why it matters</th><th>Evidence needed</th><th>Effort</th><th>Your pick</th></tr>
{des_rows}
</table></div>
<h2>Suggestions for review</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>#</th><th>Suggestion</th><th>Why it matters</th><th>Evidence needed</th><th>Effort</th><th>Your pick</th></tr>
{sg_rows}
</table></div>
<h2>Questions, information &amp; answers needed before a reasonable decision</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>#</th><th>Question</th><th>What we know</th><th>What we do not know</th><th>How to discover it</th><th>Decision blocked</th><th>Status</th></tr>
{q_rows}
</table></div>
<p class="small">Reviewer: mark each item with a pick and a date. Approved items move to COORDINATION.md as claimed tasks. Missing information is surfaced as a question above - never filled in by assumption.</p>
</article>
"""
open("suggestions.html","w").write(page("suggestions.html","Suggestions Board & Decision Log: Review Before Building | The Countertop Guide","Suggestions board and decision desk for The Countertop Guide: design and content suggestions, operational suggestions, and the Q/I/A list of questions, information and answers needed before any decision.",sugg_body))

# ---------- VERIFICATION ----------
ver_rows = ""
for pid in ["P1","P2","P3","P4","P5"]:
    p = PRODS[pid]
    dims_cell = esc(p["dimensions"]) if p["dimensions"] else '<span class="badge-flag">Blank - not captured (Flagged)</span>'
    ver_rows += f"""
<article class="card" id="{pid}">
<h3>{pid} - {esc(p['shortName'])} (ASIN {p['asin']})</h3>
<div class="table-wrap"><table class="data-table">
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
<section class="doc-hero">
<p class="eyebrow">Verification register</p>
<h1>Line-by-line verification: every fact, its source</h1>
<p>Rule: every table row has a source link to an official site. If a value cannot be confirmed, it is left blank and flagged - never inferred. Intended ASIN and observed redirect target are stored in separate fields and never merged.</p>
</section>
<article class="doc-main">
<h2>Product-intent confirmation record</h2>
{ver_rows}
<h2>Policy sources (official)</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>Source</th><th>What it governs</th><th>Link</th></tr>
<tr><td>Amazon Associates Operating Agreement (updated 2025-10-15)</td><td>Special Links must properly use tagged link formats; Program Content definition; Section 5 disclosure statement</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement</a></td></tr>
<tr><td>Amazon Associates Program Policies (updated 2026-04-14)</td><td>Commission session rules; participation requirements</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td></tr>
<tr><td>FTC Disclosures 101 for Social Media Influencers (Nov 2019)</td><td>Material-connection disclosure: hard to miss, simple clear language</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td></tr>
<tr><td>FTC Endorsements, Influencers &amp; Reviews guidance</td><td>Endorsement context and review integrity</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td></tr>
</table></div>
<p class="small">Verification performed 2026-11-19 by fetching each Amazon listing and policy page; values are snapshots and will change. Manual Special Link test in Associates Central remains a gate (see <a href="flagged.html">Flagged</a>).</p>
<div class="callout"><b>Re-verification note (session arena/bb3ae11b-prod1, 2026-11-19)</b>
<p>This session's sandbox could not reach Amazon.com or link.amazon (outbound network allowlist), so the listing values above were not re-fetched again here and no value was changed. The values reflect the full line-by-line re-verification of 2026-11-19 by session arena/2ec8638e-prod1 (see <a href="docs/verification-log.md">docs/verification-log.md</a>). The five submitted short links and their ASIN mapping were re-checked against <code>data/products.json</code> and the generator, and the register's internal consistency was confirmed.</p></div>
</article>
"""
open("verification.html","w").write(page("verification.html","Verification Register: Line-by-Line Sources for Every Fact | The Countertop Guide","Verification register for 5 products: intended ASIN, official listing URL, confirmation date and source per product, plus official Amazon and FTC policy sources.",ver_body))

# ---------- FLAGGED ----------
flag_body = f"""
<section class="doc-hero">
<p class="eyebrow">Flagged for review</p>
<h1>Flagged for review - irregularities &amp; unverified items</h1>
<p>Flagged items do not block publishing, but they block claims. Nothing below is presented as fact on product pages. Review after launch and request changes.</p>
</section>
<article class="doc-main">
<div class="table-wrap"><table class="data-table">
<tr><th>ID</th><th>Item</th><th>Detail</th><th>Action</th></tr>
<tr><td>FLG-001</td><td>Short-link compliance unresolved</td><td>Supplied link.amazon short links resolve to the ASINs, but their exact compliance status as Special Links is unresolved. We do not claim they are invalid. Site outbound buttons use official listing URLs + tag instead.</td><td>Manual test in Associates Central (SG-01)</td></tr>
<tr><td>FLG-002</td><td>Preset &amp; capacity discrepancies</td><td>Emeril: title 24 presets vs bullets 25; title 26QT vs field 24.6 liters. Chefman 6QT: title 6 Quart vs field 6 liters. Both values shown; no silent conversion.</td><td>Verify on listing; ask seller if needed</td></tr>
<tr><td>FLG-003</td><td>Newer models shown on listings</td><td>Chefman 8QT page shows newer 6QT B0CNY1YVDD ($59.99, 4.6/7,602); ThermoMaven page shows newer Orange B0GL7Z4KP4 ($16.99, 4.7/144). We promote the submitted ASINs only.</td><td>Decide lineup (SG-08)</td></tr>
<tr><td>FLG-004</td><td>Missing dimensions (thermometers)</td><td>ThermoMaven B0DHZTCNR5 and CHEF iQ B0DZFD6R9Z dimensions not in captured fields. Left blank in tables.</td><td>Re-fetch product-details; record date</td></tr>
<tr><td>FLG-005</td><td>Missing warranty (Emeril)</td><td>Emeril wattage captured 2026-11-19 (1700 watts / 120 volts per the listing's Product information table). Warranty period is not stated on the listing page; the listing links a warranty PDF only. Left blank.</td><td>Read warranty PDF if the term is needed</td></tr>
<tr><td>FLG-006</td><td>Price volatility</td><td>All prices are {VERIFIED} snapshots (Black Friday period). Live price on Amazon governs.</td><td>Re-snapshot on cadence; date every price</td></tr>
<tr><td>FLG-007</td><td>Canonical is the GitHub Pages URL, not a custom domain</td><td>Canonical/og URLs now point to https://wingbangboozle1-lang.github.io/Prod1/ (session 9969fd0c). A custom domain is still unset, and the generator previously wrote a placeholder - fixed in build_site.py 2026-11-19 so rebuilds reproduce the committed pages; session arena/bb3ae11b-prod1 made canonicals per-page (one per page, not one shared URL).</td><td>Pick domain (SG-02)</td></tr>
<tr><td>FLG-008</td><td>Analytics endpoint not deployed</td><td>Five events defined; local counter only. No server endpoint yet.</td><td>Deploy endpoint (SG-03)</td></tr>
<tr><td>FLG-009</td><td>No product photography</td><td>No Amazon images used (IP/licence). SVG/CSS illustrations only.</td><td>Licence decision (SG-04)</td></tr>
<tr><td>FLG-010</td><td>No hands-on testing</td><td>We have not cooked with or calibrated any product. No "lived-with" claims made.</td><td>Testing programme if approved (SG-09)</td></tr>
<tr><td>FLG-011</td><td>No commission / revenue claims</td><td>Rates not published; ledger empty until authorized reports arrive.</td><td>Record only from Associates reports</td></tr>
<tr><td>FLG-012</td><td>No popularity claims</td><td>"Bought in past month" badges are listing snapshots, not our ranking. The evidence rule is: dated snapshot from an official source, or no claim.</td><td>Evidence rule: dated snapshot or no claim</td></tr>
<tr><td>FLG-013</td><td>Submitted link codes are 9 characters</td><td>Each submitted link.amazon path code (e.g. B04G1MEwY) is 9 characters. Each code resolves to a listing whose ASIN differs from the code, so the code is not used as an intended ASIN. Intended ASIN fields stay blank pending submitter confirmation (session 9b748801, 2026-11-19).</td><td>Submitter confirms intended ASIN per link</td></tr>
<tr><td>FLG-014</td><td>ASIN 10-character rule: third-party sources only</td><td>The 10-character ASIN format was found on third-party guides, not on an Amazon page read in this session. The format is used only to flag the 9-character codes.</td><td>Find an official Amazon help page for the ASIN definition</td></tr>
<tr><td>FLG-015</td><td>Redirect targets carry no tag=</td><td>The final URLs of the five supplied links (read 2026-11-19) contain no tag= parameter. Attribution to shopnow047c-20 is therefore not observed on the redirect path. Site buttons use tagged listing URLs (FLG-001).</td><td>Associates tracking-report test per product (SG-01)</td></tr>
<tr><td>FLG-016</td><td>Listing pages carry widget data for other ASINs</td><td>Listing pages include Product summary links and Customers who viewed carousels with prices and ratings for other products. These are not used as data for the five products.</td><td>Use only each product's own fields; re-check on publication</td></tr>
<tr><td>FLG-017</td><td>External register: three links vs five</td><td>The external Zone4 decision log (D-13) refers to the three supplied links; this brief supplies five. Its statuses are not carried into this site. Only the first part of that log was read.</td><td>Reconcile the external register with the five links</td></tr>
<tr><td>FLG-018</td><td>Proposed Amazon content notice (not verified)</td><td>The external Zone4 decision log proposes an Amazon content notice citing IP License section 2(k). The IP License was not read, and the notice is not yet on the pages.</td><td>Read IP License 2(k); decide under SG-04</td></tr>
<tr><td>FLG-019</td><td>Creators API prerequisites not read</td><td>The external Zone4 decision log suggests the Creators API for prices and ratings. Its prerequisites were not read, and no API data is used on this site.</td><td>Read prerequisites before any price or rating source change</td></tr>
<tr><td>FLG-020</td><td>Main-product values not fully re-read in integration</td><td>The integration check confirmed the five ASINs and the ThermoMaven price ($16.99) against the listing pages. Other prices, ratings and dimensions in data/products.json were not re-read in full in that pass.</td><td>Full re-read of each listing's product details before publishing price claims</td></tr>
<tr><td>FLG-021</td><td>Accessory count discrepancy (Emeril)</td><td>Listing title says "Six Cooking Accessories Included"; the listing's item details say "Air Fryer Toaster Oven Combo with 24 Functions and 7 Accessories"; the included-components list names 6 items (Rack, Bake Pan, Drip Tray, Crisper Basket, Rotisserie Spit, Fetch Tool). All three values are listing-internal and disagree. We show the title value and flag it; no count is inferred. Observed 2026-11-19.</td><td>Ask seller / read product manual; show title value with flag until resolved</td></tr>
<tr><td>FLG-022</td><td>Wattage discrepancy (Chefman 8QT)</td><td>Chefman 8QT listing bullets state "1000 Watts/120 Volts - RJ38-SQSS-8T" while the listing's Product information table lists Output Wattage 1700 watts, 120 volts. Both values are listing-internal and disagree. We show the bullets value with attribution and flag it; no wattage is inferred. Observed 2026-11-19.</td><td>Ask seller / read user manual; resolve before any circuit-load claim</td></tr>
<tr><td>FLG-023</td><td>Intended ASIN inconsistency</td><td>data/products.json sets the intended ASIN equal to the verified/observed ASIN. FLG-013 states intended ASIN fields stay blank pending submitter confirmation, and the brief requires intended and observed targets to remain separate.</td><td>Owner confirms each intended ASIN or blanks the field (R-02, Q-03)</td></tr>
<tr><td>FLG-024</td><td>Rating-count snapshot drift</td><td>Re-read of listings 2026-11-19 shows P2 rating count 18,375 (recorded 18,371) and P3 16,892 (recorded 16,890). Ratings, like prices, are snapshots that change.</td><td>Re-snapshot ratings on cadence; treat recorded counts as unverified until re-confirmed</td></tr>
<tr><td>FLG-025</td><td>Two editorial brands on one domain</td><td>The root site (The Countertop Guide) and the docs/ + articles/ set (Counter &amp; Crumb) ship under different brand names on the same GitHub Pages domain. Both carry disclosures and sponsored-link marks; the brand split is an owner decision, not a compliance failure.</td><td>Owner decision (SG-19)</td></tr>
</table></div>
</article>
"""
open("flagged.html","w").write(page("flagged.html","Flagged for Review: Irregularities & Unverified Items | The Countertop Guide","Flagged irregularities for The Countertop Guide: short-link compliance, preset/capacity discrepancies, newer models, missing fields, price volatility and launch gates.",flag_body))

# ---------- COMPLIANCE ----------
comp_body = f"""
<section class="doc-hero">
<p class="eyebrow">Compliance gate</p>
<h1>Disclosures &amp; policy checks in the publishing workflow</h1>
<p>Disclosure above the fold on every page (and repeated in the footer). Every outbound product link is marked sponsored. Endorsement context is reviewed against the Operating Agreement and FTC guidance before publishing.</p>
</section>
<article class="doc-main">
<h2>Our disclosure (verbatim, every page)</h2>
<blockquote>{DISCLOSURE} Prices and availability are snapshots from Amazon.com on the verification date and can change - always check the price on Amazon before you buy.</blockquote>
<p class="small">Wording decision (2026-11-19): the site now uses the exact Operating Agreement Section 5 sentence, which also clears the publishing gate's variant-wording warning. Source: <a href="https://affiliate-program.amazon.com/help/operating/agreement">Amazon Associates Operating Agreement, Section 5</a>.</p>
<h2>How each outbound link is marked</h2>
<ul>
<li>URL format: <code>https://www.amazon.com/dp/ASIN?tag={TAG}</code> (official listing URL + tracking ID).</li>
<li>Attributes: <code>rel="sponsored nofollow noopener"</code>, <code>target="_blank"</code>, visible "sponsored" label and "Opens amazon.com" text so destination is never obscured.</li>
<li>Short links are recorded in the <a href="verification.html">verification register</a> as submitted links with observed redirect targets in a separate field. They are not used as outbound buttons.</li>
</ul>
<h2>Policy checklist (reviewed 2026-11-19)</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>Check</th><th>Source</th><th>Our practice</th></tr>
<tr><td>Use proper tagged Special Link formats</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement S1</a></td><td>Official URL + tag; manual SiteStripe test is a gate (FLG-001)</td></tr>
<tr><td>Do not obscure link destination</td><td><a href="https://affiliate-program.amazon.com/help/operating/policies">Program Policies</a></td><td>Button text + ASIN + "Opens amazon.com" on every card</td></tr>
<tr><td>Disclose material connection, hard to miss</td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a></td><td>Strip under masthead on every page + footer; simple language ("earns from qualifying purchases")</td></tr>
<tr><td>Endorsement honesty; no unsubstantiated claims</td><td><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews">FTC Endorsements</a></td><td>No testing/popularity claims; seller claims attributed ("per listing")</td></tr>
<tr><td>Program Content / images</td><td><a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement S1</a></td><td>No Amazon images copied; SVG/CSS only until licence decided</td></tr>
</table></div>
<p class="small">This page is a publishing checklist, not legal advice. Review disclosure placement and endorsement context against the current Agreement and FTC guidance at each publish. If in doubt, flag it.</p>
</article>
"""
open("compliance.html","w").write(page("compliance.html","Compliance: Disclosures & Amazon/FTC Policy Checks | The Countertop Guide","Compliance gate for The Countertop Guide: disclosure wording, sponsored-link marking, and Amazon Associates + FTC policy checklist reviewed before publishing.",comp_body))

# ---------- METHODOLOGY ----------
meth_body = f"""
<section class="doc-hero">
<p class="eyebrow">Method</p>
<h1>How we verify, measure, and decide - without hallucinating</h1>
<p>Automate what can be automated; put a gate in front of what cannot. This page is the machinery: evidence rules, analytics events, and the empty campaign ledger.</p>
</section>
<article class="doc-main">
<h2>Evidence rule</h2>
<ul>
<li>Every product fact links to its Amazon listing and <a href="verification.html">verification record</a>. Missing = blank + flagged.</li>
<li>Popularity claims require a dated snapshot from an official source. We make none.</li>
<li>Seller claims are attributed ("per listing"). Derived math shows its method. Prices always carry a snapshot date.</li>
<li>Hands-on testing claims require a published protocol and photos. We make none.</li>
</ul>
<h2>Analytics: five defined events (privacy-preserving)</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>Event</th><th>When it fires</th><th>Data kept</th></tr>
<tr><td>page_view</td><td>Page load</td><td>Path + timestamp (local only until endpoint deployed)</td></tr>
<tr><td>outbound_click</td><td>Sponsored Amazon click</td><td>ASIN + destination (no personal data)</td></tr>
<tr><td>search</td><td>Site search submitted</td><td>Query string</td></tr>
<tr><td>chooser_complete</td><td>3-question chooser finished</td><td>Answers (q1/q2/q3)</td></tr>
<tr><td>guide_read</td><td>Guide scrolled 75%</td><td>Guide path</td></tr>
</table></div>
<p>Implementation: <code>assets/app.js</code> counts locally in <code>localStorage</code> and beacons to a configurable endpoint (<code>data-analytics-endpoint</code>, currently empty). No third-party trackers. Deploying the endpoint is SG-03; until then, counts are device-local and the ledger stays empty.</p>
<h2>Campaign ledger (empty by design)</h2>
<div class="table-wrap"><table class="data-table">
<tr><th>Date</th><th>Source</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th><th>Reported orders</th><th>Provenance</th></tr>
<tr><td colspan="7"><em>No rows yet. Add timestamp, source, channel, eligible sessions, clicks and reported orders only when obtained from authorized first-party reports (Associates Central). No conversion score or revenue forecast is presented.</em></td></tr>
</table></div>
<h2>Publishing cadence</h2>
<p>New guides are added to <a href="sitemap.xml">sitemap.xml</a> and <a href="feed.xml">feed.xml</a> at publish. The <a href="topics.html">topic calendar</a> lists the eight working titles; the next topic is chosen from measured Search Console queries (after SG-02), not instinct.</p>
</article>
"""
open("methodology.html","w").write(page("methodology.html","Method: Verification, Analytics Events & Campaign Ledger | The Countertop Guide","Method page for The Countertop Guide: evidence rules, five privacy-preserving analytics events, empty campaign ledger with provenance rules, and publishing cadence.",meth_body))

# ---------- DESIGN BRIEF ----------
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
open("design-brief.html","w").write(page("design-brief.html","Design Brief: Suggestions for the Publication Redesign | The Countertop Guide","Design brief suggestions for The Countertop Guide redesign: design prompt blocks, three visual directions, anti-AI-slop rules, an eight-topic editorial calendar, and decision gates for review.",db_body))
# ---------- SEARCH ----------
search_body = """
<section class="doc-hero">
<p class="eyebrow">Search</p>
<h1>Search the site</h1>
<p>Search guides, products and decision pages. Results come from a local index - no query leaves your browser.</p>
</section>
<article class="doc-main">
<form id="search-page-form" role="search">
  <label for="search-input">Search guides &amp; products</label>
  <input id="search-input" type="search" placeholder="Try capacity or thermometer">
  <button class="btn" type="submit">Search</button>
</form>
<div id="search-results" aria-live="polite"></div>
<p><a href="guides.html">Browse all guides</a> &middot; <a href="topics.html">Topic calendar</a> &middot; <a href="compare.html">Compare</a></p>
</article>
"""
open("search.html","w").write(page("search.html","Search Guides & Products | The Countertop Guide","Search The Countertop Guide guides and product comparisons: air fryers, thermometers, capacity, cleanup, counter space and accuracy.",search_body))

idx = [
 {"title":"Air fryers category","url":"air-fryers.html","text":"Chefman 6QT dual-basket, Emeril 26QT French-door oven, Chefman 8QT TurboFry. Capacity, footprint, cleanup, price snapshots."},
 {"title":"Thermometers category","url":"thermometers.html","text":"ThermoMaven 1-second instant-read vs CHEF iQ Sense wireless 3-probe. Accuracy claims, range, probes."},
 {"title":"Compare all five","url":"compare.html","text":"Side-by-side table, 3-question chooser, counter-space analysis, capacity per cm depth."},
 {"title":"Topic calendar","url":"topics.html","text":"Eight spec-backed buyer questions: five published guides and three queued working titles with sources."},
 {"title":"Basket or oven-style air fryer: what should you compare?","url":"guide-basket-vs-oven.html","text":"Dual-basket vs French-door oven vs single basket. Two-dish cooking, crowd capacity, counter depth."},
 {"title":"A no-hype checklist for comparing air fryer capacity","url":"guide-capacity-checklist.html","text":"Quarts vs litres, single vs dual baskets, feeds 4-6, rotisserie and pizza claims."},
 {"title":"How to assess cleanup and counter-space trade-offs","url":"guide-cleanup-counter-space.html","text":"Dishwasher-safe baskets, footprint math, capacity per centimetre of counter depth."},
 {"title":"Questions to ask before buying a multi-function kitchen appliance","url":"guide-multifunction-questions.html","text":"Presets, accessories, wattage, warranty and fit checklist for multi-function ovens."},
 {"title":"Instant-read or wireless? How to read accuracy claims","url":"guide-thermometer-accuracy.html","text":"Plus-minus 0.5F, NIST NSF, sensor counts, WiFi range. How to read thermometer claims."},
 {"title":"Executive summary","url":"executive-summary.html","text":"What the site is, what is verified, compliance posture, measurement plan, decision gates."},
 {"title":"Suggestions board and decision desk","url":"suggestions.html","text":"Design and content suggestions, operational suggestions SG-01 to SG-12, questions Q-01 to Q-10, review picks."},
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
