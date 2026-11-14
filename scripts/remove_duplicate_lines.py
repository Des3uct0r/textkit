#!/usr/bin/env python3
"""word_count.py - count words, characters, lines and show top words.

Usage:
    python word_count.py essay.txt
    python word_count.py essay.txt --top 10
    cat essay.txt | python word_count.py
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def analyze(text, top_n=0):
    lines = text.splitlines()
    words = text.split()
    chars = len(text)
    chars_no_space = len(text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", ""))
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    result = {
        "lines": len(lines),
        "words": len(words),
        "chars": chars,
        "chars_no_space": chars_no_space,
        "paragraphs": len(paragraphs),
    }
    if top_n > 0:
        tokens = re.findall(r"[A-Za-z0-9']+", text.lower())
        result["top_words"] = Counter(tokens).most_common(top_n)
    return result


def main():
    ap = argparse.ArgumentParser(description="Count words, characters and lines.")
    ap.add_argument("input", nargs="?", help="input file (default: stdin)")
    ap.add_argument("--top", type=int, default=0, help="show top N most frequent words")
    args = ap.parse_args()

    if args.input:
        try:
            text = Path(args.input).read_text(encoding="utf-8")
        except OSError as e:
            print("Error: %s" % e, file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    r = analyze(text, args.top)
    print("Lines:            %d" % r["lines"])
    print("Words:            %d" % r["words"])
    print("Characters:       %d" % r["chars"])
    print("Chars (no space): %d" % r["chars_no_space"])
    print("Paragraphs:       %d" % r["paragraphs"])
    if "top_words" in r:
        print("\nTop words:")
        for word, n in r["top_words"]:
            print("  %4d  %s" % (n, word))


if __name__ == "__main__":
    main()
""" path="C:\x\mm\textkit\scripts\word_count.py"