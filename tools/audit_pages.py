# -*- coding: utf-8 -*-
"""
LBLB 页面审计工具
==================
对仓库内所有 HTML 页面做静态体检，找出：结构性缺陷、公式定界问题、
章节编号乱序、内部链接失效、疑似未用 LaTeX 的数学记号。

用法（在仓库根目录执行）：
    python tools/audit_pages.py                  # 审计全部页面
    python tools/audit_pages.py --section 12-高等数学
    python tools/audit_pages.py --only structure # 只看结构类问题

设计说明：
- 只读，不修改任何文件。
- 本项目有意在中文散文里使用 Unicode 数学记号（√2、H ≤ G、x²、aₙ、⟹），
  这是排版选择，不算缺陷；本工具只在下列情形报告：
    * 出现 **字面** 的 `^` 上标或 `'` 撇号（会原样显示成 x^2 / y''）
    * 出现 `∫_0^{...}` 这类**纯文本积分记号**（应写成 LaTeX）
    * `$` 定界符未配对（会让 MathJax 吞掉后续内容）
- 「输入类」文本（提示往 Desmos / Wolfram 里敲什么）里的 ^ 与 ' 是正确的，
  通过行内含 INPUT_HINTS 关键词豁免。
"""
import os
import re
import sys
import argparse
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"assets", ".git", "docs", "node_modules"}

# 出现这些词的行属于「照抄输入」语境，^ 与 ' 是正确写法
INPUT_HINTS = ("输入", "desmos", "wolfram", "alpha", "计算器", "验证", "敲", "搜索框", "站内")

# 块级边界：定界符只在一个块内配对（MathJax 的 findTeX 不会跨块把两个 $$ 配成一对，
# 否则正文里一处漏写的 $$ 会吞掉后面整段，甚至与远处的 $$ 误配而看不出问题）。
BLOCK_SPLIT = re.compile(
    r"(?is)<(?:/?(?:p|div|li|td|th|h[1-6]|tr|table|ul|ol|dl|dd|dt|section|article"
    r"|main|header|footer|aside|blockquote|figure|figcaption)\b[^>]*|br\s*/?)>"
)

# 纯文本数学记号：应改成 LaTeX 的强信号
PLAINTEXT_MATH = [
    (r"[∫∮∑∏]\s*_[\{\d]", "纯文本积分/求和上下标"),
    (r"[∫∮]\s*\d*\^?[\{\(]", "纯文本积分号"),
    (r"\b[a-zA-Z]\s*\^\s*[\{\(\d]", "字面上标 ^"),
    (r"[a-zA-Z]\s*''(?![a-zA-Z])", "字面双撇号"),
]

STRUCT_KEYS = ("缺少 title", "缺少 viewport", "缺少 lang", "页面内容过短", "章节编号不单调")
FORMULA_KEYS = ("公式定界符未配对", "纯文本积分/求和上下标", "纯文本积分号", "字面上标 ^", "字面双撇号")
LINK_KEYS = ("引用不存在",)


def iter_pages(section=None):
    base = os.path.join(ROOT, section) if section else ROOT
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if fn.lower().endswith(".html"):
                yield os.path.join(dirpath, fn)


def strip_scripts(text):
    return re.sub(r"<(script|style)\b[\s\S]*?</\1>", " ", text, flags=re.I)


# 只删「真的是标签」的东西：HTML 规范里标签名首字符必须是字母 / ! / ? / 。
# 若写成 <[^>]+>，公式里的 `$|x|<1$` 会被当成标签删掉一大段，反而制造假警报。
def strip_tags(text):
    return re.sub(r"<[/!?]?[A-Za-z][^>]*>", " ", text)


def math_segments(line):
    """把一行切成 (是否数学模式, 片段)。"""
    out = []
    for part in re.split(r"(\$\$[\s\S]*?\$\$)", line):
        if part.startswith("$$") and part.endswith("$$") and len(part) > 4:
            out.append((True, part))
            continue
        for sub in re.split(r"(\$[^$\n]{1,400}\$)", part):
            if len(sub) > 2 and sub.startswith("$") and sub.endswith("$"):
                out.append((True, sub))
            else:
                out.append((False, sub))
    return out


def unescape_entities(s):
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"')):
        s = s.replace(a, b)
    return s


def plain_text(html):
    s = strip_scripts(html)
    s = strip_tags(s)
    return unescape_entities(s)


def check_structure(path, text, stats):
    issues = []
    if "<title>" not in text:
        issues.append(("缺少 title", 0, ""))
    # 注意子串陷阱：废弃写法 http-equiv="X-Content-Security-Policy" 里也含有
    # "Content-Security-Policy"，直接子串匹配会把它误判为已具备。
    if 'http-equiv="Content-Security-Policy"' not in text:
        issues.append(("缺少 CSP（或用了已废弃的 X-Content-Security-Policy）", 0, ""))
    if "viewport" not in text:
        issues.append(("缺少 viewport", 0, ""))
    if not re.search(r"<html[^>]*\slang=", text, re.I):
        issues.append(("缺少 lang", 0, ""))
    if len(plain_text(text).strip()) < 400:
        issues.append(("页面内容过短", 0, "%d 字符" % len(plain_text(text).strip())))

    nums = []
    for h in re.findall(r"<h2[^>]*>([\s\S]{0,140}?)</h2>", text):
        m = re.match(r"\s*(\d+)\s*[a-z伴]?\s*[\.、\s]", plain_text(h).strip())
        if m:
            nums.append(int(m.group(1)))
    if len(nums) >= 4:
        drops = [i for i in range(1, len(nums)) if nums[i] < nums[i - 1]]
        if drops:
            issues.append(("章节编号不单调", 0, "顺序=%s 断裂=%s" % (nums, drops)))
    return issues


def find_unpaired(plain):
    """从左到右配对 $ / $$，返回配对不上的位置片段（模拟 MathJax 的 findTeX）。

    与逐行数数相比，这个做法能发现「写了 $$ 却没写收尾」的情况——逐行法会把
    行内孤立的 $$ 先删掉，正好漏掉这一类。
    """
    i, n, left = 0, len(plain), []
    while i < n:
        c = plain[i]
        if c == "\\":                      # 反斜杠转义（processEscapes）
            i += 2
            continue
        if c == "$":
            if plain.startswith("$$", i):
                j = plain.find("$$", i + 2)
                if j < 0:
                    left.append(plain[max(0, i - 60):i + 80])
                    break
                i = j + 2
            else:
                j = plain.find("$", i + 1)
                if j < 0:
                    left.append(plain[max(0, i - 60):i + 80])
                    break
                i = j + 1
            continue
        i += 1
    return left


def check_formulas(path, text):
    issues = []
    body = strip_scripts(text)
    search = 0
    for block in BLOCK_SPLIT.split(body):
        start = body.find(block, search)
        search = start + len(block) if start >= 0 else search
        plain = unescape_entities(strip_tags(block))
        if "$" not in plain:
            continue
        line = body.count("\n", 0, max(0, start)) + 1
        for frag in find_unpaired(plain):
            issues.append(("公式定界符未配对", line, frag.strip()[:110]))

    for i, line in enumerate(body.splitlines(), 1):
        low = line.lower()
        if any(h in low for h in INPUT_HINTS):
            continue
        for is_math, seg in math_segments(line):
            if is_math:
                continue
            for pat, label in PLAINTEXT_MATH:
                m = re.search(pat, seg)
                if m:
                    issues.append((label, i, seg.strip()[:110]))
                    break
    return issues


def check_links(path, text):
    issues = []
    d = os.path.dirname(path)
    for m in re.finditer(r'(?:src|href)\s*=\s*"([^"]+)"', text):
        u = m.group(1)
        if re.match(r"^(?:https?:|data:|mailto:|#|javascript:|\s*$)", u):
            continue
        if re.search(r"'\s*\+|\+\s*'", u):
            continue
        p = u.split("#")[0].split("?")[0]
        if not p:
            continue
        if not os.path.exists(os.path.normpath(os.path.join(d, p.replace("/", os.sep)))):
            issues.append(("引用不存在", 0, u))
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section")
    ap.add_argument("--only", choices=["structure", "formula", "link"], default=None)
    args = ap.parse_args()

    report = defaultdict(list)
    totals = Counter()
    pages = list(iter_pages(args.section))
    for p in pages:
        rel = os.path.relpath(p, ROOT)
        text = open(p, encoding="utf-8").read()
        found = []
        if args.only in (None, "structure"):
            found += check_structure(p, text, None)
        if args.only in (None, "formula"):
            found += check_formulas(p, text)
        if args.only in (None, "link"):
            found += check_links(p, text)
        for kind, line, frag in found:
            report[rel].append((kind, line, frag))
            totals[kind] += 1

    print("=" * 74)
    print("审计范围：%s    页面数：%d" % (args.section or "全仓库", len(pages)))
    print("=" * 74)
    print("\n问题统计：")
    if not totals:
        print("  未发现问题")
    for k, v in totals.most_common():
        print("  %-26s %d" % (k, v))

    if report:
        print("\n分页明细：")
        for rel in sorted(report):
            print("\n  [%s]" % rel)
            shown = Counter()
            for kind, line, frag in report[rel]:
                shown[kind] += 1
                if shown[kind] > 5:
                    continue
                loc = ("L%-5d" % line) if line else "      "
                print("      %-26s %s %s" % (kind, loc, frag))
            for kind, c in shown.items():
                if c > 5:
                    print("      %-26s ... 共 %d 处" % (kind, c))
    print("\n完成。")


if __name__ == "__main__":
    main()
