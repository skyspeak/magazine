# Ten ways in

Distribution channels ranked by fit to **this** asset . Eleven free issues in
paired editions, built to print, openly AI-written, with nothing to buy , not
by what works for products in general.

Companion to [OUTREACH.md](OUTREACH.md), which is the detailed playbook for
channel 1.

## Read this first

**"Customers" is still aspirational.** There is nothing to buy, so every channel
below acquires *distribution*, not revenue. That is the right order . You cannot
price something nobody has read , but it means success for the next three months
is measured in schools that ran an issue, not in money.

**You cannot run ten channels.** Run **1 and 3**. They are the only two that
compound, they fail in different ways, and neither needs a budget. Everything
from 6 down is a distraction until one of them shows a pulse.

## The field

| # | Channel | Effort | First result | Ceiling | Compounds |
|---|---|---|---|---|---|
| 1 | PTA & school newsletters | Medium | 2–4 weeks | High | Yes |
| 2 | Counsellors & heads of year | Medium | 4–8 weeks | High | Yes |
| 3 | Pinterest | Low | 4–12 weeks | High | Yes |
| 4 | Printable search long-tail | Medium | 3–6 months | Medium | Yes |
| 5 | Libraries | Low | 2–6 weeks | Medium | Some |
| 6 | Clinics & health visitors | High | 2–4 months | Medium | Yes |
| 7 | Parenting newsletters | Medium | 2–6 weeks | Medium | No |
| 8 | Clubs, Scouts, sports | Low | 2–6 weeks | Low | Some |
| 9 | Teacher marketplaces | Medium | 4–10 weeks | Medium | Yes |
| 10 | The AI-made story | Low | Days | Low | No |

## The ten

**1. PTA and school newsletters** — *built for; start here*
One send reaches several hundred families. The editor is not evaluating a
product, they are filling a slot in Monday's bulletin and they are short of
time , which is why `for-schools.html` hands them a finished paragraph and a
copy button rather than a pitch.
→ Twenty schools within reach. Find the newsletter editor for each. Send the
email in OUTREACH.md, one issue only, chosen by season.

**2. Counsellors and heads of year** — *same door, different room*
Slower, because they think about it properly, but they distribute
year-group-wide and they care about the half nobody else publishes: the edition
written to the child.
→ Whenever a newsletter lands, follow up once to the pastoral lead at that same
school. The second yes is far cheaper than the first.

**3. Pinterest** — *the sleeper; run in parallel with 1*
The best consumer fit you have and the one most people skip. Pinterest is a
search engine for parenting printables, and unlike Google it does not weigh
author credentials , so being AI-written costs nothing here. It rewards visual
distinctiveness, which this design has in unusual measure, and pins keep
delivering for years. You already have thirty widgets and worksheets; each is
a pin.
→ Ten vertical 1000×1500 images: the family agreement, the phone grants, the
sleepover call, the fourteen-morning tracker. Same pipeline as `src/build_og.py`.

**4. The printable search long-tail** — *a narrow, winnable slice of SEO*
Do not fight for *should my child have a phone*. That is a credentials query and
you will lose to paediatricians, correctly. Fight for *printable family phone
agreement*, *questions to ask before a sleepover*, *chore contract template*.
Those want an artefact, not an expert.
→ Give the four best printables their own landing page with a real title and
description, so each can rank on its own instead of being buried in an issue.

**5. Libraries** — *low gatekeeping, oddly overlooked*
Libraries run parenting sessions, keep noticeboards, and are far more willing
than schools to take a free printable from a stranger. Children's librarians
talk to each other regionally, so one yes travels.
→ Walk into three nearest branches with the sleepover and going-alone issues
printed. Paper in hand converts better than a link.

**6. Clinics and health visitors** — *durable, heavily gatekept*
A health visitor reaches every family in a district. But this is where the AI
disclosure bites hardest . Clinical settings are cautious about unbadged advice,
and rightly so.
→ Leave it until two schools are running it. "Three local schools use this" is
the sentence that gets you past a practice manager.

**7. Parenting newsletters** — *borrowed audience, no compounding*
Substack and beehiiv parenting writers need things to link to, and a free
printable with no signup wall is an easy recommendation. Real traffic in one
burst, but it does not accumulate.
→ Find five writers who have already recommended a free resource. Offer the one
issue matching something they wrote. Never pitch the whole magazine.

**8. Clubs, Scouts and sports** — *small, easy, well-matched*
Almost no gatekeeping and a precise content match: going alone, quitting, a
first job. Scout and Guide groups run these conversations as badge work already.
→ One email to a district commissioner or club secretary offering the quitting
issue at end of season. Volunteer-run groups answer email faster than schools.

**9. Teacher marketplaces** — *real demand, policy risk*
Built-in search demand from exactly your buyer, and a free listing builds
presence before anything is priced. The caveat is genuine: these platforms have
tightened rules on AI-generated material, and being honest about authorship may
get a listing rejected.
→ List one free resource, disclosed. Treat it as a test of the policy, not as a
channel, until it survives.

**10. The AI-made story** — *fast, loud, wrong audience*
"An AI wrote, designed and voiced an entire parenting magazine" is a real hook
for Hacker News, design communities and AI newsletters. The one channel where
the disclosure is an asset. But those readers are not parents of ten-year-olds
and will not return. Its value is indirect: links (helps 4) and screenshots
(helps 3).
→ Hold it. Fire it once, deliberately, when the site is worth arriving at.

## Three that look tempting and are not

- **Reddit parenting subs.** Millions of members, and the obvious idea. Also
  strongly anti-self-promotion and increasingly anti-AI. The realistic outcome
  is removal, a ban, and a thread attached to the name that outranks everything
  else you do.
- **Large Facebook parenting groups.** Same shape; admins remove links from
  non-members on sight. The exception is a group you are part of,
  posting as a parent who made something , which does not scale.
- **Paid ads.** Nothing to sell means no return to measure and no bid you can
  justify. Ads scale something that already converts.

## What would make all of them work better

1. **A contact address.** `CONTACT_EMAIL` in `src/build_site.py` is empty, so
   the offer page omits the contact block entirely : a keen deputy head has no
   way to reply.
2. **A real domain.** `skyspeak.github.io/magazine` is not something anyone says
   out loud or trusts in a school newsletter. Cheapest credibility available.
3. **Analytics on.** Already wired, off by default. Without it you cannot tell
   which of these is working, and you will keep doing all of them badly instead
   of two of them well.

---

The ranking assumes what is true today: nothing to buy, no list, no domain,
openly AI-written, one person doing it. Change any of those and it moves : a
paid pack would lift 4 and 9 sharply, and a named human co-author would lift 6
more than anything else here.
