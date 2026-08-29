# Golden Hour Wellness Colorado — static build

No framework, no build step. Drop the folder on Netlify / Cloudflare Pages / GitHub Pages.

```
golden-hour/
├── index.html          ← VERSION 1 (self-contained, CSS+JS inline)
├── v2.html             ← VERSION 2 — refined corners, new icons, revised snowcap
├── contact.html        ← contact form with HIPAA safeguards
├── 404.html            ← branded not-found page
├── assets/
│   ├── brand.css       ← v2 design system (shared by v2 / contact / 404)
│   ├── site.js         ← shared behaviour (nav, tabs, frame sizing, reveal)
│   ├── favicon.svg     ← v1 mark (sharp snowcap)
│   ├── favicon-v2.svg  ← v2 mark (rounded snow drift)
│   └── logo-lockup.svg ← stacked logo for print / social
└── README.md
```

**v1 is untouched.** It's still the single-file build you approved, and `index.html` is still what loads at the root of the preview. v2 links back to it via the bar at the top.

---

## What changed in v2, and why

**Corner radius — yes, v1 read a little young.** v1 used 18/28px cards with fully-round pill buttons. At that scale it lands closer to a consumer app than a clinical practice. v2 uses a tighter architectural scale (4/6/10/14/18px) with 8px buttons. Nothing is a hard corner, so it's still soft — but warmth now comes from colour, photography and type rather than from roundness. That's the main lever if you want to push further in either direction: `--r*` in `brand.css`.

**Icons.** v1 put line icons inside gradient-filled rounded squares. Those tiles were the single most template-looking element on the page. v2 drops the tile entirely: a 1.25px-stroke mark sits directly on the card next to a serif index numeral and a hairline rule. Lighter, more editorial, and it stops competing with the photography.

**Snowcap.** v1's cap was a hard zigzag (`M42 24 L47 31 L42 33 L37 30 Z`) that read as a chevron and fought the soft ridgeline. v2 draws a drift on a bezier — three rounded lobes, thicker at the peak, thinning downslope. Looks like settled snow rather than a graphic arrow.

**Photography.** Three Unsplash images added and verified loading: dawn peaks above cloud (hero), light through trees (insurance), and a misty ridge (CTA + 404). All are warm and on-palette. Deliberately avoided the arms-raised-at-sunrise genre — it's the exact stock cliché that makes wellness sites look cheap.

**Mobile pills.** The trust strip is now a single hairline-divided list where every row is identical width, and all three insurance carriers are equal (v1 had Aetna spanning full width with the other two beneath, which was the raggedness you spotted). Verified at 606px: trust rows 558/558/558, carriers 558/558/558, tabs 271/271.

**Other polish.** Fine grain overlay on the hero to stop gradient banding, a stat band, an editorial quote band over photography, hairline-ruled eyebrows, photo credits, and `aria-current` on the active nav item.

---

## Utility bar

A slim plum strip sits above the header on **all three** v2 pages, with identical markup and an identical nav beneath it. Two jobs:

- **Insurance panels in front of every visitor.** It's the first thing most people filter on, and it was previously buried below three therapist bios.
- **Click-to-call.** On mobile this is consistently the highest-converting element on a practice site. The insurance line hides under 820px so the phone number owns the bar on a phone.

The green dot on "Accepting new clients" is a small live-status cue. Kill it by deleting `.dot` if it reads as too SaaS.

## Footer extras

Two things beyond the standard columns, identical on all three v2 pages:

**Ridgeline.** An SVG silhouette rising out of the footer into the section above, two overlapping ridges echoing the logo mark. Decorative only, `aria-hidden`, scales with the viewport. The back ridge is a warm mauve rather than a tint of the footer colour, because plum-deep at low opacity over cream reads cold grey.

**Live golden-hour clock.** Renders today's actual golden hour for Colorado, e.g. *"Today's golden hour in Colorado · 7:11 to 8:11 PM"*. The practice is named for it, so showing the real window is a small factual piece of delight that changes daily.

It's computed locally with the NOAA solar equations in `site.js` — no API, no key, no network call, works offline. Times render through `Intl` in `America/Denver` so DST is handled automatically. Verified against known Denver values: winter solstice 4:38 PM, summer solstice 8:30 PM, equinox 7:10 PM, all within a minute. Golden hour is taken as the hour before sunset, the standard photographic definition. If the maths ever fails (it can't at this latitude, but still) the whole line hides rather than leaving a dangling placeholder.

## Hero legibility

The hero uses the lake-at-sunrise photo (the same one v1 used). It's warmer and more grounded than the cloud-sea alternative, but it has a bright sun flare roughly where the headline sits, so legibility needed real work rather than a single dark overlay:

1. **`object-position: 56% 56%`** shifts the frame so the flare falls to the left edge instead of directly behind the type. Tested 68% (very safe but lost most of the warm glow) and 56% (keeps the golden ice and sky, flare still clear of the text). 56% is the balance point.
2. **Three stacked scrims** — a radial pool under the text block, a heavy left-to-right linear gradient, and a vertical one for the trust strip.
3. **A soft text-shadow** on the `h1` and lede as insurance against the flare's brightest pixels.

If you ever swap the photo, re-check `object-position` first. It does more work than the gradients do.

**Neither hero option is actually Colorado** — both are European alpine stock. That's the same category of problem as the Squarespace template photo on her current homepage. Real Colorado photography from Shayla would beat either; she's a Colorado native with an active Instagram and may already have something usable.

## Team photos

The three sources are inconsistent, so each is cropped in CSS rather than re-edited:

| | Source | Treatment |
|---|---|---|
| Shayla | Squarespace CDN, wide full-body | `.zoom` — scale 2.05 to get a headshot crop |
| Ashley | Squarespace CDN, studio headshot | `.zoom-sm` — scale 1.22 to crop past white margins baked into the file |
| Chrissie | `assets/img/chrissie.jpg`, self-hosted | none — pre-cropped to 4:5 |

Chrissie's is already local (1086×1357, cropped to the frame, 287KB progressive JPEG). **Shayla's and Ashley's still come from her Squarespace CDN and will die the day she cancels** — download and convert both before launch, then drop the `.zoom` classes and crop the files properly instead.

## Before pushing this live

Two things are still preview-only and will hurt if they ship:

1. **`<meta name="robots" content="noindex, nofollow">`** is in the head of all three v2 pages. Correct while this lives on a `github.io` URL so it can't compete with her real site. **Catastrophic if it ships on her domain** — Google will drop the site entirely. Remove it the moment this points at goldenhourwellnesscolorado.com.
2. **Images still load from her Squarespace CDN.** They die the day she cancels. Download, convert to WebP, and serve locally.

## Contact page — read before touching the form

`contact.html` is deliberately **not** a clinical intake. EmailJS is not a HIPAA business associate and consumer Gmail carries no BAA, so no PHI should ever travel through it. The safeguards are structural, not decorative:

1. **No field invites clinical detail.** "What are you looking for?" is a fixed dropdown of non-diagnostic categories, not free text.
2. **The message box is capped at 300 characters** with an explicit do-not-include warning — long enough to arrange a call, too short to become a history.
3. **An explicit consent checkbox gates submission.** The submit button is disabled until it's ticked.
4. **Honeypot + timing check** for spam. EmailJS public keys are visible in the page by design, so the domain allowlist in their dashboard is what actually stops abuse — enable it.
5. **Nothing is stored client-side.** No localStorage, no analytics on field values.

The submit handler is stubbed with a `TODO` block showing exactly where EmailJS goes. **Route delivery to a BAA-covered inbox** (Google Workspace with a signed BAA, ~$7/mo), not consumer Gmail — people volunteer health details anyway, whatever the form says.

If Shayla ever wants real intake here, that needs a BAA-covered form provider. It is not a CSS change.

## Palette

| Token | Hex | Use |
|---|---|---|
| `--clay` | `#B5623A` | primary terracotta |
| `--clay-deep` | `#8E4A2E` | terracotta on light (passes contrast) |
| `--ember` | `#C9764A` | gradient midpoint |
| `--apricot` | `#E9A65D` | gradient, accents |
| `--gold` | `#F5C86E` | highlight on dark |
| `--petal` | `#F2CFC4` | soft pink |
| `--plum` | `#4A3550` | dark purple — headings, nav, footer |
| `--plum-deep` | `#362439` | footer base |
| `--lilac` / `--lilac-mist` | `#B9A3C4` / `#EFE7F1` | light purple accents, tags |
| `--cream` / `--sand` | `#FDF8F2` / `#F7EDE2` | backgrounds |

Type: **Fraunces** (display) + **Inter** (body), both Google Fonts.

## Before this goes live

1. **Self-host the images.** They currently point at Shayla's Squarespace CDN, which stops working the day she cancels. Download and drop into `assets/`, then convert to WebP/AVIF.
2. **Confirm the "headshot 3" photo is Ashley.** Flagged with an HTML comment in the team section — the source site doesn't label it.
3. **Get a headshot for Chrissie.** Currently an initials placeholder (`CF`).
4. **Get a second landscape photo.** The insurance section reuses the hero image with a warm tint and a different crop so it doesn't read as a repeat — but a distinct photo would be better.
5. **Wire up the real links.** `/appointments` should point at her Acuity/Squarespace Scheduling URL. The newsletter form is inert — connect Mailchimp/Buttondown, or Netlify Forms.
6. **Create `/privacy` and `/good-faith-estimate`.** Both are linked in the footer.
7. **Add an `og:image`.** 1200×630, referenced in the meta block.

## Third-party embeds (both verified working)

A tabbed **Book & verify** section sits above the final CTA. Both embeds were lifted from the live Squarespace site and have **no Squarespace dependency**.

| | Source | Notes |
|---|---|---|
| Acuity scheduler | `app.acuityscheduling.com/schedule.php?owner=35696713` | Plus `embed.acuityscheduling.com/js/embed.js` for auto-resize. Loaded lazily. |
| Thrizer benefits | `eligibility.thrizer.com/facility/thrizerpei0crb?type=iframe` | CSP is `frame-ancestors *` — embeddable from any http/https origin. |

Both iframes use `data-src` and only load when their tab is opened, so neither third party blocks initial page load.

**Testing note:** the Thrizer iframe will *not* render over `file://` — its `frame-ancestors *` policy matches network schemes only. Serve over `http://localhost` (e.g. `python3 -m http.server 8080`) to test it. Acuity works either way.

**Height tuning:** Acuity self-resizes via its embed script. Thrizer sends no resize event, so its height comes from `sizeBenefitsFrame()` in the inline JS.

That function keys off the **frame's own measured width**, not the viewport. This matters: Thrizer reflows at 768px and 480px of *frame* width, which lands very close to our own breakpoints — so a viewport-keyed media query produced a 176px gap at tablet the moment the shell's padding changed. Measured values:

| Frame width | Thrizer layout | Visible height |
|---|---|---|
| ≥ 768px | 3-across | 464px ✅ measured |
| 480–767px | 2-across, DOB on its own row | 670px ✅ measured |
| < 480px | fully stacked | 882px ✅ measured |

These crop just *below* Thrizer's lavender card border so the border and its rounded bottom corners stay visible. Cropping level with the border shaves it off and the card looks open-ended.

Thrizer pads roughly 18px of blank canvas below its own lavender card border. The table above is the **visible** height, cropped to that border so our white shell padding sits directly against it — uniform on all four sides, matching the Acuity tab.

**Don't crop by shrinking the iframe.** If the iframe is even 1px shorter than Thrizer's document, their page scrolls and an internal scrollbar appears. Instead the iframe is given its full natural height plus a 24px `BLEED`, and a `.benefits-clip` wrapper with `overflow:hidden` trims the excess. `sizeBenefitsFrame()` sets both — wrapper to the visible height, iframe to visible + bleed. If you ever adjust one, adjust both.

All three are now measured against the live widget. If Thrizer ever changes their form layout, re-measure: increase the value if the "Powered by thrizer" footer is clipped, decrease it if grey canvas appears below the card border.

Both panels keep the same padded `.embed-shell`, so the white border is identical whichever tab you're on.

Deep link `/#benefits` opens the benefits tab directly — useful for emails and Psychology Today.

## Full-height hero

The hero fills exactly one screen on load, so no sliver of the next section peeks above the fold.

Two things make that work, and both matter:

- **`100svh`, not `100vh`.** `svh` is the *small* viewport height — the state the page loads in, with browser chrome visible. Plain `vh` is the *large* height, which overflows on mobile until the address bar hides.
- **The header height is subtracted.** The header is `position:sticky`, so it occupies flow space above the hero. `measureHeader()` writes its real pixel height to a `--header-h` custom property on load, on `load` again (once webfonts settle and the header may reflow), and on resize. The hero is `min-height:calc(100svh - var(--header-h))`.

Under `max-height:800px` the display type shrinks rather than letting the hero overshoot and push the trust bar below the fold. `.hero h1 .nb` keeps "golden hour —" on one line so the headline can't split mid-phrase at those smaller sizes.

## Mobile

There's a dedicated `MOBILE REFINEMENTS` block at the end of the CSS (`max-width:640px`, plus a `380px` step for the tabs). The desktop defaults went ragged on phones — the fix throughout is **making repeated elements share one width** so each section reads as a clean stack:

| Was | Now |
|---|---|
| Trust bar: 3 centred pills, 3 different widths, 166px tall | Full-width left-aligned stack, 160px |
| Hero buttons: two different widths | Both full-width |
| Eyebrow wrapped to two lines | Tightened tracking, fits one |
| Tabs: wrapped and cramped | Equal-width grid, 52px tall; single column under 380px |
| Insurance carriers: ragged row | 2-col grid, "Aetna" spans full width |
| CTA buttons, footer signup | Stacked full-width |

**Watch out for this one:** `.signup` uses `flex:1 1 12rem` on the input. Once the container becomes `flex-direction:column` on mobile, that basis applies to *height* and the email field balloons to 192px tall. The mobile block resets it with `flex:0 0 auto` — if you ever restructure the footer, that trap is still there.

Audited at 500px (the narrowest this test browser allows):

- **Horizontal overflow: none.** `scrollWidth === clientWidth`.
- **Tap targets:** down from 15 undersized to 2. The remaining two are the phone and email links inside the booking note — they're inline within a sentence, which is an explicit exception under WCAG 2.5.8.
- **Hero fits one screen** with the trust bar fully visible.
- **Thrizer's `<480px` height (882px) is now confirmed correct** — the card border and rounded corners land exactly against the shell padding. That value is no longer an estimate.

## What's built in

- Sticky header with mobile nav, responsive down to 320px
- Scroll-reveal animations, disabled under `prefers-reduced-motion`
- Skip link, visible focus rings, alt text throughout, semantic heading order (one `h1`)
- `MedicalBusiness` JSON-LD structured data
- Crisis resources (988 + Colorado Crisis Services) in the footer
- Good Faith Estimate notice in the insurance section
- Collapsible bios via native `<details>` — no JS required
- No testimonials, by design (see the ethics note in the meeting doc)

## Copy

Every word of bio and clinical copy is Shayla's, pulled from the live site. Section headlines and CTAs are new. Nothing about credentials, experience, or approach was invented.
