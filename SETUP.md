# Launch setup — state of play

Live preview: **https://ghwco.pages.dev**
Repo: **github.com/ghwco/ghwco** (Shayla's account, Chad as collaborator)

---

## Done

**GitHub.** Site pushed to `ghwco/ghwco`. `push-to-github.sh` targets it and
stages through `~/Sites/ghwco`.

**Cloudflare Pages.** Connected to the repo, auto-deploying from `main`.

| Setting | Value |
|---|---|
| Build command | `npm install && npm run build` |
| Build output | `dist` |
| Root directory | *(blank)* |

Environment variables set: `NEXT_PUBLIC_TINA_CLIENT_ID`, `TINA_TOKEN`,
`TINA_SEARCH_TOKEN`, `PYTHON_VERSION=3.11`, `NODE_VERSION=20`.

> Switch `TINA_TOKEN` and `TINA_SEARCH_TOKEN` from type **Text** to type
> **Secret**. As Text they're readable in plaintext by anyone with dashboard
> access. Same values, just re-typed.

**TinaCMS.** Project "Golden Hour Wellness Colorado", client ID
`434178a2-76c3-4fe0-8bf6-83b3b3841bc8`. Repo connected, `tina-lock.json`
generated and committed, all four site URLs registered including localhost.

### What Shayla can edit at /admin

| Collection | Controls |
|---|---|
| Homepage | Hero headline and intro, the three points under it, section headlines |
| Mama's Golden Hour — cohort | Dates, time, price, capacity, *enrolling* toggle |
| Practice details | Phone, email, insurers, footer blurb, social links |
| FAQ | The questions, reorderable, add/remove |

Tina edits JSON in `/content`, never the HTML. It commits to GitHub, which
triggers a Cloudflare build, which re-runs the generators. A bad edit can
produce awkward wording; it cannot break layout, schema or accessibility.
That boundary is deliberate.

The cohort fields are the ones that will actually get used — they change every
term, and the `enrolling` toggle swaps in a "this cohort is full" notice
without anyone touching prose.

---

## Next: run one deploy with the full pipeline

Deployments → Retry deployment. This is the **first** run that executes
`tinacms build`, so it's the one that replaces the placeholder at `/admin`
with the real editor. Watch the log rather than assuming — `python3` on
Cloudflare's image and `tinacms build` are both unproven there.

Then add Shayla as a user in Tina so she can sign in.

---

## EmailJS — built, currently routed to Chad for testing

Both templates are built and live in the dashboard:

| Template | ID | Goes to |
|---|---|---|
| Golden Hour - New Enquiry | `template_ql76otu` | **chad.m.moravec@gmail.com** (temporary) |
| Golden Hour - Auto Reply | `template_tkcx2rd` | `{{from_email}}` — the enquirer |

Service `service_0z3erja` (Gmail), public key `4kZZJo5E8VJGKzGGg`. All four IDs
are already wired into `contact.html`.

### Handing the inbox over to Shayla

Two fields in the EmailJS dashboard. Nothing in the codebase changes.

1. **Template `template_ql76otu`** → *To Email* →
   `chad.m.moravec@gmail.com` → `goldenhourwellco@gmail.com`
2. **Template `template_tkcx2rd`** → *Reply To* →
   `ghwco2026@gmail.com` → `goldenhourwellco@gmail.com`

Note the account itself is registered to `ghwco2026@gmail.com` while the site
publishes `goldenhourwellco@gmail.com`. Both are hers; just make sure the one
she reads daily is the one in *To Email*, because that is where a distressed
first-time enquiry lands.

### Lock it down before handover

EmailJS → Account → Security → add `goldenhourwellnesscolorado.com` and
`ghwco.pages.dev` to allowed origins, and enable their CAPTCHA. The public key
is visible in page source by design; the domain allowlist is what stops it
becoming a spam relay. Free tier is 200 sends/month — fine for a practice this
size, but worth watching if it ever gets scraped.

## Still outstanding

**The Gmail/HIPAA gap.** The form routes to consumer Gmail, which has no BAA.
The form collects contact details only and the notice above it asks people to
keep health detail out — that's mitigation, not compliance. People sometimes
volunteer symptoms anyway. The real fix is Google Workspace with a signed BAA
(~$6/user/month) and repointing the EmailJS service at it. Worth raising with
Shayla as a decision she makes knowingly.

**Shayla should read the new copy before it's indexed.** I wrote roughly
1,800 new words describing how the practice works clinically — the "what the
work looks like" sections and the per-service Q&As. It asserts things about
her methods that only she can confirm.

**Hero photo.** Still hosted on the Squarespace CDN. It dies when she cancels
that account. Needs downloading and moving into `assets/img/`.

**DNS / custom domain.** Not done, deliberately. Adding
`goldenhourwellnesscolorado.com` in Cloudflare and repointing nameservers is
the moment the old Squarespace site goes dark, so it waits until Shayla has
signed off. Chad and Claude walk through it together.

**`logo-options.html` / `type-options.html`** are still in the repo. Not
linked, `noindex`, and disallowed in robots.txt — but publicly reachable if
guessed. Delete them whenever.

---

## Local development

```bash
npm install          # once
npm run pages        # regenerate HTML from content/ + the generators
npm run serve        # http://localhost:8080
npm run check        # report drift between content/home.json and index.html
npm run dev          # Tina editor locally at /admin
```

`npm run pages` is the one to run after editing any generator or JSON file.
