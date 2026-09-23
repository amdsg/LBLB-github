# -*- coding: utf-8 -*-
r"""
LBLB 经典难题 · 自动更新器（仿 数学前沿更新器.py）
====================================================
- 读取 经典难题数据.js（window.CLASSIC_PROBLEMS.conjectures）
- 对每个带 query 的条目，向 arXiv API 查询最近论文（每项最多 3 篇），
  转成字符串并入 key_papers（按链接去重，最多保留 8 条），并刷新 last_update
- status（未解决/部分解决/已解决）与 content/progress 由人工维护，更新器不自动改判
- 文明上网：仅标准库、带身份 UA、超时 25s、每项间隔 2.5s、失败即保留旧数据不覆盖
- 本地离线运行；联网时才会真正请求 arXiv
用法：
  python 经典难题更新器.py            # 正常更新（联网抓取 arXiv）
  python 经典难题更新器.py --demo     # 离线演示：只刷新 last_update，不联网
  python 经典难题更新器.py --once "p_vs_np"   # 只更新指定 id（调试用）
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "经典难题数据.js")
LOG = os.path.join(BASE, "_update.log")
ARXIV_API = "http://export.arxiv.org/api/query"
UA = "Mozilla/5.0 (LBLB-ClassicProblems-Updater/1.0; +local math hub, civilized requests)"
NS = {"atom": "http://www.w3.org/2005/Atom"}
MAX_RECENT = 3     # 每项取最近论文数
PAPER_CAP = 8     # key_papers 最多保留条数

HEADER = (
    "/* 经典难题与猜想数据（LBLB）\n"
    " * window.CLASSIC_PROBLEMS = { conjectures: [...] }\n"
    " * 字段：id / name / status / content(支持 $LaTeX$) / progress / key_papers / last_update / query\n"
    " * status 取值：'未解决' | '部分解决' | '已解决'\n"
    " * 状态结论由人工维护；key_papers 中的「最新论文」与 last_update 由 经典难题更新器.py 从 arXiv 自动刷新。\n"
    " */"
)


def log(msg):
    line = "[%s] %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def read_data():
    with open(DATA, "r", encoding="utf-8") as f:
        text = f.read()
    # 行首锚定，避免误匹配文件头注释里的示例写法
    m = re.search(r"^window\.CLASSIC_PROBLEMS\s*=\s*(\{.*\});\s*$", text, re.S | re.M)
    if not m:
        raise ValueError("无法在 经典难题数据.js 中定位 window.CLASSIC_PROBLEMS 赋值")
    return json.loads(m.group(1))


def write_data(obj):
    body = "window.CLASSIC_PROBLEMS = " + json.dumps(obj, ensure_ascii=False, indent=1) + ";\n"
    tmp = DATA + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(HEADER + "\n" + body)
    os.replace(tmp, DATA)


def fetch_arxiv(query, max_results=MAX_RECENT):
    """返回 [str]，每条形如 'A. Author, B. Author (2024). Title. https://arxiv.org/abs/xxxx'。
    失败抛异常，由调用方保留旧数据。"""
    params = urllib.parse.urlencode({
        "search_query": 'all:"%s"' % query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    req = urllib.request.Request(ARXIV_API + "?" + params, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as resp:
        xml_text = resp.read().decode("utf-8", "replace")
    root = ET.fromstring(xml_text)
    out = []
    for entry in root.findall("atom:entry", NS):
        title = re.sub(r"\s+", " ", (entry.findtext("atom:title", "", NS) or "").strip())
        published = (entry.findtext("atom:published", "", NS) or "")[:10]
        year = published[:4]
        authors = []
        for a in entry.findall("atom:author", NS):
            nm = a.findtext("atom:name", "", NS)
            if nm:
                authors.append(nm.strip())
        link = ""
        for lk in entry.findall("atom:link", NS):
            if lk.get("rel") == "alternate" and lk.get("href"):
                link = lk.get("href")
                break
        if not title or not year:
            continue
        who = ", ".join(authors[:3])
        if len(authors) > 3:
            who += " 等"
        s = "%s (%s). %s." % (who, year, title[:160])
        if link:
            s += " " + link
        out.append(s)
    return out


def update_one(it, today, demo):
    q = (it.get("query") or "").strip()
    if not q:
        return "skip"
    if demo:
        it["last_update"] = today
        return "demo"
    try:
        recent = fetch_arxiv(q)
    except Exception as e:
        # 失败保留旧数据：不覆盖 key_papers，也不把 last_update 改成失败当天之外的东西
        log("  FAIL %s：%s（保留旧数据）" % (it.get("name"), e))
        return "fail"
    old = list(it.get("key_papers") or [])
    seen = set()
    merged = []
    for p in old + recent:
        m = re.search(r"(https?://\S+)", p)
        key = m.group(1) if m else p
        if key in seen:
            continue
        seen.add(key)
        merged.append(p)
    it["key_papers"] = merged[:PAPER_CAP]
    it["last_update"] = today
    return "ok(%d)" % len(recent)


def main():
    demo = "--demo" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--once="):
            only = a.split("=", 1)[1]
    obj = read_data()
    items = obj.get("conjectures", [])
    today = datetime.date.today().isoformat()
    stats = {"ok": 0, "fail": 0, "skip": 0, "demo": 0}
    for i, it in enumerate(items):
        if only and it.get("id") != only:
            continue
        r = update_one(it, today, demo)
        if r.startswith("ok"):
            stats["ok"] += 1
            log("[%02d/%02d] %s：%s" % (i + 1, len(items), it.get("name"), r))
        elif r == "fail":
            stats["fail"] += 1
        elif r == "demo":
            stats["demo"] += 1
        else:
            stats["skip"] += 1
        if not demo and not only:
            time.sleep(2.5)  # 文明上网：条目之间留间隔
    obj["updatedAt"] = today
    write_data(obj)
    log("完成：成功 %d / 失败 %d / 跳过 %d / demo %d，共 %d 条；updatedAt=%s"
        % (stats["ok"], stats["fail"], stats["skip"], stats["demo"], len(items), today))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log("更新器异常：%r（数据未改动）" % e)
        print("ERROR", repr(e))
        sys.exit(1)
