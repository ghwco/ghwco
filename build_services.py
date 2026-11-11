#!/usr/bin/env python3
"""Service, FAQ and legal pages.  python3 build_services.py"""
import io, json

# Cohort details live in content/group.json so Tina can change the dates and
# price each term. Everything below reads from G rather than hard-coding.
G = json.load(io.open("content/group.json", encoding="utf-8"))
from build_pages import page, head_block, cta, SITE, titled, clean_url, BUSINESS_ID
import glob as _glob

OUT = []
def emit(slug, **kw):
    io.open(slug, "w", encoding="utf-8").write(page(slug, **kw)); OUT.append(slug)

# Journal posts that are actually live, so a "related reading" link can never
# point at a page the blog build has removed.
POSTS = {}
for _f in _glob.glob("content/blog/*.json"):
    _p = json.load(io.open(_f, encoding="utf-8"))
    if _p.get("published"):
        POSTS[_p["slug"]] = _p["title"]


def reading(slugs, intro="From the journal"):
    links = ["<li><a href=\"blog-%s.html\">%s</a></li>" % (s, POSTS[s])
             for s in slugs if s in POSTS]
    if not links:
        return ""
    return '<h2>%s</h2>\n    <ul>%s</ul>' % (intro, "".join(links))


def faq_ld(faqs):
    import re as _re, html as _h
    clean = lambda t: _h.unescape(_re.sub(r"<[^>]+>", "", t))
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":clean(q),
       "acceptedAnswer":{"@type":"Answer","text":clean(a)}}
      for q, a in faqs]}

# ─────────────────────────────────────────────── SERVICES HUB
emit("services.html",
  title=titled("Therapy Services in Colorado"),
  desc="Therapy in Colorado for trauma and EMDR, anxiety and depression, substance use and couples, plus a virtual mothers' group. In-network with Aetna, Cigna and UHC.",
  crumbs=[("Services", "services.html")],
  body=head_block("How we help", "Specialized care, without the clinical chill.",
    "Every clinician here brings a different lane of expertise. We&rsquo;ll help you find the right fit on your first call, even if that fit turns out to be somewhere else.") + f'''
<section class="section">
  <div class="wrap">
    <div class="cards">
      <a class="card" href="trauma-emdr.html"><h3>Trauma &amp; EMDR</h3><p>Eye Movement Desensitization and Reprocessing alongside other trauma-focused approaches.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="anxiety-depression.html"><h3>Anxiety &amp; Depression</h3><p>Solution-oriented, CBT-informed work, plus practical tools you can actually use.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="substance-use.html"><h3>Substance Use &amp; Recovery</h3><p>Licensed addiction counseling for substance use disorders, or feeling stuck and disconnected.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="couples-therapy.html"><h3>Couples &amp; Relationships</h3><p>Family stress, work stress, and the big pivots that change how you relate to each other.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="mamas-golden-hour.html"><h3>Mama&rsquo;s Golden Hour</h3><p>A six-week virtual therapy group for Colorado mothers. Next cohort begins {G["startDateShort"]}.</p><span class="more">Learn more &rarr;</span></a>
    </div>
    <div class="callout" style="margin-top:2.5rem; max-width:44rem">
      <p><strong>Individual therapy</strong> is the default format for everything above except the group. Sessions run 50 minutes, in person or by <a href="telehealth-therapy-colorado.html">telehealth anywhere in Colorado</a>.</p>
    </div>
  </div>
</section>

<section class="section" style="background:var(--sand)">
  <div class="wrap prose">
    <h2>Not sure which one you need?</h2>
    <p>Most people don&rsquo;t arrive with a category in mind, and you don&rsquo;t need one. The pages above are how we organize our training, not a menu you have to order from. In practice these overlap constantly. Trauma sits underneath a lot of anxiety, substance use often started as a way to manage something else, and both show up in relationships.</p>
    <p>The free consultation exists to sort this out. It takes about fifteen minutes, there&rsquo;s no cost and no obligation, and by the end you&rsquo;ll know whether this practice fits and which clinician makes sense. If we&rsquo;re not the right place, we&rsquo;ll tell you and point you somewhere better.</p>

    <h2>What a first session is like</h2>
    <p>The first appointment is mostly you talking and us listening, with some paperwork at the start. We&rsquo;ll ask what brings you in now, what you&rsquo;ve already tried, and what you want to be different. Nothing gets pushed open on day one.</p>
    <p>By the end you should have a rough sense of the plan and how long it might take. If something about the fit feels off after a session or two, say so. That conversation is normal and we&rsquo;d rather have it than have you quietly stop coming.</p>

    <h2>How we work</h2>
    <ul>
      <li><strong>Collaborative, not prescriptive.</strong> You set the pace and the goals. We bring training, structure, and an honest read on whether it&rsquo;s helping.</li>
      <li><strong>Specialized rather than general.</strong> Each clinician here has a defined lane. We&rsquo;d rather refer you out than practice at the edge of ours.</li>
      <li><strong>Across Colorado.</strong> Telehealth means you don&rsquo;t need to be in Denver, or to drive anywhere on a bad week.</li>
      <li><strong>Straight about cost.</strong> We&rsquo;re in-network with Aetna, United Healthcare and Cigna (<a href="insurance.html">what that means for your bill</a>), and you can have a written <a href="good-faith-estimate.html">Good Faith Estimate</a> before you start.</li>
    </ul>
  </div>
</section>''' + cta())

# ─────────────────────────────────────────────── SERVICE PAGES
def service(slug, name, title, desc, lede, paras, good_fit, practical, who,
            process=(), faqs=(), seo_title=None, related=()):
    """process:   paragraphs for 'What the work looks like'.
       faqs:      (question, answer) pairs, rendered as accordions AND emitted
                  as FAQPage schema, which is what earns the expandable results
                  in Google and gives summarizers clean question/answer pairs.
       seo_title: the <title>, when it should differ from the on-page H1.
       related:   journal post slugs to link under "From the journal"."""
    ld = [{"@context":"https://schema.org","@type":"MedicalTherapy","name":name,
           "url":clean_url(slug),
           "provider":{"@type":"MedicalBusiness","@id":BUSINESS_ID,
                       "name":"Golden Hour Wellness Colorado, LLC",
                       "telephone":"+1-303-736-9822",
                       "areaServed":{"@type":"State","name":"Colorado"}}}]
    if faqs:
        ld.append(faq_ld(faqs))
    fit = "".join(f"<li>{x}</li>" for x in good_fit)
    proc = ("<h2>What the work looks like</h2>" +
            "".join(f"<p>{p}</p>" for p in process)) if process else ""
    qa = ('<h2>Common questions</h2><div class="faq">' + "".join(
          f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>'
          for q, a in faqs) + "</div>") if faqs else ""
    body = head_block("Services", title, lede) + f'''
<section class="section">
  <div class="wrap prose">
    {"".join(f"<p>{p}</p>" for p in paras)}

    <h2>This may be a good fit if</h2>
    <ul>{fit}</ul>

    {proc}

    <h2>Practical details</h2>
    {practical}

    <div class="callout">
      <p><strong>Who you&rsquo;d see:</strong> {who}</p>
    </div>

    {qa}

    {reading(related)}
  </div>
</section>''' + cta()
    emit(slug, title=titled(seo_title or title), desc=desc, body=body,
         active="services.html",
         crumbs=[("Services", "services.html"), (title, slug)],
         extra_head="".join(
             '<script type="application/ld+json">%s</script>' % json.dumps(b) for b in ld))

STD = '''<table>
      <tr><th>Format</th><td>Individual, 50 minutes</td></tr>
      <tr><th>Where</th><td>In person or <a href="telehealth-therapy-colorado.html">telehealth</a>, anywhere in Colorado</td></tr>
      <tr><th>Insurance</th><td>In-network with Aetna, United Healthcare and Cigna. <a href="insurance.html">Rates and coverage</a></td></tr>
      <tr><th>First step</th><td>A free 15-minute consultation. <a href="index.html#book">Book it</a> or <a href="contact.html">send a message</a></td></tr>
    </table>'''

service("trauma-emdr.html", "EMDR Therapy", "Trauma &amp; EMDR Therapy",
  "EMDR and trauma therapy in Colorado with Shayla Martinez-O'Brien, LPC. In person or by telehealth, in-network with Aetna, Cigna and UHC. Free 15-minute consult.",
  "Eye Movement Desensitization and Reprocessing alongside other trauma-focused approaches, in person or via telehealth anywhere in Colorado.",
  ["Trauma doesn&rsquo;t only live in memory. It shows up in how your body reacts, how you sleep, what you avoid, and how quickly you move from calm to overwhelmed. EMDR works with that directly rather than asking you to talk your way through it.",
   "The goal isn&rsquo;t to erase what happened. It&rsquo;s to change your relationship to it, so the memory stops setting the terms of your present. Most people find they can hold more, react less, and recognize themselves again.",
   "Shayla uses EMDR among other trauma-focused approaches, chosen to fit what you bring rather than applied from a template. You&rsquo;ll never be pushed to revisit something before you&rsquo;re ready."],
  ["Something from your past still shapes how you react today",
   "You feel activated or shut down without always knowing why",
   "Talk therapy has helped, but only to a point",
   "You&rsquo;re carrying a single event, or years of accumulated stress",
   "You want structure rather than open-ended conversation"],
  STD, 'Shayla Martinez-O&rsquo;Brien, LPC. <a href="shayla.html">Read her profile</a>.',
  process=[
   "The first session or two is history and groundwork rather than processing. We map what you&rsquo;re carrying, what sets it off, and what already helps. Nothing gets opened before there&rsquo;s something steady to come back to.",
   "Then we build resourcing skills: practical ways to bring your body back down when it spikes. That part is not filler. It&rsquo;s what makes the rest of the work safe, and plenty of people notice things easing before any memory is touched.",
   "Processing itself is more ordinary than people expect. You hold a piece of the memory in mind while following a repeating left-right cue, usually eye movements, taps or tones. You aren&rsquo;t asked to narrate it. Sets are short, we pause often, and you can stop at any point.",
   "Over sessions the memory tends to lose its charge. It doesn&rsquo;t disappear and it isn&rsquo;t rewritten. It stops arriving as if it&rsquo;s happening now. We close every session deliberately, so you leave settled rather than opened up.",
  ],
  faqs=[
   ("Do I have to describe what happened in detail?",
    "No. EMDR is one of the few trauma therapies that doesn&rsquo;t require a full account. You need enough of an image or felt sense to hold in mind. Many people process things they&rsquo;ve never said out loud."),
   ("How many sessions does EMDR take?",
    "A single recent incident can settle in a handful of sessions. Trauma that runs through years, or that started early, usually takes longer. We&rsquo;ll give you an honest read after the first few sessions rather than a number on day one."),
   ("Is EMDR evidence-based?",
    "Yes. It&rsquo;s recommended for post-traumatic stress by the World Health Organization and the American Psychological Association, among others, and has been studied for more than thirty years."),
   ("Does EMDR work over telehealth?",
    "It does. The bilateral cue is delivered on screen or with self-tapping. The main requirement is a private space where you won&rsquo;t be interrupted."),
   ("What if I get overwhelmed during a session?",
    "That&rsquo;s what the resourcing work is for, and it&rsquo;s why sets are short. You can stop at any moment. Sessions are always closed down properly before you leave, never mid-process."),
  ],
  seo_title="EMDR &amp; Trauma Therapy in Colorado",
  related=["what-emdr-feels-like"])

service("anxiety-depression.html", "Cognitive Behavioral Therapy", "Anxiety &amp; Depression",
  "Therapy for anxiety and depression in Colorado. Practical, CBT-informed sessions in person or by telehealth, in-network with Aetna, Cigna and United Healthcare.",
  "Solution-oriented, CBT-informed work on how mood, thoughts and behavior shape one another, plus tools you can actually use.",
  ["Anxiety and depression are good at convincing you that this is simply how you are. They aren&rsquo;t, and the pattern is more changeable than it feels from inside it.",
   "The work looks at how mood, thought and behavior feed one another, then interrupts that loop somewhere practical. Often the first useful change is small and unglamorous, like what happens in the first hour of your day.",
   "You&rsquo;ll leave sessions with something to try, not just something to think about. And we&rsquo;ll keep an honest eye on whether it&rsquo;s working."],
  ["Worry runs constantly in the background",
   "You&rsquo;ve lost interest in things that used to matter",
   "Sleep, appetite or focus have shifted",
   "You&rsquo;re functioning, but it&rsquo;s costing more than it should",
   "You want practical tools alongside understanding"],
  STD, 'Shayla Martinez-O&rsquo;Brien or Chrissie Flynn-Weirich. <a href="team.html">Meet the team</a>.',
  process=[
   "We start by getting specific. &ldquo;Anxious&rdquo; and &ldquo;low&rdquo; cover an enormous range, and the useful detail is in when it shows up, what it costs you, and what you&rsquo;ve already tried.",
   "From there the work is a loop: notice the pattern, test a change, look honestly at what happened. Sometimes the change is a thought you learn to catch. Often it&rsquo;s behavioral and unglamorous: sleep, mornings, one thing you&rsquo;ve been avoiding.",
   "Depression usually needs the behavior to move first, because waiting to feel motivated is a trap. Anxiety usually needs the avoidance to shrink gradually, at a pace you set, so your nervous system gets evidence rather than reassurance.",
   "We&rsquo;ll check in openly on whether it&rsquo;s working. If it isn&rsquo;t, we change the approach or talk about what else might help, including a medication conversation with your doctor if that seems worth exploring.",
  ],
  faqs=[
   ("Do I need medication as well as therapy?",
    "Not necessarily, and that&rsquo;s not our call to make. We&rsquo;re not prescribers. What we can do is help you think it through and talk with your doctor or a psychiatrist. Plenty of people do well with therapy alone; some do better with both."),
   ("Is my anxiety bad enough for therapy?",
    "There&rsquo;s no threshold you have to clear. If worry is taking up room you&rsquo;d rather use elsewhere, that&rsquo;s reason enough. Coming in earlier generally means less to undo."),
   ("What does CBT-informed mean?",
    "It means we use cognitive behavioral tools (examining thoughts, changing behavior, testing beliefs against reality) without running a rigid protocol. The structure serves you, not the other way around."),
   ("How soon will I notice a difference?",
    "Many people feel some relief within the first few sessions, often just from having a plan. Durable change in mood usually takes longer, in the range of eight to twelve sessions for a focused piece of work."),
   ("Can I do this by telehealth?",
    "Yes, and this kind of work translates well to video. Between-session practice happens in your own life either way."),
  ],
  seo_title="Anxiety &amp; Depression Therapy in Colorado",
  related=["rest-you-have-to-earn", "baby-blues-vs-postpartum-depression"])

service("substance-use.html", "Addiction Counseling", "Substance Use &amp; Recovery",
  "Addiction counseling in Colorado with a Licensed Addiction Counselor. No shaming, no abstinence required to start. In person or by telehealth across the state.",
  "Licensed addiction counseling for people living with substance use disorders, or anyone feeling stuck and disconnected from themselves.",
  ["You don&rsquo;t need a label or a rock-bottom story to start here. Plenty of people arrive simply knowing something has taken up more room than they want it to.",
   "The work is strengths-based. We&rsquo;ll identify what&rsquo;s already working, name honestly what isn&rsquo;t, and set goals that match your own vision of your best self rather than someone else&rsquo;s.",
   "Chrissie holds a Colorado addiction counseling license, so substance use is treated here as core clinical work rather than something we refer out. Shayla brings the trauma side, which so often sits underneath it."],
  ["Substance use has become larger than you intended",
   "You feel stuck, or disconnected from yourself and others",
   "You&rsquo;ve tried to change on your own and it hasn&rsquo;t held",
   "You want support that isn&rsquo;t shaming or scripted",
   "You&rsquo;re working on recovery alongside trauma or anxiety"],
  STD, 'Chrissie Flynn-Weirich, LAC, or Shayla Martinez-O&rsquo;Brien, LPC.',
  process=[
   "Nothing here requires you to call yourself an addict or commit to abstinence at the door. We start where you are and get clear on what you actually want, which is often more specific than &ldquo;stop&rdquo;.",
   "Early sessions look at the shape of it: when use happens, what it does for you, and what it costs. That last part gets named plainly, but not with shame. Shame reliably makes use worse, not better.",
   "From there we work on the gap between the two, building alternatives that do some of the same job, planning for the situations you already know are hard, and treating a return to use as information rather than failure.",
   "Trauma, anxiety and grief sit underneath substance use often enough that we look for them. If that&rsquo;s part of your picture, it can be treated in the same place rather than handed off elsewhere.",
  ],
  faqs=[
   ("Do I have to want to quit completely?",
    "No. Some people come in aiming to stop, others to cut back or to understand a pattern before deciding. All of those are workable starting points. The goal is yours to set."),
   ("Will you tell me to go to AA?",
    "Only if you want that. Twelve-step programs help a great many people and we&rsquo;ll support you in one gladly, but they aren&rsquo;t the only route and we won&rsquo;t make them a condition."),
   ("What if I relapse?",
    "You keep your appointment. A return to use is common in recovery and it tells us something about what wasn&rsquo;t yet in place. It isn&rsquo;t grounds for being discharged or lectured."),
   ("Is this confidential?",
    "Yes, with the same legal limits as any therapy. Federal rules around substance use records are in fact stricter than general health privacy. We&rsquo;ll go through exactly what that means at intake."),
   ("Do you provide detox or medication?",
    "No. We&rsquo;re outpatient counselors, not a medical facility. If you need medically supervised withdrawal or medication for opioid or alcohol use, we&rsquo;ll help you find it and can work alongside that treatment."),
  ],
  seo_title="Addiction Counseling in Colorado",
  related=["what-emdr-feels-like"])

service("couples-therapy.html", "Couples Therapy", "Couples &amp; Relationships",
  "Couples therapy in Colorado for the argument that keeps coming back, a new baby, a move or a job change. In person or by telehealth, starting with a free call.",
  "Family stress, work stress, and the big pivots. Getting through change with more clarity and a stronger sense of purpose.",
  ["Most couples don&rsquo;t arrive because of one argument. They arrive because a pattern has set in, and the same conversation keeps happening in slightly different clothes.",
   "Sessions focus on what each of you is actually asking for underneath the disagreement, and on building a way to say it that the other person can hear.",
   "This is also useful during transitions that aren&rsquo;t anyone&rsquo;s fault. A new baby, a career change, a move, an illness, or a shift in what you each need."],
  ["The same argument keeps recurring",
   "A transition has changed how you relate to each other",
   "One or both of you has stopped raising things",
   "You want to communicate differently, not just less often",
   "You&rsquo;re deciding whether to continue and want support either way"],
  STD, 'Shayla Martinez-O&rsquo;Brien or Chrissie Flynn-Weirich.',
  process=[
   "The first session is mostly listening, and we hear from both of you. Couples usually arrive with two accounts that don&rsquo;t match. That&rsquo;s normal, and the mismatch itself is useful information.",
   "Then we slow the recurring argument down. Most couples aren&rsquo;t fighting about the thing they&rsquo;re fighting about. Underneath it is a request that hasn&rsquo;t landed, or a hurt that never got acknowledged.",
   "A lot of sessions involve practicing the conversation in the room rather than reporting on it afterward. It feels awkward at first. It&rsquo;s also where the change happens, because you get to try a different move while someone can slow it down.",
   "We stay even-handed. This isn&rsquo;t a forum for deciding who was right, and neither of you will be recruited against the other.",
  ],
  faqs=[
   ("What if only one of us wants to come?",
    "Start anyway. One person can shift a pattern, and individual work on how you show up in the relationship is legitimate on its own terms. Sometimes the other partner joins later."),
   ("Do you take sides?",
    "No. Both of you will hear things that are hard, and both of you will be asked to change something. If either of you starts to feel that we&rsquo;re building a case, say so and we&rsquo;ll address it directly."),
   ("Is couples therapy covered by insurance?",
    "Often not, or only under certain conditions, because insurers generally require an individual diagnosis. We&rsquo;ll check your plan and give you a written estimate before you start."),
   ("What if we&rsquo;re deciding whether to separate?",
    "That&rsquo;s a legitimate reason to come. The work then is to make the decision clearly and kindly rather than by attrition, and to help you do it well if separating is what you choose."),
   ("Can we do couples sessions by telehealth?",
    "Yes. Sit in the same room and use one screen if you can. If you&rsquo;re in separate places, that works too, though the in-room dynamic is part of what we&rsquo;re working with."),
  ],
  seo_title="Couples Therapy in Colorado",
  related=["baby-blues-vs-postpartum-depression"])

# ─────────────────────────────────────────────── MAMA'S GOLDEN HOUR
group_ld = {"@context":"https://schema.org","@type":"Event",
  "name":"Mama's Golden Hour Therapy Group","eventAttendanceMode":"https://schema.org/OnlineEventAttendanceMode",
  "eventStatus":"https://schema.org/EventScheduled","startDate":G["startDateISO"],
  "location":{"@type":"VirtualLocation","url":clean_url("mamas-golden-hour.html")},
  "organizer":{"@type":"MedicalBusiness","@id":BUSINESS_ID,"name":"Golden Hour Wellness Colorado, LLC","url":SITE + "/"},
  "description":"A six-week virtual therapy group for Colorado mothers covering fertility, pregnancy and birth, postpartum and all stages of parenting.",
  "offers":{"@type":"Offer","price":G["priceFull"],"priceCurrency":"USD","availability":"https://schema.org/InStock","url":clean_url("mamas-golden-hour.html")}}

emit("mamas-golden-hour.html",
  title="Mama&rsquo;s Golden Hour | Therapy Group for Colorado Moms",
  desc=f"A six-week virtual therapy group for Colorado mothers, covering fertility, pregnancy, postpartum and parenting. Next cohort begins {G['startDateShort']}.",
  active="services.html",
  crumbs=[("Services", "services.html"), ("Mama's Golden Hour", "mamas-golden-hour.html")],
  img="assets/img/mamas-group.jpg",
  extra_head=f'<script type="application/ld+json">{json.dumps(group_ld)}</script>',
  body=head_block("Group therapy", "Mama&rsquo;s Golden Hour",
    "A six-week virtual therapy group for mothers across Colorado, co-facilitated by Shayla and Ashley.") + f'''
<section class="section">
  <div class="wrap prose">
    <p>Motherhood asks a great deal and rarely leaves room to talk about it honestly. This group is that room: a small, virtual space with other Colorado mothers and two licensed clinicians.</p>

    <p>We cover the whole arc rather than one stage of it. Fertility, pregnancy and birth, postpartum, and every stage of parenting after that. Wherever you are in it, you&rsquo;re welcome.</p>

    <h2>Next cohort</h2>
    <table>
      <tr><th>Starts</th><td>{G["startDateLong"]}</td></tr>
      <tr><th>Time</th><td>{G["time"]}</td></tr>
      <tr><th>Runs for</th><td>{G["runsFor"]}</td></tr>
      <tr><th>Where</th><td>{G["where"]}</td></tr>
      <tr><th>Cost</th><td>{G["costLine"]}</td></tr>
      <tr><th>Open to</th><td>{G["openTo"]}</td></tr>
    </table>

    <div class="callout warn">
      <p><strong>Insurance is not accepted for the group.</strong> Group sessions are self-pay only. Insurance does apply to individual therapy, where we&rsquo;re in-network with Aetna, United Healthcare and Cigna.</p>
    </div>

    <h2>What it covers</h2>
    <ul>
      <li>Fertility, and the particular loneliness of that season</li>
      <li>Pregnancy and birth, including births that didn&rsquo;t go to plan</li>
      <li>Postpartum, and the gap between how you expected to feel and how you do</li>
      <li>All stages of parenting, from newborn nights to older children</li>
      <li>Identity, resentment, guilt, and the things that feel unsayable elsewhere</li>
    </ul>

    <h2>Who facilitates</h2>
    <p>The group is co-facilitated by <a href="shayla.html">Shayla Martinez-O&rsquo;Brien</a>, LPC, and <a href="ashley.html">Ashley LeRossignol</a>, LPC.</p>

    <figure>
      <img src="assets/img/mamas-group.jpg" width="1600" height="1066" loading="lazy"
           alt="Ashley LeRossignol and Shayla Martinez-O&rsquo;Brien, co-facilitators of Mama&rsquo;s Golden Hour, standing together outdoors beneath a cottonwood.">
      <figcaption>Ashley LeRossignol and Shayla Martinez-O&rsquo;Brien, co-facilitators.</figcaption>
    </figure>

    <h2>What a session looks like</h2>
    <p>Sixty minutes, the same small group of women each week, the same two facilitators. There&rsquo;s a loose theme most weeks, but it gives way if something more pressing is in the room. This is a therapy group, not a class. Nobody presents, and there&rsquo;s no homework.</p>
    <p>You are never required to speak. Plenty of people spend the first week listening and find that useful on its own. What is asked of everyone is confidentiality: what&rsquo;s said in the group stays in the group.</p>
    <p>Babies in arms are welcome on screen, and you&rsquo;re welcome to breastfeed during the session to whatever degree you&rsquo;re comfortable: camera on, camera off, however suits you. Cameras on where you can manage it, because it makes a real difference to how connected the group feels, but we&rsquo;d rather have you there with the camera off than not there at all.</p>

    <h2>Why a group and not individual therapy</h2>
    <p>A lot of what makes new motherhood hard is the conviction that everyone else is finding it easier. That belief is remarkably resistant to a therapist telling you otherwise, and it tends to dissolve the first time another mother says the thing out loud.</p>
    <p>Groups also normalize the parts that feel unspeakable: ambivalence, resentment, grief for the life before, the specific loneliness of being with a baby all day. Hearing it from someone else does something reassurance can&rsquo;t.</p>
    <p>Some people do the group alongside individual therapy, here or elsewhere. Others do it on its own. Either is fine, and it&rsquo;s worth saying that the group is not a substitute for individual treatment if you&rsquo;re struggling badly.</p>

    {reading(["baby-blues-vs-postpartum-depression"], "Before the first session")}

    {"" if G["enrolling"] else """<div class="callout warn"><p><strong>This cohort is full.</strong> Get in touch and we&rsquo;ll tell you as soon as the next one opens, usually a few weeks ahead of the start date.</p></div>"""}

    <h2>Joining</h2>
    <p>Every member has a short consultation first, so we can make sure the group is a good fit before you commit. Call or text <a href="tel:+13037369822">(303)&nbsp;736-9822</a>, or <a href="contact.html">send a message</a>.</p>
    <p>Space is limited by design. A group this size stops working past about {G["capacity"]} people. If this cohort fills or the timing doesn&rsquo;t suit, tell us and we&rsquo;ll let you know when the next one opens.</p>

    <div class="callout warn">
      <p><strong>If you&rsquo;re struggling badly right now,</strong> please don&rsquo;t wait for the group to start. Call or text <strong>988</strong>, or reach the Postpartum Support International helpline at <strong>1-800-944-4773</strong>. We can also talk about individual therapy sooner.</p>
    </div>
  </div>
</section>

<section class="section" style="background:var(--sand); text-align:center">
  <div class="wrap">
    <h2>Join the {G["startDateLong"].split(",")[1].split()[0]} cohort</h2>
    <p class="lede" style="margin-inline:auto">Six weeks, starting {G["startDateLong"]} at 6pm MT. Consultation first, always.</p>
    <div style="display:flex; gap:.7rem; justify-content:center; flex-wrap:wrap; margin-top:1.75rem">
      <a class="btn btn-primary" href="index.html#book">Book a consultation</a>
      <a class="btn btn-outline" href="tel:+13037369822">Call or text (303) 736-9822</a>
    </div>
  </div>
</section>''')

# ─────────────────────────────────────────────── TELEHEALTH
# Written only from what the rest of the site already says about telehealth:
# the FAQ, the service pages and Chrissie's profile. Nothing new is claimed.
TELE_FAQS = [
  ("Can I mix telehealth and in-person sessions?",
   "Yes. Many clients switch between the two depending on the week. The session length and format stay the same either way."),
  ("Do I have to live in Colorado?",
   "You need to be physically in Colorado during each session, because our clinicians are licensed here and therapy licensure is state-based. If you&rsquo;ll be out of state on a session day, tell us ahead of time."),
  ("Does EMDR work over video?",
   "It does. The left-right cue is delivered on screen or with self-tapping. What matters most is a private space where you won&rsquo;t be interrupted."),
  ("Can couples do sessions by telehealth?",
   "Yes. Sit in the same room and share one screen if you can. Joining from separate places also works."),
  ("Is Mama&rsquo;s Golden Hour online?",
   "Only online. The group meets by Zoom, and mothers anywhere in Colorado can join."),
]

emit("telehealth-therapy-colorado.html",
  title=titled("Telehealth Therapy in Colorado"),
  desc="Telehealth therapy anywhere in Colorado: EMDR, anxiety and depression, addiction counseling and couples sessions by video, plus a mothers' group on Zoom.",
  active="services.html",
  crumbs=[("Services", "services.html"), ("Telehealth Therapy in Colorado", "telehealth-therapy-colorado.html")],
  extra_head=f'<script type="application/ld+json">{json.dumps(faq_ld(TELE_FAQS))}</script>',
  body=head_block("Telehealth", "Therapy without the drive.",
    "Individual sessions run by video for anyone physically in Colorado, at the same length and in the same format as sessions in the room.") + f'''
<section class="section">
  <div class="wrap prose">
    <p>Some weeks the hardest part of therapy is getting out the door. Telehealth takes that part away. No waiting room, no commute, no drive across town and back for a 50-minute session.</p>
    <p>It also means where you live in the state stops mattering. Grand Junction, Pueblo, Durango or a mountain town with one stoplight: if you&rsquo;re in Colorado when the session starts, you can see the same clinicians as everyone else.</p>

    <h2>What you&rsquo;ll need</h2>
    <ul>
      <li>A private space where you won&rsquo;t be overheard or interrupted for the whole session.</li>
      <li>To be physically in Colorado during the session. That&rsquo;s a licensing rule, and it follows where you are, not your home address.</li>
      <li>A phone, tablet or computer with a camera and a steady connection.</li>
    </ul>

    <h2>What works by video</h2>
    <table>
      <tr><th><a href="trauma-emdr.html">Trauma &amp; EMDR</a></th><td>The left-right cue runs on screen, or you tap it yourself.</td></tr>
      <tr><th><a href="anxiety-depression.html">Anxiety &amp; depression</a></th><td>Translates well. The practice between sessions happens in your own life anyway.</td></tr>
      <tr><th><a href="substance-use.html">Substance use</a></th><td>Chrissie&rsquo;s sessions are all telehealth.</td></tr>
      <tr><th><a href="couples-therapy.html">Couples</a></th><td>Works best from one room, on one screen.</td></tr>
      <tr><th><a href="mamas-golden-hour.html">Mama&rsquo;s Golden Hour</a></th><td>Virtual only, by Zoom.</td></tr>
    </table>

    <h2>Insurance and cost</h2>
    <p>We&rsquo;re in-network with Aetna, United Healthcare and Cigna for individual therapy. <a href="insurance.html">Insurance and rates</a> covers what you&rsquo;d pay, how to check out-of-network benefits, and the self-pay route.</p>

    <div class="callout">
      <p><strong>Prefer to come in?</strong> In-person sessions are available too, and you can switch between the two as your weeks change. Mention it on the free consultation.</p>
    </div>

    <h2>Common questions</h2>
    <div class="faq">{"".join(f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in TELE_FAQS)}</div>

    {reading(["what-emdr-feels-like"])}
  </div>
</section>''' + cta())

print("wrote:", len(OUT)); [print("  ", o) for o in OUT]
