#!/usr/bin/env python3
"""Renders a 1200x630 social preview card for every page, into og/.

    python3 src/build_og.py

Shared links are how parenting material actually travels - WhatsApp groups,
iMessage, school parent chats, Facebook groups. Without og:image a link renders
as bare text and gets no clicks, so these are not decoration.

Uses headless Chrome, which ships on most Macs. If it is missing, the pages
still work; they just fall back to a text-only preview.
"""
import html, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import ISSUES

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "og")
TMP = os.path.join(OUT, "_card.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PARENT_CSS = """
  --bg:#E9E7DE; --ink:#191B1E; --dim:#5B5E58; --accent:#9A6E11;
  --display:'Big Shoulders Display'; --mono:'Courier Prime';"""
KID_CSS = """
  --bg:#FFD9E8; --ink:#16171C; --dim:#585B62; --accent:#E01A6F;
  --display:'Shantell Sans'; --mono:'Shantell Sans';"""

TPL = """<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Courier+Prime:wght@400;700&family=Shantell+Sans:wght@600;800&display=swap">
<style>
*{{box-sizing:border-box;margin:0}}
body{{{vars}
  width:1200px;height:630px;background:var(--bg);color:var(--ink);
  padding:72px 80px;display:flex;flex-direction:column;justify-content:space-between;
  font-family:var(--mono),monospace;overflow:hidden}}
.top{{display:flex;justify-content:space-between;align-items:baseline;
  font-size:22px;letter-spacing:.18em;text-transform:uppercase;color:var(--dim)}}
.top b{{color:var(--ink);letter-spacing:.24em}}
h1{{font-family:var(--display),sans-serif;font-weight:{weight};line-height:{lh};
  font-size:{size}px;text-transform:{tt};letter-spacing:{ls}}}
.sub{{font-family:var(--mono),monospace;font-size:26px;line-height:1.45;color:var(--dim);
  max-width:940px;margin-top:26px}}
.bar{{height:10px;background:var(--accent);width:170px;margin-bottom:30px}}
.foot{{display:flex;justify-content:space-between;align-items:baseline;
  font-size:21px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}}
.foot .who{{color:var(--accent);font-weight:700}}
</style>
<body>
  <div class="top"><span><b>The Big Ask</b></span><span>{issue}</span></div>
  <div><div class="bar"></div><h1>{title}</h1><div class="sub">{sub}</div></div>
  <div class="foot"><span class="who">{who}</span><span>{ages}</span></div>
</body>"""


def cap(t):
    return t[0].upper() + t[1:] if t else t


def card(path, *, kid, issue, title, sub, who, ages):
    size = 92 if len(title) > 26 else 116
    open(TMP, "w").write(TPL.format(
        vars=KID_CSS if kid else PARENT_CSS,
        weight=800 if kid else 900,
        lh=1.02 if kid else 0.9,
        tt="none" if kid else "uppercase",
        ls="-.02em" if kid else "-.005em",
        size=size - (10 if kid else 0),
        issue=html.escape(issue), title=html.escape(title),
        sub=html.escape(sub), who=html.escape(who), ages=html.escape(ages)))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--virtual-time-budget=5000",
                    f"--screenshot={path}", "--window-size=1200,630",
                    "file://" + TMP],
                   check=True, capture_output=True)


def main():
    if not os.path.exists(CHROME):
        print("Chrome not found - skipping preview cards"); return 0
    os.makedirs(OUT, exist_ok=True)
    jobs = [("og/home.png", dict(kid=False, issue="Issues 01-11", title="The Big Ask",
        sub="The first big decisions parents and kids make together. Every issue comes in two halves.",
        who="One for you, one for them", ages="Free - nothing to sign up for"))]
    jobs.append(("og/no-01-parents.png", dict(kid=False, issue="Issue No. 01",
        title="So you want to get a dog", sub="What it really costs, who does the six a.m. walk, and the agreement everybody signs.",
        who="For the parent", ages="Podcast inside")))
    jobs.append(("og/no-01-kids.png", dict(kid=True, issue="Issue No. 01",
        title="The case for a dog", sub="How to ask so grown-ups actually listen.",
        who="For the kid", ages="Podcast inside")))
    jobs.append(("og/contents-parents.png", dict(kid=False, issue="Issues 02-11",
        title="Ten more big asks", sub="A phone, being online, sleepovers, going alone, quitting, home alone, money, a job, how they look, dating.",
        who="For the parent", ages="One page each")))
    jobs.append(("og/contents-kids.png", dict(kid=True, issue="Issues 02-11",
        title="Ten things to ask for", sub="What they're actually scared of, and what to say instead.",
        who="For the kid", ages="One card each")))
    for i in ISSUES:
        band = i["band"].replace("&ndash;", "-")
        jobs.append((f"og/no-{i['no']}-parents.png", dict(kid=False,
            issue=f"Issue No. {i['no']}", title=i["ask"],
            sub=cap(i["deciding"]["q"].split("It is:")[-1].replace("<em>","").replace("</em>","").strip()),
            who="For the parent", ages=band)))
        k = i["kid"]
        jobs.append((f"og/no-{i['no']}-kids.png", dict(kid=True,
            issue=f"Issue No. {i['no']}", title=i["ask"],
            sub="They're scared of: " + k["scared"].replace("&rsquo;","'"),
            who="For the kid", ages=band)))
    for rel, kw in jobs:
        card(os.path.join(REPO, rel), **kw)
        print(f"  {rel:<32} {os.path.getsize(os.path.join(REPO, rel))//1024:>4} KB")
    os.remove(TMP)
    print(f"  {len(jobs)} cards")
    return 0

if __name__ == "__main__":
    sys.exit(main())
