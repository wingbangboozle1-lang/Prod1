#!/usr/bin/env node
/* The Countertop Guide — design-system gate.
 *
 * Why this exists: the site shipped for several sessions with 44 CSS classes in the
 * generated HTML that had no rule in assets/style.css, and 9 custom properties that
 * were referenced but never defined. The pages rendered, so nothing failed; they just
 * looked unstyled. A rule that is not checked is a preference, so this gate checks it.
 *
 * It is static: it reads the built HTML and the stylesheet. It cannot see whether a
 * rule is *good*, only whether the class has one. Visual review still needs eyes.
 *
 * Checks:
 *  1. Every class used in a root *.html file has a rule in assets/style.css.
 *  2. Every var(--x) in the stylesheet is declared in :root or has a fallback.
 *  3. No CSS custom property is declared twice in :root (a silent override).
 *  4. No escaped quotes or stray markup inside a class attribute.
 *  5. The stylesheet has no syntax breaks: balanced braces, no empty rules.
 *  6. Every .html file references the stylesheet, and no inline style= attributes remain
 *     in generated pages (design changes belong in the system, not in a page).
 *
 * Usage: node scripts/check_style.mjs [--root DIR] [--quiet]
 * Exit 1 = at least one blocking item.
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const args = process.argv.slice(2);
const ROOT = args.includes("--root") ? args[args.indexOf("--root") + 1] : process.cwd();
const QUIET = args.includes("--quiet");

const fails = [];
const warns = [];
const fail = (m) => fails.push(m);
const warn = (m) => warns.push(m);

const CSS_PATH = join(ROOT, "assets/style.css");
if (!existsSync(CSS_PATH)) {
  console.log("FAIL: assets/style.css is missing");
  process.exit(1);
}
const css = readFileSync(CSS_PATH, "utf8");

/* ---------- strip comments so commented-out rules never count as styling ---------- */
const cssCode = css.replace(/\/\*[\s\S]*?\*\//g, "");

/* ---------- 5. balance ---------- */
const open = (cssCode.match(/\{/g) || []).length;
const close = (cssCode.match(/\}/g) || []).length;
if (open !== close) fail(`assets/style.css: unbalanced braces (${open} open, ${close} close) - the tail of the file is being dropped by the browser`);
const emptyRules = [...cssCode.matchAll(/([^{}]+)\{\s*\}/g)].map((m) => m[1].trim());
if (emptyRules.length) fail(`assets/style.css: ${emptyRules.length} empty rule(s), e.g. "${emptyRules[0].slice(0, 60)}"`);

/* ---------- declared custom properties ---------- */
const rootMatch = cssCode.match(/:root\s*\{([\s\S]*?)\}/);
const rootBody = rootMatch ? rootMatch[1] : "";
if (!rootMatch) fail("assets/style.css: no :root block - every var() would be undefined");
const declared = [...rootBody.matchAll(/(--[\w-]+)\s*:/g)].map((m) => m[1]);
const declaredSet = new Set(declared);
const dupes = declared.filter((v, i) => declared.indexOf(v) !== i);
for (const d of [...new Set(dupes)]) warn(`:root declares ${d} more than once; the last one silently wins`);

/* ---------- 2. every var() resolves ---------- */
const refs = [...cssCode.matchAll(/var\(\s*(--[\w-]+)\s*(,)?/g)];
const unresolved = new Set();
for (const [, name, fallback] of refs) {
  if (!declaredSet.has(name) && !fallback) unresolved.add(name);
}
for (const u of unresolved) fail(`assets/style.css references ${u} but never declares it and gives no fallback - the rule is dropped`);

/* ---------- classes defined in the stylesheet ---------- */
const defined = new Set();
for (const m of cssCode.matchAll(/\.(-?[_a-zA-Z][\w-]*)/g)) defined.add(m[1]);
/* States the client script adds at runtime, and a few utility hooks that are documented
   as behaviour-only. Keeping this list short is the point; add to it only with a reason. */
const ALLOWED_UNSTYLED = new Set([
  "is-current",     // aria-current fallback written by the build
  "guide-faq",      // semantic marker, styled via .guide details
]);
/* `<tr id=...>` table rows adopted from another session's report contain fragments in a
   class attribute (a markup bug in their source). Those live under docs/ and counter-check/
   and are not ours to edit; only root pages are checked here. */

/* ---------- 1 + 4. classes used in the generated pages ---------- */
const pages = readdirSync(ROOT).filter((f) => f.endsWith(".html") && existsSync(join(ROOT, f)));
if (!pages.length) fail("no HTML pages found - did the build run?");

let classCount = 0;
for (const p of pages) {
  const h = readFileSync(join(ROOT, p), "utf8");
  if (!/assets\/style\.css/.test(h)) fail(`${p}: does not link assets/style.css`);
  for (const m of h.matchAll(/\bclass="([^"]*)"/g)) {
    const raw = m[1];
    /* 4. a class value that contains escaped quotes, angle brackets or a closing tag
          means the attribute was written with a quoting bug (see FLG-052). */
    if (/&quot;|&#34;|<|>/.test(raw)) {
      fail(`${p}: class attribute contains markup or an escaped quote -> class="${raw.slice(0, 60)}"`);
      continue;
    }
    for (const c of raw.split(/\s+/).filter(Boolean)) {
      classCount++;
      if (!/^-?[_a-zA-Z][\w-]*$/.test(c)) {
        fail(`${p}: "${c}" is not a valid class name`);
        continue;
      }
      if (!defined.has(c) && !ALLOWED_UNSTYLED.has(c)) {
        fail(`${p}: class "${c}" has no rule in assets/style.css`);
      }
    }
  }
  if (/\sstyle="/.test(h)) {
    const inline = [...h.matchAll(/\sstyle="([^"]*)"/g)].map((x) => x[1]);
    fail(`${p}: ${inline.length} inline style attribute(s) bypass the design system -> ${inline[0].slice(0, 60)}`);
  }
}

/* ---------- 8. a declared font family must actually ship ----------
   assets/style.css names Fraunces and Inter. For several sessions neither file existed and
   no @font-face rule declared them, so every page silently rendered in Georgia and the
   system UI font while the design document claimed an editorial serif (FLG-060). A fallback
   is not a design. Any family named in a font-family stack without a system fallback keyword
   must be declared by @font-face AND have its woff2 on disk. */
const SYSTEM_FAMILIES = new Set(["serif", "sans-serif", "monospace", "system-ui", "ui-monospace",
  "ui-serif", "ui-sans-serif", "cursive", "fantasy", "-apple-system", "helvetica", "arial",
  "georgia", "times", "courier", "menlo", "consolas", "roboto", "blinkmacsystemfont"]);
const faceFamilies = new Set([...cssCode.matchAll(/@font-face\s*\{[^}]*font-family\s*:\s*["']?([^;"'}]+)["']?/g)]
  .map((m) => m[1].trim().toLowerCase()));
const faceSrcs = [...cssCode.matchAll(/@font-face\s*\{[^}]*src\s*:\s*url\(["']?([^"')]+)["']?\)/g)].map((m) => m[1]);
const usedFamilies = new Set();
for (const m of cssCode.matchAll(/font-family\s*:\s*([^;}]+)/g)) {
  if (/^\s*["']?(?:inherit|initial|unset)\s*$/.test(m[1])) continue;
  for (const raw of m[1].split(",")) {
    const name = raw.trim().replace(/^["']|["']$/g, "").trim().toLowerCase();
    if (!name || SYSTEM_FAMILIES.has(name) || name.startsWith("var(")) continue;
    usedFamilies.add(name);
  }
}
for (const fam of usedFamilies) {
  if (!faceFamilies.has(fam)) fail(`assets/style.css uses the font family "${fam}" but declares no @font-face for it - the page falls back to a system font`);
}
if (faceFamilies.size && !faceSrcs.length) fail("assets/style.css has @font-face blocks with no src url()");
for (const src of faceSrcs) {
  if (/^https?:|^\/\//.test(src)) { warn(`@font-face loads ${src} from another host; a third-party font host is a runtime dependency and a privacy surface`); continue; }
  const onDisk = join(ROOT, "assets", src.replace(/^\.?\//, ""));
  if (!existsSync(onDisk)) fail(`@font-face points at ${src}, which does not exist in assets/ - the browser 404s and falls back`);
}
for (const p2 of pages) {
  const h = readFileSync(join(ROOT, p2), "utf8");
  for (const m of h.matchAll(/<link[^>]+href="[^"]*fonts\.googleapis\.com[^"]*"/g)) {
    warn(`${p2}: loads fonts from Google Fonts at runtime; self-hosting is the house rule (see assets/fonts/OFL-*.txt for how the current faces are licensed)`);
  }
}

/* ---------- 7. duplicate element ids ---------- */
for (const p of pages) {
  const h = readFileSync(join(ROOT, p), "utf8");
  const ids = [...h.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]);
  const dup = [...new Set(ids.filter((v, i) => ids.indexOf(v) !== i))];
  if (dup.length) fail(`${p}: duplicate id attribute(s) ${dup.slice(0, 4).join(", ")} - anchors and aria references break`);
}

/* ---------- report ---------- */
if (!QUIET) {
  console.log(`\nDesign-system gate: ${pages.length} pages, ${classCount} class uses, ${defined.size} classes defined, ${declaredSet.size} custom properties.`);
}
for (const w of warns) console.log(`  warn  ${w}`);
for (const f of fails) console.log(`  FAIL  ${f}`);
if (fails.length) {
  console.log(`\nGate FAILED: ${fails.length} blocking item(s), ${warns.length} warning(s).\n`);
  process.exit(1);
}
console.log(`\nGate passed: ${warns.length} warning(s), no blocking items.\n`);
