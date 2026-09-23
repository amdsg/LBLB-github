# -*- coding: utf-8 -*-
"""
原创题库 · 数据结构与验证工具
==============================
题库以 Python 数据形式定义（tools/bank/*.py），每道题带一个 `check` 表达式，
由本模块用 sympy 求值验证。只有 verify 全部通过的题才会被写进页面，
所以页面上的「答案经符号计算验证」是名副其实的。

题目对象字段：
    id       str   题号，如 "L01"
    q        str   题干（LaTeX，行内用 $...$）
    a        str   参考答案（LaTeX）
    s        str   详解（LaTeX，可空）
    check    str   用 sympy 验证答案的表达式，求值须为真
    tags     list  知识点标签
    level    int   难度 1..5

check 表达式可用的名字：
    x y z t n m a b c k   sympy Symbol（默认实数域，a/b/c 为正）
    pi E oo               sympy 常量
    sin cos tan exp log sqrt Rational Integral Sum Limit Derivative
    simplify limit integrate diff solve Eq dsolve series apart together
    zero(e)               e 化简为 0 则真
    eq(a, b)              a-b 化简为 0 则真
    approx(a, b)          数值近似相等（用于无法符号化简的情形）
"""
import re

import sympy as sp
from sympy import (Symbol, symbols, pi, E, oo, I, Rational, sqrt, exp, log,
                   sin, cos, tan, cot, sec, csc, asin, acos, atan,
                   sinh, cosh, tanh, limit, integrate, diff, series, solve,
                   Eq, dsolve, Function, sqrt, binomial, factorial, gamma,
                   Matrix, det, eye, simplify, factor, expand, apart,
                   together, cancel, nsimplify, Sum, oo, floor, ceiling,
                   S, Abs, sign, Min, Max, Piecewise, oo,
                   totient, gcd, lcm, isprime, divisor_count, divisor_sigma,
                   factorint, nextprime, primerange, beta)

x, y, z, t = symbols("x y z t", real=True)
r, u, v, w = symbols("r u v w", real=True)
n, m, k = symbols("n m k", positive=True, integer=True)
a, b, c = symbols("a b c", positive=True)
f = Function("f")
g = Function("g")

_NS = {
    "x": x, "y": y, "z": z, "t": t, "r": r, "u": u, "v": v, "w": w,
    "n": n, "m": m, "k": k,
    "a": a, "b": b, "c": c, "f": f, "g": g,
    "pi": pi, "E": E, "oo": oo, "I": I,
    "all": all, "any": any, "abs": abs, "len": len, "range": range,
    "int": int, "float": float, "round": round, "sorted": sorted, "sum": sum,
    "sin": sin, "cos": cos, "tan": tan, "cot": cot, "sec": sec, "csc": csc,
    "asin": asin, "acos": acos, "atan": atan,
    "sinh": sinh, "cosh": cosh, "tanh": tanh,
    "exp": exp, "log": log, "sqrt": sqrt, "Abs": Abs, "Rational": Rational,
    "limit": limit, "integrate": integrate, "diff": diff, "series": series,
    "solve": solve, "Eq": Eq, "dsolve": dsolve, "Function": Function,
    "binomial": binomial, "factorial": factorial, "gamma": gamma,
    "Matrix": Matrix, "det": det, "eye": eye,
    "simplify": simplify, "factor": factor, "expand": expand,
    "apart": apart, "together": together, "cancel": cancel,
    "nsimplify": nsimplify, "Sum": Sum, "S": S,
    "floor": floor, "ceiling": ceiling, "sign": sign, "Min": Min, "Max": Max,
    "Piecewise": Piecewise,
    # 数论与计数
    "totient": totient, "gcd": gcd, "lcm": lcm, "isprime": isprime,
    "divisor_count": divisor_count, "divisor_sigma": divisor_sigma,
    "factorint": factorint, "nextprime": nextprime, "primerange": primerange,
    "pow": pow, "beta": beta,
    # 数值积分核对（mpmath）：处理 sympy 符号积分卡死或过慢的经典积分
    "mp": None,          # 占位，下面赋 mpmath 模块
    "nq": None,          # 占位
}

try:
    import mpmath as _mpmath
    _NS["mp"] = _mpmath

    def nq(fn, a, b, expected, eps=1e-12, tol=1e-6):
        """数值核对 ∫_a^b fn(x) dx ≈ expected。

        用 mpmath.quad（tanh-sinh 求积），端点略缩进 eps 以容忍可积奇点
        （如 ln(sin x) 在 0 处），容差 tol。适合 sympy 符号积分会卡死的
        经典定积分（∫ln(sin x)、∫ln x/(1+x²) 等）。
        """
        try:
            lo, hi = a + eps, b
            got = _mpmath.quad(fn, [lo, hi])
            return abs(complex(got) - complex(expected)) < tol
        except Exception:
            return False

    _NS["nq"] = nq
except ImportError:                                     # pragma: no cover
    pass


def zero(e):
    """e 是否为 0。

    依次尝试多种化简策略（普通化简、展开、三角化简、化为指数形式），
    都不成功时再在若干远离奇点的点上做数值抽查。
    """
    try:
        e = sp.sympify(e)
    except Exception:
        return False
    if e == 0:
        return True

    # 矩阵：逐元素判断是否全零（sympy 的 Matrix 不能直接参与 simplify/数值抽查）
    if isinstance(e, sp.MatrixBase):
        try:
            return all(zero(v) for v in e)
        except Exception:
            return False

    strategies = [
        lambda v: sp.simplify(v),
        lambda v: sp.simplify(sp.expand(v)),
        lambda v: sp.trigsimp(v),
        # 三角恒等式（如 sin t/(1-cos t) = cot(t/2)）常需要化到指数形式才能约掉
        lambda v: sp.simplify(v.rewrite(sp.exp)),
        lambda v: sp.simplify(sp.cancel(v)),
    ]
    for fn in strategies:
        try:
            if fn(e) == 0:
                return True
        except Exception:
            continue

    # 数值抽查：在若干远离奇点的点上求值
    try:
        free = sorted(e.free_symbols, key=lambda s: s.name)
        if not free:
            # 无自由符号：sympy 有时只给出 RootSum 这类形式（如含 arctan 的定积分），
            # 符号化简不掉但数值相等，所以这里按容差判断而不是精确等于 0
            return abs(complex(e.evalf(40))) < 1e-20
        import random
        random.seed(20260101)
        for _ in range(8):
            sub = {s: sp.Rational(random.randint(2, 9), random.randint(1, 5))
                   for s in free}
            v = complex(e.subs(sub).evalf(30))
            if abs(v) > 1e-18:
                return False
        return True
    except Exception:
        return False


def eq(a_, b_):
    return zero(sp.sympify(a_) - sp.sympify(b_))


def approx(a_, b_, tol=1e-12):
    try:
        return abs(complex((sp.sympify(a_) - sp.sympify(b_)).evalf(40))) < tol
    except Exception:
        return False


def is_oo(e):
    """e 是否为 +∞（用于判断级数发散）。

    注意 eq(x, oo) 不行：oo - oo = nan，判断会失败。
    """
    try:
        e = sp.sympify(e)
    except Exception:
        return False
    if e is sp.oo or e == sp.oo:
        return True
    try:
        e = e.doit()
    except Exception:
        pass
    if e is sp.oo or e == sp.oo:
        return True
    try:
        return bool(e.is_infinite and e.is_positive)
    except Exception:
        return False


def eq_in(series_expr, closed_expr, xval):
    """幂级数与闭式在收敛域内一点处比较。

    Sum(...).doit() 对含参幂级数常返回 Piecewise（附带 |x|<1 这类收敛条件），
    无法直接与闭式相等比较。这里取收敛域内一个具体点代入后比较数值，
    等价于「在收敛域内两者相等」的抽查。
    """
    try:
        s = sp.sympify(series_expr).subs(x, xval)
        try:
            s = s.doit()
        except Exception:
            pass
        c = sp.sympify(closed_expr).subs(x, xval)
        return abs(complex(s.evalf(30)) - complex(c.evalf(30))) < 1e-14
    except Exception:
        return False


def diverges(s):
    """级数是否发散。

    比 is_oo(doit()) 更可靠：像 Σ1/√n 这种 sympy 给不出闭式的级数，
    doit() 会原样返回未求值的 Sum，但 is_convergent() 能正确判定为 False。

    注意 is_convergent() 返回的是 sympy 的 S.false / S.true 或 None，
    S.false 打印出来和 False 一样却不是同一个对象，必须用 is sp.false 判断。
    """
    try:
        r = sp.sympify(s).is_convergent()
    except Exception:
        return False
    return r is False or r is sp.false


def converges(s):
    """级数是否收敛（判定不出时返回 False，不会把 None 当成收敛）。"""
    try:
        r = sp.sympify(s).is_convergent()
    except Exception:
        return False
    return r is True or r is sp.true


_NS.update({"zero": zero, "eq": eq, "approx": approx,
            "is_oo": is_oo, "eq_in": eq_in,
            "diverges": diverges, "converges": converges})
# check 表达式是仓库自带的题目数据，不是外部输入；这里仍不放行内建函数，
# 只允许上面显式列出的名字与少量白名单函数。
_NS["__builtins__"] = {}


def run_check(expr):
    """执行 check 表达式，返回 (是否通过, 说明)。

    注意必须把符号表同时作为 globals 传入：check 里常用
    all(... for ...) 这类生成器表达式，而生成器有自己的函数作用域，
    只查 globals 不查 eval 的 locals，名字表若只放在 locals 就会 NameError。
    """
    try:
        val = eval(expr, _NS)
    except Exception as e:
        return False, "求值异常: %r" % (e,)
    if val is True or val is sp.true or val == True:  # noqa: E712
        return True, ""
    if val is False or val is sp.false or val == False:  # noqa: E712
        return False, "断言为假"
    # sympy 关系式：尝试判定真假
    try:
        if val == sp.true:
            return True, ""
        if val == sp.false:
            return False, "关系式为假"
    except Exception:
        pass
    return False, "返回非布尔值: %r" % (val,)


def _check_says_divergent(check):
    """断言是否在「把某个极限值判定为 oo」。

    只认 eq(<表达式>, oo) 这一种写法。不认 is_oo(...)/diverges(...)，
    因为那两者用于「判断级数敛散」的题，答案天然是「收敛/发散」或「R=0」这类
    表述，把它们算进来会产生误报（例如求收敛半径 R=0 的题，断言里出现的 ∞
    只是比值极限，不是答案本身）。
    """
    c = (check or "").strip()
    return re.search(r",\s*oo\s*\)$", c) is not None


_ANSWER_INF_WORDS = ("∞", "发散", "不存在", "无界")


def validate(problems, topic):
    """校验一组题目的结构完整性。"""
    errs = []
    seen = set()
    for i, p in enumerate(problems, 1):
        pid = p.get("id")
        for key in ("id", "q", "a", "check"):
            if not p.get(key):
                errs.append("%s #%d 缺字段 %s" % (topic, i, key))
        if pid in seen:
            errs.append("%s 题号重复: %s" % (topic, pid))
        seen.add(pid)
        lv = p.get("level", 3)
        if not isinstance(lv, int) or not 1 <= lv <= 5:
            errs.append("%s %s 难度越界: %r" % (topic, pid, lv))

        # 英文是可选字段，但要么齐全、要么都没有——只写一半会让英文界面出现空块
        en = [k for k in ("q_en", "a_en", "s_en") if p.get(k)]
        if en and len(en) != 3:
            errs.append("%s %s 英文字段不成套（缺 %s）"
                        % (topic, pid,
                           ", ".join(k for k in ("q_en", "a_en", "s_en")
                                     if not p.get(k))))

        # 答案文字与断言的一致性：
        # 断言判定发散，答案里却给了一个有限值——多半是手写答案时写岔了。
        # 验证器只跑 check，不会发现这种矛盾，所以单独查一遍。
        for suffix in ("", "_en"):
            a_txt = p.get("a" + suffix) or ""
            if suffix and not a_txt:
                continue
            if _check_says_divergent(p.get("check")) and not any(
                    w in a_txt for w in _ANSWER_INF_WORDS):
                errs.append("%s %s 断言判定发散/无穷，但答案%s未体现：%r"
                            % (topic, pid, suffix or "", a_txt[:60]))
    return errs


def _timed_worker(expr, q):
    try:
        q.put(run_check(expr))
    except Exception as e:                                   # pragma: no cover
        q.put((False, "子进程异常: %r" % (e,)))


def run_check_timed(expr, timeout=25):
    """带超时的 run_check。

    有些符号积分（例如 ∫₀^{π/2} ln(sin x) dx、∫₀^∞ ln x/(1+x²) dx）会让 sympy
    长时间甚至永远不返回。没有超时的话，一道题就能把整条验证流水线挂死，
    而且看不出是哪一道——所以每题放到子进程里跑，超时就判该题失败并给出提示。
    """
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=_timed_worker, args=(expr, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join(2)
        return False, "验证超时（>%d 秒）——请简化该题的断言，或改成数值核对" % timeout
    try:
        return q.get_nowait()
    except Exception:
        return False, "子进程未返回结果"


def verify(problems, topic, verbose=False, timeout=25):
    """逐题验证，返回 (通过数, 失败列表)。每题带超时。"""
    ok = 0
    fails = []
    for p in problems:
        passed, why = run_check_timed(p["check"], timeout=timeout)
        if passed:
            ok += 1
            if verbose:
                print("  OK   %-6s %s" % (p["id"], p.get("q", "")[:56]))
        else:
            fails.append((p["id"], why, p.get("q", "")[:70]))
            print("  FAIL %-6s %s\n       %s" % (p["id"], p.get("q", "")[:70], why))
    return ok, fails
