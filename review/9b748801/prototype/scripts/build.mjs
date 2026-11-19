// Static site build. No dependencies. Node >= 18.
// Reads data/*.json and src/guides.mjs, writes docs/ (served by GitHub Pages from main:/docs).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "docs");
const SITE = "https://wingbangboozle1-lang.github.io/Prod1";
const SITE_NAME = "Countertop Check";
const UPDATED = "2026-11-19";
const DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases.";

const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), "utf8"));
const { meta, products } = readJSON("data/products.json");
const flagged = readJSON("data/flagged.json");
const questions = readJSON("data/questions.json");
const suggestions = readJSON("data/suggestions.json");
const { guides } = await import(pathToFileURL(path.join(ROOT, "src/guides.mjs")).href);

const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const CAT = { "air-fryers": "Air fryers", "meat-thermometers": "Meat thermometers" };
const blank = (v, flag) => (v ? esc(v) : `<span class="unv">${flag || "Unverified — blank"}</span>`);

// ---------- page registry ----------
const pages = [];
function addPage(p) {
  pages.push({ indent: 0, sitemap: true, ...p });
}

// relative prefix from a page's output path (e.g. "products/index.html" -> "../")
const depthPrefix = (rel) => {
  const d = rel.split("/").length - 1;
  return d === 0 ? "./" : "../".repeat(d);
};
// href from a page to a site path like "products/" (trailing slash = directory)
// Placeholder resolved per page at write time (bodies are built before their page is known).
const href = (to) => "{{R}}" + to.replace(/^\//, "");

const outbound = (p, label) =>
  `<a class="btn btn-buy" href="${esc(p.submitted_link)}" rel="sponsored noopener noreferrer" target="_blank" data-outbound="${p.id}">${esc(label)} <span class="sr">(sponsored link to Amazon)</span></a>`;

const navItems = [
  ["products/", "Products"],
  ["categories/air-fryers/", "Air fryers"],
  ["categories/meat-thermometers/", "Meat thermometers"],
  ["guides/", "Guides"],
  ["about/", "About"],
];
const dashboards = [
  ["products/", "All products table"],
  ["analysis/", "Analysis"],
  ["verification/", "Verification"],
  ["campaigns/", "Campaign ledger"],
  ["measurement/", "Measurement"],
  ["suggestions/", "Suggestions"],
  ["open-questions/", "Open questions"],
  ["flagged/", "Flagged for Review"],
  ["executive-summary/", "Executive summary"],
  ["disclosure/", "Disclosure & policy"],
];

function layout({ rel, title, description, body, jsonld = null, type = "website" }) {
  const canonicalPath = rel === "index.html" ? "" : rel.replace(/index\.html$/, "");
  const canonical = `${SITE}/${canonicalPath}`;
  const fullTitle = rel === "index.html" ? `${SITE_NAME} — Air fryers and meat thermometers, checked against their listings` : `${title} · ${SITE_NAME}`;
  const navHtml = navItems
    .map(([to, label]) => `<a href="${href(to)}">${esc(label)}</a>`)
    .join("");
  const footDash = dashboards.map(([to, label]) => `<li><a href="${href(to)}">${esc(label)}</a></li>`).join("");
  const ld = jsonld ? `<script type="application/ld+json">${JSON.stringify(jsonld)}</script>` : "";
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${esc(canonical)}">
<meta property="og:type" content="${esc(type)}">
<meta property="og:site_name" content="${esc(SITE_NAME)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${esc(canonical)}">
<meta name="twitter:card" content="summary">
<meta name="analytics-endpoint" content="">
<link rel="stylesheet" href="${href("assets/site.css")}">
<link rel="alternate" type="application/rss+xml" title="${esc(SITE_NAME)} guides" href="${SITE}/rss.xml">
${ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap mast-inner">
    <a class="brand" href="${href("")}">${esc(SITE_NAME)}</a>
    <p class="tagline">Air fryers and meat thermometers, read from their Amazon listings</p>
  </div>
  <nav class="nav" aria-label="Main">
    <div class="wrap">${navHtml}</div>
  </nav>
</header>
<div class="disclosure" role="note">
  <div class="wrap"><strong>Disclosure:</strong> ${esc(DISCLOSURE)} Some links on this site are affiliate links, marked “sponsored”.</div>
</div>
<main id="main" class="wrap">
${body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="disclosure-foot"><strong>Disclosure:</strong> ${esc(DISCLOSURE)} Links marked “sponsored” go to Amazon and may earn us a commission.</div>
    <div class="foot-grid">
      <div>
        <h2>Dashboards</h2>
        <ul class="foot-list">${footDash}</ul>
      </div>
      <div>
        <h2>Site</h2>
        <ul class="foot-list">
          <li><a href="${href("guides/")}">Guides</a></li>
          <li><a href="${href("about/")}">About</a></li>
          <li><a href="${SITE}/rss.xml">RSS feed</a></li>
          <li><a href="${SITE}/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
    </div>
    <p class="small">Data last checked ${UPDATED}. Values not confirmed from an official source are left blank and marked unverified. Amazon and other product names are trademarks of their owners; this site is not affiliated with them.</p>
  </div>
</footer>
<script src="${href("assets/analytics.js")}" defer></script>
</body>
</html>
`;
}

// ---------- shared components ----------
function productTable(list) {
  const head = `<tr>
<th>ID</th><th>Product (as listed)</th><th>Category</th><th>Capacity / spec (as listed in title)</th>
<th>Intended ASIN</th><th>Observed ASIN (redirect target)</th><th>Price</th><th>Rating</th>
<th>Confirmed</th><th>Source (official listing)</th><th>Submitted link</th></tr>`;
  const rows = list
    .map(
      (p) => `<tr id="${esc(p.id)}">
<td><strong>${esc(p.id)}</strong></td>
<td><span class="ptitle">${esc(p.title_as_listed)}</span></td>
<td>${esc(CAT[p.category])}</td>
<td>${esc(p.capacity_as_listed)}</td>
<td>${blank(p.intended_asin, "Unverified — blank (FL-02)")}</td>
<td><code>${esc(p.observed_redirect_asin)}</code></td>
<td>${blank(p.price_observed, "Unverified — blank (FL-06)")}</td>
<td>${blank(p.rating_observed, "Unverified — blank (FL-06)")}</td>
<td>${esc(p.confirmation_date)}</td>
<td><a href="${esc(p.source_url)}" rel="noopener" target="_blank">amazon.com/dp/${esc(p.observed_redirect_asin)}</a></td>
<td><a href="${esc(p.submitted_link)}" rel="sponsored noopener noreferrer" target="_blank" data-outbound="${p.id}">link.amazon/${esc(p.submitted_code)}</a></td>
</tr>`
    )
    .join("");
  return `<div class="table-scroll"><table class="data"><thead>${head}</thead><tbody>${rows}</tbody></table></div>`;
}

function productCards(list) {
  return `<div class="cards">${list
    .map(
      (p) => `<article class="card">
<p class="kicker">${esc(CAT[p.category])}</p>
<h3>${esc(p.short_name)}</h3>
<p class="spec">${esc(p.capacity_as_listed)}</p>
<p class="meta">Observed ASIN <code>${esc(p.observed_redirect_asin)}</code> · Price and rating: unverified, not shown</p>
<p>${outbound(p, "View on Amazon")}</p>
<p class="small"><a href="${href(`products/#${p.id}`)}">Full record and source</a></p>
</article>`
    )
    .join("")}</div>`;
}

const guideCard = (g) => `<li><a href="${href(`guides/${g.slug}/`)}">${esc(g.title)}</a>
<span class="small"> — ${esc(g.summary)}</span></li>`;

const pill = (sev) => `<span class="pill pill-${esc(sev.toLowerCase())}">${esc(sev)}</span>`;

// ---------- pages ----------
const byCat = (c) => products.filter((p) => p.category === c);
const flagCount = flagged.items.filter((f) => f.type !== "Verified").length;

// home
addPage({
  rel: "index.html",
  title: "Home",
  description: "Five Amazon listings for air fryers and meat thermometers, with the details each listing states, the source for each one, and what is still unverified.",
  body: `
<section class="hero">
  <p class="kicker">Front page · Updated ${UPDATED}</p>
  <h1>Five listings, read closely.</h1>
  <p class="lede">Air fryers and meat thermometers, with what each Amazon listing actually states. Every figure links to its listing. Anything we could not confirm is left blank.</p>
  <p class="cta-row">
    <a class="btn" href="#products">See the products</a>
    <a class="btn btn-ghost" href="${href("guides/")}">Read the guides</a>
  </p>
</section>
<section id="products" class="block">
  <h2>The products</h2>
  ${productCards(products)}
</section>
<section class="block tiles">
  <h2>Shop by category</h2>
  <div class="cards two">
    <a class="tile" href="${href("categories/air-fryers/")}"><span class="kicker">${byCat("air-fryers").length} products</span><h3>Air fryers and ovens</h3><p>Basket and oven-style models, with the capacity each listing states.</p></a>
    <a class="tile" href="${href("categories/meat-thermometers/")}"><span class="kicker">${byCat("meat-thermometers").length} products</span><h3>Meat thermometers</h3><p>Accuracy, response time and probe count, as printed on the listing.</p></a>
  </div>
</section>
<section class="block">
  <h2>Latest guides</h2>
  <ul class="plain">${guides.slice(0, 3).map(guideCard).join("")}</ul>
  <p><a href="${href("guides/")}">All guides →</a></p>
</section>
<section class="block note">
  <h2>What we did not confirm</h2>
  <p>Prices, star ratings, item dimensions and commission rates are not shown because they could not be confirmed from an official source. The intended ASIN for each product is also blank. ${flagCount} items are on the <a href="${href("flagged/")}">Flagged for Review</a> page with source links.</p>
  <p><a href="${href("executive-summary/")}">Read the executive summary →</a></p>
</section>`,
  jsonld: {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: SITE_NAME,
    url: `${SITE}/`,
    description: "Air fryers and meat thermometers, read from their Amazon listings.",
  },
});

// products (dashboard)
addPage({
  rel: "products/index.html",
  title: "All products",
  description: "Every submitted product with its observed Amazon ASIN, listing source, title-as-listed and verification status. Unverified fields are blank.",
  body: `
<h1>All products</h1>
<p class="lede">The five products from the submitted links. Each row links to its official Amazon listing. Blank cells are unverified and flagged.</p>
<p class="small">Columns read from left to right: what the listing says, what we could confirm, and where it came from. Intended ASIN is blank for every row because the submitted codes could not be confirmed (see <a href="${href("flagged/")}">FL-01 and FL-02</a>).</p>
${productTable(products)}
<section class="block">
  <h2>How each row was built</h2>
  <ul class="plain">
    <li>Each submitted link was opened and the final Amazon URL recorded (observed redirect target).</li>
    <li>The product title and breadcrumb were read from that page. Capacity values come only from the title.</li>
    <li>Price and rating of the main product were not in the fetched text and are blank.</li>
    <li>Confirmation date: ${UPDATED}.</li>
  </ul>
</section>`,
});

// categories
for (const c of ["air-fryers", "meat-thermometers"]) {
  const list = byCat(c);
  const catGuides = guides.filter((g) => g.category === c);
  const analysisLine =
    c === "air-fryers"
      ? `Listed capacities: ${list.map((p) => p.capacity_as_listed.split(";")[0]).join("; ")}. Dimensions are not confirmed, so no counter-space figure is calculated.`
      : `Listed features (title only): ${list.map((p) => p.short_name + ": " + p.capacity_as_listed).join(" | ")}. Accuracy is quoted from titles, not tested.`;
  addPage({
    rel: `categories/${c}/index.html`,
    title: CAT[c],
    description: `${CAT[c]} from the submitted set: product table with listed specs, sources, and guides for choosing.`,
    body: `
<p class="kicker"><a href="${href("products/")}">All products</a> · Category</p>
<h1>${esc(CAT[c])}</h1>
<p class="lede">${c === "air-fryers" ? "Three air fryers and ovens from the submitted set. Use the capacity line as a starting point, then check dimensions on the listing." : "Two meat thermometers from the submitted set. Compare the accuracy and probe claims as printed, then check the certification wording."}</p>
${productCards(list)}
<section class="block">
  <h2>Comparison table</h2>
  ${productTable(list)}
</section>
<section class="block note">
  <h2>Analysis</h2>
  <p>${esc(analysisLine)}</p>
  <p class="small">Prices and ratings are not compared because neither was confirmed.</p>
</section>
<section class="block">
  <h2>Guides for this category</h2>
  <ul class="plain">${catGuides.map(guideCard).join("")}</ul>
</section>`,
  });
}

// guides index
addPage({
  rel: "guides/index.html",
  title: "Guides",
  description: "Question-shaped buying guides for air fryers and meat thermometers. Each guide sticks to what listings state and says what it does not know.",
  body: `
<h1>Guides</h1>
<p class="lede">Questions people ask before buying, answered with what the listings state. These are working titles. They are not claims about popularity or search demand.</p>
<ul class="plain guide-list">${guides.map(guideCard).join("")}</ul>`,
});

// guide pages
for (const g of guides) {
  const bodyHtml = g.body
    .map(([t, v]) => {
      if (t === "p") return `<p>${esc(v)}</p>`;
      if (t === "h2") return `<h2>${esc(v)}</h2>`;
      if (t === "ul") return `<ul>${v.map((i) => `<li>${esc(i)}</li>`).join("")}</ul>`;
      return "";
    })
    .join("\n");
  const rel = `guides/${g.slug}/index.html`;
  const related = products.filter((p) => p.category === g.category);
  addPage({
    rel,
    title: g.title,
    description: g.description,
    type: "article",
    body: `
<p class="kicker"><a href="${href("guides/")}">Guides</a> · Working title</p>
<article class="article">
<h1>${esc(g.title)}</h1>
<p class="byline small">By Editorial team · Published ${esc(g.date)} · Checked against listings ${UPDATED}</p>
${bodyHtml}
<section class="block note">
  <h2>Products in this category</h2>
  <ul class="plain">${related.map((p) => `<li>${esc(p.short_name)} — ${outbound(p, "View on Amazon")} <span class="small">· <a href="${href(`products/#${p.id}`)}">record</a></span></li>`).join("")}</ul>
  <p class="small">Links marked “sponsored” go to Amazon. ${esc(DISCLOSURE)}</p>
</section>
</article>
<p><a href="${href(`categories/${g.category}/`)}">← Back to ${esc(CAT[g.category])}</a></p>`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: g.title,
      description: g.description,
      datePublished: g.date,
      dateModified: UPDATED,
      author: { "@type": "Organization", name: "Editorial team" },
      publisher: { "@type": "Organization", name: SITE_NAME },
      mainEntityOfPage: `${SITE}/${rel.replace(/index\.html$/, "")}`,
    },
  });
}

// analysis
const observedAsins = products.map((p) => p.observed_redirect_asin);
const uniqueAsins = new Set(observedAsins).size;
const withTag = 0; // none of the observed redirect URLs contained tag=
addPage({
  rel: "analysis/index.html",
  title: "Analysis",
  description: "What the five listings show, counted from the verified fields, and what cannot yet be calculated.",
  body: `
<h1>Analysis</h1>
<p class="lede">Counts below come from the verified fields in the product table. Nothing here is a forecast or a ranking.</p>
<div class="table-scroll"><table class="data">
<thead><tr><th>Measure</th><th>Result</th><th>Basis</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Products in scope</td><td>${products.length}</td><td>Submitted links</td><td><a href="${href("products/")}">Products table</a></td></tr>
<tr><td>Distinct observed ASINs</td><td>${uniqueAsins} of ${products.length}</td><td>Final URL of each fetch</td><td><a href="https://www.amazon.com/dp/B0CDY277D3">P01 listing</a></td></tr>
<tr><td>Submitted codes that are 10 characters</td><td>0 of ${products.length}</td><td>Length of code after link.amazon/</td><td><a href="${href("flagged/")}">FL-01, FL-03</a></td></tr>
<tr><td>Intended ASINs confirmed</td><td>0 of ${products.length}</td><td>Submitter confirmation not received</td><td><a href="${href("flagged/")}">FL-02</a></td></tr>
<tr><td>Observed redirect URLs containing tag=shopnow047c-20</td><td>${withTag} of ${products.length}</td><td>Query string of each final URL as read on ${UPDATED}</td><td><a href="${href("flagged/")}">FL-04</a></td></tr>
<tr><td>Prices confirmed for the main product</td><td>0 of ${products.length}</td><td>Fetched listing text</td><td><a href="${href("flagged/")}">FL-06</a></td></tr>
<tr><td>Star ratings confirmed for the main product</td><td>0 of ${products.length}</td><td>Fetched listing text</td><td><a href="${href("flagged/")}">FL-06</a></td></tr>
<tr><td>Air fryers: listed capacity (title)</td><td>${byCat("air-fryers").map((p) => p.capacity_as_listed.split(";")[0]).join(", ")}</td><td>Product titles</td><td><a href="${href("categories/air-fryers/")}">Air fryers</a></td></tr>
<tr><td>Thermometers: listed accuracy (title)</td><td>±0.5℉ (P04); not stated in P05's title</td><td>Product titles</td><td><a href="${href("categories/meat-thermometers/")}">Meat thermometers</a></td></tr>
</tbody></table></div>
<section class="block note">
  <h2>What cannot be calculated yet</h2>
  <ul class="plain">
    <li><strong>Capacity per centimetre of counter depth</strong> — needs confirmed dimensions (Q-06).</li>
    <li><strong>Price comparison or value ranking</strong> — needs confirmed prices with dates (Q-04).</li>
    <li><strong>Commission potential</strong> — needs the official rate schedule (Q-08, FL-16).</li>
    <li><strong>Which guide topic draws readers</strong> — needs search and click data (Q-07).</li>
  </ul>
</section>`,
});

// verification
addPage({
  rel: "verification/index.html",
  title: "Verification",
  description: "How each product row was checked, which checks passed, and which fields are blank because they could not be confirmed from an official source.",
  body: `
<h1>Verification</h1>
<p class="lede">Each row was checked against the official Amazon listing it resolved to. Checks that did not pass are marked, not filled in.</p>
<div class="table-scroll"><table class="data">
<thead><tr><th>ID</th><th>Final URL is amazon.com listing</th><th>Title read from page</th><th>Breadcrumb read</th><th>Intended ASIN confirmed</th><th>Price confirmed</th><th>Rating confirmed</th><th>Tracking tag seen in redirect</th><th>Source</th></tr></thead>
<tbody>
${products
  .map(
    (p) => `<tr><td><strong>${esc(p.id)}</strong></td><td>✓</td><td>✓</td><td>✓</td><td><span class="unv">✗ blank</span></td><td><span class="unv">✗ blank</span></td><td><span class="unv">✗ blank</span></td><td><span class="unv">✗ not seen</span></td><td><a href="${esc(p.source_url)}" rel="noopener" target="_blank">${esc(p.source_url)}</a></td></tr>`
  )
  .join("")}
</tbody></table></div>
<section class="block">
  <h2>Sources used</h2>
  <ul class="plain">
    <li><a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener" target="_blank">Associates Program Operating Agreement (official)</a> — section 1 (Special Links) and section 5 (disclosure statement).</li>
    <li><a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="noopener" target="_blank">Google Search Central: qualify your outbound links (official)</a> — rel="sponsored".</li>
    <li><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers" rel="noopener" target="_blank">FTC: Disclosures 101 for Social Media Influencers</a> — read; see FL-10.</li>
    <li>Amazon listing pages for each product (linked in the table).</li>
  </ul>
  <p class="small">Third-party pages were consulted for the ASIN length rule only and are flagged as non-official (FL-03).</p>
</section>`,
});

// campaigns (empty ledger)
addPage({
  rel: "campaigns/index.html",
  title: "Campaign ledger",
  description: "The campaign ledger starts empty. Rows are added only from authorized first-party reports with a dated provenance trail.",
  body: `
<h1>Campaign ledger</h1>
<p class="lede">Empty by design. A row is added only when a figure comes from an authorized first-party report, with its date and source. No conversion score or revenue forecast is shown.</p>
<div class="table-scroll"><table class="data">
<thead><tr><th>Timestamp</th><th>Source (report name)</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th><th>Reported orders</th><th>Provenance note</th></tr></thead>
<tbody><tr><td colspan="7" class="empty">No authorized first-party report imported yet. Blank is not zero.</td></tr></tbody>
</table></div>`,
});

// measurement
addPage({
  rel: "measurement/index.html",
  title: "Measurement",
  description: "Privacy-preserving outbound-click counter and proposed events. Nothing is sent until an analytics endpoint is configured.",
  body: `
<h1>Measurement</h1>
<p class="lede">Clicks on Amazon links are recorded as named events. No cookies, no local storage, no fingerprinting. Nothing leaves the browser unless an endpoint is set in the page head.</p>
<div class="table-scroll"><table class="data">
<thead><tr><th>Event (proposed, FL-13)</th><th>Fires when</th><th>Data kept</th><th>Status</th></tr></thead>
<tbody>
<tr><td><code>page_view</code></td><td>A page loads</td><td>Page path, time</td><td>Wired; not sent (no endpoint)</td></tr>
<tr><td><code>outbound_click</code></td><td>A sponsored product link is clicked</td><td>Product ID, path, time</td><td>Wired; not sent (no endpoint)</td></tr>
<tr><td><code>category_open</code></td><td>A category page loads</td><td>Category, time</td><td>Wired; not sent (no endpoint)</td></tr>
<tr><td><code>guide_view</code></td><td>A guide page loads</td><td>Guide slug, time</td><td>Wired; not sent (no endpoint)</td></tr>
<tr><td><code>flagged_view</code></td><td>The Flagged for Review page loads</td><td>Time</td><td>Wired; not sent (no endpoint)</td></tr>
</tbody></table></div>
<section class="block note">
  <h2>Endpoint</h2>
  <p>GitHub Pages is static hosting and cannot run a self-hosted analytics endpoint. To turn events on, set the <code>analytics-endpoint</code> meta tag on each page to an HTTPS URL you control (see Suggestion S-05). Until then, the counter records to memory only.</p>
</section>`,
});

// suggestions
addPage({
  rel: "suggestions/index.html",
  title: "Suggestions",
  description: "Suggestions for review, with options. Nothing here has been implemented; choose a path first.",
  body: `
<h1>Suggestions</h1>
<p class="lede">${esc(suggestions.intro)}</p>
<div class="table-scroll"><table class="data">
<thead><tr><th>ID</th><th>Topic</th><th>Suggestion</th><th>Why</th><th>Options</th><th>Your choice</th><th>Status</th></tr></thead>
<tbody>
${suggestions.items
  .map(
    (s) => `<tr><td><strong>${esc(s.id)}</strong></td><td>${esc(s.topic)}</td><td>${esc(s.suggestion)}</td><td>${esc(s.why)}</td><td><ol class="opts">${s.options
      .map((o) => `<li><strong>${esc(o.id)}.</strong> ${esc(o.label)}<br><span class="small">${esc(o.note)}</span></li>`)
      .join("")}</ol></td><td>${s.decision ? esc(s.decision) : "—"}</td><td><span class="pill pill-open">Awaiting selection</span></td></tr>`
  )
  .join("")}
</tbody></table></div>`,
});

// open questions
addPage({
  rel: "open-questions/index.html",
  title: "Open questions",
  description: "Questions that must be answered before decisions are made: what is known, what is missing, and how to find out.",
  body: `
<h1>Open questions</h1>
<p class="lede">${esc(questions.intro)}</p>
<div class="table-scroll"><table class="data">
<thead><tr><th>ID</th><th>Area</th><th>Question</th><th>Known</th><th>Missing</th><th>How to find out</th><th>Source</th></tr></thead>
<tbody>
${questions.items
  .map(
    (q) => `<tr><td><strong>${esc(q.id)}</strong></td><td>${esc(q.area)}</td><td>${esc(q.question)}</td><td>${esc(q.known)}</td><td>${esc(q.missing)}</td><td>${esc(q.how_to_find)}</td><td><a href="${esc(q.source)}" rel="noopener" target="_blank">link</a></td></tr>`
  )
  .join("")}
</tbody></table></div>`,
});

// flagged
addPage({
  rel: "flagged/index.html",
  title: "Flagged for Review",
  description: "Irregularities, unverified items and pending decisions from the repository review, each with its source link for manual review.",
  body: `
<h1>Flagged for Review</h1>
<p class="lede">Items here do not block publication. Each one says what was checked, what was not, and where to look. Request changes against these IDs.</p>
<p class="small">Counts: ${flagged.items.length} items · ${flagged.items.filter((f) => f.severity === "High").length} high severity.</p>
${flagged.items
  .map(
    (f) => `<article class="flag" id="${esc(f.id)}">
<header><span class="flag-id">${esc(f.id)}</span> ${pill(f.severity)} <span class="pill">${esc(f.type)}</span></header>
<h2>${esc(f.title)}</h2>
<p>${esc(f.detail)}</p>
<dl class="small">
<dt>Checked</dt><dd>${esc(f.checked)}</dd>
<dt>Not checked</dt><dd>${esc(f.not_checked)}</dd>
</dl>
${f.sources.length ? `<p class="small"><strong>Sources:</strong> ${f.sources.map((s) => `<a href="${esc(s.url)}" rel="noopener" target="_blank">${esc(s.label)}</a>`).join(" · ")}</p>` : `<p class="small"><strong>Sources:</strong> none in this session.</p>`}
</article>`
  )
  .join("")}
<p class="small">Updated ${flagged.updated}. ${esc(flagged.note)}</p>`,
});

// executive summary
addPage({
  rel: "executive-summary/index.html",
  title: "Executive summary",
  description: "Executive summary: what the site contains, what was verified, what is blocked, and what needs a decision.",
  body: `
<h1>Executive summary</h1>
<p class="lede">A static, sponsored-link product site for five submitted Amazon listings, built from verified fields only. Two things keep it from being a complete affiliate operation: the link format and the tracking attribution are unconfirmed, and several decisions are still open.</p>
<section class="block">
  <h2>What exists</h2>
  <ul class="plain">
    <li>A front page, a products table, two category pages, five guides, and dashboards for analysis, verification, the campaign ledger, measurement, suggestions, open questions, Flagged for Review, and this summary.</li>
    <li>Every outbound product link is marked <code>rel="sponsored"</code>, following Google's documentation. The disclosure strip sits under the masthead of every page and is repeated in the footer.</li>
  </ul>
</section>
<section class="block">
  <h2>What was verified</h2>
  <ul class="plain">
    <li>All five submitted links resolve to amazon.com listings. Observed ASINs: ${products.map((p) => `<code>${esc(p.observed_redirect_asin)}</code>`).join(", ")}.</li>
    <li>Titles and breadcrumbs were read from each listing. Capacity and accuracy values come only from titles.</li>
    <li>Amazon's Operating Agreement section 5 disclosure wording is confirmed and used.</li>
    <li>The FTC Disclosures 101 brochure was read. It asks for disclosures that are hard to miss and placed with the endorsement (FL-10).</li>
  </ul>
</section>
<section class="block">
  <h2>What is not verified (left blank, flagged)</h2>
  <ul class="plain">
    <li>Intended ASINs: the submitted codes are 9 characters, and none has been confirmed as intended (FL-01, FL-02).</li>
    <li>Tracking attribution: none of the five redirect URLs carries <code>tag=shopnow047c-20</code> (FL-04).</li>
    <li>Special Link status of the short links: unresolved, not claimed invalid; requires an Associates test (FL-05).</li>
    <li>Prices, ratings, dimensions, commission rates (FL-06, FL-08, FL-16).</li>
  </ul>
</section>
<section class="block">
  <h2>What needs a decision</h2>
  <p>See <a href="${href("suggestions/")}">Suggestions</a> (ten items, options only). The first is S-01: test one Special Link per product before scaling. Brand, byline, cadence, analytics endpoint, imagery and price display are also open.</p>
</section>
<section class="block">
  <h2>What is not possible from here</h2>
  <ul class="plain">
    <li>Logging in to Associates or Search Console (manual).</li>
    <li>Running the analytics endpoint on static hosting (needs a server you choose).</li>
    <li>Reading the external source register in Zone3 / Zone4 (not in this repository; FL-12).</li>
  </ul>
</section>
<section class="block">
  <h2>Publishing cadence and measurement</h2>
  <p>Cadence has not been set (S-04). Guide topics should be chosen from measured queries once Search Console and the endpoint have data for 8 to 12 weeks (Q-07).</p>
</section>`,
});

// disclosure
addPage({
  rel: "disclosure/index.html",
  title: "Disclosure & policy",
  description: "The Amazon Associates statement, how affiliate links are marked, and the policy notes that apply to this site.",
  body: `
<h1>Disclosure &amp; policy</h1>
<p class="lede">Amazon's Operating Agreement (section 5) requires this statement, or a substantially similar one, on the site:</p>
<blockquote class="statement">“${esc(DISCLOSURE)}”</blockquote>
<section class="block">
  <h2>How links are marked</h2>
  <ul class="plain">
    <li>Every link to an Amazon product is marked <code>rel="sponsored noopener noreferrer"</code>. Google's documentation asks for <code>rel="sponsored"</code> on paid or affiliate links (<a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="noopener" target="_blank">source</a>).</li>
    <li>Links point to the supplied short links. They are not rewritten. Whether they are valid Special Links is unresolved (FL-05).</li>
    <li>Prices and ratings are not shown. Where they appear later, they must come from an official, dated source.</li>
  </ul>
</section>
<section class="block">
  <h2>Amazon content notice (proposed, FL-20)</h2>
<p class="small">Proposed by the external Zone4 register. Included as a proposal until the IP License section 2(k) is read and a reviewer decides:</p>
<blockquote class="statement">Certain content that appears on this site comes from Amazon. This content is provided “as is” and is subject to change or removal at any time.</blockquote>
<h2>Sources for this page</h2>
  <ul class="plain">
    <li><a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="noopener" target="_blank">Associates Program Operating Agreement, section 5 (official)</a></li>
    <li><a href="https://affiliate-program.amazon.com/help/operating/policies" rel="noopener" target="_blank">Associates Program Policies (official; opening part read, FL-11)</a></li>
    <li><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers" rel="noopener" target="_blank">FTC: Disclosures 101 (read; applicability is a reviewer decision, FL-10)</a></li>
  </ul>
</section>`,
});

// about
addPage({
  rel: "about/index.html",
  title: "About",
  description: "About Countertop Check: how the site is built, who writes it, and what it does and does not claim.",
  body: `
<h1>About</h1>
<p class="lede">${esc(SITE_NAME)} is a working name for this site (FL-14). It reads five Amazon listings closely and reports what each one says.</p>
<section class="block">
  <h2>Method</h2>
  <ul class="plain">
    <li>Only fields confirmed from a page we read are shown. Everything else is blank and flagged.</li>
    <li>Guides use the listing wording and say what they do not know.</li>
    <li>Suggestions and open questions are listed for review. Nothing is changed on the strength of a suggestion alone.</li>
  </ul>
</section>
<section class="block">
  <h2>Byline</h2>
  <p>Articles are credited to the “Editorial team”. No individual author is named. A named author can be added after a decision (S-03).</p>
</section>
<section class="block">
  <h2>Affiliation</h2>
  <p>This site is not affiliated with Amazon, Chefman, Emeril Lagasse, Nutrichef, ThermoMaven, CHEF iQ or any other brand named here. Product names are the owners' trademarks.</p>
</section>`,
});

// 404
addPage({
  rel: "404.html",
  title: "Page not found",
  description: "This page does not exist.",
  sitemap: false,
  body: `<h1>Page not found</h1><p>The page you asked for is not here. Try the <a href="${href("products/")}">products table</a> or the <a href="${href("guides/")}">guides</a>.</p>`,
});

// ---------- write ----------
function writeFile(rel, content) {
  const full = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content);
}

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, ".nojekyll"), "");
fs.mkdirSync(path.join(OUT, "assets"), { recursive: true });
fs.copyFileSync(path.join(ROOT, "src/assets/site.css"), path.join(OUT, "assets/site.css"));
fs.copyFileSync(path.join(ROOT, "src/assets/analytics.js"), path.join(OUT, "assets/analytics.js"));

// Amazon links anywhere on the site must be sponsored + noopener (compliance gate).
function normalizeAmazonLinks(html) {
  return html.replace(/<a\s([^>]*?)>/g, (full, attrs) => {
    if (!/href="https?:\/\/(?:www\.)?(?:amazon\.com|link\.amazon)[^"]*"/.test(attrs)) return full;
    const rest = attrs.replace(/\srel="[^"]*"/, "");
    return `<a ${rest} rel="sponsored noopener noreferrer">`;
  });
}

for (const p of pages) {
  const html = normalizeAmazonLinks(layout(p)).replaceAll("{{R}}", depthPrefix(p.rel));
  writeFile(p.rel, html);
}

// sitemap
const urls = pages
  .filter((p) => p.sitemap)
  .map((p) => `${SITE}/${p.rel === "index.html" ? "" : p.rel.replace(/index\.html$/, "")}`);
writeFile(
  "sitemap.xml",
  `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url><loc>${esc(u)}</loc><lastmod>${UPDATED}</lastmod></url>`).join("\n")}
</urlset>
`
);
writeFile("robots.txt", `User-agent: *\nAllow: /\n\nSitemap: ${SITE}/sitemap.xml\n`);

// RSS (guides)
const rfc822 = (d) => new Date(d + "T00:00:00Z").toUTCString();
writeFile(
  "rss.xml",
  `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>${esc(SITE_NAME)} — guides</title>
<link>${SITE}/</link>
<description>Question-shaped buying guides for air fryers and meat thermometers.</description>
<language>en-us</language>
<lastBuildDate>${rfc822(UPDATED)}</lastBuildDate>
${guides
  .map(
    (g) => `<item>
<title>${esc(g.title)}</title>
<link>${SITE}/guides/${g.slug}/</link>
<guid isPermaLink="true">${SITE}/guides/${g.slug}/</guid>
<pubDate>${rfc822(g.date)}</pubDate>
<description>${esc(g.description)}</description>
</item>`
  )
  .join("\n")}
</channel>
</rss>
`
);

console.log(`built ${pages.length} pages, ${urls.length} sitemap urls -> docs/`);
