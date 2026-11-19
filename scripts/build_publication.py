#!/usr/bin/env python3
"""Build, canonicalize, and stage the single public GitHub Pages site.

The source repository also contains historical review builds. Only this curated root
publication is copied to ``_site``; nested ``docs/``, ``articles/`` and
``counter-check/site/`` outputs are not published by the Pages workflow.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / "data" / "products.json"
GUIDE_DATA = ROOT / "data" / "guides.json"
PUBLICATION_BASE = "https://wingbangboozle1-lang.github.io/Prod1/"

ROOT_HTML = [
    "index.html",
    "air-fryers.html",
    "thermometers.html",
    "compare.html",
    "guides.html",
    "guide-basket-vs-oven.html",
    "guide-capacity-checklist.html",
    "guide-cleanup-counter-space.html",
    "guide-multifunction-questions.html",
    "guide-thermometer-accuracy.html",
    "executive-summary.html",
    "suggestions.html",
    "verification.html",
    "flagged.html",
    "compliance.html",
    "methodology.html",
    "search.html",
]
INDEXABLE_PAGES = [
    "index.html",
    "air-fryers.html",
    "thermometers.html",
    "compare.html",
    "guides.html",
]
NOINDEX_PAGES = {
    "search.html",
    "executive-summary.html",
    "suggestions.html",
    "verification.html",
    "flagged.html",
    "compliance.html",
    "methodology.html",
}
ASSETS = ["assets/app.js", "assets/style.css", "assets/og-image.svg"]

CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>', re.I)
OG_URL_RE = re.compile(r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>', re.I)
ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>', re.I)


def canonical_for(path: str) -> str:
    return PUBLICATION_BASE if path == "index.html" else PUBLICATION_BASE + path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"publication build error: {message}")


def validate_inputs(site: dict, guides: dict) -> None:
    require(site.get("site", {}).get("canonical") == PUBLICATION_BASE,
            "site canonical must match the selected root GitHub Pages URL")
    require(site.get("site", {}).get("trackingId") == "shopnow047c-20",
            "the selected Associates tracking ID changed unexpectedly")
    products = site.get("products", [])
    require(len(products) == 5, "expected the five product records from the brief")
    intent_keys = {"intendedAsin", "officialListingUrl", "confirmationDate", "source"}
    for product in products:
        intent = product.get("productIntent")
        require(isinstance(intent, dict) and intent_keys <= intent.keys(),
                f"{product.get('id', 'product')}: missing separate product-intent fields")
        populated = [bool(str(intent[k]).strip()) for k in intent_keys]
        require(not any(populated) or all(populated),
                f"{product.get('id', 'product')}: intent fields must be complete or left blank")
        observed_asin = product.get("observedAsin", "")
        require(bool(re.fullmatch(r"[A-Z0-9]{10}", observed_asin)),
                f"{product.get('id', 'product')}: malformed observed ASIN")
        require(product.get("observedListingUrl") == f"https://www.amazon.com/dp/{observed_asin}",
                f"{product.get('id', 'product')}: observed listing URL does not match the separate observed ASIN")
        require(product.get("observedRedirectUrl") == product.get("observedListingUrl"),
                f"{product.get('id', 'product')}: observed redirect URL does not match recorded listing target")
        require(product.get("observedListingUrl", "") in product.get("observedRedirectTarget", ""),
                f"{product.get('id', 'product')}: descriptive redirect observation conflicts with its URL field")
        expected_candidate = f"{product['observedListingUrl']}?tag={site['site']['trackingId']}"
        require(product.get("candidateAffiliateUrl") == expected_candidate,
                f"{product.get('id', 'product')}: candidate URL differs from the observed target or selected tracking ID")
    require(guides.get("site") == site["site"]["name"], "guide manifest site name mismatch")
    guide_paths = [g.get("path", "") for g in guides.get("guides", [])]
    require(len(guide_paths) == len(set(guide_paths)), "guide manifest has duplicate paths")
    require(bool(guide_paths), "guide manifest is empty")
    for guide in guides.get("guides", []):
        require(re.fullmatch(r"guide-[a-z0-9-]+\.html", guide.get("path", "")) is not None,
                f"invalid guide path: {guide.get('path')!r}")
        require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", guide.get("published", "")) is not None,
                f"invalid publication date for {guide.get('path')}")
        datetime.strptime(guide["published"], "%Y-%m-%d")
        require(guide.get("title") and guide.get("description"),
                f"missing feed metadata for {guide.get('path')}")


def canonicalize_html(path: Path, relative: str) -> None:
    text = path.read_text(encoding="utf-8")
    canonical = canonical_for(relative)
    canonical_tag = f'<link rel="canonical" href="{canonical}">'
    if CANONICAL_RE.search(text):
        text = CANONICAL_RE.sub(canonical_tag, text, count=1)
    else:
        text = text.replace("</head>", canonical_tag + "\n</head>", 1)
    og_tag = f'<meta property="og:url" content="{canonical}">'
    if OG_URL_RE.search(text):
        text = OG_URL_RE.sub(og_tag, text, count=1)
    else:
        text = text.replace("</head>", og_tag + "\n</head>", 1)
    if relative in NOINDEX_PAGES:
        robots_tag = '<meta name="robots" content="noindex,follow">'
        if ROBOTS_RE.search(text):
            text = ROBOTS_RE.sub(robots_tag, text, count=1)
        else:
            text = text.replace("</head>", robots_tag + "\n</head>", 1)
    elif ROBOTS_RE.search(text):
        text = ROBOTS_RE.sub("", text, count=1)
    # Every flagged record gets a stable fragment target for cross-page review links.
    if relative == "flagged.html":
        text = re.sub(r'<tr>\s*<td>(FLG-\d+)</td>', r'<tr id="\1"><td>\1</td>', text)
    path.write_text(text, encoding="utf-8")


def write_metadata(site: dict, guides: dict) -> None:
    base = PUBLICATION_BASE
    urls = [base if p == "index.html" else base + p for p in INDEXABLE_PAGES]
    urls.extend(base + g["path"] for g in guides["guides"])
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    sitemap.extend(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    channel_description = "Question-led kitchen buying guides and product comparisons based on dated listing captures."
    items = []
    for guide in guides["guides"]:
        published = datetime.strptime(guide["published"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        pub_date = published.strftime("%a, %d %b %Y 00:00:00 GMT")
        link = base + guide["path"]
        items.append(
            "    <item>\n"
            f"      <title>{escape(guide['title'])}</title>\n"
            f"      <link>{escape(link)}</link>\n"
            f"      <guid isPermaLink=\"true\">{escape(link)}</guid>\n"
            f"      <pubDate>{pub_date}</pubDate>\n"
            f"      <description>{escape(guide['description'])}</description>\n"
            "    </item>"
        )
    rss = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        "    <title>The Countertop Guide</title>",
        f"    <link>{escape(base)}</link>",
        f"    <description>{escape(channel_description)}</description>",
        f'    <atom:link href="{escape(base + "feed.xml")}" rel="self" type="application/rss+xml"/>',
        *items,
        "  </channel>",
        "</rss>",
    ]
    (ROOT / "feed.xml").write_text("\n".join(rss) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + base + "sitemap.xml\n",
        encoding="utf-8",
    )


def stage_public_site() -> None:
    stage = ROOT / "_site"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for name in ROOT_HTML:
        src = ROOT / name
        require(src.is_file(), f"missing generated page: {name}")
        shutil.copy2(src, stage / name)
    for name in ASSETS:
        src = ROOT / name
        require(src.is_file(), f"missing public asset: {name}")
        target = stage / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    for name in ("sitemap.xml", "feed.xml", "robots.txt", ".nojekyll"):
        src = ROOT / name
        require(src.is_file(), f"missing publication metadata: {name}")
        shutil.copy2(src, stage / name)
    search_index = ROOT / "data" / "search-index.json"
    require(search_index.is_file(), "missing site search index")
    (stage / "data").mkdir(exist_ok=True)
    shutil.copy2(search_index, stage / "data" / search_index.name)


def main() -> None:
    site = json.loads(SITE_DATA.read_text(encoding="utf-8"))
    guides = json.loads(GUIDE_DATA.read_text(encoding="utf-8"))
    validate_inputs(site, guides)
    subprocess.run([sys.executable, str(ROOT / "build_site.py")], cwd=ROOT, check=True)
    for relative in ROOT_HTML:
        canonicalize_html(ROOT / relative, relative)
    for guide in guides["guides"]:
        require((ROOT / guide["path"]).is_file(), f"guide manifest points to missing page: {guide['path']}")
    write_metadata(site, guides)
    stage_public_site()
    print(f"Prepared one GitHub Pages publication in _site ({len(ROOT_HTML)} pages, {len(guides['guides'])} feed items).")


if __name__ == "__main__":
    main()
