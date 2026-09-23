# -*- coding: utf-8 -*-
"""Scan JS question banks for plain-text math outside $...$ delimiters."""
import re, os, json

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    "cmc-真题.js","fdu-真题.js","zsb-真题.js","题库.js",
    "CMC题库.js","题库-汇总.js","真题卷.js","题库-专升本片段.js",
    "试卷清单.js",
]

SUP = set("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ")
# symbols that strongly indicate un-LaTeX'd math (exclude Greek letters that may appear in prose)
RAW_SYM = set("∫∑∏√∂∇∞≈≤≥≠±×÷∈∉⊂⊃∪∩∀∃")

def strip_math(line):
    # remove $$...$$
    line = re.sub(r'\$\$.*?\$\$', '', line)
    # remove $...$ (non-greedy, up to 400 chars, no newline)
    line = re.sub(r'\$[^$\n]{1,400}\$', '', line)
    return line

total = 0
for fn in FILES:
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        print(f"[MISS] {fn}")
        continue
    size = os.path.getsize(p)
    with open(p, encoding="utf-8") as f:
        lines = f.readlines()
    hits = []
    for i, line in enumerate(lines, 1):
        stripped = strip_math(line)
        sups = [c for c in stripped if c in SUP]
        syms = [c for c in stripped if c in RAW_SYM]
        if sups or syms:
            # find context
            ctx = stripped.strip()
            # only flag if it looks like a question content line (has q:/o:/s: or chinese math)
            if any(k in line for k in ['"q"', '"o"', '"s"', '"question"', '"analysis"', '"answer"', '"stem"', '"content"']) or sups or syms:
                tag = []
                if sups: tag.append("上标:"+''.join(sorted(set(sups))))
                if syms: tag.append("裸符号:"+''.join(sorted(set(syms))))
                hits.append((i, "; ".join(tag), ctx[:140]))
    print(f"\n===== {fn} ({size//1024}KB, {len(lines)} lines) hits={len(hits)} =====")
    for i, tag, ctx in hits[:40]:
        print(f"  L{i} [{tag}] {ctx}")
    if len(hits) > 40:
        print(f"  ... ({len(hits)-40} more)")
    total += len(hits)
print(f"\nTOTAL HITS: {total}")
