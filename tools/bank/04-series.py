# -*- coding: utf-8 -*-
"""原创题库 · 无穷级数"""
TOPIC = "无穷级数"

PROBLEMS = [
    dict(id="S01", level=1, tags=["几何级数"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{2^{n}}$。",
         a=r"$1$",
         s=r"首项 $\frac12$、公比 $\frac12$ 的几何级数，和为 $\frac{1/2}{1-1/2}=1$。",
         check=r"eq(Sum(1/2**n, (n, 1, oo)).doit(), 1)"),

    dict(id="S02", level=2, tags=["巴塞尔问题"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{2}}$。",
         a=r"$\dfrac{\pi^{2}}{6}$",
         s=r"巴塞尔问题，欧拉 1735 年首次求出该值。也可由 $\sin x$ 的无穷乘积展开得到。",
         check=r"eq(Sum(1/n**2, (n, 1, oo)).doit(), pi**2/6)"),

    dict(id="S03", level=2, tags=["裂项相消"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+1)}$。",
         a=r"$1$",
         s=r"$\frac{1}{n(n+1)}=\frac1n-\frac{1}{n+1}$，前 $N$ 项和为 $1-\frac{1}{N+1}\to1$。",
         check=r"eq(Sum(1/(n*(n+1)), (n, 1, oo)).doit(), 1)"),

    dict(id="S04", level=3, tags=["交错级数"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}$。",
         a=r"$\ln 2$",
         s=r"这是 $\ln(1+x)$ 在 $x=1$ 处的展开（由 Abel 定理保证收敛到该值）。",
         check=r"eq(Sum((-1)**(n+1)/n, (n, 1, oo)).doit(), log(2))"),

    dict(id="S05", level=2, tags=["指数级数"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n!}$。",
         a=r"$e-1$",
         s=r"由 $e=\sum_{n=0}^{\infty}\frac{1}{n!}$ 减去 $n=0$ 项（等于 1）。",
         check=r"eq(Sum(1/factorial(n), (n, 1, oo)).doit(), E-1)"),

    dict(id="S06", level=3, tags=["奇子列"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{(2n-1)^{2}}$。",
         a=r"$\dfrac{\pi^{2}}{8}$",
         s=r"把 $\sum\frac{1}{n^{2}}=\frac{\pi^{2}}{6}$ 拆成奇数项与偶数项：偶数项之和 $=\frac14\cdot\frac{\pi^{2}}{6}$，"
           r"故奇数项之和 $=\frac{\pi^{2}}{6}-\frac{\pi^{2}}{24}=\frac{\pi^{2}}{8}$。",
         check=r"eq(Sum(1/(2*n-1)**2, (n, 1, oo)).doit(), pi**2/8)"),

    dict(id="S07", level=3, tags=["收敛半径", "比值判别法"], q=r"求幂级数 $\displaystyle\sum_{n=1}^{\infty}\frac{x^{n}}{n}$ 的收敛半径。",
         a=r"$R=1$",
         s=r"$a_n=\frac1n$，$\lim\left|\frac{a_{n+1}}{a_n}\right|=\lim\frac{n}{n+1}=1$，故 $R=1$；端点 $x=\pm1$ 处分别条件收敛、发散。",
         check=r"eq(limit((1/(n+1))/(1/n), n, oo), 1)"),

    dict(id="S08", level=3, tags=["收敛半径"], q=r"求幂级数 $\displaystyle\sum_{n=0}^{\infty}\frac{x^{n}}{n!}$ 的收敛半径。",
         a=r"$R=+\infty$",
         s=r"$\lim\left|\frac{a_{n+1}}{a_n}\right|=\lim\frac{1}{n+1}=0$，故收敛半径无穷（即 $e^{x}$ 的展开）。",
         check=r"eq(limit((1/factorial(n+1))/(1/factorial(n)), n, oo), 0)"),

    dict(id="S09", level=2, tags=["p 级数", "发散"], q=r"判断 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{\sqrt n}$ 的敛散性。",
         a=r"发散（$p=\frac12\le1$）",
         s=r"$p$ 级数 $\sum\frac{1}{n^{p}}$ 在 $p\le1$ 时发散、$p>1$ 时收敛。这里 $p=\frac12$。",
         check=r"diverges(Sum(1/sqrt(n), (n, 1, oo)))"),

    dict(id="S10", level=3, tags=["错位相减"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{n}{2^{n}}$。",
         a=r"$2$",
         s=r"由 $\sum nx^{n}=\frac{x}{(1-x)^{2}}$ 取 $x=\frac12$：$\frac{1/2}{(1/2)^{2}}=2$。",
         check=r"eq(Sum(n/2**n, (n, 1, oo)).doit(), 2)"),

    dict(id="S11", level=2, tags=["泰勒级数"], q=r"写出 $e^{x}$ 在 $x=0$ 处的泰勒级数，并说明其四阶导数在 0 处的值。",
         a=r"$e^{x}=\sum_{n=0}^{\infty}\frac{x^{n}}{n!}$，且 $e^{(4)}(0)=1$",
         s=r"各阶导数均为 $e^{x}$，在 $x=0$ 处取值都是 1，故系数为 $\frac{1}{n!}$。",
         check=r"eq(diff(exp(x), x, 4).subs(x, 0), 1)"),

    dict(id="S12", level=2, tags=["几何级数", "幂级数"], q=r"在收敛域内求 $\displaystyle\sum_{n=0}^{\infty}x^{n}$。",
         a=r"$\dfrac{1}{1-x}\quad(|x|<1)$",
         s=r"几何级数求和公式，收敛域为 $|x|<1$。",
         check=r"eq_in(Sum(x**n, (n, 0, oo)), 1/(1-x), Rational(1,3))"),

    dict(id="S13", level=3, tags=["对数级数"], q=r"在收敛域内求 $\displaystyle\sum_{n=1}^{\infty}(-1)^{n+1}\frac{x^{n}}{n}$。",
         a=r"$\ln(1+x)\quad(-1&lt;x\le1)$",
         s=r"把 $\frac{1}{1+t}$ 展开再逐项积分即得。",
         check=r"eq_in(Sum((-1)**(n+1)*x**n/n, (n, 1, oo)), log(1+x), Rational(1,3))"),

    dict(id="S14", level=3, tags=["莱布尼茨级数"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{2n-1}$。",
         a=r"$\dfrac{\pi}{4}$",
         s=r"$\arctan x$ 的展开取 $x=1$（莱布尼茨级数）。",
         check=r"eq(Sum((-1)**(n+1)/(2*n-1), (n, 1, oo)).doit(), pi/4)"),

    dict(id="S15", level=4, tags=["比较判别法"], q=r"判断 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{2}+1}$ 是否收敛，并求其和。",
         a=r"收敛，和为 $\dfrac{\pi\coth\pi-1}{2}$",
         s=r"由 $\frac{1}{n^{2}+1}<\frac{1}{n^{2}}$ 知收敛。用 $\pi\coth(\pi z)$ 的部分分式展开可得闭式。",
         check=r"approx(Sum(1/(n**2+1), (n, 1, oo)).doit(), (pi/tanh(pi)-1)/2, tol=1e-12)"),

    dict(id="S16", level=3, tags=["错位相减"], q=r"在收敛域内求 $\displaystyle\sum_{n=1}^{\infty}nx^{n}$。",
         a=r"$\dfrac{x}{(1-x)^{2}}\quad(|x|<1)$",
         s=r"对 $\sum x^{n}=\frac{1}{1-x}$ 两边求导再乘 $x$。",
         check=r"eq_in(Sum(n*x**n, (n, 1, oo)), x/(1-x)**2, Rational(1,3))"),

    dict(id="S17", level=2, tags=["偶数子列"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{(2n)^{2}}$。",
         a=r"$\dfrac{\pi^{2}}{24}$",
         s=r"$=\frac14\sum\frac{1}{n^{2}}=\frac14\cdot\frac{\pi^{2}}{6}$。",
         check=r"eq(Sum(1/(2*n)**2, (n, 1, oo)).doit(), pi**2/24)"),

    dict(id="S18", level=3, tags=["收敛半径", "阶乘"], q=r"求幂级数 $\displaystyle\sum_{n=0}^{\infty}n!\,x^{n}$ 的收敛半径。",
         a=r"$R=0$",
         s=r"$\lim\frac{(n+1)!}{n!}=\lim(n+1)=+\infty$，故只在 $x=0$ 收敛。",
         check=r"is_oo(limit(factorial(n+1)/factorial(n), n, oo))"),

    dict(id="S19", level=3, tags=["条件收敛"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n}}{n}$。",
         a=r"$-\ln 2$",
         s=r"与 S04 相差一个符号：$\sum\frac{(-1)^{n}}{n}=-\sum\frac{(-1)^{n+1}}{n}=-\ln2$。",
         check=r"eq(Sum((-1)**n/n, (n, 1, oo)).doit(), -log(2))"),

    dict(id="S20", level=3, tags=["比值判别法"], q=r"用比值判别法判断 $\displaystyle\sum_{n=0}^{\infty}\frac{2^{n}}{n!}$ 的敛散性。",
         a=r"收敛（比值极限为 0）",
         s=r"$\frac{a_{n+1}}{a_n}=\frac{2}{n+1}\to0<1$，故收敛。其和为 $e^{2}$。",
         check=r"eq(limit((2**(n+1)/factorial(n+1))/(2**n/factorial(n)), n, oo), 0)"),

    dict(id="S21", level=4, tags=["幂级数求和"], q=r"在收敛域内求 $\displaystyle\sum_{n=0}^{\infty}\frac{x^{n}}{n+1}$。",
         a=r"$-\dfrac{\ln(1-x)}{x}\quad(|x|<1,\ x\neq0)$",
         s=r"记 $S=x\sum\frac{x^{n+1}}{n+1}$，而 $\sum_{n\ge1}\frac{t^{n}}{n}=-\ln(1-t)$，整理即得。",
         check=r"eq_in(Sum(x**n/(n+1), (n, 0, oo)), -log(1-x)/x, Rational(1,3))"),

    dict(id="S22", level=4, tags=["裂项相消"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+1)(n+2)}$。",
         a=r"$\dfrac14$",
         s=r"$\frac{1}{n(n+1)(n+2)}=\frac12\left(\frac{1}{n(n+1)}-\frac{1}{(n+1)(n+2)}\right)$，相加后大部分项抵消。",
         check=r"eq(Sum(1/(n*(n+1)*(n+2)), (n, 1, oo)).doit(), Rational(1,4))"),

    dict(id="S23", level=3, tags=["交错级数"], q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n^{2}}$。",
         a=r"$\dfrac{\pi^{2}}{12}$",
         s=r"$\eta(2)=(1-2^{1-2})\zeta(2)=\frac12\cdot\frac{\pi^{2}}{6}$。",
         check=r"eq(Sum((-1)**(n+1)/n**2, (n, 1, oo)).doit(), pi**2/12)"),

    dict(id="S24", level=4, tags=["收敛半径"], q=r"求幂级数 $\displaystyle\sum_{n=1}^{\infty}\frac{2^{n}x^{n}}{n}$ 的收敛半径。",
         a=r"$R=\dfrac12$",
         s=r"$\lim\left|\frac{a_{n+1}}{a_n}\right|=\lim 2\cdot\frac{n}{n+1}=2$，故 $R=\frac1{2}$。",
         check=r"eq(limit((2**(n+1)/(n+1))/(2**n/n), n, oo), 2)"),

    dict(id="S25", level=4, tags=["双曲函数", "奇阶乘"], q=r"求 $\displaystyle\sum_{n=0}^{\infty}\frac{1}{(2n+1)!}$。",
         a=r"$\sinh 1=\dfrac{e-e^{-1}}{2}$",
         s=r"把 $e$ 与 $e^{-1}$ 的级数相减，偶数项抵消、奇数项加倍。",
         check=r"eq(Sum(1/factorial(2*n+1), (n, 0, oo)).doit(), sinh(1))"),

    dict(id="S26", level=2, tags=["调和级数", "发散"], q=r"判断 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n}$ 的敛散性。",
         a=r"发散",
         s=r"调和级数。可用 $\sum_{n=1}^{2^{k}}\frac1n\ge1+\frac k2$ 说明部分和无界。",
         check=r"diverges(Sum(1/n, (n, 1, oo)))"),
]
