# -*- coding: utf-8 -*-
"""原创题库 · 极限与连续（每题附 sympy 验证断言）"""

PROBLEMS = [
    dict(id="L01", level=2, tags=["等价无穷小", "洛必达"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^{2}}$。",
         a=r"$\dfrac{1}{2}$",
         s=r"$1-\cos x=2\sin^{2}\frac{x}{2}\sim 2\cdot\left(\frac{x}{2}\right)^{2}=\frac{x^{2}}{2}$，故极限为 $\frac12$。",
         check=r"eq(limit((1-cos(x))/x**2, x, 0), Rational(1,2))"),

    dict(id="L02", level=3, tags=["等价无穷小", "通分"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\tan x-\sin x}{x^{3}}$。",
         a=r"$\dfrac{1}{2}$",
         s=r"$\tan x-\sin x=\sin x\left(\frac{1}{\cos x}-1\right)=\sin x\cdot\frac{1-\cos x}{\cos x}$，"
           r"于是原式 $=\frac{\sin x}{x}\cdot\frac{1-\cos x}{x^{2}}\cdot\frac{1}{\cos x}\to 1\cdot\frac12\cdot 1=\frac12$。",
         check=r"eq(limit((tan(x)-sin(x))/x**3, x, 0), Rational(1,2))"),

    dict(id="L03", level=2, tags=["重要极限"], q=r"计算 $\displaystyle\lim_{x\to\infty}\left(1+\frac{3}{x}\right)^{x}$。",
         a=r"$e^{3}$",
         s=r"$\left(1+\frac3x\right)^{x}=\left[\left(1+\frac3x\right)^{x/3}\right]^{3}\to e^{3}$。",
         check=r"eq(limit((1+3/x)**x, x, oo), exp(3))"),

    dict(id="L04", level=2, tags=["泰勒展开"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{e^{x}-1-x}{x^{2}}$。",
         a=r"$\dfrac{1}{2}$",
         s=r"$e^{x}=1+x+\frac{x^{2}}{2}+o(x^{2})$，代入得 $\frac{x^{2}/2+o(x^{2})}{x^{2}}\to\frac12$。",
         check=r"eq(limit((exp(x)-1-x)/x**2, x, 0), Rational(1,2))"),

    dict(id="L05", level=3, tags=["泰勒展开"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\ln(1+x)-x}{x^{2}}$。",
         a=r"$-\dfrac{1}{2}$",
         s=r"$\ln(1+x)=x-\frac{x^{2}}{2}+o(x^{2})$，故极限为 $-\frac12$。",
         check=r"eq(limit((log(1+x)-x)/x**2, x, 0), Rational(-1,2))"),

    dict(id="L06", level=3, tags=["重要极限", "含参"], q=r"设 $a>0$，计算 $\displaystyle\lim_{x\to 0}\frac{a^{x}-1}{x}$。",
         a=r"$\ln a$",
         s=r"$a^{x}=e^{x\ln a}$，原式 $=\frac{e^{x\ln a}-1}{x\ln a}\cdot\ln a\to\ln a$。",
         check=r"eq(limit((a**x-1)/x, x, 0), log(a))"),

    dict(id="L07", level=2, tags=["因式分解"], q=r"设 $n$ 为正整数，计算 $\displaystyle\lim_{x\to 1}\frac{x^{n}-1}{x-1}$。",
         a=r"$n$",
         s=r"$x^{n}-1=(x-1)(x^{n-1}+x^{n-2}+\cdots+1)$，约去 $x-1$ 后令 $x\to1$ 得 $n$。",
         check=r"eq(limit((x**n-1)/(x-1), x, 1), n)"),

    dict(id="L08", level=3, tags=["有理化"], q=r"计算 $\displaystyle\lim_{n\to\infty}n\left(\sqrt{n^{2}+1}-n\right)$。",
         a=r"$\dfrac{1}{2}$",
         s=r"有理化：$n\cdot\frac{1}{\sqrt{n^{2}+1}+n}=\frac{1}{\sqrt{1+1/n^{2}}+1}\to\frac12$。",
         check=r"eq(limit(n*(sqrt(n**2+1)-n), n, oo), Rational(1,2))"),

    dict(id="L09", level=3, tags=["重要极限"], q=r"计算 $\displaystyle\lim_{x\to 0}(1+2x)^{3/x}$。",
         a=r"$e^{6}$",
         s=r"$(1+2x)^{3/x}=\left[(1+2x)^{1/(2x)}\right]^{6}\to e^{6}$。",
         check=r"eq(limit((1+2*x)**(3/x), x, 0), exp(6))"),

    dict(id="L10", level=3, tags=["三角恒等变形"], q=r"计算 $\displaystyle\lim_{x\to \pi/2}\left(\sec x-\tan x\right)$。",
         a=r"$0$",
         s=r"$\sec x-\tan x=\frac{1-\sin x}{\cos x}=\frac{\cos x}{1+\sin x}\to\frac{0}{2}=0$。",
         check=r"eq(limit(sec(x)-tan(x), x, pi/2), 0)"),

    dict(id="L11", level=2, tags=["等价无穷小"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\sin 3x}{\tan 5x}$。",
         a=r"$\dfrac{3}{5}$",
         s=r"$\sin 3x\sim 3x$，$\tan 5x\sim 5x$，比值为 $\frac35$。",
         check=r"eq(limit(sin(3*x)/tan(5*x), x, 0), Rational(3,5))"),

    dict(id="L12", level=3, tags=["有理化"], q=r"计算 $\displaystyle\lim_{x\to\infty}\left(\sqrt{x^{2}+3x}-x\right)$。",
         a=r"$\dfrac{3}{2}$",
         s=r"有理化得 $\frac{3x}{\sqrt{x^{2}+3x}+x}\to\frac{3}{2}$。",
         check=r"eq(limit(sqrt(x**2+3*x)-x, x, oo), Rational(3,2))"),

    dict(id="L13", level=2, tags=["连续", "待定常数"], q=r"设 $f(x)=\dfrac{e^{2x}-1}{x}\ (x\neq0)$，$f(0)=k$。求 $k$ 使 $f$ 在 $x=0$ 处连续。",
         a=r"$k=2$",
         s=r"连续要求 $k=\lim_{x\to0}\frac{e^{2x}-1}{x}=2$。",
         check=r"eq(limit((exp(2*x)-1)/x, x, 0), 2)"),

    dict(id="L14", level=4, tags=["幂指函数", "洛必达"], q=r"计算 $\displaystyle\lim_{x\to 0}(\cos x)^{1/x^{2}}$。",
         a=r"$e^{-1/2}$",
         s=r"取对数：$\frac{\ln\cos x}{x^{2}}\to-\frac12$（$\ln\cos x=\ln(1-\frac{x^2}{2}+o(x^2))\sim-\frac{x^2}{2}$），故原式为 $e^{-1/2}$。",
         check=r"eq(limit(cos(x)**(1/x**2), x, 0), exp(Rational(-1,2)))"),

    dict(id="L15", level=3, tags=["泰勒展开"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\ln\cos x}{x^{2}}$。",
         a=r"$-\dfrac{1}{2}$",
         s=r"$\ln\cos x=\ln\left(1-\frac{x^{2}}{2}+o(x^{2})\right)=-\frac{x^{2}}{2}+o(x^{2})$，故为 $-\frac12$。",
         check=r"eq(limit(log(cos(x))/x**2, x, 0), Rational(-1,2))"),

    dict(id="L16", level=4, tags=["无穷小阶"], q=r"当 $x\to0$ 时，$\tan x-\sin x$ 是 $x$ 的几阶无穷小？并写出等价无穷小。",
         a=r"$3$ 阶，且 $\tan x-\sin x\sim\dfrac{x^{3}}{2}$",
         s=r"由 L02 知 $\frac{\tan x-\sin x}{x^{3}}\to\frac12\neq0$，故为 3 阶无穷小，等价于 $\frac{x^{3}}{2}$。",
         check=r"eq(limit((tan(x)-sin(x))/x**3, x, 0), Rational(1,2))"),

    dict(id="L17", level=3, tags=["对数", "单侧极限"], q=r"计算 $\displaystyle\lim_{x\to 0^{+}}x\ln x$。",
         a=r"$0$",
         s=r"令 $t=1/x\to+\infty$，则 $x\ln x=-\frac{\ln t}{t}\to0$。",
         check=r"eq(limit(x*log(x), x, 0, '+'), 0)"),

    dict(id="L18", level=4, tags=["通分", "泰勒展开"], q=r"计算 $\displaystyle\lim_{x\to 0}\left(\frac{1}{x}-\frac{1}{e^{x}-1}\right)$。",
         a=r"$\dfrac{1}{2}$",
         s=r"通分：$\frac{e^{x}-1-x}{x(e^{x}-1)}$。分子 $\sim\frac{x^{2}}{2}$，分母 $\sim x^{2}$，故为 $\frac12$。",
         check=r"eq(limit(1/x - 1/(exp(x)-1), x, 0), Rational(1,2))"),

    dict(id="L19", level=3, tags=["等价无穷小"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\tan x^{2}}{1-\cos x}$。",
         a=r"$2$",
         s=r"$\tan x^{2}\sim x^{2}$，$1-\cos x\sim\frac{x^{2}}{2}$，比值为 2。",
         check=r"eq(limit(tan(x**2)/(1-cos(x)), x, 0), 2)"),

    dict(id="L20", level=3, tags=["幂指函数"], q=r"计算 $\displaystyle\lim_{x\to\infty}x^{1/x}$。",
         a=r"$1$",
         s=r"$x^{1/x}=e^{\ln x/x}$，而 $\frac{\ln x}{x}\to0$，故为 $e^{0}=1$。",
         check=r"eq(limit(x**(1/x), x, oo), 1)"),

    dict(id="L21", level=3, tags=["夹逼定理", "有界乘无穷小"], q=r"计算 $\displaystyle\lim_{x\to 0}x^{2}\sin\frac{1}{x}$。",
         a=r"$0$",
         s=r"$\left|x^{2}\sin\frac1x\right|\le x^{2}\to0$，由夹逼定理极限为 0。",
         check=r"eq(limit(x**2*sin(1/x), x, 0), 0)"),

    dict(id="L22", level=4, tags=["通分", "泰勒展开"], q=r"计算 $\displaystyle\lim_{x\to 1}\left(\frac{1}{\ln x}-\frac{1}{x-1}\right)$。",
         a=r"$\dfrac{1}{2}$",
         s=r"通分得 $\frac{x-1-\ln x}{(x-1)\ln x}$。由 $\ln x=\ln(1+(x-1))$ 展开：分子 $\sim\frac{(x-1)^{2}}{2}$，分母 $\sim(x-1)^{2}$，故为 $\frac12$。",
         check=r"eq(limit(1/log(x) - 1/(x-1), x, 1), Rational(1,2))"),

    dict(id="L23", level=2, tags=["等价无穷小"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x\sin x}$。",
         a=r"$\dfrac{1}{2}$",
         s=r"$1-\cos x\sim\frac{x^{2}}{2}$，$x\sin x\sim x^{2}$，比值为 $\frac12$。",
         check=r"eq(limit((1-cos(x))/(x*sin(x)), x, 0), Rational(1,2))"),

    dict(id="L24", level=2, tags=["反三角", "等价无穷小"], q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\arcsin x}{x}$。",
         a=r"$1$",
         s=r"令 $t=\arcsin x$，则 $x=\sin t$，$t\to0$ 时 $\frac{t}{\sin t}\to1$。",
         check=r"eq(limit(asin(x)/x, x, 0), 1)"),

    dict(id="L25", level=3, tags=["间断点"], q=r"判断 $x=1$ 是 $f(x)=\dfrac{\sin(x-1)}{x-1}$ 的哪一类间断点（可去／跳跃／无穷）。",
         a=r"可去间断点",
         s=r"$\lim_{x\to1}\frac{\sin(x-1)}{x-1}=1$ 存在，但 $f$ 在 $x=1$ 无定义，故为可去间断点。",
         check=r"eq(limit(sin(x-1)/(x-1), x, 1), 1)"),

    dict(id="L26", level=4, tags=["夹逼定理", "取整函数"], q=r"计算 $\displaystyle\lim_{x\to\infty}\frac{\lfloor x\rfloor}{x}$。",
         a=r"$1$",
         s=r"$x-1<\lfloor x\rfloor\le x$，两边除以 $x$ 后夹逼，极限为 1。",
         check=r"eq(limit(floor(x)/x, x, oo), 1)"),
]
