# -*- coding: utf-8 -*-
"""原创题库 · 一元微分学"""
TOPIC = "一元微分学"

PROBLEMS = [
    dict(id="D01", level=3, tags=["对数求导法", "幂指函数"], q=r"求 $y=x^{x}\ (x>0)$ 的导数。",
         a=r"$y'=x^{x}(\ln x+1)$",
         s=r"两边取对数 $\ln y=x\ln x$，求导得 $\frac{y'}{y}=\ln x+1$，故 $y'=x^{x}(\ln x+1)$。",
         check=r"eq(diff(x**x, x), x**x*(log(x)+1))"),

    dict(id="D02", level=2, tags=["复合函数"], q=r"求 $y=\ln\sin x$ 的导数。",
         a=r"$y'=\cot x$",
         s=r"链式法则：$y'=\frac{1}{\sin x}\cdot\cos x=\cot x$。",
         check=r"eq(diff(log(sin(x)), x), cot(x))"),

    dict(id="D03", level=3, tags=["隐函数"], q=r"设 $x^{2}+y^{2}=1$，求 $\dfrac{dy}{dx}$。",
         a=r"$\dfrac{dy}{dx}=-\dfrac{x}{y}$",
         s=r"两边对 $x$ 求导：$2x+2yy'=0$，得 $y'=-\frac{x}{y}$。",
         check=r"zero(2*x + 2*y*(-x/y))"),

    dict(id="D04", level=3, tags=["参数方程"], q=r"设 $x=t-\sin t,\ y=1-\cos t$，求 $\dfrac{dy}{dx}$。",
         a=r"$\dfrac{dy}{dx}=\dfrac{\sin t}{1-\cos t}=\cot\dfrac{t}{2}$",
         s=r"$\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{\sin t}{1-\cos t}$，用半角公式化为 $\cot\frac t2$。",
         check=r"eq(diff(1-cos(t), t)/diff(t-sin(t), t), cot(t/2))"),

    dict(id="D05", level=2, tags=["反三角"], q=r"求 $y=\arctan x$ 的导数。",
         a=r"$y'=\dfrac{1}{1+x^{2}}$",
         s=r"由 $\tan y=x$ 求隐函数导数：$\sec^{2}y\cdot y'=1$，而 $\sec^{2}y=1+\tan^{2}y=1+x^{2}$。",
         check=r"eq(diff(atan(x), x), 1/(1+x**2))"),

    dict(id="D06", level=3, tags=["高阶导数"], q=r"求 $y=xe^{x}$ 的二阶导数。",
         a=r"$y''=(x+2)e^{x}$",
         s=r"$y'=e^{x}+xe^{x}=(x+1)e^{x}$，$y''=e^{x}+(x+1)e^{x}=(x+2)e^{x}$。",
         check=r"eq(diff(x*exp(x), x, 2), (x+2)*exp(x))"),

    dict(id="D07", level=3, tags=["罗尔定理"], q=r"验证 $f(x)=x^{3}-x$ 在 $[-1,1]$ 上满足罗尔定理，并求出 $\xi$。",
         a=r"$\xi=\pm\dfrac{1}{\sqrt3}$",
         s=r"$f(-1)=f(1)=0$，$f$ 在 $[-1,1]$ 可导。$f'(x)=3x^{2}-1=0$ 得 $x=\pm\frac{1}{\sqrt3}$，两者都在 $(-1,1)$ 内。",
         check=r"zero(diff(x**3-x, x).subs(x, 1/sqrt(3))) and zero(diff(x**3-x, x).subs(x, -1/sqrt(3)))"),

    dict(id="D08", level=4, tags=["洛必达", "泰勒展开"], q=r"计算 $\displaystyle\lim_{x\to0}\frac{e^{x}-e^{-x}-2x}{x-\sin x}$。",
         a=r"$2$",
         s=r"分子 $=\left(2x+\frac{x^{3}}{3}+\cdots\right)-2x=\frac{x^{3}}{3}+\cdots$；分母 $=x-\left(x-\frac{x^{3}}{6}\right)=\frac{x^{3}}{6}$。比值趋于 2。",
         check=r"eq(limit((exp(x)-exp(-x)-2*x)/(x-sin(x)), x, 0), 2)"),

    dict(id="D09", level=3, tags=["极值"], q=r"求 $f(x)=x^{3}-3x^{2}+2$ 的极值点与极值。",
         a=r"$x=0$ 极大值 $f(0)=2$；$x=2$ 极小值 $f(2)=-2$",
         s=r"$f'(x)=3x(x-2)$，得驻点 $0,2$。$f''(x)=6x-6$，$f''(0)=-6<0$ 故极大，$f''(2)=6>0$ 故极小。",
         check=r"eq(diff(x**3-3*x**2+2, x, 2).subs(x, 0), -6) and eq(diff(x**3-3*x**2+2, x, 2).subs(x, 2), 6)"),

    dict(id="D10", level=2, tags=["凹凸性", "拐点"], q=r"求 $y=x^{3}$ 的凹凸区间与拐点。",
         a=r"拐点 $(0,0)$；$x<0$ 凸，$x>0$ 凹",
         s=r"$y''=6x$，在 $x=0$ 两侧变号，故 $(0,0)$ 为拐点。",
         check=r"eq(diff(x**3, x, 2), 6*x) and eq(diff(x**3, x, 2).subs(x, 0), 0)"),

    dict(id="D11", level=4, tags=["曲率"], q=r"求曲线 $y=x^{2}$ 在 $x=1$ 处的曲率。",
         a=r"$K=\dfrac{2\sqrt5}{25}=\dfrac{2}{5\sqrt5}$",
         s=r"$K=\frac{|y''|}{(1+y'^{2})^{3/2}}$，$y'=2x$、$y''=2$，在 $x=1$ 处 $K=\frac{2}{(1+4)^{3/2}}=\frac{2}{5\sqrt5}$。",
         check=r"approx(Rational(2)/(1+4)**Rational(3,2), 2/(5*sqrt(5)))"),

    dict(id="D12", level=3, tags=["微分近似"], q=r"用微分近似计算 $\sqrt{1.02}$（保留到 $10^{-4}$）。",
         a=r"$\approx 1.01$",
         s=r"取 $f(x)=\sqrt x$，$x_{0}=1$、$\Delta x=0.02$。$f'(1)=\frac12$，故 $\sqrt{1.02}\approx1+\frac12(0.02)=1.01$。",
         check=r"approx(1 + Rational(1,2)*Rational(2,100), sqrt(Rational(102,100)), tol=1e-4)"),

    dict(id="D13", level=3, tags=["极值"], q=r"求 $y=xe^{-x}$ 的最大值。",
         a=r"最大值 $y(1)=e^{-1}=\dfrac1e$",
         s=r"$y'=e^{-x}(1-x)=0$ 得 $x=1$；$y''=e^{-x}(x-2)$，$y''(1)=-e^{-1}<0$ 故为极大也即最大。",
         check=r"eq(diff(x*exp(-x), x), exp(-x)*(1-x)) and eq((x*exp(-x)).subs(x, 1), exp(-1))"),

    dict(id="D14", level=4, tags=["罗尔定理"], q=r"对 $f(x)=x(x-1)(x-2)$ 在 $[0,2]$ 上求罗尔定理中的 $\xi$。",
         a=r"$\xi=1\pm\dfrac{1}{\sqrt3}$",
         s=r"$f(0)=f(2)=0$。$f'(x)=3x^{2}-6x+2=0$ 得 $x=1\pm\frac{1}{\sqrt3}$，均在 $(0,2)$ 内。",
         check=r"zero(diff(x*(x-1)*(x-2), x).subs(x, 1 - 1/sqrt(3))) and zero(diff(x*(x-1)*(x-2), x).subs(x, 1 + 1/sqrt(3)))"),

    dict(id="D15", level=2, tags=["拉格朗日中值定理"], q=r"对 $f(x)=x^{2}$ 在 $[0,2]$ 上求拉格朗日中值定理中的 $\xi$。",
         a=r"$\xi=1$",
         s=r"$\frac{f(2)-f(0)}{2-0}=2$，令 $f'(\xi)=2\xi=2$ 得 $\xi=1\in(0,2)$。",
         check=r"zero(diff(x**2, x).subs(x, 1) - Rational(4-0, 2-0))"),

    dict(id="D16", level=2, tags=["切线"], q=r"求曲线 $y=\ln x$ 在 $x=1$ 处的切线方程。",
         a=r"$y=x-1$",
         s=r"切点 $(1,0)$，斜率 $y'(1)=1$，故切线为 $y-0=1\cdot(x-1)$。",
         check=r"eq(diff(log(x), x).subs(x, 1), 1) and eq(log(1), 0)"),

    dict(id="D17", level=3, tags=["高阶导数", "三角函数"], q=r"求 $y=\sin x$ 的二阶与四阶导数。",
         a=r"$y''=-\sin x,\quad y^{(4)}=\sin x$",
         s=r"每求一次导相位前移 $\pi/2$，四次一循环。",
         check=r"eq(diff(sin(x), x, 2), -sin(x)) and eq(diff(sin(x), x, 4), sin(x))"),

    dict(id="D18", level=4, tags=["分段函数", "导数定义"], q=r"设 $f(x)=x^{2}\sin\frac1x\ (x\neq0)$，$f(0)=0$。求 $f'(0)$。",
         a=r"$f'(0)=0$",
         s=r"按定义 $f'(0)=\lim_{h\to0}\frac{h^{2}\sin(1/h)-0}{h}=\lim_{h\to0}h\sin\frac1h=0$（有界量乘无穷小）。",
         check=r"eq(limit((x**2*sin(1/x))/x, x, 0), 0)"),

    dict(id="D19", level=4, tags=["参数方程", "二阶导数"], q=r"设 $x=t^{2},\ y=t^{3}$，求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^{2}y}{dx^{2}}$。",
         a=r"$\dfrac{dy}{dx}=\dfrac{3t}{2}$，$\dfrac{d^{2}y}{dx^{2}}=\dfrac{3}{4t}$",
         s=r"$\frac{dy}{dx}=\frac{3t^{2}}{2t}=\frac{3t}{2}$；再对 $x$ 求导需除以 $\frac{dx}{dt}=2t$：$\frac{d}{dt}\left(\frac{3t}{2}\right)\Big/2t=\frac{3}{4t}$。",
         check=r"eq(diff(t**3, t)/diff(t**2, t), 3*t/2) and eq(diff(3*t/2, t)/diff(t**2, t), 3/(4*t))"),

    dict(id="D20", level=3, tags=["乘积求导"], q=r"求 $y=(1+x^{2})\arctan x$ 的导数。",
         a=r"$y'=2x\arctan x+1$",
         s=r"$y'=2x\arctan x+(1+x^{2})\cdot\frac{1}{1+x^{2}}=2x\arctan x+1$。",
         check=r"eq(diff((1+x**2)*atan(x), x), 2*x*atan(x)+1)"),

    dict(id="D21", level=3, tags=["最值", "对勾函数"], q=r"求 $f(x)=x+\dfrac1x\ (x>0)$ 的最小值。",
         a=r"最小值 $f(1)=2$",
         s=r"$f'(x)=1-\frac{1}{x^{2}}=0$ 得 $x=1$；$x\to0^{+}$ 与 $x\to+\infty$ 时 $f\to+\infty$，故为全局最小。",
         check=r"eq(diff(x+1/x, x), 1-1/x**2) and eq((x+1/x).subs(x, 1), 2)"),

    dict(id="D22", level=3, tags=["相关变化率"], q=r"圆面积 $A=\pi r^{2}$，半径以 $2$ 单位/秒增长。求 $r=3$ 时面积的变化率。",
         a=r"$12\pi$ 单位²/秒",
         s=r"$\frac{dA}{dt}=2\pi r\frac{dr}{dt}=2\pi\cdot3\cdot2=12\pi$。",
         check=r"eq(diff(pi*x**2, x).subs(x, 3)*2, 12*pi)"),

    dict(id="D23", level=3, tags=["乘积求导", "指数三角"], q=r"求 $y=e^{2x}\cos 3x$ 的导数。",
         a=r"$y'=e^{2x}(2\cos 3x-3\sin 3x)$",
         s=r"乘积法则：$y'=2e^{2x}\cos3x-3e^{2x}\sin3x$。",
         check=r"eq(diff(exp(2*x)*cos(3*x), x), exp(2*x)*(2*cos(3*x)-3*sin(3*x)))"),

    dict(id="D24", level=4, tags=["对数求导法"], q=r"求 $y=x^{\sin x}\ (x>0)$ 的导数。",
         a=r"$y'=x^{\sin x}\left(\cos x\ln x+\dfrac{\sin x}{x}\right)$",
         s=r"$\ln y=\sin x\ln x$，求导得 $\frac{y'}{y}=\cos x\ln x+\frac{\sin x}{x}$。",
         check=r"eq(diff(x**sin(x), x), x**sin(x)*(cos(x)*log(x)+sin(x)/x))"),

    dict(id="D25", level=4, tags=["隐函数", "数值代入"], q=r"设 $x^{3}+y^{3}-3xy=0$，求 $\dfrac{dy}{dx}$，并求点 $\left(\frac32,\frac32\right)$ 处的值。",
         a=r"$\dfrac{dy}{dx}=\dfrac{y-x^{2}}{y^{2}-x}$；在 $\left(\frac32,\frac32\right)$ 处为 $-1$",
         s=r"对 $x$ 求导：$3x^{2}+3y^{2}y'-3y-3xy'=0$，解出 $y'$，再代入点坐标得 $-1$。",
         check=r"eq(((y-x**2)/(y**2-x)).subs({x: Rational(3,2), y: Rational(3,2)}), -1)"),

    dict(id="D26", level=3, tags=["导数定义", "可导性"], q=r"讨论 $f(x)=|x|$ 在 $x=0$ 处是否可导，并指出左右导数。",
         a=r"不可导；左导数 $-1$，右导数 $+1$",
         s=r"$f'_{-}(0)=\lim_{h\to0^{-}}\frac{|h|}{h}=-1$，$f'_{+}(0)=1$，两者不等故不可导。",
         check=r"eq(limit((-x-0)/x, x, 0, '-'), -1) and eq(limit((x-0)/x, x, 0, '+'), 1)"),
]
