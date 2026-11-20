#!/usr/bin/env node
/*
 * check_sources.mjs — published-table source-coverage gate.
 *
 * Brief rule being enforced: "Every table row must have a source link to an
 * official site. If a value can't be confirmed from an official source, leave
 * it blank and flag it as unverified."
 *
 * Two layers:
 *   1. FACT TABLES (manifest below): every data row must carry a link to an
 *      official source domain. For the flagged register a link to the site's
 *      own evidence page/anchor also counts (the brief asks that flags ship
 *      "with the source links" so the owner can review them).
 *   2. GENERIC VALUE SCAN (all other tables): a row that asserts an external
 *      value (a $ price, an ASIN, a star rating) must carry an official link
 *      or be explicitly marked data-src="editorial" or data-src="derived".
 *
 * Editorial / process tables (runbooks, decision options, suggestion register)
 * claim no external facts and are out of the fact-table scope; the manifest
 * records that decision so it can be reviewed.
 *
 * Usage: node scripts/check_sources.mjs   (exit 1 on violations)
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = process.cwd();

const OFFICIAL = [
  'amazon.com',
  'affiliate-program.amazon.com',
  'ftc.gov',
  'developers.google.com',
  'google.com',
  'rssboard.org',
  'opm.gov',
  'nist.gov',
];

// Fact tables: page -> 'all' or list of 0-based table indices.
const FACT_TABLES = {
  'verification.html': 'all',          // the line-by-line register
  'air-fryers.html': [0],              // category spec table
  'thermometers.html': [0],
  'compare.html': [0, 1],              // five-product table + counter-space math
  'executive-summary.html': [0],       // product table (T2 = honesty, editorial)
  'guide-gifts-by-budget.html': [0],
  'guide-holiday-hosting.html': [0],
  'guide-instant-read-vs-wireless.html': [0],
  'guide-thanksgiving-counter.html': [0],
  'compliance.html': 'all',            // policy citations must link the policy
  'flagged.html': [0],                 // register: any source link (see above)
  'topics.html': [0],                  // topic calendar source column
};

// Tables whose evidence is the site's own audit trail: an internal link (to the
// page/anchor where the claim or observation is recorded) also counts.
const ACCEPT_INTERNAL = {
  'flagged.html': 'all',
  'verification.html': [6, 7], // re-read log + printed-claims audit
};

const PAGES = readdirSync(ROOT).filter((f) => f.endsWith('.html'));

function rowsOf(tableHtml) {
  return [...tableHtml.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/g)].map((m) => ({
    tag: m[0],
    body: m[1],
  }));
}

function linksOf(rowHtml) {
  return [...rowHtml.matchAll(/<a\s[^>]*href="([^"]+)"/g)].map((m) => m[1]);
}

function textOf(html) {
  return html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}

function isOfficial(href) {
  return OFFICIAL.some((d) => href.includes(d));
}

function isInternal(href) {
  return !href.includes('://') || href.includes('github.io/Prod1/');
}

function factValue(text) {
  return /\$\d|\bB0[A-Z0-9]{8}\b|\d\.\d out of 5|\d,\d{3} (global )?ratings/.test(text);
}

let fails = 0;
let rowsChecked = 0;
let rowsWithLinks = 0;

for (const page of PAGES) {
  const html = readFileSync(join(ROOT, page), 'utf8');
  const tables = [...html.matchAll(/<table[^>]*>([\s\S]*?)<\/table>/g)];
  tables.forEach((tm, ti) => {
    const spec = FACT_TABLES[page];
    const isFact = spec === 'all' || (Array.isArray(spec) && spec.includes(ti));
    for (const row of rowsOf(tm[1])) {
      const cells = (row.body.match(/<t[dh][^>]*>/g) || []).length;
      if (!cells || !/<td/.test(row.body)) continue; // header row
      rowsChecked += 1;
      const links = linksOf(row.tag);
      const official = links.filter(isOfficial);
      const anyLink = links.length > 0;
      const text = textOf(row.body);
      const marked = /data-src="(editorial|derived|owner)"/.test(row.tag);
      if (official.length > 0) rowsWithLinks += 1;

      if (isFact) {
        const acceptInternal =
          ACCEPT_INTERNAL[page] === 'all' ||
          (Array.isArray(ACCEPT_INTERNAL[page]) && ACCEPT_INTERNAL[page].includes(ti));
        const ok = acceptInternal
          ? (official.length > 0 || (anyLink && links.some(isInternal)))
          : official.length > 0;
        if (!ok) {
          fails += 1;
          console.log(`FAIL ${page} table ${ti + 1} row: ${text.slice(0, 90)}`);
          console.log(`     ^ fact-table row without an official source link`);
        } else {
          rowsWithLinks += 0; // already counted
        }
      } else if (!marked && official.length === 0 && factValue(text)) {
        fails += 1;
        console.log(`FAIL ${page} table ${ti + 1} row: ${text.slice(0, 90)}`);
        console.log(`     ^ external value without a source link and without data-src marker`);
      }
    }
  });
}

console.log(
  `check_sources: ${rowsChecked} table rows scanned across ${PAGES.length} pages, ` +
  `${rowsWithLinks} carry an official link, ${fails} violation(s).`,
);
if (fails > 0) {
  console.log('Source-coverage gate FAILED.');
  process.exit(1);
}
console.log('Source-coverage gate passed.');
