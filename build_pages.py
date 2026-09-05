#!/usr/bin/env python3
"""
Generates the inner pages of the Golden Hour site.

Why a generator rather than 15 hand-written files: the header, footer and
nav have to be byte-identical everywhere, and hand-maintaining them across
15 pages is how drift starts. Edit this file, re-run it, done.

  python3 build_pages.py

index.html, contact.html and 404.html are NOT generated. They were built and
tuned by hand and this script deliberately leaves them alone.
"""
import io, os

SITE = "https://www.goldenhourwellnesscolorado.com"
PHONE_HREF = "tel:+13037369822"
PHONE = "(303) 736-9822"
EMAIL = "goldenhourwellco@gmail.com"

# Google Analytics 4 (GA4) — property "Golden Hour Wellness Colorado",
# measurement ID G-14KQ8308P5. Must be the first thing after <head> so it
# starts capturing before anything else loads. Same snippet on every page,
# generated or hand-written (index.html, contact.html, 404.html carry it too
# since build_pages.py doesn't touch those — keep all four in sync if this
# ID ever changes).
GA_TAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-14KQ8308P5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-14KQ8308P5');
</script>'''

MARK = '''<svg class="brand__mark" viewBox="0 0 64 64" aria-hidden="true">
        <defs>
          <linearGradient id="s1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#F3CB80"/><stop offset="100%" stop-color="#DE9855"/></linearGradient>
          <linearGradient id="r1" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#B4623A"/><stop offset="100%" stop-color="#8A4623"/></linearGradient>
          <clipPath id="c1"><circle cx="32" cy="32" r="29"/></clipPath>
        </defs>
        <circle cx="32" cy="32" r="29" fill="#FBF7F2"/>
        <g clip-path="url(#c1)">
          <circle cx="32" cy="27.5" r="12.5" fill="url(#s1)"/>
          <path d="M-4 51 L17 36.5 L27.5 46 L41 27 L55 47 L68 51 Z" fill="url(#r1)"/>
          <path d="M34.8 35.73 L41 27 L47.6 36.43 C45.6 34.5 43.9 33.9 42.5 34.7 C41.8 35.1 41.2 35.1 40.5 34.7 C38.9 33.8 36.9 34.5 34.8 35.73 Z" fill="#FBF7F2" opacity=".95"/>
          <rect x="0" y="51" width="64" height="13" fill="#423049"/>
        </g>
        <circle cx="32" cy="32" r="29" fill="none" stroke="#A85832" stroke-width="2.5"/>
      </svg>'''

# Insurance used to be an anchor into the homepage, which meant the nav item
# scrolled you somewhere rather than taking you to a page — confusing, and it
# gave the topic no URL of its own. It now lives at the top of the FAQ, which
# is where people look for cost questions anyway.
NAV = [("index.html", "Home"), ("about.html", "About"),
       ("services.html", "Services"), ("team.html", "Our Team"),
       ("blog.html", "Journal"), ("faq.html", "FAQ"),
       ("contact.html", "Contact")]

RIDGE = '''  <div class="footer__ridge" aria-hidden="true">
    <svg viewBox="0 0 1440 90" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M0,90 L0,66 L150,38 L268,58 L392,22 L520,52 L648,34 L790,64 L920,30 L1064,56 L1200,26 L1330,50 L1440,34 L1440,90 Z" fill="#7C5F76" opacity=".42"/>
      <path d="M0,90 L0,74 L128,52 L246,70 L378,40 L500,66 L636,50 L772,76 L900,46 L1046,70 L1186,44 L1320,66 L1440,52 L1440,90 Z" fill="#2E2034"/>
    </svg>
  </div>'''


def header(active):
    CUR = ' aria-current="page"'
    links = "".join(
        '\n      <a href="%s"%s>%s</a>' % (h, CUR if h == active else "", t)
        for h, t in NAV)
    return f'''<header class="header" id="header">
  <div class="wrap header__inner">
    <a class="brand" href="index.html" aria-label="Golden Hour Wellness Colorado home">
      {MARK}
      <span class="brand__text">
        <span class="brand__name">Golden Hour Wellness</span>
        <span class="brand__sub">Colorado</span>
      </span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">{links}
      <a class="btn btn-primary" href="index.html#book">Book Now</a>
    </nav>
    <a class="btn btn-primary header__cta" href="index.html#book">Book Now</a>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''


FOOTER = f'''<footer class="footer">
{RIDGE}
  <div class="wrap footer__grid">
    <div>
      <span class="brand__text" style="display:block">
        <span class="brand__name" style="font-size:1.25rem">Golden Hour Wellness</span>
        <span class="brand__sub" style="display:block">Colorado</span>
      </span>
      <p style="margin-top:1.15rem; max-width:32ch">Therapist-owned counseling for trauma, EMDR and addiction. Serving clients across Colorado.</p>
      <div class="social">
        <a href="https://www.instagram.com/goldenhourwellnesscolorado" aria-label="Instagram" rel="noopener">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4.5"/><circle cx="12" cy="12" r="3.75"/><circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/></svg>
        </a>
        <a href="https://www.psychologytoday.com/profile/1406337" aria-label="Psychology Today profile" rel="noopener">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h8a5 5 0 0 1 0 10H9v6H5z"/></svg>
        </a>
      </div>
    </div>

    <div>
      <h4>Explore</h4>
      <ul class="footer__links">
        <li><a href="about.html">About</a></li>
        <li><a href="services.html">Services</a></li>
        <li><a href="team.html">Our Team</a></li>
        <li><a href="blog.html">Journal</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="faq.html#insurance">Insurance &amp; rates</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>

    <div>
      <h4>Get in touch</h4>
      <ul class="footer__contact">
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{PHONE_HREF}">{PHONE}</a></li>
      </ul>
      <div class="crisis">
        <strong>In crisis?</strong> This site is not for emergencies. Call or text <strong>988</strong> (Suicide &amp; Crisis Lifeline), or <strong>Colorado Crisis Services at 1-844-493-8255</strong>. Both available 24/7.
      </div>
    </div>
  </div>
  <div class="wrap">
    <p class="goldenhour">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.2M12 19.2v2.2M2.6 12h2.2M19.2 12h2.2M5.4 5.4l1.6 1.6M17 17l1.6 1.6M18.6 5.4 17 7M7 17l-1.6 1.6"/></svg>
      Today&rsquo;s golden hour in Colorado <span class="gh-sep">&middot;</span> <b id="ghTime">calculating</b>
    </p>
  </div>
  <div class="wrap footer__bar">
    <span>&copy; <span id="yr">2026</span> Golden Hour Wellness Colorado, LLC</span>
    <span>Licensed in the State of Colorado &middot; <a href="privacy.html">Privacy</a> &middot; <a href="terms.html">Terms</a> &middot; <a href="good-faith-estimate.html">Good Faith Estimate</a></span>
  </div>
</footer>'''


PAGE_CSS = '''
.page-head{background:var(--sand); border-bottom:1px solid var(--hair); padding:clamp(2.75rem,6vw,4.5rem) 0 clamp(2.25rem,4vw,3rem)}
.prose{max-width:44rem}
.prose h2{margin-top:2.5rem}
.prose h3{margin-top:1.9rem; color:var(--plum)}
.prose ul,.prose ol{padding-left:1.15rem; color:var(--ink-mid)}
.prose li{margin-bottom:.5rem}
.prose table{width:100%; border-collapse:collapse; margin:1.5rem 0; font-size:.94rem}
.prose th,.prose td{text-align:left; padding:.7rem .6rem; border-bottom:1px solid var(--hair)}
.prose th{font-size:.72rem; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-soft)}
.callout{background:var(--lilac-mist); border-left:2px solid var(--lilac); border-radius:0 var(--r-sm) var(--r-sm) 0; padding:1.05rem 1.2rem; margin:1.5rem 0; font-size:.92rem; color:var(--plum)}
.callout p:last-child{margin:0}
.warn{background:rgba(180,71,47,.06); border-left-color:#B4472F; color:var(--ink-mid)}
.warn strong{color:#8E3A26}
.cards{display:grid; grid-template-columns:repeat(3,1fr); gap:1.25rem; margin-top:2.5rem}
@media (max-width:980px){.cards{grid-template-columns:repeat(2,1fr)}}
@media (max-width:620px){.cards{grid-template-columns:1fr}}
/* ── Orphan-row centering ─────────────────────────────────────────────
   With 5 cards in a 3-across grid the last row holds 2 and hangs left.
   Switching to a 6-column track and spanning each card 2 columns lets
   the final pair start at column 2 and 4, which centres them under the
   row above. The :nth-child/:nth-last-child pair means this only fires
   when there are exactly 5 cards, so 3- and 6-card grids are untouched. */
@media (min-width:981px){
  .grid-3, .cards{grid-template-columns:repeat(6,1fr)}
  .grid-3 > *, .cards > *{grid-column:span 2}
  .grid-3 > :nth-child(4):nth-last-child(2),
  .cards  > :nth-child(4):nth-last-child(2){grid-column:2 / span 2}
  .grid-3 > :nth-child(5):nth-last-child(1),
  .cards  > :nth-child(5):nth-last-child(1){grid-column:4 / span 2}
}
/* Same trick one breakpoint down. In the 2-across band a trailing odd card
   hangs left — team.html's three profiles do exactly this on a tablet.
   A 4-column track with span 2 lets that lone last card sit across 2–3.
   :nth-child(odd):nth-last-child(1) means "last card, and odd-numbered",
   which in a 2-col grid is precisely the case where it's alone in its row. */
@media (min-width:621px) and (max-width:980px){
  .grid-3, .cards{grid-template-columns:repeat(4,1fr)}
  .grid-3 > *, .cards > *{grid-column:span 2}
  .grid-3 > :nth-child(odd):nth-last-child(1),
  .cards  > :nth-child(odd):nth-last-child(1){grid-column:2 / span 2}
}
/* single column: the span must be released or each card fills half a row */
@media (max-width:620px){
  .grid-3 > *, .cards > *{grid-column:auto}
}

/* Photo set inside a prose column. Capped and centered so it never towers over
   the text on a phone; height:auto keeps the width/height attributes from
   being read as a CSS presentational hint and stretching the image. */
.prose figure{margin:2.25rem auto; max-width:38rem}
.prose figure img{display:block; width:100%; height:auto; aspect-ratio:3/2; object-fit:cover;
  border-radius:var(--r-lg); box-shadow:var(--shadow-md)}
.prose figcaption{margin-top:.7rem; font-size:.78rem; color:var(--ink-soft); text-align:center}

/* Blog cards carry a hero image, so the padding moves inside and the image
   sits flush to the card edge. aspect-ratio keeps the grid even regardless of
   what dimensions the author uploads through the CMS. */
.postcards .card{padding:0; overflow:hidden}
.postcard img{display:block; width:100%; height:auto; aspect-ratio:3/2; object-fit:cover}
.postcard__body{padding:1.5rem 1.5rem 1.75rem}
.postcard__meta{margin:0 0 .5rem; font-size:.72rem; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-soft)}
.postcard h3{margin-top:0}

.card{background:var(--shell); border:1px solid var(--line); border-radius:var(--r); padding:1.75rem 1.5rem; text-decoration:none; color:inherit; display:flex; flex-direction:column; transition:border-color .2s ease, transform .2s ease, box-shadow .2s ease}
.card:hover{border-color:rgba(168,88,50,.32); transform:translateY(-2px); box-shadow:var(--shadow-sm)}
.card h3{margin:0 0 .4rem; color:var(--plum); font-size:1.15rem}
.card p{margin:0; font-size:.93rem; color:var(--ink-mid)}
.card .more{margin-top:.9rem; font-size:.84rem; font-weight:600; color:var(--clay-deep)}
.faq{border-top:1px solid var(--hair); max-width:46rem}
.faq details{border-bottom:1px solid var(--hair)}
.faq summary{cursor:pointer; list-style:none; padding:1.15rem 2rem 1.15rem 0; font-family:var(--serif); font-size:1.08rem; color:var(--plum); position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+"; position:absolute; right:.25rem; top:1rem; font-family:var(--sans); font-size:1.3rem; color:var(--clay); transition:transform .2s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq .a{padding:0 0 1.3rem; color:var(--ink-mid); font-size:.95rem; max-width:44rem}
.faq .a p:last-child{margin:0}
.bio-grid{display:grid; grid-template-columns:.85fr 1.15fr; gap:clamp(2rem,5vw,3.5rem); align-items:start}
@media (max-width:820px){.bio-grid{grid-template-columns:1fr; max-width:34rem}}
.bio-photo img{width:100%; height:auto; border-radius:var(--r-lg); box-shadow:var(--shadow-md); aspect-ratio:4/5; object-fit:cover}
.meta-list{list-style:none; padding:0; margin:1.5rem 0 0; font-size:.9rem}
.meta-list li{display:flex; gap:.7rem; padding:.6rem 0; border-bottom:1px solid var(--hair)}
.meta-list b{color:var(--plum); min-width:6.5rem; font-weight:600}
'''


def page(slug, title, desc, body, extra_head="", active=None, extra_css="", img="assets/img/hero.jpg"):
    canon = f"{SITE}/" if slug == "index.html" else f"{SITE}/{slug}"
    img_abs = img if img.startswith("http") else f"{SITE}/{img}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{GA_TAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="assets/favicon-v2.svg" type="image/svg+xml">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Golden Hour Wellness Colorado">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img_abs}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{img_abs}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/brand.css">
{extra_head}
<style>{PAGE_CSS}{extra_css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{header(active or slug)}

<main id="main">
{body}
</main>

{FOOTER}

<script src="assets/site.js"></script>
</body>
</html>
'''


def head_block(eyebrow, h1, lede=""):
    l = f'\n      <p class="lede">{lede}</p>' if lede else ""
    return f'''<section class="page-head">
  <div class="wrap">
    <div class="measure">
      <p class="eyebrow">{eyebrow}</p>
      <h1 style="font-size:clamp(2.1rem,4.4vw,3.1rem)">{h1}</h1>{l}
    </div>
  </div>
</section>'''


def cta():
    return '''<section class="section" style="background:var(--sand); text-align:center">
  <div class="wrap">
    <h2>Ready when you are.</h2>
    <p class="lede" style="margin-inline:auto">Book a free 15-minute consultation, or call <a href="tel:+13037369822">(303)&nbsp;736-9822</a>.</p>
    <div style="display:flex; gap:.7rem; justify-content:center; flex-wrap:wrap; margin-top:1.75rem">
      <a class="btn btn-primary" href="index.html#book">Book a consultation</a>
      <a class="btn btn-outline" href="contact.html">Send a message</a>
    </div>
  </div>
</section>'''
