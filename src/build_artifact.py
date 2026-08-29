#!/usr/bin/env python3
"""Build self-contained copies of the pages, for publishing as Claude Artifacts.

The files in parents/ and kids/ are the *web* versions: they stream audio from
audio/ and link to each other with relative paths. That is right for a website
and wrong for an Artifact, which has to be a single file with no siblings.

This script produces the Artifact form in build/ by doing two things:
  1. inlining the episode audio back into the page as a base64 data URI
  2. re-pointing the cross-links at the published Artifact URLs

    python3 src/build_artifact.py            # all four
    python3 src/build_artifact.py magazine   # just one

Keep ARTIFACTS below in sync if a page is ever republished to a new URL.
"""
import base64, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.path.join(REPO, "build")

ARTIFACTS = {
    "magazine": "https://claude.ai/code/artifact/f75889a1-2ca1-495f-895f-3bda5af26691",
    "zine":     "https://claude.ai/code/artifact/a2f0380d-366a-4424-b2a4-bedd9ef126cf",
    "issues":   "https://claude.ai/code/artifact/7dd95626-01a6-4380-abed-d1bdd10a545f",
    "kidvol":   "https://claude.ai/code/artifact/5374ee8d-b3a6-45ce-be68-e106ee82c04b",
}
PAGES = {
    "magazine": "parents/no-01-so-you-want-a-dog.html",
    "issues":   "parents/no-02-11-ten-more-big-asks.html",
    "zine":     "kids/no-01-the-case-for-a-dog.html",
    "kidvol":   "kids/no-02-11-ten-things-to-ask-for.html",
}
# Only Issue No. 01 has an episode; the 02-11 volumes have no audio.
AUDIO = {"magazine": "audio/no-01-dog-parents-web.m4a",
         "zine":     "audio/no-01-dog-kids-web.m4a"}

# The canonical site. Links to pages that have no Artifact of their own are
# rewritten to point here, so an Artifact never contains a dead relative link.
SITE = "https://skyspeak.github.io/magazine/"


def inline_assets(html, page_path):
    """Fold ../assets/*.css and ../assets/widgets.js into the document.

    An Artifact is one file with no siblings, so a relative asset reference is a
    dead link. Issue No. 01 has its CSS inline already and is unaffected."""
    base = os.path.dirname(os.path.join(REPO, page_path))

    def css(m):
        p = os.path.normpath(os.path.join(base, m.group(1)))
        return "<style>\n" + open(p).read() + "\n</style>" if os.path.exists(p) else m.group(0)
    html = re.sub(r'<link rel="stylesheet" href="((?:\.\./)?assets/[^"]+)">', css, html)

    def js(m):
        p = os.path.normpath(os.path.join(base, m.group(1)))
        return "<script>\n" + open(p).read() + "\n</script>" if os.path.exists(p) else m.group(0)
    return re.sub(r'<script src="((?:\.\./)?assets/[^"]+)"[^>]*></script>', js, html)


def absolutise(html, page_path):
    """Point any remaining local link at the published site."""
    def fix(m):
        attr, href = m.group(1), m.group(2)
        if href.startswith(("http", "data:", "mailto:", "#")):
            return m.group(0)
        target = os.path.normpath(os.path.join(os.path.dirname(page_path), href))
        return f'{attr}="{SITE}{target}"'
    return re.sub(r'(href|src)="([^"]+)"', fix, html)


def build(key):
    src = os.path.join(REPO, PAGES[key])
    html = open(src).read()

    if key in AUDIO:
        raw = open(os.path.join(REPO, AUDIO[key]), "rb").read()
        uri = "data:audio/mp4;base64," + base64.b64encode(raw).decode()
        html, n = re.subn(r'src="[^"]*\.m4a"', 'src="' + uri + '"', html)
        if n != 1:
            raise SystemExit(f"{PAGES[key]}: expected one .m4a src, found {n}")

    html = inline_assets(html, PAGES[key])

    # The Artifact sandbox blocks third-party scripts, so the analytics beacon
    # would be a request that can never succeed. Strip it rather than ship it.
    html = re.sub(r"\s*<!-- Cloudflare Web Analytics -->.*?<!-- End Cloudflare Web Analytics -->",
                  "", html, flags=re.S)

    for other, url in ARTIFACTS.items():
        if other == key:
            continue
        rel = os.path.relpath(PAGES[other], os.path.dirname(PAGES[key]))
        html = html.replace('href="' + rel + '"',
                            'href="' + url + '" target="_blank" rel="noopener"')

    html = absolutise(html, PAGES[key])

    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, os.path.basename(PAGES[key]))
    open(dst, "w").write(html)
    print(f"  {PAGES[key]:<44} -> build/{os.path.basename(dst):<40} {len(html)/1048576:5.2f} MB")


if __name__ == "__main__":
    keys = sys.argv[1:] or list(PAGES)
    unknown = [k for k in keys if k not in PAGES]
    if unknown:
        raise SystemExit(f"unknown page(s): {unknown}. Choose from {list(PAGES)}")
    for k in keys:
        build(k)
