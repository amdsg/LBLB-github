# 13-应试训练 · 真题刷题与组卷

本目录提供一套**纯前端的刷题 / 组卷 / 覆盖统计系统**：原生整卷限时作答、真实单题乱序训练、
按类别与难度自定义组卷、逐省逐科逐届的来源覆盖表。

> **关于真题与试卷：默认不随仓库发布。**
> 这些材料的权利人是教育部考试中心、中国数学会竞赛工作组、各高校与各省考试院。
> 逐项核查后确认**没有任何权利方给出可再分发的授权**，因此本仓库只发布元数据
> （试卷标题、年份、出处 URL）与自备题库的接口，不发布题目正文与试卷原件。
> 完整依据、官方获取渠道与合规操作方式见 
>
> **本地使用不受影响**：把题库文件放回 `123/` 目录后，三个页面照常工作
> （实测可加载 12858 道单题、417 套整卷）。
>
> **如果想要难度对标考试、答案经机器验证的原创题**，另见
> [`15-应试实战`](../15-应试实战/index.html)（考研数一/数二、专升本、竞赛四册）与
> [`14-自测题库`](../14-自测题库/index.html)（9 个知识分支）。

---

## 页面

| 文件 | 作用 | 是否依赖题库数据 |
| --- | --- | --- |
| `00-应试总览.html` | 本分区导航 | 否 |
| `01-CMC全国大学生数学竞赛.html` | 竞赛考点与题型讲义 | 否 |
| `02-考研数学-高等数学强化.html` | 考研高数强化讲义 | 否 |
| `03-考研数学-线性代数与概率强化.html` | 考研线代与概率强化讲义 | 否 |
| `05-真题模拟卷.html` | 整卷模式：限时作答、查看官方过程、逐步自评 | **是** |
| `06-真实单题训练.html` | 单题模式：乱序训练、按分类/地区/难度组卷 | **是** |
| `07-题库覆盖与来源.html` | 来源覆盖表：逐省、逐科、逐届检查缺项 | **是** |

全部页面统一使用 `assets/mathjax/` 下的 MathJax 3 构建（SVG 矢量输出），随仓库提供、离线可用。
（原先 01／02／03 三个页面用的是体积 22.8 MB 的 MathJax 4 构建，已合并到同一份构建，
节省约 21 MB 仓库体积。）

---

## 如何接入自备题库

把数据文件放进本目录的 `123/` 子目录，刷新页面即可。三个页面对应的文件如下：

| 文件 | 定义全局变量 | 被哪个页面使用 |
| --- | --- | --- |
| `123/真题卷.js` | `window.LBLB_EXAMS` | 05、06、07 |
| `123/题库-汇总.js` | `window.LBLB_UNIFIED` | 06 |
| `123/文本整卷-新增.js` | `window.LBLB_TEXT_PAPERS` | 05 |
| `123/试卷清单.js` | `window.PAPER_LIBRARY` | 试卷索引（仓库已含一份示例） |

这些文件都是**可直接双击打开的 JS 赋值语句**（不是模块），形如
`window.XXX = {...};`，因此用 `<script src>` 同步加载，无需服务器。

> `.gitignore` 已默认忽略 `123/` 下的题库 JS 与试卷 PDF，避免误把受版权保护的材料提交到公开仓库。

### `真题卷.js` — `window.LBLB_EXAMS`

```js
window.LBLB_EXAMS_VER = "2026-09-18";        // 可选：版本号，会显示在页面上
window.LBLB_EXAMS = {
  version: "2026-09-18",
  papers: [ /* 整卷索引 */ ],
  questions: [ /* 单题，被 06 页面作为「种子题库」 */ ]
};
```

**整卷记录**（`papers[]`）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 唯一标识 |
| `cat` | string | 总分类：`zsb`（专升本）/ `kaoyan`（考研）/ `cmc`（竞赛）/ `exercise`（练习题） |
| `sub` | string | 子分类，如省份名或 `数一`／`数二`／`数三` |
| `title` | string | 试卷标题 |
| `year` | number | 年份 |
| `stage` | string | 如 `真题` |
| `topic` | string | 主题标签 |
| `paper.file` | string | 试卷文件路径（相对 `13-应试训练/`） |
| `paper.pages` / `paper.bytes` | number | 页数与字节数 |
| `paper.sha256` | string | 文件校验值 |
| `answer` | object | 解析文件，字段同上；无独立解析时可与 `paper` 相同 |
| `source` | string | 来源标注 |
| `questionCount` | number | 题目数 |
| `difficulty` | string | `简单`／`比较简单`／`基础`／`比较难`／`难`／`提高` |

**单题记录**（`questions[]`）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 唯一标识，用于去重 |
| `cat` | string | 总分类，同上 |
| `sub` | string | 子分类 |
| `topic` | string | 主题 |
| `skill` | string | 能力/知识块标签 |
| `source` / `sourceUrl` | string | 来源名称与链接 |
| `license` | string | 该题的授权说明 |
| `difficulty` | string | 难度标签 |
| `q` | string | 题干，支持 `$LaTeX$` |
| `o` | string[] | 选项数组；开放题为 `[]` |
| `a` | number | 正确选项下标（从 0 起）；开放题为 `-1` |
| `answer` | string | 参考答案文本 |
| `s` | string | 解析过程 |
| `score` | number | 分值 |
| `type` | string | 题型，如 `choice`／`fill` |

### `题库-汇总.js` — `window.LBLB_UNIFIED`

06 页面会把 `LBLB_EXAMS.questions`（种子）与 `LBLB_UNIFIED.extras`（额外题）合并，
按 `id` 去重后作为完整题库。字段与上表单题记录一致。

```js
window.LBLB_UNIFIED = {
  version: "2026-09-18-unified",
  builtAt: "2026-09-18T14:01:22.751Z",
  papers: 0,
  seedQuestions: 0,
  extraQuestions: 0,
  byCat: { cmc: 0, fdu: 0, zsb: 0, exercise: 0, kaoyan: 0 },
  sources: [ /* 每个源文件的统计 */ ],
  extras: [ /* 归一化后的题目数组 */ ]
};
```

该文件是**构建产物**，由 `123/代码/build_unified.js` 扫描 `123/` 下所有题库源生成：

```bash
cd 13-应试训练/123/代码
node build_unified.js
```

脚本会自动识别以下全局变量并归一化：`QUESTION_BANK.questions`、`LBLB_QUIZ`、
`LBLB_CMC_REAL`、`LBLB_FDU_REAL`、`LBLB_ZSB_REAL`。字段别名（如 `stem`→`q`、
`options`→`o`、`analysis`→`s`）也会一并处理。

### `文本整卷-新增.js` — `window.LBLB_TEXT_PAPERS`

用于无法直接分发 PDF、只能以文字形式保存的整卷。05 页面会把这些卷与 PDF 整卷一起列出。

```js
window.LBLB_TEXT_PAPERS = [
  {
    type: "text-paper",
    category: "专升本",     // 中文分类名，不是 cat 代码
    sub: "江苏",
    year: 2022,
    difficulty: 4,          // 数字：1=简单 … 5=难
    source: "来源名称 https://来源链接",
    title: "试卷标题",
    note: "关于转录方式与分值的说明",
    questions: [
      {
        no: 1,              // 题号
        q: "题干文字",
        opts: ["A 选项", "B 选项", "C 选项", "D 选项"],  // 填空题/解答题为 []
        ans: "C",           // 选择题为选项字母；其余为题面答案文本
        analysis: "解析文字"
      }
    ]
  }
];
```

### `试卷清单.js` — `window.PAPER_LIBRARY`

轻量的试卷索引，仓库已包含一份（示例/元数据）。字段为
`{ category, tag, year, title, file }`，其中 `file` 是相对 `13-应试训练/123/` 的试卷文件名。
页面并未强依赖此文件，缺失不影响运行。

### `_papers*.json` — 原始来源清单（仅元数据）

`123/` 下另有四个 JSON 文件（`_papers.json`、`_papers__来自专升本.json`、
`_papers__来自练习题.json`、`_papers__来自考研.json`），是整理题库时记录的**来源清单**：
每套试卷的标题、分类、年份、来源 URL、页数与是否已结构化。

它们只含元数据，**不含任何题目正文**，因此随仓库保留以便追溯出处。页面与脚本均不读取这些文件；
其中的 `file` 字段指向整理时的原始本地目录结构，与当前仓库布局不一致，仅作来源记录参考。


---

## 数据审计脚本

`123/代码/` 下提供四个脚本，用于在录入题库后批量检查质量：

| 脚本 | 运行方式 | 作用 |
| --- | --- | --- |
| `scan_deep.py` | `python scan_deep.py` | 检查 `$` 配对、`$...$` 之外的裸导数记号与 `^` 指数 |
| `scan_formulas.py` | `python scan_formulas.py` | 检查公式定界符与转义 |
| `scan_js.py` | `python scan_js.py` | 检查题库 JS 中裸数学符号（应改用 LaTeX） |
| `build_unified.js` | `node build_unified.js` | 汇总去重，生成 `题库-汇总.js` |

`scan_deep.py` 与 `scan_formulas.py` 直接扫描本目录下的 7 个页面文件，
不依赖题库数据；`scan_js.py` 与 `build_unified.js` 针对题库数据文件，
缺少数据时会打印 `[MISS]` 并跳过对应文件。

三个 Python 脚本仅使用标准库，无需安装依赖。
