#!/usr/bin/env python3
"""
Pushes content/home.json into index.html.

index.html is hand-tuned and deliberately NOT generated, so it can't be
rebuilt from a template the way the other pages are. Instead every editable
string carries a data-cms="section.field" marker, and this script rewrites
the text inside those elements in place. Markup, classes and attributes are
untouched — only the text between the tags changes.

That is what makes it safe to hand the homepage to a CMS: the worst a bad
edit can do is produce awkward wording, never a broken layout.

    python3 apply_content.py            # write
    python3 apply_content.py --check    # report drift, change nothing

Runs as part of build.sh, after the generators.
"""
import io, json, re, sys

HTML = "index.html"
DATA = "content/home.json"

# hero.headline is the one rich field. Authors write *golden hour* and get
# the gold italic; everything else is escaped as-is. Keeping the CMS syntax
# this small is deliberate — it can't emit markup the design didn't plan for.
RICH = {"hero.headline"}


def to_html(value: str) -> str:
    """CMS text -> the markup the page expects."""
    out = value.replace("*", "\x00")          # sentinel survives the split
    parts = out.split("\x00")
    if len(parts) >= 3:
        # *emphasized* plus any punctuation glued to it stays on one line
        out = parts[0] + '<span class="nb"><em>' + parts[1] + "</em>"
        tail = parts[2]
        m = re.match(r"([^\s<]*)(.*)", tail, re.S)
        out += (m.group(1) if m else "") + "</span>" + (m.group(2) if m else "")
    else:
        out = value
    return out


def from_html(markup: str) -> str:
    """The inverse, so --check can compare like with like."""
    s = re.sub(r'<span class="nb"><em>(.*?)</em>([^\s<]*)</span>', r"*\1*\2", markup, flags=re.S)
    return re.sub(r"\s+", " ", s).strip()


def flatten(d, prefix=""):
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            yield from flatten(v, key)
        else:
            yield key, v


def main():
    check = "--check" in sys.argv
    html = io.open(HTML, encoding="utf-8").read()
    content = dict(flatten(json.load(io.open(DATA, encoding="utf-8"))))

    seen, drift = set(), []
    changed = 0

    # A non-greedy regex would stop at the first </...> it met, which for the
    # headline is the inner </em>, not the </h1>. So find each marked element's
    # own closing tag by scanning forward with a depth counter.
    TAG = re.compile(r'<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>[^>]*\bdata-cms="(?P<key>[^"]+)"[^>]*)>')
    pieces, pos = [], 0
    for m in TAG.finditer(html):
        if m.start() < pos:
            continue
        tag, key = m.group("tag"), m.group("key")
        body_start = m.end()
        depth, i = 1, body_start
        open_re = re.compile(r'<(/?)%s\b' % re.escape(tag))
        while depth and i < len(html):
            om = open_re.search(html, i)
            if not om:
                break
            depth += -1 if om.group(1) else 1
            i = om.end()
        if depth:
            continue                      # unbalanced; leave the page alone
        close_start = html.rindex("<", body_start, i)
        inner = html[body_start:close_start]

        seen.add(key)
        pieces.append(html[pos:body_start])
        if key in content:
            new_inner = to_html(content[key]) if key in RICH else content[key]
            if from_html(inner) != from_html(new_inner):
                lead = re.match(r"\s*", inner).group(0)
                trail = re.search(r"\s*$", inner).group(0)
                drift.append((key, from_html(inner)[:60], from_html(new_inner)[:60]))
                changed += 1
                inner = lead + new_inner + trail
        pieces.append(inner)
        pos = close_start
    pieces.append(html[pos:])
    out = "".join(pieces)

    missing = sorted(set(content) - seen)
    orphan = sorted(seen - set(content))

    if check:
        for k, a, b in drift:
            print("  DRIFT  %-20s page:%r  json:%r" % (k, a, b))
        for k in missing:
            print("  IN JSON, NO MARKER ON PAGE:", k)
        for k in orphan:
            print("  MARKER ON PAGE, NOT IN JSON:", k)
        print("%d marker(s), %d would change" % (len(seen), len(drift)))
        return 1 if (drift or missing or orphan) else 0

    if changed:
        io.open(HTML, "w", encoding="utf-8").write(out)
    print("apply_content: %d marker(s), %d updated" % (len(seen), changed))
    for k in missing:
        print("  warning: %s is in home.json but has no marker in index.html" % k)
    for k in orphan:
        print("  warning: %s is marked in index.html but missing from home.json" % k)
    return 0


if __name__ == "__main__":
    sys.exit(main())
