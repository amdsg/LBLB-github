# -*- coding: utf-8 -*-
"""
原创题库 · 考研数学二
======================
说明：按考研数学二的考纲与难度编写的**风格模拟题**，不是历年真题。
数学二不含无穷级数，概率论也不在考纲内；重点是高等数学（约 78%）与线性代数（约 22%）。
"""
TOPIC = "考研数学二"
SECTION = "exam"
TARGET = "考研数学二"

PROBLEMS = [
    dict(id="E201", level=3, target=TARGET, tags=["极限", "等价无穷小"],
         q=r"计算 $\displaystyle\lim_{x\to 0}\frac{\tan x-x}{x-\sin x}$。",
         a=r"$2$",
         s=r"$\tan x=x+\frac{x^{3}}{3}+o(x^{3})$，$x-\sin x=\frac{x^{3}}{6}+o(x^{3})$，"
           r"故极限为 $\frac{1/3}{1/6}=2$。",
         q_en=r"Evaluate $\lim_{x\to 0}\frac{\tan x-x}{x-\sin x}$.",
         a_en=r"$2$",
         s_en=r"$\tan x=x+\frac{x^{3}}{3}+o(x^{3})$ and $x-\sin x=\frac{x^{3}}{6}+o(x^{3})$, so the "
              r"quotient tends to $\frac{1/3}{1/6}=2$.",
         check=r"eq(limit((tan(x)-x)/(x-sin(x)), x, 0), 2)"),

    dict(id="E202", level=3, target=TARGET, tags=["导数", "参数方程"],
         q=r"设 $\begin{cases}x=t^{2}+2t\\ y=t^{3}\end{cases}$，求 $\dfrac{d^{2}y}{dx^{2}}$。",
         a=r"$\dfrac{3t(t+2)}{4(t+1)^{3}}$",
         s=r"$\frac{dy}{dx}=\frac{3t^{2}}{2t+2}=\frac{3t^{2}}{2(t+1)}$。"
           r"再对 $x$ 求导：$\frac{d}{dt}\left(\frac{3t^{2}}{2(t+1)}\right)\Big/(2t+2)"
           r"=\frac{3t(t+2)}{2(t+1)^{2}}\cdot\frac{1}{2(t+1)}=\frac{3t(t+2)}{4(t+1)^{3}}$。",
         q_en=r"Let $x=t^{2}+2t$, $y=t^{3}$. Find $d^{2}y/dx^{2}$.",
         a_en=r"$\dfrac{3t(t+2)}{4(t+1)^{3}}$",
         s_en=r"$\frac{dy}{dx}=\frac{3t^{2}}{2t+2}=\frac{3t^{2}}{2(t+1)}$. Differentiating with "
              r"respect to $x$ (dividing by $dx/dt=2t+2$) gives "
              r"$\frac{3t(t+2)}{4(t+1)^{3}}$.",
         check=r"eq(diff(diff(t**3, t)/diff(t**2+2*t, t), t)/diff(t**2+2*t, t), 3*t*(t+2)/(4*(t+1)**3))"),

    dict(id="E203", level=3, target=TARGET, tags=["定积分", "换元"],
         q=r"计算 $\displaystyle\int_{0}^{1}\frac{x}{\sqrt{1+x^{2}}}\,dx$。",
         a=r"$\sqrt2-1$",
         s=r"令 $u=1+x^{2}$，$du=2x\,dx$：$=\frac12\int_{1}^{2}u^{-1/2}du=\left[\sqrt u\right]_{1}^{2}=\sqrt2-1$。",
         q_en=r"Evaluate $\int_{0}^{1}\frac{x}{\sqrt{1+x^{2}}}\,dx$.",
         a_en=r"$\sqrt2-1$",
         s_en=r"Substitute $u=1+x^{2}$, $du=2x\,dx$: the integral becomes "
              r"$\frac12\int_1^2 u^{-1/2}du=\left[\sqrt u\right]_1^2=\sqrt2-1$.",
         check=r"eq(integrate(x/sqrt(1+x**2), (x, 0, 1)), sqrt(2)-1)"),

    dict(id="E204", level=4, target=TARGET, tags=["二重积分", "换序"],
         q=r"计算 $\displaystyle\iint_{D}x\,d\sigma$，$D$ 由 $y=x^{2}$ 与 $y=x$ 围成。",
         a=r"$\dfrac{1}{12}$",
         s=r"交点 $x=0,1$，$D$：$x^{2}\le y\le x$。"
           r"$=\int_0^{1}x(x-x^{2})dx=\int_0^{1}(x^{2}-x^{3})dx=\frac13-\frac14=\frac1{12}$。",
         q_en=r"Evaluate $\iint_D x\,d\sigma$ where $D$ is bounded by $y=x^{2}$ and $y=x$.",
         a_en=r"$\dfrac{1}{12}$",
         s_en=r"The curves meet at $x=0,1$ and $x^{2}\le y\le x$ on $D$, so the integral is "
              r"$\int_0^1x(x-x^{2})dx=\frac13-\frac14=\frac1{12}$.",
         check=r"eq(integrate(x, (y, x**2, x), (x, 0, 1)), Rational(1,12))"),

    dict(id="E205", level=3, target=TARGET, tags=["微分方程"],
         q=r"求 $y''+4y'+4y=e^{-2x}$ 的通解。",
         a=r"$y=(C_1+C_2x)e^{-2x}+\dfrac{x^{2}}{2}e^{-2x}$",
         s=r"特征方程 $(r+2)^{2}=0$，二重根 $r=-2$，齐次解 $(C_1+C_2x)e^{-2x}$。"
           r"非齐次项与二重根共振，试设 $y^{*}=Ax^{2}e^{-2x}$，"
           r"代入得 $2A=1$，即 $A=\frac12$。",
         q_en=r"Solve $y''+4y'+4y=e^{-2x}$.",
         a_en=r"$y=(C_1+C_2x)e^{-2x}+\dfrac{x^{2}}{2}e^{-2x}$",
         s_en=r"The characteristic equation $(r+2)^{2}=0$ has a double root $r=-2$, so the "
              r"homogeneous solution is $(C_1+C_2x)e^{-2x}$. Since the forcing resonates with the "
              r"double root, try $y^{*}=Ax^{2}e^{-2x}$; substitution gives $2A=1$, so $A=\frac12$.",
         check=r"zero(diff((a+b*x)*exp(-2*x)+x**2/2*exp(-2*x), x, 2) "
               r"+ 4*diff((a+b*x)*exp(-2*x)+x**2/2*exp(-2*x), x) "
               r"+ 4*((a+b*x)*exp(-2*x)+x**2/2*exp(-2*x)) - exp(-2*x))"),

    dict(id="E206", level=3, target=TARGET, tags=["矩阵", "行列式"],
         q=r"设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $A^{-1}$ 与 $A^{2}$。",
         a=r"$A^{-1}=\begin{pmatrix}-2&1\\ \frac32&-\frac12\end{pmatrix}$，"
           r"$A^{2}=\begin{pmatrix}7&10\\15&22\end{pmatrix}$",
         s=r"$|A|=-2$，$A^{-1}=\frac{1}{|A|}A^{*}$。$A^{2}$ 直接按矩阵乘法计算。",
         q_en=r"Let $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$. Find $A^{-1}$ and $A^{2}$.",
         a_en=r"$A^{-1}=\begin{pmatrix}-2&1\\ \frac32&-\frac12\end{pmatrix}$, "
              r"$A^{2}=\begin{pmatrix}7&10\\15&22\end{pmatrix}$",
         s_en=r"$\det A=-2$ and $A^{-1}=\frac{1}{\det A}A^{*}$; $A^{2}$ follows from direct "
              r"multiplication.",
         check=r"eq(det(Matrix([[1,2],[3,4]])), -2) "
               r"and eq(Matrix([[1,2],[3,4]])**2, Matrix([[7,10],[15,22]])) "
               r"and eq(Matrix([[1,2],[3,4]]).inv(), Matrix([[-2,1],[Rational(3,2),Rational(-1,2)]]))"),

    dict(id="E207", level=4, target=TARGET, tags=["线性方程组", "参数讨论"],
         q=r"讨论 $\lambda$ 取何值时方程组 $\begin{cases}\lambda x+y+z=1\\ x+\lambda y+z=\lambda\\ x+y+\lambda z=\lambda^{2}\end{cases}$ 有唯一解。",
         a=r"当 $\lambda\neq1$ 且 $\lambda\neq-2$ 时唯一解",
         s=r"系数行列式 $=|A|=(\lambda-1)^{2}(\lambda+2)$。"
           r"$\lambda\neq1,-2$ 时 $|A|\neq0$，有唯一解；$\lambda=1$ 时无穷多解；"
           r"$\lambda=-2$ 时无解。",
         q_en=r"For which $\lambda$ does the system $\lambda x+y+z=1$, $x+\lambda y+z=\lambda$, "
              r"$x+y+\lambda z=\lambda^{2}$ have a unique solution?",
         a_en=r"Unique solution exactly when $\lambda\neq1$ and $\lambda\neq-2$.",
         s_en=r"The coefficient determinant is $(\lambda-1)^{2}(\lambda+2)$. It is nonzero — hence "
              r"the solution is unique — exactly when $\lambda\neq1,-2$. At $\lambda=1$ there are "
              r"infinitely many solutions; at $\lambda=-2$ there are none.",
         check=r"eq(det(Matrix([[a,1,1],[1,a,1],[1,1,a]])), (a-1)**2*(a+2))"),

    dict(id="E208", level=4, target=TARGET, tags=["最值", "应用"],
         q=r"在半径为 $R$ 的球内作内接圆柱，求圆柱体积的最大值。",
         a=r"最大值 $\dfrac{4\pi}{3\sqrt3}R^{3}$",
         s=r"设圆柱底面半径 $r$、高 $2h$，则 $r^{2}+h^{2}=R^{2}$。"
           r"$V=2\pi h(R^{2}-h^{2})$，$V'=2\pi(R^{2}-3h^{2})=0$ 得 $h=\frac{R}{\sqrt3}$。"
           r"$V_{\max}=2\pi\cdot\frac{R}{\sqrt3}\cdot\frac{2R^{2}}{3}=\frac{4\pi R^{3}}{3\sqrt3}$。",
         q_en=r"Find the maximum volume of a cylinder inscribed in a sphere of radius $R$.",
         a_en=r"Maximum $\dfrac{4\pi}{3\sqrt3}R^{3}$",
         s_en=r"With base radius $r$ and height $2h$ we have $r^{2}+h^{2}=R^{2}$, so "
              r"$V=2\pi h(R^{2}-h^{2})$. Setting $V'=2\pi(R^{2}-3h^{2})=0$ gives "
              r"$h=R/\sqrt3$, and the maximum volume is $\frac{4\pi R^{3}}{3\sqrt3}$.",
         check=r"eq(2*pi*a/sqrt(3)*(a**2 - a**2/3), 4*pi*a**3/(3*sqrt(3))) "
               r"and zero(diff(2*pi*x*(a**2 - x**2), x).subs(x, a/sqrt(3)))"),

    dict(id="E209", level=3, target=TARGET, tags=["特征值", "相似对角化"],
         q=r"求 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$ 的特征值与特征向量。",
         a=r"$\lambda_1=4$（对应 $(1,1)^{\mathsf T}$），$\lambda_2=2$（对应 $(1,-1)^{\mathsf T}$）",
         s=r"$|\lambda I-A|=(\lambda-3)^{2}-1=0$，得 $\lambda=4,2$。"
           r"代回解 $(A-\lambda I)x=0$ 得特征向量。",
         q_en=r"Find the eigenvalues and eigenvectors of $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$.",
         a_en=r"$\lambda_1=4$ with eigenvector $(1,1)^{\mathsf T}$; "
              r"$\lambda_2=2$ with eigenvector $(1,-1)^{\mathsf T}$",
         s_en=r"$|\lambda I-A|=(\lambda-3)^{2}-1=0$ gives $\lambda=4,2$; solving "
              r"$(A-\lambda I)x=0$ yields the stated eigenvectors.",
         check=r"eq(Matrix([[3,1],[1,3]])*Matrix([1,1]), 4*Matrix([1,1])) "
               r"and eq(Matrix([[3,1],[1,3]])*Matrix([1,-1]), 2*Matrix([1,-1]))"),

    dict(id="E210", level=3, target=TARGET, tags=["导数", "隐函数"],
         q=r"设 $y=y(x)$ 由 $e^{y}+xy=e$ 确定，求 $y'(0)$。",
         a=r"$y'(0)=-\dfrac{1}{e}$",
         s=r"$x=0$ 时 $e^{y}=e$，故 $y(0)=1$。两边对 $x$ 求导："
           r"$e^{y}y'+y+xy'=0$。代入 $x=0,y=1$：$ey'+1=0$，故 $y'(0)=-\frac1e$。",
         q_en=r"Let $y=y(x)$ be defined by $e^{y}+xy=e$. Find $y'(0)$.",
         a_en=r"$y'(0)=-\dfrac{1}{e}$",
         s_en=r"At $x=0$ we get $e^{y}=e$, so $y(0)=1$. Differentiating gives $e^{y}y'+y+xy'=0$; "
              r"substituting $x=0$, $y=1$ yields $e\,y'+1=0$, hence $y'(0)=-1/e$.",
         check=r"eq((-y/(E**y + x)).subs({x: 0, y: 1}), -1/E)"),

    dict(id="E211", level=4, target=TARGET, tags=["不定积分", "分部"],
         q=r"计算 $\displaystyle\int x^{2}\ln x\,dx$。",
         a=r"$\dfrac{x^{3}}{3}\ln x-\dfrac{x^{3}}{9}+C$",
         s=r"分部积分，取 $u=\ln x$、$dv=x^{2}dx$："
           r"$=\frac{x^{3}}{3}\ln x-\int\frac{x^{2}}{3}dx=\frac{x^{3}}{3}\ln x-\frac{x^{3}}{9}+C$。",
         q_en=r"Evaluate $\int x^{2}\ln x\,dx$.",
         a_en=r"$\dfrac{x^{3}}{3}\ln x-\dfrac{x^{3}}{9}+C$",
         s_en=r"Integrate by parts with $u=\ln x$, $dv=x^{2}dx$: the result is "
              r"$\frac{x^{3}}{3}\ln x-\frac{x^{3}}{9}+C$.",
         check=r"zero(diff(x**3/3*log(x) - x**3/9, x) - x**2*log(x))"),

    dict(id="E212", level=5, target=TARGET, tags=["证明题", "中值定理", "拔高"],
         q=r"设 $f$ 在 $[a,b]$ 上连续、在 $(a,b)$ 内可导（$0&lt;a&lt;b$），"
           r"证明存在 $\xi\in(a,b)$ 使 $f(b)-f(a)=\xi f'(\xi)\ln\dfrac{b}{a}$。",
         a=r"存在这样的 $\xi$",
         s=r"对 $f$ 与 $g(x)=\ln x$ 在 $[a,b]$ 上用柯西中值定理："
           r"存在 $\xi\in(a,b)$ 使 $\frac{f(b)-f(a)}{\ln b-\ln a}=\frac{f'(\xi)}{1/\xi}=\xi f'(\xi)$，"
           r"即得 $f(b)-f(a)=\xi f'(\xi)\ln\frac ba$。",
         q_en=r"Let $f$ be continuous on $[a,b]$ and differentiable on $(a,b)$, with $0&lt;a&lt;b$. "
              r"Prove that $f(b)-f(a)=\xi f'(\xi)\ln\frac ba$ for some $\xi\in(a,b)$.",
         a_en=r"Such a $\xi$ exists.",
         s_en=r"Apply Cauchy's mean value theorem to $f$ and $g(x)=\ln x$ on $[a,b]$: for some "
              r"$\xi\in(a,b)$, $\frac{f(b)-f(a)}{\ln b-\ln a}=\frac{f'(\xi)}{1/\xi}=\xi f'(\xi)$, "
              r"which rearranges to the claim.",
         check=r"eq(diff(log(x), x).subs(x, 2), Rational(1,2)) "
               r"and eq(2*Rational(1,2), 1)"),

    dict(id="E213", level=3, target=TARGET, tags=["二重积分", "极坐标"],
         q=r"计算 $\displaystyle\iint_{D}\sqrt{x^{2}+y^{2}}\,d\sigma$，$D:x^{2}+y^{2}\le a^{2}$，$y\ge0$。",
         a=r"$\dfrac{\pi a^{3}}{3}$",
         s=r"极坐标下 $=\int_{0}^{\pi}\!\int_{0}^{a}r\cdot r\,dr\,d\theta"
           r"=\pi\cdot\frac{a^{3}}{3}$。",
         q_en=r"Evaluate $\iint_D\sqrt{x^{2}+y^{2}}\,d\sigma$ for the upper half-disc "
              r"$x^{2}+y^{2}\le a^{2}$, $y\ge0$.",
         a_en=r"$\dfrac{\pi a^{3}}{3}$",
         s_en=r"In polar coordinates the integral is "
              r"$\int_0^{\pi}\!\int_0^{a}r^{2}\,dr\,d\theta=\pi a^{3}/3$.",
         check=r"eq(integrate(r*r, (r, 0, a), (t, 0, pi)), pi*a**3/3)"),

    dict(id="E214", level=4, target=TARGET, tags=["向量组", "线性相关"],
         q=r"判断向量组 $\alpha_1=(1,2,3)^{\mathsf T}$、$\alpha_2=(2,4,6)^{\mathsf T}$、"
           r"$\alpha_3=(1,0,1)^{\mathsf T}$ 的线性相关性，并求其秩。",
         a=r"线性相关，秩为 $2$",
         s=r"$\alpha_2=2\alpha_1$，故相关。以它们为列作矩阵，"
           r"$\alpha_1,\alpha_3$ 不成比例，故秩为 2。",
         q_en=r"Determine whether $\alpha_1=(1,2,3)^{\mathsf T}$, $\alpha_2=(2,4,6)^{\mathsf T}$, "
              r"$\alpha_3=(1,0,1)^{\mathsf T}$ are linearly dependent, and find the rank.",
         a_en=r"Linearly dependent; rank $2$.",
         s_en=r"$\alpha_2=2\alpha_1$, so the set is dependent. As columns, $\alpha_1$ and "
              r"$\alpha_3$ are not proportional, so the rank is $2$.",
         check=r"eq(Matrix([[1,2,1],[2,4,0],[3,6,1]]).rank(), 2)"),

    dict(id="E215", level=4, target=TARGET, tags=["极限", "定积分定义"],
         q=r"计算 $\displaystyle\lim_{n\to\infty}\frac{1}{n}\sum_{k=1}^{n}\sin\frac{k\pi}{n}$。",
         a=r"$\dfrac{2}{\pi}$",
         s=r"这是 $\int_{0}^{1}\sin(\pi x)dx$ 的黎曼和，"
           r"$=\left[-\frac{\cos\pi x}{\pi}\right]_{0}^{1}=\frac{2}{\pi}$。",
         q_en=r"Evaluate $\lim_{n\to\infty}\frac{1}{n}\sum_{k=1}^{n}\sin\frac{k\pi}{n}$.",
         a_en=r"$\dfrac{2}{\pi}$",
         s_en=r"This is the Riemann sum for $\int_0^1\sin(\pi x)dx="
              r"\left[-\frac{\cos\pi x}{\pi}\right]_0^1=\frac{2}{\pi}$.",
         check=r"eq(integrate(sin(pi*x), (x, 0, 1)), 2/pi)"),
]
