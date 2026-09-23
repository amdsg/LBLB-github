# -*- coding: utf-8 -*-
"""
从桌面那份 9117 人名录生成「数学家名录」页面
============================================
数据体检结论（详见对话记录）：贡献栏 94.6% 是未翻译英文、74.8% 的「中文译名」就是
拉丁原名、19% 的贡献只写「数学家」，达标率仅 0.3%。直接全量搬运等于发布半成品。

因此本生成器只发布**事实性字段**——姓名（原文）、生卒年、国籍/时代、出处链接。
这些是事实，不受著作权保护，也不存在「半成品翻译」问题。
贡献栏只在原文本身已是中文时收录（约 490 条）；英文原文一律不搬，
改为在页面上说明「原文见出处链接」。

用法：python tools/build_math_roster.py
"""
import csv
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"E:\360MoveData\Users\25559\Desktop\数学家\数学家名录_最终版.csv"
OUT_JS = os.path.join(ROOT, "11-数学家", "数学家名录数据.js")


def cjk_ratio(s):
    if not s:
        return 0.0
    return len(re.findall(r"[\u4e00-\u9fff]", s)) / max(1, len(s))


TRIVIAL = re.compile(r"^(一名|一位)?\s*(数学家|M(athematician)?)\s*[。.]?$", re.I)


def norm_nat(n):
    """国籍字段去噪：Unknown/空 归为「未标注」，去掉 /Soviet 之类后缀重复。"""
    n = (n or "").strip()
    if not n or n.lower() in ("unknown", "n/a"):
        return "未标注"
    return n


def era_of(bd):
    """从生卒年粗略推时代，用于分档浏览。"""
    s = bd or ""
    m = re.search(r"(\d{3,4})", s.replace("c.", ""))
    if not m:
        return "年代不详"
    y = int(m.group(1))
    if "BCE" in s.upper() or "前" in s:
        return "公元前"
    if y < 500:
        return "5世纪以前"
    if y < 1400:
        return "中世纪"
    if y < 1600:
        return "文艺复兴"
    if y < 1700:
        return "17世纪"
    if y < 1800:
        return "18世纪"
    if y < 1900:
        return "19世纪"
    if y < 1950:
        return "20世纪上半"
    if y < 2000:
        return "20世纪下半"
    return "当代"


def main():
    with io.open(SRC, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    print("源记录: %d" % len(rows))

    out = []
    n_contrib = 0
    nat_count = {}
    era_count = {}
    for r in rows:
        name = (r["original_name"] or "").strip()
        if not name:
            continue
        cn = (r["chinese_name"] or "").strip()
        # 「中文译名」与原名相同 = 未翻译，不重复展示
        if cn == name:
            cn = ""
        bd = (r["birth_death"] or "").strip()
        nat = norm_nat(r["nationality"])
        src = (r["source"] or "").strip()
        contrib = (r["contributions"] or "").strip()
        # 只保留中文贡献；英文原文不搬
        czh = ""
        if contrib and cjk_ratio(contrib) >= 0.15 and len(contrib) >= 8 and not TRIVIAL.match(contrib):
            czh = contrib
            n_contrib += 1
        nat_count[nat] = nat_count.get(nat, 0) + 1
        era = era_of(bd)
        era_count[era] = era_count.get(era, 0) + 1
        out.append({"n": name, "c": cn, "d": bd, "g": nat, "e": era,
                    "u": src, "k": czh})

    print("导出: %d 人" % len(out))
    print("  含中文贡献: %d (%.1f%%)" % (n_contrib, 100.0 * n_contrib / len(out)))
    print("  国籍种类: %d；时代档: %d" % (len(nat_count), len(era_count)))

    js = ("/* 数学家名录数据（由 tools/build_math_roster.py 生成，勿手改）\n"
          " * 字段：n=外文原名 c=中文译名(仅已译) d=生卒 g=国籍/地区 e=时代档 u=出处链接 k=中文贡献(仅原文为中文时)\n"
          " * 只收录事实性字段；原数据中未翻译的英文贡献不在此列。\n"
          " * 出处与权利归属见 11-数学家/README.md。\n"
          " */\n"
          "window.LBLB_MATH_ROSTER=" + json.dumps(out, ensure_ascii=False,
                                                  separators=(",", ":")) + ";\n")
    io.open(OUT_JS, "w", encoding="utf-8", newline="\n").write(js)
    print("\n写出 %s (%.0f KB)" % (os.path.relpath(OUT_JS, ROOT),
                                  os.path.getsize(OUT_JS) / 1024))

    # 顺带输出分档统计，供页面写死文案
    top_nat = sorted(nat_count.items(), key=lambda kv: -kv[1])[:12]
    print("\n国籍 Top12: %s" % ", ".join("%s %d" % kv for kv in top_nat))
    order = ["公元前", "5世纪以前", "中世纪", "文艺复兴", "17世纪", "18世纪",
             "19世纪", "20世纪上半", "20世纪下半", "当代", "年代不详"]
    print("时代分档: %s" % ", ".join("%s %d" % (k, era_count[k])
                                    for k in order if era_count.get(k)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
