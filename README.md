# Counter & Crumb

A static, editorial-style kitchen appliance publication and evidence register. Built for GitHub Pages.

## Current status

- Publication homepage and three question-led buyer guides are included.
- Five supplied product links are recorded without guessing product identity or specifications. Intended ASINs, official listing URLs, confirmation dates/sources, and observed redirects remain blank pending official verification.
- Affiliate disclosure is shown in the masthead strip on every page and repeated in each footer. The unverified submitted links are not presented as product recommendations.
- `sitemap.xml` and `feed.xml` list the homepage and guides. `robots.txt` points to the sitemap.
- `app.js` increments an outbound-link count in the visitor's own browser storage only. It is not server analytics, does not send data, and cannot measure site-wide clicks or orders.
- No self-hosted analytics endpoint, Search Console property, Associates report, or product API integration is configured. See `docs/method.html`, `docs/campaign-ledger.html`, and `docs/flagged.html`.

## Develop and verify

No build step or dependencies are required. Serve the repository root with any static HTTP server, then run the local structural/link test:

```sh
python3 -m http.server 8000
python3 - <<'PY'
from pathlib import Path
from html.parser import HTMLParser
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('a','link','script'): self.links += [v for k,v in attrs if k in ('href','src') and v]
for f in [Path('index.html'),*Path('docs').glob('*.html'),*Path('articles').glob('*.html')]:
    p=Links(); p.feed(f.read_text())
    for u in p.links:
        if u.startswith(('http:','https:','mailto:','#','data:')): continue
        target=(f.parent/u.split('#')[0]).resolve()
        if not target.exists(): raise SystemExit(f'Broken local link: {f}: {u}')
print('Local HTML links: OK')
PY
```

## Publication and review

The site is configured for the project URL `https://wingbangboozle1-lang.github.io/Prod1/`. GitHub Pages must be enabled for the repository (or the deployment workflow configured) before the public URL is confirmed. No claim is made that deployment has already succeeded.

Before making product recommendations, verify each link and intended ASIN with the enrolled Amazon Associates workflow. Record intended destination separately from observed redirect, and validate Special Link behavior and reporting before scaling. Follow the current [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) and [Program Policies](https://affiliate-program.amazon.com/help/operating/policies). Review [FTC disclosure guidance](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) and [Google people-first content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). See the site’s Suggestions and Flagged for Review pages for the decision queue.
