# -*- coding: utf-8 -*-
"""原创题库 · 一元积分学"""
TOPIC = "一元积分学"

PROBLEMS = [
    dict(id="I01", level=3, tags=["分部积分"], q=r"计算 $\displaystyle\int x e^{x}\,dx$。",
         a=r"$(x-1)e^{x}+C$",
         s=r"分部积分：$\int xe^{x}dx=xe^{x}-\int e^{x}dx=(x-1)e^{x}+C$。",
         check=r"zero(diff((x-1)*exp(x), x) - x*exp(x))"),

    dict(id="I02", level=3, tags=["分部积分"], q=r"计算 $\displaystyle\int \ln x\,dx$。",
         a=r"$x\ln x-x+C$",
         s=r"把 $\ln x$ 看作 $\ln x\cdot1$，分部积分得 $x\ln x-\int x\cdot\frac1x dx=x\ln x-x+C$。",
         check=r"zero(diff(x*log(x)-x, x) - log(x))"),

    dict(id="I03", level=1, tags=["基本积分表"], q=r"计算 $\displaystyle\int\frac{dx}{1+x^{2}}$。",
         a=r"$\arctan x+C$",
         s=r"基本积分表：$(\arctan x)'=\frac{1}{1+x^{2}}$。",
         check=r"zero(diff(atan(x), x) - 1/(1+x**2))"),

    dict(id="I04", level=2, tags=["凑微分"], q=r"计算 $\displaystyle\int\frac{x}{1+x^{2}}\,dx$。",
         a=r"$\dfrac12\ln(1+x^{2})+C$",
         s=r"令 $u=1+x^{2}$，$du=2x\,dx$，得 $\frac12\int\frac{du}{u}=\frac12\ln(1+x^{2})+C$。",
         check=r"zero(diff(Rational(1,2)*log(1+x**2), x) - x/(1+x**2))"),

    dict(id="I05", level=3, tags=["降幂公式"], q=r"计算 $\displaystyle\int\sin^{2}x\,dx$。",
         a=r"$\dfrac{x}{2}-\dfrac{\sin 2x}{4}+C$",
         s=r"用 $\sin^{2}x=\frac{1-\cos2x}{2}$ 降幂后逐项积分。",
         check=r"zero(diff(x/2 - sin(2*x)/4, x) - sin(x)**2)"),

    dict(id="I06", level=3, tags=["含参积分", "反三角"], q=r"设 $a>0$，计算 $\displaystyle\int\frac{dx}{x^{2}+a^{2}}$。",
         a=r"$\dfrac1a\arctan\dfrac{x}{a}+C$",
         s=r"提出 $a^{2}$：$\frac{1}{a^{2}}\int\frac{dx}{1+(x/a)^{2}}$，令 $u=x/a$ 即得。",
         check=r"zero(diff(atan(x/a)/a, x) - 1/(x**2+a**2))"),

    dict(id="I07", level=1, tags=["牛顿-莱布尼茨"], q=r"计算 $\displaystyle\int_{0}^{1}x^{2}\,dx$。",
         a=r"$\dfrac13$",
         s=r"$=\left[\frac{x^{3}}{3}\right]_{0}^{1}=\frac13$。",
         check=r"eq(integrate(x**2, (x, 0, 1)), Rational(1,3))"),

    dict(id="I08", level=1, tags=["牛顿-莱布尼茨"], q=r"计算 $\displaystyle\int_{0}^{\pi}\sin x\,dx$。",
         a=r"$2$",
         s=r"$=[-\cos x]_{0}^{\pi}=1-(-1)=2$。",
         check=r"eq(integrate(sin(x), (x, 0, pi)), 2)"),

    dict(id="I09", level=1, tags=["牛顿-莱布尼茨"], q=r"计算 $\displaystyle\int_{0}^{\pi/2}\cos x\,dx$。",
         a=r"$1$",
         s=r"$=[\sin x]_{0}^{\pi/2}=1$。",
         check=r"eq(integrate(cos(x), (x, 0, pi/2)), 1)"),

    dict(id="I10", level=2, tags=["分部积分", "定积分"], q=r"计算 $\displaystyle\int_{1}^{e}\ln x\,dx$。",
         a=r"$1$",
         s=r"原函数为 $x\ln x-x$，代入得 $(e-e)-(0-1)=1$。",
         check=r"eq(integrate(log(x), (x, 1, E)), 1)"),

    dict(id="I11", level=3, tags=["分部积分"], q=r"计算 $\displaystyle\int x\ln x\,dx$。",
         a=r"$\dfrac{x^{2}}{2}\ln x-\dfrac{x^{2}}{4}+C$",
         s=r"分部积分，取 $u=\ln x$、$dv=x\,dx$：$\frac{x^{2}}{2}\ln x-\int\frac{x}{2}dx$。",
         check=r"zero(diff(x**2/2*log(x) - x**2/4, x) - x*log(x))"),

    dict(id="I12", level=3, tags=["分部积分"], q=r"计算 $\displaystyle\int x\sin x\,dx$。",
         a=r"$-x\cos x+\sin x+C$",
         s=r"分部积分两次：$\int x\sin x\,dx=-x\cos x+\int\cos x\,dx$。",
         check=r"zero(diff(-x*cos(x)+sin(x), x) - x*sin(x))"),

    dict(id="I13", level=3, tags=["换元法", "对数"], q=r"计算 $\displaystyle\int\frac{dx}{x\ln x}$（$x>1$）。",
         a=r"$\ln\ln x+C$",
         s=r"令 $u=\ln x$，$du=\frac{dx}{x}$，得 $\int\frac{du}{u}=\ln|u|+C$。",
         check=r"zero(diff(log(log(x)), x) - 1/(x*log(x)))"),

    dict(id="I14", level=3, tags=["反常积分"], q=r"判断 $\displaystyle\int_{1}^{+\infty}\frac{dx}{x^{2}}$ 是否收敛，收敛时求值。",
         a=r"收敛，值为 $1$",
         s=r"$\left[-\frac1x\right]_{1}^{+\infty}=0-(-1)=1$。",
         check=r"eq(integrate(1/x**2, (x, 1, oo)), 1)"),

    dict(id="I15", level=2, tags=["反常积分"], q=r"计算 $\displaystyle\int_{0}^{+\infty}e^{-x}\,dx$。",
         a=r"$1$",
         s=r"$=[-e^{-x}]_{0}^{+\infty}=0-(-1)=1$。",
         check=r"eq(integrate(exp(-x), (x, 0, oo)), 1)"),

    dict(id="I16", level=2, tags=["定积分", "反三角"], q=r"计算 $\displaystyle\int_{0}^{1}\frac{dx}{1+x^{2}}$。",
         a=r"$\dfrac{\pi}{4}$",
         s=r"$=[\arctan x]_{0}^{1}=\frac\pi4-0$。",
         check=r"eq(integrate(1/(1+x**2), (x, 0, 1)), pi/4)"),

    dict(id="I17", level=4, tags=["有理函数", "部分分式"], q=r"计算 $\displaystyle\int\frac{dx}{x^{2}-1}$。",
         a=r"$\dfrac12\ln\left|\dfrac{x-1}{x+1}\right|+C$",
         s=r"部分分式 $\frac{1}{x^{2}-1}=\frac12\left(\frac{1}{x-1}-\frac{1}{x+1}\right)$，积分后合并对数。",
         check=r"zero(diff(Rational(1,2)*log((x-1)/(x+1)), x) - 1/(x**2-1))"),

    dict(id="I18", level=2, tags=["对称性", "奇函数"], q=r"计算 $\displaystyle\int_{-1}^{1}x^{3}\,dx$。",
         a=r"$0$",
         s=r"被积函数是奇函数、区间关于原点对称，故积分为 0。也可直接算出 $\left[\frac{x^4}{4}\right]_{-1}^{1}=0$。",
         check=r"eq(integrate(x**3, (x, -1, 1)), 0)"),

    dict(id="I19", level=3, tags=["面积", "定积分应用"], q=r"求曲线 $y=x$ 与 $y=x^{2}$ 围成的图形面积。",
         a=r"$\dfrac16$",
         s=r"交点 $x=0,1$。面积 $=\int_{0}^{1}(x-x^{2})dx=\frac12-\frac13=\frac16$。",
         check=r"eq(integrate(x - x**2, (x, 0, 1)), Rational(1,6))"),

    dict(id="I20", level=3, tags=["旋转体体积"], q=r"求 $y=\sqrt x$（$0\le x\le1$）绕 $x$ 轴旋转所得旋转体的体积。",
         a=r"$\dfrac{\pi}{2}$",
         s=r"$V=\pi\int_{0}^{1}(\sqrt x)^{2}dx=\pi\int_{0}^{1}x\,dx=\frac\pi2$。",
         check=r"eq(pi*integrate(x, (x, 0, 1)), pi/2)"),

    dict(id="I21", level=4, tags=["弧长"], q=r"求曲线 $y=\dfrac23x^{3/2}$ 在 $0\le x\le1$ 上的弧长。",
         a=r"$\dfrac23\left(2\sqrt2-1\right)$",
         s=r"$y'=\sqrt x$，弧长 $=\int_{0}^{1}\sqrt{1+y'^{2}}\,dx=\int_{0}^{1}\sqrt{1+x}\,dx=\frac23\left[(1+x)^{3/2}\right]_{0}^{1}$。",
         check=r"eq(integrate(sqrt(1+x), (x, 0, 1)), Rational(2,3)*(2*sqrt(2)-1))"),

    dict(id="I22", level=2, tags=["基本积分表"], q=r"计算 $\displaystyle\int\tan x\,dx$。",
         a=r"$-\ln|\cos x|+C$",
         s=r"$\int\frac{\sin x}{\cos x}dx$，令 $u=\cos x$ 得 $-\ln|\cos x|+C$。",
         check=r"zero(diff(-log(cos(x)), x) - tan(x))"),

    dict(id="I23", level=4, tags=["配方", "反三角"], q=r"计算 $\displaystyle\int\frac{dx}{x^{2}+2x+5}$。",
         a=r"$\dfrac12\arctan\dfrac{x+1}{2}+C$",
         s=r"配方 $x^{2}+2x+5=(x+1)^{2}+4$，再用 $\int\frac{du}{u^{2}+a^{2}}=\frac1a\arctan\frac ua$。",
         check=r"zero(diff(atan((x+1)/2)/2, x) - 1/(x**2+2*x+5))"),

    dict(id="I24", level=4, tags=["分部积分", "反三角"], q=r"计算 $\displaystyle\int\arctan x\,dx$。",
         a=r"$x\arctan x-\dfrac12\ln(1+x^{2})+C$",
         s=r"分部积分：$x\arctan x-\int\frac{x}{1+x^{2}}dx$，后一项即 I04。",
         check=r"zero(diff(x*atan(x) - Rational(1,2)*log(1+x**2), x) - atan(x))"),

    dict(id="I25", level=3, tags=["反常积分", "瑕积分"], q=r"计算 $\displaystyle\int_{0}^{1}\frac{dx}{\sqrt x}$。",
         a=r"$2$",
         s=r"$x=0$ 处被积函数无界。$=\left[2\sqrt x\right]_{0}^{1}=2$。",
         check=r"eq(integrate(1/sqrt(x), (x, 0, 1)), 2)"),

    dict(id="I26", level=4, tags=["换元法", "定积分"], q=r"计算 $\displaystyle\int_{0}^{\ln 2}\frac{e^{x}}{1+e^{2x}}\,dx$。",
         a=r"$\arctan 2-\dfrac{\pi}{4}$",
         s=r"令 $u=e^{x}$，$du=e^{x}dx$，积分化为 $\int_{1}^{2}\frac{du}{1+u^{2}}=[\arctan u]_{1}^{2}$。",
         check=r"eq(integrate(exp(x)/(1+exp(2*x)), (x, 0, log(2))), atan(2)-pi/4)"),
]
