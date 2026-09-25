#!/usr/bin/env python3
"""Point internal links at clean URLs.

Cloudflare Pages serves /about.html at /about and 308-redirects the .html
form. The generators write href="about.html", so every internal link cost
a redirect and disagreed with the canonical. Runs last in `npm run pages`,
so whatever the generators or Tina produce comes out clean.
"""
import glob, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PAT = re.compile(r'href=(["\'])([A-Za-z0-9_-]+)\.html(#[^"\']*)?\1')

def fix(m):
    q, slug, frag = m.group(1), m.group(2), m.group(3) or ""
    return "href=%s%s%s%s" % (q, "/" if slug == "index" else "/" + slug, frag, q)

# Schema and meta use absolute URLs; those must match the canonical too.
ABS = re.compile(r'(https://www\.goldenhourwellnesscolorado\.com/)([A-Za-z0-9_-]+)\.html\b')

def fix_abs(m):
    return m.group(1) + ("" if m.group(2) == "index" else m.group(2))

changed = 0
for f in glob.glob(os.path.join(ROOT, "*.html")):
    s = open(f, encoding="utf-8").read()
    n = ABS.sub(fix_abs, PAT.sub(fix, s))
    if n != s:
        open(f, "w", encoding="utf-8").write(n)
        changed += 1
print("clean_links: %d files updated" % changed)
