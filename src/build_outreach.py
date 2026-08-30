#!/usr/bin/env python3
"""Generates the ready-to-send outreach assets into outreach/.

    python3 src/build_outreach.py

Blurbs, links and the tracker are built from content.py so they cannot drift
from the site. The emails are written by hand and live in EMAILS below.
Every link is a tracked /s/NN.html path, which is the only thing that makes
the schools channel measurable (see OUTREACH.md).
"""
import csv, os, re, sys, html, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import ISSUES

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.path.join(REPO, "outreach")
SITE = "https://skyspeak.github.io/magazine/"
FROM = "Megh"
EMAIL = "skyspeak@gmail.com"
OFFER = SITE + "for-schools.html"

strip = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

def catalogue():
    rows = [dict(no="01", ask="So you want to get a dog", band="Usually 6-16",
                 q="What a dog really costs, and who does the six a.m. walk in February.")]
    for i in ISSUES:
        rows.append(dict(no=i["no"], ask=strip(i["ask"]),
                         band=strip(i["band"]).replace("–", "-"),
                         q=strip(i["deciding"]["q"])))
    for r in rows:
        r["link"] = f"{SITE}s/{r['no']}.html"
    return rows


EMAILS = [
("PTA / PTO newsletter editor", "The first email. Fastest yes: they need copy weekly and have no budget to clear.",
 ["Free one-page parent guides, yours to print",
  "Something free for the newsletter",
  "A parent guide you can reprint"],
 """Hello,

I make a free thing that might suit the newsletter.

It covers eleven conversations most families end up having: the first phone, a
first sleepover, walking into town alone, quitting the instrument, a first job.
Each one is a single page for parents. There is a second page written to the
child, so both halves of the conversation get something.

Free to print, copy and hand out. No sign-up, no fee, nothing to install.

The newsletter paragraphs are already written, so it is about thirty seconds of
work at your end: {offer}

One thing before you use it, because a parent will ask: an AI wrote it, and it
says so on every page. Worth reading one first. Most people start with the phone
issue.

Thanks either way,
{name}
{email}"""),

("Pastoral lead / head of year / counsellor", "Slower than the newsletter editor, but distributes year-group-wide.",
 ["A free page for tutor time",
  "Something for PSHE, free to print",
  "Free conversation guides, written to the child as well"],
 """Hello,

I run a small free magazine for parents about the decisions families make
together: the first phone, being online, a sleepover, going into town alone,
quitting, a first job.

The part that might interest you is that every issue has a second edition
written to the child rather than about them. One card each, about three hundred
words: what the adult is worried about, what to say, what not to say, and one
thing to go and do.

It is built to run in twenty minutes. Read the card, do the exercise, practise
the line in pairs, send the parent half home.

Free to print and copy, no sign-up: {offer}

One thing before you use it: an AI wrote it, and every page says so. Worth
reading one first.

{name}
{email}"""),

("Librarian", "Low gatekeeping. Children's librarians talk to each other regionally.",
 ["Free printable parent guides for the noticeboard",
  "Something for the parenting shelf",
  "Free to print, for parents"],
 """Hello,

I make a free magazine about the decisions parents and children have to make
together: a first phone, a first sleepover, going into town alone, a first job.

Each issue is one page for the parent and a second page written to the child.
They are built to print. Black on white, no wasted ink, and the worksheets do
not break across pages.

If they suit a noticeboard, a parenting session or the shelf, they are free to
print and copy. No sign-up and no fee: {offer}

An AI wrote all of it and every page says so, which you may want to know before
putting it out.

{name}
{email}"""),

("Scout / Guide group, sports club, youth group", "Volunteer-run, so they answer email far faster than schools.",
 ["Free guide for parents at the end of the season",
  "Something for the parents' mailing list",
  "A free page on quitting, if it is useful"],
 """Hello,

I make free one-page guides for parents on the decisions families make
together. Three of them might suit your group: quitting the thing, going
somewhere alone, and a first job.

The quitting one lands well at the end of a season, when a few families are
having that conversation anyway. One page for the parent, and a page written to
the child.

Free to print or to put in a mailing list, no sign-up:
{site}s/06.html

An AI wrote it, and it says so on the page.

{name}
{email}"""),

("Follow-up, once, about ten days later", "Send this once and then stop. Two follow-ups is a nuisance.",
 ["Re: (keep the original subject line)"],
 """Hello,

Following up once on the below, then I will leave you alone.

If it is not right for you, no problem at all. If a different issue would suit
better, the sleepover and the phone are the two people ask for most.

{offer}

{name}"""),

("Reply when they say yes", "Make the next step smaller than they expect.",
 ["Re: (keep the thread)"],
 """Thanks, glad it is useful.

The newsletter paragraphs are on this page, ready to paste:
{offer}

Pick whichever issue fits the year group. The age band is on each one. If you
would rather I pasted the text straight into an email so you do not have to
visit the site, say so and I will send it over.

Nothing to credit and nothing to link back to, though a link is welcome.

{name}"""),

("Reply to the AI question", "You will get this. Answer it plainly and let them decide.",
 ["Re: (keep the thread)"],
 """Fair question, and I would rather you asked.

Yes. An AI wrote all of it, and every page says so in language a child can read.
There is no human author to credit and I do not pretend there is.

What that means in practice: the advice is conventional and cautious. It will
not tell a child to keep something from a parent, and anything touching safety
it points back to adults who know the family. It is not medical or safeguarding
guidance and does not claim to be.

My suggestion is the one I would make about anything you hand to families: read
one before you send it. If it is not right for your school, that is a completely
reasonable call.

{name}"""),
]


def write_emails(rows):
    fill = lambda t: t.format(offer=OFFER, site=SITE, name=FROM, email=EMAIL)
    out = ["# Outreach emails",
           "",
           "Ready to send. Proofread, pick a subject line, paste into your mail client.",
           "Plain text only, no attachment: attachments from strangers do not get opened.",
           "",
           f"Sign-off is set to **{FROM}** / {EMAIL}. Change it in `src/build_outreach.py` and rebuild.",
           ""]
    for n, (who, note, subjects, body) in enumerate(EMAILS, 1):
        out += [f"## {n}. {who}", "", f"*{note}*", "", "**Subject line** (pick one):", ""]
        out += [f"- {s}" for s in subjects]
        out += ["", "```", fill(body).strip(), "```", ""]
    out += ["## Tracked links", "",
            "Every link above goes through `/s/NN.html`. That is deliberate: email strips",
            "the referrer, so a plain link arrives as anonymous direct traffic. These paths",
            "show up by name in analytics.", "",
            "| No. | Issue | Ages | Link |", "|---|---|---|---|"]
    out += [f"| {r['no']} | {r['ask']} | {r['band']} | {r['link']} |" for r in rows]
    out += [""]
    open(os.path.join(OUT, "emails.md"), "w").write("\n".join(out))
    return len(EMAILS)


def write_blurbs(rows):
    out = ["NEWSLETTER PARAGRAPHS",
           "",
           "One finished paragraph per issue. Copy one, paste it in, done.",
           "One a month works well. The age band tells you which year groups it lands with.",
           "", "." * 72, ""]
    for r in rows:
        q = r["q"][0].lower() + r["q"][1:]
        para = (f"{r['ask']}. A free one-page guide for parents on {q} "
                f"There is a second page written for your child. "
                f"No sign-up and nothing to install: {r['link']}")
        out += [f"No. {r['no']}  |  {r['ask']}  |  {r['band']}", "." * 72]
        out += textwrap.wrap(para, 76)
        out += ["", ""]
    open(os.path.join(OUT, "blurbs.txt"), "w").write("\n".join(out))
    return len(rows)


def write_tracker(rows):
    # template only. The filled copy is gitignored: it will hold the names and
    # email addresses of real school staff, and this repository is public.
    p = os.path.join(OUT, "tracker-template.csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["organisation", "contact name", "role", "email", "issue no",
                    "tracked link", "date sent", "follow-up due", "replied",
                    "outcome", "notes"])
    p2 = os.path.join(OUT, "links.csv")
    with open(p2, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["issue no", "issue", "ages", "tracked link", "the question it answers"])
        for r in rows:
            w.writerow([r["no"], r["ask"], r["band"], r["link"], r["q"]])
    return p, p2


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rows = catalogue()
    n_mail = write_emails(rows)
    n_blurb = write_blurbs(rows)
    write_tracker(rows)
    print(f"  outreach/emails.md    {n_mail} emails, {len(rows)} tracked links")
    print(f"  outreach/blurbs.txt   {n_blurb} newsletter paragraphs")
    print(f"  outreach/links.csv    {len(rows)} rows")
    print(f"  outreach/tracker-template.csv  send log (copy to tracker.csv, which is gitignored)")
