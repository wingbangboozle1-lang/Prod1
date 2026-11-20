# Session 1b65e5a1 — line-by-line re-verification (2026-11-20)

This is the evidence log for the T-VER task of session `1b65e5a1`. Every field below was
re-read from the **official Amazon.com listing page** for each ASIN on **2026-11-20** via the
`fetch_page` tool (the sandbox cannot reach `amazon.com` over a raw socket). The register value
is what `data/products.json` held before this pass; the observed value is what the listing showed
on 2026-11-20. Status: `match` = identical, `drift` = the register was corrected, `carried` =
carried from the 2026-11-19 register because that specific row was not re-captured this pass.

## Sources (all fetched 2026-11-20)

| Product | ASIN | Official listing URL |
|---|---|---|
| P1 | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 |
| P2 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R |
| P3 | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH |
| P4 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 |
| P5 | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z |

## P1 — Chefman 6QT Dual-Basket Air Fryer (B0CDY277D3)

| Field | Register (pre-pass) | Observed 2026-11-20 | Status |
|---|---|---|---|
| Title | Chefman 6QT Dual-Basket Air Fryer Oven… | same | match |
| Rating | 4.2 | 4.2 | match |
| Rating count | 4,876 | **4,877** | **drift** → updated |
| Buy-box price | $79.93 | $79.93 | match |
| List price | $99.99 | $99.99 | match |
| Used price | $59.95 | **$62.85** | **drift** → updated |
| Capacity | 6 L / 6 Quart | 6 L | match |
| Dimensions | 13.38"D × 11.81"W × 10.63"H | same | match |
| Wattage | 1700 W / 120 V | same | match |
| Badge / bought | Amazon's Choice / 1K+ bought | same | match |

## P2 — Emeril Lagasse 26QT French-Door Oven (B09B7SB46R)

| Field | Register (pre-pass) | Observed 2026-11-20 | Status |
|---|---|---|---|
| Title | Emeril Lagasse 26QT French Door… | same | match |
| Rating | 4.3 | 4.3 | match |
| Rating count | 18,375 | **18,380** | **drift** → updated |
| Buy-box price | $149.99 | $149.99 | match |
| List price | $209.99 | $209.99 | match |
| Capacity | 24.6 L | same | match |
| Dimensions | (register) | same | match |
| Wattage | 1700 W / 120 V | not re-captured this pass | **carried** |
| Accessories | title "Six" vs config "7" | 24 functions and 7 accessories (Item-details) | re-confirms **FLG-021** |

## P3 — Chefman 8QT TurboFry Basket (B08DKYBTPH)

| Field | Register (pre-pass) | Observed 2026-11-20 | Status |
|---|---|---|---|
| Title | Chefman 8QT TurboFry… | same | match |
| Rating / count | 4.4 / 16,892 | 4.4 / 16,892 | match |
| Buy-box price | $69.99 | $69.99 | match |
| List price | $119.99 | $119.99 | match |
| Wattage | 1000 W / 120 V (bullets) | 1000 W / 120 V — RJ38-SQSS-8T | match (FLG-022 resolved) |
| Capacity / badge | 8 qt / Amazon's Choice | same | match |

## P4 — ThermoMaven 1-Second Instant-Read (B0DHZTCNR5)

| Field | Register (pre-pass) | Observed 2026-11-20 | Status |
|---|---|---|---|
| Title | ThermoMaven 1-Second Instant-Read… | same | match |
| Rating count | 3,499 | 3,499 | match |
| Buy-box price | $16.99 | $16.99 | match |
| Spec field | NIST / NSF | same | match |
| Dimensions | blank (not listed) | not listed | **carried** (FLG-004 open) |

## P5 — CHEF iQ Sense Wireless 3-probe (B0DZFD6R9Z)

| Field | Register (pre-pass) | Observed 2026-11-20 | Status |
|---|---|---|---|
| Title | CHEF iQ Sense Wireless… | same | match |
| Rating / count | 4.2 / 2,178 | 4.2 / 2,178 | match |
| Buy-box price | $119.99 (3-probe) | $119.99 | match |
| List price | $219.99 | $219.99 | match |
| Warranty | two-year assurance | same | match |
| Dimensions | blank (not listed) | not listed | **carried** (FLG-004 open) |

## Register changes applied

- `site.verifiedDate`: 2026-11-19 → **2026-11-20**
- All five `confirmationDate`: 2026-11-19 → **2026-11-20**
- P1 `ratingCount`: 4,876 → **4,877**
- P1 `priceUsed`: $59.95 → **$62.85**
- P2 `ratingCount`: 18,375 → **18,380**
- Each `sourceNote` appended with the 2026-11-20 re-read trail and the specific drift.

## Carried, not re-confirmed this pass

- **P2 wattage** (1700 W / 120 V): the Item-details/Product-information table was not in the
  re-fetched chunks; kept from the 2026-11-19 register and attributed, not re-confirmed today.
- **P4 rating value / list price**: the rating value and list price rows were not re-captured in
  this pass's chunks; kept from the 2026-11-19 register and attributed.
- **Short links**: the direct `/dp/<ASIN>` pages were fetched, not the `link.amazon` short links,
  so `observedRedirectTarget` stays "observed 2026-11-19" and **FLG-001** (short-link compliance)
  remains unresolved. No new claim is made about short-link compliance this pass.

## Irregularities

- **FLG-060** (new): records this pass and its drifts (P1 rating count, P1 used price, P2 rating
  count) plus the FLG-021 re-confirmation and the two carried-not-reconfirmed scope notes.
- **FLG-021** (open, re-confirmed): P2 accessory count — title says six, configuration says seven.
- **FLG-004** (open): P4 and P5 dimensions absent from the Amazon listing fields.
- **FLG-001** (open, unresolved): short-link compliance not re-tested this pass.
