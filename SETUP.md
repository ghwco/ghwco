# Launch setup: state of play

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
| Mama's Golden Hour cohort | Dates, time, price, capacity, *enrolling* toggle |
| Practice details | Phone, email, insurers, footer blurb, social links |
| FAQ | The questions, reorderable, add/remove |
| **Journal** | Blog posts: create, edit, and a real Published on/off switch |

Tina edits JSON in `/content`, never the HTML. It commits to GitHub, which
triggers a Cloudflare build, which re-runs the generators. A bad edit can
produce awkward wording; it cannot break layout, schema or accessibility.
That boundary is deliberate.

The cohort fields are the ones that will actually get used. They change every
term, and the `enrolling` toggle swaps in a "this cohort is full" notice
without anyone touching prose.

---

## Next: run one deploy with the full pipeline

Deployments → Retry deployment. This is the **first** run that executes
`tinacms build`, so it's the one that replaces the placeholder at `/admin`
with the real editor. Watch the log rather than assuming. `python3` on
Cloudflare's image and `tinacms build` are both unproven there.

Then add Shayla as a user in Tina so she can sign in.

---

## Contact form: Resend (EmailJS retired November 2026)

The form posts to `/api/contact` (`functions/api/contact.js`) and sends
through Resend. Env vars, the health check and key rotation are in the
README under "Contact form (Resend)".

The old EmailJS service (`service_0z3erja`, templates `template_ql76otu` and
`template_tkcx2rd`) is no longer called by the site. Leave it in place until
the Resend version has delivered a real inquiry, then it can be disabled.

---

## Whenever the Tina schema changes: READ THIS

Editing `tina/config.ts` (adding a collection, adding a field) puts the local
schema out of step with what TinaCloud has indexed. The Cloudflare build then
fails with:

    The local GraphQL schema doesn't match the remote GraphQL schema.
    Reason: [NON_BREAKING - TYPE_ADDED] Type 'X' was added

This is Tina refusing to build against a stale schema rather than serving
something wrong. The fix is always the same:

```bash
cd "$HOME/Desktop/Projects/Clients/golden-hour-wellness-WORKING-SOURCE"
npx tinacms dev      # wait for "Dev Server is active", then Ctrl+C
```

That regenerates `tina-lock.json`. Commit and push it. TinaCloud re-indexes
from the push, and the next build passes.

**Content edits never need this.** Only schema changes do. Anything Shayla
does through /admin is content, so she will never hit it.

The previous successful deployment stays live throughout, so a failed build
never takes the site down.

## Still outstanding

**The Gmail/HIPAA gap.** The form routes to consumer Gmail, which has no BAA.
The form collects contact details only and the notice above it asks people to
keep health detail out. That's mitigation, not compliance. People sometimes
volunteer symptoms anyway. The real fix is Google Workspace with a signed BAA
(~$6/user/month) and pointing `TO_EMAIL` at that inbox. Worth raising with
Shayla as a decision she makes knowingly.

**Shayla should read the new copy before it's indexed.** I wrote roughly
1,800 new words describing how the practice works clinically: the "what the
work looks like" sections and the per-service Q&As. It asserts things about
her methods that only she can confirm.

**Hero photo.** Still hosted on the Squarespace CDN. It dies when she cancels
that account. Needs downloading and moving into `assets/img/`.

**DNS / custom domain.** Not done, deliberately. Adding
`goldenhourwellnesscolorado.com` in Cloudflare and repointing nameservers is
the moment the old Squarespace site goes dark, so it waits until Shayla has
signed off. Chad walks through it with her.

**`logo-options.html` / `type-options.html`** are still in the repo. Not
linked, `noindex`, and disallowed in robots.txt, but publicly reachable if
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
