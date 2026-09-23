# -*- coding: utf-8 -*-
"""
检查哪些文件会被发布、哪些被 .gitignore 排除
=============================================
用途：在 `git add .` 之前先看清结果。本仓库默认**不发布**真题数据与试卷 PDF
（权利人是教育部考试中心、竞赛工作组、各高校与各省考试院，未给出再分发授权），
但文件仍在你磁盘上，本地页面照常可用。

用法：
    python tools/check_tracked.py            # 汇总
    python tools/check_tracked.py --list     # 列出被排除的文件
"""
import argparse
import fnmatch
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITIGNORE = os.path.join(ROOT, ".gitignore")

# 这些目录永远不参与（GitHub 也不该有）
SKIP_DIRS = {".git", "__pycache__"}


def load_patterns():
    pats = []
    with open(GITIGNORE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pats.append(line.replace("\\", "/"))
    return pats


def is_ignored(rel, patterns):
    """按 .gitignore 的常见语义做匹配（够用即可，不追求完整实现）。"""
    rel = rel.replace("\\", "/")
    for pat in patterns:
        p = pat.rstrip("/")
        if fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(rel, p + "/*"):
            return pat
        # 目录规则：前缀匹配
        if pat.endswith("/") and (rel + "/").startswith(pat):
            return pat
        if "/" in p and rel.startswith(p + "/"):
            return pat
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    patterns = load_patterns()
    tracked, ignored = [], {}
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT)
            hit = is_ignored(rel, patterns)
            if hit:
                ignored.setdefault(hit, []).append((rel, os.path.getsize(full)))
            else:
                tracked.append((rel, os.path.getsize(full)))

    ts = sum(s for _r, s in tracked)
    isum = sum(s for lst in ignored.values() for _r, s in lst)

    # 统一成正斜杠再比对，否则 Windows 下反斜杠会让下面的检查全部误判
    tset = {r.replace("\\", "/") for r, _s in tracked}
    iset = {r.replace("\\", "/") for lst in ignored.values() for r, _s in lst}

    print("=" * 68)
    print("会被发布（git add 收录）: %d 个文件, %.1f MB" % (len(tracked), ts / 1048576))
    print("不会发布（被忽略）      : %d 个文件, %.1f MB"
          % (sum(len(v) for v in ignored.values()), isum / 1048576))
    print("合计                    : %.1f MB" % ((ts + isum) / 1048576))
    print("=" * 68)

    print("\n被忽略的组成:")
    for pat, lst in sorted(ignored.items(), key=lambda kv: -sum(s for _r, s in kv[1])):
        print("  %-38s %4d 个  %8.1f MB" % (pat, len(lst), sum(s for _r, s in lst) / 1048576))

    # 抽查关键文件是否仍在发布清单里
    must_track = [
        "13-应试训练/123/试卷清单.js",
        "13-应试训练/123/_papers.json",
        "13-应试训练/题库来源与授权.md",
        "14-自测题库/index.html",
        "15-应试实战/index.html",
        "tools/check_tracked.py",
    ]
    print("\n关键文件发布状态:")
    for m in must_track:
        print("  %-42s %s" % (m, "发布" if m in tset else "!! 未发布"))

    # 抽查关键排除
    must_ignore = [
        "13-应试训练/123/真题卷.js",
        "13-应试训练/123/题库-汇总.js",
        "13-应试训练/123/考研/数一/1987-数学一-原题.html",
        "13-应试训练/123/练习题/华东师范大学/2023_练习题_华东师范大学_高等数学B期末B卷.pdf",
    ]
    print("\n关键文件排除状态:")
    for m in must_ignore:
        print("  %-42s %s" % (m, "已排除" if m in iset else "!! 仍会发布"))

    if args.list:
        print("\n被排除的文件清单:")
        for pat, lst in sorted(ignored.items()):
            print("\n[%s]" % pat)
            for r, s in lst[:40]:
                print("   %-70s %8.1f KB" % (r[:70], s / 1024))
            if len(lst) > 40:
                print("   … 其余 %d 个" % (len(lst) - 40))
    return 0


if __name__ == "__main__":
    sys.exit(main())
