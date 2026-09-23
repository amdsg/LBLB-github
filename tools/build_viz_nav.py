# -*- coding: utf-8 -*-
"""
生成 05-可视化/可视化导航.html
=============================
原先该文件是一份纯文本转储（无任何 HTML 标签、无链接），
而 36 个可视化页面都写着「← 返回可视化」指向它，导致导航死循环。
本脚本按仓库既有设计语言生成一个带卡片链接的导航页。

用法：python tools/build_viz_nav.py
"""
import os
import sys
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIZ_DIR = os.path.join(ROOT, "05-可视化")
OUT = os.path.join(VIZ_DIR, "可视化导航.html")

# (分类标题, 分类说明, [(文件名, 卡片标题, 一句话描述, 标签)])
GROUPS = [
    (
        "分形与动力系统",
        "自相似、迭代与混沌：一条简单规则重复下去能长出什么",
        [
            ("Julia集.html", "Julia 集", "固定复数 $c$，平面每点反复迭代 $z\\leftarrow z^2+c$：不逃逸的点染成黑色，换一个 $c$，形状天差地别。", "分形 · 复迭代"),
            ("巴恩斯利蕨.html", "巴恩斯利蕨", "四条仿射变换按概率随机选用，迭代几百万次——一株由纯粹随机数长成的自相似蕨。", "分形 · IFS"),
            ("分形树.html", "分形树", "末端长出两根略短略偏的枝再递归重复；调分叉角与缩放比，松柏、垂柳、仙人掌次第出现。", "分形 · 递归"),
            ("复平面映射z→zⁿ.html", "复平面映射 z ↦ zⁿ", "极坐标一眼看穿：模长 $r\\mapsto r^n$、辐角 $\\theta\\mapsto n\\theta$，圆映成圆、射线被抻成 $n$ 倍角的射线。", "复分析 · 映射"),
            ("科赫雪花.html", "科赫雪花", "每段中段换成小三角凸起，无限重复：周长趋于无穷而面积有限，维数约 1.262。", "分形 · 维数"),
            ("曼德博集合-交互版.html", "曼德博集合 · 交互版", "滚轮以光标为中心缩放、拖拽平移、双击复位，钻进迷你心脏线看自相似层层嵌套。", "分形 · 交互"),
            ("曼德博集合.html", "曼德博集合", "从 $z_0=0$ 反复迭代 $z\\leftarrow z^2+c$，永不逃逸的 $c$ 属于集合；点击任意位置放大 2 倍看无尽边界。", "分形 · 复数"),
            ("谢尔宾斯基三角.html", "谢尔宾斯基三角", "不断挖去中心小三角，任何尺度都长得一样，Hausdorff 维数约 1.585，不是整数。", "分形 · 自相似"),
            ("洛伦兹吸引子.html", "洛伦兹吸引子", "三个大气方程，却得到一只绕两翼永转、永不重复相交的蝴蝶；可拖拽旋转视角。", "动力 · 吸引子"),
            ("双摆混沌.html", "双摆混沌", "没有外力却翻跟头永不重复；两个初值只差百万分之一的双摆，几秒后天壤之别。", "混沌 · 蝴蝶效应"),
            ("相空间摆.html", "相空间摆", "把角度 $\\theta$ 与角速度 $\\omega$ 画成状态点：低能量是闭合椭圆，越过红线就翻着圈走。", "动力 · 相图"),
            ("逻辑斯蒂分叉图.html", "逻辑斯蒂分叉图", "$x\\leftarrow r\\,x(1-x)$：横轴放参数 $r$、纵轴放长期轨道，从一条线周期倍增通向混沌雾。", "混沌 · 分叉"),
            ("混沌与分叉.html", "混沌与分叉", "逻辑斯蒂映射只有一行，却产生稳定、周期倍增与混沌；1975 年后走进主流研究。", "动力系统 · 混沌"),
        ],
    ),
    (
        "概率统计与数值分析",
        "随机性如何被驯服成规律，以及用有限步骤逼近连续对象",
        [
            ("大数定律-骰子试验.html", "大数定律 · 骰子试验", "前几十次均值上蹿下跳，一直掷下去必然稳落期望附近——偶然被无限次重复驯服成必然。", "概率 · 大数定律"),
            ("中心极限定理.html", "中心极限定理", "无论原分布多歪斜，样本量够大时均值总长成正态钟形；拖动 $n$、换源头分布亲眼看它圆起来。", "统计 · 极限"),
            ("蒲丰投针求π.html", "蒲丰投针求 π", "1777 年蒲丰：等距平行线间随机扔一根针，它压线的概率里竟藏着 $\\pi$；扔得越多估计越逼近。", "概率 · 几何概型"),
            ("蒙特卡洛求π.html", "蒙特卡洛求 π", "往 $2\\times2$ 正方形里随机撒点，数落在内切圆里的比例——点够多时，$\\pi$ 从随机中浮现。", "概率 · 随机"),
            ("正态分布拟合.html", "正态分布拟合", "真实数据来自一条看不见的钟形，用样本均值 $\\hat\\mu$、标准差 $\\hat\\sigma$ 把它重新画出来，样本越多越逼近。", "统计 · 拟合"),
            ("随机游走2D.html", "二维随机游走", "醉汉每步朝随机方向走一格，没有目标却有确定规律：走 $N$ 步后与起点的典型距离约为 $\\sqrt N$。", "概率 · 随机游走"),
            ("马尔可夫链状态转移.html", "马尔可夫链状态转移", "明天是否下雨只取决于今天——无记忆性的马氏链，随时间演化收敛到与起点无关的平稳分布。", "概率 · 马氏链"),
            ("傅里叶级数.html", "傅里叶级数", "一串匀速旋转的圆周（本轮）叠加起来，竟能画出方波与三角波——项数越多越像。", "分析 · 动画"),
            ("傅里叶级数叠加.html", "傅里叶级数叠加", "周期波形拆成无穷多条正弦波，只取前 $N$ 条叠加——方波由纯音画出，跳变处永远甩不掉小过冲。", "分析 · 逼近"),
            ("泰勒展开逼近.html", "泰勒展开逼近", "用一条多项式去贴曲线：展开点附近贴合，越远越走样；拖动阶数 $n$，看它一级级吞掉原函数。", "分析 · 逼近"),
            ("黎曼和与梯形法.html", "黎曼和与梯形法", "积分就是曲线下面积，把区间切成 $n$ 块用矩形或梯形近似；拖动 $n$ 看近似值收敛到真值。", "数值 · 积分"),
            ("梯度下降可视化.html", "梯度下降可视化", "站在 loss 山坡沿最陡方向迈步：学习率太小走得慢，太大直接飞过谷底——拖动 $\\eta$ 亲自试。", "优化 · 梯度"),
        ],
    ),
    (
        "数论 · 几何 · 图论 · 线代",
        "离散结构里的模式：素数、铺砌、图与线性变换",
        [
            ("埃拉托斯特尼筛法.html", "埃拉托斯特尼筛法", "约公元前 240 年的素数渔网：发现一个素数就划掉它的所有倍数，剩下的全是素数。", "数论 · 筛法"),
            ("欧拉φ函数与模表.html", "欧拉 φ 函数与模表", "$\\varphi(n)$ 等于 $1\\dots n$ 中与 $n$ 互素的个数，也就是模 $n$ 乘法群里可逆元素的数量。", "数论 · 模群"),
            ("帕斯卡三角模素数染色.html", "帕斯卡三角模素数染色", "组合数对素数 $p$ 取余并染色：模 2 就是 Sierpinski 三角，模 3、模 7 是更精细的自相似分形。", "数论 · 模运算"),
            ("素数螺旋.html", "Ulam 素数螺旋", "自然数排成螺旋，素数竟常排出神秘对角线——1963 年的草稿发现，至今没人完全解释为什么。", "数论 · 模式"),
            ("黄金比例斐波那契螺线.html", "黄金比例与斐波那契螺线", "边长按 $1,1,2,3,5,8\\dots$ 拼出正方形，依次接四分之一圆弧，逼近那条传说中的黄金螺线。", "数论 · 螺线"),
            ("彭罗斯铺砌.html", "彭罗斯铺砌", "只用胖、瘦两种菱形却永远拼不出重复周期——1974 年的发现，后来启发了准晶体物理。", "几何 · 非周期铺砌"),
            ("正多面体3D旋转.html", "正多面体 3D 旋转", "柏拉图立体全空间只存在这五种；拖拽旋转，观察欧拉示性数 $V-E+F=2$。", "几何 · 欧拉公式"),
            ("欧拉七桥一笔画.html", "欧拉七桥与一笔画", "1736 年欧拉把哥尼斯堡七桥变成图：度数为奇的顶点恰好 0 或 2 个，才能一笔画完。", "图论 · 一笔画"),
            ("Dijkstra最短路径.html", "Dijkstra 最短路径", "每次贪心选最近的未访问点、松弛它的邻居——1959 年的算法，至今是导航软件的核心。", "图论 · 算法"),
            ("矩阵线性变换与特征向量.html", "矩阵线性变换与特征向量", "调滑块改 $2\\times2$ 矩阵，看单位网格被拉伸旋转；金色箭头是只伸缩不转向的特征方向。", "线代 · 特征向量"),
            ("生命游戏.html", "康威生命游戏", "只有三条规则：邻居 2–3 个才活、死细胞恰好 3 邻复活；1970 年 Conway 用它模拟了图灵机。", "元胞自动机"),
        ],
    ),
]

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; object-src 'none'">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta http-equiv="Referrer-Policy" content="no-referrer">
<title>交互可视化导航 · LBLB</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2322262B'/%3E%3Ctext x='32' y='46' font-size='30' text-anchor='middle' fill='%23F7F3E7' font-family='Georgia,serif'%3E%E2%88%9E%3C/text%3E%3C/svg%3E">
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
  font-family:"Times New Roman","Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.75;}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px 80px;}
header{padding:52px 0 6px;}
.back{font-size:13px;color:var(--blue);text-decoration:none;}
.back:hover{text-decoration:underline;}
h1{font-family:Georgia,"Noto Serif SC","Songti SC",serif;font-size:42px;margin:12px 0 6px;}
h1 .sym{color:var(--blue);font-style:italic;}
.sub{color:var(--ink2);font-size:16px;max-width:780px;}
.counts{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;}
.chip{background:#fffdf6;border:1px solid var(--line);border-radius:999px;padding:4px 13px;font-size:12.5px;color:var(--ink2);}
.chip b{color:var(--blue);}
nav.toc{margin-top:22px;background:#fffdf6;border:1px solid var(--line);border-radius:14px;padding:14px 20px;font-size:14px;}
nav.toc a{color:var(--blue);text-decoration:none;margin-right:16px;}
nav.toc a:hover{text-decoration:underline;}
h2.sec{font-family:Georgia,"Noto Serif SC",serif;font-size:25px;border-left:6px solid var(--teal);padding-left:14px;margin-top:46px;}
h2.sec small{font-size:13px;color:var(--ink2);font-family:"Noto Sans SC",sans-serif;font-weight:400;margin-left:8px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-top:16px;}
.card{display:block;background:#fffdf6;border:1px solid var(--line);border-top:4px solid var(--c,var(--blue));
  border-radius:10px;padding:14px 16px;text-decoration:none;color:var(--ink);
  transition:transform .12s ease, box-shadow .12s ease;}
.card:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(34,38,43,.10);}
.card h3{font-family:Georgia,"Noto Serif SC",serif;font-size:17px;margin-bottom:5px;color:var(--ink);}
.card p{font-size:13px;color:var(--ink2);line-height:1.65;}
.card .tag{display:inline-block;margin-top:9px;font-size:11px;letter-spacing:.06em;color:var(--c,var(--blue));font-weight:600;}
footer{margin-top:52px;border-top:1px solid var(--line);padding-top:18px;font-size:12.5px;color:var(--ink2);}
footer code{background:var(--paper2);border-radius:4px;padding:1px 6px;}
.hint{margin-top:18px;background:#fffdf6;border:1px solid var(--line);border-radius:12px;padding:13px 18px;font-size:13px;color:var(--ink2);}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="back" href="../00-总览/index.html">← 返回总览</a>
  <h1>交互可视化 <span class="sym">●</span></h1>
  <p class="sub">数学最动人的时刻是「看见」。本页收录 <b>{{total}}</b> 个交互模块——全部是单文件离线页面，
  用浏览器打开，亲手拖一拖、点一点、放大缩小，公式与图形都在本地渲染，不联网也能跑。</p>
  <div class="counts">{{chips}}</div>
  <nav class="toc">{{toc}}</nav>
</header>
{{sections}}
<div class="hint">
  <b>使用提示：</b>所有页面均为单文件 HTML，无需联网；公式由本地 <code>../assets/mathjax</code> 离线渲染，零外部请求。
  画布会自适应窗口宽度——直接缩放浏览器窗口即可改变画布大小。
</div>
<footer>
  本目录共收录 {{total}} 个交互模块：{{summary}}。<br>
  <a class="back" href="../00-总览/index.html">← 返回总览</a> ·
  <a class="back" href="../04-美丽证明/美丽证明集锦.html">美丽证明 →</a>
</footer>
</div>
</body>
</html>
"""

COLORS = ["var(--blue)", "var(--teal)", "var(--red)", "var(--gold)",
          "var(--green)", "var(--violet)"]


def main():
    missing = []
    sections = []
    toc_parts = []
    counts = []
    summary_parts = []
    total = 0

    for gi, (gname, gdesc, items) in enumerate(GROUPS):
        anchor = "g%d" % (gi + 1)
        toc_parts.append('<a href="#%s">%s（%d）</a>' % (anchor, gname, len(items)))
        counts.append('<span class="chip">%s <b>%d</b> 个</span>' % (gname, len(items)))
        summary_parts.append("%s %d" % (gname, len(items)))
        total += len(items)

        cards = []
        for ci, (fn, title, desc, tag) in enumerate(items):
            path = os.path.join(VIZ_DIR, fn)
            if not os.path.exists(path):
                missing.append(fn)
                continue
            color = COLORS[(gi + ci) % len(COLORS)]
            cards.append(
                '<a class="card" style="--c:%s" href="%s">'
                "<h3>%s</h3><p>%s</p><span class=\"tag\">%s</span></a>"
                % (color, html.escape(fn, quote=True), html.escape(title),
                   desc, html.escape(tag))
            )
        sections.append(
            '<h2 class="sec" id="%s">%s <small>%s</small></h2>\n<div class="grid">\n%s\n</div>'
            % (anchor, html.escape(gname), html.escape(gdesc), "\n".join(cards))
        )

    # 校验：本目录内是否存在未被收录的页面
    listed = {fn for _, _, items in GROUPS for fn, _, _, _ in items}
    on_disk = {f for f in os.listdir(VIZ_DIR)
               if f.endswith(".html") and f != "可视化导航.html"}
    unlisted = sorted(on_disk - listed)

    doc = HEAD
    for key, val in (("total", total),
                     ("chips", "\n    ".join(counts)),
                     ("toc", " ".join(toc_parts)),
                     ("sections", "\n".join(sections)),
                     ("summary", " · ".join(summary_parts))):
        doc = doc.replace("{{" + key + "}}", str(val))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)

    print("written: %s" % OUT)
    print("modules: %d" % total)
    if missing:
        print("MISSING TARGETS: %s" % missing)
    if unlisted:
        print("UNLISTED PAGES in dir: %s" % unlisted)
    if not missing and not unlisted:
        print("OK: all listed targets exist, no page left unlisted")
    return 0 if not (missing or unlisted) else 1


if __name__ == "__main__":
    sys.exit(main())
