#!/usr/bin/env python3
"""case_convert.py - convert text case in bulk.

Supports: upper, lower, title, sentence, snake, camel, kebab, slug.
Reads from a file or stdin; writes to stdout or a file.

Usage:
    python case_convert.py input.txt --to upper
    python case_convert.py input.txt --to slug --out slugs.txt
    echo "hello world" | python case_convert.py --to title
"""

import argparse
import re
import sys
from pathlib import Path


def convert(text, mode):
    if mode == "upper":
        return text.upper()
    if mode == "lower":
        return text.lower()
    if mode == "title":
        return text.title()
    if mode == "sentence":
        def repl(m):
            return m.group(1) + m.group(2).upper()
        return re.sub(r"(^|[.!?]\s+)([a-z])", repl, text)
    if mode == "snake":
        s = re.sub(r"[^A-Za-z0-9]+", "_", text.strip())
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", s).lower().strip("_")
    if mode == "camel":
        words = re.split(r"[^A-Za-z0-9]+", text.strip())
        words = [w for w in words if w]
        if not words:
            return ""
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])
    if mode == "kebab":
        s = re.sub(r"[^A-Za-z0-9]+", "-", text.strip())
        return re.sub(r"([a-z])([A-Z])", r"\1-\2", s).lower().strip("-")
    if mode == "slug":
        s = text.lower()
        s = re.sub(r"[^a-z0-9]+", "-", s)
        return s.strip("-")
    raise ValueError("unknown mode: " + mode)


def main():
    ap = argparse.ArgumentParser(description="Convert text case.")
    ap.add_argument("input", nargs="?", help="input file (default: stdin)")
    ap.add_argument("--to", required=True,
                    choices=["upper", "lower", "title", "sentence", "snake",
                             "camel", "kebab", "slug"],
                    help="target case")
    ap.add_argument("--out", help="output file (default: stdout)")
    args = ap.parse_args()

    if args.input:
        try:
            text = Path(args.input).read_text(encoding="utf-8")
        except OSError as e:
            print("Error: %s" % e, file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    result = convert(text, args.to)

    if args.out:
        try:
            Path(args.out).write_text(result, encoding="utf-8")
        except OSError as e:
            print("Error: %s" % e, file=sys.stderr)
            sys.exit(1)
        print("Wrote %s" % args.out)
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
""" path="C:\x\mm\textkit\scripts\case_convert.py"