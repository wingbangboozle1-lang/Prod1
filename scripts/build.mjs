#!/usr/bin/env node
// Static site generator and publishing gate for the affiliate site.
// Reads data/*.json, writes docs/ (served by GitHub Pages from main:/docs),
// then runs the compliance and link gates. Exits non-zero if any gate fails.
// No dependencies. Node 18+.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = path.join(ROOT, 'docs');
const read = (f) => JSON.parse(fs.readFileSync(path.join(ROOT, 'data', f), 'utf8'));

const site = read('site.json');
const products = read('products.json');
const guides = read('guides.json').guides;
const sources = read('sources.json');
const flags = read('flags.json').flags;
const suggestions = read('suggestions.json').suggestions;
const questions = read('questions.json').questions;
const ledger = read('ledger.json');

const BASE = site.base_url;
const DISCLOSURE = site.disclosure_text;
const CATEGORIES = {
  'air-fryers': { name: 'Air fryers and ovens', href: 'categories/air-fryers.html' },
  thermometers: { name: 'Meat thermometers', href: 'categories/thermometers.html' },
};
const NAV = [
  ['products.html', 'Products'],
  ['guides/index.html', 'Guides'],
  ['categories/air-fryers.html', 'Air fryers and ovens'],
  ['categories/thermometers.html', 'Thermometers'],
  ['analysis.html', 'Analysis'],
  ['sources.html', 'Sources'],
  ['suggestions.html', 'Suggestions'],
  ['flagged.html', 'Flagged for Review'],
];
const ASIN_RE = /^B[0-9A-Z]{9}$/;
const BANNED = /\b(trending|best[- ]?sellers?|#1|top[- ]rated|most popular|guaranteed)\b/i;

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const unverified = (v) => (v && String(v).trim() ? esc(v) : '<span class="pill pill-warn">Unverified</span>');
const pagesOut = []; // { file, html, title, description }

function prefixFor(file) {
  return file.includes('/') ? '../' : '';
}

function layout({ file, title, description, body, bodyClass = '' }) {
  const p = prefixFor(file);
  const fullTitle = file === 'index.html' ? `${site.name}: ${site.tagline}` : `${title} · ${site.name}`;
  const nav = NAV.map(([href, label]) => {
    const dataTrack = href.startsWith('categories/') ? ' data-track="category"' : '';
    return `<a href="${p}${href}"${dataTrack}>${esc(label)}</a>`;
  }).join('');
  const footNav = NAV.map(([href, label]) => `<li><a href="${p}${href}">${esc(label)}</a></li>`).join('');
  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${BASE}/${file}">
<link rel="alternate" type="application/rss+xml" title="${esc(site.name)} feed" href="${p}feed.xml">
<link rel="stylesheet" href="${p}assets/site.css">
</head>
<body class="${bodyClass}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="wrap masthead-inner">
  <a class="brand" href="${p}index.html">${esc(site.name)}</a>
  <span class="tagline">${esc(site.tagline)}</span>
</div></header>
<div class="disclosure" role="note" aria-label="Affiliate disclosure"><div class="wrap">
  <strong>Disclosure:</strong> ${esc(DISCLOSURE)} ${esc(site.not_endorsed_text)}
</div></div>
<nav class="nav" aria-label="Main"><div class="wrap">${nav}</div></nav>
<main id="main" class="wrap">
${body}
</main>
<footer class="footer"><div class="wrap">
  <p class="disclosure-foot"><strong>Disclosure:</strong> ${esc(DISCLOSURE)} ${esc(site.not_endorsed_text)}</p>
  <div class="foot-grid">
    <div><h2>Dashboards</h2><ul>${footNav}</ul></div>
    <div><h2>About</h2><ul>
      <li><a href="${p}about.html">About, method and disclosure</a></li>
      <li><a href="${p}feed.xml" data-track="feed">RSS feed</a></li>
      <li><a href="${p}sitemap.xml">Sitemap</a></li>
    </ul></div>
    <div><h2>Status</h2><p>Last updated ${esc(site.updated)}. ${esc(site.name_status)}</p><p>Byline: ${esc(site.byline)}</p></div>
  </div>
</div></footer>
<script src="${p}assets/measure.js" defer></script>
</body>
</html>
`;
  // Gate-by-construction: every link to an Amazon host is marked sponsored.
  const sponsored = html.replace(/<a\b([^>]*?)href="(https?:\/\/(?:www\.)?(?:amazon\.com|link\.amazon)\b[^"]*)"([^>]*)>/g, (m, pre, href, post) => {
    const attrs = pre + post;
    const relm = attrs.match(/rel="([^"]*)"/);
    if (relm) {
      if (/\bsponsored\b/.test(relm[1])) return m;
      const newRel = `${relm[1]} sponsored`.trim();
      return m.replace(/rel="[^"]*"/, `rel="${newRel}"`);
    }
    return `<a${pre}href="${href}" rel="sponsored noopener"${post}>`;
  });
  pagesOut.push({ file, html: sponsored, title: fullTitle, description });
}

const productCard = (p) => {
  const prod = products.products.find((x) => x.id === p);
  return `<article class="card">
  <p class="kicker">${esc(CATEGORIES[prod.category].name)} · ${esc(prod.id)}</p>
  <h3>${esc(prod.observed_title.length > 90 ? prod.observed_title.slice(0, 88).replace(/\s+\S*$/, '') + '…' : prod.observed_title)}</h3>
  <p class="meta">Observed ASIN <code>${esc(prod.observed_asin)}</code> · Intended ASIN <span class="pill pill-warn">Unverified</span></p>
  <p><a class="btn" href="${esc(prod.submitted_link)}" rel="sponsored noopener" target="_blank" data-track="outbound" data-asin="${esc(prod.observed_asin)}" data-target="${esc(prod.id)}">View listing on Amazon (sponsored)</a></p>
</article>`;
};

const guideCard = (g, p = '') => `<article class="card">
  <p class="kicker">${esc(CATEGORIES[g.category].name)}${g.working_title ? ' · working title' : ''}</p>
  <h3><a href="${p}guides/${esc(g.slug)}.html">${esc(g.title)}</a></h3>
  <p>${esc(g.dek)}</p>
  <p class="meta">Published ${esc(g.date)} · ${esc(site.byline)}</p>
</article>`;

// ---------- Front page: products first ----------
const pickIds = ['P1', 'P2', 'P3', 'P4', 'P5'];
const heroGuide = guides[0];
layout({
  file: 'index.html',
  title: 'Home',
  description: 'Five product listings for air fryers, ovens and meat thermometers, with guides on the questions to ask first. Every listing link is marked sponsored.',
  body: `
<section class="hero">
  <div class="hero-main">
    <p class="kicker">This week's listings</p>
    <h1>Five picks to compare, and the questions to ask before you buy</h1>
    <p class="lede">Three air fryers and ovens, and two digital meat thermometers. Each listing link goes to the Amazon page and is marked sponsored. Each guide below explains what to check on the listing.</p>
    <p><a class="btn btn-ghost" href="products.html">See the full product table</a></p>
  </div>
  <aside class="hero-side">
    <p class="kicker">Latest guide</p>
    <h2><a href="guides/${esc(heroGuide.slug)}.html">${esc(heroGuide.title)}</a></h2>
    <p>${esc(heroGuide.dek)}</p>
  </aside>
</section>

<section>
  <h2 class="section-h">The products</h2>
  <div class="grid">${pickIds.map(productCard).join('')}</div>
</section>

<section>
  <h2 class="section-h">Guides</h2>
  <div class="grid">${guides.map((g) => guideCard(g)).join('')}</div>
</section>

<section>
  <h2 class="section-h">Categories</h2>
  <div class="grid tiles">
    <a class="tile" href="categories/air-fryers.html" data-track="category"><strong>Air fryers and ovens</strong><span>3 listings · 2 guides</span></a>
    <a class="tile" href="categories/thermometers.html" data-track="category"><strong>Meat thermometers</strong><span>2 listings · 1 guide</span></a>
  </div>
</section>

<section class="callout">
  <h2>What is confirmed, and what is not</h2>
  <p>All five listing pages were opened on ${esc(products.observed_on)}. Each titled product was observed. Intended ASINs, confirmation dates, prices and ratings are <span class="pill pill-warn">Unverified</span> and are left blank on purpose. The supplied links do not show the tracking ID ${esc(products.tracking_id_supplied)} in their redirect targets. See the <a href="flagged.html">Flagged for Review</a> page.</p>
</section>`,
});

// ---------- Products table ----------
const rows = products.products.map((p) => `<tr>
  <td><strong>${esc(p.observed_title)}</strong><br><span class="meta">${esc(CATEGORIES[p.category].name)} · ${esc(p.id)}</span></td>
  <td class="mono"><a href="${esc(p.submitted_link)}" rel="sponsored noopener" target="_blank" data-track="outbound" data-asin="${esc(p.observed_asin)}" data-target="${esc(p.id)}">${esc(p.submitted_link)}</a></td>
  <td>${p.intended_asin ? `<code>${esc(p.intended_asin)}</code>` : unverified(p.intended_asin)}</td>
  <td><code>${esc(p.observed_asin)}</code></td>
  <td><a href="${esc(p.official_listing_url)}" rel="noopener" target="_blank">${esc(p.official_listing_url)}</a></td>
  <td>${p.confirmation_date ? esc(p.confirmation_date) : unverified('')}</td>
  <td>${unverified('')}</td>
  <td>${unverified('')}</td>
  <td><a href="${esc(p.source)}" rel="noopener" target="_blank">${esc(p.source)}</a><br><span class="meta">Observed ${esc(p.observed_on)}</span></td>
  <td class="mono small">${esc(p.observed_redirect_target)}</td>
</tr>`).join('');
layout({
  file: 'products.html',
  title: 'Products',
  description: 'Product table for the five supplied Amazon listings: submitted link, observed ASIN, intended ASIN, official listing URL, confirmation date and source. Unverified fields are blank.',
  body: `
<h1>Products</h1>
<p class="lede">One row per submitted link. Observed values come from the page the link opens to, and are kept apart from the intended values, which the owner must supply. Blank cells are unverified and are not inferred.</p>
<p class="notice"><strong>Tracking:</strong> none of the five observed redirect targets contains <code>tag=${esc(products.tracking_id_supplied)}</code>. See FLAG-01. Links are kept as supplied and marked sponsored.</p>
<div class="table-wrap"><table class="data">
  <thead><tr>
    <th>Product (observed title)</th>
    <th>Submitted link</th>
    <th>Intended ASIN</th>
    <th>Observed ASIN</th>
    <th>Official listing URL</th>
    <th>Confirmation date</th>
    <th>Price</th>
    <th>Rating</th>
    <th>Source</th>
    <th>Observed redirect target (kept separate)</th>
  </tr></thead>
  <tbody>${rows}</tbody>
</table></div>
<p class="meta">Observed on ${esc(products.observed_on)}. ${esc(products.observation_method)}</p>
<h2 class="section-h">Field definitions</h2>
<ul class="plain">
  <li><strong>Intended ASIN:</strong> the product the owner meant to link. Not supplied, so blank.</li>
  <li><strong>Observed ASIN:</strong> the ASIN in the URL the link opened to. Not the same as the intended ASIN.</li>
  <li><strong>Confirmation date:</strong> the date the owner confirmed the intended product. Not yet recorded.</li>
  <li><strong>Price and rating:</strong> not recorded. See FLAG-04.</li>
</ul>`,
});

// ---------- Categories ----------
for (const [key, cat] of Object.entries(CATEGORIES)) {
  const list = products.products.filter((p) => p.category === key);
  const gs = guides.filter((g) => g.category === key);
  const file = cat.href;
  layout({
    file,
    title: cat.name,
    description: `${cat.name}: ${list.length} listings and ${gs.length} guides. Listing links are sponsored.`,
    body: `
<p class="kicker"><a href="../index.html">Home</a> / ${esc(cat.name)}</p>
<h1>${esc(cat.name)}</h1>
<h2 class="section-h">Listings</h2>
<div class="grid">${list.map((p) => productCard(p.id)).join('')}</div>
<h2 class="section-h">Guides</h2>
<div class="grid">${gs.map((g) => guideCard(g, '../')).join('')}</div>`,
  });
}

// ---------- Guides index and pages ----------
layout({
  file: 'guides/index.html',
  title: 'Guides',
  description: 'Question-shaped guides on comparing air fryers, ovens and meat thermometers. Working titles; no popularity claims.',
  body: `
<p class="kicker"><a href="../index.html">Home</a> / Guides</p>
<h1>Guides</h1>
<p class="lede">Each guide starts with a question a buyer might ask. The titles are working titles. They are not based on search volume or popularity data.</p>
<div class="grid">${guides.map((g) => guideCard(g, '../')).join('')}</div>`,
});

for (const g of guides) {
  const prods = g.products.map((id) => products.products.find((p) => p.id === id));
  const body = `
<p class="kicker"><a href="../index.html">Home</a> / <a href="index.html">Guides</a></p>
<article class="article">
  <h1>${esc(g.title)}</h1>
  <p class="dek">${esc(g.dek)}</p>
  <p class="meta">${esc(site.byline)} · Published ${esc(g.date)}${g.working_title ? ' · Working title' : ''}</p>
  ${g.sections.map((s) => `<h2>${esc(s.h)}</h2>${s.paras.map((t) => `<p>${esc(t)}</p>`).join('')}${s.list.length ? `<ul>${s.list.map((t) => `<li>${esc(t)}</li>`).join('')}</ul>` : ''}`).join('')}
  <aside class="callout">
    <h2>Listings mentioned in this guide</h2>
    <ul class="plain">${prods.map((p) => `<li><a href="${esc(p.submitted_link)}" rel="sponsored noopener" target="_blank" data-track="outbound" data-asin="${esc(p.observed_asin)}" data-target="${esc(p.id)}">${esc(p.observed_title.slice(0, 80))}${p.observed_title.length > 80 ? '…' : ''}</a> <span class="meta">(sponsored)</span></li>`).join('')}</ul>
    <p class="meta">Facts are as listed on the Amazon page on ${esc(products.observed_on)}. Check the listing before you buy.</p>
  </aside>
</article>`;
  layout({
    file: `guides/${g.slug}.html`,
    title: g.title,
    description: g.dek,
    body,
    bodyClass: 'guide',
  });
}

// ---------- Sources ----------
const srcRows = sources.sources.map((s) => `<tr>
  <td class="mono">${esc(s.id)}</td>
  <td><a href="${esc(s.url)}" rel="noopener" target="_blank">${esc(s.title)}</a><br><span class="meta">${esc(s.publisher)}</span></td>
  <td>${esc(s.page_date)}</td>
  <td>${esc(s.verified_items)}</td>
  <td>${esc(s.verification)}</td>
</tr>`).join('');
layout({
  file: 'sources.html',
  title: 'Sources',
  description: 'Official sources used for the site, with what was checked and on what date. Unverified items are marked.',
  body: `
<h1>Sources</h1>
<p class="lede">Each row links to an official or primary source. Checks were done on ${esc(sources.checked_on)}. Where a check was partial, the row says so.</p>
<div class="table-wrap"><table class="data">
  <thead><tr><th>ID</th><th>Source</th><th>Page date</th><th>What it supports</th><th>How it was checked</th></tr></thead>
  <tbody>${srcRows}</tbody>
</table></div>
<h2 class="section-h">Reference only (not verified)</h2>
<ul class="plain">${sources.reference_not_verified.map((r) => `<li><a href="${esc(r.url)}" rel="noopener" target="_blank">${esc(r.title)}</a>: ${esc(r.status)}</li>`).join('')}</ul>`,
});

// ---------- Analysis ----------
const pCount = products.products.length;
const asinOK = products.products.filter((p) => ASIN_RE.test(p.observed_asin)).length;
const intendedOK = products.products.filter((p) => p.intended_asin).length;
const tagOK = products.products.filter((p) => p.associates_tag_in_observed_url).length;
const openQs = questions.filter((q) => q.status !== 'Answered').length;
const openFlags = flags.length;
layout({
  file: 'analysis.html',
  title: 'Analysis',
  description: 'Measured status of the site: listings observed, confirmations recorded, tracking checks, and browser-only counts. No revenue forecast or conversion score.',
  body: `
<h1>Analysis</h1>
<p class="lede">What the data shows today. Counts only. No conversion score, revenue forecast or popularity claim is made here.</p>
<div class="stats">
  <div class="stat"><span>${pCount}</span>listings in the table</div>
  <div class="stat"><span>${asinOK}</span>observed ASINs in URL format</div>
  <div class="stat"><span>${intendedOK}</span>intended ASINs confirmed</div>
  <div class="stat"><span>${tagOK}</span>observed URLs with the tracking tag</div>
  <div class="stat"><span>${ledger.rows.length}</span>campaign-ledger rows</div>
  <div class="stat"><span>${openFlags}</span>items flagged for review</div>
</div>
<h2 class="section-h">Findings</h2>
<ol class="plain">
  <li>All five submitted links opened to amazon.com product pages with a title and a 10-character ASIN (<a href="products.html">Products</a>).</li>
  <li>No intended ASIN, confirmation date, price or rating is recorded, so none is shown. These are open items (<a href="flagged.html">FLAG-02, FLAG-04</a>).</li>
  <li>None of the five observed redirect targets carries the tracking ID ${esc(products.tracking_id_supplied)} (<a href="flagged.html">FLAG-01</a>).</li>
  <li>Two of five listings are thermometers, outside the air-fryer register (<a href="flagged.html">FLAG-03</a>).</li>
</ol>
<h2 class="section-h">Open questions</h2>
<div class="table-wrap"><table class="data">
  <thead><tr><th>ID</th><th>Question</th><th>Known</th><th>Unknown</th><th>To resolve</th><th>Status</th></tr></thead>
  <tbody>${questions.map((q) => `<tr><td class="mono">${esc(q.id)}</td><td>${esc(q.question)}</td><td>${esc(q.known)}</td><td>${esc(q.unknown)}</td><td>${esc(q.to_resolve)}</td><td><span class="pill pill-warn">${esc(q.status)}</span></td></tr>`).join('')}</tbody>
</table></div>
<h2 class="section-h">Browser-only counts (this browser)</h2>
<p>Counts stored on this device only. Nothing is sent anywhere unless an endpoint is configured (<a href="flagged.html">FLAG-06</a>).</p>
<div class="table-wrap"><table class="data" id="local-counts">
  <thead><tr><th>Event</th><th>Count in this browser</th></tr></thead>
  <tbody><tr><td colspan="2">Loading…</td></tr></tbody>
</table></div>
<p class="meta" id="local-status"></p>
<h2 class="section-h">Campaign ledger</h2>
<p>Starts empty. Rows are added only from authorised first-party reports, with timestamp, source, channel, eligible sessions, clicks and reported orders.</p>
<div class="table-wrap"><table class="data">
  <thead><tr>${ledger.columns.map((c) => `<th>${esc(c)}</th>`).join('')}</tr></thead>
  <tbody><tr><td colspan="${ledger.columns.length}" class="empty">No authorised first-party reports recorded yet.</td></tr></tbody>
</table></div>`,
});

// ---------- Suggestions ----------
layout({
  file: 'suggestions.html',
  title: 'Suggestions',
  description: 'Suggestions with options for each open decision. Nothing is implemented beyond the stated default until the owner chooses.',
  body: `
<h1>Suggestions</h1>
<p class="lede">Each suggestion lists the options. Pick one, and the site is changed to match. Until then the default shown is what the site does.</p>
${suggestions.map((s) => `<article class="card wide">
  <p class="kicker">${esc(s.id)} · ${esc(s.topic)}</p>
  <h2>${esc(s.question)}</h2>
  <ol class="options">${s.options.map((o) => `<li><strong>${esc(o.label)}</strong><br><span class="meta">${esc(o.argument)}</span></li>`).join('')}</ol>
  <p><strong>Default in this build:</strong> ${esc(s.default_in_build)}</p>
  <p><strong>Decision:</strong> <span class="pill pill-warn">${esc(s.decision)}</span> · <strong>Unlocks:</strong> ${esc(s.unlocks)}</p>
</article>`).join('')}`,
});

// ---------- Flagged ----------
layout({
  file: 'flagged.html',
  title: 'Flagged for Review',
  description: 'Irregularities and unverified items for owner review, each with its source links and the action needed.',
  body: `
<h1>Flagged for Review</h1>
<p class="lede">Irregularities and unverified items. They do not block publication. Each has the source links and the action needed.</p>
${flags.map((f) => `<article class="card wide">
  <p class="kicker">${esc(f.id)} · <span class="pill ${f.severity === 'High' ? 'pill-warn' : 'pill-ok'}">${esc(f.severity)}</span></p>
  <h2>${esc(f.title)}</h2>
  <p>${esc(f.detail)}</p>
  <p><strong>Action:</strong> ${esc(f.action)}</p>
  ${f.sources.length ? `<p class="meta">Sources: ${f.sources.map((u) => `<a href="${esc(u)}" rel="noopener" target="_blank">${esc(u.replace(/^https?:\/\//, '').replace(/\/$/, ''))}</a>`).join(' · ')}</p>` : ''}
</article>`).join('')}`,
});

// ---------- About ----------
layout({
  file: 'about.html',
  title: 'About, method and disclosure',
  description: 'How the site records product facts, how it measures clicks, and the disclosure it carries.',
  body: `
<h1>About, method and disclosure</h1>
<h2 class="section-h">Disclosure</h2>
<p class="notice"><strong>${esc(DISCLOSURE)}</strong> ${esc(site.not_endorsed_text)} The Associates Operating Agreement, Section 5, asks for this statement to be clearly and prominently displayed. It is shown under the masthead on every page and repeated in the footer. Sources: <a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener" target="_blank">Operating Agreement</a>; <a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers" rel="noopener" target="_blank">FTC Disclosures 101</a>.</p>
<h2 class="section-h">Sponsored links</h2>
<p>Every link to an Amazon page is marked <code>rel="sponsored"</code>. Source: <a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="noopener" target="_blank">Google Search Central</a>.</p>
<h2 class="section-h">How product facts are recorded</h2>
<ul class="plain">
  <li>Each submitted link is opened and the final URL and page title are recorded, as observed.</li>
  <li>Intended ASIN, confirmation date, price and rating are kept in separate fields. If a field cannot be confirmed from an official source, it stays blank and is marked Unverified.</li>
  <li>Claims that depend on popularity or trends are not made. Guide titles are working titles.</li>
</ul>
<h2 class="section-h">Measurement</h2>
<p>Five events are defined: ${site.measure_events.map((e) => `<code>${esc(e)}</code>`).join(', ')}. They are counted in the visitor's browser only. No cookies, no third-party scripts, and no personal data are used. A self-hosted endpoint is provided in the repository, but it is not wired to this site until an owner decides where it runs (<a href="flagged.html">FLAG-06</a>).</p>
<h2 class="section-h">Publishing gate</h2>
<p>The build (scripts/build.mjs) checks every page before publication: the disclosure is above the main content and repeated in the footer; every Amazon link is sponsored; every internal link resolves; each page has a unique title and description; banned claim words are absent; the sitemap lists every page; and the product table has a source on every row.</p>`,
});

// ---------- 404 ----------
layout({
  file: '404.html',
  title: 'Page not found',
  description: 'This page does not exist. Go back to the home page.',
  body: `<h1>Page not found</h1><p><a href="index.html">Go to the home page</a>.</p>`,
});

// ---------- Write files ----------
fs.rmSync(DOCS, { recursive: true, force: true });
fs.mkdirSync(path.join(DOCS, 'assets'), { recursive: true });
fs.mkdirSync(path.join(DOCS, 'categories'), { recursive: true });
fs.mkdirSync(path.join(DOCS, 'guides'), { recursive: true });
fs.writeFileSync(path.join(DOCS, '.nojekyll'), '');
for (const pg of pagesOut) fs.writeFileSync(path.join(DOCS, pg.file), pg.html);
fs.copyFileSync(path.join(ROOT, 'scripts', 'assets', 'site.css'), path.join(DOCS, 'assets', 'site.css'));
fs.copyFileSync(path.join(ROOT, 'scripts', 'assets', 'measure.js'), path.join(DOCS, 'assets', 'measure.js'));

const htmlFiles = pagesOut.map((p) => p.file).filter((f) => f !== '404.html');
const pubDate = (d) => new Date(d + 'T00:00:00Z').toUTCString();
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${htmlFiles.map((f) => `  <url><loc>${BASE}/${f}</loc><lastmod>${site.updated}</lastmod></url>`).join('\n')}
</urlset>
`;
fs.writeFileSync(path.join(DOCS, 'sitemap.xml'), sitemap);
const feed = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>${esc(site.name)}</title>
  <link>${BASE}/</link>
  <description>${esc(site.tagline)}</description>
  <language>en-us</language>
  <lastBuildDate>${pubDate(site.updated)}</lastBuildDate>
${guides.map((g) => `  <item>
    <title>${esc(g.title)}</title>
    <link>${BASE}/guides/${g.slug}.html</link>
    <guid isPermaLink="true">${BASE}/guides/${g.slug}.html</guid>
    <pubDate>${pubDate(g.date)}</pubDate>
    <description>${esc(g.dek)}</description>
  </item>`).join('\n')}
</channel>
</rss>
`;
fs.writeFileSync(path.join(DOCS, 'feed.xml'), feed);
fs.writeFileSync(path.join(DOCS, 'robots.txt'), `User-agent: *\nAllow: /\nSitemap: ${BASE}/sitemap.xml\n`);

// ---------- Gates ----------
const failures = [];
const fail = (msg) => failures.push(msg);
const titles = new Map();
const descs = new Map();

for (const pg of pagesOut) {
  const h = pg.html;
  const label = pg.file;
  // G1 disclosure above main and in footer
  const discIdx = h.indexOf('class="disclosure" role="note"');
  const mainIdx = h.indexOf('<main');
  const footIdx = h.indexOf('<footer');
  if (discIdx < 0 || discIdx > mainIdx) fail(`${label}: disclosure strip missing or below main content`);
  if (!h.includes(DISCLOSURE)) fail(`${label}: required disclosure sentence missing`);
  if (footIdx < 0 || !h.slice(footIdx).includes(DISCLOSURE)) fail(`${label}: disclosure not repeated in footer`);
  // G2 every link to an Amazon host is sponsored (enforced in layout(); verified here)
  for (const m of h.matchAll(/<a\b([^>]*)>/g)) {
    const attrs = m[1];
    const href = (attrs.match(/href="([^"]*)"/) || [])[1] || '';
    if (/^https?:\/\/(www\.)?(amazon\.com|link\.amazon)\b/.test(href)) {
      const rel = (attrs.match(/rel="([^"]*)"/) || [])[1] || '';
      if (!/\bsponsored\b/.test(rel)) fail(`${label}: Amazon link without rel="sponsored": ${href}`);
    }
  }
  // G3 internal links resolve
  for (const m of h.matchAll(/href="([^"#]+)(#[^"]*)?"/g)) {
    const href = m[1];
    if (/^(https?:|mailto:|tel:)/.test(href)) continue;
    const target = path.normalize(path.join(DOCS, path.dirname(pg.file), href));
    if (!target.startsWith(DOCS)) fail(`${label}: link escapes site: ${href}`);
    else if (!fs.existsSync(target)) fail(`${label}: broken internal link: ${href}`);
  }
  // G4 title / description
  const t = (h.match(/<title>([^<]*)<\/title>/) || [])[1] || '';
  const d = (h.match(/<meta name="description" content="([^"]*)"/) || [])[1] || '';
  if (!t) fail(`${label}: empty title`);
  if (!d) fail(`${label}: empty meta description`);
  if (titles.has(t)) fail(`${label}: duplicate title with ${titles.get(t)}`);
  if (descs.has(d)) fail(`${label}: duplicate description with ${descs.get(d)}`);
  titles.set(t, label);
  descs.set(d, label);
  // G5 banned claim words in visible text
  const visible = h.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<[^>]+>/g, ' ');
  const hit = visible.match(BANNED);
  if (hit) fail(`${label}: banned claim wording "${hit[0]}"`);
}
// G6 product table: every row has an official source; blanks are flagged Unverified
for (const p of products.products) {
  if (!/^https:\/\/www\.amazon\.com\//.test(p.source)) fail(`${p.id}: source is not an official Amazon listing`);
  if (!/^https:\/\/www\.amazon\.com\/dp\/B[0-9A-Z]{9}$/.test(p.official_listing_url)) fail(`${p.id}: official listing URL is not a /dp/ ASIN URL`);
  if (p.intended_asin && !ASIN_RE.test(p.intended_asin)) fail(`${p.id}: intended ASIN not in ASIN format`);
  if (!ASIN_RE.test(p.observed_asin)) fail(`${p.id}: observed ASIN not in ASIN format`);
  if (p.observed_redirect_target.includes(p.intended_asin || '\u0000')) { /* intentionally no check: intended is blank */ }
  if (p.intended_asin === p.observed_asin && !p.confirmation_date) fail(`${p.id}: intended ASIN copied from observed ASIN without confirmation`);
}
// G7 sitemap covers every page, feed has every guide
const sm = fs.readFileSync(path.join(DOCS, 'sitemap.xml'), 'utf8');
for (const f of htmlFiles) if (!sm.includes(`${BASE}/${f}`)) fail(`sitemap missing ${f}`);
const fd = fs.readFileSync(path.join(DOCS, 'feed.xml'), 'utf8');
for (const g of guides) if (!fd.includes(`guides/${g.slug}.html`)) fail(`feed missing ${g.slug}`);
// G8 no published guide without a product or category tie
for (const g of guides) if (!g.products.length || !CATEGORIES[g.category]) fail(`guide ${g.slug} has no product or category`);

if (failures.length) {
  console.error('PUBLISHING GATE FAILED:\n- ' + failures.join('\n- '));
  process.exit(1);
}
console.log(`Built ${pagesOut.length} pages into docs/. Gates passed: disclosure, sponsored links, internal links, titles and descriptions, claim wording, product table, sitemap, feed.`);
