#!/usr/bin/env python3
"""Static checks over every page in the repo.

    python3 src/check_site.py

Catches the things that actually break here: dead internal links, unbalanced
tags, duplicate ids, stray non-ASCII, malformed widget payloads, and colour
tokens that exist in only one of the three theme blocks.

Note the attribute stripping below. Widget payloads are JSON in a single-quoted
data-w attribute and legitimately contain "<em>". A tag scanner that is not
attribute-aware reports those as stray closing tags. They are not.
"""
import json, os, re, sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr"}
SKIP = (".git", "build", "node_modules")

def strip_attrs(s):
    """Blank out attribute values so '<' inside them is not read as a tag."""
    return re.sub(r'=\s*(".*?"|\'.*?\')', '=""', s, flags=re.S)

def check(path):
    out = []
    raw = open(path).read()
    s = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S)
    s = re.sub(r"<style>.*?</style>", "", s, flags=re.S)
    payloads = re.findall(r"data-w='([^']*)'", s)
    s = strip_attrs(s)

    stack = []
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>", s):
        closing, tag, selfc = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or selfc:
            continue
        if closing:
            if stack and stack[-1] == tag: stack.pop()
            else: out.append(f"stray </{tag}>")
        else:
            stack.append(tag)
    if stack:
        out.append(f"unclosed: {stack[:4]}")

    dupes = [k for k, v in Counter(re.findall(r'\sid="([^"]+)"', raw)).items() if v > 1]
    if dupes: out.append(f"duplicate ids: {dupes}")

    non_ascii = [c for c in raw if ord(c) > 127]
    if non_ascii: out.append(f"{len(non_ascii)} non-ASCII characters")

    for p in payloads:
        try: json.loads(p)
        except Exception as e: out.append(f"bad widget JSON: {e}")

    for href in re.findall(r'(?:href|src)="([^"#][^"]*)"', raw):
        if href.startswith(("http", "data:", "mailto:")): continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), href.split("#")[0]))
        if not os.path.exists(target): out.append(f"dead link -> {href}")
    return out

def check_css(path):
    s, out = open(path).read(), []
    def block(pattern):
        m = re.search(pattern, s, re.S | re.M)
        return set(re.findall(r"--([a-z0-9-]+):", m.group(1))) if m else set()
    root = block(r"^:root\{(.*?)\n\}")
    dark = block(r':root\[data-theme="dark"\]\{(.*?)\n\}')
    media = block(r'@media \(prefers-color-scheme:dark\)\{:root:not\(\[data-theme="light"\]\)\{(.*?)\n\}\}')
    if dark - root: out.append(f"defined only in dark: {sorted(dark - root)}")
    if dark != media: out.append(f"media/data-theme mismatch: {sorted(dark ^ media)}")
    if "@media print" not in s: out.append("no print stylesheet")
    return out

def main():
    pages = sorted(os.path.join(d, f)
                   for d, _, fs in os.walk(REPO) for f in fs
                   if f.endswith(".html") and not any(k in d for k in SKIP))
    failures = 0
    for p in pages:
        problems = check(p)
        if problems:
            failures += 1
            print(f"FAIL {os.path.relpath(p, REPO)}")
            for x in problems: print(f"       {x}")
    for c in ("assets/parents.css", "assets/kids.css"):
        problems = check_css(os.path.join(REPO, c))
        if problems:
            failures += 1
            print(f"FAIL {c}")
            for x in problems: print(f"       {x}")
    print(f"\n{len(pages)} pages + 2 stylesheets checked, {failures} with problems")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
