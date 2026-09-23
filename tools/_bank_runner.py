# -*- coding: utf-8 -*-
"""
题库断言求值器（子进程入口）
============================
供 tools/verify_bank.py 在独立子进程里调用：给定一个 bank 文件，逐题求值断言，
每完成一题就往 stdout 打一行结果并立即 flush。

为什么要单独起进程：某些符号积分会让 sympy 长时间不返回。放在子进程里跑，
父进程就能设硬超时；配合「做完一题就打印一行」，超时时还能直接看出卡在哪一题。

用法（由 verify_bank.py 调用，一般不直接手跑）：
    python tools/_bank_runner.py <bank文件路径>
"""
import importlib.util
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_kit  # noqa: E402


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: _bank_runner.py <bank file>\n")
        return 2
    path = sys.argv[1]

    spec = importlib.util.spec_from_file_location(
        "bankmod_" + os.path.basename(path).replace("-", "_")[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    probs = getattr(mod, "PROBLEMS", [])
    topic = getattr(mod, "TOPIC", os.path.basename(path))
    section = getattr(mod, "SECTION", "core")
    out = sys.stdout

    out.write("META\t%s\t%s\t%d\n" % (topic, section, len(probs)))
    out.flush()

    # 结构校验（快，先做）
    for e in bank_kit.validate(probs, topic):
        out.write("STRUCT\t%s\n" % e)
    out.flush()

    for p in probs:
        pid = p.get("id", "?")
        out.write("BEGIN\t%s\t%s\n" % (pid, (p.get("q") or "")[:70].replace("\t", " ")))
        out.flush()
        t0 = time.time()
        ok, why = bank_kit.run_check(p["check"])
        out.write("RESULT\t%s\t%d\t%.2f\t%s\n"
                  % (pid, 1 if ok else 0, time.time() - t0,
                     (why or "").replace("\t", " ").replace("\n", " ")))
        out.flush()
    out.write("DONE\n")
    out.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
