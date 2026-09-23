# -*- coding: utf-8 -*-
"""
从 tools/bank/*.py 生成 14-自测题库/ 下的 HTML 页面
==================================================
先跑 tools/verify_bank.py 确认全部答案通过，再跑本脚本。
生成前会再验一次，任何一题不通过就中止，避免把没验证的答案写进页面。

用法：python tools/build_bank.py
"""
import html
import importlib.util
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import bank_kit  # noqa: E402

BANK_DIR = os.path.join(HERE, "bank")
OUT_DIR = os.path.join(ROOT, "14-自测题库")
EXAM_DIR = os.path.join(ROOT, "15-应试实战")

# 文件名 -> (输出页序号与标题, 页面导语, 章节图标)
PAGE_META = {
    "01-limits.py":        ("01-极限与连续", "极限与连续", "⟶", "从等价无穷小到夹逼定理，极限题的核心是「先看能不能代入，再看能不能化」。"),
    "02-derivatives.py":   ("02-一元微分学", "一元微分学", "′", "求导本身不难，难的是判断该用哪种方法：对数求导、隐函数、参数方程各有适用场合。"),
    "03-integrals.py":     ("03-一元积分学", "一元积分学", "∫", "积分的技巧全在「凑」：凑微分、凑分部、凑配方。定积分还要善用对称性。"),
    "04-series.py":        ("04-无穷级数", "无穷级数", "∑", "级数先判敛散再求和。收敛半径用比值判别法，求和常靠错位相减与裂项。"),
    "05-odes.py":          ("05-常微分方程", "常微分方程", "∂", "解方程就是「把导数消掉」：能分离就分离，不能分离就找积分因子。"),
    "06-multivariable.py": ("06-多元微积分", "多元微积分", "∇", "多元的关键是化为累次积分并选对坐标系，对称性往往能让积分瞬间归零。"),
    "07-linear-algebra.py":("07-线性代数", "线性代数", "λ", "行列式、秩、特征值是三根支柱；几乎所有结论都能回溯到这三者。"),
    "08-probability.py":   ("08-概率与统计", "概率与统计", "𝔼", "概率题先想对立事件与条件分解，统计题先看估计量是否无偏。"),
    "09-number-theory.py": ("09-数论与组合", "数论与组合", "≡", "同余、计数与恒等式：数论题的答案通常很小，但推到答案的过程很长。"),
}

# 应试实战：按目标考试分册，难度与题型分布对标该考试
EXAM_META = {
    "10-exam-math1.py": ("01-考研数学一", "考研数学一", "Ⅰ",
                         "对标考研数学一的题型分布与难度：高等数学约占 56%，含多元微积分、曲线曲面积分与级数——这正是数一区别于数二的部分；计算量偏大，证明题集中在微分中值定理与级数。"),
    "11-exam-math2.py": ("02-考研数学二", "考研数学二", "Ⅱ",
                         "对标考研数学二：不含无穷级数与概率论，重点为高等数学（约 78%）与线性代数（约 22%）；计算为主，要求步骤稳、算得准。"),
    "12-exam-zb.py":    ("03-专升本", "专升本高等数学", "Z",
                         "对标普通高校专升本高等数学：覆盖面广、计算为主、证明较少，难度大致相当于理工科高数期末的偏易档到中档。"),
    "13-exam-cmc.py":   ("04-数学竞赛", "大学生数学竞赛", "◎",
                         "对标全国大学生数学竞赛非数学类：更依赖巧劲——换元、对称性、夹逼与构造，而非标准套路的堆叠；证明题比重明显高于考研。"),
}

LEVEL_TEXT = {1: "入门", 2: "基础", 3: "进阶", 4: "较难", 5: "挑战"}

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; object-src 'none'">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{{title}} · 自测题库 · LBLB</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2322262B'/%3E%3Ctext x='32' y='46' font-size='34' text-anchor='middle' fill='%23F7F3E7' font-family='Georgia,serif'%3E{{icon}}%3C/text%3E%3C/svg%3E">
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']], processEscapes: true },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] },
  svg: { fontCache: 'local' },
  startup: { typeset: true }
};
</script>
<script src="../assets/mathjax/es5/tex-svg.js" async onerror="var b=document.createElement('div');b.style.cssText='padding:8px 12px;background:#FDEDE8;border:1px solid #EAC6B8;border-radius:8px;color:#C0392B;font-size:13px;margin:10px 0';b.textContent='公式渲染组件加载失败：请确认 ../assets/mathjax/es5/tex-svg.js 存在（本页需与 assets 目录保持原有相对位置）。';document.currentScript.after(b);"></script>
<style>
:root{--paper:#F7F3E7;--paper2:#EFE9D8;--ink:#22262B;--ink2:#4A5258;--line:#D8D0BC;
  --blue:#1F4E9C;--teal:#177E89;--gold:#A8751E;--red:#C0392B;--green:#2E7D5B;--violet:#6B4C9A;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--paper);color:var(--ink);
  font-family:"Times New Roman","Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.8;}
button{font-family:inherit;}
.wrap{max-width:960px;margin:0 auto;padding:0 24px 90px;}
header{padding:52px 0 6px;}
.back{font-size:13px;color:var(--blue);text-decoration:none;}
.back:hover{text-decoration:underline;}
.kicker{font-size:11px;letter-spacing:.32em;color:var(--ink2);text-transform:uppercase;margin-top:22px;}
h1{font-family:Georgia,"Noto Serif SC","Songti SC",serif;font-size:40px;margin:10px 0 8px;}
h1 .sym{color:var(--blue);font-style:italic;}
.sub{color:var(--ink2);font-size:15.5px;max-width:760px;}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;}
.chip{background:#fffdf6;border:1px solid var(--line);border-radius:999px;padding:4px 13px;font-size:12.5px;color:var(--ink2);}
.chip b{color:var(--blue);}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:20px;padding:12px 16px;
  background:#fffdf6;border:1px solid var(--line);border-radius:12px;}
.bar .btn{background:var(--blue);color:#fff;border:none;border-radius:8px;padding:7px 16px;font-size:13.5px;cursor:pointer;min-height:38px;}
.bar .btn.gray{background:#8A8270;}
.bar .note{font-size:12.5px;color:var(--ink2);}
.toc{margin-top:22px;background:#fffdf6;border:1px solid var(--line);border-radius:14px;padding:16px 22px;font-size:14px;}
.toc b{font-size:13.5px;}
.toc ol{margin:8px 0 0 22px;column-count:2;column-gap:30px;}
.toc a{color:var(--blue);text-decoration:none;}
.toc a:hover{text-decoration:underline;}
.toc .tt{color:var(--ink2);font-size:12px;}
.prob{background:#fffdf6;border:1px solid var(--line);border-left:5px solid var(--c,var(--blue));
  border-radius:10px;padding:15px 18px;margin-top:16px;}
.prob .head{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:7px;}
.prob .num{font-family:Georgia,serif;font-weight:700;font-size:15px;color:var(--c,var(--blue));letter-spacing:.04em;}
.prob .lvl{font-size:11.5px;color:var(--gold);letter-spacing:.1em;}
.prob .tags{font-size:11.5px;color:var(--ink2);margin-left:auto;}
.prob .tgt{display:inline-block;font-size:11px;letter-spacing:.06em;color:#fff;background:var(--c,var(--blue));
  border-radius:999px;padding:1px 9px;margin-left:6px;vertical-align:1px;}
.prob .q{font-size:15px;}
.prob details{margin-top:10px;border-top:1px dashed var(--line);padding-top:9px;}
.prob summary{cursor:pointer;font-size:13.5px;color:var(--blue);user-select:none;display:inline-block;padding:3px 0;}
.prob summary:hover{text-decoration:underline;}
.prob .ans{margin-top:9px;font-size:14.5px;}
.prob .ans b{color:var(--green);}
.prob .sol{margin-top:8px;font-size:14px;color:var(--ink2);}
.prob .sol b{color:var(--ink);}
.prob .ver{margin-top:9px;font-size:11.5px;color:var(--ink2);border-top:1px dotted var(--line);padding-top:7px;}
.prob .ver code{background:var(--paper2);border-radius:3px;padding:1px 5px;}
footer{margin-top:50px;border-top:1px solid var(--line);padding-top:18px;font-size:12.5px;color:var(--ink2);}
footer code{background:var(--paper2);border-radius:4px;padding:1px 6px;}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="back" href="index.html">← 返回题库总览</a>
  <div class="kicker">LBLB · Self-Test Problem Bank</div>
  <h1>{{h1}} <span class="sym">{{icon}}</span></h1>
  <p class="sub">{{lead}}</p>
  <div class="stats">{{chips}}</div>
  <div class="bar">
    <button class="btn" id="showAll">展开全部详解</button>
    <button class="btn gray" id="hideAll">收起全部</button>
    <span class="note">共 {{count}} 题 · 每题答案均由 sympy 符号计算验证</span>
  </div>
  <nav class="toc"><b>本页目录</b><ol>{{toc}}</ol></nav>
</header>
{{body}}
<footer>
  本页题目与详解由本库编写，答案经符号计算验证；解题方法不限一种，详解给出的是其中一条思路。<br>
  返回 <a class="back" href="index.html">{{idxname}}</a> ·
  <a class="back" href="../00-总览/index.html">总览</a> ·
  授权见仓库根目录 <code>LICENSE</code>
</footer>
</div>
<script>
(function(){
  var d=document.querySelectorAll('.prob details');
  var s=document.getElementById('showAll'), h=document.getElementById('hideAll');
  if(s) s.onclick=function(){ for(var i=0;i<d.length;i++) d[i].open=true; };
  if(h) h.onclick=function(){ for(var i=0;i<d.length;i++) d[i].open=false; };
})();
</script>
</body>
</html>
"""


def load(path):
    spec = importlib.util.spec_from_file_location(
        "bank_" + os.path.basename(path).replace("-", "_").replace(".py", ""), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def esc(s):
    return html.escape(s or "", quote=False)


def stars(level):
    return "★" * level + "☆" * (5 - level)


def prob_html(p, color):
    """渲染一道题（只排中文）。"""
    tags = esc(" · ".join(p.get("tags", [])))
    target = p.get("target")
    tgt_html = ('<span class="tgt">%s</span>' % esc(target)) if target else ""
    ver = ('%s：<code>%s</code>'
           % (esc(LEVEL_TEXT.get(p.get("level", 3), "")), esc(p["check"])))

    # 只排中文（原先的双语 data-lang 区块已移除）
    q_html = '<div class="q">%s</div>' % p["q"]
    ans_html = '<div class="ans"><b>答案：</b>%s</div>' % p["a"]
    sol_html = '<div class="sol"><b>详解：</b>%s</div>' % p["s"]

    return (
        '<article class="prob" id="%s" style="--c:%s">\n'
        '<div class="head"><span class="num">%s</span>%s'
        '<span class="lvl">%s %s</span>'
        '<span class="tags">%s</span></div>\n'
        '%s\n'
        '<details><summary>查看参考答案与详解</summary>\n'
        '%s\n%s\n'
        '<div class="ver">%s</div>\n'
        '</details>\n</article>'
        % (esc(p["id"]), color, esc(p["id"]), tgt_html,
           stars(p.get("level", 3)), LEVEL_TEXT.get(p.get("level", 3), ""),
           tags, q_html, ans_html, sol_html, ver)
    )


def main():
    files = sorted(f for f in os.listdir(BANK_DIR)
                   if f.endswith(".py") and not f.startswith("_"))
    collected = []
    total = 0

    # 生成前再验一次，不通过就中止
    for fn in files:
        mod = load(os.path.join(BANK_DIR, fn))
        probs = getattr(mod, "PROBLEMS", [])
        ok, fails = bank_kit.verify(probs, fn)
        if fails:
            print("!! %s 有 %d 题未通过验证，中止生成" % (fn, len(fails)))
            return 1
        section = getattr(mod, "SECTION", "core")
        if section not in ("core", "exam"):
            print("!! %s 的 SECTION 取值非法: %r（只允许 core / exam）" % (fn, section))
            return 1
        collected.append((fn, probs, section))
        total += len(probs)
        print("  %-24s %2d 题 全部通过  [%s]" % (fn, len(probs), section))

    COLORS = ["var(--blue)", "var(--teal)", "var(--red)", "var(--gold)",
              "var(--green)", "var(--violet)"]

    grand = 0
    for section, outdir in (("core", OUT_DIR), ("exam", EXAM_DIR)):
        subset = [(fn, pr) for fn, pr, sec in collected if sec == section]
        if not subset:
            continue
        grand += build_section(section, outdir, subset, COLORS)
    print("\n共生成 %d 道题，全部通过 sympy 验证。" % grand)
    return 0


def build_section(section, outdir, subset, COLORS):
    meta = PAGE_META if section == "core" else EXAM_META
    idx_text = IDX_CORE if section == "core" else IDX_EXAM
    os.makedirs(outdir, exist_ok=True)
    index_rows = []
    total = 0

    for gi, (fn, probs) in enumerate(subset):
        page, h1, icon, lead = meta[fn]
        total += len(probs)
        color = COLORS[gi % len(COLORS)]
        body = "\n".join(prob_html(p, COLORS[(gi + i) % len(COLORS)])
                         for i, p in enumerate(probs))
        toc = "\n".join(
            '    <li><a href="#%s">%s</a> <span class="tt">%s</span></li>'
            % (esc(p["id"]), esc(p["id"]),
               esc(p.get("tags", [""])[0] if p.get("tags") else ""))
            for p in probs)
        levels = {}
        for p in probs:
            levels[p.get("level", 3)] = levels.get(p.get("level", 3), 0) + 1
        chips = "".join('<span class="chip">%s <b>%d</b> 题</span>' % (LEVEL_TEXT[k], v)
                        for k, v in sorted(levels.items()))
        tags = sorted({t for p in probs for t in p.get("tags", [])})
        chips += '<span class="chip">知识点 <b>%d</b> 个</span>' % len(tags)

        doc = HEAD
        for k, v in (("title", h1), ("h1", h1), ("icon", icon), ("lead", lead),
                     ("chips", chips), ("count", str(len(probs))),
                     ("toc", toc), ("body", body),
                     ("idxname", "题库总览" if section == "core" else "应试实战总览")):
            doc = doc.replace("{{" + k + "}}", v)
        out = os.path.join(outdir, page + ".html")
        io.open(out, "w", encoding="utf-8", newline="\n").write(doc)
        print("  -> %s (%d 题)" % (os.path.relpath(out, ROOT), len(probs)))

        index_rows.append((page, h1, icon, lead, len(probs), color, tags))

    # 总览页
    cards = []
    for page, h1, icon, lead, cnt, color, tags in index_rows:
        cards.append(
            '<a class="card" style="--c:%s" href="%s.html">'
            '<div class="cardtop"><span class="ic">%s</span><span class="cnt">%d 题</span></div>'
            "<h3>%s</h3><p>%s</p>"
            '<div class="tg">%s</div></a>'
            % (color, page, icon, cnt, esc(h1), esc(lead),
               esc(" · ".join(tags[:8])) + (" 等" if len(tags) > 8 else ""))
        )

    idx = IDX_HEAD
    for k, v in (("cards", "\n".join(cards)), ("total", str(total)),
                 ("topics", str(len(index_rows))),
                 ("idxtitle", idx_text[0]), ("idxkicker", idx_text[1]),
                 ("idxh1", idx_text[2]), ("idxicon", idx_text[3]),
                 ("idxlead", idx_text[4].replace("{{total}}", str(total))
                                          .replace("{{topics}}", str(len(index_rows)))),
                 ("idxnote", idx_text[5])):
        idx = idx.replace("{{" + k + "}}", v)
    io.open(os.path.join(outdir, "index.html"), "w",
            encoding="utf-8", newline="\n").write(idx)
    print("  -> %s/index.html" % os.path.basename(outdir))
    return total


# 两个分区的总览文案：(标题, kicker, h1, 图标, 导语, 说明块)
IDX_CORE = (
    "自测题库",
    "LBLB · Self-Test Problem Bank",
    "自测题库", "✎",
    "共 <b>{{total}}</b> 道题，覆盖 {{topics}} 个主题。每题都给出可直接展开的参考答案与详解，"
    "答案均经 sympy 符号计算验证——不是「看起来对」，而是机器判定为真。",
    "<b>这套题从哪来？</b>题目由本库自行编写，覆盖 9 个知识分支——"
    "因此不涉及真题原卷的著作权问题。想要真题请见 <a href=\"../15-应试实战/index.html\">15-应试实战</a>，"
    "那里按目标考试收录了公开来源的真题。"
    "数学内容本身（定理、方法、恒等式）不受版权保护，可以自由分发。题目中的答案由符号计算逐题校验，"
    "验证表达式就写在每题详解下方，可自行复核。<br>"
    "<b>与 12-高等数学、13-应试训练的分工：</b>12 区是按教材目录组织的讲义，13 区是刷题框架（需自备题库数据），"
    "本区则是可直接练手、自带答案的自测题集。",
)

IDX_EXAM = (
    "应试实战题库",
    "LBLB · Exam-Targeted Practice",
    "应试实战题库", "◎",
    "共 <b>{{topics}}</b> 套、<b>{{total}}</b> 道题，按目标考试分册：考研数学一 / 数学二、专升本、大学生数学竞赛。"
    "每套的题型分布与难度按对应考试的实际情况编排，而不是把同一批题换个标题。",
    "<b>这些题对标真实考试，但不是历年真题。</b>真题原卷的版权属于各命题单位，不能随公开仓库分发；"
    "这里给出的是按考纲范围、题型分布与难度梯度重新编写的题目——<b>数学内容本身不受版权保护</b>，"
    "所以你拿到的是一套难度对得上、可以放心练手的题。"
    "真要练原卷，请用 <a href=\"../13-应试训练/00-应试总览.html\">13-应试训练</a> 的框架接入你自备的题库。<br>"
    "<b>难度怎么标的：</b>每题按 5 级标注，其中「较难」「挑战」两档对应各套考试里的压轴题与拔高题比重。"
    "答案全部经 sympy 符号计算验证，验证表达式印在每题详解下方。",
)


IDX_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; object-src 'none'">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{{idxtitle}} · LBLB</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2322262B'/%3E%3Ctext x='32' y='45' font-size='30' text-anchor='middle' fill='%23F7F3E7' font-family='Georgia,serif'%3E%E2%88%B4%3C/text%3E%3C/svg%3E">
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']], processEscapes: true },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] },
  svg: { fontCache: 'local' },
  startup: { typeset: true }
};
</script>
<script src="../assets/mathjax/es5/tex-svg.js" async onerror="var b=document.createElement('div');b.style.cssText='padding:8px 12px;background:#FDEDE8;border:1px solid #EAC6B8;border-radius:8px;color:#C0392B;font-size:13px;margin:10px 0';b.textContent='公式渲染组件加载失败：请确认 ../assets/mathjax/es5/tex-svg.js 存在（本页需与 assets 目录保持原有相对位置）。';document.currentScript.after(b);"></script>
<style>
:root{--paper:#F7F3E7;--paper2:#EFE9D8;--ink:#22262B;--ink2:#4A5258;--line:#D8D0BC;
  --blue:#1F4E9C;--teal:#177E89;--gold:#A8751E;--red:#C0392B;--green:#2E7D5B;--violet:#6B4C9A;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--paper);color:var(--ink);
  font-family:"Times New Roman","Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.8;}
.wrap{max-width:1040px;margin:0 auto;padding:0 24px 90px;}
header{padding:52px 0 6px;}
.back{font-size:13px;color:var(--blue);text-decoration:none;}
.back:hover{text-decoration:underline;}
.kicker{font-size:11px;letter-spacing:.32em;color:var(--ink2);text-transform:uppercase;margin-top:22px;}
h1{font-family:Georgia,"Noto Serif SC","Songti SC",serif;font-size:42px;margin:10px 0 8px;}
h1 .sym{color:var(--red);font-style:italic;}
.sub{color:var(--ink2);font-size:16px;max-width:800px;}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;}
.chip{background:#fffdf6;border:1px solid var(--line);border-radius:999px;padding:4px 13px;font-size:12.5px;color:var(--ink2);}
.chip b{color:var(--blue);}
.note{margin-top:28px;background:#fffdf6;border:1px solid var(--line);border-left:5px solid var(--gold);
  border-radius:10px;padding:14px 18px;font-size:13.5px;color:var(--ink2);}
.note b{color:var(--ink);}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:15px;margin-top:26px;}
.card{display:block;background:#fffdf6;border:1px solid var(--line);border-top:4px solid var(--c,var(--blue));
  border-radius:12px;padding:16px 18px;text-decoration:none;color:var(--ink);
  transition:transform .12s ease, box-shadow .12s ease;}
.card:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(34,38,43,.10);}
.cardtop{display:flex;align-items:baseline;justify-content:space-between;}
.card .ic{font-family:Georgia,serif;font-size:23px;color:var(--c,var(--blue));}
.card .cnt{font-size:11.5px;color:var(--ink2);letter-spacing:.08em;}
.card h3{font-family:Georgia,"Noto Serif SC",serif;font-size:18px;margin:6px 0 5px;}
.card p{font-size:13px;color:var(--ink2);line-height:1.65;}
.card .tg{margin-top:10px;font-size:11px;color:var(--c,var(--blue));letter-spacing:.03em;}
footer{margin-top:50px;border-top:1px solid var(--line);padding-top:18px;font-size:12.5px;color:var(--ink2);}
footer code{background:var(--paper2);border-radius:4px;padding:1px 6px;}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="back" href="../00-总览/index.html">← 返回总览</a>
  <div class="kicker">{{idxkicker}}</div>
  <h1>{{idxh1}} <span class="sym">{{idxicon}}</span></h1>
  <p class="sub">{{idxlead}}</p>
  <div class="stats">
    <span class="chip">主题 <b>{{topics}}</b> 个</span>
    <span class="chip">题目 <b>{{total}}</b> 道</span>
    <span class="chip">难度 <b>5</b> 级标注</span>
    <span class="chip">验证 <b>sympy</b></span>
  </div>
  <div class="note">{{idxnote}}</div>
</header>
<div class="grid">
{{cards}}
</div>
<footer>
  题目与详解由本库编写，授权见仓库根目录 <code>LICENSE</code>（内容 CC BY-NC-SA 4.0）。<br>
  <a class="back" href="../00-总览/index.html">← 返回总览</a> ·
  <a class="back" href="../12-高等数学/07-速查与题库.html">配套：高数速查与题库 →</a>
</footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
