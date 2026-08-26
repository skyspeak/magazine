# Getting it into schools

The offer page is `for-schools.html`. Everything below assumes you have sent
someone that link and nothing else.

## Why this channel

One school newsletter reaches several hundred families in one send. The person
you are emailing is not evaluating a product — they are filling a slot in
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

## The email

Short. One link. No attachment — attachments from strangers do not get opened.

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

Low response rates are normal — this is cold outreach to busy people. Ten
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

Analytics are off by default. To turn them on, put a Cloudflare Web Analytics
token in `ANALYTICS_TOKEN` in `src/build_site.py` and rebuild — the privacy
wording on every page updates itself to match. Then watch referrers: a school
newsletter usually shows up as direct traffic in a burst on one day.
