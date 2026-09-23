# -*- coding: utf-8 -*-
"""Scan HTML entry pages for plain-text math expressions outside $...$ delimiters."""
import re, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 13-应试训练
HTMLS = [
    "00-应试总览.html",
    "01-CMC全国大学生数学竞赛.html",
    "02-考研数学-高等数学强化.html",
    "03-考研数学-线性代数与概率强化.html",
    "05-真题模拟卷.html",
    "06-真实单题训练.html",
    "07-题库覆盖与来源.html",
]

# Unicode superscript chars
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ"
# Raw math symbols that usually indicate un-LaTeX'd formulas
MATH_SYM = "∫∑∏√∂∇∞≈≤≥≠±×÷∈∉⊂⊃∪∩∀∃αβγδεζηθικλμνξοπρστυφχψω"

def strip_math(text):
    """Remove $...$ and $$...$$ segments so we only inspect plain text."""
    # remove display math
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.S)
    # remove inline math
    text = re.sub(r"\$[^$\n]{1,200}\$", "", text, flags=re.S)
    # remove \[...\] and \(...\)
    text = re.sub(r"\\\[(.*?)\\\]", "", text, flags=re.S)
    text = re.sub(r"\\\((.*?)\\\)", "", text, flags=re.S)
    return text

for h in HTMLS:
    p = os.path.join(BASE, h)
    if not os.path.exists(p):
        print(f"[MISS] {h}")
        continue
    with open(p, encoding="utf-8") as f:
        lines = f.readlines()
    print(f"\n===== {h} ({len(lines)} lines) =====")
    # balance check for $
    for i, line in enumerate(lines, 1):
        # skip script/style lines roughly
        stripped = strip_math(line)
        issues = []
        # unicode superscripts
        sups = [c for c in stripped if c in SUP]
        if sups:
            issues.append(f"Unicode上标: {''.join(sups)}")
        # raw math symbols (but skip lines that are pure CSS/JS)
        syms = [c for c in stripped if c in MATH_SYM]
        if syms:
            # dedupe
            issues.append(f"裸符号: {''.join(sorted(set(syms)))}")
        # raw caret exponent: e^ or )^ or digit^ or letter^ followed by digit/letter/(
        if re.search(r"[a-zA-Z)\d]\^[\(\d]", stripped):
            issues.append("疑似^指数")
        if issues:
            snippet = stripped.strip()[:120]
            print(f"  L{i}: {'; '.join(issues)} | {snippet}")
