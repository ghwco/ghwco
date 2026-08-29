#!/usr/bin/env python3
"""
Fails the build if _redirects contains a rule that loops on Cloudflare Pages.

This exists because I have now written the same broken rule twice — once for
/services and once for /blog — despite a comment in _redirects saying not to.
A comment is a suggestion; an exit code is a rule.

Cloudflare Pages serves clean URLs: it answers /blog with blog.html and
308-redirects /blog.html -> /blog. So a rule mapping /blog -> /blog.html
bounces forever and the page becomes unreachable.
"""
import io, re, sys

BAD = []
for n, line in enumerate(io.open("_redirects", encoding="utf-8"), 1):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split()
    if len(parts) < 2:
        continue
    src, dest = parts[0], parts[1]
    base = dest.split("#")[0]
    if base == src + ".html" or base == src.rstrip("/") + ".html":
        BAD.append((n, src, dest, "redirect loop: Cloudflare already 308s the .html form back here"))
    if src.endswith(".html"):
        BAD.append((n, src, dest, "source ends in .html; Cloudflare redirects that away before rules run"))
    if src == "/*":
        BAD.append((n, src, dest, "catch-all intercepts real pages before they resolve"))

if BAD:
    print("\n_redirects has %d rule(s) that will break the site:\n" % len(BAD))
    for n, src, dest, why in BAD:
        print("  line %-3d  %-24s -> %-24s  %s" % (n, src, dest, why))
    print("\nOnly list paths whose destination is a genuinely DIFFERENT page.\n")
    sys.exit(1)

print("_redirects: no loops")
