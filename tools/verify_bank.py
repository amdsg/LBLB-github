# -*- coding: utf-8 -*-
"""
逐题验证 tools/bank/*.py 中的答案断言
======================================
每个 bank 文件在**独立子进程**里跑，父进程设硬超时。这样做是因为：
有些符号积分会让 sympy 长时间不返回，没有超时的话一道题就能把整条验证流程挂死，
而且看不出卡在哪里。子进程每做完一题就打印一行，所以超时时能直接定位到具体的题。

用法：
    python tools/verify_bank.py                # 全部
    python tools/verify_bank.py --file 13-exam-cmc.py
    python tools/verify_bank.py --timeout 60   # 每个文件的超时秒数
"""
import argparse
import io
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BANK_DIR = os.path.join(HERE, "bank")
RUNNER = os.path.join(HERE, "_bank_runner.py")


def run_one(path, fname, timeout):
    """在子进程里验证一个 bank 文件，返回 (topic, section, 总数, 通过数, 失败列表)。"""
    proc = subprocess.Popen(
        [sys.executable, RUNNER, path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=ROOT, text=True, encoding="utf-8", bufsize=1)

    topic, section, total = fname, "core", 0
    cur = None
    ok_count = 0
    fails = []
    struct = []
    done = False
    deadline = time.time() + timeout

    for line in proc.stdout:
        line = line.rstrip("\n")
        parts = line.split("\t")
        kind = parts[0]
        if kind == "META":
            topic, section, total = parts[1], parts[2], int(parts[3])
        elif kind == "STRUCT":
            struct.append(parts[1])
            fails.append(("(结构)", parts[1], ""))
        elif kind == "BEGIN":
            cur = parts[1]
        elif kind == "RESULT":
            pid, ok, dt, why = parts[1], parts[2] == "1", parts[3], parts[4]
            if ok:
                ok_count += 1
                if float(dt) > 3:
                    print("  （慢）%s 用时 %ss" % (pid, dt))
            else:
                fails.append((pid, why, ""))
        elif kind == "DONE":
            done = True
            break
        if time.time() > deadline:
            break

    if not done:
        try:
            proc.kill()
        except Exception:
            pass
        fails.append((cur or "?", "整个文件验证超时（>%ds），上一题未完成" % timeout, ""))

    try:
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

    err = proc.stderr.read() if proc.stderr else ""
    if err and not fails:
        fails.append(("(stderr)", err.strip()[-300:], ""))

    return topic, section, total, ok_count, fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--timeout", type=int, default=240,
                    help="单个 bank 文件的超时秒数（默认 240）")
    args = ap.parse_args()

    files = sorted(f for f in os.listdir(BANK_DIR)
                   if f.endswith(".py") and not f.startswith("_"))
    if args.file:
        files = [f for f in files if f == args.file]
        if not files:
            print("找不到 bank 文件: %s" % args.file)
            return 2

    grand_ok = 0
    grand_total = 0
    grand_fail = []
    for fn in files:
        topic, section, total, ok, fails = run_one(
            os.path.join(BANK_DIR, fn), fn, args.timeout)
        grand_ok += ok
        grand_total += total
        print("\n== %s（%s / %s，%d 题）==" % (topic, fn, section, total))
        for pid, why, _q in fails:
            print("  FAIL %-8s %s" % (pid, why[:90]))
        print("   通过 %d / %d" % (ok, total))
        grand_fail.extend((topic, p, w) for p, w, _ in fails)

    print("\n" + "=" * 70)
    print("总计通过 %d 题，失败 %d 题" % (grand_ok, len(grand_fail)))
    if grand_fail:
        print("失败清单：")
        for topic, pid, why in grand_fail:
            print("  %s %s : %s" % (topic, pid, why[:80]))
    return 1 if grand_fail else 0


if __name__ == "__main__":
    sys.exit(main())
