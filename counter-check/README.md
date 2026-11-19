# Counter Check (Prod1)

A static affiliate site for five Amazon listings in two categories (air fryers, kitchen thermometers), with sources, flags, suggestions and disclosures. Built into `counter-check/site/`; served by the repository GitHub Pages site at https://wingbangboozle1-lang.github.io/Prod1/counter-check/site/.

Live: https://wingbangboozle1-lang.github.io/Prod1/

## Layout

- `data/` — source of truth: product intent records, source register, flags, questions, suggestions, guides, measurement plan, campaign ledger (header only).
- `tools/build_site.py` — generates every page in `site/` from `data/`.
- `tools/check_site.py` — the publishing gate. Fails on a missing disclosure, a non-sponsored Amazon link, a buy link without the tag, an unsourced table row, a broken internal link, a missing sitemap entry, a price or rating on a product page, or an undefined flag.
- `site/` — generated site (do not edit by hand).
- `COORDINATION.md` — shared task board.

## Rebuild

```
python3 counter-check/tools/build_site.py
python3 counter-check/tools/check_site.py
```

## Rules

- Values that cannot be confirmed from an official source are left blank and flagged. Nothing is inferred.
- Prices, availability and star ratings are not shown (Associates Participation Requirements 2(b)).
- Every outbound Amazon link is `rel="sponsored"`. Buy links carry the tracking ID.
- The disclosure sentence in Associates Operating Agreement section 5 appears under the masthead of every page and in the footer.
