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

| | Parents | Kids |
|---|---|---|
| **No. 01 — So you want to get a dog** | [`parents/no-01-so-you-want-a-dog.html`](parents/no-01-so-you-want-a-dog.html) | [`kids/no-01-the-case-for-a-dog.html`](kids/no-01-the-case-for-a-dog.html) |
| **Nos. 02–11 — ten more asks** | [`parents/no-02-11-ten-more-big-asks.html`](parents/no-02-11-ten-more-big-asks.html) | [`kids/no-02-11-ten-things-to-ask-for.html`](kids/no-02-11-ten-things-to-ask-for.html) |

**Issue No. 01** takes one decision apart at full length: a live cost engine that
prices a dog over its whole life, a labour audit of an ordinary Tuesday, scripts
by age, a two-week trial protocol, a fillable job application, and a family
agreement everybody signs. The kid's half has a fourteen-morning tracker and a
builder that assembles a one-page case they can hand over.

**Issues Nos. 02–11** are deliberately short — one page each, filterable by your
kid's age: a phone, being online, a sleepover, going somewhere alone, quitting
the thing, staying home alone, money of their own, a first job, changing how
they look, and going out with someone. The kid's edition of those ten is one
card per ask, about sixty words each.

Each page is a single self-contained HTML file. No build step, no dependencies,
no network calls except Google Fonts. Open one in a browser and it works.

## The episodes

Two podcast episodes for Issue No. 01, in `audio/`. The voices are macOS speech
synthesis; the scripts were written for the ear, not adapted from the page. The
episodes are embedded in the HTML as base64 so the pages stay self-contained,
and are also here as standalone files.

| Episode | Length | File |
|---|---|---|
| Parents — *So you want to get a dog* | 11:59 | `audio/no-01-dog-parents.m4a` |
| Kids — *How to ask for a dog* | 6:33 | `audio/no-01-dog-kids.m4a` |

Transcripts are in `transcripts/`. The `-web` files are the lower-bitrate
versions that are actually embedded in the pages.

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

The HTML files are the source of truth. `src/gen_issues.py` and `src/gen_kid.py`
hold the content for Nos. 02–11 as plain Python data and emit HTML fragments —
useful for bulk edits or for adding an issue, but the fragment has to go back
into the page by hand.

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
  is the kids' fourteen-morning tracker, which uses `localStorage` and degrades
  gracefully when it is unavailable.

## A note on the numbers

Costs are 2026 US estimates assembled from typical published ranges, and are
labelled as estimates on the page. Age bands are rough. None of this is
veterinary, medical, legal, financial or safeguarding advice, and anything
touching a child's safety belongs with people who know your family.

The method, in one line: decide it out loud, decide it with them in the room,
and if the answer is "not yet", bring a reason and a date.
