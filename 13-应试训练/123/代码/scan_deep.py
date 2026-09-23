# -*- coding: utf-8 -*-
"""Deeper scan: $ balance, raw primes y', raw caret exponents, outside $...$"""
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 13-应试训练
HTMLS = [
    "00-应试总览.html","01-CMC全国大学生数学竞赛.html",
    "02-考研数学-高等数学强化.html","03-考研数学-线性代数与概率强化.html",
    "05-真题模拟卷.html","06-真实单题训练.html","07-题库覆盖与来源.html",
]

def split_outside_math(line):
    """Return list of (is_math, text) segments."""
    segs = []
    # remove $$...$$ first
    parts = re.split(r'(\$\$.*?\$\$)', line, flags=re.S)
    out = []
    for p in parts:
        if p.startswith('$$'):
            out.append((True, p))
        else:
            sub = re.split(r'(\$[^$\n]{1,300}\$)', p)
            for s in sub:
                if s.startswith('$') and s.endswith('$') and len(s) > 1:
                    out.append((True, s))
                else:
                    out.append((False, s))
    return out

for h in HTMLS:
    p = os.path.join(BASE, h)
    with open(p, encoding="utf-8") as f:
        lines = f.readlines()
    print(f"\n===== {h} =====")
    for i, line in enumerate(lines, 1):
        # $ balance per line (crude): count $ not escaped
        cnt = len(re.findall(r'(?<!\\)\$', line))
        if cnt % 2 != 0:
            print(f"  [配对?] L{i}: $ count={cnt} | {line.strip()[:100]}")
        for is_m, seg in split_outside_math(line):
            if is_m: continue
            # raw prime like y' or y'' or f' outside math
            if re.search(r"[yfuxvts]'+'(?![a-zA-Z])", seg):
                # skip if inside english word
                m = re.search(r".{0,15}[yfuxvts]'+'(?![a-zA-Z]).{0,15}", seg)
                if m: print(f"  [裸导数] L{i}: ...{m.group()}...")
            # raw caret exponent
            m = re.search(r".{0,10}[a-zA-Z)\d]\^[\(\da-zA-Z].{0,15}", seg)
            if m and 'http' not in seg and 'src=' not in seg:
                print(f"  [裸^指数] L{i}: ...{m.group()}...")
