# Source-coverage audit + repo review — session arena/0f8382dd-prod1 (2026-11-20)

Companion to `VERIFICATION.md` (the line-by-line evidence log). This file records:
the classification rules the new `scripts/check_sources.mjs` gate enforces, the findings
it raised on the combined tree, the fixes applied to the generator, and the repo-review
irregularities found while reading the tree line by line.

## The rule being enforced

Brief: *"Every table row must have a source link to an official site. If a value can't be
confirmed from an official source, leave it blank and flag it as unverified."*

`scripts/check_sources.mjs` (new in this pass) encodes it as:

1. **Fact tables** (manifest in the script header: the five verification registers,
   every category/comparison spec table, the topic calendar, compliance, the flag
   register, the executive product table, and the guide comparison tables): every data
   row must carry a link to an official source domain (amazon.com, the Associates
   program pages, ftc.gov, Google, RSS board, OPM — the brief's official list).
   On the audit-trail tables (flag register, re-read log, claim audit) a repo-evidence
   link (a page on this site or a file in this repository) also counts: their claims
   are about the repository, and the linked file/page IS the reviewable source.
2. **Explicit classification**: a row with `data-src="owner"` (owner-supplied input with
   no official source that could exist), `data-src="derived"` (our own construction, with
   the recipe stated in the row), or `data-src="editorial"` (process/opinion) passes
   without a link. The marker is the audit decision; every marked row names its evidence
   in text. This is the machine form of "leave it blank and flag it" — the row cannot
   sneak an unverified *value* past the gate because…
3. **Generic value scan** on all other tables: any row asserting an external value (a `$`
   price, an ASIN, a star rating) must carry an official link or a classification marker.

Result on the integrated tree: **587 rows scanned across 41 pages, 193 rows carry an
official link, 0 violations.** The gate is meant to be added to `pages.yml` like the
other checks (one `node scripts/check_sources.mjs` step); the workflow file is shared and
was left untouched in this pass — request logged in `COORDINATION.md` (SG-63's sibling).

## Findings raised by the first run (158 violations) and how each class was fixed

All fixes are in `build_site.py` (the generator) — no generated page was hand-edited.

| Class | Count | Fix |
|---|---|---|
| Flag register rows with no link | 80 | 33 rows got their natural source linked (5 ASIN listings, 28 site/repo pages); 47 repo-process rows are classified `data-src="editorial"` and name their evidence in text |
| Verification registers T1–T5, linkless Source cells | 25 | Official-listing rows now link the listing (Official listing URL, Confirmation date source); the Observed-redirect row links the observed URL (the observation itself); the short-link row is `data-src="owner"` (owner brief; no official source can exist — and FLG-003's compliance question is deliberately untouched); the Affiliate-URL row is `data-src="derived"` with its construction recipe stated |
| Claim audit + re-read log rows | 14 | Row renderers now linkify page names (`link_pages()`) and link each product ref to its listing |
| Spec tables with one Source row but no per-row links | 15 rows / 90+ cells | Every product fact cell now links its own Amazon listing (the repo's own README rule: "Every product fact links to its Amazon listing"). Derived rows keep their formula footnote; the "Why no price here" row cites the Program Policies price rule; the Verify row links listings plus the register |
| Guide comparison tables (gifts by budget, hosting, Thanksgiving, instant-read vs wireless, buyer briefs) | 18 | Product cells/names link their listings |
| Compliance quote rows | 7 | Each quoted clause now links the policy page it is quoted from (Operating Agreement §5 / Program Policies §2) |
| Editorial stragglers (runbook steps, calendar rows) | 2 | `data-src="editorial"` at the renderer level |

Two provenance mistakes made and caught during the fix itself (recorded because the
point of this pass is that links are only worth what their accuracy is worth): an
intermediate pass wrapped two air-fryer power cells with the wrong ASINs (a shared row
label matched the wrong table); both were repaired before commit, and the repaired cells
cite B0CDY277D3 / B09B7SB46R as the listings do.

## Repo review (line-by-line read of the tree) — findings

1. **`README.md` contains two concatenated README texts** (duplicated sections, stale
   counts). Left in place: editing shared docs mid-integration churns conflicts; the
   duplication is logged here and in `COORDINATION.md` for the owner (one delete).
2. **Stale prose counts** (found pre-integration, partly fixed since by other passes):
   "Ten guides, three clusters" on guides.html — the heading count is now computed from
   the guide list (`@@NGWORD@@`/`GUIDE_N`), and the 2026-11-20 merges made the front-page,
   feed, footer and index counts derive from one `GUIDE_CARDS` source with a build-time
   assertion (`guide index and feed disagree`). Typed literals from parallel passes were
   replaced by the computed versions in the integration merges.
3. **Register id collisions from parallel sessions** (SG/FLG/Q): resolved at each merge
   by renumbering the later pass's rows past the current maximum and shifting the
   references inside those rows — no row deleted, every renumber noted in-cell
   (FLG-091..093 from the e7dcb638 pass, FLG-094..098 + SG-64/65 + Q-45 from e0c70d8e,
   FLG-099..103 + SG-66..70 + Q-46..50 from c2a9c3e8, SG-60..63 from this session's rows).
   Known cosmetic defect kept visible: some earlier rows carry an `id` attribute that
   predates their `td` label (`<tr id="Q-38"><td>Q-42</td>`); the labels are the
   canonical numbering, the anchors are stale. The duplicate-id gate passes; fixing the
   anchor/label pairs is one mechanical pass (logged for the owner).
4. **Duplicate same-question guides** (accessories pair; fit trio): counter-fit
   consolidated onto counter-depth-fit (FLG-047 pattern, registered in `check_meta.mjs`'s
   consolidation list); accessories pair kept live with FLG-104 offering the owner the
   consolidation decision. `counter-height` vs `counter-depth-fit` kept separate
   (vertical clearance vs overall fit).
5. **`styles.css` at the repo root** is linked by nothing (FLG-069 in the register);
   untouched, owner's call.
6. **Conflict-marker hygiene**: this integration strip-scanned every merged file; the
   e0c70d8e branch carried three stray `>>>>>>>` lines inside its `COORDINATION.md`
   block (stripped, records kept) and marker text shipped inside five generated pages
   from an earlier unresolved merge (regenerated from the merged generator).
7. **Provenance note on ratings**: shop pages deliberately show no prices or ratings
   (Program Policies price-display rule and §6(t)); all rating/price figures live in the
   dated verification register only. The intraday rating drift (P1 4,877→4,878,
   P3 16,892→16,894) is recorded in `VERIFICATION.md` and the register notes.

## What the gate does NOT prove

A link proves where a value came from, not that the value is right — that is
`VERIFICATION.md`'s job (the live re-reads). A `data-src` marker is a human
classification; the gate only forces the classification to exist and be visible.
Editorial rows are exempt by design (the brief's rule governs factual values), and the
manifest of fact tables is itself a reviewable decision list at the top of the script.
