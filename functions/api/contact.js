/**
 * Contact form handler for goldenhourwellnesscolorado.com
 * Cloudflare Pages Function: POST /api/contact
 *
 * Environment variables (Pages > Settings > Variables and Secrets, set for
 * both Production and Preview):
 *   RESEND_API_KEY    required, secret. Resend API key.
 *   TO_EMAIL          required. Where inquiries land
 *                     (goldenhourwellco@gmail.com).
 *   FROM_EMAIL        required. Verified Resend sender, either a bare address
 *                     (website@notify.goldenhourwellnesscolorado.com) or
 *                     "Name <address>".
 *   HEALTH_TOKEN      optional, secret. Enables the daily health check.
 *   HEALTH_TO         optional. Where health checks go (Chad only).
 *   TURNSTILE_SECRET  optional, secret. Turns on the Cloudflare Turnstile check.
 *
 * Optional binding:
 *   SUBMISSIONS       KV namespace. When bound, every real inquiry is saved
 *                     for 30 days before any email is sent, so a lead is never
 *                     lost even if email delivery fails.
 *
 * Health check: POST with header "x-health-token: <HEALTH_TOKEN>" and any valid
 * name, email and message. It sends one email to HEALTH_TO with a
 * "[Health check]" subject, skips the auto-reply and the saved copy, and never
 * touches the practice inbox.
 *
 * HIPAA posture: this form is not a clinical intake. Inquiry type and
 * insurance are fixed lists, the message is capped at 300 characters, and the
 * visitor must confirm the channel isn't secure before sending. Keep it that
 * way. Real intake belongs in Acuity or the EHR portal.
 */

const PRACTICE = 'Golden Hour Wellness Colorado';
const SITE = 'goldenhourwellnesscolorado.com';
const SITE_URL = 'https://www.goldenhourwellnesscolorado.com';
const PHONE = '(303) 736-9822';
const PHONE_HREF = 'tel:+13037369822';
const PRACTICE_EMAIL = 'goldenhourwellco@gmail.com';
const REPLY_TIME = 'one business day';
const MAX_MESSAGE = 300;

// The dropdowns on /contact send their visible text. Anything outside these
// lists is replaced, so the email never carries free text from those fields.
const INTERESTS = [
  'Individual therapy',
  'Couples therapy',
  'Group therapy',
  'EMDR / trauma support',
  'Mama’s Golden Hour group',
  'Substance use support',
  'Not sure yet',
];
const INSURERS = ['Aetna', 'United Healthcare', 'Cigna', 'Other / out-of-network', 'Self-pay'];
const PREFER = { email: 'Email', phone: 'Phone call', text: 'Text' };

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });

const esc = (s = '') =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const validEmail = (e) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(e || '').trim());

// Constant-time compare so the health token can't be guessed by timing.
function sameToken(a = '', b = '') {
  if (!a || !b || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

const truthy = (v) => v === true || ['on', 'true', 'yes', '1'].includes(String(v || '').toLowerCase());

// Brand palette, from assets/brand.css.
const C = {
  clay: '#A85832',
  plumDeep: '#2E2034',
  plum: '#423049',
  gold: '#F0C579',
  sand: '#F4EBE1',
  cream: '#FBF7F2',
  shell: '#FFFDFB',
  ink: '#3A342F',
  inkMid: '#4A443E',
  inkSoft: '#6E6A66',
  label: '#8B857E',
  hair: '#EFE8DF',
  line: '#E4DCD2',
};
const SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif";
const SERIF = "Georgia, 'Times New Roman', serif";

// Table layout and inline styles on purpose: Gmail, Outlook and Apple Mail
// strip <style> blocks and ignore flex and grid.
function shell(inner, footer) {
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:0;background:${C.sand};font-family:${SANS};color:${C.ink};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${C.sand};padding:24px 12px;">
  <tr><td align="center">
    <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:100%;background:${C.shell};border-radius:14px;overflow:hidden;border:1px solid ${C.line};">
      <tr><td style="background:${C.plumDeep};padding:22px 28px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
          <td style="padding-right:12px;vertical-align:middle;">
            <img src="${SITE_URL}/assets/img/email-mark.png" width="38" height="38" alt="" style="display:block;border:0;border-radius:19px;">
          </td>
          <td style="vertical-align:middle;">
            <div style="font-family:${SERIF};font-size:18px;font-weight:600;color:#ffffff;">Golden Hour Wellness</div>
            <div style="font-size:10px;letter-spacing:2.4px;text-transform:uppercase;color:${C.gold};padding-top:3px;">Colorado</div>
          </td>
        </tr></table>
      </td></tr>
      ${inner}
      <tr><td style="background:${C.plumDeep};padding:16px 28px;text-align:center;font-size:11.5px;line-height:1.7;color:#B7ADA4;">${footer}</td></tr>
    </table>
  </td></tr>
</table>
</body></html>`;
}

const row = (k, v, last = false) => {
  const b = last ? '' : `border-bottom:1px solid ${C.hair};`;
  return `<tr>
                <td width="130" style="padding:11px 0;${b}color:${C.label};font-size:11px;letter-spacing:1.2px;text-transform:uppercase;vertical-align:top;">${esc(k)}</td>
                <td style="padding:11px 0;${b}font-size:14px;color:${C.ink};">${v}</td>
              </tr>`;
};

function notification(f) {
  const replySubject = `Your message to ${PRACTICE}`;
  const phoneCell = f.phone
    ? `<a href="tel:${esc(f.phone.replace(/[^\d+]/g, ''))}" style="color:${C.clay};text-decoration:none;">${esc(f.phone)}</a>`
    : 'Not given';
  const inner = `
      <tr><td style="padding:28px 28px 6px;">
        <div style="font-size:11px;letter-spacing:1.8px;text-transform:uppercase;color:${C.clay};font-weight:700;">New inquiry from the website</div>
        <div style="font-family:${SERIF};font-size:24px;color:${C.plumDeep};font-weight:600;padding-top:8px;line-height:1.25;">${esc(f.name)}</div>
        <div style="font-size:14px;color:${C.inkSoft};padding-top:6px;">${esc(f.interest)}</div>
      </td></tr>
      <tr><td style="padding:20px 28px 0;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              ${row('Email', `<a href="mailto:${esc(f.email)}" style="color:${C.clay};text-decoration:none;">${esc(f.email)}</a>`)}
              ${row('Phone', phoneCell)}
              ${row('Prefers', esc(f.prefer))}
              ${row('Insurance', esc(f.insurance))}
              ${row('Consent', esc(f.consent), true)}
        </table>
      </td></tr>
      <tr><td style="padding:22px 28px 0;">
        <div style="font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:${C.label};padding-bottom:9px;">Message</div>
        <div style="background:${C.cream};border-left:3px solid ${C.clay};border-radius:0 8px 8px 0;padding:15px 17px;font-size:14.5px;line-height:1.6;color:${C.ink};white-space:pre-wrap;">${esc(f.message || 'No additional message.')}</div>
      </td></tr>
      <tr><td style="padding:24px 28px 4px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
          <td style="background:${C.clay};border-radius:8px;">
            <a href="mailto:${esc(f.email)}?subject=${encodeURIComponent(replySubject)}" style="display:inline-block;padding:13px 26px;font-size:14px;font-weight:600;color:#ffffff;text-decoration:none;">Reply to ${esc(f.first)}</a>
          </td>
        </tr></table>
        <div style="font-size:12px;color:${C.label};padding-top:12px;line-height:1.5;">Hitting Reply in your inbox works too. It goes straight to ${esc(f.first)}.</div>
      </td></tr>
      <tr><td style="padding:22px 28px 26px;">
        <div style="border:1px solid #EBD9A9;background:#FDF8EC;border-radius:8px;padding:13px 15px;font-size:12.5px;line-height:1.55;color:${C.inkSoft};">
          <strong style="color:#8A6A43;">Before you reply:</strong> this inbox is not a secure channel for health information. Keep clinical detail out of email and move it to a phone call or the practice portal once you&rsquo;ve made contact.
        </div>
      </td></tr>`;
  const text = [
    `New inquiry from ${f.name} through ${SITE}`,
    '',
    `Looking for: ${f.interest}`,
    `Email: ${f.email}`,
    `Phone: ${f.phone || 'Not given'}`,
    `Prefers: ${f.prefer}`,
    `Insurance: ${f.insurance}`,
    `Consent: ${f.consent}`,
    '',
    f.message || 'No additional message.',
    '',
    `Submitted ${f.when}`,
    'Reply to this email to answer them directly. Keep health details out of email.',
  ].join('\n');
  const footer = `Sent from the contact form at <a href="${SITE_URL}/" style="color:${C.gold};text-decoration:none;">${SITE}</a> &nbsp;&middot;&nbsp; ${esc(f.when)}`;
  return { html: shell(inner, footer), text };
}

function autoReply(f) {
  const link = (path, label) =>
    `<a href="${SITE_URL}${path}" style="color:${C.clay};text-decoration:none;">${label}</a>`;
  const inner = `
      <tr><td style="padding:30px 28px 0;">
        <div style="font-family:${SERIF};font-size:23px;color:${C.plumDeep};font-weight:600;line-height:1.3;">Thanks for reaching out, ${esc(f.first)}.</div>
        <div style="font-size:15px;line-height:1.65;color:${C.inkMid};padding-top:16px;">Your message got here. Someone from our team will reply within ${REPLY_TIME}, usually sooner.</div>
        <div style="font-size:15px;line-height:1.65;color:${C.inkMid};padding-top:14px;">If you don&rsquo;t hear back within ${REPLY_TIME}, please call or text <a href="${PHONE_HREF}" style="color:${C.clay};text-decoration:none;font-weight:600;">${PHONE.replace(' ', '&nbsp;')}</a> or email <a href="mailto:${PRACTICE_EMAIL}" style="color:${C.clay};text-decoration:none;font-weight:600;">${PRACTICE_EMAIL}</a>. Messages do occasionally go astray, and we&rsquo;d hate to miss you.</div>
        <div style="font-size:15px;line-height:1.65;color:${C.inkMid};padding-top:14px;">First conversations are a free 15 minutes, with no cost and no obligation.</div>
      </td></tr>
      <tr><td style="padding:24px 28px 0;">
        <div style="background:${C.cream};border-left:3px solid ${C.clay};border-radius:0 8px 8px 0;padding:15px 17px;">
          <div style="font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:${C.label};padding-bottom:8px;">What you sent</div>
          <div style="font-size:14px;line-height:1.6;color:${C.ink};">${esc(f.interest)}</div>
          ${f.message ? `<div style="font-size:14px;line-height:1.6;color:${C.ink};white-space:pre-wrap;padding-top:8px;">${esc(f.message)}</div>` : ''}
        </div>
      </td></tr>
      <tr><td style="padding:24px 28px 0;">
        <div style="font-size:13.5px;line-height:1.6;color:${C.inkSoft};">While you wait, these might help:</div>
        <div style="padding-top:10px;font-size:14px;line-height:2;">
          ${link('/faq', 'Questions people usually ask first')}<br>
          ${link('/team', 'Meet the clinicians')}<br>
          ${link('/services', 'What we help with')}
        </div>
      </td></tr>
      <tr><td style="padding:24px 28px 28px;">
        <div style="border:1px solid #E9C4B8;background:#FCF2EF;border-radius:8px;padding:14px 16px;font-size:13px;line-height:1.6;color:#5A4E48;">
          <strong style="color:#8E3A26;">If you need help before then:</strong> this inbox isn&rsquo;t monitored for emergencies. Call or text <a href="tel:988" style="color:#8E3A26;font-weight:700;text-decoration:none;">988</a> (Suicide &amp; Crisis Lifeline) or <strong>Colorado Crisis Services at 1-844-493-8255</strong>. Both are staffed 24 hours a day. In an emergency, call 911.
        </div>
      </td></tr>`;
  const text = [
    `Thanks for reaching out, ${f.first}.`,
    '',
    `Your message got here. Someone from our team will reply within ${REPLY_TIME}, usually sooner.`,
    '',
    `If you don't hear back within ${REPLY_TIME}, please call or text ${PHONE} or email ${PRACTICE_EMAIL}.`,
    '',
    'First conversations are a free 15 minutes, with no cost and no obligation.',
    '',
    `${PRACTICE}`,
    SITE_URL,
    '',
    "If you need help before then: this inbox isn't monitored for emergencies. Call or text 988 (Suicide & Crisis Lifeline) or Colorado Crisis Services at 1-844-493-8255. Both are staffed 24 hours a day. In an emergency, call 911.",
  ].join('\n');
  const footer = `${PRACTICE}, LLC &nbsp;&middot;&nbsp; Licensed in the State of Colorado<br>
        <a href="${SITE_URL}/" style="color:${C.gold};text-decoration:none;">${SITE}</a> &nbsp;&middot;&nbsp; <a href="${SITE_URL}/privacy" style="color:#B7ADA4;text-decoration:none;">Privacy</a>`;
  return { html: shell(inner, footer), text };
}

async function send(env, payload) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => '');
    throw new Error(`Resend ${res.status}: ${detail.slice(0, 300)}`);
  }
}

const FALLBACK = `Your message didn't go through. Please call or text ${PHONE}, or email ${PRACTICE_EMAIL}.`;

export async function onRequestPost({ request, env, waitUntil }) {
  let data;
  try {
    const ct = request.headers.get('content-type') || '';
    data = ct.includes('application/json') ? await request.json() : Object.fromEntries(await request.formData());
  } catch {
    return json({ ok: false, error: 'Could not read that submission.' }, 400);
  }
  if (!data || typeof data !== 'object') return json({ ok: false, error: 'Could not read that submission.' }, 400);

  // Honeypot: people never see this field, so anything in it is a bot.
  if (data.website || data._gotcha || data.company) return json({ ok: true });

  // A health check with a wrong or missing token is refused outright, so a
  // misconfigured monitor can never land a test in the practice inbox.
  const healthHeader = request.headers.get('x-health-token');
  const health = healthHeader !== null && sameToken(healthHeader, env.HEALTH_TOKEN || '');
  if (healthHeader !== null && !health) return json({ ok: false, error: 'Unauthorized.' }, 401);

  const first = String(data.first || '').trim().slice(0, 60);
  const last = String(data.last || '').trim().slice(0, 60);
  const name = (String(data.name || '').trim() || [first, last].filter(Boolean).join(' ')).slice(0, 120);
  const interest = String(data.interest || '').trim();
  const insurance = String(data.insurance || '').trim();
  const f = {
    name,
    first: first || name.split(/\s+/)[0] || '',
    email: String(data.email || '').trim().slice(0, 200),
    phone: String(data.phone || '').trim().slice(0, 40),
    prefer: PREFER[String(data.prefer || 'email')] || PREFER.email,
    interest: INTERESTS.includes(interest) ? interest : (health ? 'Health check' : ''),
    insurance: INSURERS.includes(insurance) ? insurance : 'Not given',
    message: String(data.message || '').trim().slice(0, MAX_MESSAGE),
    consent: truthy(data.consent) ? 'Yes, confirmed this isn’t a secure channel' : 'Not confirmed',
    when: new Date().toLocaleString('en-US', { timeZone: 'America/Denver', dateStyle: 'medium', timeStyle: 'short' }) + ' MT',
  };

  if (!f.name || !validEmail(f.email)) {
    return json({ ok: false, error: 'Please add your name and a valid email address.' }, 400);
  }
  if (!health && !f.interest) {
    return json({ ok: false, error: 'Please choose what you’re looking for.' }, 400);
  }
  if (!health && !truthy(data.consent)) {
    return json({ ok: false, error: 'Please tick the box confirming you understand this form isn’t a secure channel.' }, 400);
  }

  if (env.TURNSTILE_SECRET && !health) {
    const body = new FormData();
    body.append('secret', env.TURNSTILE_SECRET);
    body.append('response', data['cf-turnstile-response'] || '');
    const ip = request.headers.get('CF-Connecting-IP');
    if (ip) body.append('remoteip', ip);
    const v = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body })
      .then((r) => r.json())
      .catch(() => ({ success: false }));
    if (!v.success) return json({ ok: false, error: 'The spam check didn’t go through. Please try again.' }, 400);
  }

  if (!env.RESEND_API_KEY || !env.TO_EMAIL || !env.FROM_EMAIL) {
    console.error('Contact form: RESEND_API_KEY, TO_EMAIL or FROM_EMAIL is not set.');
    return json({ ok: false, error: FALLBACK }, 500);
  }
  if (health && !env.HEALTH_TO) {
    return json({ ok: false, error: 'HEALTH_TO is not set.' }, 500);
  }

  const from = /</.test(env.FROM_EMAIL) ? env.FROM_EMAIL : `${PRACTICE} <${env.FROM_EMAIL}>`;
  const later = typeof waitUntil === 'function' ? waitUntil : (p) => p;

  // Save first, so the inquiry survives even if every email below fails.
  if (env.SUBMISSIONS && !health) {
    const key = `inquiry:${new Date().toISOString()}:${crypto.randomUUID().slice(0, 8)}`;
    try {
      await env.SUBMISSIONS.put(key, JSON.stringify({ ...f, delivered: false }), { expirationTtl: 60 * 60 * 24 * 30 });
      f.savedKey = key;
    } catch (err) {
      console.error('KV save failed', err);
    }
  }

  const note = notification(f);
  try {
    await send(env, {
      from,
      to: [health ? env.HEALTH_TO : env.TO_EMAIL],
      reply_to: f.email,
      subject: `${health ? '[Health check] ' : ''}New inquiry from ${f.name}: ${f.interest}`,
      html: note.html,
      text: note.text,
    });
  } catch (err) {
    console.error(err);
    return json({ ok: false, error: FALLBACK }, 502);
  }

  if (f.savedKey) {
    later(env.SUBMISSIONS.put(f.savedKey, JSON.stringify({ ...f, delivered: true }), { expirationTtl: 60 * 60 * 24 * 30 }).catch(() => {}));
  }

  // The visitor's confirmation is a courtesy. If it fails, the inquiry still
  // reached the practice, so the visitor still sees success.
  if (!health) {
    const reply = autoReply(f);
    later(
      send(env, {
        from,
        to: [f.email],
        reply_to: env.TO_EMAIL,
        subject: `We got your message | ${PRACTICE}`,
        html: reply.html,
        text: reply.text,
      }).catch((err) => console.error('Auto-reply failed', err)),
    );
  }

  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: 'Method not allowed.' }, 405);
