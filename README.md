# Golden Hour Wellness Colorado

Static site for Golden Hour Wellness Colorado, LLC. No framework and no build
step to serve it. The HTML in this repo is the site. Cloudflare Pages
publishes the repo root as-is.

**Live:** https://ghwco.pages.dev
**Editor:** `/admin` (TinaCMS)
**Setup steps:** see [SETUP.md](SETUP.md)

---

## How it's put together

Pages are built by Python scripts so the header, footer and nav stay
byte-identical across every page. Editing one file and re-running beats
hand-maintaining the same markup on each one.

```
build_pages.py      shared shell: header, footer, nav, page CSS
build_content.py    about, team, and the three clinician profiles
build_services.py   services hub + 5 service pages + the group page + telehealth
build_legal.py      FAQ, privacy, terms, Good Faith Estimate, insurance
apply_content.py    pushes content/home.json into index.html
```

`index.html`, `contact.html` and `404.html` are hand-tuned and deliberately
NOT generated. The generators leave them alone.

```bash
npm run pages     # regenerate everything
npm run serve     # http://localhost:8080
npm run check     # report drift between content/home.json and index.html
```

Serve over HTTP rather than opening files directly. The Thrizer embed's
`frame-ancestors` policy matches network schemes only, so it won't render
over `file://`.

## Content editing

Editable content lives in `/content` as JSON. TinaCMS edits those files,
commits to GitHub, and the build re-runs the generators.

| File | Controls |
|---|---|
| `home.json` | Homepage hero, trust points, section headlines |
| `group.json` | Mama's Golden Hour cohort: dates, price, capacity, enrolling flag |
| `practice.json` | Phone, email, insurers, footer blurb, social links |
| `faq.json` | The FAQ page questions |
| `blog/*.json` | One file per Journal post. `published: false` means the page is never built at all |

Tina never touches the HTML. A bad edit can produce awkward wording; it
cannot break layout, schema or accessibility. That boundary is the point.

## Third-party embeds

Both were lifted from the old Squarespace site and have no Squarespace
dependency, so they keep working after that account is canceled.

| | |
|---|---|
| Acuity scheduler | `app.acuityscheduling.com/schedule.php?owner=35696713`, self-resizing |
| Thrizer benefits | `eligibility.thrizer.com/facility/thrizerpei0crb`, no resize event |

Thrizer's height is set by `sizeBenefitsFrame()` in `assets/site.js`, keyed
off the **frame's** measured width rather than the viewport, because Thrizer
reflows at 768px and 480px of frame width and a viewport-keyed query left a
176px gap at tablet. The iframe gets its full natural height plus a 24px
bleed, and `.benefits-clip` trims the excess. Shrinking the iframe instead
makes Thrizer's own page scroll.

## Contact form

`contact.html` is deliberately not a clinical intake. Neither Resend nor
consumer Gmail is covered by a BAA, so no PHI should travel through it. The
safeguards are structural:

- No field invites clinical detail; inquiry type is a fixed non-diagnostic list
- Message capped at 300 characters with an explicit do-not-include warning
- Consent checkbox gates submission; submit is disabled until ticked
- Honeypot plus a timing check for bots
- Inquiry type and insurance are checked server-side against the same fixed lists
- Nothing stored client-side

If Shayla ever wants real intake here, that needs a BAA-covered form
provider. It is not a CSS change.

## Contact form (Resend)

Since November 2026 the form posts to `/api/contact`, a Cloudflare Pages
Function in `functions/api/contact.js`. It sends through Resend from a
verified subdomain (`website@notify.goldenhourwellnesscolorado.com`), so it no
longer depends on a Gmail sign-in and a password change can't break it.
EmailJS is gone from the page; the files in `emailjs/` are kept only as the
original design reference for the two emails.

What it sends:
- A branded notification to the practice inbox. Reply goes straight to the visitor.
- A confirmation to the visitor with the one-business-day reply time, the
  phone and email to use if nobody answers, and the 988 and Colorado Crisis
  Services lines.

`functions/` lives at the repo root, not in `dist/`. Cloudflare Pages picks
Functions up from the project root regardless of the build output folder.

Cloudflare Pages > Settings > Variables and Secrets (set for Production and Preview):

| Name | What |
|---|---|
| `RESEND_API_KEY` | Secret. Resend API key for this domain |
| `TO_EMAIL` | `goldenhourwellco@gmail.com` |
| `FROM_EMAIL` | `website@notify.goldenhourwellnesscolorado.com` |
| `HEALTH_TOKEN` | Secret. Random string used by the daily health check |
| `HEALTH_TO` | Where health checks go (not the practice inbox) |
| `TURNSTILE_SECRET` | Optional. Turns on the Cloudflare Turnstile spam check |

Optional: bind a KV namespace as `SUBMISSIONS` and every inquiry is saved for
30 days before any email goes out, so nothing is lost if delivery fails.

Health check: POST to `/api/contact` with header `x-health-token: <HEALTH_TOKEN>`
and a JSON body with `name`, `email` and `message`. It emails only `HEALTH_TO`,
with a `[Health check]` subject, sends no auto-reply and saves nothing. A
wrong token gets a 401 and sends nothing.

To rotate the Resend key: create a new key in Resend, paste it into
`RESEND_API_KEY`, redeploy, then delete the old key.

If sending fails, the visitor sees the phone number and email address
instead of a dead end. A 400 means a field needs fixing and shows that message.

DNS: Resend needs its DKIM and SPF records on the `notify` subdomain before it
will send. The root domain should also get SPF and a DMARC record, or replies
and auto-replies are more likely to land in spam.

## Accessibility and SEO

Skip link, visible focus rings, alt text throughout, one `h1` per page,
`aria-current` on the active nav item, 44px tap targets, and scroll-reveal
animations that respect `prefers-reduced-motion`. Verified with no horizontal
overflow at 1440 / 834 / 390.

Every page carries a canonical URL, Open Graph and Twitter tags and JSON-LD:
`MedicalBusiness` (`#business`) on the homepage, which every other page points
back to by `@id`; `MedicalTherapy` and `FAQPage` on service pages; `Person` on
profiles; `Event` on the group page; `FAQPage` on the FAQ, insurance and
telehealth pages; and a `BreadcrumbList` on inner pages
(`page(..., crumbs=[...])` in build_pages.py).
`llms.txt` gives search and answer engines a plain-language summary so their
descriptions of the practice come out accurate.

Internal linking: each service page links to the insurance page, contact, and
one or two journal posts (`related=` in build_services.py, which skips any
post that isn't published). Each post links back to its service
(`SERVICE_FOR` in build_blog.py). Search descriptions for posts can be set in
`META_DESC` in build_blog.py when the card excerpt is the wrong length.

`/insurance` used to 301 to `/faq#insurance`. It is now a real page, so that
rule is gone from `_redirects` (a rule there would hide the page).

## Known outstanding

- **Hero image** still loads from the old Squarespace CDN and dies when that
  account is canceled. Download and self-host.
- **Gmail has no BAA.** See SETUP.md.
- `logo-options.html` and `type-options.html` are working files, `noindex`
  and disallowed in robots.txt. Delete whenever.

## Copy

Clinical and bio copy originates with Shayla. Section headlines, service-page
detail and the FAQs were written for the site and should be reviewed by her
for clinical accuracy. Nothing about credentials or experience was invented.

## Palette and type

Clay `#A85832` · Clay deep `#82431F` · Gold `#F0C579` · Plum `#423049` ·
Plum deep `#2E2034` · Sand `#F4EBE1` · Cream `#FBF7F2` · Shell `#FFFDFB`

Fraunces (display) and Inter (body), both Google Fonts. Logo files and a
brand sheet are supplied separately in the brand kit.
