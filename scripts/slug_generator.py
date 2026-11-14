#!/usr/bin/env python3
"""remove_duplicate_lines.py - remove duplicate lines, keeping first occurrence.

Usage:
    python remove_duplicate_lines.py input.txt
    python remove_duplicate_lines.py input.txt --out clean.txt
    python remove_duplicate_lines.py input.txt --ignore-case --trim
"""

import argparse
import sys
from pathlib import Path


def dedup(lines, ignore_case=False, trim=False):
    seen = set()
    out = []
    for line in lines:
        key = line
        if trim:
            key = key.strip()
        if ignore_case:
            key = key.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser(description="Remove duplicate lines.")
    ap.add_argument("input", help="input text file")
    ap.add_argument("--out", help="output file (default: print to stdout)")
    ap.add_argument("--ignore-case", action="store_true", help="treat lines differing only by case as duplicates")
    ap.add_argument("--trim", action="store_true", help="ignore leading/trailing whitespace when comparing")
    args = ap.parse_args()

    try:
        text = Path(args.input).read_text(encoding="utf-8")
    except OSError as e:
        print("Error: %s" % e, file=sys.stderr)
        sys.exit(1)

    lines = text.splitlines(keepends=True)
    result_lines = dedup(lines, args.ignore_case, args.trim)
    result = "".join(result_lines)

    if args.out:
        try:
            Path(args.out).write_text(result, encoding="utf-8")
        except OSError as e:
            print("Error: %s" % e, file=sys.stderr)
            sys.exit(1)
        removed = len(lines) - len(result_lines)
        print("Wrote %s (%d duplicates removed)" % (args.out, removed))
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
""" path="C:\x\mm\textkit\scripts\remove_duplicate_lines.py"