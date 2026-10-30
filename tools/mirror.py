#!/usr/bin/env python3
"""
Stoppage Time: copy editions over from The Newsstand.

The Newsstand site (evanagribben/evanagribben.github.io) already pulls every
new edition out of Google Drive each hour, including the club newsletters it
does not show itself. This site does not talk to Drive at all: it reads that
public repository (checked out into ./source by the workflow) and copies the
editions of every publication in theme.PUBS.

Usage: python3 tools/mirror.py [path-to-newsstand-checkout]
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from theme import PUBS  # noqa: E402

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "source")


def main():
    with open(os.path.join(SRC, "manifest.json"), encoding="utf-8") as f:
        theirs = json.load(f)
    with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
        ours = json.load(f)
    wanted = [e for e in theirs.get("editions", []) if e.get("pub") in PUBS]
    raw_src = os.path.join(SRC, "editions", "raw")
    raw_dst = os.path.join(ROOT, "editions", "raw")
    os.makedirs(raw_dst, exist_ok=True)
    copied = 0
    for e in wanted:
        a = os.path.join(raw_src, e["slug"] + ".html")
        b = os.path.join(raw_dst, e["slug"] + ".html")
        if not os.path.isfile(a):
            continue
        new = open(a, "rb").read()
        old = open(b, "rb").read() if os.path.isfile(b) else None
        if new != old:
            open(b, "wb").write(new)
            copied += 1
    keep = {e["slug"] for e in wanted}
    for name in os.listdir(raw_dst):
        if name.endswith(".html") and name[:-5] not in keep:
            os.remove(os.path.join(raw_dst, name))
    ours["editions"] = [e for e in wanted
                        if os.path.isfile(os.path.join(raw_dst, e["slug"] + ".html"))]
    with open(os.path.join(ROOT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(ours, f, indent=2, ensure_ascii=False)
        f.write("\n")
    t = os.path.join(SRC, "titles.json")
    if os.path.isfile(t):
        shutil.copyfile(t, os.path.join(ROOT, "titles.json"))
    print(f"{len(ours['editions'])} editions, {copied} new or changed")


if __name__ == "__main__":
    main()
