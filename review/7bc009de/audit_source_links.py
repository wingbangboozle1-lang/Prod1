"""Read-only audit: does every data row of every built HTML table carry a source link?
Usage (from repo root): python3 review/7bc009de/audit_source_links.py
A row counts as sourced when its text or an href contains an official-domain URL
(Amazon, Associates, FTC, Google, OPM, GitHub, schema.org, W3C, RSS Board) or an internal link.
Pure header rows (all <th>) and empty rows are skipped. Writes nothing; prints a summary."""
import glob, re
from html.parser import HTMLParser
OFF = re.compile(r'https?://(www\.)?(amazon\.com|affiliate-program\.amazon\.com|developers\.google\.com|ftc\.gov|www\.ftc\.gov|github\.com|opm\.gov|wingbangboozle1-lang\.github\.io|schema\.org|w3\.org|link\.amazon|www\.rssboard\.org)[^\s"\'<)]*')
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.tables = []; s.cur = None; s.row = None; s.cell = None
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == 'table': s.cur = []; s.tables.append(s.cur)
        elif t == 'tr' and s.cur is not None: s.row = {'cells': [], 'links': [], 'kinds': []}; s.cur.append(s.row)
        elif t in ('td', 'th') and s.row is not None:
            s.cell = []; s.row['cells'].append(s.cell); s.row['kinds'].append(t)
        elif t == 'a' and s.row is not None and 'href' in a: s.row['links'].append(a['href'])
    def handle_endtag(s, t):
        if t == 'table': s.cur = None
        elif t == 'tr': s.row = None
        elif t in ('td', 'th'): s.cell = None
    def handle_data(s, d):
        if s.cell is not None: s.cell.append(d)
tot = ok = 0
for f in sorted(glob.glob('*.html')):
    p = P(); p.feed(open(f, encoding='utf-8').read())
    n = k = 0
    for t in p.tables:
        for r in t:
            if not r['cells'] or all(not ''.join(c).strip() for c in r['cells']): continue
            if all(x == 'th' for x in r['kinds']): continue
            txt = ' | '.join(' '.join(''.join(c).split()) for c in r['cells'])
            n += 1
            if OFF.search(txt + ' ' + ' '.join(r['links'])) or any(l.startswith(('#', '/')) or l.endswith('.html') for l in r['links']): k += 1
    if n: print(f"{f:36} rows={n:3} with_source={k:3} without={n-k:3}")
    tot += n; ok += k
print(f"TOTAL rows={tot} with_source={ok} without={tot-ok}")
