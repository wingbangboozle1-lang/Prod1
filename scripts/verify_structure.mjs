#!/usr/bin/env node
/* Structural verification of the built pages.
 *
 * Why: this sandbox cannot download a browser, so visual review is impossible here. What can
 * be checked mechanically is structure - that the document parses, that every image and
 * stylesheet it points at exists, that the type it asks for is on disk, that headings are in
 * order, that the disclosure really is above `</main>`, and that nothing overflows its column
 * by construction (fixed-width children inside a grid).
 *
 * It is a proof of structure, not of taste. Say so wherever it is reported.
 *
 * Usage: node scripts/verify_structure.mjs [--root DIR]
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = process.argv.includes("--root") ? process.argv[process.argv.indexOf("--root") + 1] : process.cwd();
const pages = readdirSync(ROOT).filter((f) => f.endsWith(".html"));
const fails = [];
const warns = [];
const fail = (m) => fails.push(m);
const warn = (m) => warns.push(m);

const DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases.";

/* ---------- a small tag balance walker: enough to catch an unclosed section ---------- */
const VOID = new Set(["area", "base", "br", "col", "embed", "hr", "img", "input", "link",
  "meta", "param", "source", "track", "wbr", "path", "rect", "circle", "line", "polyline",
  "polygon", "ellipse", "use", "stop"]);

const untagged = {};

for (const page of pages) {
  const html = readFileSync(join(ROOT, page), "utf8");
  const body = html.slice(html.indexOf("<body"), html.indexOf("</body>"));

  /* 1. tag balance over the body */
  const stack = [];
  const tagRe = /<(\/?)([a-zA-Z][a-zA-Z0-9:-]*)([^>]*?)(\/?)>/g;
  let m;
  while ((m = tagRe.exec(body))) {
    const [, closing, name, attrs, selfClose] = m;
    const tag = name.toLowerCase();
    if (tag === "script" || tag === "style") {
      if (!closing) {
        const end = body.indexOf(`</${tag}>`, tagRe.lastIndex);
        if (end === -1) { fail(`${page}: <${tag}> is never closed`); break; }
        tagRe.lastIndex = end + tag.length + 3;
      }
      continue;
    }
    if (VOID.has(tag) || selfClose) continue;
    if (closing) {
      const last = stack.pop();
      if (last !== tag) { fail(`${page}: </${tag}> closes <${last || "nothing"}> - tags are not nested`); break; }
    } else stack.push(tag);
  }
  const openLeft = stack.filter((t) => t !== "body"); // the slice stops before </body>
  if (openLeft.length) warn(`${page}: ${openLeft.length} tag(s) left open at end of body: ${openLeft.slice(-3).join(", ")}`);

  /* 2. every local asset it points at exists */
  for (const a of html.matchAll(/(?:href|src)="([^"#:]+\.(?:css|js|svg|png|jpg|woff2|json|xml))"/g)) {
    const rel = a[1].replace(/^.*\/(?=(assets|data)\/)/, "");
    if (!existsSync(join(ROOT, rel))) fail(`${page}: references ${rel}, which does not exist`);
  }

  /* 3. the disclosure is above </main> and repeated in the footer */
  const stripAt = body.indexOf("disclosure-strip");
  const mainEnd = body.indexOf("</main>");
  if (stripAt === -1) fail(`${page}: no disclosure strip`);
  else if (mainEnd > -1 && stripAt > mainEnd) fail(`${page}: disclosure strip is below </main>`);
  if (!body.includes(DISCLOSURE)) fail(`${page}: exact Operating Agreement sentence missing`);
  if (!/<footer[\s\S]*?disclosure-strip/.test(body)) fail(`${page}: disclosure not repeated in the footer`);

  /* 4. one h1, in order */
  const h1s = (body.match(/<h1[\s>]/g) || []).length;
  if (h1s !== 1) fail(`${page}: ${h1s} <h1> elements - a page needs exactly one`);
  const levels = [...body.matchAll(/<h([1-6])[\s>]/g)].map((x) => Number(x[1]));
  for (let i = 1; i < levels.length; i++) {
    if (levels[i] - levels[i - 1] > 1) { warn(`${page}: heading jumps h${levels[i - 1]} to h${levels[i]}`); break; }
  }

  /* 5. a screen reader needs every image to have a decision made about it */
  for (const img of html.matchAll(/<img\b[^>]*>/g)) {
    if (!/\balt=/.test(img[0])) fail(`${page}: <img> with no alt attribute (write alt="" if decorative) -> ${img[0].slice(0, 70)}`);
    if (!/\bwidth=/.test(img[0]) || !/\bheight=/.test(img[0])) warn(`${page}: <img> without width and height can shift layout -> ${img[0].slice(0, 60)}`);
  }

  /* 6. a fixed-width child inside a grid overflowed the viewport in the last theme;
        the rule now is that no card may declare a pixel width. */
  if (/\bclass="(?:prod|pick|card)"[^>]*style="[^"]*width:\s*\d+px/.test(html)) fail(`${page}: fixed pixel width on a card`);

  /* 7. links that leave the site carry noopener, and Amazon links carry sponsored */
  for (const a of html.matchAll(/<a\b[^>]*href="(https?:\/\/[^"]+)"[^>]*>/g)) {
    if (/target="_blank"/.test(a[0]) && !/noopener/.test(a[0])) warn(`${page}: target=_blank without noopener -> ${a[1].slice(0, 60)}`);
    if (/amazon\.com\/dp\//.test(a[1]) && !/rel="[^"]*sponsored/.test(a[0])) fail(`${page}: Amazon product link without rel=sponsored -> ${a[1].slice(0, 60)}`);
    /* A citation in the verification register is evidence, not a CTA: it should NOT carry the
       tracking id, because it is the page we read, not the page we send a buyer to. Count
       them per page instead of warning per link. */
    if (/amazon\.com\/dp\//.test(a[1]) && !/tag=shopnow047c-20/.test(a[1])) untagged[page] = (untagged[page] || 0) + 1;
  }
}

for (const [p2, n] of Object.entries(untagged)) {
  console.log(`  note  ${p2}: ${n} untagged Amazon citation(s) - expected on the register, which cites the page it read`);
}

/* ---------- stylesheet: every @font-face file exists and every family is declared ---------- */
const css = readFileSync(join(ROOT, "assets/style.css"), "utf8");
for (const m of css.matchAll(/url\(["']?([^"')]+\.woff2)["']?\)/g)) {
  if (!existsSync(join(ROOT, "assets", m[1].replace(/^\.?\//, "")))) fail(`assets/style.css: font file ${m[1]} is missing`);
}

/* ---------- report ---------- */
console.log(`\nStructure: ${pages.length} pages walked, ${fails.length} blocking, ${warns.length} warning(s).`);
for (const w of warns) console.log(`  warn  ${w}`);
for (const f of fails) console.log(`  FAIL  ${f}`);
if (fails.length) { console.log("\nStructure check FAILED.\n"); process.exit(1); }
console.log("Structure check passed. This is a structural proof, not a visual review.\n");
