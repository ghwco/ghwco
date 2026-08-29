#!/usr/bin/env python3
"""Page content + writer. Run:  python3 build_content.py"""
import io, json
from build_pages import page, head_block, cta, SITE

W = lambda slug, html: io.open(slug, "w", encoding="utf-8").write(html)
OUT = []

def emit(slug, **kw):
    W(slug, page(slug, **kw)); OUT.append(slug)

# ─────────────────────────────────────────────── ABOUT
emit("about.html",
  title="About | Golden Hour Wellness Colorado",
  desc="A therapist-owned counseling practice in Colorado specializing in trauma, EMDR and addiction counseling. Founded by Shayla Martinez-O'Brien, LPC.",
  body=head_block("About", "A practice built around the person in the room.",
       "Golden Hour Wellness Colorado, LLC is a small, therapist-owned counseling practice serving clients across the state.") + '''
<section class="section">
  <div class="wrap prose">
    <p>The practice was founded by <a href="shayla.html">Shayla Martinez-O&rsquo;Brien</a>, a Licensed Professional Counselor with 11 years of clinical practice. What began as one clinician is now a small, hand-picked team.</p>

    <p>We believe true healing comes from an increased ability to tolerate challenging emotion, paired with a clearer understanding of your own value system. That work is slow, human, and worth it, and you don&rsquo;t have to do it alone.</p>

    <h2>How we work</h2>
    <p>Therapy here is collaborative rather than prescriptive. You set the pace. We bring the training, the structure, and an honest read on what seems to be helping.</p>
    <p>Sessions are available in person and by telehealth anywhere in Colorado. If you&rsquo;re not sure what you need yet, that&rsquo;s a normal place to start, and a free consultation is the right first step.</p>

    <h2>Who we work with</h2>
    <p>Adults navigating trauma, anxiety, depression, substance use, relationship strain and major life transitions. We also run <a href="mamas-golden-hour.html">Mama&rsquo;s Golden Hour</a>, a virtual therapy group for Colorado mothers.</p>

    <div class="callout">
      <p><strong>If we&rsquo;re not the right fit, we&rsquo;ll say so.</strong> Part of a first conversation is working out whether this practice is the right place for you. Sometimes the honest answer is a referral elsewhere, and that&rsquo;s a good outcome too.</p>
    </div>

    <h2>What &ldquo;golden hour&rdquo; means</h2>
    <p>Photographers use the term for the hour after sunrise and before sunset, when the light is low and warm and makes almost anything look softer. It&rsquo;s also a clinical term for the window right after an injury when care matters most.</p>
    <p>Both meanings are the point. Therapy is often about arriving in a difficult window and being met properly in it, and about the fact that the same life can look very different under a different quality of light.</p>

    <h2>What to expect</h2>
    <p>A first conversation is a free fifteen-minute call. No intake forms, no commitment — you say as much as you want about what brings you in, and we work out together whether this is the right place.</p>
    <p>If it is, the first full session is mostly history and orientation. Sessions run 50 minutes, usually weekly to begin with, moving to less often as things settle. You&rsquo;ll know roughly what the plan is by the end of the first few.</p>
    <p>Some people come for a focused stretch of eight to twelve sessions around one issue. Others stay considerably longer. We&rsquo;ll keep checking honestly whether the work is helping, and you&rsquo;re free to pause or stop whenever you want.</p>

    <h2>Insurance</h2>
    <p>We&rsquo;re in-network with <strong>Aetna</strong>, <strong>United Healthcare</strong> and <strong>Cigna</strong>. If your plan isn&rsquo;t one of those, get in touch anyway and we can talk through out-of-network reimbursement and self-pay rates. You&rsquo;re also entitled to a <a href="good-faith-estimate.html">Good Faith Estimate</a> before your first session.</p>
    <p class="callout warn"><strong>Please note:</strong> insurance is not accepted for Mama&rsquo;s Golden Hour. Group sessions are self-pay.</p>
  </div>
</section>''' + cta())

# ─────────────────────────────────────────────── TEAM
emit("team.html",
  title="Our Team | Golden Hour Wellness Colorado",
  desc="Meet the clinicians at Golden Hour Wellness Colorado: Shayla Martinez-O'Brien LPC, Chrissie Flynn-Weirich LAC, and Ashley LeRossignol LPC.",
  body=head_block("Our team", "Three clinicians. Roughly 34 years of practice between them.") + '''
<section class="section">
  <div class="wrap">
    <div class="cards">
      <a class="card" href="shayla.html">
        <h3>Shayla Martinez-O&rsquo;Brien</h3>
        <p><strong>LPC &middot; Founder</strong><br>Trauma, EMDR and substance use. Accepting individual clients.</p>
        <span class="more">Read profile &rarr;</span>
      </a>
      <a class="card" href="chrissie.html">
        <h3>Chrissie Flynn-Weirich</h3>
        <p><strong>LAC &middot; Wellness Facilitator</strong><br>Substance use, anxiety and life transitions. Accepting individual clients.</p>
        <span class="more">Read profile &rarr;</span>
      </a>
      <a class="card" href="ashley.html">
        <h3>Ashley LeRossignol</h3>
        <p><strong>LPC &middot; Consultant &amp; group facilitator</strong><br>Co-facilitates Mama&rsquo;s Golden Hour. Does not take individual clients here.</p>
        <span class="more">Read profile &rarr;</span>
      </a>
    </div>

    <div class="callout" style="margin-top:2.5rem; max-width:44rem">
      <p><strong>Scheduling.</strong> Individual sessions are available with Shayla and Chrissie. Ashley&rsquo;s work with the practice is limited to co-facilitating <a href="mamas-golden-hour.html">Mama&rsquo;s Golden Hour</a> and clinical consultation.</p>
    </div>
  </div>
</section>

<section class="section" style="background:var(--sand)">
  <div class="wrap prose">
    <h2>How we choose who you see</h2>
    <p>On your first call we&rsquo;ll ask enough to point you at the right person. Trauma and EMDR go to Shayla. Substance use and recovery usually go to Chrissie. Anxiety, depression and life transitions can go to either, and sometimes the deciding factor is simply who has availability that suits your week.</p>
    <p>Fit matters more than credentials past a certain point. If the person you start with doesn&rsquo;t feel right, say so — moving to the other clinician is straightforward and nobody takes it personally. If neither of us is the right answer, we&rsquo;ll help you find someone who is.</p>

    <h2>A small practice on purpose</h2>
    <p>Golden Hour is deliberately small. It means you&rsquo;re seen by the person you chose rather than whoever is next in a rota, that your clinician knows your history without re-reading a file, and that scheduling is handled by people who actually work here.</p>
    <p>It also means we say no sometimes. When something falls outside what we do well, a referral is a better outcome than stretching to cover it.</p>

    <h2>Licensing and consultation</h2>
    <p>All three clinicians are licensed in Colorado, which is the state you need to be physically located in during sessions. The team meets for clinical consultation, so the thinking behind your care isn&rsquo;t happening in isolation — a normal and expected part of good practice, and it happens without identifying details leaving the room.</p>
  </div>
</section>''' + cta())

# ─────────────────────────────────────────────── PROFILES
def profile(slug, name, cred, img, w, h, tags, lead, paras, bookable, extra_meta):
    person = {"@context":"https://schema.org","@type":"Person","name":name,
              "jobTitle":cred,"worksFor":{"@type":"MedicalBusiness","name":"Golden Hour Wellness Colorado, LLC"},
              "url":f"{SITE}/{slug}"}
    book = ('<a class="btn btn-primary" href="index.html#book">Book with ' + name.split()[0] + '</a>'
            if bookable else
            '<a class="btn btn-outline" href="mamas-golden-hour.html">About the group</a>')
    meta = "".join(f"<li><b>{k}</b><span>{v}</span></li>" for k, v in extra_meta)
    body = head_block("Our team", name, cred) + f'''
<section class="section">
  <div class="wrap bio-grid">
    <div class="bio-photo">
      <img src="assets/img/{img}" width="{w}" height="{h}" alt="Portrait of {name}">
      <ul class="meta-list">{meta}</ul>
    </div>
    <div class="prose" style="max-width:none">
      <p class="lede">{lead}</p>
      {"".join(f"<p>{p}</p>" for p in paras)}
      <p style="margin-top:2rem">{book}</p>
    </div>
  </div>
</section>'''
    emit(slug, title=f"{name} | Golden Hour Wellness Colorado",
         desc=lead[:180], body=body, active="team.html",
         extra_head=f'<script type="application/ld+json">{json.dumps(person)}</script>')

profile("shayla.html", "Shayla Martinez-O&rsquo;Brien", "LPC &middot; Founder",
  "shayla.jpg", 1086, 1357, [],
  "A Licensed Professional Counselor in Colorado, specializing in trauma therapy, with 11 years of practice.",
  ["I use Eye Movement Desensitization and Reprocessing (EMDR) among other trauma-focused approaches to help clients better tolerate emotion related to past and present traumas and stressors.",
   "I believe true healing comes from an increased ability to tolerate challenging emotion along with a better understanding of one&rsquo;s own value system. I would love the opportunity to walk alongside you in your journey to improved self-awareness, strengthened positive neural pathways, and deeper connection with who you are.",
   "I&rsquo;m a Colorado native and do my very best to live up to the stereotype. I&rsquo;m married, a mother of two, with two lab mixes at home.",
   "<strong>How I work.</strong> Sessions with me are structured but not scripted. I&rsquo;ll usually have a direction in mind and I&rsquo;ll say what it is, because I&rsquo;d rather you know where we&rsquo;re going than have to guess. If something isn&rsquo;t working, I want to hear it &mdash; that conversation is part of the work, not an interruption to it.",
   "<strong>Who I tend to work well with.</strong> People carrying something from the past that still sets the terms of the present. People who&rsquo;ve done talk therapy and found it helpful up to a point. People navigating substance use alongside trauma, which is a pairing I see often and treat as one picture rather than two separate problems.",
   "<strong>What I ask of you.</strong> Honesty about what&rsquo;s actually happening, including the parts you&rsquo;d rather leave out, and a willingness to try things between sessions. Not perfection &mdash; most weeks are partial, and that is still progress.",
   "I founded Golden Hour Wellness Colorado and work as both clinician and business manager. I also co-facilitate <a href=\"mamas-golden-hour.html\">Mama&rsquo;s Golden Hour</a>."],
  True,
  [("License", "LPC (Colorado)"), ("Experience", "11 years"),
   ("Focus", "Trauma, EMDR, substance use"), ("Sessions", "In person &amp; telehealth")])

profile("chrissie.html", "Chrissie Flynn-Weirich", "LAC &middot; Wellness Facilitator",
  "chrissie.jpg", 1086, 1357, [],
  "A Licensed Addiction Counselor and Wellness Facilitator with over 13 years supporting people living with substance use disorders.",
  ["Together we will identify your strengths and your passions. Side by side we will assess what&rsquo;s working, what&rsquo;s not, and set meaningful goals that align with your vision of your best self. Each session will envelop empathy and unconditional regard.",
   "I&rsquo;ll support and empower your narrative through mindfulness and compassion as we explore challenges and discover solutions for navigating major life changes with greater clarity and sense of purpose, reconnecting with yourself and others.",
   "<strong>How I work.</strong> I start from strengths rather than deficits, because most people arriving to talk about substance use have heard plenty already about what&rsquo;s wrong with them. What&rsquo;s usually missing is a clear-eyed look at what is still working, and how to build on it.",
   "<strong>On abstinence.</strong> I don&rsquo;t require it and I don&rsquo;t assume it. Some clients want to stop entirely, others want to cut back, and others want to understand a pattern before deciding anything. Your goal is yours to set, and I&rsquo;ll be honest with you about what I think it will take to get there.",
   "<strong>Sessions are telehealth.</strong> That suits a lot of people &mdash; no waiting room, no commute, and it&rsquo;s easier to keep going on the weeks when leaving the house is the hard part. You&rsquo;ll need a private space, and to be physically in Colorado.",
   "I believe in the healing powers of self-reflection, curiosity, self-compassion and connection. Outside of sessions I enjoy baking, reading, music and dance, and my own wellness comes from meditation, yoga and poetry."],
  True,
  [("License", "LAC (Colorado)"), ("Experience", "13+ years"),
   ("Focus", "Substance use, anxiety"), ("Sessions", "Telehealth")])

profile("ashley.html", "Ashley LeRossignol", "LPC &middot; Consultant &amp; group facilitator",
  "ashley.jpg", 1103, 1378, [],
  "Ashley co-facilitates Mama&rsquo;s Golden Hour alongside Shayla and consults on clinical practice. She does not take individual clients through Golden Hour Wellness.",
  ["Working from a solution-oriented framework, Ashley brings over 10 years of experience treating anxiety, depression, relationship challenges, and family and work stressors. She utilizes Cognitive Behavioral Therapy, highlighting the ways mood, thoughts and behaviors shape one another, and emphasizing self-compassion along the way.",
   "She received her master&rsquo;s degree in counseling psychology from the University of San Francisco. Outside of therapy you&rsquo;ll find her outdoors, traveling, cooking and exploring new restaurants, places, cultures and communities.",
   "<strong>In the group.</strong> Ashley co-facilitates <a href=\"mamas-golden-hour.html\">Mama&rsquo;s Golden Hour</a> with Shayla. Two facilitators means one can hold the shape of the session while the other follows what is actually happening in the room, which matters a great deal in a group where a lot goes unsaid at first.",
   "<strong>In consultation.</strong> She also meets with the team to think through clinical work. This is a normal part of good practice: it means the reasoning behind your care has been pressure-tested by someone other than the person sitting with you, and it happens without identifying details leaving the room.",
   "<strong>Scheduling note:</strong> individual sessions at Golden Hour Wellness are available with Shayla and Chrissie. Ashley&rsquo;s role here is the group and consultation."],
  False,
  [("License", "LPC"), ("Experience", "10+ years"),
   ("Role", "Group &amp; consulting"), ("Individual clients", "Not through this practice")])

print("wrote:", len(OUT), "pages")
for o in OUT: print("  ", o)
