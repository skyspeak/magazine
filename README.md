# The Big Ask

A small magazine about the first big decisions parents and kids have to make
together — and a companion edition, for every issue, written for the kid.

Every issue comes in two halves. The parents' half has the numbers, the labour
audit, the scripts and the contract. The kid's half is shorter, plainer, and
written to them rather than about them. Neither half contradicts the other, and
each links to its counterpart.

The whole thing — writing, design, illustration, and the voices in the two
podcast episodes — was made by Claude, an AI model from Anthropic. There is no
human newsroom behind it and no byline to look up. It says so on every page,
because a magazine that reads like people wrote it should say plainly when
nobody did.

---

## What's here

**No. 01 — the dog** is the long-form issue, hand-built:
[parents](parents/no-01-so-you-want-a-dog.html) · [kids](kids/no-01-the-case-for-a-dog.html).

**Nos. 02–11** are one issue each, generated from `src/content.py`. Contents pages:
[parents, filterable by age](parents/no-02-11-ten-more-big-asks.html) ·
[kids](kids/no-02-11-ten-things-to-ask-for.html).

| No. | Issue | Ages |
|---|---|---|
| 02 | A phone | 10–13 |
| 03 | Being online | 12–15 |
| 04 | A sleepover | 6–10 |
| 05 | Going somewhere alone | 8–12 |
| 06 | Quitting | any, repeatedly |
| 07 | Staying home alone | 9–13 |
| 08 | Money of their own | 7–14 |
| 09 | A first job | 13–17 |
| 10 | How they look | 10–16 |
| 11 | Going out with someone | 13–17 |

**Issue No. 01** takes one decision apart at full length: a live cost engine that
prices a dog over its whole life, a labour audit of an ordinary Tuesday, scripts
by age, a two-week trial protocol, a fillable job application, and a family
agreement everybody signs. The kid's half has a fourteen-morning tracker and a
builder that assembles a one-page case they can hand over.

**Issues Nos. 02–11** are short by design — one page each, same shape every time:
what you are actually deciding, the facts worth knowing, a script, the one rule,
the longer version, and a live readiness checklist. Each has a companion kid
edition of about three hundred words: what they're scared of, what to say, what
not to say, the one job, and what to ask for instead if it's a no.

`index.html` at the root is the cover: it links to all four editions and both
episodes.

Every page is one HTML file with no build step and no dependencies. The only
outbound requests are Google Fonts and, on Issue No. 01, the episode audio.

## The episodes

Two podcast episodes for Issue No. 01, in `audio/`. The voices are macOS speech
synthesis; the scripts were written for the ear, not adapted from the page. The
players in Issue No. 01 stream these files with chapter jumping, so the pages
themselves stay small.

| Episode | Length | File |
|---|---|---|
| Parents — *So you want to get a dog* | 11:59 | `audio/no-01-dog-parents.m4a` |
| Kids — *How to ask for a dog* | 6:33 | `audio/no-01-dog-kids.m4a` |

Transcripts are in `transcripts/`. The `-web` files are the lower-bitrate
versions the pages stream; the others are the higher-bitrate downloads.

Chapter jumping needs a server that honours HTTP `Range` requests. GitHub Pages
does. Python's `http.server` does **not** — audio will play from the start but
will not seek, which is a property of that server, not of the page.

## Rebuilding the audio

Needs macOS (`say` and `afconvert` ship with it). No other dependencies.

```bash
python3 src/render.py          # -> audio/no-01-dog-parents.wav
python3 src/render-kid.py      # -> audio/no-01-dog-kids.wav, src/chapters-kid.json
```

Then encode. 32 kbps is the version embedded in the pages; 64 kbps is the
standalone download:

```bash
afconvert -f m4af -d aac -s 0 -b 64000 audio/no-01-dog-parents.wav audio/no-01-dog-parents.m4a
```

The render scripts read `src/script.txt` and `src/script-kid.txt`, one line per
line of dialogue in the form `SPEAKER::RATE::text`. `[[slnc 400]]` inserts a
400 ms pause — it is a macOS speech command, not markup. Theme music is
synthesised from sine tones inside the render scripts; there are no audio assets.

Chapter offsets are computed from the render and live in `src/chapters.json` and
`src/chapters-kid.json`. They are pasted into the players in the HTML, so if you
re-record, update them there too.

## Editing

Issues 02–11 are **generated**. Do not edit those HTML files by hand — they are
build output and the next build will overwrite them.

```
src/content.py      all issue content, as plain Python data
src/build_site.py   renders 22 pages + index.html
src/check_site.py   static checks over everything
assets/parents.css  the parents' edition
assets/kids.css     the kids' edition
assets/widgets.js   the five widgets, shared by both
```

```bash
python3 src/build_site.py    # rebuild
python3 src/check_site.py    # dead links, tag balance, theme-token parity
```

**To add an issue:** append a dict to `ISSUES` in `src/content.py` and rebuild.
Both editions, the contents pages, the age filter, the previous/next pager and
the index all pick it up. Nothing else needs touching.

**The five widgets.** A page declares one with a `data-widget` attribute and a
JSON payload; `assets/widgets.js` does the rest. Nothing is transmitted, and
only `streak` persists — to `localStorage`, degrading quietly when unavailable.

| kind | what it does |
|---|---|
| `checklist` | tick items, get a verdict banded by how many |
| `chooser` | pick one of N, get the answer for that one |
| `streak` | N-day tracker, saved on the device |
| `dial` | a number you set, a sentence you get |
| `sorter` | put each item in a bucket, with a right answer |

Issue No. 01 is hand-built, has its CSS inline, and is deliberately untouched by
the generator. It is the one page where the layout is bespoke enough to be worth
the duplication.

Things worth preserving if you change the CSS:

- **Both themes are designed, not inverted.** Colours are defined as tokens in
  three places: `:root` (light), a `prefers-color-scheme: dark` block guarded
  with `:not([data-theme="light"])`, and `:root[data-theme="dark"]`. Never give a
  colour its only definition inside a media query — the un-stamped "system"
  state is the common case and it will fall through.
- **The print stylesheets use `!important` on purpose.** Without it the print
  tokens lose on specificity to the dark-mode rule, and printing from a dark
  browser produces a black page. These documents are meant to be printed.
- Nothing typed into any worksheet is stored or transmitted. The only exception
  is the streak trackers, which use `localStorage` and degrade gracefully when
  it is unavailable.
- Widget payloads are JSON inside a single-quoted `data-w` attribute and may
  legitimately contain `<em>`. A tag scanner that is not attribute-aware will
  report those as stray closing tags; `src/check_site.py` strips attribute
  values before scanning for exactly this reason.

## Deploying

The repo is the site. Settings -> Pages -> Source: *Deploy from a branch*,
branch `main`, folder `/ (root)`. It goes live at
`https://skyspeak.github.io/magazine/` and redeploys on every push. The
`.nojekyll` file stops Jekyll from processing the tree.

Nothing here needs a build pipeline, serverless functions, previews or edge
config, so a static host is the whole requirement.

## Two forms of the same page

The files in `parents/` and `kids/` are the **web** form: they stream audio from
`audio/` and link to each other by relative path. That is right for a website
and wrong for a Claude Artifact, which must be a single file with no siblings.

`src/build_artifact.py` produces the Artifact form in `build/` (gitignored). It
inlines the audio as a base64 data URI, folds in the shared CSS and JS (an
Artifact has no siblings, so a relative asset path is a dead link), re-points
cross-links at the published Artifact URLs, and rewrites anything else to the
live site:

```bash
python3 src/build_artifact.py            # all four
python3 src/build_artifact.py magazine   # just one
```

The difference is not small. Inlining costs about 33% on top of the audio and
has to arrive before the page renders:

| | web | artifact |
|---|---|---|
| `no-01-so-you-want-a-dog.html` | 80 KB | 3.83 MB |
| `no-01-the-case-for-a-dog.html` | 47 KB | 2.10 MB |

Edit the web version. Treat `build/` as output.

## Distribution

[ACQUISITION.md](ACQUISITION.md) ranks ten channels by fit to this project, with
the first concrete move for each and three tempting ones to avoid.
[OUTREACH.md](OUTREACH.md) is the detailed playbook for the one that was chosen:
schools and PTAs.

## A note on the numbers

Costs are 2026 US estimates assembled from typical published ranges, and are
labelled as estimates on the page. Age bands are rough. None of this is
veterinary, medical, legal, financial or safeguarding advice, and anything
touching a child's safety belongs with people who know your family.

The method, in one line: decide it out loud, decide it with them in the room,
and if the answer is "not yet", bring a reason and a date.
