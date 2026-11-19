#!/usr/bin/env python3
"""Build the static site from data/, content/ and site_src/ into docs/ (GitHub Pages source).

Standard library only. Run:  python3 tools/build.py && python3 tools/check.py
"""
import email.utils
import html
import json
import pathlib
import shutil
import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTENT = ROOT / "content"
SRC = ROOT / "site_src"
OUT = ROOT / "docs"

SITE_NAME = "Counter Notes"          # working name, see Q-04 / F-08
SITE_BASE = "https://wingbangboozle1-lang.github.io/Prod1"
TODAY = "2026-11-19"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
NOT_ENDORSED = "This site is not endorsed by or affiliated with Amazon."
# Left empty on purpose: no analytics endpoint is hosted (see F-07 and the analytics page).
TRACKER_ENDPOINT = ""
REPO_URL = "https://github.com/wingbangboozle1-lang/Prod1"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def e(value):
    return html.escape(str(value), quote=True)


PRODUCTS = load("products.json")["products"]
CATS = {c["slug"]: c for c in load("categories.json")["categories"]}
GUIDES = load("guides.json")["guides"]
SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
FLAGS = load("flags.json")["flags"]
QUESTIONS = load("questions.json")["questions"]
SUGG = load("suggestions.json")
REGISTER = load("register.json")
PROD_BY_ID = {p["id"]: p for p in PRODUCTS}

NAV = [
    ("products/", "Products"),
    ("guides/", "Guides"),
    ("analysis/", "Analysis"),
    ("questions/", "Questions"),
    ("suggestions/", "Suggestions"),
    ("flagged/", "Flagged for Review"),
    ("executive-summary/", "Executive summary"),
]

FOOTER = [
    ("Shop", [
        ("products/", "All products"),
        ("categories/air-fryers/", "Air fryers"),
        ("categories/multi-function-ovens/", "Multi-function ovens"),
        ("categories/meat-thermometers/", "Meat thermometers"),
    ]),
    ("Guides", [("guides/", "All guides")] + [(f"guides/{g['slug']}/", g["title"]) for g in GUIDES]),
    ("Dashboards", [
        ("analysis/", "Analysis"),
        ("register/", "Backlog register"),
        ("intent-records/", "Product-intent records"),
        ("questions/", "Open questions"),
        ("suggestions/", "Suggestions (awaiting choice)"),
        ("ledger/", "Campaign ledger"),
        ("analytics/", "Analytics and measurement"),
        ("flagged/", "Flagged for Review"),
        ("executive-summary/", "Executive summary"),
    ]),
    ("Site", [
        ("about/", "About and editorial standard"),
        ("feed.xml", "RSS feed"),
        ("sitemap.xml", "Sitemap"),
        ("ledger.csv", "Ledger CSV (header only)"),
    ]),
]

PAGES = []  # dicts: path, title, desc, fn, active, jsonld, sitemap


def page(path, title, desc, active="", jsonld=None, sitemap=True):
    def wrap(fn):
        PAGES.append(dict(path=path, title=title, desc=desc, fn=fn, active=active, jsonld=jsonld, sitemap=sitemap))
        return fn
    return wrap


def rel_prefix(path):
    return "../" * path.count("/")


def shell(p):
    R = rel_prefix(p["path"])
    canonical = f"{SITE_BASE}/{p['path']}" if not p["path"].endswith("index.html") else f"{SITE_BASE}/{p['path'][:-len('index.html')]}"
    if p["path"] == "404.html":
        canonical = f"{SITE_BASE}/404.html"
    title_full = f"{p['title']} · {SITE_NAME}" if p["path"] != "index.html" else f"{SITE_NAME}: {p['title']}"
    nav = "".join(
        f'<li><a href="{R}{href}"' + (' aria-current="page"' if href == p["active"] else "") + f">{e(label)}</a></li>"
        for href, label in NAV
    )
    footer_cols = "".join(
        f'<div><h2>{e(group)}</h2><ul>' + "".join(
            f'<li><a href="{R}{href}"' + (' data-event="feed_subscribe_click"' if href == "feed.xml" else "") + f">{e(label)}</a></li>"
            for href, label in links
        ) + "</ul></div>"
        for group, links in FOOTER
    )
    jsonld = f'<script type="application/ld+json">{json.dumps(p["jsonld"], ensure_ascii=False)}</script>' if p["jsonld"] else ""
    body = p["fn"](R)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title_full)}</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE_NAME)}">
<meta property="og:title" content="{e(title_full)}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{e(canonical)}">
<meta name="analytics-endpoint" content="{e(TRACKER_ENDPOINT)}">
<link rel="stylesheet" href="{R}assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{e(SITE_NAME)} guides" href="{SITE_BASE}/feed.xml">
{jsonld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="wrap">
<div class="row"><a class="brand" href="{R}">{e(SITE_NAME)}</a><p class="tagline">Air fryers and meat thermometers, sorted by the questions to settle first</p></div>
<nav class="primary" aria-label="Main"><ul>{nav}</ul></nav>
</div></header>
<div class="disclosure" role="note"><div class="wrap"><p><strong>Disclosure:</strong> {e(DISCLOSURE)} {e(NOT_ENDORSED)} Prices and availability are not shown here; check the listing.</p></div></div>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
<div class="disclosure disc"><strong>Disclosure:</strong> {e(DISCLOSURE)} {e(NOT_ENDORSED)}</div>
<div class="foot-grid">{footer_cols}</div>
<p class="small" style="margin-top:20px">Working name. Last reviewed {TODAY}. Every fact is taken from the source named on the page; anything not confirmed is marked UNVERIFIED. Repository: <a href="{REPO_URL}">{REPO_URL.replace('https://', '')}</a></p>
</div></footer>
<script src="{R}assets/track.js" defer></script>
</body>
</html>
"""


def ext(url, label=None, product=None):
    """Outbound link. Every Amazon or outbound product link is sponsored."""
    attrs = f' href="{e(url)}" rel="sponsored noopener" target="_blank"'
    if product:
        attrs += f' data-event="outbound_click" data-product="{e(product)}"'
    return f"<a{attrs}>{e(label or url)}</a>"


def outlink(url, label):
    """Plain source link; Amazon hosts are paid-relationship links, so they are sponsored."""
    rel = "sponsored noopener" if "amazon.com" in url else "noopener"
    return f'<a href="{e(url)}" rel="{rel}" target="_blank">{e(label)}</a>'


def src_link(src_id):
    s = SOURCES[src_id]
    return outlink(s["url"], s["label"])


def product_card(p, R):
    specs = "".join(f"<li>{e(s)}</li>" for s in p["title_stated_specs"][:4])
    return f"""<article class="card">
<p class="kicker" style="margin:0">{e(CATS[p['category']]['name'])}</p>
<h3>{e(p['display_name'])}</h3>
<p class="meta">Observed ASIN <code>{e(p['observed_asin'])}</code> · intended ASIN <span class="unverified">UNVERIFIED</span></p>
<p class="meta">The listing title states:</p>
<ul class="specs">{specs}</ul>
<div class="actions">
{ext(p['supplied_link'], 'View on Amazon', p['id']).replace('<a ', '<a class="btn" ', 1)}
<a class="btn ghost" href="{R}products/#{e(p['id'])}">Source row</a>
</div></article>"""


def guide_card(g, R):
    return f"""<article class="card">
<p class="kicker" style="margin:0">{e(CATS[g['category']]['name'])}</p>
<h3><a href="{R}guides/{e(g['slug'])}/" style="text-decoration:none;color:inherit">{e(g['title'])}</a></h3>
<p class="meta">{e(g['description'])}</p>
<div class="actions"><a class="btn ghost" href="{R}guides/{e(g['slug'])}/">Read the guide</a></div>
</article>"""


def product_rows(R, products):
    rows = []
    for i, p in enumerate(products, 1):
        rows.append(f"""<tr id="{e(p['id'])}">
<td class="num">{i}</td>
<td><strong>{e(p['display_name'])}</strong><br><a href="{R}categories/{e(p['category'])}/">{e(CATS[p['category']]['name'])}</a></td>
<td>{e(p['observed_listing_title'])}</td>
<td><code>{e(p['observed_asin'])}</code><br><span class="small">Observed {TODAY}</span></td>
<td>{ext(p['supplied_link'], p['supplied_link'], p['id'])}</td>
<td>{ext(p['source_url'], 'Amazon.com listing (source)')}<br><span class="small">Observed {TODAY}</span></td>
<td><span class="unverified">Intended ASIN UNVERIFIED</span><br><span class="small">Special Link test not run</span></td>
</tr>""")
    return "".join(rows)


PRODUCT_TH = """<tr><th>#</th><th>Product</th><th>Listing title (as shown)</th><th>Observed ASIN</th><th>Supplied link</th><th>Source</th><th>Status</th></tr>"""


def table(cls, headers, rows, table_id=None, verified=True):
    ids = f' id="{table_id}"' if table_id else ""
    vcls = " data-verified" if verified else ""
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join(rows)
    return f'<div class="tablewrap"><table class="data {cls}"{ids}{vcls}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def row(cells):
    return "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"


def cell_text(t):
    return e(t)


def unverified(text="UNVERIFIED"):
    return f'<span class="unverified">{e(text)}</span>'


def flag_sources(f):
    if not f["sources"]:
        return "Internal (from the brief or this repository)"
    return "<br>".join(outlink(SOURCES[s]["url"], SOURCES[s]["label"]) for s in f["sources"])


# ---------------------------------------------------------------- pages

@page("index.html", "Air fryers and meat thermometers, with the questions to settle first",
      "Five products from the supplied list, each linked to its Amazon listing, with guides on the questions to settle before buying.",
      active="", sitemap=True)
def page_home(R):
    observed = sum(1 for p in PRODUCTS if p["observed_asin"])
    confirmed = sum(1 for p in PRODUCTS if p["intended_asin"])
    cards = "".join(product_card(p, R) for p in PRODUCTS)
    gcards = "".join(guide_card(g, R) for g in GUIDES)
    tiles = "".join(
        f'<a class="tile" href="{R}categories/{c["slug"]}/"><strong>{e(c["name"])}</strong><span>{e(c["summary"])}</span></a>'
        for c in CATS.values()
    )
    return f"""
<section class="hero"><div>
<p class="kicker">Buyer's shortlist · {TODAY}</p>
<h1>Air fryers and meat thermometers, with the questions to settle first</h1>
<p class="dek">Five products from the supplied list. Each card's button goes to the supplied Amazon link, and the card shows only what that listing's title states. Anything we could not confirm is marked UNVERIFIED rather than filled in.</p>
<p><a class="btn" href="{R}products/">Compare all five</a> <a class="btn ghost" href="{R}analysis/">What we checked</a></p>
</div>
<aside class="notice"><p><strong>Status, {TODAY}:</strong> {observed} of {len(PRODUCTS)} supplied short links resolved to an Amazon listing page. {confirmed} of {len(PRODUCTS)} intended ASINs confirmed. 0 Special Link tests run. Prices, ratings and commissions are not shown. See <a href="{R}flagged/">Flagged for Review</a>.</p></aside>
</section>
<h2>The five products</h2>
<div class="cards">{cards}</div>
<h2>Start with a question</h2>
<div class="cards">{gcards}</div>
<h2>Shop by category</h2>
<div class="tiles">{tiles}</div>
<h2>What this site does not claim</h2>
<ul class="plain">
<li>No ranking, bestseller, or "trending" claim. Our evidence rule is on the <a href="{R}about/">About</a> page.</li>
<li>No price, rating, or commission figure. None was confirmed from an official source.</li>
<li>No claim that the supplied short links are valid or invalid. Their status is open (<a href="{R}flagged/">F-03</a>).</li>
</ul>
"""


@page("products/index.html", "All five products with listing sources",
      "Every product in the table with its observed Amazon ASIN, listing title and source link. Unconfirmed fields are marked.",
      active="products/")
def page_products(R):
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Products</p>
<h1>All products, with sources</h1>
<p class="dek">One row per supplied link. Columns come from the Amazon.com listing page the link resolved to on {TODAY}. Intended ASINs are not confirmed, so they are not shown.</p>
<div class="filter">
<label for="filter-products" class="small">Filter rows</label>
<input id="filter-products" type="search" placeholder="Type a brand, ASIN or category" data-filter-for="products-table">
<span class="count" data-filter-count>{len(PRODUCTS)} of {len(PRODUCTS)} rows shown</span>
</div>
{table("", ["#", "Product", "Listing title (as shown)", "Observed ASIN", "Supplied link", "Source", "Status"], [product_rows(R, PRODUCTS)], table_id="products-table")}
<p class="small">Each row's source is an Amazon.com listing page. No price, rating or availability is shown. The supplied short links are shown as submitted.</p>
"""


def cat_page(c):
    @page(f"categories/{c['slug']}/index.html", f"{c['name']}: the supplied products and their sources",
          f"{c['name']}: the supplied products in this category, their observed ASINs and listing sources. {c['summary']}")
    def _fn(R, c=c):
        prods = [p for p in PRODUCTS if p["category"] == c["slug"]]
        guide = ""
        if c["guide"]:
            g = next(x for x in GUIDES if x["slug"] == c["guide"])
            guide = f'<p>Read the guide: <a href="{R}guides/{e(g["slug"])}/">{e(g["title"])}</a></p>'
        else:
            guide = f'<p>{unverified("NO GUIDE YET")} See suggestion SG-06.</p>'
        cards = "".join(product_card(p, R) for p in prods)
        return f"""
<p class="crumbs"><a href="{R}">Home</a> › <a href="{R}products/">Products</a> › {e(c['name'])}</p>
<p class="kicker">Category</p>
<h1>{e(c['name'])}</h1>
<p class="dek">{e(c['summary'])}</p>
<p class="small">Category source: {ext(c['source_url'], c['source_label'])}</p>
{guide}
<div class="cards">{cards}</div>
<h2>Sources for this category</h2>
{table("compact", ["#", "Product", "Listing title (as shown)", "Observed ASIN", "Supplied link", "Source", "Status"], [product_rows(R, prods)])}
"""
    return _fn


for _c in CATS.values():
    cat_page(_c)


@page("guides/index.html", "Guides: questions to settle before you buy",
      "Four question-shaped buying guides for air fryers and multi-function kitchen appliances, each tied to the listings it cites.",
      active="guides/")
def page_guides(R):
    cards = "".join(guide_card(g, R) for g in GUIDES)
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Guides</p>
<h1>Guides: start with the question</h1>
<p class="dek">Each guide is built around a question a buyer would ask. Titles are working titles chosen as editorial hypotheses. They are not claims about popularity or search volume.</p>
<div class="cards">{cards}</div>
"""


def guide_fn(g):
    @page(f"guides/{g['slug']}/index.html", g["title"], g["description"], active="guides/",
          jsonld={
              "@context": "https://schema.org",
              "@type": "Article",
              "headline": g["title"],
              "description": g["description"],
              "datePublished": g["published"],
              "dateModified": TODAY,
              "inLanguage": "en",
              "mainEntityOfPage": f"{SITE_BASE}/guides/{g['slug']}/",
              "author": {"@type": "Organization", "name": SITE_NAME},
              "publisher": {"@type": "Organization", "name": SITE_NAME},
          })
    def _fn(R, g=g):
        body = (CONTENT / "guides" / f"{g['slug']}.html").read_text(encoding="utf-8")
        cut = body.rfind("<h2>")
        if cut != -1:
            body = body[:cut] + '<div data-scroll-sentinel aria-hidden="true"></div>' + body[cut:]
        cat = CATS[g["category"]]
        cited_products = [x for x in PRODUCTS if x["observed_asin"] in g["listing_sources"]]
        cited = "".join(f"<li>{ext(x['source_url'], x['display_name'] + ' (Amazon.com listing)')}</li>" for x in cited_products)
        return f"""
<p class="crumbs"><a href="{R}">Home</a> › <a href="{R}guides/">Guides</a> › {e(g['title'])}</p>
<p class="kicker">{e(cat['name'])} · {e(g['status'])}</p>
<h1>{e(g['title'])}</h1>
<p class="byline">By {e(SITE_NAME)} editorial (author to be named). Published {e(g['published'])}. Facts checked on {TODAY} against the listings cited below.</p>
{body}
<h2>Listings cited in this guide</h2>
<ul>{cited}</ul>
<section class="related"><h2>Related</h2><ul>
<li><a href="{R}categories/{e(cat['slug'])}/">{e(cat['name'])} category</a></li>
<li><a href="{R}products/">Product table with sources</a></li>
<li><a href="{R}guides/">All guides</a></li>
</ul></section>
"""
    return _fn


for _g in GUIDES:
    guide_fn(_g)


@page("intent-records/index.html", "Product-intent confirmation record",
      "For each supplied link: the intended ASIN, official listing URL, confirmation date and source, kept apart from the observed redirect target.",
      active="")
def page_intent(R):
    rows = []
    for p in PRODUCTS:
        rows.append(row([
            ext(p["supplied_link"], p["supplied_link"], p["id"]),
            unverified("BLANK, UNVERIFIED") if not p["intended_asin"] else f"<code>{e(p['intended_asin'])}</code>",
            unverified("NOT SET"),
            unverified("NOT CONFIRMED"),
            unverified("NONE"),
            ext(p["observed_redirect_target"], p["observed_redirect_target"]) + f'<br><span class="small">ASIN <code>{e(p["observed_asin"])}</code> · observed {TODAY}</span>',
        ]))
    t = table("", ["Submitted link", "Intended ASIN", "Official listing URL (for intended ASIN)", "Confirmation date", "Confirmation source", "Observed redirect target (separate field)"], rows, verified=False)
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Product-intent records</p>
<h1>Product-intent confirmation record</h1>
<p class="dek">For every submitted link this record keeps two fields apart. <strong>Intended ASIN</strong> is what the owner says the link should be. <strong>Observed redirect target</strong> is where the link went when we opened it. The observed value is never copied into the intended column.</p>
<div class="notice"><p><strong>No intended ASIN has been confirmed.</strong> The short-link slugs are 9 characters, and ASINs are 10 (<a href="{R}flagged/">F-01</a>). The brief did not supply intended ASINs, so the intended fields stay blank until the owner confirms them (<a href="{R}questions/">Q-01</a>).</p></div>
{t}
<p class="small">Source for the observed targets: the Amazon.com listing pages linked in each row, read on {TODAY}.</p>
"""


@page("analysis/index.html", "Analysis: what the listings support and what they do not",
      "Verification results for the five supplied links, the findings they support, and the gaps that stop any further decision.",
      active="analysis/")
def page_analysis(R):
    rows = []
    for p in PRODUCTS:
        rows.append(row([
            f"<strong>{e(p['display_name'])}</strong>",
            f"Yes, to <code>{e(p['observed_asin'])}</code>",
            e(p["observed_breadcrumb"]),
            unverified("NOT CAPTURED"),
            unverified("NOT CAPTURED"),
            unverified("NOT CONFIRMED"),
            ext(p["source_url"], "Amazon.com listing"),
        ]))
    verif = table("compact", ["Product", "Short link resolved?", "Breadcrumb read", "Price", "Rating", "Intended ASIN", "Source"], rows)
    slug_rows = []
    for p in PRODUCTS:
        slug = p["supplied_link"].rsplit("/", 1)[-1]
        slug_rows.append(row([
            ext(p["supplied_link"], p["supplied_link"]),
            f"<code>{e(slug)}</code> ({len(slug)} characters)",
            f"<code>{e(p['observed_asin'])}</code> ({len(p['observed_asin'])} characters)",
            ext(p["source_url"], "Amazon.com listing"),
        ]))
    slugs = table("compact", ["Supplied link", "Slug after the domain", "Observed ASIN", "Source"], slug_rows)
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Analysis</p>
<h1>Analysis: what the listings support</h1>
<p class="dek">Method: each supplied short link was opened on {TODAY}. The redirect target, page title and breadcrumb were read from the page. Prices, ratings and availability were not captured, so they are not used anywhere on the site.</p>

<h2>Verification by product</h2>
{verif}

<h2>Findings</h2>
<ol class="steps">
<li><strong>All five short links resolved to amazon.com product pages</strong> on {TODAY} (<a href="{R}intent-records/">intent record</a>). This is an observation, not a validation of the tracking.</li>
<li><strong>The slugs are not ASINs.</strong> Each slug is 9 characters; the observed ASINs are 10 characters (<a href="{R}flagged/">F-01</a>).</li>
<li><strong>The five products fall into three categories:</strong> two basket-style air fryers and one French-door air-fryer oven under "Fryers &gt; Air Fryers", and two thermometers under "Thermometers &amp; Timers &gt; Meat". The breadcrumb is the source for each.</li>
<li><strong>Capacity is stated in different units.</strong> The titles say "6 Quart", "8 Qt" and "26QT", and the 6-quart listing also gives "2 Independent 3Qt" baskets. The guide on capacity explains why these figures are not directly comparable.</li>
<li><strong>Counter-space analysis cannot be done yet.</strong> The listing dimensions were not captured, so no capacity-per-depth figure is published (<a href="{R}register/">S-23</a>).</li>
</ol>

<h2>Short-link slugs and observed ASINs</h2>
<p>The slug is shown as submitted. The observed ASIN is the redirect target, read from the Amazon.com page.</p>
{slugs}

<h2>What the current data can and cannot support</h2>
{table("compact", ["Decision", "Supported now?", "What is missing", "Source"], [
    row(["Which product each link is meant to sell", unverified("NO"), "Owner-confirmed intended ASIN per link (Q-01)", ext("https://affiliate-program.amazon.com/help/operating/policies", "Associates Program Policies")]),
    row(["Whether links track sales to this Associates account", unverified("NO"), "Special Link test and tracking report (Q-02, Q-03)", ext("https://affiliate-program.amazon.com/help/operating/policies", "Associates Program Policies")]),
    row(["Which product has the lower price", unverified("NO"), "Prices not captured or confirmed (F-05)", ext("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement")]),
    row(["Which product is better rated", unverified("NO"), "Ratings not captured (F-05)", ext("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement")]),
    row(["Which format suits a given household", "Partly, as a question list", "Household answers from the buyer (see guides)", ext("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content")]),
    row(["Whether the guides attract search traffic", unverified("NO"), "Search Console data (Q-09)", ext("https://developers.google.com/search/docs/appearance/page-experience", "Google: page experience")]),
], verified=True)}
"""


@page("register/index.html", "Backlog register: what is done, partly done or not done",
      "The brief's backlog rows (S-04 to S-25), with the status it states and the status this build actually has.",
      active="")
def page_register(R):
    rows = []
    for r in REGISTER["rows"]:
        src = outlink(r["source"], "Official source") if r["source"] else unverified("NO SOURCE SUPPLIED")
        rows.append(row([
            f"<strong>{e(r['id'])}</strong><br><span class='small'>{e(r['priority'])}</span>",
            e(r["item"]),
            e(r["stated"]),
            e(r["build"]),
            src,
        ]))
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Backlog register</p>
<h1>Backlog register</h1>
<p class="dek">{e(REGISTER['note'])}</p>
{table("compact", ["ID", "Item", "Status as stated", "Status in this build", "Source"], rows)}
<p class="small">Rows S-06 and S-14 are recorded as the brief states. Their decision records are in a separate project and were not independently verified (<a href="{R}flagged/">F-10</a>).</p>
"""


@page("questions/index.html", "Open questions before any decision can be made",
      "What is known, what is missing, and how to get each missing item, for every open question blocking a decision.",
      active="questions/")
def page_questions(R):
    src_map = {
        "Q-01": ext("https://affiliate-program.amazon.com/help/operating/policies", "Associates Program Policies"),
        "Q-02": ext("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 5"),
        "Q-03": ext("https://affiliate-program.amazon.com/help/operating/policies", "Associates Program Policies"),
        "Q-04": ext("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content"),
        "Q-05": unverified("NO OFFICIAL SOURCE LOCATED"),
        "Q-06": unverified("NO OFFICIAL SOURCE LOCATED"),
        "Q-07": unverified("NO OFFICIAL SOURCE LOCATED"),
        "Q-08": ext("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement"),
        "Q-09": ext("https://search.google.com/search-console/about", "Google Search Console"),
        "Q-10": unverified("NO OFFICIAL SOURCE LOCATED"),
        "Q-11": ext("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement"),
        "Q-12": ext("https://www.amazon.com/dp/B0CDY277D3", "Amazon.com listing (example)"),
    }
    rows = [row([
        f"<strong>{e(q['id'])}</strong>",
        e(q["question"]),
        e(q["have"]),
        e(q["missing"]),
        e(q["how_to_get"]),
        e(q["blocks"]),
        src_map.get(q["id"], unverified("NO SOURCE")),
    ]) for q in QUESTIONS]
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Open questions</p>
<h1>Open questions</h1>
<p class="dek">These questions must be answered before a decision is made from this data. Each row says what we have, what is missing, and how to get it. Nothing here is filled in from assumption.</p>
{table("compact", ["ID", "Question", "What we have", "What is missing", "How to get it", "Blocks", "Source"], rows)}
"""


@page("suggestions/index.html", "Suggestions for review: choose before anything changes",
      "Options for the site's open decisions. Each is listed with its trade-offs and a labelled recommendation. Nothing is implemented until the owner chooses.",
      active="suggestions/")
def page_suggestions(R):
    cards = []
    for s in SUGG["suggestions"]:
        opts = "".join(
            f"<li><strong>{e(o['id'])}.</strong> {e(o['label'])}<br><span class='small'>Trade-off: {e(o['tradeoff'])}</span></li>"
            for o in s["options"]
        )
        cards.append(f"""<article class="card">
<p class="kicker" style="margin:0">{e(s['id'])} · awaiting choice</p>
<h3>{e(s['topic'])}</h3>
<ul class="plain">{opts}</ul>
<p class="small"><strong>Recommendation (an argument, not a decision):</strong> {e(s['recommendation'])}</p>
</article>""")
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Suggestions</p>
<h1>Suggestions for review</h1>
<p class="dek">{e(SUGG['note'])} To choose, reply with the suggestion ID and option (for example, SG-01: A).</p>
<div class="cards">{''.join(cards)}</div>
"""


@page("flagged/index.html", "Flagged for Review: irregularities, unverified items and sources",
      "Irregularities and unverified items found while building the site, with the source link for each. None blocks publication.",
      active="flagged/")
def page_flagged(R):
    extra = {"F-09": outlink("https://github.com/wingbangboozle1-lang/Prod1/tree/arena/cba9af3f-prod1", "Other session's branch on origin")}
    rows = []
    for f in FLAGS:
        sev = {"high": unverified("HIGH"), "medium": "<span class='pill'>MEDIUM</span>", "low": "<span class='pill'>LOW</span>"}[f["severity"]]
        srcs = extra.get(f["id"]) or flag_sources(f)
        rows.append(row([f"<strong>{e(f['id'])}</strong>", sev, e(f["title"]), e(f["detail"]), srcs]))
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Flagged for Review</p>
<h1>Flagged for Review</h1>
<p class="dek">Irregularities and unverified items, for the owner to review after the site is live. None of them blocks publication. Each one says what is wrong and the source to check.</p>
<div class="notice"><p>Items marked UNVERIFIED are blank on purpose. Nothing has been filled in from inference.</p></div>
{table("compact", ["ID", "Severity", "Issue", "Detail", "Source"], rows, verified=False)}
"""


@page("ledger/index.html", "Campaign ledger (no first-party data yet)",
      "The campaign ledger is empty by design. Rows will be added only from authorized first-party Associates or analytics reports.",
      active="")
def page_ledger(R):
    headers = ["Timestamp (UTC)", "Source", "Channel", "Eligible sessions", "Clicks", "Reported orders", "Provenance (report and date)", "Notes"]
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Campaign ledger</p>
<h1>Campaign ledger</h1>
<p class="dek">The ledger starts empty. A row is added only when an authorized first-party report supplies the value. No conversion score, revenue figure or forecast is shown.</p>
<div class="tablewrap"><table class="data compact" id="ledger-table"><thead><tr>{''.join(f'<th>{e(h)}</th>' for h in headers)}</tr></thead><tbody>
<tr><td colspan="{len(headers)}" class="small">No rows yet. No first-party report has been received.</td></tr>
</tbody></table></div>
<p class="small">The same header is in <a href="{R}ledger.csv">ledger.csv</a>.</p>
"""


@page("analytics/index.html", "Analytics and measurement: five events, tracker off",
      "The five proposed click and page events, what each sends, and why measurement is off until an endpoint and a consent decision exist.",
      active="")
def page_analytics(R):
    events = [
        ("page_view", "A page loads", "Path only (no query string)"),
        ("outbound_click", "A product link is clicked", "Path and product ID"),
        ("guide_scroll_75", "A reader reaches the end section of a guide", "Path only"),
        ("table_filter", "A reader first types in the products filter", "Path only"),
        ("feed_subscribe_click", "A reader clicks the RSS link", "Path only"),
    ]
    rows = [row([f"<code>{e(n)}</code>", e(w), e(d), unverified("PROPOSED, NOT APPROVED")]) for n, w, d in events]
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Analytics and measurement</p>
<h1>Analytics and measurement</h1>
<div class="notice"><p><strong>Tracker status: off.</strong> No endpoint is hosted. GitHub Pages serves static files only, so the collector in <code>endpoint/</code> must run on a server the owner controls (<a href="{R}flagged/">F-07</a>).</p></div>
<h2>The five events</h2>
<p class="small">The brief refers to "the five defined events" but does not list them. These five are a proposal (<a href="{R}flagged/">F-06</a>).</p>
{table("compact", ["Event", "Fires when", "Sends", "Status"], rows, verified=False)}
<h2>Privacy design</h2>
<ul class="plain">
<li>No cookies, no localStorage, no fingerprinting.</li>
<li>The tracker sends the event name, the path without query string, and a product ID for outbound clicks.</li>
<li>The collector stores daily counts only: no IP address, no user agent.</li>
<li>Nothing is sent until an endpoint URL is set in the page's <code>analytics-endpoint</code> meta tag.</li>
</ul>
<h2>What is needed before this is on</h2>
<ol class="steps">
<li>Owner approves the event list (Q-06).</li>
<li>Owner chooses a hosting option (<a href="{R}suggestions/">SG-01</a>).</li>
<li>A privacy notice and consent approach are written (Q-05).</li>
</ol>
"""


@page("executive-summary/index.html", "Executive summary",
      "What this site is, what has been verified, what has not, and the decisions that remain with the owner.",
      active="executive-summary/")
def page_summary(R):
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › Executive summary</p>
<h1>Executive summary</h1>
<p class="byline">As of {TODAY}. Working name: {e(SITE_NAME)}.</p>
<h2>What was built</h2>
<p>A static site with a product table, five category and product views, four question-led guides, and dashboards for the analysis, backlog register, product-intent records, open questions, suggestions, campaign ledger, analytics, and flagged items. It publishes from <code>docs/</code> on GitHub Pages.</p>
<h2>What is verified</h2>
<ul class="plain">
<li>All five supplied short links resolved to Amazon.com product pages, observed {TODAY} (<a href="{R}intent-records/">records</a>).</li>
<li>The title, breadcrumb and observed ASIN for each product (<a href="{R}products/">products</a>).</li>
<li>The Associates disclosure wording, from the Operating Agreement, Section 5 (<a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener" target="_blank">source</a>). Confirmed from a search excerpt of the official page; the full text should be re-checked before any change.</li>
<li>The rel="sponsored" rule for paid links (<a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="noopener" target="_blank">Google</a>).</li>
</ul>
<h2>What is not verified</h2>
<ul class="plain">
<li>The intended ASIN for each link. None was supplied (<a href="{R}questions/">Q-01</a>).</li>
<li>Whether the links track to the owner's Associates account. The Special Link test was not run (<a href="{R}flagged/">F-03</a>).</li>
<li>Prices, ratings, commission rates, and listing dimensions (<a href="{R}flagged/">F-05</a>).</li>
<li>Any traffic, click or order data. None exists yet (<a href="{R}analytics/">analytics</a>).</li>
</ul>
<h2>Decisions waiting for the owner</h2>
<ol class="steps">
<li>Hosting for the analytics collector, and the consent approach (<a href="{R}suggestions/">SG-01</a>).</li>
<li>Whether to run the Special Link test before scaling (<a href="{R}suggestions/">SG-02</a>).</li>
<li>Publishing cadence (<a href="{R}suggestions/">SG-03</a>).</li>
<li>Product imagery (<a href="{R}suggestions/">SG-04</a>).</li>
<li>Which build publishes, given another session's overlapping branch (<a href="{R}suggestions/">SG-08</a>).</li>
</ol>
<h2>Compliance posture</h2>
<p>The Associates statement appears under the masthead of every page and in the footer. Every Amazon link is marked <code>rel="sponsored"</code>. The site does not say or imply that Amazon endorses it. Link-level and placement review against the FTC guidance is still an open item for the owner (<a href="{R}flagged/">F-03</a>).</p>
<p><a class="btn" href="{R}flagged/">Open Flagged for Review</a></p>
"""


@page("about/index.html", "About Counter Notes and its editorial standard",
      "How the site is written and checked: the evidence rule, the disclosure, what the site does with data, and how to report a correction.",
      active="")
def page_about(R):
    return f"""
<p class="crumbs"><a href="{R}">Home</a> › About</p>
<h1>About and editorial standard</h1>
<h2>Who writes it</h2>
<p>{e(SITE_NAME)} is a working name. No author is named yet (<a href="{R}questions/">Q-04</a>).</p>
<h2>Evidence rule</h2>
<ul class="plain">
<li>Every product fact comes from a named source. Facts we cannot confirm are marked UNVERIFIED.</li>
<li>No "trending", "bestseller", or popularity claim. None was verified from an official dated snapshot.</li>
<li>No superiority claim between products.</li>
</ul>
<h2>Disclosure</h2>
<p>{e(DISCLOSURE)} {e(NOT_ENDORSED)}</p>
<h2>Data and privacy</h2>
<p>The site uses no cookies. Analytics are off (<a href="{R}analytics/">details</a>).</p>
<h2>Corrections</h2>
<p>Report a correction through the <a href="{REPO_URL}/issues" rel="noopener" target="_blank">repository issue tracker</a>.</p>
"""


@page("404.html", "Page not found", "The page you requested is not on this site.", sitemap=False)
def page_404(R):
    return f"""<h1>Page not found</h1><p class="dek">The page is not here. Start from the <a href="{R}">home page</a> or the <a href="{R}products/">products</a>.</p>"""


# ---------------------------------------------------------------- outputs

def write_sitemap(pages):
    urls = []
    for p in pages:
        if not p["sitemap"]:
            continue
        loc = p["path"][:-len("index.html")] if p["path"].endswith("index.html") else p["path"]
        urls.append(f"  <url><loc>{SITE_BASE}/{loc}</loc><lastmod>{TODAY}</lastmod></url>")
    body = "\n".join(urls)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body + "\n</urlset>\n", encoding="utf-8")


def write_feed():
    day = datetime.date.fromisoformat(TODAY)
    pub = email.utils.format_datetime(datetime.datetime(day.year, day.month, day.day, 0, 0, tzinfo=datetime.timezone.utc))
    items = []
    for g in GUIDES:
        link = f"{SITE_BASE}/guides/{g['slug']}/"
        items.append(f"""  <item>
    <title>{e(g['title'])}</title>
    <link>{e(link)}</link>
    <guid isPermaLink="true">{e(link)}</guid>
    <pubDate>{pub}</pubDate>
    <description>{e(g['description'])}</description>
  </item>""")
    (OUT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>{e(SITE_NAME)}: guides</title>
  <link>{SITE_BASE}/</link>
  <description>Question-led buying guides for air fryers and multi-function kitchen appliances. Working name; see the about page.</description>
  <language>en</language>
  <lastBuildDate>{pub}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
""", encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "assets").mkdir()
    shutil.copy(SRC / "assets" / "style.css", OUT / "assets" / "style.css")
    shutil.copy(SRC / "assets" / "track.js", OUT / "assets" / "track.js")
    shutil.copy(DATA / "ledger.csv", OUT / "ledger.csv")
    for p in PAGES:
        target = OUT / p["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(shell(p), encoding="utf-8")
    write_sitemap(PAGES)
    write_feed()
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(PAGES)} pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
