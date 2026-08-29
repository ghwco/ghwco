# Launch setup — the parts that need your logged-in accounts

Everything in the codebase is done. What's left is four dashboards, and each
one needs credentials I shouldn't be handling. Roughly 20 minutes total.

Work through these in order — Cloudflare needs the repo, Tina needs the repo
and Cloudflare's env vars, EmailJS is independent.

---

## 1. Push to the repo in Shayla's name

The push script currently targets `losmanzanos/shayla`. Point it at the new
repo first:

```bash
# edit this line in push-to-github.sh
REPO="https://github.com/<owner>/<repo>.git"
```

Then push. The old preview repo can stay as-is or be deleted — nothing
depends on it.

**Verify:** `content/`, `tina/`, `emailjs/`, `package.json` and `.gitignore`
are all present in the pushed tree.

---

## 2. Cloudflare Pages

Connect the repo, then set:

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | `npm install && npm run build` |
| Build output directory | `/` |
| Root directory | *(leave blank)* |

Environment variables (Settings → Environment variables, **both** Production
and Preview):

```
NEXT_PUBLIC_TINA_CLIENT_ID   <from Tina, step 3>
TINA_TOKEN                   <from Tina, step 3>
PYTHON_VERSION               3.11
NODE_VERSION                 20
```

You'll need to come back and fill the two Tina values after step 3, then
re-run the deploy.

**Custom domain:** add `goldenhourwellnesscolorado.com` and `www` once the
build is green. Cloudflare will want the nameservers pointed at it — that's
the moment the site goes live, so do it last.

**Verify:** the deploy log shows the Python generators running, then
`tinacms build`. Visit `/sitemap.xml` and `/robots.txt` on the
`*.pages.dev` URL.

---

## 3. TinaCMS

In app.tina.io, on the project connected to this repo:

1. Overview → copy **Client ID** → that's `NEXT_PUBLIC_TINA_CLIENT_ID`
2. Tokens → create/copy a **read-only token** → that's `TINA_TOKEN`
3. Paste both into Cloudflare (step 2) and redeploy
4. Configuration → confirm the branch is `main`

Then add Shayla as a user in Tina so she can log in. She goes to
`goldenhourwellnesscolorado.com/admin/`, signs in, and edits.

### What she can edit

| Collection | What it controls |
|---|---|
| Homepage | Hero headline and intro, the three points under it, section headlines |
| Mama's Golden Hour — cohort | Dates, time, price, capacity, and an *enrolling* toggle |
| Practice details | Phone, email, insurers, footer blurb, social links |
| FAQ | The ten questions, reorderable, add/remove |

**The important part:** Tina edits JSON in `/content`, never the HTML. It
commits to GitHub, which triggers a Cloudflare build, which re-runs the
generators. A bad edit can produce awkward wording; it cannot break layout,
schema, or accessibility. That boundary is deliberate.

The cohort fields are the ones that will actually get used — they change
every term, and the `enrolling` toggle swaps in a "this cohort is full"
notice without anyone editing prose.

**Verify:** make a trivial edit in `/admin`, save, and watch a Cloudflare
build kick off. Confirm the change appears on the live page.

---

## 4. EmailJS

Two templates are in `emailjs/`. Paste each into EmailJS → Email Templates →
new template → the **Code** (`</>`) tab.

**`template-notification.html`** — goes to the practice.

| Field | Value |
|---|---|
| To | `goldenhourwellco@gmail.com` |
| Reply-To | `{{from_email}}` ← so Reply reaches the enquirer |
| Subject | `New enquiry from {{from_name}} — {{enquiry_type}}` |

**`template-autoreply.html`** — goes to the person who wrote in. Optional but
worth it; it carries the crisis numbers, which matters for a form someone
might fill in at 2am.

| Field | Value |
|---|---|
| To | `{{from_email}}` |
| Reply-To | `goldenhourwellco@gmail.com` |
| Subject | `We got your message — Golden Hour Wellness Colorado` |

Then replace four placeholders in `contact.html`:

```
EMAILJS_PUBLIC_KEY               Account → General → Public Key
EMAILJS_SERVICE_ID               Email Services → your Gmail service
EMAILJS_TEMPLATE_ID              the notification template
EMAILJS_AUTOREPLY_TEMPLATE_ID    the auto-reply, or '' to skip
```

They appear in two places — the `emailjs.init()` call near the bottom and the
`CFG` object just below it.

**Lock it down before launch:** EmailJS → Account → Security → add
`goldenhourwellnesscolorado.com` to the allowed origins, and turn on their
CAPTCHA. The public key is visible in page source by design; the domain
allowlist is what stops it becoming a spam relay.

**Verify:** submit the form on the live site. Until the keys are in, it
fails loudly with a console error and tells the visitor to call instead —
deliberately, so nobody sees "message sent" for an email that never sent.

---

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
