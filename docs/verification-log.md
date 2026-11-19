# Verification log

## 2026-11-19 — Initial verification pass
- Fetched all 5 submitted short links; resolved to ASINs B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z.
- Fetched each Amazon listing (title, rating, buy-box price, purchase-options table, bullets) and recorded fields in data/products.json with per-product source URLs.
- Fetched Amazon Associates Operating Agreement (upd. 2025-10-15), Program Policies (upd. 2026-04-14), FTC Disclosures 101 (Nov 2019).
- Irregularities logged as FLG-001..FLG-012 in flagged.html. Missing fields left blank.
- Next: re-fetch thermometer dimensions + Emeril wattage; manual Special Link test (SG-01).
