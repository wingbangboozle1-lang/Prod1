#!/usr/bin/env node
/* The Countertop Guide - measurement-contract gate.
 *
 * The site's five defined events are a contract shared by four places:
 *   data/editorial.json   events.five            (the data record)
 *   assets/app.js         EVENTS list + payload  (the client)
 *   analytics-endpoint/server.py  EVENT_NAMES    (the server)
 *   methodology.html      the published table    (what readers are told)
 * A rule that is not checked is a preference: this script fails the deploy when any of
 * the four disagree, when a retired tracker vocabulary reappears, when the campaign
 * ledger schema drifts, or when the data-analytics-endpoint wiring disappears.
 *
 * It also runs the endpoint's own self-test (python3 analytics-endpoint/selftest.py),
 * which proves the server accepts the client envelope and rejects everything else.
 *
 * Zero dependencies. Usage: node scripts/check_measure.mjs [--root DIR] [--quiet]
 */
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { spawnSync } from "node:child_process";

const args = process.argv.slice(2);
const ROOT = args.includes("--root") ? args[args.indexOf("--root") + 1] : process.cwd();
const QUIET = args.includes("--quiet");
const fails = [], warns = [];
const fail = (m) => fails.push(m);
const warn = (m) => warns.push(m);
const read = (f) => readFileSync(join(ROOT, f), "utf8");

/* ---------- 1. the data record: data/editorial.json ---------- */
const EDIT = JSON.parse(read("data/editorial.json"));
const dataNames = (EDIT.events?.five || []).map((e) => e.name).sort();
if (dataNames.length !== 5) fail(`data/editorial.json: events.five has ${dataNames.length} entries, expected 5`);
for (const n of dataNames) if (!/^[a-z][a-z0-9_]*$/.test(n)) fail(`data/editorial.json: event name "${n}" is not snake_case`);

/* ---------- 2. the client: assets/app.js ---------- */
const client = read("assets/app.js");
const m = client.match(/var EVENTS = \[([^\]]*)\]/);
const clientNames = m ? [...m[1].matchAll(/"([^"]+)"/g)].map((x) => x[1]).sort() : null;
if (!clientNames) fail("assets/app.js: no `var EVENTS = [...]` list found");
else if (JSON.stringify(clientNames) !== JSON.stringify(dataNames))
  fail(`assets/app.js EVENTS ${JSON.stringify(clientNames)} != data/editorial.json ${JSON.stringify(dataNames)}`);
if (!client.includes("data-analytics-endpoint")) fail("assets/app.js: does not read data-analytics-endpoint - the endpoint wiring is gone");
if (!/if \(!ENDPOINT\) return;/.test(client)) fail("assets/app.js: missing the `if (!ENDPOINT) return;` gate - events could leave the device before a host is configured");
if (!/event: name/.test(client) || !/path: location\.pathname/.test(client))
  fail("assets/app.js: payload must send `event` and `path` (the server validator requires both)");

/* ---------- 3. the server: analytics-endpoint/server.py ---------- */
const serverPy = read("analytics-endpoint/server.py");
const s = serverPy.match(/EVENT_NAMES = frozenset\(\{([^}]*)\}\)/);
const serverNames = s ? [...s[1].matchAll(/"([^"]+)"/g)].map((x) => x[1]).sort() : null;
if (!serverNames) fail("analytics-endpoint/server.py: no EVENT_NAMES frozenset found");
else if (JSON.stringify(serverNames) !== JSON.stringify(dataNames))
  fail(`analytics-endpoint/server.py EVENT_NAMES ${JSON.stringify(serverNames)} != data/editorial.json ${JSON.stringify(dataNames)}`);

/* ---------- 4. the published record: methodology.html ---------- */
if (!existsSync(join(ROOT, "methodology.html"))) fail("methodology.html missing - run python3 build_site.py");
else {
  const meth = read("methodology.html");
  const section = meth.split("five defined events")[1] || "";
  const table = section.split("</table>")[0] || "";
  const pubNames = [...table.matchAll(/<tr><td>([a-z][a-z0-9_]*)<\/td>/g)].map((x) => x[1]).sort();
  if (JSON.stringify(pubNames) !== JSON.stringify(dataNames))
    fail(`methodology.html publishes ${JSON.stringify(pubNames)} != the contract ${JSON.stringify(dataNames)}`);

  /* campaign ledger: the defined schema, and still empty of fabricated rows */
  const ledger = meth.split("Campaign ledger")[1]?.split("</table>")[0] || "";
  const header = (ledger.match(/<tr>((?:<th>[^<]*<\/th>)+)<\/tr>/) || [])[1] || "";
  const want = ["Timestamp", "Source", "Channel", "Eligible sessions", "Clicks", "Reported orders", "Provenance (report + date obtained)"];
  const cells = [...header.matchAll(/<th>([^<]*)<\/th>/g)].map((x) => x[1]);
  if (JSON.stringify(cells) !== JSON.stringify(want))
    fail(`campaign ledger header ${JSON.stringify(cells)} != defined schema ${JSON.stringify(want)}`);
  const rows = [...ledger.matchAll(/<tr><td/g)].length;
  if (rows > 1 && !ledger.includes("Associates Central"))
    warn("campaign ledger has rows: confirm each was taken from an authorized first-party report (Associates Central)");
}

/* ---------- 5. retired vocabularies must not come back ---------- */
/* Two older trackers used these names; both were removed (R-06/R-07). Any .js file
   (or the server) naming one of them is a tracker drift, not prose - prose about the
   history lives in HTML/MD and is out of scope for this scan. selftest.py names them
   only to prove the server rejects them. */
const RETIRED = ["guide_read_75", "category_click", "feed_click", "affiliate_redirect", "guide_view", "conversion_signal"];
const jsFiles = [];
(function walk(dir) {
  for (const f of readdirSync(dir)) {
    const p = join(dir, f);
    if (f === ".git" || f === "node_modules" || f === "counter-check" || f === "review" || f === "docs" || f === "articles") continue;
    if (statSync(p).isDirectory()) walk(p);
    else if (f.endsWith(".js")) jsFiles.push(p);
  }
})(ROOT);
for (const p of jsFiles) {
  const src = readFileSync(p, "utf8");
  for (const bad of RETIRED) if (src.includes(bad)) fail(`${relative(ROOT, p)}: retired event name "${bad}" reappeared`);
}
for (const bad of RETIRED) if (serverPy.includes(bad)) fail(`analytics-endpoint/server.py: retired event name "${bad}" reappeared`);
if (existsSync(join(ROOT, "assets/js"))) {
  const stray = readdirSync(join(ROOT, "assets/js")).filter((f) => f.endsWith(".js"));
  for (const f of stray) fail(`assets/js/${f}: a second tracker directory is back - one client only (assets/app.js)`);
}
if (existsSync(join(ROOT, "assets/measure.js"))) fail("assets/measure.js: legacy tracker reappeared");

/* ---------- 6. every generated page keeps the endpoint wiring + no premature network ---------- */
const pages = readdirSync(ROOT).filter((f) => f.endsWith(".html") && statSync(join(ROOT, f)).isFile());
for (const p of pages) {
  const h = read(p);
  const body = (h.match(/<body[^>]*>/) || [])[0] || "";
  if (!body.includes("data-analytics-endpoint=")) fail(`${p}: <body> lost data-analytics-endpoint - the client would have nowhere to read the host from`);
}
/* Root app.js serves the supplementary builds and may only count locally. */
if (existsSync(join(ROOT, "app.js"))) {
  const legacy = read("app.js");
  if (/sendBeacon|XMLHttpRequest|fetch\(/.test(legacy)) fail("app.js: the supplementary-build counter must not transmit anything");
}

/* ---------- 7. the endpoint proves itself ---------- */
const selftest = spawnSync("python3", [join(ROOT, "analytics-endpoint", "selftest.py")], { encoding: "utf8" });
if (selftest.error) warn(`analytics-endpoint/selftest.py could not run (${selftest.error.message}) - static contract checks only`);
else if (selftest.status !== 0) fail(`analytics-endpoint/selftest.py FAILED:\n${selftest.stdout || ""}${selftest.stderr || ""}`);
else if (!QUIET) console.log((selftest.stdout || "").trim().split("\n").slice(-1)[0]);

/* ---------- 8. no merge conflict markers may ever ship ---------- */
/* A marker in a shipped file is how a broken workflow YAML reached main on 2026-11-20;
   the failing run caught it in seconds, this makes the class of bug impossible to repeat. */
const markerScan = [...jsFiles, ...pages.map((p) => join(ROOT, p)),
  join(ROOT, ".github", "workflows", "pages.yml"),
  join(ROOT, "analytics-endpoint", "server.py"),
  join(ROOT, "analytics-endpoint", "selftest.py"),
  join(ROOT, "build_site.py"),
].filter((p) => existsSync(p));
for (const p of markerScan) {
  const srcText = readFileSync(p, "utf8");
  if (/^<<<<<<< |^>>>>>>> /m.test(srcText) || /^={7}$/m.test(srcText))
    fail(`${relative(ROOT, p)}: unresolved merge conflict marker`);
}

/* ---------- report ---------- */
for (const w of warns) console.log("WARN  " + w);
for (const f of fails) console.log("FAIL  " + f);
if (fails.length) {
  console.log(`\nMEASURE GATE FAILED: ${fails.length} problem(s), ${warns.length} warning(s).`);
  process.exit(1);
}
console.log(`MEASURE GATE PASSED: contract = [${dataNames.join(", ")}] across data, client, server and the published page; ${jsFiles.length} JS file(s) clean; ${pages.length} page(s) wired.${warns.length ? ` ${warns.length} warning(s).` : ""}`);
