#!/usr/bin/env python3
"""Renders Issues No. 02-11 - both editions, the two contents pages, and index.html.

    python3 src/build_site.py

Content lives in src/content.py. Styling lives in assets/*.css. Widget behaviour
lives in assets/widgets.js. This file only decides what goes where, so adding an
issue means editing content.py and re-running - not writing HTML.

Issue No. 01 is hand-built and is deliberately not touched by this script.
"""
import json, os, re, sys, html as _html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import ISSUES

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

P_FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap">\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800;900&display=swap">\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap">')
K_FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap">\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shantell+Sans:ital,wght@0,500;0,600;0,700;0,800;1,600&display=swap">')

# Cookieless, aggregate-only analytics. Empty means nothing is emitted at all -
# no dead script tag, and the privacy wording stays literally true. To turn it
# on, paste the Cloudflare Web Analytics token here and rebuild.
ANALYTICS_TOKEN = "0025ab66f6d745d8b51a958d7c208e7f"

# Institutional enquiries need somewhere to land. Leave empty and the contact
# block is omitted rather than shipping a dead mailto.
CONTACT_EMAIL = ""

def analytics():
    if not ANALYTICS_TOKEN:
        return ""
    return ('\n<!-- Cloudflare Web Analytics -->'
            '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
            'data-cf-beacon=\'{"token": "%s"}\'></script>'
            '<!-- End Cloudflare Web Analytics -->' % ANALYTICS_TOKEN)

PRIVACY = ("<strong>Nothing you tick or type is stored or sent.</strong> Every worksheet is "
 "local to your browser and vanishes when you close the tab.")
PRIVACY_WITH_ANALYTICS = ("<strong>Nothing you tick or type is stored or sent.</strong> Every "
 "worksheet is local to your browser and vanishes when you close the tab. We do count page "
 "visits in aggregate, with no cookies and nothing that identifies you.")

P_COLO = (
 "<strong>The Big Ask.</strong> Written and designed by Claude, an AI made by Anthropic. "
 "There is no human newsroom here and no byline to look up.<br><br>"
 "<strong>Not professional advice.</strong> These are conversation structures, not rules. Nothing here is "
 "medical, legal, psychological or safeguarding guidance. Age bands are rough and your child is not a band. "
 "Anything touching a child's safety belongs with people who know your family.<br><br>"
 + (PRIVACY_WITH_ANALYTICS if ANALYTICS_TOKEN else PRIVACY)
 + "<br><br>"
 "The method, in one line: decide it out loud, decide it with them in the room, and if the answer is "
 "not yet, bring a reason and a date.")

K_COLO = (
 "<strong>Made by a computer.</strong> All of this was written by an AI called Claude. There's no person "
 "behind it. You should know that when someone gives you advice.<br><br>"
 "The advice is real though - it's the same as the grown-up version, with fewer words.<br><br>"
 "<strong>Nothing you tap gets sent anywhere.</strong> Streak trackers are saved on your own device and "
 "nobody else can see them."
 + ("<br><br>We do count page visits in aggregate - no cookies, nothing that says it was you."
    if ANALYTICS_TOKEN else ""))





def ascii_only(s):
    return "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in s)

SITE = "https://skyspeak.github.io/magazine/"



def social(title, desc, page_path, image):
    """Open Graph + Twitter card. Without these a shared link is bare text, and
    shared links are how this kind of thing actually travels."""
    url = SITE + page_path
    return f'''<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The Big Ask">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}og/{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}og/{image}">'''


def page(title, desc, css, fonts, body, extra_js="", up="../", page_path="", image="home.png"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{social(title, desc, page_path, image)}
{fonts}
<link rel="stylesheet" href="{css}">
</head>
<body>
{body}
<script src="{up}assets/widgets.js" defer></script>{extra_js}{analytics()}
</body>
</html>"""

def widget(w, up=".."):
    wid = "w-" + w["kind"] + "-" + str(abs(hash(w["title"])) % 99999)
    return (f'<div class="sheet" style="margin-top:1rem">'
            f'<div class="sheet-head"><span>{w["title"]}</span><span>Nothing here is saved or sent</span></div>'
            f'<p class="w-lead">{w["note"]}</p>'
            f'<div id="{wid}" data-widget="{w["kind"]}" data-w=\'{json.dumps(w["data"])}\'></div>'
            f'</div>')

def kid_widget(w):
    wid = "k-" + w["kind"] + "-" + str(abs(hash(w["title"])) % 99999)
    return (f'<div class="card yellow"><h3 class="mid" style="margin-top:0">{w["title"]}</h3>'
            f'<p>{w["note"]}</p>'
            f'<div id="{wid}" data-widget="{w["kind"]}" data-w=\'{json.dumps(w["data"])}\'></div></div>')


def parent_page(i, prev, nxt):
    ready_w = dict(kind="checklist", title="Ready when", note="Tick honestly. This is not a quiz you are meant to pass.",
        data=dict(empty="Tick what is true today.",
            items=[dict(t=r["t"], why=r.get("why","")) for r in i["ready"]],
            verdicts=[dict(min=len(i["ready"]), say="That is a yes. Say it warmly and completely, then write down who does what."),
                      dict(min=max(2,len(i["ready"])-1), say="Close. Name the missing one out loud and put a date on it. That list <em>is</em> your &ldquo;not yet&rdquo;."),
                      dict(min=1, say="This is a &ldquo;not yet&rdquo;, which is a real answer rather than a soft no. Give the reason, the condition and the date.")]))
    scripts = "".join(
        f'<div class="script"><span class="role">{s["role"]}</span><p><span class="say">{s["say"]}</span></p>'
        f'<p style="font-size:.9rem;color:var(--ink-2)">{s["why"]}</p></div>' for s in i["scripts"])
    depth = "".join(f'<h3 class="sub">{h}</h3>' + "".join(f"<p>{p}</p>" for p in ps) for h, ps in i["depth"])
    facts = "".join(f"<p>{f}</p>" for f in i["facts"])
    bullets = "".join(f"<li>{b}</li>" for b in i["deciding"]["bullets"])
    body = f"""<div class="top"><div class="wrap">
  <span><a href="../index.html">The Big Ask</a> &middot; <a href="no-02-11-ten-more-big-asks.html">Contents</a></span>
  <span>Issue No. {i['no']} &middot; For the parent</span>
</div></div>

<header class="hd"><div class="wrap">
  <p class="eyebrow">Issue No. {i['no']} &middot; {i['band']}</p>
  <h1 class="ask display">{i['ask']}</h1>
  <p class="thesis">{i['thesis']}</p>
</div></header>

<main class="wrap">
  <section class="blk">
    <h2 class="sec">What you are actually deciding</h2>
    <p class="sec-sub">Start here, because the wrong question wastes the conversation</p>
    <div class="grid">
      <div class="box"><h4>The real question</h4><p>{i['deciding']['q']}</p><ul class="ck">{bullets}</ul></div>
      <div class="box"><h4>Facts worth knowing</h4>{facts}</div>
    </div>
    {widget(i['widget'])}
  </section>

  <section class="blk">
    <h2 class="sec">Say this, not that</h2>
    <p class="sec-sub">Adapt the words, keep the structure</p>
    <div class="col">{scripts}
      <div class="script bad"><span class="role">Not this</span><p><span class="say">{i['dont']['say']}</span></p>
        <p style="font-size:.9rem;color:var(--ink-2)">{i['dont']['why']}</p></div>
    </div>
    <p class="pull display">{i['rule']['text']}</p>
    <div class="col"><p>{i['rule']['why']}</p></div>
  </section>

  <section class="blk">
    <h2 class="sec">The longer version</h2>
    <p class="sec-sub">If you have ten minutes rather than two</p>
    <div class="col">{depth}</div>
  </section>

  <section class="blk">
    <h2 class="sec">How you will know</h2>
    <p class="sec-sub">And what to do if the answer is not yet</p>
    {widget(ready_w)}
    <div class="box hard" style="margin-top:1.1rem"><h4>If it is not yet</h4><p>{i['notyet']}</p></div>
    <div class="crossref"><span class="k">There is an edition for them</span>
      <p style="margin:0"><a href="../kids/no-{i['no']}-{i['slug']}.html">The kid&rsquo;s version of this issue</a>
      is written to your child rather than about them: what you are actually worried about, what to say, and the one job that does the work. Hand it over and leave the room.</p></div>
  </section>

  <nav class="pager">
    <span>{f'<a href="no-{prev["no"]}-{prev["slug"]}.html">&larr; No. {prev["no"]} &middot; {prev["title"]}</a>' if prev else '<a href="no-02-11-ten-more-big-asks.html">&larr; Contents</a>'}</span>
    <span>{f'<a href="no-{nxt["no"]}-{nxt["slug"]}.html">No. {nxt["no"]} &middot; {nxt["title"]} &rarr;</a>' if nxt else '<a href="no-02-11-ten-more-big-asks.html">Contents &rarr;</a>'}</span>
  </nav>
</main>

<footer><div class="wrap"><p class="colo">{P_COLO}</p></div></footer>"""
    return page(f"No. {i['no']} - {i['title']}",
                _html.escape(real_question(i)),
                "../assets/parents.css", P_FONTS, body,
                page_path=f"parents/no-{i['no']}-{i['slug']}.html",
                image=f"no-{i['no']}-parents.png")


def kid_page(i, prev, nxt):
    k = i["kid"]
    why = "".join(f"<p>{p}</p>" for p in k["why"])
    steps = "".join(f"<li>{s}</li>" for s in k["steps"])
    body = f"""<div class="top"><div class="wrap">
  <span><a href="no-02-11-ten-things-to-ask-for.html">All ten</a></span>
  <span>No. {i['no']}</span>
</div></div>

<header><div class="wrap">
  <span class="kick">The Big Ask &middot; Kid Cut &middot; No. {i['no']}</span>
  <h1 class="marker">{k.get('h1', i['ask'])}</h1>
  <p class="sub">What they&rsquo;re actually scared of, what to say, and the one job that does the work.</p>
</div></header>

<main><div class="wrap">
  <div class="card {i['colour']}">
    <h2 class="big marker">The short version</h2>
    <div class="row"><span class="k">They&rsquo;re scared of</span><span class="v">{k['scared']}</span></div>
    <div class="row"><span class="k">Say</span><span class="v bub">{k['say']}</span></div>
    <div class="row"><span class="k">Don&rsquo;t say</span><span class="v">{k['dont']}</span></div>
    <div class="row"><span class="k">Your job</span><span class="v"><b>{k['job']}</b></span></div>
    <div class="row"><span class="k">If they say not yet</span><span class="v">{k['notyet']}</span></div>
  </div>

  <h3 class="mid">Why that works</h3>
  {why}

  <h3 class="mid">What to actually do</h3>
  <ol class="steps">{steps}</ol>

  {kid_widget(k['widget'])}

  <div class="grown">
    <h3 class="marker">For the grown-up reading over a shoulder</h3>
    <p>This is the child&rsquo;s half of <a href="../parents/no-{i['no']}-{i['slug']}.html">Issue No. {i['no']}</a>.
    Nothing here contradicts yours. It tells them that asking repeatedly fails, that you are worried about something
    specific and findable, and that &ldquo;not yet&rdquo; is a real answer <em>if</em> it comes with a date.
    If you are going to say not yet, please bring the date.</p>
  </div>

  <nav class="pager">
    <span>{f'<a href="no-{prev["no"]}-{prev["slug"]}.html">&larr; {prev["title"]}</a>' if prev else '<a href="no-02-11-ten-things-to-ask-for.html">&larr; All ten</a>'}</span>
    <span>{f'<a href="no-{nxt["no"]}-{nxt["slug"]}.html">{nxt["title"]} &rarr;</a>' if nxt else '<a href="no-02-11-ten-things-to-ask-for.html">All ten &rarr;</a>'}</span>
  </nav>
</div></main>

<footer><div class="wrap"><p class="colo">{K_COLO}</p></div></footer>"""
    return page(i["title"], _html.escape(f"What they're scared of, what to say, and the one job that does the work."),
                "../assets/kids.css", K_FONTS, body,
                page_path=f"kids/no-{i['no']}-{i['slug']}.html",
                image=f"no-{i['no']}-kids.png")


def real_question(i):
    """The one-line summary for the contents pages.

    deciding.q is written as "Not <em>the wrong question</em>. It is: the real one?"
    Take the half after "It is:" - the half before it is the question the issue
    exists to talk you out of, and showing that as the summary inverts the point.
    """
    q = i["deciding"]["q"]
    q = q.split("It is:", 1)[1] if "It is:" in q else q
    q = re.sub(r"<[^>]+>", "", q).strip()
    return q[0].upper() + q[1:] if q else q


def parents_contents():
    rows = "".join(f"""
    <a class="toc-row" href="no-{i['no']}-{i['slug']}.html" data-lo="{i['ages'][0]}" data-hi="{i['ages'][1]}">
      <span class="n mono">No. {i['no']}</span>
      <span class="t"><b>{i['ask']}</b><em>{i['band']}</em></span>
      <span class="d">{real_question(i)}</span>
    </a>""" for i in ISSUES)
    body = f"""<div class="top"><div class="wrap">
  <span><a href="../index.html">The Big Ask</a> &middot; A field manual for the decisions you make together</span>
  <span>Issues 02&ndash;11</span>
</div></div>

<header class="hd"><div class="wrap">
  <h1 class="ask display">Ten more<br><em>big asks</em></h1>
  <p class="thesis">Issue No. 01 took one decision apart at full length. These are the ten that follow it &mdash; each its own issue, same shape every time, so you can find the thing you need the night before you need it.</p>
  <div class="filter">
    <label for="age">Whose house is this?</label>
    <input type="range" id="age" min="5" max="18" value="10">
    <span class="age display" id="agev">10</span>
    <span class="msg mono" id="agemsg"></span>
    <button type="button" id="showall">Show all ten</button>
  </div>
</div></header>

<main class="wrap">
  <div class="toc-list" id="toc">{rows}</div>
  <div class="crossref"><span class="k">The kid&rsquo;s edition</span>
    <p style="margin:0">Every one of these has a companion written to your child rather than about them &mdash;
    one card each, about sixty words. <a href="../kids/no-02-11-ten-things-to-ask-for.html">Ten things to ask for</a>.</p></div>
</main>

<footer><div class="wrap"><p class="colo">{P_COLO}</p></div></footer>"""
    js = """
<script>
(function(){"use strict";
 var $=function(i){return document.getElementById(i)},s=$("age"),o=$("agev"),m=$("agemsg"),all=false;
 var rows=[].slice.call(document.querySelectorAll(".toc-row"));
 function apply(){var v=+s.value;o.textContent=v;var live=0;
  rows.forEach(function(r){var on=all||(v>=+r.dataset.lo&&v<=+r.dataset.hi);
   r.classList.toggle("dim",!on); if(on)live++;});
  m.textContent=all?"Showing all ten."
   :live?live+(live===1?" issue is":" issues are")+" live at "+v+". The rest are dimmed, not gone."
        :"Nothing lands squarely at "+v+", but the nearest ones are worth reading early.";}
 s.addEventListener("input",function(){all=false;apply()});
 $("showall").addEventListener("click",function(){all=!all;
   $("showall").textContent=all?"Filter by age":"Show all ten";apply()});
 apply();})();
</script>"""
    return page("Ten More Big Asks", "Issues 02-11 of The Big Ask, one page each, filterable by your kid's age.",
                "../assets/parents.css", P_FONTS, body, js,
                page_path="parents/no-02-11-ten-more-big-asks.html", image="contents-parents.png")


def kids_contents():
    chips = "".join(f'<a class="chip {i["colour"]}" href="no-{i["no"]}-{i["slug"]}.html">{i["title"]}</a>' for i in ISSUES)
    cards = "".join(f"""
    <a class="mini {i['colour']}" href="no-{i['no']}-{i['slug']}.html">
      <span class="mn marker">{i['no']}</span>
      <span class="mt marker">{i['title']}</span>
      <span class="ms">{i['kid']['scared']}</span>
    </a>""" for i in ISSUES)
    body = f"""<div class="top"><div class="wrap">
  <span>The Big Ask &middot; Kid Cut</span><span>Nos. 02&ndash;11</span>
</div></div>

<header><div class="wrap">
  <span class="kick">The Big Ask &middot; Kid Cut &middot; Nos. 02&ndash;11</span>
  <h1 class="marker">Ten things<br>you&rsquo;re going<br>to <em>ask for</em></h1>
  <p class="sub">One page each. What they&rsquo;re actually scared of, what to say, and the one job that does the work.</p>
  <div class="rules">
    <div class="rule"><b>1</b><p>Asking again doesn&rsquo;t work. Proof does.</p></div>
    <div class="rule"><b>2</b><p>Find out what they&rsquo;re scared of. It&rsquo;s never the thing you think.</p></div>
    <div class="rule"><b>3</b><p>&ldquo;Not yet&rdquo; isn&rsquo;t &ldquo;no&rdquo; &mdash; but only if you get a date.</p></div>
  </div>
  <nav class="chips" aria-label="Jump to an ask">{chips}</nav>
</div></header>

<main><div class="wrap"><div class="minis">{cards}</div>
  <div class="grown">
    <h3 class="marker">Want the long one?</h3>
    <p><a href="no-01-the-case-for-a-dog.html">The case for a dog</a> takes a single ask apart properly, with a
    fourteen-morning tracker and a builder that makes the page you hand over.</p>
  </div>
</div></main>

<footer><div class="wrap"><p class="colo">{K_COLO}</p></div></footer>"""
    return page("Ten Things to Ask For", "The kid's edition of Issues 02-11 - one page per ask.",
                "../assets/kids.css", K_FONTS, body,
                page_path="kids/no-02-11-ten-things-to-ask-for.html", image="contents-kids.png")


def school_entry_pages():
    """Distinct entry paths for links handed to schools, at s/<no>.html.

    Cloudflare Web Analytics reports the path only - query strings and hashes
    are both stripped from the beacon payload (verified by intercepting it), and
    email clients drop the referrer. So a newsletter click is indistinguishable
    from someone typing the URL unless it lands on a path of its own.

    These are the same page, not a redirect: a redirect would race the beacon,
    which fires an XHR immediately and would be cancelled by the navigation.
    Each one carries a canonical pointing at the real issue so search engines
    consolidate them, and they are kept out of sitemap.xml.
    """
    out = []
    for n, i in enumerate(ISSUES):
        prev = ISSUES[n - 1] if n else None
        nxt = ISSUES[n + 1] if n + 1 < len(ISSUES) else None
        html = parent_page(i, prev, nxt)
        real = f"{SITE}parents/no-{i['no']}-{i['slug']}.html"
        # point canonical and og:url at the real issue, not at the tracking path
        html = re.sub(r'<link rel="canonical" href="[^"]*">',
                      f'<link rel="canonical" href="{real}">', html)
        html = re.sub(r'<meta property="og:url" content="[^"]*">',
                      f'<meta property="og:url" content="{real}">', html)
        # sits one level deep like parents/, so ../assets and ../kids still
        # resolve - but bare sibling links (the pager, the contents link) were
        # relative to parents/ and must be repointed there.
        html = re.sub(r'href="(?!\.\.|https?:|#|mailto:)([^"]+)"',
                      r'href="../parents/\1"', html)
        out.append((f"s/{i['no']}.html", html))
    return out


def schools_page():
    """The institutional offer.

    A PTA newsletter editor and a form tutor both have the same objection, which
    is not price - it is effort. So this page hands over paste-ready copy and a
    session that runs itself, and answers the AI question before it gets asked."""
    ALL = [dict(no="01", ask="So you want to get a dog", band="Usually 6&ndash;16",
                q="What a dog actually costs, and who does the six a.m. walk.",
                p="parents/no-01-so-you-want-a-dog.html", k="kids/no-01-the-case-for-a-dog.html")]
    ALL += [dict(no=i["no"], ask=i["ask"], band=i["band"], q=real_question(i),
                 p=f"parents/no-{i['no']}-{i['slug']}.html",
                 k=f"kids/no-{i['no']}-{i['slug']}.html") for i in ISSUES]

    blurbs = "".join(f"""
    <div class="blurb">
      <span class="bt">No. {a['no']} &middot; {a['band']}</span>
      <div class="bx" id="b{a['no']}"><strong>{a['ask']}</strong> &mdash; {a['q']}
      A free one-page guide for parents, plus a version written for your child. No sign-up and nothing to install:
      {SITE}s/{a['no']}.html</div>
      <button type="button" class="copy" data-copy="#b{a['no']}">Copy</button>
    </div>""" for a in ALL)

    rows = "".join(f"""
      <a class="toc-row" href="{a['p']}">
        <span class="n mono">No. {a['no']}</span>
        <span class="t"><b>{a['ask']}</b><em>{a['band']}</em></span>
        <span class="d">{a['q']} &middot; <a href="{a['k']}">kid&rsquo;s edition</a></span>
      </a>""" for a in ALL)

    contact = (f"""
  <section class="blk">
    <h2 class="sec">Ask us anything</h2>
    <p class="sec-sub">Including &ldquo;can we put this in Monday&rsquo;s newsletter&rdquo;, to which the answer is yes</p>
    <div class="col"><p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p></div>
  </section>""" if CONTACT_EMAIL else "")

    body = f"""<div class="top"><div class="wrap">
  <span><a href="index.html">The Big Ask</a></span><span>For schools, PTAs and practices</span>
</div></div>

<header class="hd"><div class="wrap">
  <p class="eyebrow">For schools, PTAs, tutors and practices</p>
  <h1 class="ask display">Print it.<br><em>Hand it out.</em></h1>
  <p class="thesis">Eleven conversations every family has to have, each on one page &mdash; with a second page
  written for the child. <b>Free to copy and distribute.</b> No sign-up, no licence fee, no accounts, nothing to install.</p>
</div></header>

<main class="wrap">
  <section class="blk">
    <h2 class="sec">Permission, in plain terms</h2>
    <p class="sec-sub">So nobody has to email anyone to find out</p>
    <div class="offer">
      <p><strong>You may</strong> print these, photocopy them, put them in a newsletter, hand them out at
      parents&rsquo; evening, put them in a waiting room, or run them in a tutor-time session. For any school,
      nursery, PTA, library, clinic or youth group. No permission needed and no fee.</p>
      <p><strong>Two conditions.</strong> Keep the note saying it was written by an AI &mdash; families are entitled
      to know that. And do not resell it.</p>
      <p style="color:var(--ink-2);font-size:.95rem;margin-top:.8rem">Every page is built to print: black on white,
      no wasted ink, worksheets that do not break across pages. Print from a browser, or hand over the link.</p>
    </div>
  </section>

  <section class="blk">
    <h2 class="sec">Put one in your newsletter</h2>
    <p class="sec-sub">Written to be pasted &mdash; no editing needed, nothing to write</p>
    <div class="col"><p>Each of these is a finished paragraph. Copy one, paste it into the newsletter, done.
    One a month works well; the age band tells you which year groups it lands with.</p></div>
    {blurbs}
  </section>

  <section class="blk">
    <h2 class="sec">Run it in twenty minutes</h2>
    <p class="sec-sub">Tutor time, PSHE, advisory, form period</p>
    <div class="col">
      <p>The kid&rsquo;s edition is built for this. Each one is a single card &mdash; what the adult is actually
      worried about, what to say, what not to say, and one thing to go and do.</p>
      <ol class="steps-n">
        <li><b>Read the card together. Two minutes.</b> The whole thing is about three hundred words.</li>
        <li><b>Do the widget. Five minutes.</b> Every issue has one &mdash; a checklist, a sorter, a chooser. It works on a phone or a shared screen, and nothing they tap is recorded.</li>
        <li><b>Practise the line, in pairs. Eight minutes.</b> One is the child, one is the adult. Swap. The point is saying the sentence out loud before it matters.</li>
        <li><b>Send the parent half home. Five minutes.</b> Print it, or put the link in the bulletin. The two halves are written to agree with each other.</li>
      </ol>
      <p style="margin-top:1rem">It maps onto PSHE relationships and health education in the UK, and onto
      responsible decision-making in most SEL frameworks in the US. We would not overclaim it as a scheme of
      work &mdash; it is a conversation starter that happens to be structured.</p>
    </div>
  </section>

  <section class="blk">
    <h2 class="sec">Before you ask: yes, an AI wrote it</h2>
    <p class="sec-sub">You will need to answer this, so here is the answer</p>
    <div class="col">
      <p>Every word, both podcast voices and all of the design were produced by Claude, an AI model made by
      Anthropic. There is no human author to credit and we do not pretend otherwise &mdash; it says so on
      every page, in language a child can read.</p>
      <p>What that means for you, plainly. The advice is conventional and conservative: it will not tell a
      child to keep a secret from a parent, and it routes anything touching safety back to adults who know
      the family. It is not medical, legal or safeguarding guidance and does not claim to be. Read one before
      you send it &mdash; that is a reasonable bar for anything you hand to families, whoever wrote it.</p>
      <p>Some schools will be fine with that and some will not. We would rather you decided knowing.</p>
    </div>
  </section>

  <section class="blk">
    <h2 class="sec">The eleven</h2>
    <p class="sec-sub">Each with a parent page and a kid page</p>
    <div class="toc-list">{rows}</div>
  </section>
{contact}
</main>

<footer><div class="wrap"><p class="colo">{P_COLO}</p></div></footer>"""
    return page("For Schools", "Eleven conversations every family has to have - free to print, copy and hand out. No sign-up, no licence fee.",
                "assets/parents.css", P_FONTS, body, up="", page_path="for-schools.html", image="schools.png")


def index_page():
    rows = "".join(f"""
      <a class="toc-row" href="parents/no-{i['no']}-{i['slug']}.html">
        <span class="n mono">No. {i['no']}</span>
        <span class="t"><b>{i['ask']}</b><em>{i['band']}</em></span>
        <span class="d">Kid&rsquo;s edition: <a href="kids/no-{i['no']}-{i['slug']}.html">{i['title']}</a></span>
      </a>""" for i in ISSUES)
    body = f"""<div class="top"><div class="wrap">
  <span>A field manual for the decisions you make together</span>
  <span>Issues 01&ndash;11</span>
</div></div>

<header class="hd"><div class="wrap">
  <h1 class="ask display">The<br><em>Big Ask</em></h1>
  <p class="thesis">A magazine about the first big decisions parents and kids have to make together.
  Every issue comes in <b>two halves</b> &mdash; one written for you, one written for them.</p>
</div></header>

<main class="wrap">
  <section class="blk">
    <h2 class="sec">Issue No. 01 &mdash; The dog</h2>
    <p class="sec-sub">The long one &middot; with a podcast episode on each side</p>
    <div class="grid">
      <div class="box"><h4>For the parent</h4>
        <p><a href="parents/no-01-so-you-want-a-dog.html"><strong>So you want to get a dog</strong></a></p>
        <p>A live cost engine that prices a dog over its whole life, an audit of who really does the six a.m.
        walk, scripts by age, a two-week trial, and an agreement everybody signs. 12-minute episode inside.</p></div>
      <div class="box"><h4>For the kid</h4>
        <p><a href="kids/no-01-the-case-for-a-dog.html"><strong>The case for a dog</strong></a></p>
        <p>How to ask so grown-ups actually listen. A fourteen-morning tracker, and a builder that makes
        the one page you hand over. 6-minute episode inside.</p></div>
    </div>
  </section>

  <section class="blk">
    <h2 class="sec">Issues No. 02&ndash;11</h2>
    <p class="sec-sub">One issue each &middot; <a href="parents/no-02-11-ten-more-big-asks.html">contents, filterable by age</a>
      &middot; <a href="kids/no-02-11-ten-things-to-ask-for.html">the kid&rsquo;s ten</a></p>
    <div class="toc-list">{rows}</div>
  </section>

  <section class="blk">
    <h2 class="sec">The episodes</h2>
    <p class="sec-sub">Both built into Issue No. 01, or listen from here</p>
    <div class="grid">
      <div class="box"><h4>For parents &middot; 11:59</h4>
        <p><a href="audio/no-01-dog-parents.m4a">So you want to get a dog</a> &middot;
           <a href="transcripts/no-01-dog-parents.txt">transcript</a></p></div>
      <div class="box"><h4>For kids &middot; 6:33</h4>
        <p><a href="audio/no-01-dog-kids.m4a">How to ask for a dog</a> &middot;
           <a href="transcripts/no-01-dog-kids.txt">transcript</a></p></div>
    </div>
  </section>
</main>

  <section class="blk">
    <h2 class="sec">For schools, PTAs and practices</h2>
    <p class="sec-sub">Free to print, copy and hand out &mdash; no sign-up, no licence fee</p>
    <div class="col"><p>Paste-ready newsletter copy, a twenty-minute session that runs itself, and permission
    stated in plain terms so nobody has to email anyone. <a href="for-schools.html"><strong>Take a look &rarr;</strong></a></p></div>
  </section>

<footer><div class="wrap"><p class="colo">{P_COLO}<br><br>
Source, scripts and the audio pipeline:
<a href="https://github.com/skyspeak/magazine">github.com/skyspeak/magazine</a></p></div></footer>"""
    return page("The Big Ask",
        "A magazine about the first big decisions parents and kids make together. Every issue comes in two halves.",
        "assets/parents.css", P_FONTS, body, up="", page_path="", image="home.png")


def build():
    out = []
    for n, i in enumerate(ISSUES):
        prev = ISSUES[n-1] if n else None
        nxt = ISSUES[n+1] if n+1 < len(ISSUES) else None
        out.append((f"parents/no-{i['no']}-{i['slug']}.html", parent_page(i, prev, nxt)))
        out.append((f"kids/no-{i['no']}-{i['slug']}.html", kid_page(i, prev, nxt)))
    out.append(("parents/no-02-11-ten-more-big-asks.html", parents_contents()))
    out.append(("kids/no-02-11-ten-things-to-ask-for.html", kids_contents()))
    out.append(("index.html", index_page()))
    out.append(("for-schools.html", schools_page()))
    out.extend(school_entry_pages())
    for path, htm in out:
        full = os.path.join(REPO, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(ascii_only(htm))
    print(f"  built {len(out)} pages")
    for path, htm in out:
        print(f"    {path:<52} {len(htm)/1024:6.1f} KB")

if __name__ == "__main__":
    build()
