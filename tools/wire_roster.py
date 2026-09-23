# -*- coding: utf-8 -*-
"""把数学家名录接进导航，并写 11-数学家/README.md 说明数据来源与现状。"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\LBLB-github"

# ---- 1) 三个原有数学家页面加「名录」入口 ----
LINK = '<a class="back" href="数学家名录.html">数学家名录（10,000 人检索）</a>'
for f in ["数学群星谱.html", "数学家的故事.html", "当代华人数学家.html"]:
    p = os.path.join(ROOT, "11-数学家", f)
    t = io.open(p, encoding="utf-8").read()
    if "数学家名录.html" in t:
        print("%-22s 已有入口，跳过" % f)
        continue
    # 插在第一个 </footer> 之前
    i = t.rfind("</footer>")
    if i < 0:
        print("%-22s 未找到 footer" % f)
        continue
    t = t[:i] + "  " + LINK + "<br>\n" + t[i:]
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("%-22s 已加入口" % f)

# ---- 2) 00-总览 的数学家卡片区补一张 ----
p = os.path.join(ROOT, "00-总览", "index.html")
t = io.open(p, encoding="utf-8").read()
if "数学家名录.html" not in t:
    anchor = '<h2 class="sec">数学家 · 历史 · 书单</h2>\n<div class="grid">\n'
    card = ('  <a class="card" style="--c:var(--red)" href="../11-数学家/数学家名录.html">'
            '<div class="num">40</div><h3>数学家名录</h3>'
            "<p>检索 10,000 位数学家：按原名/译名、国籍、时代筛选，每人附可核实来源。</p></a>\n")
    if anchor in t:
        t = t.replace(anchor, anchor + card, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("00-总览 已加入名录卡片")
    else:
        print("00-总览 未找到锚点")
else:
    print("00-总览 已有名录卡片")

# ---- 3) 写 11-数学家/README.md ----
README = """# 11-数学家 · 数据来源与现状

本目录有四个页面：

| 页面 | 性质 | 说明 |
| --- | --- | --- |
| `数学群星谱.html` | 精编 | 两千年数学家巡礼，按时代与分支编排 |
| `数学家的故事.html` | 精编 | 七个转折时刻的叙事 |
| `当代华人数学家.html` | 精编 | 当代华人数学家小传 |
| `数学家名录.html` | 检索 | 10,000 人事实性名录，见下 |

---

## 数学家名录：收录什么、不收录什么

名录数据由 `tools/build_math_roster.py` 从桌面采集数据生成，只收录**事实性字段**：

| 字段 | 说明 |
| --- | --- |
| 外文原名 | 拉丁字母原文拼写（东亚学者保留拼音/罗马音） |
| 中文译名 | **仅在已翻译时显示**；与原名相同则视为未翻译，不重复展示 |
| 生卒年 | 原数据未考订者如实标为 `?` |
| 国籍/地区 | 形容词形式 |
| 时代分档 | 由生卒年推出，用于按时代浏览 |
| 出处链接 | Wikipedia 或 MacTutor 的个人页面 |
| 中文贡献 | **仅在原始描述本身为中文时收录** |

姓名、生卒年、国籍、出处属**事实性信息**，不受著作权保护，可安全发布。

### 为什么不收录贡献描述

对原始采集数据做过体检，结论是**不能直接搬运**：

| 问题 | 占比 |
| --- | --- |
| 贡献描述是未翻译的英文原文 | 81.0% |
| 「中文译名」实际就是拉丁原名（未译） | 64.0% |
| 生卒年为 `?`（原数据未考订） | 23.9% |
| 贡献栏写「具体贡献待补充」 | 14.1% |
| 国籍未标注 | 8.8% |

同时满足「中文贡献 ≥10 字 + 有具体年份 + 有中文译名」的仅 **0.9%（91 条）**。

把这 10000 条按原样发布，等于在一个中文站点上放出 81% 的英文原文与 64% 的未翻译人名——
这正是「发布半成品」。因此名录只发布事实字段，贡献栏留待翻译后补充。

采集数据中还存在少量字符损坏（如 `Đ` → `?`、`ã` → `?`），本页如实呈现原始拼写，不做猜测性修补。

### 想补全贡献栏怎么办

1. 对原始 CSV 逐条翻译 `contributions` 列（英文 → 中文）；
2. 把译好的 CSV 放回采集目录；
3. 重跑 `python tools/build_math_roster.py` 与 `python tools/build_math_roster_page.py`。

翻译是唯一可靠的路——机器批量翻译数学术语的错译率不可接受，而错译比不译更有害。

---

## 数据出处

- English Wikipedia 各数学家条目
- MacTutor History of Mathematics Archive（University of St Andrews）
- 原始采集脚本与中间产物不属于本仓库

本仓库不对上述外部页面的内容主张任何权利；出处以每条的 `source` 字段为准。
"""
io.open(os.path.join(ROOT, "11-数学家", "README.md"), "w",
        encoding="utf-8", newline="\n").write(README)
print("已写 11-数学家/README.md")
