# -*- coding: utf-8 -*-
"""
把正文里的「纯文本数学记号」转换为 LaTeX（$...$）
==================================================
背景：本仓库大多数页面用 $...$ 写 LaTeX 由 MathJax 排版，但 02/12 等分区里
夹杂着 e^(iπ)、∫_0^1、∮_{|z|=2} 这类纯文本写法，会原样显示成 ^ 和 _，与
其余内容排版不一致。

做法：只处理「文本节点」，跳过 <script>/<style>、标签属性、以及已经在
$...$ / $$...$$ 里的内容；只匹配边界明确的模式，宁可漏改也不误改。

用法：
    python tools/fix_plaintext_math.py            # 干跑，只报告
    python tools/fix_plaintext_math.py --apply    # 实际写入
    python tools/fix_plaintext_math.py --apply --section 12-高等数学
"""
import argparse
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"assets", ".git", "docs", "tools", "node_modules", "14-自测题库"}

# Unicode 上下标 → LaTeX
SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6",
       "⁷": "7", "⁸": "8", "⁹": "9", "ⁿ": "n", "⁺": "+", "⁻": "-", "ᵏ": "k",
       "ᵖ": "p", "ᵐ": "m", "ᵢ": "i", "ᵣ": "r", "ᵈ": "d", "ᵉ": "e", "ᵃ": "a",
       "ᵇ": "b", "ˣ": "x", "ʸ": "y"}
SUB = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6",
       "₇": "7", "₈": "8", "₉": "9", "ₙ": "n", "ₐ": "a", "ₘ": "m", "ₖ": "k",
       "ᵢ": "i", "ⱼ": "j", "ᵣ": "r", "ₓ": "x", "ᵨ": "p"}

DELIM = "，。；：、（）()<>「」【】\"' \t\n"


# 运算符 → LaTeX 命令（放在 $...$ 内由 MathJax 排版）
OP_LATEX = {
    "∫": r"\int ", "∮": r"\oint ", "∬": r"\iint ", "∭": r"\iiint ",
    "Σ": r"\sum ", "∏": r"\prod ",
}


# 形如 ^(...) / _(...) 的 ASCII 写法，需转成 LaTeX 的 ^{...}。
# 用平衡括号匹配，因为内容里可能嵌套括号（如 e^(i·(ln 1 + iπ/2))）。
def _ascii_sup_sub(s):
    for sigil, cmd in (("^", "^"), ("_", "_")):
        out = []
        i = 0
        n = len(s)
        while i < n:
            if s[i] == sigil and i + 1 < n and s[i + 1] == "(":
                depth = 0
                j = i + 1
                while j < n:
                    if s[j] == "(":
                        depth += 1
                    elif s[j] == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                if j < n:
                    out.append("%s{%s}" % (cmd, s[i + 2:j]))
                    i = j + 1
                    continue
            out.append(s[i])
            i += 1
        s = "".join(out)
    return s


def norm_unicode_math(s):
    """把 Unicode 上下标、运算符与常见符号换成 LaTeX 写法（用于确定在数学环境内的片段）。"""
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in SUP:
            run = ""
            while i < len(s) and s[i] in SUP:
                run += SUP[s[i]]
                i += 1
            out.append("^{%s}" % run)
            continue
        if ch in SUB:
            run = ""
            while i < len(s) and s[i] in SUB:
                run += SUB[s[i]]
                i += 1
            out.append("_{%s}" % run)
            continue
        if ch == "∞":
            out.append(r"\infty ")
            i += 1
            continue
        if ch in OP_LATEX:
            out.append(OP_LATEX[ch])
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


# 数学函数名 → LaTeX 命令（仅在 wrap 内部执行，避免动到正文里的英文词）
FUNCS = ["arctan", "arcsin", "arccos", "sinh", "cosh", "tanh",
         "sin", "cos", "tan", "cot", "sec", "csc",
         "ln", "log", "lim", "max", "min", "exp", "det", "sup", "inf"]


def _latex_funcs(s):
    for name in FUNCS:
        s = re.sub(r"(?<![\\A-Za-z])%s(?![A-Za-z])" % name, r"\\" + name, s)
    return s


def _latex_sqrt(s):
    """√(...) → \\sqrt{...}（平衡括号）；√X → \\sqrt{X}。"""
    out = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] == "√" and i + 1 < n and s[i + 1] == "(":
            depth = 0
            j = i + 1
            while j < n:
                if s[j] == "(":
                    depth += 1
                elif s[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j < n:
                out.append(r"\sqrt{%s}" % s[i + 2:j])
                i = j + 1
                continue
        if s[i] == "√" and i + 1 < n and (s[i + 1].isalnum()):
            out.append(r"\sqrt{%s}" % s[i + 1])
            i += 2
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def _latex_diff(s):
    r"""微分项排版：dx → \,dx（LaTeX 惯例，$d$ 用正体并加细空格）。"""
    return re.sub(r"(?<![A-Za-z\\])d([a-zA-Z])(?![A-Za-z])", r"\\,d\1", s)


def wrap(inner):
    """把一段纯文本数学收进 $...$，并做 Unicode 与 ASCII 记号的归一化。"""
    body = norm_unicode_math(inner)
    body = body.replace("−", "-")           # Unicode 减号 → LaTeX 减号
    body = _ascii_sup_sub(body)             # e^(iπ) → e^{iπ}，a_(n+1) → a_{n+1}
    body = _latex_sqrt(body)                # √(1−x²) → \sqrt{1-x^{2}}
    body = _latex_funcs(body)               # ln x → \ln x
    body = _latex_diff(body)                # dx → \,dx
    body = re.sub(r"\^\{([^{}]*)\}", r"^{\1}", body)
    body = re.sub(r"_\{([^{}]*)\}", r"_{\1}", body)
    body = re.sub(r"\s+", " ", body).strip()
    if not body or body.startswith("$") or body.endswith("$"):
        return inner
    return "$%s$" % body


PATTERNS = [
    # e^(iπ)  a^(p−1)  x^(1/n)  e^(i·(ln 1 + iπ/2))  ← 允许一层嵌套括号
    ("上标带括号", re.compile(
        r"(?<![\w$])([A-Za-z]|[A-Za-z][A-Za-z0-9]{0,3})\^"
        r"(\([^()]*(?:\([^()]*\)[^()]*)*\))"),
     lambda m: wrap("%s^%s" % (m.group(1), m.group(2)))),
    # a^d  x^y  n^2（单个字母/数字作指数）
    ("上标单字符", re.compile(r"(?<![\w$])([A-Za-z])\^([A-Za-z0-9](?![\w(]))"),
     lambda m: wrap("%s^%s" % (m.group(1), m.group(2)))),
    # ∮_{|z|=2}   ∬_D   ∭_V
    ("积分号带限", re.compile(r"([∮∬∭])_(\{[^}]{1,20}\}|[A-Za-z0-9])"),
     lambda m: wrap("%s_%s" % (m.group(1), m.group(2)))),
    # ∫_0^1  ∫₀^∞  ∫_{−π}^π
    #
    # 只包装「积分号 + 上下限」，被积函数留在正文里。这样渲染出来是 ∫₀¹ 后面跟
    # 正常字体的被积函数，虽然不如整式放进 $...$ 好看，但绝不会把句子成分
    # 误当成公式吃掉——早先尝试捕获到句末的版本会把 "]′ = f(x)" 也圈进去。
    ("定积分带限", re.compile(
        r"∫(_(?:\{[^}]{1,20}\}|[0-9A-Za-zπ∞₀-₉]+)\^(?:\{[^}]{1,20}\}|[0-9A-Za-zπ∞⁰-⁹]+))"),
     lambda m: wrap("∫%s" % m.group(1))),
    # Σ_{n=1}^∞ 之类带限的求和
    ("求和号带限", re.compile(
        r"[Σ∏](_\{[^}]{1,20}\}\^\{[^}]{1,20}\}|_[0-9A-Za-z]\^[0-9A-Za-z∞])"),
     lambda m: wrap("Σ%s" % m.group(1))),
    # 正文里已经写成 ^{...} 的上标（如 x^{1−p}），连同算式一起收进 $...$
    ("花括号上标", re.compile(
        r"(?<![\w$])([A-Za-z0-9])\^\{([^{}]{1,20})\}"),
     lambda m: wrap("%s^{%s}" % (m.group(1), m.group(2)))),
    # 不定积分：以 dx / dz / dt / dσ 等微分项为结束标志，边界比「到句末」可靠得多
    ("积分到微分项", re.compile(
        r"∫((?:[^∫∮∬∭，。；：、<>]|\^\{[^}]*\}|_\{[^}]*\}){1,60}?d[a-zA-Z]\b)"),
     lambda m: wrap("∫%s" % m.group(1))),
]

MATH_SPLIT = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]{1,400}\$)")
TAG_SPLIT = re.compile(r"(<[^>]*>)")
# code/pre 不参与转换：MathJax 的 skipHtmlTags 会跳过这些标签，
# 在其中插入 $...$ 只会让读者看到原始美元符号，反而更糟。
PROTECT = re.compile(r"<(script|style|code|pre)\b[\s\S]*?</\1>", re.I)


def transform_text(text):
    """对一段纯文本做替换，返回 (新文本, 替换次数)。"""
    n = 0
    for _name, pat, fn in PATTERNS:
        def sub(m):
            nonlocal n
            n += 1
            return fn(m)
        text = pat.sub(sub, text)
    return text, n


def transform_segment(seg):
    """一段非标签文本：跳过已在 $...$ 内的部分。"""
    out = []
    total = 0
    for part in MATH_SPLIT.split(seg):
        if part.startswith("$"):
            out.append(part)
            continue
        new, c = transform_text(part)
        total += c
        out.append(new)
    return "".join(out), total


def process_file(path, apply_changes=False):
    src = io.open(path, encoding="utf-8").read()
    # 先把 script/style 整块挖出来保护起来
    protected = []

    def stash(m):
        protected.append(m.group(0))
        return "\x00PROT%d\x00" % (len(protected) - 1)

    work = PROTECT.sub(stash, src)
    pieces = TAG_SPLIT.split(work)
    total = 0
    out = []
    for p in pieces:
        if p.startswith("<") and p.endswith(">"):
            out.append(p)
            continue
        if p.startswith("\x00PROT"):
            out.append(p)
            continue
        new, c = transform_segment(p)
        total += c
        out.append(new)
    res = "".join(out)

    def unstash(m):
        return protected[int(m.group(1))]

    res = re.sub(r"\x00PROT(\d+)\x00", unstash, res)

    if total and apply_changes:
        io.open(path, "w", encoding="utf-8", newline="\n").write(res)
    return total, src != res


def iter_pages(section=None):
    base = os.path.join(ROOT, section) if section else ROOT
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if f.lower().endswith(".html"):
                yield os.path.join(dp, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--section")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    grand = 0
    touched = 0
    for p in iter_pages(args.section):
        n, changed = process_file(p, args.apply)
        if n:
            rel = os.path.relpath(p, ROOT)
            if args.verbose or not args.apply:
                print("  %-46s %3d 处" % (rel, n))
            grand += n
            touched += 1

    mode = "已写入" if args.apply else "干跑（未写入）"
    print("\n%s：%d 个文件，共 %d 处替换" % (mode, touched, grand))
    if not args.apply and grand:
        print("确认无误后加 --apply 实际写入。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
