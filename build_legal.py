#!/usr/bin/env python3
"""FAQ + legal pages.  python3 build_legal.py"""
import io, json
from build_pages import page, head_block, cta, SITE

OUT = []
def emit(slug, **kw):
    io.open(slug, "w", encoding="utf-8").write(page(slug, **kw)); OUT.append(slug)

UPDATED = "22 August 2026"

# ─────────────────────────────────────────────── FAQ
# Questions live in content/faq.json so Tina can edit them without
# anyone touching Python. Order in the file is order on the page.
QA = [(i["question"], i["answer"])
      for i in json.load(io.open("content/faq.json", encoding="utf-8"))["items"]]

faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,
   "acceptedAnswer":{"@type":"Answer","text":a.replace("&rsquo;","'").replace("&nbsp;"," ")}}
  for q, a in QA]}
items = "".join(
  f'<details><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in QA)

emit("faq.html",
  title="Frequently Asked Questions | Golden Hour Wellness Colorado",
  desc="Answers about insurance, cost, telehealth, EMDR, scheduling and getting started with Golden Hour Wellness Colorado.",
  extra_head=f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>',
  body=head_block("FAQ", "Questions people usually ask first.",
    "If yours isn&rsquo;t here, just ask. We&rsquo;d rather answer it than have it stop you.") + f'''
<section class="section">
  <div class="wrap">
    <div class="faq">{items}</div>
  </div>
</section>''' + cta())

# ─────────────────────────────────────────────── PRIVACY
emit("privacy.html",
  title="Privacy Policy | Golden Hour Wellness Colorado",
  desc="How Golden Hour Wellness Colorado collects, uses and protects information submitted through this website, and why not to send health details.",
  body=head_block("Legal", "Privacy Policy", f"Last updated {UPDATED}.") + f'''
<section class="section">
  <div class="wrap prose">
    <div class="callout warn">
      <p><strong>This policy covers the website only.</strong> Protected health information created in the course of treatment is governed by our separate HIPAA Notice of Privacy Practices, which you receive as part of intake paperwork.</p>
    </div>

    <h2>What we collect</h2>
    <p>If you submit the contact form, we collect the name, email address, phone number, preferred contact method and general enquiry type you provide, plus any message you choose to write.</p>
    <p>We do not use advertising trackers, and we do not sell or share personal information with third parties for marketing.</p>

    <h2>Please don&rsquo;t send health information</h2>
    <p>The contact form is not a secure or encrypted medical channel. Please don&rsquo;t include diagnoses, symptoms, medications or other health details in it. Tell us how to reach you and we&rsquo;ll continue the conversation somewhere private.</p>

    <h2>How we use it</h2>
    <p>Solely to respond to your enquiry and, if you become a client, to arrange care. We keep enquiries only as long as needed for that purpose.</p>

    <h2>Third-party services</h2>
    <p>Some parts of this site are provided by third parties, each with its own privacy policy:</p>
    <ul>
      <li><strong>Acuity Scheduling</strong> (a Squarespace company) powers appointment booking.</li>
      <li><strong>Thrizer</strong> powers the out-of-network benefits checker.</li>
      <li><strong>Google Fonts</strong> serves the typefaces used on this site.</li>
    </ul>
    <p>Information you enter into those tools is handled under their policies, not this one.</p>

    <h2>Your choices</h2>
    <p>You can ask us what enquiry information we hold about you, and ask us to delete it, by emailing <a href="mailto:goldenhourwellco@gmail.com">goldenhourwellco@gmail.com</a>. Requests relating to treatment records are handled under the HIPAA notice instead.</p>

    <h2>Children</h2>
    <p>This site is not directed at children under 13 and we do not knowingly collect their information through it.</p>

    <h2>Changes</h2>
    <p>If this policy changes we&rsquo;ll update the date at the top of this page.</p>

    <h2>Contact</h2>
    <p>Golden Hour Wellness Colorado, LLC<br>
    <a href="mailto:goldenhourwellco@gmail.com">goldenhourwellco@gmail.com</a><br>
    <a href="tel:+13037369822">(303) 736-9822</a></p>
  </div>
</section>''')

# ─────────────────────────────────────────────── TERMS
emit("terms.html",
  title="Terms &amp; Conditions | Golden Hour Wellness Colorado",
  desc="Terms of use for the Golden Hour Wellness Colorado website, including scheduling, licensure, third-party tools and limitations of liability.",
  body=head_block("Legal", "Terms &amp; Conditions", f"Last updated {UPDATED}.") + '''
<section class="section">
  <div class="wrap prose">
    <h2>About this site</h2>
    <p>This website is operated by Golden Hour Wellness Colorado, LLC. By using it you agree to these terms.</p>

    <h2>Not medical advice</h2>
    <p>Everything here is general information about our practice and services. It is not medical or mental health advice, and reading it does not create a therapist-client relationship. That relationship begins only when you and a clinician have agreed to work together and completed intake.</p>

    <div class="callout warn">
      <p><strong>Emergencies.</strong> This site is not monitored for urgent messages. If you are in crisis, call or text <strong>988</strong>, call <strong>Colorado Crisis Services at 1-844-493-8255</strong>, or dial <strong>911</strong>.</p>
    </div>

    <h2>Scheduling and payment</h2>
    <p>Appointments booked through this site are requests until confirmed. Fees, insurance participation and cancellation terms are set out in your intake paperwork and take precedence over anything summarised here.</p>
    <p>Insurance is accepted for individual therapy with participating carriers. It is not accepted for Mama&rsquo;s Golden Hour, which is self-pay.</p>

    <h2>Licensure and location</h2>
    <p>Our clinicians are licensed in Colorado. Services are available only to people physically located in Colorado at the time of the session.</p>

    <h2>Third-party tools and links</h2>
    <p>This site embeds scheduling and insurance-verification tools operated by third parties, and links to external sites such as Psychology Today. We don&rsquo;t control those services and aren&rsquo;t responsible for their content or practices.</p>

    <h2>Intellectual property</h2>
    <p>The text, images, logo and design of this site belong to Golden Hour Wellness Colorado, LLC unless otherwise noted, and may not be reproduced without permission.</p>

    <h2>Limitation of liability</h2>
    <p>The site is provided as is. To the extent permitted by law, Golden Hour Wellness Colorado, LLC is not liable for damages arising from your use of it. Nothing here limits liability for professional services, which is governed by Colorado law and our professional obligations.</p>

    <h2>Governing law</h2>
    <p>These terms are governed by the laws of the State of Colorado.</p>

    <h2>Contact</h2>
    <p><a href="mailto:goldenhourwellco@gmail.com">goldenhourwellco@gmail.com</a> &middot; <a href="tel:+13037369822">(303) 736-9822</a></p>
  </div>
</section>''')

# ─────────────────────────────────────────────── GFE
emit("good-faith-estimate.html",
  title="Good Faith Estimate | Golden Hour Wellness Colorado",
  desc="Your right to a Good Faith Estimate of expected charges under the No Surprises Act, and how to request one from Golden Hour Wellness Colorado.",
  body=head_block("Your rights", "Good Faith Estimate",
    "Under the No Surprises Act you have the right to know what your care will cost before you begin.") + '''
<section class="section">
  <div class="wrap prose">
    <p>You have the right to receive a <strong>Good Faith Estimate</strong> explaining how much your care will cost.</p>

    <p>Under the law, health care providers must give people who are uninsured, or who are not using insurance, an estimate of the expected charges for medical services, including psychotherapy.</p>

    <h2>What this means for you</h2>
    <ul>
      <li>You have the right to a Good Faith Estimate for the total expected cost of any non-emergency services, including psychotherapy.</li>
      <li>You can ask for one before you schedule, or at any point during treatment.</li>
      <li>If you receive a bill that is at least <strong>$400 more</strong> than your Good Faith Estimate, you can dispute it.</li>
      <li>Make sure to save a copy or picture of your estimate.</li>
    </ul>

    <h2>How to request one</h2>
    <p>Just ask. Email <a href="mailto:goldenhourwellco@gmail.com">goldenhourwellco@gmail.com</a> or call <a href="tel:+13037369822">(303)&nbsp;736-9822</a> and we&rsquo;ll send a written estimate covering your expected sessions and rates. We&rsquo;ll also provide one automatically before your first session if you&rsquo;re self-pay.</p>

    <p><a class="btn btn-outline" href="assets/good-faith-estimate.pdf" download>Download the printable notice (PDF)</a></p>

    <h2>Current self-pay rates</h2>
    <table>
      <tr><th>Service</th><th>Rate</th></tr>
      <tr><td>Individual therapy, 50 minutes</td><td>Provided in your written estimate</td></tr>
      <tr><td>Mama&rsquo;s Golden Hour group</td><td>$25 per session, or $150 for six weeks</td></tr>
      <tr><td>Initial consultation</td><td>Free, 15 minutes</td></tr>
    </table>

    <div class="callout">
      <p>If you&rsquo;re using in-network insurance, the Good Faith Estimate requirement doesn&rsquo;t apply in the same way. Your cost is set by your plan, and we&rsquo;ll help you check your benefits before you start.</p>
    </div>

    <h2>Questions or disputes</h2>
    <p>For questions or more information about your right to a Good Faith Estimate, visit <a href="https://www.cms.gov/nosurprises" rel="noopener">www.cms.gov/nosurprises</a> or call <strong>1-800-985-3059</strong>.</p>
  </div>
</section>''')

print("wrote:", len(OUT)); [print("  ", o) for o in OUT]
