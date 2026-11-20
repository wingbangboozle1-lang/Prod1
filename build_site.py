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
# Editorial reading of the listing. Every phrase below paraphrases a field on the linked
# Amazon listing (attributed "per listing" in the copy) or says a figure is not shown there.
POSITION = {
    "P1": {"good": "two different dishes finishing at the same time (2 independent 3-quart baskets, Sync Finish - per listing)",
           "check": "34.0 cm of counter depth (13.38 in, as listed) - measure your own space, and check the clearance the manual asks for",
           "headline": "The two-basket one"},
    "P2": {"good": "cooking for four to six, rotisserie and a 12-inch pizza in one cavity (per listing)",
           "check": "42.9 cm of depth - the largest here - plus room for the doors to swing; the warranty period is not stated on the listing",
           "headline": "The family-size oven"},
    "P3": {"good": "one big batch on a shallow footprint, with a top-rack dishwasher-safe basket and tray (per listing)",
           "check": "one cavity, so two dishes means staggering; 450F Hi-Fry appears in the title while the bullets give 200-400F",
           "headline": "The weeknight workhorse"},
    "P4": {"good": "a one-second reading in your hand, with a +/-0.5F and NIST/NSF claim on the listing",
           "check": "it is handheld - it will not watch the roast from another room; its dimensions are not in the fields we captured",
           "headline": "The pocket read"},
    "P5": {"good": "three probes and app alerts while you are away from the oven",
           "check": "no +/-F accuracy figure appears in the fields we captured, and it needs WiFi, the hub and the app to earn its place",
           "headline": "The phone-watched setup"},
}
# ---------------------------------------------------------------- product card
def cta_note(p):
    return (f'Sponsored link &middot; opens Amazon &middot; as listed {VERIFIED} &middot; '
            f'<a href="verification.html#{p["id"]}">source record</a>')
def product_card(pid, bullets_n=3, detailed=False):
    p = PRODS[pid]; pos = POSITION[pid]; dm = dims_of(p)
    bl = "".join(f"<li>{esc(b)}</li>" for b in p["bullets"][:bullets_n])
    dims = esc(p["dimensions"]) if p["dimensions"] else "not shown in the fields we captured"
    if SHOW_PRICE:
        money = f'<p class="price-row"><span class="price">{esc(p["priceNew"])}</span> <span class="fine">listed {VERIFIED} &middot; Amazon price governs</span></p>'
    else:
        money = f'<p class="price-row"><span class="price-live">Price moves on Amazon</span> <span class="fine">we do not publish a stale figure &mdash; the button shows today&rsquo;s</span></p>'
    rating = (f'<p class="fine"><span class="stars">&#9733; {esc(p["rating"])}</span> from {esc(p["ratingCount"])} ratings, as counted on {VERIFIED}. Live count on the listing.</p>') if SHOW_RATING else ""
    footprint = f'<div><dt>Counter depth</dt><dd>{dm["depth_in"]} in ({dm["depth_cm"]} cm)</dd></div>' if dm else ""
    height = f'<div><dt>Height</dt><dd>{dm["height_in"]} in ({dm["height_cm"]} cm) &mdash; check your cabinet clearance</dd></div>' if dm and dm.get("height_cm") else ""
    power = f'<div><dt>Power, as listed</dt><dd>{flaglinks(esc(p["wattage"]))}</dd></div>' if p.get("wattage") and p["wattage"] not in ("", "—") else ""
    extra = f'<ul class="bullets">{bl}</ul>' if detailed else ""
    return f"""
<article class="prod" id="{pid}">
  <div class="prod-head">
    <span class="chip">{esc(p['form'])}</span>
    <h3>{esc(p['shortName'])}</h3>
    <p class="prod-sub">{esc(pos['headline'])} &middot; {esc(p['category'])}</p>
    {money}{rating}
  </div>
  <dl class="specs">
    <div><dt>Capacity, as titled</dt><dd>{esc(p['capacityTitle'])}</dd></div>
    <div><dt>Footprint on the listing</dt><dd>{dims}</dd></div>
    {footprint}{height}{power}
    <div><dt>Features, as listed</dt><dd>{esc(p['specialFeatures']) or 'not summarised here'}</dd></div>
  </dl>
  <p class="best"><strong>Good for:</strong> {esc(pos['good'])}</p>
  <p class="watch"><strong>Check before you buy:</strong> {esc(pos['check'])}</p>
  {extra}
  <p class="cta-row"><a class="btn" href="{aff(p)}" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="{p['asin']}">{('See today&rsquo;s price on Amazon' if not SHOW_PRICE else 'Buy at Amazon')}</a>
     <a class="link-quiet" href="compare.html#{pid}">See how it compares</a></p>
  <p class="fine">{cta_note(p)}</p>
</article>"""
# ---------------------------------------------------------------- chrome
NAV = f"""<nav class="nav" aria-label="Main">
  <a href="air-fryers.html">Air fryers</a>
  <a href="thermometers.html">Thermometers</a>
  <a href="compare.html">Compare</a>
  <a href="guides.html">Guides</a>
  <a href="about.html">About</a>
  <a href="review-desk.html" class="nav-desk">Review desk</a>
</nav>
<form class="searchbox" id="site-search-form" role="search">
  <label class="skip" for="site-search-input">Search the site</label>
  <input id="site-search-input" type="search" placeholder="Search specs, guides" aria-label="Search the site">
  <button class="btn small secondary" type="submit">Search</button>
</form>"""
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
    <nav aria-label="Review desk"><p><strong>Review desk</strong></p><p><a href="review-desk.html">Desk index</a><br><a href="verification.html">Verification register</a><br><a href="flagged.html">Flagged for review</a><br><a href="suggestions.html">Suggestions &amp; decisions</a><br><a href="methodology.html">Method &amp; ledger</a><br><a href="compliance.html">Compliance gate</a><br><a href="executive-summary.html">Executive summary</a><br><a href="design-brief.html">Design brief (parallel)</a><br><a href="about.html">About &amp; contact</a></p></nav>
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
    PAGES.append({"slug": slug, "title": title, "description": desc, "kind": kind, "canonical": canon})
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
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
{NAV}
</div></header>
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
     "angle": "What an Amazon's Choice badge and a rating snapshot can and cannot tell a buyer, with the snapshot date kept visible.",
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


index_body = f"""
<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">Air fryers &amp; meat thermometers &middot; checked {VERIFIED}</p>
    <h1>Find the one that fits your counter and your weeknight.</h1>
    <p class="lede">Five machines, compared on the four things that actually decide it: capacity, counter depth, cleanup, and what the listing quietly leaves out. Every spec links to the Amazon page it came from, with the date we read it.</p>
    <p class="hero-cta"><a class="btn" href="compare.html#chooser">Answer three questions</a> <a class="btn ghost" href="air-fryers.html">Browse air fryers</a></p>
    <ul class="hero-facts">
      <li><strong>5</strong> products, each read from its own listing</li>
      <li><strong>0</strong> claims of cooking with a machine nobody cooked with</li>
      <li><strong>1</strong> source link per fact</li>
    </ul>
  </div>
  <aside class="hero-side" aria-label="Start here">
    <p class="side-title">Two minutes, three decisions</p>
    <ol>
      <li><a href="guide-basket-vs-oven.html">Basket or oven-style?</a> <span>Form factor first - it decides everything else.</span></li>
      <li><a href="guide-capacity-checklist.html">How much capacity is real?</a> <span>Quarts, litres and &ldquo;feeds 4-6&rdquo; read honestly.</span></li>
      <li><a href="guide-cleanup-counter-space.html">Will it fit, and will you wash it?</a> <span>Depth, cabinet clearance, dishwasher parts.</span></li>
    </ol>
    <p class="fine">Listing data checked {VERIFIED}. Prices and ratings live on Amazon and move - we link to them rather than quote a stale figure.</p>
  </aside>
</section>

<h2>Quick picks, straight from the listings</h2>
<div class="grid cols-3">
  <article class="pick"><span class="chip">Two dishes at once</span><h3>Chefman 6QT Dual-Basket</h3><p>Two independent 3-quart baskets with Sync Finish, so chicken and vegetables land together. The narrowest of the three fryers at 11.81 in wide.</p><p><a class="btn small" href="air-fryers.html#P1">Look at this one</a></p></article>
  <article class="pick"><span class="chip">Feeding four to six</span><h3>Emeril Lagasse 26QT French-Door</h3><p>The biggest cavity here: rotisserie for a 6-lb chicken and a 12-inch pizza, per the listing. Also the deepest, at 16.9 in - measure before you order.</p><p><a class="btn small" href="air-fryers.html#P2">Look at this one</a></p></article>
  <article class="pick"><span class="chip">Shallowest of the fryers</span><h3>Chefman 8QT TurboFry</h3><p>One big basket in 12.75 in of depth, 450F Hi-Fry in the title, basket and tray top-rack dishwasher safe per the bullets.</p><p><a class="btn small" href="air-fryers.html#P3">Look at this one</a></p></article>
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
<div class="grid cols-3">{product_card('P1')}{product_card('P2')}{product_card('P3')}</div>
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
<div class="grid cols-2">{product_card('P4')}{product_card('P5')}</div>
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
<h2>Guide</h2>
<ul><li><a href="guide-thermometer-accuracy.html">Instant-read or wireless? How to read accuracy claims without being misled</a></li></ul>
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
<div class="grid cols-2">
<article class="card"><span class="tag">Air fryers - Form</span><h3>Basket or oven-style air fryer: what should you compare?</h3><p>Dual-basket vs French-door oven vs single basket: cooking two dishes, crowd capacity, and counter depth.</p><p><a class="btn small" href="guide-basket-vs-oven.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Capacity</span><h3>A no-hype checklist for comparing air fryer capacity</h3><p>Quarts vs litres, "feeds 4-6", rotisserie and pizza claims - how to read capacity without being misled.</p><p><a class="btn small" href="guide-capacity-checklist.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Space &amp; cleanup</span><h3>How to assess cleanup and counter-space trade-offs</h3><p>Dishwasher-safe baskets, footprint math, and capacity per centimetre of counter depth.</p><p><a class="btn small" href="guide-cleanup-counter-space.html">Read guide</a></p></article>
<article class="card"><span class="tag">Multi-function</span><h3>Questions to ask before buying a multi-function kitchen appliance</h3><p>Presets, accessories, wattage and warranty - the pre-purchase checklist, applied to the Emeril oven.</p><p><a class="btn small" href="guide-multifunction-questions.html">Read guide</a></p></article>
<article class="card"><span class="tag">Thermometers - Accuracy</span><h3>Instant-read or wireless? How to read accuracy claims</h3><p>+/-0.5F, NIST/NSF, sensor counts and range - what each claim does and does not prove.</p><p><a class="btn small" href="guide-thermometer-accuracy.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal</span><h3>Holiday air fryer gifts: how to choose one that gets used</h3><p>The gift checklist that works without a price tag: depth, cleanup, one control panel they will actually learn.</p><p><a class="btn small" href="guide-gift-picks.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Hosting</span><h3>The holiday hosting test: which air fryer actually feeds a crowd?</h3><p>Capacity claims, a 6-lb rotisserie chicken, 12-inch pizzas - and the counter-depth number that decides fit in December.</p><p><a class="btn small" href="guide-holiday-hosting.html">Read guide</a></p></article>
<article class="card"><span class="tag">Seasonal - Budget</span><h3>Kitchen gifts under $25, under $80 and under $150</h3><p>Budget bands mapped to the five verified picks, with each listing's own gift claims quoted, not invented.</p><p><a class="btn small" href="guide-gifts-by-budget.html">Read guide</a></p></article>
<article class="card"><span class="tag">Air fryers - Specs</span><h3>Will it trip the breaker? Wattage and outlet math for air fryers</h3><p>1000W or 1700W? One of our listings answers that question two different ways - here is how to check yours.</p><p><a class="btn small" href="guide-wattage-outlets.html">Read guide</a></p></article>
</div>
<h2>Consolidated URLs</h2>
<p class="small">A parallel pass published three more seasonal pages on questions this list already covers. They stay live but return a canonical reference to the surviving guide, so one question has one answer: <a href="guide-holiday-gifts.html">holiday gifts</a> &rarr; <a href="guide-gift-picks.html">gift picks</a>; <a href="guide-small-kitchen.html">small-kitchen fit</a> &rarr; <a href="guide-cleanup-counter-space.html">counter space</a>; <a href="guide-holiday-roast.html">holiday roast thermometer</a> &rarr; <a href="guide-thermometer-accuracy.html">accuracy claims</a>. Reason and reversal option: <a href="flagged.html#FLG-047">FLG-047</a>.</p>
"""
page_to("guides.html","Buying guides for air fryers & probes | Countertop Guide","Nine question-led guides on air fryers and meat thermometers: form factor, capacity, cleanup, presets, accuracy claims, gift picks, hosting, budget bands and wattage.",guides_body)
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
# ---------- EXECUTIVE SUMMARY ----------
exec_body = f"""
<p class="eyebrow">Executive summary</p>
<h1>What this site is, what is verified, and what happens next</h1>
<p class="lede">The Countertop Guide is a spec-backed affiliate publication for two kitchen categories - air fryers and meat thermometers - built from five Amazon listings verified on {VERIFIED}. It leads with products and buyer questions, not with process. Every number links to its source.</p>
<h2>The five products</h2>
<div class="table-scroll"><table>
<tr><th>ID</th><th>Product</th><th>ASIN</th><th>Category</th><th>Spec fields verified</th><th>Listing</th></tr>
<tr><td>P1</td><td>Chefman 6QT Dual-Basket Air Fryer Oven</td><td>B0CDY277D3</td><td>Air fryers</td><td>title, capacity, dimensions, features, bullets</td><td><a href="https://www.amazon.com/dp/B0CDY277D3">B0CDY277D3</a></td></tr>
<tr><td>P2</td><td>Emeril Lagasse 26QT French-Door Oven</td><td>B09B7SB46R</td><td>Air fryers</td><td>title, capacity, dimensions, features, bullets, wattage (warranty period not stated)</td><td><a href="https://www.amazon.com/dp/B09B7SB46R">B09B7SB46R</a></td></tr>
<tr><td>P3</td><td>Chefman 8QT TurboFry Basket</td><td>B08DKYBTPH</td><td>Air fryers</td><td>title, capacity, dimensions, features, bullets</td><td><a href="https://www.amazon.com/dp/B08DKYBTPH">B08DKYBTPH</a></td></tr>
<tr><td>P4</td><td>ThermoMaven 1-Second Instant-Read</td><td>B0DHZTCNR5</td><td>Thermometers</td><td>title, accuracy claim, features, bullets (dimensions not captured)</td><td><a href="https://www.amazon.com/dp/B0DHZTCNR5">B0DHZTCNR5</a></td></tr>
<tr><td>P5</td><td>CHEF iQ Sense Wireless (3 probes)</td><td>B0DZFD6R9Z</td><td>Thermometers</td><td>title, sensors, features, bullets (dimensions and +/-F figure not captured)</td><td><a href="https://www.amazon.com/dp/B0DZFD6R9Z">B0DZFD6R9Z</a></td></tr>
</table></div>
<h2>What is verified</h2>
<ul>
<li>Each submitted short link resolves to the ASIN and official listing URL in <a href="verification.html">verification register</a> (intended ASIN kept separate from observed redirect target).</li>
<li>Titles, dimensions (air fryers), capacity, special features and bullets as shown on Amazon.com on {VERIFIED}. Price and rating were observed on the same date and are recorded in the register, not displayed on shop pages - see FLG-032 for the policy reason.</li>
<li>Compliance posture: disclosure above the fold on every page and in the footer; every outbound product link is rel="sponsored" and labeled; no trend or popularity claims without a dated snapshot; no hands-on testing claims.</li>
</ul>
<h2>What is not verified (and therefore not claimed)</h2>
<ul>
<li>Thermometer dimensions (not stated on either listing), the Emeril warranty period (a PDF is linked, nothing on the page), the CHEF iQ +/-F accuracy figure, and the Chefman 8QT wattage, where one listing disagrees with itself - all blank or attributed, and flagged.</li>
<li>Short-link compliance status (unresolved), Special Link test in Associates Central (manual gate), commission rates (not published here), search volume / popularity (not claimed).</li>
<li>Product photography (no Amazon images used; real photography needs a licence decision).</li>
</ul>
<h2>How money and measurement work</h2>
<p>Outbound links use tracking ID <code>{TAG}</code> and are marked sponsored. Click and conversion measurement is defined (five events) with a privacy-preserving local counter; the self-hosted endpoint is a documented stub, not yet deployed. The campaign ledger starts empty - orders and revenue are recorded only from authorized first-party reports. See <a href="methodology.html">Method &amp; campaign ledger</a>.</p>
<h2>What this pass changed</h2>
<ul>
<li><strong>Reader-facing order.</strong> Front page now leads with the picks and the products; the register, flags and method moved behind one Review desk link and the footer.</li>
<li><strong>No stale figures.</strong> Price, rating, rating count, badge and &ldquo;bought in past month&rdquo; are off the shop pages, with the policy read behind the decision (<a href="flagged.html#FLG-032">FLG-032</a>).</li>
<li><strong>Disclosure wording.</strong> The strip and footer carry the Operating Agreement&rsquo;s sentence verbatim, plus a plain-language line a reader can parse.</li>
<li><strong>Findability.</strong> Per-page canonical, unique titles and descriptions, absolute raster og:image, generated sitemap and feed, ItemList/Article/Breadcrumb structured data, and the canonical-vs-sitemap mismatch closed.</li>
<li><strong>Links.</strong> Script-built chooser links now carry <code>rel="sponsored"</code> and a visible label, and the CI gate checks the JavaScript too.</li>
<li><strong>Gate in the pipeline.</strong> <code>scripts/check_meta.mjs</code> runs before the Pages upload, which also closes request R-01 from session b4c6c619.</li>
<li><strong>New surfaces.</strong> <code>about.html</code> (who writes this, how it earns), <code>review-desk.html</code> (every internal surface in one group) and a seasonal guide that demonstrates the cadence pipeline.</li>
</ul>
<h2>Next gates (owner decisions)</h2>
<p>Canonical domain, Special Link validation, photography licence, analytics endpoint, and the Suggestions board priorities. Nothing scales until those gates pass. See <a href="suggestions.html">Suggestions &amp; decision log</a> and <a href="flagged.html">Flagged for review</a>.</p>
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

<h2>The board</h2>
<div class="table-scroll"><table>
<tr><th>#</th><th>Suggestion</th><th>Why it matters</th><th>Evidence needed</th><th>Effort</th><th>Status</th></tr>
<tr id="SG-01"><td>SG-01</td><td>Validate one Special Link per product in Associates Central (SiteStripe) and confirm destination + tracking report</td><td>Proves outbound links earn correctly before scaling</td><td>Associates Central test clicks + report screenshots</td><td>Low (manual)</td><td><span class="badge-warn">Needs decision - gate</span></td></tr>
<tr id="SG-02"><td>SG-02</td><td>Set canonical domain + Search Console + sitemap submission</td><td>One site to index; measured queries drive next topics</td><td>Domain choice; Search Console property</td><td>Low</td><td><span class="badge-warn">Needs decision</span></td></tr>
<tr id="SG-03"><td>SG-03</td><td>Deploy self-hosted analytics endpoint (5 events) + weekly ledger review</td><td>Turns clicks into decisions without third-party trackers</td><td>Hosting choice; retention policy</td><td>Medium</td><td><span class="badge-warn">Needs decision</span></td></tr>
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
<tr id="Q-27"><td>Q-27</td><td>Who publishes this site, the branch or the workflow?</td><td>The workflow gates every push to <code>main</code>; GitHub&rsquo;s legacy branch build is what actually serves the pages. <a href="flagged.html#FLG-051">FLG-051</a> and <a href="suggestions.html#SG-43">SG-43</a></td><td>Whether to move Pages to the GitHub Actions build source</td><td>Owner: Settings &rarr; Pages &rarr; Build source &rarr; GitHub Actions; then the next deploy run publishes the artifact and a failed gate stops it</td><td>Every claim this site makes about automation being load-bearing</td></tr>
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
<tr><td>SG-11</td><td>Run the design brief as the brief for the visual overhaul</td><td><select data-pick="SG-11"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-12</td><td>Adopt the eight-topic editorial calendar as the publishing cadence</td><td><select data-pick="SG-12"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-22</td><td>One site, one canonical, one sitemap (consolidate the builds)</td><td><select data-pick="SG-22"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>SG-43</td><td>Switch Pages to the GitHub Actions build source</td><td><select data-pick="SG-43"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>Q-21</td><td>Which design direction does the owner want?</td><td><select data-pick="Q-21"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
<tr><td>Q-23</td><td>What is the publishing cadence and who approves topics?</td><td><select data-pick="Q-23"><option value="">- pick a path -</option><option>Approve</option><option>Reject</option><option>Defer</option><option>Needs more info</option></select></td><td class="pick-status">Not picked yet</td></tr>
</table></div>
<div class="review-panel">
  <button class="btn small" id="sg-export" type="button">Export review sheet (JSON)</button>
  <button class="btn secondary small" id="sg-print" type="button">Print this board</button>
  <button class="btn secondary small" id="sg-reset" type="button">Clear my picks</button>
</div>
</div>
"""
page_to("suggestions.html","Decision desk: options & evidence | Countertop Guide","Twenty-five ranked suggestions with options and trade-offs, a copy-paste design brief, and fourteen questions whose answers gate the next build.",sugg_body)

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
<tr id="FLG-008"><td>FLG-008</td><td>Analytics endpoint not deployed</td><td>Five events defined; local counter only. No server endpoint yet.</td><td>Deploy endpoint (SG-03)</td></tr>
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
<tr id="FLG-039"><td>FLG-039</td><td>Three builds are published on one host, under two brands</td><td>The root publication, <code>counter-check/site/</code> (Counter Check) and the <code>docs/</code> + <code>articles/</code> build (Counter &amp; Crumb, still open as draft PR #10) are all reachable and all indexable, and the root sitemap previously listed <code>docs/</code> and <code>articles/</code> URLs. That splits the domain across near-duplicate content and two mastheads. Nothing here is a policy breach - it is a findability and brand problem. The sitemap generated by this pass lists only the pages this build writes.</td><td>Owner picks one publication (SG-22); then noindex or remove the others and reconcile the two mastheads</td></tr>
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
<h2>What the policies say, in their own words (read {VERIFIED})</h2>
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
<p class="fine">Contract notes settled in this pass: two other tracker scripts exist in the repository (<code>app.js</code> at the root, serving the <code>articles/</code> and <code>docs/</code> build, and <code>assets/js/analytics.js</code>, unreferenced). They use different event names and payloads from the server stub in <code>analytics-endpoint/</code>. This session did not edit those files - they belong to other sessions - and instead records the single taxonomy above as the one the root site uses. Unifying the rest is <a href="suggestions.html#SG-03">SG-03</a>; see also <a href="flagged.html">FLG-034</a> for the sponsored-marking fix in the chooser output.</p>
<p class="fine">Endpoint status, stated exactly: no host is configured, so nothing is transmitted. The endpoint implementation in this repository (<code>analytics-endpoint/server.py</code>, owned by another session) accepts a payload carrying <code>event</code>, <code>path</code> and an optional <code>asin</code> and knows three of these five names (<code>page_view</code>, <code>outbound_click</code>, and its own <code>guide_read_75</code> for the 75% scroll event). The client here sends a payload that satisfies that validator today, and keeps the five names above as this site&rsquo;s contract. Checked by running the endpoint&rsquo;s own validator against our payload in this session: <code>page_view</code> and <code>outbound_click</code> return valid, the other three names return &ldquo;unknown event&rdquo;. Reconciling that vocabulary is request R-06 in <code>COORDINATION.md</code> - the endpoint is owned by another session, so it was not edited here.</p>
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
<tr><td>Adding a guide to sitemap and feed</td><td><span class="badge-ok">Automated</span></td><td>The guide list and the page registry drive both files, so a new guide cannot be published and forgotten.</td></tr>
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
{"".join(f'<tr><td>{c["week"]}</td><td>{esc(c["title"])}</td><td>{esc(c["status"])}{" &middot; " + esc(c["page"]) if c["page"] else ""}</td></tr>' for c in CADENCE["queue"])}
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
<h1>The topic calendar: eight questions, eight spec-backed answers</h1>
<p>Five guides are published; three are queued as working titles. Every title is an editorial hypothesis backed by verified listing fields - not a claim about search volume, popularity or product superiority. The next topic is chosen from measured queries, not instinct.</p>
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
page_to("topics.html","Topic calendar: eight spec-backed buyer questions | Countertop Guide","Eight question-shaped, spec-backed article working titles - five published, three queued - with the verified fields and sources each is built from.",topics_body)


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
<p class="fine">This page describes our practice; it is not legal advice. The Operating Agreement and the Program Policies govern, and were read on {VERIFIED}.</p>
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
page_to("guide-holiday-hosting.html", "The holiday hosting test: which air fryer feeds a crowd? | Countertop Guide", "Holiday hosting questions answered from verified Amazon listings: two dishes at once, rotisserie and pizza claims, counter-depth math and dated holiday-return observations.", b7, j7, "guide-page")

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
page_to("guide-gifts-by-budget.html", "Kitchen gifts under $25, $80 and $150: budget bands | Countertop Guide", "Holiday gift bands from five verified Amazon listings: who each pick is for, the listings' own gift claims quoted, and a gift-giver's checklist.", b8, j8, "guide-page")

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
page_to("guide-wattage-outlets.html", "Will it trip the breaker? Air fryer wattage and outlet math | Countertop Guide", "What 1000W vs 1700W means for a 120V kitchen circuit, the wattage conflict on the Chefman 8QT, and a checklist for verifying wattage on any listing.", b9, j9, "guide-page")

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

# ---------- REVIEW DESK ----------
desk_body = f"""
<p class="eyebrow">Review desk</p>
<h1>Everything internal, in one place</h1>
<p class="lede">This is the counter behind the counter: the register, the open questions, the flags, the method and the money rules. Reader-facing pages stay out of here on purpose - you will not find a row of status badges on the shop pages - but every one of these surfaces is reachable from the masthead&rsquo;s Review desk link and from the footer of every page.</p>
<div class="grid cols-2">
  <article class="card"><span class="tag">Evidence</span><h3><a href="verification.html">Verification register</a></h3><p>Line by line: submitted short link, intended ASIN, official listing URL, confirmation date and source, the observed redirect target in its own separate field, and every product fact with the link it came from.</p></article>
  <article class="card"><span class="tag">Open items</span><h3><a href="flagged.html">Flagged for review</a></h3><p>Every irregularity and unverified item, with the action that would close it. Flags never block publishing; they block claims.</p></article>
  <article class="card"><span class="tag">Decisions</span><h3><a href="suggestions.html">Suggestions &amp; decision desk</a></h3><p>Ranked suggestions with options, a copy-paste design brief, and the fourteen questions whose answers gate the next build.</p></article>
  <article class="card"><span class="tag">Money &amp; policy</span><h3><a href="compliance.html">Compliance gate</a></h3><p>Disclosure wording, sponsored marking, price and image rules read from the Operating Agreement and Program Policies.</p></article>
  <article class="card"><span class="tag">Measurement</span><h3><a href="methodology.html">Method, events &amp; ledger</a></h3><p>What is automated, what is gated, the five defined events, and an empty campaign ledger that only first-party reports may fill.</p></article>
  <article class="card"><span class="tag">Design</span><h3><a href="suggestions.html#design-inputs">Design inputs DI-1 to DI-8</a></h3><p>The eight inputs a parallel pass wrote for the design prompt, kept as a separate register on the board so the owner can approve, reject or defer each line before any CSS ships.</p></article>
  <article class="card"><span class="tag">Design</span><h3><a href="design-brief.html">Design brief (parallel pass)</a></h3><p>A second, independently written brief for the visual overhaul: prompt blocks, three visual directions and an eight-topic calendar. The owner picks one brief to execute - the choice is noted at the end of the decision desk.</p></article>
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
  "Holiday gifts guide (consolidated) | Countertop Guide",
  "This URL now points at the site's gift guide: five questions that predict whether a gifted air fryer stays on the counter, answered from verified listings.",
  "Holiday air fryer gifts"),
 ("guide-small-kitchen.html", "guide-cleanup-counter-space.html",
  "How to assess cleanup and counter-space trade-offs",
  "Small-kitchen fit guide (consolidated) | Countertop Guide",
  "This URL now points at the counter-space guide: counter depth, footprint arithmetic and cleanup, taken from the listings rather than estimated.",
  "Small kitchen, big appetite"),
 ("dashboard.html", "review-desk.html",
  "Review desk: every data surface in one place",
  "Dashboard hub (consolidated) | Countertop Guide",
  "This URL now points at the review desk: verification register, flag list, suggestions board, compliance, method and ledger, and both design briefs - one link each.",
  "Dashboard hub"),
 ("guide-holiday-roast.html", "guide-thermometer-accuracy.html",
  "Instant-read or wireless? How to read accuracy claims",
  "Roast-thermometer guide (consolidated) | Countertop Guide",
  "This URL now points at the thermometer accuracy guide: what a stated tolerance, a named certification and a sensor count each do and do not prove.",
  "Roast like a pro"),
]
for slug, target, dest, title, desc, h1 in MERGED:
    merged_body = f"""<p class="eyebrow">Consolidated</p>
<h1>{h1}</h1>
<p class="lede">This page moved. Its subject is covered in full on <a href="{target}">{dest}</a>, and keeping one answer per question is why.</p>
<div class="callout"><p>This URL was published earlier today as a separate guide by a parallel pass. Two pages answering the same question, at different lengths, is the classic way a small site starts to read like a content farm - and the earlier draft published dated price figures, which this site no longer does anywhere outside the <a href="verification.html">verification register</a> (see <a href="flagged.html#FLG-032">FLG-032</a>). So the shorter page was folded into the longer one rather than kept beside it.</p>
<p class="fine"><strong>What the destination covers:</strong> the same product facts, each linked to its Amazon listing and dated {VERIFIED}, with the arithmetic for the derived figures shown so you can repeat it.</p></div>
<p><a class="btn" href="{target}">Read the guide</a></p>
<p class="small">If the owner would rather this URL stay a standalone article, the earlier draft is in the repository history at <code>guide-holiday-gifts.html</code>, <code>guide-small-kitchen.html</code> or <code>guide-holiday-roast.html</code> as of <code>9e4b359</code>; restoring it is a one-line change plus removing the dated figures. Recorded as <a href="flagged.html#FLG-047">FLG-047</a>.</p>
"""
    page_to(slug, title, desc, merged_body, canonical=target)
print("consolidated pages wired:", len(MERGED))
# ---------- sitemap / feed / robots / search index ----------
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pg in PAGES:
    if pg["kind"] == "merged":
        continue
    sm.append(f"<url><loc>{esc(abs_url(pg['slug']))}</loc><lastmod>{VERIFIED}</lastmod></url>")
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
]
fd = ['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
      '<channel>', f'<title>{esc(BRAND)}</title>', f'<link>{esc(abs_url("index.html"))}</link>',
      '<description>Spec-backed air fryer and meat thermometer buying guides, written from the Amazon listing.</description>',
      f'<atom:link href="{esc(BASE)}/feed.xml" rel="self" type="application/rss+xml"/>',
      f'<lastBuildDate>{rfc(VERIFIED)}</lastBuildDate>']
for slug, t, d in GUIDES:
    u = esc(abs_url(slug))
    fd.append(f"<item><title>{esc(t)}</title><link>{u}</link><guid>{u}</guid><pubDate>{rfc(VERIFIED)}</pubDate><description>{esc(d)}</description></item>")
fd += ['</channel>','</rss>']
open("feed.xml","w").write("\n".join(fd) + "\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
idx = [{"title": p["title"].split(" | ")[0], "url": p["slug"], "text": p["description"]} for p in PAGES if p["kind"] not in ("admin", "merged")]
json.dump(idx, open("data/search-index.json","w"), indent=2)
SM_URLS = open("sitemap.xml").read().count("<url>")
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
