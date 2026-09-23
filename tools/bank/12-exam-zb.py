# -*- coding: utf-8 -*-
"""
原创题库 · 专升本（高等数学）
============================
说明：按各省普通高校专升本高等数学考试的范围与难度编写的**风格模拟题**，不是历年真题。
特点是覆盖面广、计算为主、证明较少，难度大致相当于理工科高数期末的偏易档到中档。
"""
TOPIC = "专升本高等数学"
SECTION = "exam"
TARGET = "专升本"

PROBLEMS = [
    dict(id="Z01", level=1, target=TARGET, tags=["极限"],
         q=r"计算 $\displaystyle\lim_{x\to 1}\frac{x^{2}-1}{x-1}$。",
         a=r"$2$",
         s=r"约去公因式：$\frac{(x-1)(x+1)}{x-1}=x+1\to2$。",
         q_en=r"Evaluate $\lim_{x\to 1}\frac{x^{2}-1}{x-1}$.",
         a_en=r"$2$",
         s_en=r"Cancel the common factor: $\frac{(x-1)(x+1)}{x-1}=x+1\to2$.",
         check=r"eq(limit((x**2-1)/(x-1), x, 1), 2)"),

    dict(id="Z02", level=2, target=TARGET, tags=["极限", "重要极限"],
         q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\sin 5x}{2x}$。",
         a=r"$\dfrac{5}{2}$",
         s=r"$\frac{\sin5x}{5x}\to1$，故原式 $=\frac52$。",
         q_en=r"Evaluate $\lim_{x\to 0}\frac{\sin 5x}{2x}$.",
         a_en=r"$\dfrac{5}{2}$",
         s_en=r"Since $\frac{\sin 5x}{5x}\to1$, the limit is $5/2$.",
         check=r"eq(limit(sin(5*x)/(2*x), x, 0), Rational(5,2))"),

    dict(id="Z03", level=2, target=TARGET, tags=["导数"],
         q=r"求 $y=x^{3}-3x^{2}+5$ 的导数与 $x=2$ 处的导数值。",
         a=r"$y'=3x^{2}-6x$，$y'(2)=0$",
         s=r"逐项求导得 $y'=3x^{2}-6x$，代入 $x=2$ 得 $12-12=0$。",
         q_en=r"Differentiate $y=x^{3}-3x^{2}+5$ and evaluate $y'$ at $x=2$.",
         a_en=r"$y'=3x^{2}-6x$; $y'(2)=0$",
         s_en=r"Term-by-term differentiation gives $y'=3x^{2}-6x$; at $x=2$ this is $12-12=0$.",
         check=r"eq(diff(x**3-3*x**2+5, x), 3*x**2-6*x) "
               r"and eq(diff(x**3-3*x**2+5, x).subs(x, 2), 0)"),

    dict(id="Z04", level=2, target=TARGET, tags=["导数", "切线"],
         q=r"求曲线 $y=x^{3}$ 在点 $(1,1)$ 处的切线方程。",
         a=r"$y=3x-2$",
         s=r"$y'=3x^{2}$，$y'(1)=3$，故切线为 $y-1=3(x-1)$。",
         q_en=r"Find the tangent to $y=x^{3}$ at $(1,1)$.",
         a_en=r"$y=3x-2$",
         s_en=r"$y'=3x^{2}$ so the slope at $x=1$ is $3$, giving $y-1=3(x-1)$.",
         check=r"eq(diff(x**3, x).subs(x, 1), 3) and eq((3*1-2), 1)"),

    dict(id="Z05", level=2, target=TARGET, tags=["不定积分"],
         q=r"计算 $\displaystyle\int\left(3x^{2}-2x+1\right)dx$。",
         a=r"$x^{3}-x^{2}+x+C$",
         s=r"逐项积分：$\frac{3x^{3}}{3}-\frac{2x^{2}}{2}+x+C$。",
         q_en=r"Evaluate $\int(3x^{2}-2x+1)\,dx$.",
         a_en=r"$x^{3}-x^{2}+x+C$",
         s_en=r"Integrating term by term gives $x^{3}-x^{2}+x+C$.",
         check=r"zero(diff(x**3-x**2+x, x) - (3*x**2-2*x+1))"),

    dict(id="Z06", level=3, target=TARGET, tags=["定积分", "分部"],
         q=r"计算 $\displaystyle\int_{0}^{1}xe^{x}\,dx$。",
         a=r"$1$",
         s=r"分部积分：$\int xe^{x}dx=(x-1)e^{x}$，代入得 $0-(-1)=1$。",
         q_en=r"Evaluate $\int_{0}^{1}xe^{x}\,dx$.",
         a_en=r"$1$",
         s_en=r"Integrating by parts, $\int xe^{x}dx=(x-1)e^{x}$; substituting gives $0+1=1$.",
         check=r"eq(integrate(x*exp(x), (x, 0, 1)), 1)"),

    dict(id="Z07", level=3, target=TARGET, tags=["定积分", "面积"],
         q=r"求曲线 $y=x^{2}$ 与直线 $y=2x$ 围成的图形面积。",
         a=r"$\dfrac{4}{3}$",
         s=r"交点 $x=0,2$。面积 $=\int_{0}^{2}(2x-x^{2})dx=\left[x^{2}-\frac{x^{3}}{3}\right]_{0}^{2}"
           r"=4-\frac83=\frac43$。",
         q_en=r"Find the area enclosed by $y=x^{2}$ and the line $y=2x$.",
         a_en=r"$\dfrac{4}{3}$",
         s_en=r"The curves meet at $x=0,2$, so the area is "
              r"$\int_0^2(2x-x^{2})dx=4-\frac83=\frac43$.",
         check=r"eq(integrate(2*x-x**2, (x, 0, 2)), Rational(4,3))"),

    dict(id="Z08", level=2, target=TARGET, tags=["极限", "洛必达"],
         q=r"计算 $\displaystyle\lim_{x\to 0}\frac{e^{x}-1}{\sin x}$。",
         a=r"$1$",
         s=r"$e^{x}-1\sim x$、$\sin x\sim x$，比值为 1。",
         q_en=r"Evaluate $\lim_{x\to 0}\frac{e^{x}-1}{\sin x}$.",
         a_en=r"$1$",
         s_en=r"$e^{x}-1\sim x$ and $\sin x\sim x$, so the ratio tends to $1$.",
         check=r"eq(limit((exp(x)-1)/sin(x), x, 0), 1)"),

    dict(id="Z09", level=3, target=TARGET, tags=["导数应用", "单调性"],
         q=r"求 $f(x)=x^{3}-3x$ 的单调区间与极值。",
         a=r"递增区间 $(-\infty,-1)$ 与 $(1,+\infty)$，递减区间 $(-1,1)$；"
           r"极大值 $f(-1)=2$，极小值 $f(1)=-2$",
         s=r"$f'(x)=3x^{2}-3=3(x-1)(x+1)$。$f'$ 的符号决定单调性，"
           r"$x=-1$ 处由增转减为极大，$x=1$ 处由减转增为极小。",
         q_en=r"Find the intervals of monotonicity and the extrema of $f(x)=x^{3}-3x$.",
         a_en=r"Increasing on $(-\infty,-1)$ and $(1,+\infty)$; decreasing on $(-1,1)$; "
              r"local maximum $f(-1)=2$, local minimum $f(1)=-2$",
         s_en=r"$f'(x)=3(x-1)(x+1)$. The sign of $f'$ gives the intervals; $f$ changes from "
              r"increasing to decreasing at $x=-1$ (maximum) and the reverse at $x=1$ (minimum).",
         check=r"eq(diff(x**3-3*x, x), 3*x**2-3) "
               r"and eq((x**3-3*x).subs(x, -1), 2) and eq((x**3-3*x).subs(x, 1), -2)"),

    dict(id="Z10", level=2, target=TARGET, tags=["行列式"],
         q=r"计算 $\begin{vmatrix}2&1\\4&3\end{vmatrix}$。",
         a=r"$2$",
         s=r"$2\cdot3-1\cdot4=6-4=2$。",
         q_en=r"Evaluate $\begin{vmatrix}2&1\\4&3\end{vmatrix}$.",
         a_en=r"$2$",
         s_en=r"$2\cdot3-1\cdot4=2$.",
         check=r"eq(det(Matrix([[2,1],[4,3]])), 2)"),

    dict(id="Z11", level=3, target=TARGET, tags=["矩阵", "线性方程组"],
         q=r"解方程组 $\begin{cases}2x+y=5\\ x-3y=-1\end{cases}$。",
         a=r"$x=2,\ y=1$",
         s=r"消元：第一式乘 3 加第二式得 $7x=14$，故 $x=2$，回代得 $y=1$。",
         q_en=r"Solve $2x+y=5$, $x-3y=-1$.",
         a_en=r"$x=2$, $y=1$",
         s_en=r"Multiplying the first equation by $3$ and adding the second gives $7x=14$, so "
              r"$x=2$ and back-substitution gives $y=1$.",
         check=r"zero((2*x+y-5).subs({x: 2, y: 1})) and zero((x-3*y+1).subs({x: 2, y: 1}))"),

    dict(id="Z12", level=3, target=TARGET, tags=["多元", "偏导数"],
         q=r"设 $z=x^{2}y+\sin(xy)$，求 $\dfrac{\partial z}{\partial x}$、$\dfrac{\partial z}{\partial y}$。",
         a=r"$z_x=2xy+y\cos(xy)$，$z_y=x^{2}+x\cos(xy)$",
         s=r"对 $x$ 求偏导时把 $y$ 当常数，对 $\sin(xy)$ 用链式法则得 $y\cos(xy)$；对 $y$ 类似。",
         q_en=r"Let $z=x^{2}y+\sin(xy)$. Find $\partial z/\partial x$ and $\partial z/\partial y$.",
         a_en=r"$z_x=2xy+y\cos(xy)$, $z_y=x^{2}+x\cos(xy)$",
         s_en=r"Treating $y$ as constant, the chain rule on $\sin(xy)$ gives $y\cos(xy)$; "
              r"similarly for $z_y$.",
         check=r"eq(diff(x**2*y+sin(x*y), x), 2*x*y+y*cos(x*y)) "
               r"and eq(diff(x**2*y+sin(x*y), y), x**2+x*cos(x*y))"),

    dict(id="Z13", level=3, target=TARGET, tags=["微分方程"],
         q=r"求微分方程 $y'-2y=e^{3x}$ 的通解。",
         a=r"$y=Ce^{2x}+e^{3x}$",
         s=r"积分因子 $e^{-2x}$：$(ye^{-2x})'=e^{x}$，积分得 $ye^{-2x}=e^{x}+C$。",
         q_en=r"Solve $y'-2y=e^{3x}$.",
         a_en=r"$y=Ce^{2x}+e^{3x}$",
         s_en=r"The integrating factor is $e^{-2x}$, so $(ye^{-2x})'=e^{x}$ and "
              r"$ye^{-2x}=e^{x}+C$.",
         check=r"zero(diff(a*exp(2*x)+exp(3*x), x) - 2*(a*exp(2*x)+exp(3*x)) - exp(3*x))"),

    dict(id="Z14", level=4, target=TARGET, tags=["对数求导法", "幂指函数"],
         q=r"求 $y=x^{x}\ (x>0)$ 的导数。",
         a=r"$y'=x^{x}(\ln x+1)$",
         s=r"取对数 $\ln y=x\ln x$，两边求导得 $\frac{y'}{y}=\ln x+1$。",
         q_en=r"Differentiate $y=x^{x}$ for $x>0$.",
         a_en=r"$y'=x^{x}(\ln x+1)$",
         s_en=r"Taking logarithms, $\ln y=x\ln x$; differentiating gives "
              r"$y'/y=\ln x+1$.",
         check=r"eq(diff(x**x, x), x**x*(log(x)+1))"),

    dict(id="Z15", level=4, target=TARGET, tags=["反常积分"],
         q=r"判断 $\displaystyle\int_{1}^{+\infty}\frac{dx}{x^{3}}$ 是否收敛，收敛时求值。",
         a=r"收敛，值为 $\dfrac{1}{2}$",
         s=r"$\left[-\frac{1}{2x^{2}}\right]_{1}^{+\infty}=0+\frac12=\frac12$。",
         q_en=r"Determine whether $\int_{1}^{+\infty}\frac{dx}{x^{3}}$ converges, and find its value.",
         a_en=r"Converges, with value $\dfrac{1}{2}$",
         s_en=r"$\left[-\frac{1}{2x^{2}}\right]_1^{+\infty}=\frac12$.",
         check=r"eq(integrate(1/x**3, (x, 1, oo)), Rational(1,2))"),

    dict(id="Z16", level=4, target=TARGET, tags=["定积分", "换元"],
         q=r"计算 $\displaystyle\int_{0}^{\pi/2}\sin^{3}x\,dx$。",
         a=r"$\dfrac{2}{3}$",
         s=r"$\sin^{3}x=(1-\cos^{2}x)\sin x$，令 $u=\cos x$："
           r"$=\int_{0}^{1}(1-u^{2})du=1-\frac13=\frac23$。",
         q_en=r"Evaluate $\int_{0}^{\pi/2}\sin^{3}x\,dx$.",
         a_en=r"$\dfrac{2}{3}$",
         s_en=r"Write $\sin^{3}x=(1-\cos^{2}x)\sin x$ and substitute $u=\cos x$: the integral "
              r"becomes $\int_0^1(1-u^{2})du=2/3$.",
         check=r"eq(integrate(sin(x)**3, (x, 0, pi/2)), Rational(2,3))"),

    dict(id="Z17", level=4, target=TARGET, tags=["向量", "数量积"],
         q=r"已知 $\mathbf a=(1,2,-1)$、$\mathbf b=(2,-1,3)$，求 $\mathbf a\cdot\mathbf b$ 与 "
           r"$\mathbf a\times\mathbf b$。",
         a=r"$\mathbf a\cdot\mathbf b=2-2-3=-3$，"
           r"$\mathbf a\times\mathbf b=(5,-5,-5)$",
         s=r"数量积按对应分量相乘相加；向量积按行列式展开。",
         q_en=r"Given $\mathbf a=(1,2,-1)$ and $\mathbf b=(2,-1,3)$, compute $\mathbf a\cdot\mathbf b$ "
              r"and $\mathbf a\times\mathbf b$.",
         a_en=r"$\mathbf a\cdot\mathbf b=-3$, $\mathbf a\times\mathbf b=(5,-5,-5)$",
         s_en=r"The dot product multiplies corresponding components; the cross product expands as a "
              r"determinant.",
         check=r"eq(Matrix([1,2,-1]).dot(Matrix([2,-1,3])), -3) "
               r"and eq(Matrix([1,2,-1]).cross(Matrix([2,-1,3])), Matrix([5,-5,-5]))"),

    dict(id="Z18", level=5, target=TARGET, tags=["证明题", "中值定理"],
         q=r"设 $f$ 在 $[0,1]$ 上连续、在 $(0,1)$ 内可导，$f(0)=f(1)=0$。"
           r"证明存在 $\xi\in(0,1)$ 使 $f'(\xi)=0$。",
         a=r"存在这样的 $\xi$（罗尔定理）",
         s=r"$f$ 在闭区间连续，故取到最大值与最小值。若 $f\equiv0$，任取 $\xi$ 即可；"
           r"否则最值至少有一个在内部取得，该点导数为 0。",
         q_en=r"Let $f$ be continuous on $[0,1]$, differentiable on $(0,1)$, with $f(0)=f(1)=0$. "
              r"Prove that $f'(\xi)=0$ for some $\xi\in(0,1)$.",
         a_en=r"Such a $\xi$ exists (Rolle's theorem).",
         s_en=r"$f$ attains its maximum and minimum on the closed interval. If $f\equiv0$ any "
              r"$\xi$ works; otherwise an extremum is attained in the interior, where $f'=0$.",
         check=r"zero(diff(x*(x-1), x).subs(x, Rational(1,2)))"),
]
