# -*- coding: utf-8 -*-
"""把数据源（题库 .py / 运行时 .js）里数学公式中未转义的 `<` 改成 `&lt;`。

只改「看起来一定是 LaTeX」的片段：片段里必须出现 \ _ ^ { 之一，
避免误伤脚本代码里的 `$` 选择器（那类只出现在 HTML 的 <script> 里，本脚本不处理 HTML）。

用法：
    python tools/fix_data_lt.py          # 只报告
    python tools/fix_data_lt.py --all    # 连「无 LaTeX 标记」的裸比较（$0<x<1$）一起改
    python tools/fix_data_lt.py --fix
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'assets', 'node_modules', '__pycache__'}
BUG = re.compile(r"\$[^$>]{0,300}?<[A-Za-z][^$>]{0,300}?\$")
LATEX_MARK = re.compile(r"[\\_^{}]")

TARGET_DIRS = [os.path.join(ROOT, 'tools', 'bank'), os.path.join(ROOT, '13-应试训练', '123')]
EXT = ('.py', '.js')


def main():
    fix = '--fix' in sys.argv
    allow_all = '--all' in sys.argv
    tot = skip = 0
    files = 0
    for base in TARGET_DIRS:
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in sorted(fn):
                if not f.lower().endswith(EXT):
                    continue
                p = os.path.join(dp, f)
                text = open(p, encoding='utf-8').read()
                positions = []
                skipped = []
                for m in BUG.finditer(text):
                    span, base = m.group(0), m.start()
                    for mm in re.finditer(r"<[A-Za-z]", span):
                        lt = base + mm.start()
                        if text[max(0, lt - 3):lt].endswith('&') or text[max(0, lt - 1):lt] == '\\':
                            continue
                        if LATEX_MARK.search(span) or allow_all:
                            positions.append(lt)
                        else:
                            skipped.append(span[:80].replace('\n', ' '))
                if not positions and not skipped:
                    continue
                files += 1
                rel = os.path.relpath(p, ROOT)
                tot += len(positions)
                skip += len(skipped)
                print('[%s] 修 %d 处%s' % (rel, len(positions),
                                          '，跳过 %d 处' % len(skipped) if skipped else ''))
                for s in skipped[:4]:
                    print('    跳过：%s' % s)
                if fix and positions:
                    chars = list(text)
                    for pos in positions:
                        chars[pos] = '&lt;'
                    open(p, 'w', encoding='utf-8', newline='').write(''.join(chars))

    print('\n合计 %d 个文件：改 %d 处、跳过 %d 处%s' %
          (files, tot, skip, '（已写入）' if fix else '（未改动）'))


if __name__ == '__main__':
    main()
