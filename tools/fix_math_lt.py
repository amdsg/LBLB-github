# -*- coding: utf-8 -*-
"""找出 HTML 里数学公式中未转义的 `<`（后跟字母）。

浏览器看到 `$P(a<X<b)$` 会把 `<X<b)$` 当标签吃掉，MathJax 于是收到一个没配对的 `$`，
整段公式变成原样文字。修法是写成 `&lt;`。

用法：
    python tools/fix_math_lt.py            # 只报告
    python tools/fix_math_lt.py --fix      # 就地替换
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"assets", ".git", "docs", "node_modules"}

# 数学区间内出现 <字母，且中间没有 `>`（真标签必然带 `>`）→ 一定是被浏览器吃掉的写法
BUG = re.compile(r"\$[^$>]{0,400}?<[A-Za-z][^$>]{0,400}?\$")
STRIP = re.compile(r"<(script|style|pre|code|textarea)\b[\s\S]*?</\1>", re.I)


def sites(text):
    """返回 [(pos, snippet)]，pos 是那个 `<` 的位置。

    一个片段里可能不止一处（`$P(a<X<b)$` 就有两处），所以逐个 `<` 都收。
    """
    out = []
    for m in BUG.finditer(text):
        span, base = m.group(0), m.start()
        for mm in re.finditer(r"<[A-Za-z]", span):
            lt = base + mm.start()
            if text[max(0, lt - 3):lt].endswith("&"):
                continue
            if text[max(0, lt - 1):lt] == "\\":
                continue
            out.append((lt, text[max(0, lt - 45):lt + 55].replace("\n", " ")))
    return out


def main():
    fix = "--fix" in sys.argv
    total = 0
    pages = 0
    changed = 0
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if not f.lower().endswith(".html"):
                continue
            p = os.path.join(dp, f)
            text = open(p, encoding="utf-8").read()
            masked = STRIP.sub(lambda m: " " * len(m.group(0)), text)
            hits = sites(masked)
            if not hits:
                continue
            pages += 1
            total += len(hits)
            rel = os.path.relpath(p, ROOT)
            print("\n[%s]  %d 处" % (rel, len(hits)))
            for pos, frag in hits[:5]:
                print("    ...%s..." % frag)
            if len(hits) > 5:
                print("    ... 另 %d 处" % (len(hits) - 5))
            if fix:
                chars = list(text)
                for pos, _ in hits:
                    chars[pos] = "&lt;"
                open(p, "w", encoding="utf-8", newline="").write("".join(chars))
                changed += 1

    print("\n合计：%d 个页面，%d 处；%s" % (pages, total, "已修复 %d 页" % changed if fix else "（未改动）"))


if __name__ == "__main__":
    main()
