# Getting it into schools

The offer page is `for-schools.html`. Everything below assumes you have sent
someone that link and nothing else.

## Why this channel

One school newsletter reaches several hundred families in one send. The person
you are emailing is not evaluating a product . They are filling a slot in
Monday's bulletin and they are short of time. The whole pitch is that you have
already done their work: the paragraph is written, the permission is granted,
and there is nothing to sign up for.

## Who to contact, in order

1. **PTA / PTO newsletter editor** — the fastest yes. They need content weekly
   and have no budget process to clear. Usually listed on the school website or
   the PTA Facebook page.
2. **School counsellor / pastoral lead / head of year** — cares about the kid
   editions and tutor-time use. Slower, but they distribute year-group-wide.
3. **PSHE / SEL / advisory coordinator** — the twenty-minute session is aimed
   squarely at them.
4. **Nursery and primary heads** — for issues 04 (sleepover) and 05 (going alone).
5. **Paediatric and GP practices, libraries, youth groups** — waiting-room
   printables. Slowest and most gatekept; leave until the others are working.

## The assets

Everything you need to send is generated into `outreach/`:

- `emails.md` - seven emails, ready to paste. Newsletter editor, pastoral lead,
  librarian, club secretary, one follow-up, a reply for when they say yes, and
  a reply for the AI question. Three subject lines each.
- `blurbs.txt` - the eleven newsletter paragraphs as plain text.
- `links.csv` - issue, age band and tracked link, for pasting into a sheet.
- `tracker-template.csv` - the send log. Copy it to `tracker.csv` before you
  use it. That filename is gitignored, because a filled tracker holds the names
  and email addresses of real people and this repository is public.

Regenerate with `python3 src/build_outreach.py`. The blurbs and links come from
`src/content.py`, so they cannot drift from the site. The emails are hand
written and live in that script.

## The email


Short. One link. No attachment . Attachments from strangers do not get opened.

> **Subject:** Free one-page parent guides — yours to print
>
> Hello — I make a small free thing that might suit your newsletter.
>
> It is eleven of the conversations every family ends up having: the first
> phone, the first sleepover, going into town alone, quitting the instrument,
> a first job. Each one is a single page for parents, and there is a second
> page written for the child, so both halves of the conversation get something.
>
> It is free to print, copy and hand out — no sign-up, no fee, nothing to
> install. There is paste-ready newsletter copy here, so it is about thirty
> seconds of work for you: https://skyspeak.github.io/magazine/for-schools.html
>
> One thing you should know before you use it, because you will be asked: it
> was written by an AI, and it says so on every page. Worth reading one before
> you send it out. The phone one is the usual starting point.
>
> Either way, thanks for the time.

## What to expect

Low response rates are normal . This is cold outreach to busy people. Ten
sends producing one yes is a working funnel. The compounding bit is that a
school that runs one issue will usually run the next.

Send them **one** issue, not eleven. Choose by season:

| When | Issue |
|---|---|
| Start of the school year | 02 a phone, 05 going somewhere alone |
| Transition to secondary / middle school | 02 a phone, 03 being online |
| Exam season | 09 a first job (hours cap), 06 quitting |
| Long holidays approaching | 04 a sleepover, 07 staying home alone |
| New year | 08 money of their own |

## Things not to do

- **Do not post it to r/Parenting or big Facebook parenting groups.** They are
  hostile to self-promotion and increasingly hostile to AI-written material.
  The likely outcome is a ban and a pile-on that follows the name.
- **Do not lead with the AI angle to schools.** Disclose it plainly, as the
  template does, but it is not the selling point here. It is the objection.
- **Do not hide the AI angle either.** A school that finds out later, from a
  parent, will never use it again.

## Measuring it

Cloudflare Web Analytics is on. Read it by **path**, not by referrer.

The newsletter blurbs link to `/s/01.html` … `/s/11.html` rather than to the
issue directly. That is not decoration . It is the only thing that makes this
channel measurable:

- email clients strip the referrer, so a newsletter click arrives as "direct",
  indistinguishable from someone typing the URL
- Cloudflare's beacon reports the **path only**. Query strings and hashes are
  both stripped from the payload (verified by intercepting it), so `?from=school`
  would have shown nothing

So `/s/04.html` in the dashboard means: somebody clicked the sleepover issue
from something you sent a school. Pinterest and other web referrers still show
up normally as referrers, so the two channels stay separable.

Each `s/` page is the real issue with a canonical pointing at the proper URL,
so search engines consolidate them and they are kept out of `sitemap.xml`.
They are regenerated by `src/build_site.py` . Do not edit them.

**Send one issue at a time and note the date.** A school newsletter produces a
burst on one day; that shape plus the path is your attribution.
