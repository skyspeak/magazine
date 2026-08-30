#!/usr/bin/env python3
"""Generates the social assets into social/ : Pinterest pins, post copy,
influencer notes, and the Reddit and Hacker News posts.

    python3 src/build_social.py           # copy only
    python3 src/build_social.py --pins    # also re-render the pin images

Pin images are rendered with headless Chrome at 1000x1500 and are hosted from
the repo, so social/pinterest.csv is usable with Pinterest's bulk upload.
"""
import csv, html, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.path.join(REPO, "social")
PINS = os.path.join(OUT, "pins")
SITE = "https://skyspeak.github.io/magazine/"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Pins link to the real issue, not a tracked path: Pinterest sends a referrer,
# so it separates itself in analytics, and the canonical URL keeps the SEO.
PINSPEC = [
 ("01-dog-cost", "01", "What a dog really costs",
  ["Adoption fee: $50 to $500", "Then food, vet, insurance",
   "One emergency: $3,500", "Twelve years: $25,000"],
  "The number nobody says out loud, and the calculator that says it for you.",
  "parents/no-01-so-you-want-a-dog.html", "Money talks with kids"),
 ("01-dog-agreement", "01", "The family dog agreement",
  ["Who does mornings", "Who does the evening walk",
   "Who pays the vet bill", "Reviewed in three months"],
  "One page. Named jobs at named times, and a date to check it is still true.",
  "parents/no-01-so-you-want-a-dog.html", "Family routines"),
 ("02-phone-four", "02", "A phone is four decisions, not one",
  ["1  A device", "2  A phone number", "3  The open internet", "4  An app store"],
  "They arrive in one box. You can hand them over separately.",
  "parents/no-02-a-phone.html", "First phone"),
 ("02-phone-rule", "02", "The one phone rule worth setting",
  ["It sleeps in the kitchen", "Every night", "Yours does too", "Set it on day one"],
  "Frictionless on day one. Nearly impossible to introduce six months later.",
  "parents/no-02-a-phone.html", "First phone"),
 ("03-online-worry", "03", "What are you worried about?",
  ["Strangers", "It never goes away", "How much time it eats", "How it makes them feel"],
  "Four different fears, four different answers. The wrong one wastes the conversation.",
  "parents/no-03-being-online.html", "Kids and screens"),
 ("04-sleepover-call", "04", "6 questions before a sleepover",
  ["Who is home overnight?", "Who else is staying?",
   "Where is everyone sleeping?", "What are the screen rules?"],
  "The four minute phone call. Most parents ask these and nobody minds being asked.",
  "parents/no-04-a-sleepover.html", "Sleepovers"),
 ("04-sleepover-exit", "04", "The sleepover code word",
  ["Agree one word", "They text it", "You drive", "No questions till morning"],
  "A child will use an exit they are certain costs them nothing.",
  "parents/no-04-a-sleepover.html", "Sleepovers"),
 ("05-alone-ladder", "05", "Before they walk it alone",
  ["Together, three times", "Then wait at the far end",
   "Then they go alone", "Then a different route"],
  "Independence is a distance and you extend it. Rehearse the road, not the fear.",
  "parents/no-05-going-somewhere-alone.html", "Raising independent kids"),
 ("06-quitting-four", "06", "Which part do they hate?",
  ["The thing itself", "The teacher or coach", "The practising", "That it got hard"],
  "Four problems, four different fixes. I hate it is a noise, not information.",
  "parents/no-06-quitting.html", "Kids and activities"),
 ("07-home-alone", "07", "Home alone: the 4 boring emergencies",
  ["The doorbell", "The smoke alarm", "Locked out", "You do not pick up"],
  "Rehearse these four, not the ones you are picturing.",
  "parents/no-07-staying-home-alone.html", "Raising independent kids"),
 ("08-money-lose", "08", "Let them buy the rubbish thing",
  ["Let them buy it", "Do not replace it", "A regret at nine is cheap",
   "The same lesson later is not"],
  "Money only teaches when it can be lost. An allowance you top up is a lesson deleted.",
  "parents/no-08-money-of-their-own.html", "Money talks with kids"),
 ("10-looks-sort", "10", "Grows back. Washes out. Doesn't.",
  ["Hair grows back", "Dye washes out", "Most holes close", "Tattoos do not"],
  "Sort every request onto one axis and most of the argument disappears.",
  "parents/no-10-how-they-look.html", "Teenagers"),
]

PIN_TPL = """<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Courier+Prime:wght@400;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
*{{box-sizing:border-box;margin:0}}
body{{width:1000px;height:1500px;background:#E9E7DE;color:#191B1E;
 font-family:'Source Serif 4',Georgia,serif;padding:70px 66px;display:flex;flex-direction:column}}
.kicker{{font-family:'Courier Prime',monospace;font-size:25px;letter-spacing:.2em;
 text-transform:uppercase;color:#5B5E58}}
.bar{{height:12px;background:#9A6E11;width:190px;margin:34px 0 30px}}
h1{{font-family:'Big Shoulders Display',sans-serif;font-weight:900;text-transform:uppercase;
 font-size:{size}px;line-height:.9;letter-spacing:-.01em}}
.cards{{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:24px;margin:50px 0 0}}
.c{{border:4px solid #191B1E;background:#F3F1EA;padding:34px 30px;
 display:flex;flex-direction:column;justify-content:center}}
.c b{{font-family:'Big Shoulders Display',sans-serif;font-weight:700;text-transform:uppercase;
 font-size:50px;line-height:.98;display:block}}
.blurb{{font-size:35px;line-height:1.4;margin:46px 0 0;flex:0 0 auto}}
.foot{{margin-top:44px;border-top:5px solid #191B1E;padding-top:26px;
 display:flex;justify-content:space-between;align-items:baseline;
 font-family:'Courier Prime',monospace;font-size:24px;letter-spacing:.14em;text-transform:uppercase}}
.foot b{{letter-spacing:.24em}}
.foot span{{color:#9A6E11;font-weight:700}}
</style>
<body>
 <div class="kicker">The Big Ask &middot; No. {no}</div>
 <div class="bar"></div>
 <h1>{title}</h1>
 <div class="cards">
   <div class="c"><b>{i1}</b></div>
   <div class="c"><b>{i2}</b></div>
   <div class="c"><b>{i3}</b></div>
   <div class="c"><b>{i4}</b></div>
 </div>
 <div class="blurb">{blurb}</div>
 <div class="foot"><b>Free. No sign-up.</b><span>Both halves inside</span></div>
</body>"""


def render_pins():
    if not os.path.exists(CHROME):
        print("  Chrome not found, skipping pin images"); return 0
    os.makedirs(PINS, exist_ok=True)
    tmp = os.path.join(PINS, "_pin.html")
    for slug, no, title, items, blurb, link, board in PINSPEC:
        e = [html.escape(x) for x in items]
        open(tmp, "w").write(PIN_TPL.format(
            no=no, title=html.escape(title), size=96 if len(title) > 26 else 112,
            i1=e[0], i2=e[1], i3=e[2], i4=e[3], blurb=html.escape(blurb)))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--virtual-time-budget=5000",
                        f"--screenshot={os.path.join(PINS, slug + '.png')}",
                        "--window-size=1000,1500", "file://" + tmp],
                       check=True, capture_output=True)
    os.remove(tmp)
    return len(PINSPEC)


def write_pinterest_csv():
    p = os.path.join(OUT, "pinterest.csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail",
                    "Description", "Link", "Publish date", "Keywords"])
        for slug, no, title, items, blurb, link, board in PINSPEC:
            w.writerow([title, f"{SITE}social/pins/{slug}.png", board, "",
                        f"{blurb} Free to read and print, no sign-up. Written by an AI, "
                        f"and it says so on every page.", SITE + link, "",
                        board.lower().replace(" ", ", ")])
    return len(PINSPEC)


POSTS = [
("Instagram / Facebook / Threads", "Use a pin image or an issue card. Caption below.",
 """Eleven conversations every family ends up having: the first phone, the first
sleepover, walking into town alone, quitting the instrument, a first job.

Each one is a single page for you. And a second page written to your kid, so
both halves of the conversation get something.

Free to read and print. No sign-up, no app, nothing to buy.

An AI wrote all of it and every page says so, which you should probably know
before you hand it to a nine year old.

Link in bio."""),

("LinkedIn", "Aim it at teachers, PTA committees and school leaders rather than parents.",
 """Schools and PTAs: this is free to print and hand out, and there is nothing to
sign up for.

It is eleven of the conversations families have to have. A first phone, a first
sleepover, walking into town alone, quitting, a first job. Each one is a single
page for the parent, plus a second page written to the child.

The newsletter paragraphs are already written, so putting one in Monday's
bulletin is about thirty seconds of work.

An AI wrote it, and every page says so in language a child can read. Read one
before you send it out. That is a fair bar for anything you give to families,
whoever wrote it.

https://skyspeak.github.io/magazine/for-schools.html"""),

("X / Bluesky", "Short. The AI angle is the hook here, not the parenting angle.",
 """An AI wrote an entire parenting magazine.

Eleven issues on the decisions families argue about: first phone, first
sleepover, walking home alone, quitting, a first job.

Every issue has two halves. One for the parent. One written to the kid.

Free, no sign-up, and it tells you on every page that nobody human wrote it.

https://skyspeak.github.io/magazine/"""),

("Instagram story / short video script", "15 seconds. Read it straight, no music bed needed.",
 """Your kid asks for a phone.

You say no. They ask again. Louder.

Here is the thing nobody tells either of you: a phone is four decisions, not
one. A device. A number. The open internet. An app store.

You can give them separately.

There is a free page on this. And a second page written to your kid, so they
know what you are worried about.

No sign-up. Link in bio."""),
]

INFLUENCERS = """# Influencer and newsletter outreach

Aim at people who have already recommended a free resource. They are used to
linking out and their audience expects it.

## Who fits

- Parenting newsletter writers on Substack and beehiiv
- Instagram accounts about school-age parenting, not baby or bump accounts
- Teachers and school counsellors with an audience
- Anyone who has written about kids and phones in the last year

Skip anyone whose whole feed is sponsored posts. They will ask for a rate and
you have no budget.

## The email or DM

Keep it to one screen. Offer one issue, not the magazine.

---

Hello,

You wrote about {topic} recently, so this may be useful or may not.

I make a free thing: eleven of the conversations families end up having, one
page each. The first phone, a first sleepover, walking into town alone,
quitting, a first job.

The bit that is unusual is that every issue has a second page written to the
child rather than about them, so both halves of the conversation get something.

No sign-up, no email wall, nothing to buy. If it suits your readers, the phone
one is here: https://skyspeak.github.io/magazine/parents/no-02-a-phone.html

One thing you would want to know before linking it: an AI wrote all of it, and
every page says so plainly. Happy for you to say that too.

No obligation either way, and no need to reply if it is not for you.

Megh
skyspeak@gmail.com

---

## What to offer, by what they cover

| They write about | Send them |
|---|---|
| Screens, phones, social media | No. 02 a phone, No. 03 being online |
| Anxiety, independence, free-range | No. 05 going somewhere alone, No. 07 home alone |
| Younger children, starting school | No. 04 a sleepover |
| Teenagers | No. 10 how they look, No. 11 going out with someone |
| Money, chores, allowance | No. 08 money of their own |
| Music lessons, sport, activities | No. 06 quitting |

## Do not

Do not offer payment, affiliate splits or exclusivity. You have nothing to pay
with and the offer reads as spam. The pitch is that it is free and it is
useful.
"""

REDDIT = """# Reddit

Read this before posting anything.

Reddit removes link drops from accounts with no history, and several parenting
subs remove AI-generated material on sight. The approach that survives is to be
a person who made something, not a brand doing distribution.

## Rules that apply

- Read each subreddit's rules page first. Several ban self-promotion outright.
- Most subs enforce a ratio. Comment for a week or two before you post a link.
- Do not post the same thing to five subs. That is what gets accounts banned.
- Disclose the AI authorship in the post body, not in a reply after someone
  finds out. Reddit forgives AI far more readily than it forgives concealment.

## Where it plausibly fits

| Subreddit | Fit | Note |
|---|---|---|
| r/Parenting | High reach | Strict on self-promotion. Comment first. |
| r/daddit, r/Mommit | Warmer | Still read the rules. |
| r/raisingkids, r/parentingteens | Better fit, smaller | Fewer rules, more tolerance |
| r/homeschool | Good fit for printables | |
| r/teachers | For the schools angle only | Never pitch parents here |

## The comment, which is the real strategy

Most of the value is answering a question properly and mentioning the page only
when it fits. Something like:

---

We went through this last year. The thing that helped was splitting it up:
a phone is really four separate decisions, and they arrive in one box. A
device, a phone number, the open internet, and an app store. You can hand over
the first two and hold the other two for six months.

The other one worth deciding on day one is where it charges at night, because
adding that rule later reads as a punishment for something.

I ended up writing this out as a free page, no sign-up: [link]. Fair warning,
an AI wrote it and it says so on the page.

---

## The self post, if you post one

Title: `I made a free parenting magazine and an AI wrote all of it`

Body:

---

I have been making a small free thing and would rather show it to people who
will tell me if it is bad.

It is eleven of the conversations families end up having. The first phone, a
first sleepover, walking into town alone, quitting an instrument, a first job.
Each one is a single page for the parent, and there is a second page written to
the child rather than about them.

Being upfront: an AI wrote all of it, including the two podcast episodes. Every
page says so in language a kid can read. I am not going to pretend a person
wrote it and let you find out later.

It is free, there is no sign-up, no email wall and nothing to buy. I am not
selling anything and there is no newsletter to join.

What I would find useful is whether the advice is any good, especially from
anyone who has had these conversations recently. The sleepover one is the one I
am least sure about.

[link]

---

## If it goes badly

If a post is removed, do not repost it or message the mods to argue. Delete it
and use a different sub. An argument with a moderator becomes the first result
for your project name.
"""

HN = """# Hacker News

Post once. Fire this when the site is worth arriving at, not before, because
you only get one first impression here.

## Timing

Tuesday to Thursday, roughly 8 to 10am US Eastern. Avoid weekends and holidays.

## Title

HN titles must be plain. No hype, no colons stacking clauses, no emoji.

Best option:

    Show HN: A parenting magazine written entirely by an AI, with a version for the kid

Alternates:

    Show HN: The Big Ask, a free parenting magazine written by an AI
    Show HN: I had an AI write a parenting magazine, both halves of it

## The post body

---

Every issue is one page for the parent and a second page written to the child
rather than about them, which is the part I have not seen elsewhere. Eleven
issues so far: a first phone, being online, a sleepover, walking into town
alone, quitting, staying home alone, money, a first job, appearance, dating.

An AI wrote all of it, including the design and both podcast episodes, and every
page says so in language a child can read. That felt like the only defensible
way to publish it.

Technically it is a static site with no build step for the reader: 37 pages of
plain HTML, shared CSS, five reusable widgets in about 150 lines of vanilla JS,
and the whole thing regenerates from one Python data file. The two podcast
episodes are macOS speech synthesis stitched in Python with synthesised theme
music. No dependencies, no framework, no tracking beyond cookieless page counts.

Free, no sign-up, nothing to buy. Source is on GitHub.

---

## The first comment, posted by you immediately

This matters as much as the post. Pre-empt the obvious objection.

---

Author here. The question I expect is whether AI-written parenting advice is a
good idea, and I think it is a fair thing to be suspicious of.

Two things I did about it. The advice is deliberately conventional and cautious:
it never tells a child to keep something from a parent, and anything touching
safety routes back to adults who know the family. And the disclosure is on every
page rather than in a footer, in words a nine year old can read, because a
parent finding out later from their kid would be much worse than being told
up front.

Happy to be told the writing is bad or the advice is wrong. That is the more
useful feedback.

---

## Answering comments

Answer everything for the first three hours, briefly, without defending. If
someone says the advice is wrong on a specific point, say you will look at it
and then change it. That plays well and it is also just correct.

Do not argue about whether AI should write things. You will lose the thread and
the thread is the point.
"""


def write_copy():
    out = ["# Social post copy", "",
           "Ready to paste. One platform per section.", ""]
    for who, note, body in POSTS:
        out += [f"## {who}", "", f"*{note}*", "", "```", body.strip(), "```", ""]
    out += ["## Images", "",
            "Pin images are in `social/pins/` at 1000x1500. The 1200x630 cards in `og/`",
            "suit Facebook, LinkedIn and X. Both are hosted from the repo, so they are",
            "linkable directly:", "",
            f"    {SITE}social/pins/04-sleepover-call.png",
            f"    {SITE}og/no-02-parents.png", ""]
    open(os.path.join(OUT, "posts.md"), "w").write("\n".join(out))
    open(os.path.join(OUT, "influencers.md"), "w").write(INFLUENCERS)
    open(os.path.join(OUT, "reddit.md"), "w").write(REDDIT)
    open(os.path.join(OUT, "hackernews.md"), "w").write(HN)
    return len(POSTS)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    n_posts = write_copy()
    n_csv = write_pinterest_csv()
    n_pins = render_pins() if "--pins" in sys.argv else 0
    print(f"  social/posts.md        {n_posts} platforms")
    print(f"  social/pinterest.csv   {n_csv} pins, bulk-upload ready")
    print(f"  social/influencers.md  outreach + what-to-send-whom table")
    print(f"  social/reddit.md       rules, comment script, self post")
    print(f"  social/hackernews.md   title options, body, first comment")
    if n_pins: print(f"  social/pins/           {n_pins} images at 1000x1500")
