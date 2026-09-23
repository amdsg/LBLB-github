# -*- coding: utf-8 -*-
r"""
LBLB 数学前沿自动更新器
====================================
- 每次运行抓取 arXiv 数学分类（math）最新论文（多端点 + 自动重试退避）
- arXiv 直连不可达时，自动切换 Semantic Scholar 备用数据源（按 12 个数学主题
  检索、合并去重生成日报），arXiv 恢复可达后下次运行自动切回
- 自动生成/更新：09-前沿动态/论文日报.html
- 按主题抓取 12 个分支的最新论文，生成 09-前沿动态/论文数据.js
  （各主题深度讲义页通过 <script src> 加载它，实现「打开页面即见该主题最新研究」）
- 由 Windows 计划任务每天触发；手动运行：python 数学前沿更新器.py
  （--demo 参数用内置示例数据生成页面，用于离线验证，不联网；
    --proxy http://127.0.0.1:7890 可显式指定代理，默认遵循系统代理/环境变量）
- 仅使用 Python 标准库（urllib + xml.etree + json），无第三方依赖
- 文明上网：每天最多一次、每主题单次少量请求、带身份标识 UA、超时与退避、
  失败即保留旧数据，不批量下载、不并发轰炸任何站点
"""

import datetime
import html as htmlmod
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "09-前沿动态")
OUT_FILE = os.path.join(OUT_DIR, "论文日报.html")
LOG_FILE = os.path.join(OUT_DIR, "_update.log")
TOPIC_JS = os.path.join(OUT_DIR, "论文数据.js")

MAX_ITEMS = 25          # 日报最多展示条数
TOPIC_ITEMS = 5         # 每主题最新论文条数

# arXiv 数据源按优先级排列；每个源失败后自动尝试下一个
FEEDS = [
    ("https://export.arxiv.org/api/query?search_query=cat:math.*&sortBy=submittedDate&sortOrder=descending&max_results=" + str(MAX_ITEMS), "atom"),
    ("https://rss.arxiv.org/rss/math", "rss"),
    ("http://export.arxiv.org/rss/math", "rss"),
    ("https://arxiv.org/atom/math", "atom"),
]

# 主题 -> arXiv 分类（供深度讲义页的「该主题最新论文」模块使用）
TOPICS = {
    "数论": "math.NT",
    "几何": "math.MG",
    "代数": "math.AG",
    "分析": "math.CA",
    "概率与统计": "math.PR",
    "组合与图论": "math.CO",
    "线性代数": "math.RA",
    "拓扑学": "math.AT",
    "复分析": "math.CV",
    "微分方程": "math.AP",
    "博弈论": "math.OC",
    "数理逻辑": "math.LO",
}

# 主题 -> Semantic Scholar 英文检索词（arXiv 分类查询不可达时的备用通道）
TOPIC_QUERIES = {
    "数论": "number theory",
    "几何": "metric geometry differential geometry",
    "代数": "algebra algebraic geometry",
    "分析": "mathematical analysis",
    "概率与统计": "probability statistics",
    "组合与图论": "combinatorics graph theory",
    "线性代数": "linear algebra matrix",
    "拓扑学": "topology",
    "复分析": "complex analysis",
    "微分方程": "differential equations",
    "博弈论": "game theory optimization",
    "数理逻辑": "mathematical logic",
}

S2_API = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
S2_FIELDS = "title,abstract,authors,publicationDate,externalIds,url"

ABS_LEN = 220
TITLE_LEN = 180      # 标题展示上限（超长标题截断并加省略号）
ARXIV_NS = "{http://purl.org/dc/elements/1.1/}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 LBLB-math-updater"

# ---------------------------------------------------------------------------
# 摘要清洗
# ---------------------------------------------------------------------------
# 摘要直接取自 arXiv / Semantic Scholar 的 LaTeX 源文本，若原样塞进页面会有三类显示缺陷：
#   1) LaTeX 重音转义（Corti\~nas）会原样显示成反斜杠，应转成 Unicode 字母；
#   2) 定长截断可能把 $...$ 切成半个，未闭合的 $ 会让 MathJax 把后续文字整段当作公式吞掉；
#   3) arXiv 常用 \F、\C 等自定义宏未定义，MathJax 会渲染成红色报错。
# 下面分别处理 1、2；第 3 类在页面 MathJax 配置里补宏定义（见 MACRO_DEFS）。

_ACCENT_MARKS = {
    "'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303",
    "=": "\u0304", ".": "\u0307", "u": "\u0306", "v": "\u030c", "H": "\u030b",
    "c": "\u0327", "k": "\u0328", "r": "\u030a", "b": "\u0331", "d": "\u0323",
}
# 非字母重音：\'e \`a \^o \"u \~n —— 这几个符号没有同名宏，可以不要求花括号
_ACCENT_SYMBOL_RE = re.compile(r"\\(['\"`^~])\s?\{?([A-Za-z])\}?")
# 字母型重音：\c{c} \u{a} \v{s} \H{o} \k{a} \r{a} \b{h} \d{d} \={a} \.{z}
# 必须要求花括号，否则会把 \chi、\beta、\delta、\boxtimes、\ldots 这类普通宏的
# 首字母误当成重音命令吃掉（例如 \chi 被读成 \c + h）。
_ACCENT_LETTER_RE = re.compile(r"\\([uvHckrbd=.])\s?\{([A-Za-z])\}")


def latex_accents(text):
    """把 LaTeX 重音转义还原成 Unicode 字母：Corti\\~nas -> Cortiñas。"""
    if "\\" not in text:
        return text

    def sub(m):
        mark = _ACCENT_MARKS.get(m.group(1))
        if mark is None:
            return m.group(0)
        try:
            return unicodedata.normalize("NFC", m.group(2) + mark)
        except Exception:
            return m.group(0)

    text = _ACCENT_SYMBOL_RE.sub(sub, text)
    text = _ACCENT_LETTER_RE.sub(sub, text)
    return text


# 有的论文把整段 LaTeX 导言区塞进了标题/摘要字段（Semantic Scholar 上游数据里就有），
# 例如 "On p→(·)\documentclass[12pt]{minimal}\usepackage{amsmath}...\begin{document}...".
# 若原样进页面，MathJax 的 processEnvironments 会去解析它，页面会报
# "Unknown environment 'document'" 并把这一大段以红字显示出来。
_PREAMBLE_RE = re.compile(
    r"\\documentclass(?:\[[^\]]*\])?\{[^}]*\}[\s\S]*?\\begin\{document\}", re.I)
# 上游数据有时会把 \documentclass 截断在末尾，没有配对的 \begin{document}，
# 所以还要能单独清掉残留的 \documentclass / \usepackage / \begin{document} 片段。
_TEXCMD_RE = re.compile(
    r"\\(?:documentclass|usepackage)(?:\[[^\]]*\])?\{[^}]*\}")
_BEGEND_RE = re.compile(r"\\(?:begin|end)\{document\}", re.I)


def strip_latex_preamble(text):
    """去掉元数据里混入的 LaTeX 导言区与 \\begin/\\end{document} 包装。"""
    if "\\documentclass" not in text and "\\begin{document}" not in text:
        return text
    text = _PREAMBLE_RE.sub("", text)
    text = _TEXCMD_RE.sub("", text)
    text = _BEGEND_RE.sub("", text)
    text = text.replace("$$", "$")   # $$...$$ → $...$，保持定界符成对
    return re.sub(r"\s+", " ", text).strip()


def prep_title(text):
    """标题进页面前的统一处理。

    上游被导言区污染的标题往往同时是被截断的（如 "...with Gene"），
    这类标题清洗后补一个省略号，如实标示原标题不完整。
    """
    raw = clean(text)
    polluted = "\\documentclass" in raw or "\\begin{document}" in raw
    out = truncate_balanced(strip_latex_preamble(latex_accents(raw)), TITLE_LEN)
    if polluted and out and not out.endswith("…"):
        out += "…"
    return out


def truncate_balanced(text, limit):
    """按 limit 截断，但不切断 $...$：截完保证未转义 $ 的个数为偶数。

    未闭合的 $ 会让 MathJax 把后面整段文字当成公式（甚至跨到下一条摘要），
    造成可读内容凭空消失，所以这里宁可少截几个字也要保证配平。
    """
    truncated = len(text) > limit
    cut = text[:limit] if truncated else text
    if truncated:
        sp = cut.rfind(" ")
        if sp > limit * 0.6:
            cut = cut[:sp]

    while len(re.findall(r"(?<!\\)\$", cut)) % 2:
        idx = cut.rfind("$")
        if idx <= 0:
            cut = cut.replace("$", "")
            break
        cut = cut[:idx]

    cut = cut.rstrip(" ,;:")
    if truncated:
        cut += "…"
    return cut


def prep_abstract(text):
    """摘要进页面前的统一处理。"""
    return truncate_balanced(
        strip_latex_preamble(latex_accents(clean(text))), ABS_LEN)


DEMO_ITEMS = [
    {
        "title": "【示例·离线演示】On the Riemann Hypothesis and the distribution of zeros",
        "link": "https://arxiv.org/abs/demo.00001",
        "abs": "这是一条内置演示数据，用于在无网络环境下验证页面生成逻辑。真实运行时此区会被 arXiv 最新论文替换。",
        "date": "2026-09-14",
        "author": "Demo Author",
    },
    {
        "title": "【示例·离线演示】A new proof of the Collatz conjecture in positive density regions",
        "link": "https://arxiv.org/abs/demo.00002",
        "abs": "演示条目之二：仅用于验证更新器页面渲染，不代表真实研究结论。",
        "date": "2026-09-13",
        "author": "Demo Author",
    },
    {
        "title": "【示例·离线演示】Effective bounds in the abc conjecture framework",
        "link": "https://arxiv.org/abs/demo.00003",
        "abs": "演示条目之三：请通过 --demo 之外的正常方式运行以获取真实 arXiv 数据。",
        "date": "2026-09-12",
        "author": "Demo Author",
    },
]


def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("[%s] %s\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))
    except Exception:
        pass


def build_opener():
    """构造 URL 打开器：--proxy 显式指定代理；否则遵循系统代理与环境变量。"""
    proxy = None
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--proxy" and i + 1 < len(args):
            proxy = args[i + 1]
        elif a.startswith("--proxy="):
            proxy = a.split("=", 1)[1]
    if proxy:
        log("使用代理：%s" % proxy)
        return urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    return urllib.request.build_opener()


def fetch_once(url, opener):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=25) as r:
        return r.read()


def fetch_with_retry(url, opener, tries=2):
    for i in range(tries):
        try:
            data = fetch_once(url, opener)
            log("抓取成功：%s（%d 字节）" % (url, len(data)))
            return data
        except urllib.error.HTTPError as e:
            log("抓取失败 %s（第 %d 次）: HTTP %d" % (url, i + 1, e.code))
            if e.code == 429 and i < tries - 1:
                time.sleep(20)  # 限流长退避（Semantic Scholar 共享配额）
            elif i < tries - 1:
                time.sleep(2 * (i + 1))
        except Exception as e:
            log("抓取失败 %s（第 %d 次）: %s" % (url, i + 1, e))
            if i < tries - 1:
                time.sleep(2 * (i + 1))
    return None


def clean(text):
    if not text:
        return ""
    t = re.sub(r"<[^>]+>", " ", text)
    t = htmlmod.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def esc(text):
    return htmlmod.escape(text or "")


def parse_pubdate(s):
    if not s:
        return ""
    m = re.search(r"\d{1,2}\s+\w+\s+\d{4}", s)
    if m:
        try:
            return datetime.datetime.strptime(m.group(0), "%d %b %Y").strftime("%Y-%m-%d")
        except Exception:
            pass
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m2:
        return m2.group(0)
    return clean(s)[:40]


def parse_rss(data):
    root = ET.fromstring(data)
    items = []
    for item in root.iter("item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        desc = item.findtext("description") or ""
        pub = item.findtext("pubDate") or ""
        creator = item.findtext(ARXIV_NS + "creator") or ""
        if not title:
            continue
        items.append({
            "title": prep_title(title),
            "link": clean(link),
            "abs": prep_abstract(desc),
            "date": parse_pubdate(pub),
            "author": clean(creator),
        })
    return items


def parse_atom(data):
    root = ET.fromstring(data)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = []
    for entry in root.findall("a:entry", ns):
        title = entry.findtext("a:title", default="", namespaces=ns) or ""
        link_el = entry.find("a:link", ns)
        link = link_el.get("href") if link_el is not None else ""
        summary = entry.findtext("a:summary", default="", namespaces=ns) or ""
        pub = entry.findtext("a:published", default="", namespaces=ns) or ""
        author = entry.findtext("a:author/a:name", default="", namespaces=ns) or ""
        if not title:
            continue
        items.append({
            "title": prep_title(title),
            "link": clean(link),
            "abs": prep_abstract(summary),
            "date": parse_pubdate(pub),
            "author": clean(author),
        })
    return items


def s2_date_fix(raw_date, arxiv_id):
    """S2 记录的 'publicationDate' 常为期刊待刊的未来日期（如 2026-12-01）。
    若日期晚于今天，则用 arXiv ID 前四位编码的真实提交年月（YYMM）修正为 YYYY-MM-01；
    无法修正的返回空串（由调用方决定保留或丢弃）。"""
    if not raw_date:
        return raw_date or ""
    today = datetime.date.today().isoformat()
    if raw_date <= today:
        return raw_date
    m = re.match(r"^(\d{2})(\d{2})\.\d{4,5}$", arxiv_id or "")
    if m:
        try:
            yy, mm = int(m.group(1)), int(m.group(2))
            if 0 <= yy <= 99 and 1 <= mm <= 12:
                return "20%02d-%02d-01" % (yy, mm)
        except Exception:
            pass
    return ""


def s2_search(query, opener, max_items):
    """Semantic Scholar 备用通道：按发表日期倒序取最新数学论文。
    返回列表按日期倒序；未来日期（期刊待刊）按 arXiv ID 提交年月修正，无法修正则丢弃。"""
    url = (S2_API + "?query=" + urllib.parse.quote(query)
           + "&fieldsOfStudy=Mathematics&fields=" + S2_FIELDS
           + "&sort=publicationDate:desc")
    data = fetch_with_retry(url, opener, tries=3)
    if data is None:
        return []
    try:
        obj = json.loads(data.decode("utf-8"))
    except Exception as e:
        log("S2 解析失败: %s" % e)
        return []
    out = []
    skipped = 0
    for p in obj.get("data") or []:
        title = prep_title(p.get("title"))
        link = p.get("url") or ""
        if not title or not link:
            continue
        arxiv_id = (p.get("externalIds") or {}).get("ArXiv") or ""
        date = s2_date_fix(p.get("publicationDate") or "", arxiv_id)
        if (p.get("publicationDate") or "") > datetime.date.today().isoformat() and not date:
            skipped += 1
            continue
        names = [a.get("name", "") for a in (p.get("authors") or []) if a.get("name")]
        author = "、".join(names[:2]) + (" 等" if len(names) > 2 else "")
        if arxiv_id:
            author = (author + " · " if author else "") + "arXiv:" + arxiv_id
        out.append({
            "title": title,
            "link": link,
            "abs": prep_abstract(p.get("abstract")),
            "date": date,
            "author": author,
        })
        if len(out) >= max_items:
            break
    if skipped:
        log("S2[%s] 跳过 %d 条未来日期且无 arXiv ID 的记录" % (query[:30], skipped))
    return out


def fetch_arxiv_feeds(opener):
    """arXiv 主通道：依次尝试各端点，成功返回条目列表，全部失败返回 None。"""
    for url, kind in FEEDS:
        data = fetch_with_retry(url, opener)
        if data is None:
            continue
        try:
            items = parse_rss(data) if kind == "rss" else parse_atom(data)
            if items:
                log("解析成功：%s，%d 条" % (url, len(items)))
                return items[:MAX_ITEMS]
            log("解析结果为空：%s" % url)
        except Exception as e:
            log("解析失败 %s: %s" % (url, e))
    return None


def fetch_topic_arxiv(topic, cat, opener):
    """按 arXiv 分类抓取某主题最新论文，失败返回 []。"""
    url = ("https://export.arxiv.org/api/query?search_query=cat:%s"
           "&sortBy=submittedDate&sortOrder=descending&max_results=%d"
           % (cat, TOPIC_ITEMS))
    data = fetch_with_retry(url, opener, tries=2)
    if data is None:
        return []
    try:
        items = parse_atom(data)
        log("主题[%s] arXiv %s：%d 条" % (topic, cat, len(items)))
        return items[:TOPIC_ITEMS]
    except Exception as e:
        log("主题[%s] arXiv 解析失败: %s" % (topic, e))
        return []


def fetch_topic_papers(topic, cat, opener, demo=False, arxiv_ok=True):
    """抓取某一主题最新 TOPIC_ITEMS 篇论文：arXiv 优先，Semantic Scholar 备用。"""
    if demo:
        return [{
            "title": "【示例】" + topic + " 主题演示论文（离线）",
            "link": "https://arxiv.org/abs/demo." + topic,
            "date": "2026-09-14",
            "author": "Demo Author",
            "abs": "离线演示数据。联网运行更新器后此处为真实论文。",
        }]
    if arxiv_ok:
        papers = fetch_topic_arxiv(topic, cat, opener)
        if papers:
            return papers
        log("主题[%s] arXiv 不可用，切换 Semantic Scholar" % topic)
    papers = s2_search(TOPIC_QUERIES[topic], opener, TOPIC_ITEMS)
    log("主题[%s] S2：%d 条" % (topic, len(papers)))
    return papers


def merge_topics(topic_data):
    """主题数据合并去重、按日期倒序，作为日报备用内容。"""
    seen = set()
    merged = []
    for papers in topic_data.values():
        for p in papers:
            key = re.sub(r"\W+", "", (p["title"] or "").lower())[:80]
            if not key or key in seen:
                continue
            seen.add(key)
            merged.append(p)
    merged.sort(key=lambda p: p["date"] or "", reverse=True)
    return merged[:MAX_ITEMS]


def write_topic_js(topic_data):
    """生成 window.LBLB_PAPERS = {...} 数据文件，供各主题讲义页加载。"""
    js = "/* 由 LBLB 数学前沿更新器自动生成：各主题最新论文（arXiv 优先，Semantic Scholar 备用）。请勿手动编辑。 */\n"
    js += "window.LBLB_PAPERS = " + json.dumps(topic_data, ensure_ascii=False, indent=1) + ";\n"
    tmp = TOPIC_JS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(js)
    os.replace(tmp, TOPIC_JS)
    ok = sum(1 for v in topic_data.values() if v)
    log("主题数据生成完成：%d/%d 个主题有数据 -> %s" % (ok, len(topic_data), TOPIC_JS))
    print("TOPICS %d/%d -> %s" % (ok, len(topic_data), TOPIC_JS))


def extract_events_block(old_html):
    if not old_html:
        return ""
    m = re.search(r"(<!-- EVENTS:BEGIN -->.*?<!-- EVENTS:END -->)", old_html, re.S)
    return m.group(1) if m else ""


def shell(page):
    favicon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2322262B'/%3E%3Ctext x='32' y='46' font-size='30' text-anchor='middle' fill='%23F7F3E7' font-family='Georgia,serif'%3E%CE%A3%3C/text%3E%3C/svg%3E"
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>论文日报 · LBLB 数学前沿</title>
<link rel="icon" href="%s">
<style>
:root{--paper:#F7F3E7;--paper2:#FFFDF6;--ink:#22262B;--ink2:#5A5F66;--line:#D8D2C2;--red:#B23A2E;--blue:#2F5D8A;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--paper);color:var(--ink);font-family:"Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.75;padding:30px 20px 64px;}
.wrap{max-width:920px;margin:0 auto;}
.crumb{font-size:14px;color:var(--ink2);margin-bottom:10px;}
.crumb a{color:var(--blue);text-decoration:none;}
.crumb a:hover{text-decoration:underline;}
h1{font-family:Georgia,"Noto Serif SC","Songti SC",serif;font-size:38px;margin:10px 0 8px;}
.sub{color:var(--ink2);font-size:14px;margin-bottom:6px;}
.status{color:var(--red);font-size:13px;margin-bottom:22px;}
.sec{margin-top:28px;}
.sec h2{font-family:Georgia,"Noto Serif SC",serif;font-size:22px;border-left:6px solid var(--red);padding-left:12px;margin-bottom:14px;}
ol.papers{list-style:none;counter-reset:p;display:grid;gap:14px;}
ol.papers li{counter-increment:p;background:var(--paper2);border:1px solid var(--line);border-radius:10px;padding:14px 16px;}
ol.papers li::before{content:counter(p);font-family:Georgia,serif;color:var(--red);font-weight:700;margin-right:8px;font-size:15px;}
ol.papers a{color:var(--blue);text-decoration:none;font-weight:600;font-size:15px;}
ol.papers a:hover{text-decoration:underline;}
.meta{font-size:13px;color:var(--ink2);margin:4px 0 6px;}
.abs{font-size:14px;color:var(--ink);}
.events{margin-top:4px;}
.events .empty{background:var(--paper2);border:1px dashed var(--line);border-radius:10px;padding:14px 16px;font-size:14px;color:var(--ink2);}
.events .empty a{color:var(--blue);text-decoration:none;}
.waiting{background:var(--paper2);border:1px dashed var(--line);border-radius:10px;padding:20px 22px;font-size:15px;color:var(--ink);}
.waiting code{background:#E4DECC;border-radius:4px;padding:1px 6px;word-break:break-all;}
.note{margin-top:34px;background:#EFE9D8;border-radius:10px;padding:14px 16px;font-size:13px;color:var(--ink2);}
.note code{background:#E4DECC;border-radius:4px;padding:1px 6px;word-break:break-all;}
@media (max-width:640px){body{padding:20px 12px 48px;}h1{font-size:30px;}ol.papers li{padding:12px 12px;}}
</style><script>
window.MathJax = {
 tex: {
  inlineMath: [['$','$'],['\\(','\\)']],
  // arXiv 摘要常用自定义宏，缺定义会渲染成红色报错；补成常规含义
  macros: { F: '\\mathbb{F}', C: '\\mathbb{C}', R: '\\mathbb{R}',
            Z: '\\mathbb{Z}', Q: '\\mathbb{Q}', N: '\\mathbb{N}',
            HH: '\\mathbb{H}', PP: '\\mathbb{P}', eps: '\\varepsilon',
            vphi: '\\varphi', half: '\\tfrac{1}{2}' }
 },
 options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] },
 startup: { typeset: true }
};
</script>
<script src="../assets/mathjax/es5/tex-svg.js" async onerror="var b=document.createElement('div');b.style.cssText='padding:8px 12px;background:#FDEDE8;border:1px solid #EAC6B8;border-radius:8px;color:#C0392B;font-size:13px;margin:10px 0';b.textContent='公式渲染组件加载失败：请确认 ../assets/mathjax/es5/tex-svg.js 存在（本页需与 assets 目录保持原有相对位置）。';document.currentScript.after(b);"></script>

</head>
<body>
<div class="wrap">
  %s
</div>
</body>
</html>
""" % (favicon, page)


def build_page(items, now, events_block, status_note, source_note):
    rows = []
    for it in items:
        author = it["author"] or "—"
        date = it["date"] or "日期未知"
        rows.append(
            '<li>\n'
            '  <a href="%s" rel="noopener" target="_blank">%s</a>\n'
            '  <div class="meta">%s · %s</div>\n'
            '  <div class="abs">%s</div>\n'
            '</li>'
            % (esc(it["link"]), esc(it["title"]), esc(author), esc(date), esc(it["abs"]))
        )
    papers_html = "\n".join(rows)

    if events_block:
        events_section = (
            '<div class="sec">\n'
            '  <h2>重大事件（人工维护，不受自动更新影响）</h2>\n'
            '  <div class="events">\n%s\n  </div>\n'
            '</div>\n' % events_block
        )
    else:
        events_section = (
            '<div class="sec">\n'
            '  <h2>重大事件</h2>\n'
            '  <div class="events">\n'
            '    <p class="empty">重大事件（如菲尔兹奖、千年难题进展）由人工整理，见'
            '<a href="数学前沿.html">数学前沿 · 重大事件页</a>。</p>\n'
            '  </div>\n'
            '</div>\n'
        )

    inner = (
        '  <p class="crumb"><a href="../00-总览/index.html">← 总览</a> · '
        '<a href="数学前沿.html">数学前沿（重大事件）</a></p>\n'
        '  <h1>论文日报 Σ</h1>\n'
        '  <p class="sub">%s</p>\n'
        '  <p class="status">%s</p>\n\n'
        '  %s\n\n'
        '  <div class="sec">\n'
        '    <h2>最新论文（前 %d 篇）</h2>\n'
        '    <ol class="papers">\n%s\n    </ol>\n'
        '  </div>\n\n'
        '  <div class="sec">\n'
        '    <h2>关于本页</h2>\n'
        '    <div class="note">\n'
        '      <p>本页由 <code>09-前沿动态/数学前沿更新器.py</code> 自动生成：每次运行抓取 arXiv 数学分类最新论文并刷新此页；'
        'arXiv 直连不可达时自动改用 Semantic Scholar 备用数据源，恢复后自动切回。</p>\n'
        '      <p>自动调度：Windows 计划任务「LBLB数学前沿日报」每天执行一次；也可随时运行 <code>python 数学前沿更新器.py</code> 立即更新。</p>\n'
        '      <p>更新失败时保留上一版内容，详情见 <code>09-前沿动态\\_update.log</code>。重大事件区块（<!-- EVENTS:BEGIN --> 与 <!-- EVENTS:END --> 之间）由人工维护，自动更新不会覆盖。</p>\n'
        '    </div>\n'
        '  </div>\n'
    ) % (esc(source_note), esc(status_note), events_section, len(items), papers_html)
    return shell(inner)


def build_placeholder(now):
    inner = (
        '  <p class="crumb"><a href="../00-总览/index.html">← 总览</a> · '
        '<a href="数学前沿.html">数学前沿（重大事件）</a></p>\n'
        '  <h1>论文日报 Σ</h1>\n'
        '  <p class="sub">数据源：arXiv 数学分类（math）· Semantic Scholar（备用）</p>\n'
        '  <p class="status">尚未成功抓取（%s）</p>\n\n'
        '  <div class="sec">\n'
        '    <h2>最新论文</h2>\n'
        '    <div class="waiting">\n'
        '      <p>本页等待首次成功抓取后自动填充最新数学论文。</p>\n'
        '      <p>当前 arXiv 与备用数据源均不可达（可能被临时限流或网络不可达），已按「文明上网」原则停止重试，未生成任何不可靠数据。</p>\n'
        '      <p>请稍后手动运行 <code>python 09-前沿动态/数学前沿更新器.py</code>，'
        '或等待 Windows 计划任务「LBLB数学前沿日报」在下次调度时自动更新。</p>\n'
        '    </div>\n'
        '  </div>\n\n'
        '  <div class="sec">\n'
        '    <h2>关于本页</h2>\n'
        '    <div class="note">\n'
        '      <p>由 <code>09-前沿动态/数学前沿更新器.py</code> 自动管理。</p>\n'
        '      <p>更新日志见 <code>09-前沿动态\\_update.log</code>。</p>\n'
        '      <p>重大事件（菲尔兹奖、千年难题进展等）见<a href="数学前沿.html">数学前沿 · 重大事件页</a>。</p>\n'
        '    </div>\n'
        '  </div>\n'
    ) % now.strftime("%Y-%m-%d %H:%M")
    return shell(inner)


def write_file(path, page):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(page)
    os.replace(tmp, path)


def main():
    demo = "--demo" in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)
    now = datetime.datetime.now()
    old = ""
    if os.path.exists(OUT_FILE):
        try:
            with open(OUT_FILE, "r", encoding="utf-8") as f:
                old = f.read()
        except Exception as e:
            log("读取旧页面失败（忽略）: %s" % e)

    events_block = extract_events_block(old)

    if demo:
        items = DEMO_ITEMS
        source_note = "离线演示模式（--demo）：以下为内置示例数据，未联网抓取。"
        status_note = "演示生成于 %s" % now.strftime("%Y-%m-%d %H:%M")
        log("以 --demo 模式生成页面")
        write_file(OUT_FILE, build_page(items, now, events_block, status_note, source_note))
        write_topic_js({t: fetch_topic_papers(t, c, None, demo=True)
                        for t, c in TOPICS.items()})
        log("演示更新成功：%d 篇 -> %s" % (len(items), OUT_FILE))
        print("DEMO %d items -> %s" % (len(items), OUT_FILE))
        return 0

    opener = build_opener()

    # 第一通道：arXiv 直连（失败即视为整体不可达，主题抓取直接走备用通道，避免逐主题空等）
    items = fetch_arxiv_feeds(opener)
    arxiv_ok = items is not None
    if not arxiv_ok:
        log("arXiv 各端点均不可达，启用 Semantic Scholar 备用通道")

    # 主题数据：arXiv 优先，Semantic Scholar 备用
    topic_data = {}
    for topic, cat in TOPICS.items():
        topic_data[topic] = fetch_topic_papers(topic, cat, opener, arxiv_ok=arxiv_ok)
        time.sleep(1)  # 文明上网：主题间留出间隔
    if any(topic_data.values()):
        write_topic_js(topic_data)
    elif os.path.exists(TOPIC_JS):
        log("主题数据全空，保留旧版 论文数据.js")
    else:
        write_topic_js(topic_data)

    # 日报内容：arXiv 直连成功用之；否则由备用通道主题数据合并去重
    if items is not None:
        source_note = "数据源：arXiv 数学分类（math）RSS/Atom"
    else:
        items = merge_topics(topic_data)
        source_note = ("数据源：Semantic Scholar API（arXiv 直连不可达，已切换备用通道；"
                       "按 12 个数学主题检索合并去重，arXiv 恢复后自动切回）")

    if not items:
        log("所有数据源均失败")
        if os.path.exists(OUT_FILE):
            print("UPDATE_FAILED (kept previous page)")
        else:
            write_file(OUT_FILE, build_placeholder(now))
            log("生成待首次更新占位页")
            print("UPDATE_FAILED (placeholder written)")
        return 1

    status_note = "自动更新于 %s · 共 %d 篇" % (now.strftime("%Y-%m-%d %H:%M"), len(items))
    write_file(OUT_FILE, build_page(items, now, events_block, status_note, source_note))
    log("更新成功：%d 篇（%s）-> %s" % (len(items), "arXiv" if arxiv_ok else "S2", OUT_FILE))
    print("UPDATED %d items -> %s" % (len(items), OUT_FILE))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log("未捕获异常: %r" % e)
        print("ERROR", repr(e))
        sys.exit(2)
