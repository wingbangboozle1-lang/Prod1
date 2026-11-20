# Verification record - session arena/42e09357-prod1, 2026-11-20

Scope, stated plainly: a **partial, dated re-read** of the five listings plus the sources needed for
the copy this session wrote. This session did not re-read spec tables, ratings or the remaining
buy-box prices, so `data/products.json` keeps its `verifiedDate` of 2026-11-19 and no shop-page field
is labelled as freshly confirmed.

## 1. The five listings, read 2026-11-20

| Ref | Page read | Result |
|---|---|---|
| P1 | https://www.amazon.com/dp/B0CDY277D3 | Reachable. Page title matches `title` in the register exactly. Buy box not isolated in this read, so the dated price ($79.93) was not re-sampled. |
| P2 | https://www.amazon.com/dp/B09B7SB46R | Reachable. Title matches, and still states "24 One-Touch Preset Options" and "Six Cooking Accessories Included". FLG-002 and FLG-021 unchanged by this read. |
| P3 | https://www.amazon.com/dp/B08DKYBTPH | Reachable. Title matches apart from the registered-trademark mark the register drops (FLG-061). The page's own "Customers who viewed" block still shows the newer 6QT B0CNY1YVDD at $59.99 with 4.6/7,602, corroborating FLG-003. |
| P4 | https://www.amazon.com/dp/B0DHZTCNR5 | Reachable. Title matches; the seller now carries holiday keywords in it ("Stocking Stuffers Gifts for Men, Black"). Buy box read as the product's own: $16.99, equal to the register's dated figure. Register writes °F where the page uses U+2109 (FLG-061). |
| P5 | https://www.amazon.com/dp/B0DZFD6R9Z | Reachable. Title matches, including "Gen3", "5 Sensors", "3 Ultra-Thin Probes". No dimensions in the fields captured, so FLG-004 stays open. |

Method note: every listing page carries widget blocks (product summary, "also viewed") that show
other ASINs' prices and star counts. None of those figures were used, per FLG-016. Where the buy box
could not be attributed to the product with certainty, nothing was recorded.

## 2. Sources read for the seasonal copy

| Source | Read | What it settled |
|---|---|---|
| https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | 2026-11-20 | Thanksgiving Day 2026 is **Thursday, 26 November 2026**, a federal holiday under 5 U.S.C. 6103. The Friday (27 Nov) and the Monday (30 Nov) are not in that list, so the guides treat them as retail names for ordinary weekdays. |
| https://affiliate-program.amazon.com/help/operating/policies | quoted on the site from session b49d8595 (2026-11-19) and reused, not re-read here | Participation requirements bar price-tracking and alerting functionality on a Site, which is why the buying-window guide does the arithmetic on Amazon's page instead of on ours. |
| https://www.amazon.com/dp/B0CDY277D3 (and the four above) | 2026-11-20 | The only product facts used in the three new guides: capacity and form fields, dimensions, wattage, bullets, variant selectors, warranty and certification statements. |

## 3. Claims this session checked, and the machinery added

- The site's comparative labels are now recomputed from the register on every build (`CLAIMS` in
  `build_site.py`): narrowest, shallowest, deepest, biggest cavity, the cm conversion, the three-forms
  claim, the five-product count, and the floor-area arithmetic. A contradicted sentence stops the
  build. Negative test performed: setting P1's width to 20.00 in made the build refuse with
  "The narrowest of the three fryers at 11.81 in wide; 158.0, 267.0 and 172.1 sq in of floor area".
- Two claims are labelled *untestable here* rather than passed: the derived capacity-per-square-inch
  row, and the "distance question" framing on the thermometers page.
- Decision register (`data/decisions.json` + `decisions.html`): the build compares the register with the board
  on every publish and lists unowned rows on the page plus a warning on the build. It began as a hard failure and was
  softened the same day - see FLG-082 - because an append-only board let an unrelated session's new row block the site's deploy. It currently maps 43 suggestions and 27 questions to seven gates.
- Topic 12 on the calendar was marked Planned for a question `guide-gift-picks.html` already answers;
  corrected to Published with an href, and recorded as FLG-065 because it edits another session's row.

## 4. New flags filed (published at flagged.html)

FLG-060 (partial re-read, dated), FLG-061 (normalised titles in the register), FLG-062 (three guides
published before any measured demand), FLG-063 (drawings are ours and do not answer the licence
question), FLG-064 (the 28-day default rule is a proposal, not policy), FLG-065 (topic-12 status fix).

## 5. Not verified by this session

Commission rates, API eligibility, the supplied short links' compliance as Special Links, the two
thermometers' dimensions, the Emeril warranty period, search demand for any published topic, and
whether Pages will publish from Actions or from the branch. Each is on flagged.html or the decision
register with the step that would close it.
