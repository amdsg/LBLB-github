# -*- coding: utf-8 -*-
"""去掉全站的双语（中文 / English）切换，只保留中文。

背景：assets/i18n.js 会给页面注入语言切换按钮，并用 data-lang="en" 区块存放英文译文。
改成纯中文后必须同时做三件事，否则会退化（中英文同时显示）：
  1) 生成器里不再输出 data-lang="en" / data-i18n 与 i18n.js 的 <script>；
  2) 现有页面里删掉 data-lang="en" 区块、去掉 data-lang 属性、删掉 data-i18n 属性与脚本标签；
  3) 删掉 assets/i18n.js 本体。

用法：
    python tools/remove_i18n.py          # 干跑，只报告
    python tools/remove_i18n.py --apply  # 写入
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '__pycache__'}

SCRIPT = re.compile(r'[ \t]*<script[^>]*src="[^"]*assets/i18n\.js"[^>]*></script>\r?\n?', re.I)
ATTR = re.compile(r'\s+data-i18n="[^"]*"')
OPEN_EN = re.compile(r'<div\b[^>]*\bdata-lang="en"[^>]*>', re.I)
OPEN_ZH = re.compile(r'(<div\b[^>]*?)\s+data-lang="zh"', re.I)


def drop_en_block(text):
    """删除 <div ... data-lang="en"> … </div>（配平，支持嵌套）。"""
    out = []
    pos = 0
    removed = 0
    while True:
        m = OPEN_EN.search(text, pos)
        if not m:
            out.append(text[pos:])
            break
        out.append(text[pos:m.start()])
        depth = 1
        i = m.end()
        for t in re.finditer(r'</?div\b[^>]*>', text[i:], re.I):
            if t.group(0).startswith('</'):
                depth -= 1
            else:
                depth += 1
            if depth == 0:
                i = i + t.end()
                break
        else:
            i = len(text)
        # 连同紧随其后的换行一起吃掉
        while i < len(text) and text[i] in '\r\n':
            i += 1
        removed += 1
        pos = i
    return ''.join(out), removed


def main():
    apply = '--apply' in sys.argv
    stats = []

    # 1) 生成器
    for f in sorted(os.listdir(os.path.join(ROOT, 'tools'))):
        if not f.endswith('.py') or f == 'remove_i18n.py':
            continue
        p = os.path.join(ROOT, 'tools', f)
        t = open(p, encoding='utf-8').read()
        if 'i18n' not in t and 'data-lang' not in t:
            continue
        new = t
        # 双语块 → 只留中文
        new = re.sub(
            r'    has_en = bool\([\s\S]*?\n    else:\n'
            r'        q_html = \'<div class="q">%s</div>\' % p\["q"\]\n'
            r'        ans_html = \'<div class="ans"><b>答案：</b>%s</div>\' % p\["a"\]\n'
            r'        sol_html = \'<div class="sol"><b>详解：</b>%s</div>\' % p\["s"\]\n',
            '    # 只排中文（原先的双语 data-lang 区块已移除）\n'
            '    q_html = \'<div class="q">%s</div>\' % p["q"]\n'
            '    ans_html = \'<div class="ans"><b>答案：</b>%s</div>\' % p["a"]\n'
            '    sol_html = \'<div class="sol"><b>详解：</b>%s</div>\' % p["s"]\n',
            new)
        new = SCRIPT.sub('', new)
        new = ATTR.sub('', new)
        new = re.sub(r'\s*data-lang="(?:zh|en)"', '', new)
        if new != t:
            stats.append(('生成器', os.path.relpath(p, ROOT), t.count('data-lang')))
            if apply:
                open(p, 'w', encoding='utf-8', newline='').write(new)

    # 2) 页面
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if not f.lower().endswith('.html'):
                continue
            p = os.path.join(dp, f)
            t = open(p, encoding='utf-8').read()
            if 'i18n' not in t and 'data-lang' not in t:
                continue
            new, n_en = drop_en_block(t)
            new = SCRIPT.sub('', new)
            new = ATTR.sub('', new)
            new = OPEN_ZH.sub(r'\1', new)
            if new != t:
                stats.append(('页面', os.path.relpath(p, ROOT), n_en))
                if apply:
                    open(p, 'w', encoding='utf-8', newline='').write(new)

    # 3) i18n.js
    i18n = os.path.join(ROOT, 'assets', 'i18n.js')
    if os.path.exists(i18n):
        stats.append(('删除', 'assets/i18n.js', 0))
        if apply:
            os.remove(i18n)

    for kind, rel, n in stats:
        print('%-4s %-52s 英文块=%d' % (kind, rel[:52], n))
    print('\n合计 %d 处（%s）' % (len(stats), '已写入' if apply else '干跑，未写入'))


if __name__ == '__main__':
    main()
