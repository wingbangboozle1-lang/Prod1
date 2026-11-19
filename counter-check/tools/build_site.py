#!/usr/bin/env python3
"""Build the static site in counter-check/site/ from the data/ files.

Every page is generated from data/*.json so the tables, flags and sources
stay in step. Run:  python3 tools/build_site.py
"""
import csv
import html
import json
import os
import shutil
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "site")

BASE = "https://wingbangboozle1-lang.github.io/Prod1/counter-check/site/"
SITE = "Counter Check"  # provisional brand, see flag P-12
TAG = "shopnow047c-20"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
NOT_ENDORSED = "This site is not endorsed by or affiliated with Amazon."
BUILD_DATE = "2026-11-19"


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


PRODUCTS = load("products.json")
SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
FLAGS = load("flags.json")["flags"]
FLAG_BY_ID = {f["id"]: f for f in FLAGS}
QUESTIONS = load("questions.json")["questions"]
SUGGESTIONS = load("suggestions.json")
GUIDES = load("guides.json")["guides"]
MEASURE = load("measurement.json")
with open(os.path.join(DATA, "ledger.csv"), encoding="utf-8") as f:
    LEDGER_ROWS = list(csv.DictReader(f))

CATEGORIES = {
    "air-fryers": {"title": "Air fryers", "slug": "shop/air-fryers.html",
                   "blurb": "Three listings: two basket-style air fryers and one French-door air fryer oven. Each row shows the title as Amazon lists it, the ASIN we intend, and the source."},
    "kitchen-thermometers": {"title": "Kitchen thermometers", "slug": "shop/kitchen-thermometers.html",
                             "blurb": "Two digital meat thermometers. Titles as listed; specifications were not captured in this pass."},
}


def esc(s):
    return html.escape(str(s), quote=True)


def page_url(path):
    return BASE if path == "index.html" else BASE + path


def rel(cur, target):
    """Relative href from page `cur` to site path `target` (both root-relative)."""
    cur_dir = os.path.dirname(cur)
    return os.path.relpath(target, cur_dir or ".").replace(os.sep, "/")


def sponsored(url, text, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{esc(url)}" rel="sponsored noopener" target="_blank"{c}>{esc(text)}</a>'


def link(cur, target, text, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{esc(rel(cur, target))}"{c}>{esc(text)}</a>'


# ---------- navigation ----------
PRIMARY_NAV = [
    ("shop/air-fryers.html", "Air fryers"),
    ("shop/kitchen-thermometers.html", "Thermometers"),
    ("guides/index.html", "Guides"),
    ("summary.html", "Executive summary"),
]
FOOTER_NAV = [
    ("index.html", "Home"),
    ("shop/air-fryers.html", "Air fryers"),
    ("shop/kitchen-thermometers.html", "Kitchen thermometers"),
    ("guides/index.html", "Guides"),
    ("summary.html", "Executive summary"),
    ("analysis.html", "Analysis and findings"),
    ("verification.html", "Verification and sources"),
    ("flagged.html", "Flagged for Review"),
    ("suggestions.html", "Suggestions for decision"),
    ("questions.html", "Questions and information gaps"),
    ("measurement.html", "Measurement"),
    ("policy.html", "Disclosure and policy gate"),
    ("feed.xml", "RSS feed"),
    ("sitemap.xml", "Sitemap"),
]


def shell(cur, title, desc, body, *, jsonld=None, canonical=None):
    nav_items = "".join(
        f'<li><a href="{esc(rel(cur, p))}">{esc(t)}</a></li>' for p, t in PRIMARY_NAV)
    home = rel(cur, "index.html")
    foot_items = "".join(
        f'<li><a href="{esc(rel(cur, p))}">{esc(t)}</a></li>' for p, t in FOOTER_NAV)
    canon = canonical or page_url(cur)
    ld = ""
    if jsonld:
        ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {SITE}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<link rel="alternate" type="application/rss+xml" title="{SITE} feed" href="{esc(rel(cur, 'feed.xml'))}">
<link rel="stylesheet" href="{esc(rel(cur, 'styles.css'))}">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="brand" href="{esc(home)}">{SITE}</a>
    <span class="tagline">Air fryers and meat thermometers, shown as the listings state them</span>
  </div>
  <nav class="primary" aria-label="Primary">
    <div class="wrap"><ul>{nav_items}</ul></div>
  </nav>
</header>
<div class="disclosure-strip" role="note">
  <div class="wrap"><strong>Disclosure:</strong> {esc(DISCLOSURE)} Some links on this site go to Amazon with our Associates tag. {esc(NOT_ENDORSED)}</div>
</div>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p class="disclosure-footer"><strong>Disclosure:</strong> {esc(DISCLOSURE)} {esc(NOT_ENDORSED)} Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates. Product titles are quoted as listed on Amazon; no Amazon images are reproduced.</p>
    <nav aria-label="Site sections"><ul class="footer-nav">{foot_items}</ul></nav>
    <p class="small">Last built {BUILD_DATE}. Prices and availability are not shown on this site; see the listing. Working-title guides make no popularity claims. Items marked <span class="pill unv">Unverified</span> are blank by design.</p>
  </div>
</footer>
</body>
</html>
"""


# ---------- components ----------
def source_link(cur, sid):
    s = SOURCES[sid]
    return f'<a class="cite" href="{esc(s["url"])}" rel="sponsored noopener" target="_blank">{esc(sid)}</a>'


def flag_pills(cur, ids):
    out = []
    for fid in ids:
        f = FLAG_BY_ID.get(fid)
        sev = f["severity"].lower() if f else "low"
        out.append(f'<a class="pill {sev}" href="{esc(rel(cur, "flagged.html"))}#{esc(fid)}">{esc(fid)}</a>')
    return " ".join(out)


def product_table(cur, category):
    rows = []
    for p in PRODUCTS["products"]:
        if p["category"] != category:
            continue
        cap = p["capacity_as_listed_in_title"] or "n/a"
        short = p["submitted_short_link"]
        observed = p["observed_redirect_target"]
        src_ids = {
            "B0CDY277D3": "S5", "B09B7SB46R": "S6", "B08DKYBTPH": "S7",
            "B0DHZTCNR5": "S8", "B0DZFD6R9Z": "S9"}
        sid = src_ids[p["intended_asin"]]
        short_sid = {
            "chefman-6qt-dual-basket": "S10", "emeril-26qt-french-door": "S11",
            "chefman-8qt-turbofry": "S12", "thermomaven-1sec-thermometer": "S13",
            "chef-iq-sense-gen3-thermometer": "S14"}[p["id"]]
        rows.append(f"""<tr>
  <td data-label="Product"><strong>{esc(p['name_short'])}</strong><br><span class="small">{esc(p['listing_title_as_listed'])}</span></td>
  <td data-label="Intended ASIN"><code>{esc(p['intended_asin'])}</code><br><span class="small">Pending owner confirmation <span class="pill low">P-03</span></span></td>
  <td data-label="Capacity (title)">{esc(cap)}</td>
  <td data-label="Dimensions"><span class="pill unv">Unverified</span> left blank <span class="pill low">P-07</span></td>
  <td data-label="Listing link">{sponsored(p['tagged_outbound_url'], 'View listing on Amazon', 'btn-small')}</td>
  <td data-label="Source">{source_link(cur, sid)} <span class="small">(listing)</span><br><span class="small">Submitted: <code>{esc(short)}</code></span></td>
  <td data-label="Confirmed">{esc(p['confirmation_date'])}</td>
  <td data-label="Observed redirect target"><code>{esc(observed)}</code><br><span class="small">Tag parameter present: no. Recorded as text, not as a buy link.</span></td>
  <td data-label="Flags">{flag_pills(cur, p['flags'])}</td>
</tr>""")
    return f"""<div class="table-wrap"><table class="data">
<thead><tr>
<th scope="col">Product (title as listed)</th>
<th scope="col">Intended ASIN</th>
<th scope="col">Capacity (title)</th>
<th scope="col">Dimensions</th>
<th scope="col">Listing</th>
<th scope="col">Source (official)</th>
<th scope="col">Confirmed</th>
<th scope="col">Observed redirect</th>
<th scope="col">Flags</th>
</tr></thead>
<tbody>
{''.join(rows)}
</tbody></table></div>"""


def product_cards(cur, category=None):
    cards = []
    for p in PRODUCTS["products"]:
        if category and p["category"] != category:
            continue
        cap = p["capacity_as_listed_in_title"]
        cat = CATEGORIES[p["category"]]["title"]
        cap_line = f'<p class="small">Capacity in title: {esc(cap)}</p>' if cap else ""
        cards.append(f"""<article class="card product">
  <p class="kicker">{esc(cat)}</p>
  <h3>{esc(p['name_short'])}</h3>
  <p class="small">{esc(p['listing_title_as_listed'])}</p>
  {cap_line}
  <p class="card-foot">{sponsored(p['tagged_outbound_url'], 'View on Amazon', 'btn')} <span class="small">ASIN {esc(p['intended_asin'])}</span></p>
</article>""")
    return f'<div class="grid">{"".join(cards)}</div>'


def guide_cards(cur):
    cards = []
    for g in GUIDES:
        cards.append(f"""<article class="card">
  <p class="kicker">Guide &middot; working title</p>
  <h3><a href="{esc(rel(cur, 'guides/' + g['slug'] + '.html'))}">{esc(g['title'])}</a></h3>
  <p>{esc(g['dek'])}</p>
</article>""")
    return f'<div class="grid">{"".join(cards)}</div>'


def flag_table(cur, ids=None):
    rows = []
    for f in FLAGS:
        if ids is not None and f["id"] not in ids:
            continue
        srcs = " ".join(source_link(cur, s) for s in f["sources"]) or "-"
        rows.append(f"""<tr id="{esc(f['id'])}">
<td data-label="ID"><strong>{esc(f['id'])}</strong></td>
<td data-label="Severity"><span class="pill {esc(f['severity'].lower())}">{esc(f['severity'])}</span></td>
<td data-label="Issue"><strong>{esc(f['issue'])}</strong><br><span class="small">{esc(f['detail'])}</span></td>
<td data-label="Sources">{srcs}</td>
<td data-label="Action requested">{esc(f['action'])}</td>
</tr>""")
    return f"""<div class="table-wrap"><table class="data">
<thead><tr><th>ID</th><th>Severity</th><th>Issue and detail</th><th>Source links</th><th>Action requested</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""


def source_table(cur):
    rows = []
    for s in SOURCES.values():
        rows.append(f"""<tr>
<td data-label="ID"><strong>{esc(s['id'])}</strong></td>
<td data-label="Source"><a class="cite" href="{esc(s['url'])}" target="_blank" rel="sponsored noopener">{esc(s['title'])}</a><br><span class="small">{esc(s['url'])}</span></td>
<td data-label="Used for">{esc(s['used_for'])}</td>
<td data-label="Checked">{esc(s['checked'])}</td>
<td data-label="Status">{esc(s['status'])}</td>
</tr>""")
    return f"""<div class="table-wrap"><table class="data">
<thead><tr><th>ID</th><th>Source (official where marked)</th><th>Used for</th><th>Checked</th><th>Status</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""


def count_status(qs):
    buckets = {}
    for q in qs:
        k = q["status"].split(":")[0].split(" (")[0].strip()
        buckets[k] = buckets.get(k, 0) + 1
    return buckets


# ---------- pages ----------
def build_index():
    cur = "index.html"
    body = f"""
<section class="hero">
  <p class="kicker">Front page &middot; {BUILD_DATE}</p>
  <h1>Five products from the owner's shortlist, laid out as the listings state them</h1>
  <p class="dek">Two categories, five Amazon listings. For each one: the title as listed, the ASIN we intend, the source, and the fields we could not verify. Nothing is ranked. No prices, ratings, or popularity claims appear on this site.</p>
  <p><a class="btn" href="{esc(rel(cur, 'shop/air-fryers.html'))}">Start with air fryers</a>
     <a class="btn alt" href="{esc(rel(cur, 'shop/kitchen-thermometers.html'))}">Thermometers</a></p>
</section>

<section>
  <h2>Shop the listings</h2>
  {product_cards(cur)}
</section>

<section>
  <h2>Guides</h2>
  <p class="small">Working-title guides that ask what to compare, not which to buy.</p>
  {guide_cards(cur)}
</section>

<section class="panel">
  <h2>Behind the picks</h2>
  <ul class="plain">
    <li>{link(cur, 'analysis.html', 'Analysis and findings')}: counts and what they do and do not show.</li>
    <li>{link(cur, 'verification.html', 'Verification and sources')}: every source with the date it was read.</li>
    <li>{link(cur, 'flagged.html', 'Flagged for Review')}: irregularities and unverified items, for owner review.</li>
    <li>{link(cur, 'suggestions.html', 'Suggestions for decision')}: options to choose from before anything changes.</li>
    <li>{link(cur, 'summary.html', 'Executive summary')}: the one-page version.</li>
  </ul>
</section>
"""
    jsonld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": BASE,
              "description": "Air fryer and meat thermometer listings with sources, flags and disclosures."}
    return shell(cur, f"{SITE}: air fryers and meat thermometers",
                 "Five Amazon listings in two categories, with the title as listed, the ASIN, the official source, and every unverified field flagged.",
                 body, jsonld=jsonld, canonical=BASE)


def build_category(path, key):
    cur = path
    c = CATEGORIES[key]
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; {esc(c['title'])}</p>
<h1>{esc(c['title'])}</h1>
<p class="dek">{esc(c['blurb'])}</p>
<section>
  {product_cards(cur, key)}
</section>
<section>
  <h2>Listing table</h2>
  <p class="small">Each row links to its official Amazon listing. Blank or unverified cells are marked. The short-link column shows the link as submitted; the observed target is recorded separately and carries no tag parameter.</p>
  {product_table(cur, key)}
</section>
<section class="panel">
  <h2>What this table does not show</h2>
  <ul class="plain">
    <li>Prices and availability: withheld (flag P-05).</li>
    <li>Star ratings and review counts: withheld (flag P-05).</li>
    <li>Commission rates per product: not confirmed (flag P-06).</li>
    <li>Dimensions: left blank as unverified (flag P-07).</li>
  </ul>
</section>
"""
    return shell(cur, c["title"], c["blurb"], body)


def build_guides_index():
    cur = "guides/index.html"
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Guides</p>
<h1>Guides</h1>
<p class="dek">Question-shaped guides. Titles are working titles chosen as editorial hypotheses. The next topic will be chosen from measured reader questions once measurement is live.</p>
{guide_cards(cur)}
"""
    return shell(cur, "Guides", "Question-shaped guides on comparing air fryers and kitchen appliances, with what each guide does not claim.", body)


def build_guide(g):
    cur = f"guides/{g['slug']}.html"
    parts = []
    for s in g["sections"]:
        parts.append(f"<h2>{esc(s['heading'])}</h2>")
        for p in s.get("paras", []):
            parts.append(f"<p>{esc(p)}</p>")
        if s.get("list"):
            parts.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in s["list"]) + "</ul>")
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; {link(cur, 'guides/index.html', 'Guides')} &rsaquo; Guide</p>
<article class="prose">
<p class="kicker">Guide &middot; working title &middot; {esc(g['date'])}</p>
<h1>{esc(g['title'])}</h1>
<p class="dek">{esc(g['dek'])}</p>
<p class="byline">By the Editorial team <span class="small">(no named author; see flag P-13)</span></p>
{''.join(parts)}
<h2>Products in our table</h2>
<p>See {link(cur, 'shop/air-fryers.html', 'air fryers')} or {link(cur, 'shop/kitchen-thermometers.html', 'kitchen thermometers')} for the listing rows, sources and flags.</p>
</article>"""
    jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"],
              "datePublished": g["date"], "dateModified": g["date"],
              "author": {"@type": "Organization", "name": "Editorial team"},
              "publisher": {"@type": "Organization", "name": SITE},
              "mainEntityOfPage": page_url(cur)}
    return shell(cur, g["title"], g["dek"], body, jsonld=jsonld, canonical=page_url(cur))


def build_summary():
    cur = "summary.html"
    n_products = len(PRODUCTS["products"])
    n_open = sum(1 for f in FLAGS if f["severity"] in ("High", "Medium"))
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Executive summary</p>
<h1>Executive summary</h1>
<p class="dek">What the site is, what has been verified, what has not, and what the owner needs to decide.</p>
<section class="panel">
<h2>What was built</h2>
<ul>
<li>A static site of {n_products} product listings in two categories, four question-shaped guides, and pages for analysis, sources, flags, suggestions, questions, measurement and policy. All are linked from the footer.</li>
<li>Every product row links to its official Amazon listing. Every outbound product link carries the tracking ID <code>{TAG}</code> and <code>rel="sponsored"</code>.</li>
<li>The disclosure required by Associates Operating Agreement section 5 appears under the masthead of every page and again in the footer.</li>
<li>A build script and a gate (tools/check_site.py) regenerate the site from the data files and fail the build on a missing disclosure, a sponsored-link error, or a broken internal link.</li>
</ul>
</section>
<section>
<h2>What has been verified</h2>
<ul>
<li>The five submitted short links each resolve to one Amazon listing (ASINs B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z), checked 2026-11-19.</li>
<li>None of the five resolved URLs carries a <code>tag=</code> parameter. This matches the earlier Zone4 audit (S15, context only).</li>
<li>Associates Operating Agreement section 5 wording and Participation Requirements section 2(a)-(b) were read directly (S1, S2). Google's sponsored-link guidance (S3) and FTC placement guidance (S4) were read.</li>
</ul>
</section>
<section>
<h2>What is not verified, and why</h2>
<ul>
<li><strong>Tracking ID status.</strong> The ID was supplied; it has not been confirmed as the enrolled Partner Tag (P-01).</li>
<li><strong>Special Links.</strong> The one-link-per-product test in Associates Central has not been run (P-02).</li>
<li><strong>Intended ASINs.</strong> Read from the resolved listings; the owner has not confirmed them (P-03).</li>
<li><strong>Prices, availability, ratings.</strong> Not shown; the policy limits them (P-05).</li>
<li><strong>Commission rates and earnings.</strong> Not shown; the per-ASIN category is unknown (P-06).</li>
<li><strong>Analytics and conversions.</strong> Not measured. GitHub Pages cannot host the requested endpoint (P-10). No conversion score or revenue forecast is made.</li>
<li><strong>Trends and popularity.</strong> No claim is made; no dated first-party data exists (P-19).</li>
</ul>
</section>
<section class="panel">
<h2>Decisions the owner needs to make</h2>
<p>{len(SUGGESTIONS['suggestions'])} suggestions are listed on the {link(cur, 'suggestions.html', 'suggestions page')} with options and a recommended choice. The first two (confirm the Partner Tag; run one Special Link test per product) block any commission reporting.</p>
<p>{n_open} flags rated High or Medium are on the {link(cur, 'flagged.html', 'Flagged for Review page')}, with source links.</p>
</section>
<section>
<h2>Sources</h2>
<p>The full register, with the date each source was read, is on the {link(cur, 'verification.html', 'verification page')}.</p>
</section>
"""
    return shell(cur, "Executive summary", "Executive summary: what was built, what is verified, what is not, and the decisions the owner needs to make.", body)


def build_analysis():
    cur = "analysis.html"
    counts = {}
    for p in PRODUCTS["products"]:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    tag_present = sum(1 for p in PRODUCTS["products"] if p["observed_redirect_has_tag_param"])
    dims_blank = sum(1 for p in PRODUCTS["products"] if not p["dimensions_as_listed"])
    sev = {}
    for f in FLAGS:
        sev[f["severity"]] = sev.get(f["severity"], 0) + 1
    qc = count_status(QUESTIONS)
    qrows = "".join(f"<tr><td>{esc(k)}</td><td>{v}</td></tr>" for k, v in qc.items())
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Analysis</p>
<h1>Analysis and findings</h1>
<p class="dek">Counts from the data files, and what they do and do not show. No conversion score, revenue forecast, or ranking is produced.</p>
<section>
<h2>Counts</h2>
<div class="table-wrap"><table class="data">
<thead><tr><th>Measure</th><th>Value</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Product listings, air fryers</td><td>{counts.get('air-fryers', 0)}</td><td>{source_link(cur, 'S5')}, {source_link(cur, 'S6')}, {source_link(cur, 'S7')}</td></tr>
<tr><td>Product listings, kitchen thermometers</td><td>{counts.get('kitchen-thermometers', 0)}</td><td>{source_link(cur, 'S8')}, {source_link(cur, 'S9')}</td></tr>
<tr><td>Submitted short links that resolved to a listing</td><td>{len(PRODUCTS['products'])} of {len(PRODUCTS['products'])}</td><td>{source_link(cur, 'S10')} to {source_link(cur, 'S14')}</td></tr>
<tr><td>Resolved links containing a tag= parameter</td><td>{tag_present} of {len(PRODUCTS['products'])}</td><td>{source_link(cur, 'S10')} to {source_link(cur, 'S14')}</td></tr>
<tr><td>Listings with dimensions verified</td><td>{len(PRODUCTS['products']) - dims_blank} of {len(PRODUCTS['products'])}</td><td>Not captured (P-07)</td></tr>
<tr><td>Prices or ratings shown</td><td>0 (withheld by policy)</td><td>{source_link(cur, 'S2')}</td></tr>
<tr><td>Flags: High / Medium / Low</td><td>{sev.get('High', 0)} / {sev.get('Medium', 0)} / {sev.get('Low', 0)}</td><td><a href="{esc(rel(cur, 'flagged.html'))}">Flagged for Review</a></td></tr>
</tbody></table></div>
</section>
<section>
<h2>Findings</h2>
<ol>
<li><strong>The five submitted links point to five different listings:</strong> three air fryers and two thermometers. The short-link codes are not ASINs, so each intended ASIN is read from the resolved URL (P-03).</li>
<li><strong>No resolved link carries the tag.</strong> The site therefore links to tagged listing URLs in the format Associates describes, and keeps the observed targets in their own column (P-02, P-04).</li>
<li><strong>The 8 Qt link opens a variation page.</strong> The resolved URL includes <code>th=1</code>; the other size options were not checked (P-08).</li>
<li><strong>Units in titles differ.</strong> Two titles use Quart, one uses QT. Units are not converted (P-07).</li>
<li><strong>Price and rating analysis cannot appear on a static site under the current policy.</strong> The owner must choose between API access and price-free listings (P-05).</li>
</ol>
</section>
<section>
<h2>Open questions</h2>
<p>Counts of the {len(QUESTIONS)} questions by status. The full list is on the {link(cur, 'questions.html', 'questions page')}.</p>
<div class="table-wrap"><table class="data"><thead><tr><th>Status</th><th>Questions</th></tr></thead><tbody>{qrows}</tbody></table></div>
</section>
"""
    return shell(cur, "Analysis and findings", "Counts and findings from the product data, with what they do and do not show.", body)


def build_verification():
    cur = "verification.html"
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Verification</p>
<h1>Verification and sources</h1>
<p class="dek">Every source the site relies on, with the date it was read. Where a value could not be confirmed from an official source, it is left blank and flagged. Nothing is inferred.</p>
<section>
<h2>Source register</h2>
{source_table(cur)}
</section>
<section>
<h2>Verification log (session 2026-11-19)</h2>
<ul>
<li>Resolved each of the five submitted short links; recorded the observed target in its own field; confirmed no tag= parameter in any.</li>
<li>Read the listing header and title for each of the five ASINs. Captured titles verbatim with the ASIN. Did not capture specification tables or prices.</li>
<li>Read Associates Operating Agreement section 5 (disclosure wording) and Participation Requirements section 2 (tag and price display rules).</li>
<li>Read Google's rel="sponsored" guidance and the FTC disclosure brochure.</li>
<li>Did not access Associates Central, any tracking report, or Search Console.</li>
<li>Re-read the Zone4 flagged page for context only; its items were not re-verified in full.</li>
</ul>
</section>
"""
    return shell(cur, "Verification and sources", "Source register with read dates, verification log, and what could not be checked.", body)


def build_flagged():
    cur = "flagged.html"
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Flagged for Review</p>
<h1>Flagged for Review</h1>
<p class="dek">Irregularities and unverified items, with source links. They do not block publication. They are listed here so the owner can review them and request changes.</p>
<section class="panel">
<h2>Unverified fields left blank</h2>
<ul class="plain">
<li>Dimensions for all five listings (P-07).</li>
<li>Commission category and rate for all five (P-06).</li>
<li>Prices, availability and star ratings for all five, withheld by policy (P-05).</li>
<li>Owner confirmation of intended ASINs (P-03).</li>
</ul>
</section>
<section>
<h2>All flags</h2>
{flag_table(cur)}
</section>
"""
    return shell(cur, "Flagged for Review", "Flagged for Review: irregularities and unverified items with source links and requested actions.", body)


def build_suggestions():
    cur = "suggestions.html"
    rows = []
    for s in SUGGESTIONS["suggestions"]:
        opts = "<br>".join(esc(o) for o in s["options"])
        rec = esc(s["recommendation"])
        blocks = ", ".join(s.get("blocks", [])) or "-"
        rows.append(f"""<tr>
<td data-label="ID"><strong>{esc(s['id'])}</strong><br><span class="small">{esc(s['area'])}</span></td>
<td data-label="Suggestion">{esc(s['suggestion'])}</td>
<td data-label="Options">{opts}</td>
<td data-label="Recommended">{rec}</td>
<td data-label="Blocks">{esc(blocks)}</td>
<td data-label="Status"><span class="pill med">{esc(s['status'])}</span></td>
</tr>""")
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Suggestions</p>
<h1>Suggestions for decision</h1>
<p class="dek">Choose the best path before anything changes. Each suggestion lists its options and a recommended choice. Nothing here has been implemented, except the site itself as described on the executive summary.</p>
<div class="table-wrap"><table class="data">
<thead><tr><th>ID</th><th>Suggestion</th><th>Options</th><th>Recommended</th><th>Blocks</th><th>Status</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="small">Blocks lists the questions or flags a choice would resolve. Questions are on the {link(cur, 'questions.html', 'questions page')}.</p>
"""
    return shell(cur, "Suggestions for decision", "Options and recommendations for the owner to choose from before any change.", body)


def build_questions():
    cur = "questions.html"
    rows = []
    for q in QUESTIONS:
        fl = flag_pills(cur, q["flags"]) if q["flags"] else "-"
        rows.append(f"""<tr>
<td data-label="ID"><strong>{esc(q['id'])}</strong></td>
<td data-label="Question">{esc(q['question'])}</td>
<td data-label="Status">{esc(q['status'])}</td>
<td data-label="Evidence">{esc(q['evidence'])}</td>
<td data-label="Needed">{esc(q['needed'])}</td>
<td data-label="Flags">{fl}</td>
</tr>""")
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Questions</p>
<h1>Questions and information gaps</h1>
<p class="dek">What must be answered before a decision can reasonably be made, based on what this repository already holds and what it does not.</p>
<div class="table-wrap"><table class="data">
<thead><tr><th>ID</th><th>Question</th><th>Status</th><th>Evidence</th><th>Still needed</th><th>Flags</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
"""
    return shell(cur, "Questions and information gaps", "Questions that must be answered before decisions, with the evidence held and the information still needed.", body)


def build_measurement():
    cur = "measurement.html"
    ev = "".join(f"<tr><td>{esc(e['id'])}</td><td><code>{esc(e['name'])}</code></td><td>{esc(e['fires_when'])}</td><td>{esc(e['destination'])}</td></tr>" for e in MEASURE["proposed_events"])
    cols = MEASURE["ledger_columns"]
    head = "".join(f"<th>{esc(c)}</th>" for c in cols)
    ledger_rows = "".join("<tr>" + "".join(f"<td>{esc(r.get(c, ''))}</td>" for c in cols) + "</tr>" for r in LEDGER_ROWS)
    if not ledger_rows:
        ledger_rows = f'<tr><td colspan="{len(cols)}">No rows yet. Rows are added only from authorized first-party reports.</td></tr>'
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Measurement</p>
<h1>Measurement</h1>
<p class="dek">{esc(MEASURE['status'])} This page holds the proposed events, the campaign ledger, and the rule for adding data.</p>
<section class="panel">
<h2>Proposed events</h2>
<p class="small">The brief asks for five defined events but does not list them, so this list is a proposal awaiting approval (flag P-11, suggestion SG-04).</p>
<div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Event</th><th>Fires when</th><th>Destination</th></tr></thead><tbody>{ev}</tbody></table></div>
</section>
<section>
<h2>Campaign ledger</h2>
<p>{esc(MEASURE['ledger_rule'])}</p>
<div class="table-wrap"><table class="data"><thead><tr>{head}</tr></thead><tbody>{ledger_rows}</tbody></table></div>
</section>
"""
    return shell(cur, "Measurement", "Proposed analytics events and the campaign ledger, with the rule for adding data.", body)


def build_policy():
    cur = "policy.html"
    body = f"""
<p class="crumb">{link(cur, 'index.html', 'Home')} &rsaquo; Disclosure and policy gate</p>
<h1>Disclosure and policy gate</h1>
<p class="dek">The checks applied to every page before publication, and the policy text they rely on.</p>
<section class="panel">
<h2>Required disclosure (verbatim)</h2>
<blockquote>“As an Amazon Associate I earn from qualifying purchases.”</blockquote>
<p class="small">Source: {source_link(cur, 'S1')}, section 5. The site shows it under the masthead of every page and again in the footer.</p>
</section>
<section>
<h2>Gate checks</h2>
<div class="table-wrap"><table class="data">
<thead><tr><th>Check</th><th>Rule and source</th><th>How it is enforced</th></tr></thead>
<tbody>
<tr><td>Disclosure above the fold</td><td>Section 5 “clearly and prominently” (S1). FTC: hard to miss, placed with the endorsement (S4).</td><td>tools/check_site.py fails the build if the disclosure is not under the masthead of any page.</td></tr>
<tr><td>Tag in every product link</td><td>Participation Requirements 2(b): Associates ID as a URL parameter (S2).</td><td>Build checks every amazon.com product link has <code>tag={TAG}</code>.</td></tr>
<tr><td>Sponsored attribute</td><td>Google: rel="sponsored" for paid links (S3).</td><td>Build checks every Amazon link has rel containing "sponsored".</td></tr>
<tr><td>No prices or ratings</td><td>Participation Requirements 2(b) (S2).</td><td>Build fails if a currency amount appears on a product or guide page.</td></tr>
<tr><td>Every table row sourced</td><td>Brief: every row needs an official source link.</td><td>Build checks each product row links to an amazon.com listing.</td></tr>
<tr><td>No broken internal links</td><td>Brief: no broken links before publish.</td><td>Build checks every relative link resolves to a generated file.</td></tr>
</tbody></table></div>
</section>
<section class="panel">
<h2>Citations to Amazon</h2>
<p>Links to Amazon listings that appear in source columns are citations to the official listing, not buy links. They are marked sponsored too, and no untagged Amazon URL is offered as a buy link.</p>
</section>
<section class="panel">
<h2>Not yet verified</h2>
<p>The Amazon IP License notice wording and Participation Requirements 6(t) were not re-read this session. Until they are, no notice text is published and no rating is shown (flags P-05, P-09).</p>
</section>
"""
    return shell(cur, "Disclosure and policy gate", "Required disclosure, the gate checks applied before publication, and what is not yet verified.", body)


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def build_feed_and_sitemap(pages):
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for g in GUIDES:
        url = page_url(f"guides/{g['slug']}.html")
        d = datetime.strptime(g["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")
        items.append(f"""<item><title>{esc(g['title'])}</title><link>{esc(url)}</link><guid isPermaLink="true">{esc(url)}</guid><pubDate>{d}</pubDate><description>{esc(g['dek'])}</description></item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>{SITE}</title><link>{BASE}</link><description>Guides on comparing air fryers and kitchen thermometers. {esc(DISCLOSURE)}</description>
<language>en-us</language><lastBuildDate>{now}</lastBuildDate>
{''.join(items)}
</channel></rss>
"""
    write("feed.xml", feed)
    urls = "".join(f"<url><loc>{esc(page_url(p))}</loc><lastmod>{BUILD_DATE}</lastmod></url>" for p in pages)
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">{urls}</urlset>
""")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")


CSS = """
:root{--ink:#1d1d1b;--muted:#5b5b56;--paper:#fbfaf6;--rule:#dedbd2;--accent:#7a3e1d;--accent2:#2f5d50;--warn:#fff4cf;--warnline:#c9a227;--chip:#efece4}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:17px/1.6 Georgia,"Iowan Old Style","Times New Roman",serif;color:var(--ink);background:var(--paper)}
h1,h2,h3,.brand,.kicker,nav,.btn,th,.pill{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
h1{font-size:clamp(1.8rem,4vw,2.6rem);line-height:1.15;margin:.3em 0 .4em}
h2{font-size:1.35rem;margin:1.6em 0 .5em;border-top:1px solid var(--rule);padding-top:.8em}
h3{font-size:1.05rem;margin:.2em 0}
a{color:var(--accent2)}
a:focus-visible,.btn:focus-visible{outline:3px solid #f0a500;outline-offset:2px}
.wrap{max-width:1080px;margin:0 auto;padding:0 18px}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:8px;background:#fff;padding:6px 10px;z-index:9}
.masthead{border-bottom:3px double var(--ink);background:#fff}
.masthead-row{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px;padding-top:14px;padding-bottom:8px}
.brand{font-size:1.6rem;font-weight:800;color:var(--ink);text-decoration:none;letter-spacing:-.02em}
.tagline{color:var(--muted);font-size:.9rem;font-family:-apple-system,Segoe UI,Arial,sans-serif}
.primary ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 18px;padding:8px 0}
.primary a{text-decoration:none;color:var(--ink);font:600 .95rem -apple-system,Segoe UI,Arial,sans-serif;padding:4px 0;display:inline-block;min-height:32px}
.primary a:hover{color:var(--accent);text-decoration:underline}
.disclosure-strip{background:var(--warn);border-bottom:1px solid var(--warnline);font:.92rem/1.45 -apple-system,Segoe UI,Arial,sans-serif;padding:10px 0}
main{padding-top:14px;padding-bottom:30px;min-height:60vh}
section{margin:18px 0}
.hero{padding:10px 0 4px}
.dek{font-size:1.12rem;color:var(--muted);max-width:760px}
.kicker{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin:0 0 .3em;font-weight:700}
.crumb{font:.88rem -apple-system,Segoe UI,Arial,sans-serif;color:var(--muted);margin:6px 0 0}
.small{font-size:.86rem;color:var(--muted);font-family:-apple-system,Segoe UI,Arial,sans-serif}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:12px 0}
.card{background:#fff;border:1px solid var(--rule);border-radius:10px;padding:16px 16px 14px}
.card p{margin:.4em 0}
.card-foot{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;margin-top:12px!important}
.btn{display:inline-block;background:var(--accent);color:#fff!important;padding:9px 14px;border-radius:7px;text-decoration:none;font-weight:700;font-size:.95rem;min-height:40px;line-height:22px}
.btn.alt{background:#fff;color:var(--accent)!important;border:1px solid var(--accent)}
.btn-small{display:inline-block;background:var(--accent);color:#fff!important;padding:6px 10px;border-radius:6px;text-decoration:none;font:700 .85rem -apple-system,Segoe UI,Arial,sans-serif;white-space:nowrap}
.small-link{font-size:.85rem}
.panel{background:#fff;border:1px solid var(--rule);border-radius:10px;padding:14px 18px}
.plain{list-style:none;padding:0}.plain li{margin:.45em 0}
.table-wrap{overflow-x:auto;background:#fff;border:1px solid var(--rule);border-radius:10px}
table.data{border-collapse:collapse;width:100%;font-size:.92rem;min-width:720px}
table.data th,table.data td{padding:9px 10px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top}
table.data th{background:var(--chip);font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:#3a3a36}
table.data tr:last-child td{border-bottom:0}
code{font:.88em ui-monospace,Menlo,Consolas,monospace;background:var(--chip);padding:1px 4px;border-radius:4px;word-break:break-all}
.pill{display:inline-block;font:700 .72rem -apple-system,Segoe UI,Arial,sans-serif;padding:2px 7px;border-radius:999px;background:var(--chip);color:var(--ink);text-decoration:none;margin:1px 2px 1px 0;border:1px solid transparent;white-space:nowrap}
.pill.high{background:#f7d4cc;color:#6a1c0c}.pill.medium,.pill.med{background:#fbe8b5;color:#5c4305}.pill.low{background:#dfeee9;color:#1f4a3e}
.pill.unv{background:#ececec;color:#444;border-color:#bbb}
blockquote{margin:.4em 0;padding:.5em 1em;border-left:4px solid var(--accent);background:#fff;font-size:1.05rem}
.prose{max-width:720px}
.prose p,.prose li{font-size:1.04rem}
.byline{font:.9rem -apple-system,Segoe UI,Arial,sans-serif;color:var(--muted)}
.site-footer{background:#23231f;color:#e9e6dd;padding:22px 0;font-size:.93rem}
.site-footer a{color:#f3d9a4}
.site-footer .disclosure-footer{margin-top:0}
.site-footer .small{color:#c8c4b8}
.footer-nav{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:6px 16px;margin:12px 0}
.footer-nav a{font:.9rem -apple-system,Segoe UI,Arial,sans-serif}
@media (max-width:640px){
  table.data{min-width:0}
  table.data thead{display:none}
  table.data,table.data tbody,table.data tr,table.data td{display:block;width:100%}
  table.data tr{border-bottom:1px solid var(--rule);padding:8px 10px}
  table.data td{border:0;padding:4px 0}
  table.data td::before{content:attr(data-label);display:block;font:700 .72rem -apple-system,Segoe UI,Arial,sans-serif;text-transform:uppercase;color:var(--muted)}
  .table-wrap{overflow:visible;border:0;background:none}
  .btn,.btn-small{min-height:44px;display:inline-flex;align-items:center}
}
"""


def main():
    if os.path.isdir(OUT):
        for entry in os.listdir(OUT):
            if entry in (".nojekyll",):
                continue
            p = os.path.join(OUT, entry)
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    write("styles.css", CSS)

    pages = {}
    pages["index.html"] = build_index()
    pages["shop/air-fryers.html"] = build_category("shop/air-fryers.html", "air-fryers")
    pages["shop/kitchen-thermometers.html"] = build_category("shop/kitchen-thermometers.html", "kitchen-thermometers")
    pages["guides/index.html"] = build_guides_index()
    for g in GUIDES:
        pages[f"guides/{g['slug']}.html"] = build_guide(g)
    pages["summary.html"] = build_summary()
    pages["analysis.html"] = build_analysis()
    pages["verification.html"] = build_verification()
    pages["flagged.html"] = build_flagged()
    pages["suggestions.html"] = build_suggestions()
    pages["questions.html"] = build_questions()
    pages["measurement.html"] = build_measurement()
    pages["policy.html"] = build_policy()
    for path, content in pages.items():
        write(path, content)
    build_feed_and_sitemap(list(pages.keys()))
    print(f"Built {len(pages)} HTML pages, feed, sitemap and robots.txt into site/")


if __name__ == "__main__":
    main()
