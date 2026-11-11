#!/usr/bin/env python3
"""
Blog index + post pages, generated from content/blog/*.json.

    python3 build_blog.py

The `published` flag is the whole point of this file. An unpublished post is
not merely hidden; it is never written to disk at all, so there's no orphan
URL sitting on the server for someone to find or for Google to index. Toggling
it in Tina commits a one-character change, the build runs, and the page either
exists or it doesn't.

Stale HTML from a post that has just been unpublished is deleted on each run,
so un-publishing genuinely removes the page rather than leaving the last build
behind.
"""
import io, os, glob, json, re
from build_pages import page, head_block, cta, SITE, clean_url, titled

OUT = []

# Where each post points back to. Keyed by slug so a new post written in the
# CMS falls back to the services hub until it gets an entry here.
SERVICE_FOR = {
    "what-emdr-feels-like": [("trauma-emdr.html", "Trauma &amp; EMDR therapy")],
    "baby-blues-vs-postpartum-depression": [
        ("mamas-golden-hour.html", "Mama&rsquo;s Golden Hour"),
        ("anxiety-depression.html", "therapy for anxiety and depression")],
    "rest-you-have-to-earn": [("anxiety-depression.html", "Therapy for anxiety and depression")],
}

# Search descriptions, when the card excerpt runs long or short for a
# results page. The excerpt still shows on the Journal cards.
META_DESC = {
    "baby-blues-vs-postpartum-depression":
        "Baby blues, postpartum depression and postpartum anxiety get lumped together. They aren't the same, and knowing which one you're in changes what helps.",
    "what-emdr-feels-like":
        "People expect EMDR to be dramatic. It's quieter and more ordinary than that. A Colorado EMDR therapist on what the first sessions and processing feel like.",
    "rest-you-have-to-earn":
        "If you can only rest once the list is finished, you will never rest, because the list is not a finite object. Where that belief comes from, and where to start.",
}


def emit(slug, **kw):
    io.open(slug, "w", encoding="utf-8").write(page(slug, **kw))
    OUT.append(slug)


def load_posts():
    posts = []
    for f in sorted(glob.glob("content/blog/*.json")):
        p = json.load(io.open(f, encoding="utf-8"))
        p["_file"] = f
        posts.append(p)
    # newest first
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return posts


def render_body(blocks):
    """Minimal block renderer: a line starting '## ' is a heading, else a paragraph.

    Deliberately not full markdown. The author is a therapist, not a
    typesetter, and a small syntax that can't produce broken markup is worth
    more here than a large one that can."""
    out = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if b.startswith("## "):
            out.append("<h2>%s</h2>" % b[3:].strip())
        else:
            out.append("<p>%s</p>" % b)
    return "\n    ".join(out)


def post_url(p):
    return "blog-%s.html" % p["slug"]


def hero_path(p):
    """Full site-relative path to a post's hero image.

    Tina's media picker is rooted at assets/img (see tina/config.ts), so it
    stores and expects just the filename there, not the full path. The
    generator is what needs the full path, so it adds the prefix back on
    here rather than the content JSON carrying it twice."""
    name = p.get("heroImage", "hero.jpg")
    return name if "/" in name else "assets/img/%s" % name


def human_date(iso):
    try:
        date_part = iso[:10]
        y, m, d = date_part.split("-")
        months = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
        return "%s %d, %s" % (months[int(m) - 1], int(d), y)
    except Exception:
        return iso


posts = load_posts()
live = [p for p in posts if p.get("published")]
drafts = [p for p in posts if not p.get("published")]

# ── Remove pages for anything that is no longer published ────────────────
for p in drafts:
    stale = post_url(p)
    if os.path.exists(stale):
        os.remove(stale)
        print("  unpublished, removed:", stale)

# ── Individual post pages ────────────────────────────────────────────────
for p in live:
    ld = {"@context": "https://schema.org", "@type": "BlogPosting",
          "headline": p["title"],
          "datePublished": p.get("date"),
          "description": p.get("excerpt", ""),
          "image": "%s/%s" % (SITE, hero_path(p).lstrip("/")),
          "author": {"@type": "Person", "name": p.get("author", "Golden Hour Wellness Colorado"),
                     "url": clean_url("shayla.html") if p.get("author", "").startswith("Shayla") else SITE + "/"},
          "publisher": {"@type": "MedicalBusiness", "@id": SITE + "/#business",
                        "name": "Golden Hour Wellness Colorado, LLC"},
          "mainEntityOfPage": clean_url(post_url(p))}

    body = head_block("Journal", p["title"],
                      "%s &middot; %s" % (human_date(p.get("date", "")), p.get("author", ""))) + '''
<section class="section">
  <div class="wrap prose">
    <figure>
      <img src="%s" width="1600" height="1066" alt="%s">
    </figure>

    %s

    <div class="callout" style="margin-top:2.5rem">
      <p>If any of this lands close to home, a first conversation is free and
      fifteen minutes. Call or text <a href="tel:+13037369822">(303)&nbsp;736-9822</a>,
      or <a href="contact.html">send a message</a>.</p>
      <p>More on how we work with this: %s.</p>
    </div>

    <p style="margin-top:2rem"><a href="blog.html">&larr; All posts</a></p>
  </div>
</section>''' % (hero_path(p), p.get("heroAlt", ""), render_body(p.get("body", [])),
       " and ".join('<a href="%s">%s</a>' % pair
                    for pair in SERVICE_FOR.get(p["slug"], [("services.html", "our services")]))) + cta()

    emit(post_url(p),
         title=titled(p["title"]),
         desc=META_DESC.get(p["slug"], p.get("excerpt", "")[:180]),
         body=body, active="blog.html",
         crumbs=[("Journal", "blog.html"), (p["title"], post_url(p))],
         img=hero_path(p),
         extra_head='<script type="application/ld+json">%s</script>' % json.dumps(ld))

# ── Index ────────────────────────────────────────────────────────────────
if live:
    cards = "".join('''
      <a class="card postcard" href="%s">
        <img src="%s" width="1600" height="1066" alt="" loading="lazy">
        <div class="postcard__body">
          <p class="postcard__meta">%s</p>
          <h3>%s</h3>
          <p>%s</p>
          <span class="more">Read more &rarr;</span>
        </div>
      </a>''' % (post_url(p), hero_path(p), human_date(p.get("date", "")),
                 p["title"], p.get("excerpt", "")) for p in live)
    inner = '<div class="cards postcards">%s</div>' % cards
else:
    inner = ('<div class="callout"><p>There are no posts here yet. '
             'New writing will appear on this page.</p></div>')

emit("blog.html",
     title=titled("Journal: Notes on Therapy"),
     desc="Notes from the therapists at Golden Hour Wellness Colorado on EMDR, the "
          "baby blues, rest, and the questions that come up most in a first session.",
     crumbs=[("Journal", "blog.html")],
     body=head_block("Journal", "Notes from the practice.",
                     "Occasional writing on the things that come up most often in "
                     "the room. Nothing here is a substitute for therapy, but it "
                     "might make the first conversation easier.") + '''
<section class="section">
  <div class="wrap">
    %s
  </div>
</section>''' % inner + cta())

# ── Keep sitemap.xml in step ────────────────────────────────────────────
# Posts come and go through the CMS, so the sitemap can't be hand-maintained
# without going stale. Everything between the markers is regenerated here.
START, END = "  <!-- blog:start -->", "  <!-- blog:end -->"
sm = io.open("sitemap.xml", encoding="utf-8").read()
rows = ['  <url><loc>%s</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>' % clean_url("blog.html")]
for p_ in live:
    rows.append('  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>yearly</changefreq><priority>0.5</priority></url>'
                % (clean_url(post_url(p_)), p_.get("date", "")))
block = START + "\n" + "\n".join(rows) + "\n" + END
if START in sm and END in sm:
    sm = re.sub(re.escape(START) + r".*?" + re.escape(END), block.replace("\\", "\\\\"), sm, flags=re.S)
else:
    sm = sm.replace("</urlset>", block + "\n</urlset>")
io.open("sitemap.xml", "w", encoding="utf-8").write(sm)

print("blog: %d published, %d draft" % (len(live), len(drafts)))
for o in OUT:
    print("  ", o)
