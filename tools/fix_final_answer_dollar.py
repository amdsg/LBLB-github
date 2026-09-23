# -*- coding: utf-8 -*-
"""修补考研 123 解析页「答案块」里未收尾的 $$。

分两类（判据：最后一个 $$ 之后、剔除 \\text{...} 内容后，是否还有中文散文）：
  A. 没有散文 → 这个 $$ 是漏了收尾，算式一直排到块尾 → 在块尾补一个 $$。
  B. 还有散文 → 这个 $$ 是写错了，本该是行内公式 → 把该 $$ 改成 $，
     并在「答案：」之后补一个开头的 $（仅当答案正文紧接就是数学内容时才这么改）。

只动 <div class="final-answer">…</div>，不碰其它结构。

用法： python tools/fix_final_answer_dollar.py [--fix]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import audit_pages as ap

BLOCK = re.compile(r'<div class="final-answer">([\s\S]*?)</div>', re.I)
ANS = re.compile(r'答案[：:]')
TEXTARG = re.compile(r'\\text\s*\{[^{}]*\}')
CJK = re.compile(r'[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]')


def decide(inner):
    """返回 ('A'|'B'|None, 说明)"""
    plain = ap.unescape_entities(ap.strip_tags(inner))
    if not ap.find_unpaired(plain):
        return None, '已配对'
    if plain.count('$$') % 2 == 0:
        return None, '$$ 数为偶数，交人工'
    after = plain.rsplit('$$', 1)[1]
    if CJK.search(TEXTARG.sub('', after)):
        # B：$$ 之后还有散文
        m = ANS.search(inner)
        if not m:
            return None, '找不到「答案：」'
        nxt = inner[m.end():m.end() + 1]
        if not (nxt.isascii() and (nxt.isalpha() or nxt == '\\')):
            return None, '答案正文不是紧接数学，交人工'
        return 'B', '收尾 $$ -> $，并在答案后开 $'
    return 'A', '块尾补 $$'


def main():
    fix = '--fix' in sys.argv
    rows = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, '13-应试训练', '123', '考研')):
        for f in sorted(fn):
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            html = open(p, encoding='utf-8').read()
            plans = []

            def repl(m):
                inner = m.group(1)
                kind, why = decide(inner)
                if kind is None:
                    if why != '已配对':
                        rows.append((os.path.relpath(p, ROOT), 'SKIP', why))
                    return m.group(0)
                if kind == 'A':
                    new = inner + '$$'
                else:
                    k = inner.rfind('$$')
                    new = inner[:k] + '$' + inner[k + 2:]
                    mm = ANS.search(new)
                    new = new[:mm.end()] + '$' + new[mm.end():]
                plans.append((kind, inner[-90:], new[-90:]))
                return m.group(0).replace(inner, new)

            new_html = BLOCK.sub(repl, html)
            if plans:
                rows.append((os.path.relpath(p, ROOT), 'FIX', plans))
                if fix:
                    open(p, 'w', encoding='utf-8', newline='').write(new_html)

    nfix = 0
    for rel, tag, payload in rows:
        if tag == 'FIX':
            nfix += 1
            print('[%s] %s' % (rel, ' / '.join(k for k, _, _ in payload)))
            for k, before, after in payload:
                print('    前: %s' % repr(before))
                print('    后: %s' % repr(after))
        else:
            print('[%s] 跳过：%s' % (rel, payload))
    print('\n改动 %d 个页面（%s）' % (nfix, '已写入' if fix else '干跑，未写入'))


if __name__ == '__main__':
    main()
