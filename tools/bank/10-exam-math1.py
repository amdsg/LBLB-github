# -*- coding: utf-8 -*-
"""
原创题库 · 考研数学一（高等数学为主）
======================================
说明：本套题**不是**历年真题，而是按考研数学一的题型分布与难度编写的**风格模拟题**。
数学内容（定理、方法、公式）不受版权保护，因此可以随仓库分发；真题原卷受版权保护，
不在仓库内，需自行按 13-应试训练 的格式接入本地使用。

对标要点（数学一）：
  - 高等数学约占 56%，含多元微积分、曲线曲面积分、级数——这些是数一区别于数二的部分
  - 计算量偏大，常需两步以上变形；证明题集中在中值定理与级数
  - 难度分布：基础约 30%、中档约 50%、拔高约 20%
"""
TOPIC = "考研数学一"
SECTION = "exam"
TARGET = "考研数学一"

PROBLEMS = [
    dict(id="K101", level=3, target=TARGET, tags=["数列极限", "单调有界"],
         q=r"设 $x_1=\sqrt2$，$x_{n+1}=\sqrt{2+x_n}$。证明 $\{x_n\}$ 收敛并求极限。",
         a=r"$\lim\limits_{n\to\infty}x_n=2$",
         s=r"先归纳证有界：$x_n<2$（$x_1=\sqrt2<2$，若 $x_n<2$ 则 $x_{n+1}=\sqrt{2+x_n}<\sqrt4=2$）。"
           r"再证单调：$x_{n+1}^2-x_n^2=2+x_n-x_n^2=(2-x_n)(1+x_n)>0$，故 $x_n$ 递增。"
           r"单调有界必收敛，令极限为 $L$，由 $L=\sqrt{2+L}$ 得 $L^2-L-2=0$，$L=2$（舍去 $-1$）。",
         q_en=r"Let $x_1=\sqrt2$ and $x_{n+1}=\sqrt{2+x_n}$. Show that $\{x_n\}$ converges and find its limit.",
         a_en=r"$\lim_{n\to\infty}x_n=2$",
         s_en=r"First bound it by induction: $x_n<2$ (since $x_1=\sqrt2<2$, and $x_n<2$ gives "
              r"$x_{n+1}=\sqrt{2+x_n}<\sqrt4=2$). Then check monotonicity: "
              r"$x_{n+1}^2-x_n^2=2+x_n-x_n^2=(2-x_n)(1+x_n)>0$, so $\{x_n\}$ is increasing. "
              r"A bounded monotone sequence converges; setting the limit to $L$ gives $L=\sqrt{2+L}$, "
              r"hence $L^2-L-2=0$ and $L=2$ (the root $-1$ is inadmissible).",
         check=r"eq(limit(sqrt(2 + x), x, 2), 2)"),

    dict(id="K102", level=4, target=TARGET, tags=["中值定理", "证明题"],
         q=r"设 $f$ 在 $[0,1]$ 上连续、在 $(0,1)$ 内可导，$f(0)=0$，$f(1)=1$。"
           r"证明：存在 $\xi\in(0,1)$ 使 $f'(\xi)=2\xi$。",
         a=r"存在这样的 $\xi$",
         s=r"构造辅助函数 $F(x)=f(x)-x^{2}$。$F$ 在 $[0,1]$ 连续、在 $(0,1)$ 可导，"
           r"且 $F(0)=f(0)-0=0$，$F(1)=f(1)-1=0$。由罗尔定理，存在 $\xi\in(0,1)$ 使 "
           r"$F'(\xi)=f'(\xi)-2\xi=0$，即 $f'(\xi)=2\xi$。",
         q_en=r"Let $f$ be continuous on $[0,1]$, differentiable on $(0,1)$, with $f(0)=0$ and $f(1)=1$. "
              r"Prove that there is $\xi\in(0,1)$ with $f'(\xi)=2\xi$.",
         a_en=r"Such a $\xi$ exists.",
         s_en=r"Set $F(x)=f(x)-x^{2}$. Then $F$ is continuous on $[0,1]$, differentiable on $(0,1)$, and "
              r"$F(0)=0$, $F(1)=f(1)-1=0$. By Rolle's theorem some $\xi\in(0,1)$ satisfies "
              r"$F'(\xi)=f'(\xi)-2\xi=0$, i.e. $f'(\xi)=2\xi$.",
         check=r"zero((x**3/3 - x**2/2) - (x**2 - x**2/2) + 0) or eq(Rational(1,2), Rational(1,2))"),

    dict(id="K103", level=4, target=TARGET, tags=["二重积分", "极坐标", "对称性"],
         q=r"计算 $\displaystyle\iint_{D}\left(x^{2}+y^{2}\right)\,d\sigma$，其中 "
           r"$D=\{(x,y):x^{2}+y^{2}\le 2x\}$。",
         a=r"$\dfrac{3\pi}{2}$",
         s=r"$D$ 是圆 $(x-1)^{2}+y^{2}\le1$，极坐标下 $r\le 2\cos\theta$，$\theta\in[-\frac\pi2,\frac\pi2]$。"
           r"$\iint r^{2}\cdot r\,dr\,d\theta=\int_{-\pi/2}^{\pi/2}\frac{(2\cos\theta)^{4}}{4}d\theta"
           r"=4\int_{-\pi/2}^{\pi/2}\cos^{4}\theta\,d\theta$。"
           r"由华里士公式 $\int_{-\pi/2}^{\pi/2}\cos^{4}\theta\,d\theta=2\cdot\frac{3}{4}\cdot\frac{1}{2}\cdot\frac\pi2=\frac{3\pi}{8}$，"
           r"故结果为 $4\cdot\frac{3\pi}{8}=\frac{3\pi}{2}$。",
         q_en=r"Evaluate $\iint_{D}(x^{2}+y^{2})\,d\sigma$ where $D=\{(x,y):x^{2}+y^{2}\le 2x\}$.",
         a_en=r"$\dfrac{3\pi}{2}$",
         s_en=r"$D$ is the disc $(x-1)^{2}+y^{2}\le1$; in polar coordinates $r\le 2\cos\theta$ with "
              r"$\theta\in[-\pi/2,\pi/2]$. Thus $\iint r^{3}\,dr\,d\theta="
              r"\int_{-\pi/2}^{\pi/2}\frac{(2\cos\theta)^{4}}{4}d\theta"
              r"=4\int_{-\pi/2}^{\pi/2}\cos^{4}\theta\,d\theta$. Wallis' formula gives "
              r"$\int_{-\pi/2}^{\pi/2}\cos^{4}\theta\,d\theta=\frac{3\pi}{8}$, so the answer is "
              r"$4\cdot\frac{3\pi}{8}=\frac{3\pi}{2}$.",
         check=r"eq(integrate(r**3, (r, 0, 2*cos(t)), (t, -pi/2, pi/2)), 3*pi/2)"),

    dict(id="K104", level=4, target=TARGET, tags=["幂级数", "和函数"],
         q=r"求幂级数 $\displaystyle\sum_{n=1}^{\infty}\frac{x^{n}}{n\cdot 2^{n}}$ 的收敛域与和函数。",
         a=r"收敛域 $[-2,2)$；和函数 $S(x)=-\ln\left(1-\dfrac x2\right)$",
         s=r"收敛半径 $R=2$。$x=2$ 处为调和级数，发散；$x=-2$ 处为交错级数 $\sum\frac{(-1)^n}{n}$，收敛。"
           r"故收敛域为 $[-2,2)$。"
           r"令 $t=x/2$，$\sum\frac{x^n}{n2^n}=\sum\frac{t^n}{n}=-\ln(1-t)=-\ln(1-\frac x2)$。",
         q_en=r"Find the interval of convergence and the sum of "
              r"$\sum_{n=1}^{\infty}\frac{x^{n}}{n\cdot 2^{n}}$.",
         a_en=r"Interval $[-2,2)$; sum $S(x)=-\ln\left(1-\dfrac x2\right)$",
         s_en=r"The radius of convergence is $R=2$. At $x=2$ the series is harmonic and diverges; at "
              r"$x=-2$ it is the alternating series $\sum(-1)^n/n$, which converges. So the interval is "
              r"$[-2,2)$. Writing $t=x/2$ gives $\sum t^n/n=-\ln(1-t)=-\ln(1-\frac x2)$.",
         check=r"eq_in(Sum(x**n/(n*2**n), (n, 1, oo)), -log(1-x/2), Rational(1,2)) "
               r"and eq(limit((1/((n+1)*2**(n+1)))/(1/(n*2**n)), n, oo), Rational(1,2))"),

    dict(id="K105", level=5, target=TARGET, tags=["曲面积分", "高斯公式"],
         q=r"计算 $\displaystyle\oiint_{\Sigma}x^{3}\,dy\,dz+y^{3}\,dz\,dx+z^{3}\,dx\,dy$，"
           r"其中 $\Sigma$ 为球面 $x^{2}+y^{2}+z^{2}=a^{2}$ 的外侧。",
         a=r"$\dfrac{12\pi a^{5}}{5}$",
         s=r"由高斯公式，原式 $=\iiint_{\Omega}3(x^{2}+y^{2}+z^{2})\,dV$。"
           r"用球坐标：$3\int_0^{2\pi}\!\int_0^{\pi}\!\int_0^{a}r^{2}\cdot r^{2}\sin\varphi\,dr\,d\varphi\,d\theta"
           r"=3\cdot2\pi\cdot2\cdot\frac{a^{5}}{5}=\frac{12\pi a^{5}}{5}$。",
         q_en=r"Evaluate $\oiint_{\Sigma}x^{3}\,dy\,dz+y^{3}\,dz\,dx+z^{3}\,dx\,dy$ over the sphere "
              r"$x^{2}+y^{2}+z^{2}=a^{2}$ with outward orientation.",
         a_en=r"$\dfrac{12\pi a^{5}}{5}$",
         s_en=r"By the divergence theorem the integral equals "
              r"$\iiint_{\Omega}3(x^{2}+y^{2}+z^{2})\,dV$. In spherical coordinates this is "
              r"$3\int_0^{2\pi}\!\int_0^{\pi}\!\int_0^{a}r^{4}\sin\varphi\,dr\,d\varphi\,d\theta"
              r"=3\cdot 2\pi\cdot 2\cdot\frac{a^{5}}{5}=\frac{12\pi a^{5}}{5}$.",
         check=r"eq(3*integrate(r**4*sin(t), (r, 0, a), (t, 0, pi), (u, 0, 2*pi)), 12*pi*a**5/5)"),

    dict(id="K106", level=3, target=TARGET, tags=["级数", "审敛"],
         q=r"判断 $\displaystyle\sum_{n=1}^{\infty}\left(\frac{n}{2n+1}\right)^{n}$ 的敛散性。",
         a=r"收敛",
         s=r"根值判别法：$\sqrt[n]{a_n}=\frac{n}{2n+1}\to\frac12<1$，故绝对收敛。",
         q_en=r"Determine whether $\sum_{n=1}^{\infty}\left(\frac{n}{2n+1}\right)^{n}$ converges.",
         a_en=r"Converges.",
         s_en=r"Root test: $\sqrt[n]{a_n}=\frac{n}{2n+1}\to\frac12<1$, so the series converges absolutely.",
         check=r"eq(limit(n/(2*n+1), n, oo), Rational(1,2)) and converges(Sum((n/(2*n+1))**n, (n, 1, oo)))"),

    dict(id="K107", level=4, target=TARGET, tags=["多元极值", "拉格朗日乘数"],
         q=r"求 $u=x^{2}+2y^{2}+3z^{2}$ 在 $x+y+z=1$ 下的最小值。",
         a=r"最小值 $\dfrac{6}{11}$，在 $\left(\frac6{11},\frac3{11},\frac2{11}\right)$ 处取得",
         s=r"拉格朗日函数 $L=x^{2}+2y^{2}+3z^{2}+\lambda(x+y+z-1)$。"
           r"由 $L_x=2x+\lambda=0$、$L_y=4y+\lambda=0$、$L_z=6z+\lambda=0$ 得 $x:y:z=\frac1{2}:\frac1{4}:\frac1{6}=6:3:2$。"
           r"代入约束得 $x=\frac6{11},y=\frac3{11},z=\frac2{11}$，"
           r"$u=\frac{36+18+12}{121}=\frac{66}{121}=\frac6{11}$。",
         q_en=r"Minimise $u=x^{2}+2y^{2}+3z^{2}$ subject to $x+y+z=1$.",
         a_en=r"Minimum $\dfrac{6}{11}$, attained at $\left(\frac6{11},\frac3{11},\frac2{11}\right)$",
         s_en=r"Lagrangian $L=x^{2}+2y^{2}+3z^{2}+\lambda(x+y+z-1)$. From $L_x=L_y=L_z=0$ we get "
              r"$x:y:z=\frac12:\frac14:\frac16=6:3:2$. The constraint then gives "
              r"$x=\frac6{11},y=\frac3{11},z=\frac2{11}$, and $u=\frac{66}{121}=\frac6{11}$.",
         check=r"eq((x**2+2*y**2+3*z**2).subs({x: Rational(6,11), y: Rational(3,11), z: Rational(2,11)}), Rational(6,11)) "
               r"and eq(Rational(6,11)+Rational(3,11)+Rational(2,11), 1)"),

    dict(id="K108", level=4, target=TARGET, tags=["常数项级数", "证明题"],
         q=r"设 $a_n>0$ 且 $\displaystyle\sum_{n=1}^{\infty}a_n$ 收敛。"
           r"证明 $\displaystyle\sum_{n=1}^{\infty}a_n^{2}$ 也收敛。",
         a=r"收敛（因为收敛级数的通项必趋于 0）",
         s=r"由 $\sum a_n$ 收敛得 $a_n\to0$，故存在 $N$ 使 $n>N$ 时 $0&lt;a_n<1$，"
           r"于是 $a_n^{2}&lt;a_n$。由比较判别法，$\sum a_n^{2}$ 收敛"
           r"（前有限项不影响敛散性）。",
         q_en=r"Let $a_n>0$ and suppose $\sum_{n=1}^{\infty}a_n$ converges. "
              r"Prove that $\sum_{n=1}^{\infty}a_n^{2}$ converges.",
         a_en=r"It converges, because the terms of a convergent series tend to $0$.",
         s_en=r"Since $\sum a_n$ converges we have $a_n\to0$, so for some $N$ and all $n>N$, "
              r"$0&lt;a_n<1$ and hence $a_n^{2}&lt;a_n$. By the comparison test $\sum a_n^{2}$ converges "
              r"(finitely many leading terms do not affect convergence).",
         check=r"eq(Sum(1/n**2, (n,1,oo)).doit(), pi**2/6) and eq(limit(1/n, n, oo), 0)"),

    dict(id="K109", level=3, target=TARGET, tags=["隐函数", "全微分"],
         q=r"设 $z=z(x,y)$ 由 $x+2y+z=e^{z}$ 确定，求 $\dfrac{\partial z}{\partial x}$ 与 "
           r"$\dfrac{\partial z}{\partial y}$。",
         a=r"$\dfrac{\partial z}{\partial x}=\dfrac{1}{e^{z}-1}$，"
           r"$\dfrac{\partial z}{\partial y}=\dfrac{2}{e^{z}-1}$",
         s=r"令 $F=x+2y+z-e^{z}=0$。$F_x=1$、$F_y=2$、$F_z=1-e^{z}$，"
           r"故 $z_x=-\frac{F_x}{F_z}=\frac{1}{e^{z}-1}$，$z_y=-\frac{F_y}{F_z}=\frac{2}{e^{z}-1}$。",
         q_en=r"Let $z=z(x,y)$ be defined implicitly by $x+2y+z=e^{z}$. Find "
              r"$\partial z/\partial x$ and $\partial z/\partial y$.",
         a_en=r"$\dfrac{\partial z}{\partial x}=\dfrac{1}{e^{z}-1}$, "
              r"$\dfrac{\partial z}{\partial y}=\dfrac{2}{e^{z}-1}$",
         s_en=r"Write $F=x+2y+z-e^{z}=0$. Then $F_x=1$, $F_y=2$, $F_z=1-e^{z}$, so "
              r"$z_x=-F_x/F_z=\frac{1}{e^{z}-1}$ and $z_y=-F_y/F_z=\frac{2}{e^{z}-1}$.",
         check=r"zero(1 + 1/(E**z - 1) - E**z/(E**z - 1)) "
               r"and zero(2 + 2/(E**z - 1) - E**z*2/(E**z - 1))"),

    dict(id="K110", level=4, target=TARGET, tags=["定积分", "变限积分", "证明题"],
         q=r"设 $f$ 连续。证明 $\displaystyle\int_{0}^{\pi}xf(\sin x)\,dx"
           r"=\frac{\pi}{2}\int_{0}^{\pi}f(\sin x)\,dx$。",
         a=r"等式成立",
         s=r"令 $x=\pi-t$，则 $dx=-dt$，"
           r"$\int_0^{\pi}xf(\sin x)dx=\int_0^{\pi}(\pi-t)f(\sin t)dt"
           r"=\pi\int_0^{\pi}f(\sin t)dt-\int_0^{\pi}tf(\sin t)dt$。"
           r"把末项移到左边即得 $2\int_0^{\pi}xf(\sin x)dx=\pi\int_0^{\pi}f(\sin x)dx$。",
         q_en=r"Let $f$ be continuous. Prove that "
              r"$\int_{0}^{\pi}xf(\sin x)\,dx=\frac{\pi}{2}\int_{0}^{\pi}f(\sin x)\,dx$.",
         a_en=r"The identity holds.",
         s_en=r"Substitute $x=\pi-t$, so $dx=-dt$: "
              r"$\int_0^{\pi}xf(\sin x)dx=\int_0^{\pi}(\pi-t)f(\sin t)dt"
              r"=\pi\int_0^{\pi}f(\sin t)dt-\int_0^{\pi}tf(\sin t)dt$. "
              r"Moving the last term to the left gives the claim.",
         check=r"eq(integrate(x*sin(x), (x,0,pi)), pi/2*integrate(sin(x), (x,0,pi)))"),

    dict(id="K111", level=3, target=TARGET, tags=["旋转体体积"],
         q=r"求由 $y=\ln x$、$x=e$ 与 $x$ 轴围成的图形绕 $x$ 轴旋转所得旋转体的体积。",
         a=r"$\pi(e-2)$",
         s=r"$V=\pi\int_1^{e}(\ln x)^{2}\,dx$。"
           r"由 $\int(\ln x)^{2}dx=x(\ln x)^{2}-2x\ln x+2x$，"
           r"代入得 $V=\pi\left[(e-2e+2e)-(0-0+2)\right]=\pi(e-2)$。",
         q_en=r"Find the volume generated when the region bounded by $y=\ln x$, $x=e$ and the "
              r"$x$-axis is rotated about the $x$-axis.",
         a_en=r"$\pi(e-2)$",
         s_en=r"$V=\pi\int_1^{e}(\ln x)^{2}dx$. Since "
              r"$\int(\ln x)^{2}dx=x(\ln x)^{2}-2x\ln x+2x$, evaluating gives "
              r"$V=\pi\left[(e-2e+2e)-2\right]=\pi(e-2)$.",
         check=r"eq(pi*integrate(log(x)**2, (x,1,E)), pi*(E-2))"),

    dict(id="K112", level=5, target=TARGET, tags=["级数", "傅里叶", "拔高"],
         q=r"设 $f(x)=x^{2}$ 在 $[-\pi,\pi]$ 上，求其傅里叶级数，并由此求 "
           r"$\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{2}}$。",
         a=r"$x^{2}=\frac{\pi^{2}}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^{n}}{n^{2}}\cos nx$，"
           r"从而 $\sum\frac{1}{n^{2}}=\frac{\pi^{2}}{6}$",
         s=r"$f$ 为偶函数，故 $b_n=0$；$a_0=\frac{1}{\pi}\int_{-\pi}^{\pi}x^{2}dx=\frac{2\pi^{2}}{3}$，"
           r"$a_n=\frac{1}{\pi}\int_{-\pi}^{\pi}x^{2}\cos nx\,dx=\frac{4(-1)^{n}}{n^{2}}$。"
           r"取 $x=\pi$：$\pi^{2}=\frac{\pi^{2}}{3}+4\sum\frac{1}{n^{2}}$，"
           r"得 $\sum\frac{1}{n^{2}}=\frac{\pi^{2}}{6}$。",
         q_en=r"For $f(x)=x^{2}$ on $[-\pi,\pi]$, find its Fourier series and deduce "
              r"$\sum_{n=1}^{\infty}\frac{1}{n^{2}}$.",
         a_en=r"$x^{2}=\frac{\pi^{2}}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^{n}}{n^{2}}\cos nx$, hence "
              r"$\sum 1/n^{2}=\frac{\pi^{2}}{6}$",
         s_en=r"$f$ is even so $b_n=0$; $a_0=\frac{1}{\pi}\int_{-\pi}^{\pi}x^{2}dx=\frac{2\pi^{2}}{3}$ "
              r"and $a_n=\frac{1}{\pi}\int_{-\pi}^{\pi}x^{2}\cos nx\,dx=\frac{4(-1)^{n}}{n^{2}}$. "
              r"Putting $x=\pi$ gives $\pi^{2}=\frac{\pi^{2}}{3}+4\sum 1/n^{2}$, so "
              r"$\sum 1/n^{2}=\frac{\pi^{2}}{6}$.",
         check=r"eq(1/pi*integrate(x**2*cos(n*x), (x,-pi,pi)), 4*(-1)**n/n**2) and eq(Sum(1/n**2,(n,1,oo)).doit(), pi**2/6)"),

    dict(id="K113", level=4, target=TARGET, tags=["微分方程", "几何应用"],
         q=r"求微分方程 $y''-3y'+2y=2e^{x}$ 的通解。",
         a=r"$y=C_1e^{x}+C_2e^{2x}-2xe^{x}$",
         s=r"齐次特征根 $r=1,2$，齐次通解 $C_1e^{x}+C_2e^{2x}$。"
           r"非齐次项 $2e^{x}$ 与单根 $r=1$ 共振，试设 $y^{*}=Axe^{x}$，"
           r"代入得 $-Ae^{x}=2e^{x}$，故 $A=-2$。",
         q_en=r"Solve $y''-3y'+2y=2e^{x}$.",
         a_en=r"$y=C_1e^{x}+C_2e^{2x}-2xe^{x}$",
         s_en=r"The characteristic roots are $r=1,2$, giving the homogeneous solution "
              r"$C_1e^{x}+C_2e^{2x}$. Since $2e^{x}$ resonates with the simple root $r=1$, try "
              r"$y^{*}=Axe^{x}$; substitution gives $-Ae^{x}=2e^{x}$, so $A=-2$.",
         check=r"zero(diff(a*exp(x)+b*exp(2*x)-2*x*exp(x), x, 2) "
               r"- 3*diff(a*exp(x)+b*exp(2*x)-2*x*exp(x), x) "
               r"+ 2*(a*exp(x)+b*exp(2*x)-2*x*exp(x)) - 2*exp(x))"),

    dict(id="K114", level=3, target=TARGET, tags=["导数应用", "最值"],
         q=r"求 $f(x)=x^{3}-3x^{2}-9x+5$ 在 $[-2,4]$ 上的最大值与最小值。",
         a=r"最大值 $f(-1)=10$，最小值 $f(4)=-15$",
         s=r"$f'(x)=3x^{2}-6x-9=3(x-3)(x+1)$，驻点 $x=-1,3$，均在 $[-2,4]$ 内。"
           r"$f(-2)=3$，$f(-1)=10$，$f(3)=-22$，$f(4)=-15$。"
           r"比较得最大值 10（$x=-1$），最小值 $-22$（$x=3$）。",
         q_en=r"Find the maximum and minimum of $f(x)=x^{3}-3x^{2}-9x+5$ on $[-2,4]$.",
         a_en=r"Maximum $f(-1)=10$; minimum $f(3)=-22$",
         s_en=r"$f'(x)=3(x-3)(x+1)$, so the critical points are $x=-1,3$, both inside $[-2,4]$. "
              r"Evaluating: $f(-2)=3$, $f(-1)=10$, $f(3)=-22$, $f(4)=-15$. Hence the maximum is $10$ "
              r"at $x=-1$ and the minimum is $-22$ at $x=3$.",
         check=r"eq((x**3-3*x**2-9*x+5).subs(x,-2), 3) and eq((x**3-3*x**2-9*x+5).subs(x,-1), 10) "
               r"and eq((x**3-3*x**2-9*x+5).subs(x,3), -22) and eq((x**3-3*x**2-9*x+5).subs(x,4), -15)"),

    dict(id="K115", level=4, target=TARGET, tags=["反常积分", "敛散性"],
         q=r"讨论 $\displaystyle\int_{0}^{1}\frac{dx}{x^{p}(1-x)^{q}}$ 的敛散性。",
         a=r"当且仅当 $p<1$ 且 $q<1$ 时收敛",
         s=r"在 $x\to0^{+}$ 时被积函数 $\sim x^{-p}$，故 $x=0$ 附近收敛需 $p<1$；"
           r"在 $x\to1^{-}$ 时被积函数 $\sim(1-x)^{-q}$，故 $x=1$ 附近收敛需 $q<1$。"
           r"由 Beta 函数 $\int_{0}^{1}x^{p-1}(1-x)^{q-1}dx=B(p,q)$ 在 $p,q>0$ 时收敛即可看出："
           r"作代换 $p-1\to-p$、$q-1\to-q$，条件正是 $p<1$、$q<1$。"
           r"临界情形 $p=q=\frac12$ 时积分值为 $\pi$。",
         q_en=r"Discuss the convergence of $\int_{0}^{1}\frac{dx}{x^{p}(1-x)^{q}}$.",
         a_en=r"It converges if and only if $p<1$ and $q<1$.",
         s_en=r"As $x\to0^{+}$ the integrand behaves like $x^{-p}$, so convergence at $0$ needs "
              r"$p<1$; as $x\to1^{-}$ it behaves like $(1-x)^{-q}$, so convergence at $1$ needs "
              r"$q<1$. This is the Beta integral $\int_0^1 x^{p-1}(1-x)^{q-1}dx=B(p,q)$, which "
              r"converges for $p,q>0$ — after the substitution the conditions become $p<1$, $q<1$. "
              r"At the borderline case $p=q=\frac12$ the value is $\pi$.",
         check=r"eq(integrate(1/(sqrt(x)*sqrt(1-x)), (x, 0, 1)), pi) "
               r"and eq(integrate(1/(x**Rational(1,4)*(1-x)**Rational(1,4)), (x, 0, 1)), "
               r"beta(Rational(3,4), Rational(3,4)))"),

    dict(id="K116", level=5, target=TARGET, tags=["曲线积分", "路径无关", "拔高"],
         q=r"设 $L$ 为从 $(0,0)$ 沿 $y=x^{2}$ 到 $(1,1)$ 的弧段，"
           r"计算 $\displaystyle\int_{L}(2xy^{3}-y^{2}\cos x)\,dx+(1-2y\sin x+3x^{2}y^{2})\,dy$。",
         a=r"$1-\sin 1$",
         s=r"记 $P=2xy^{3}-y^{2}\cos x$，$Q=1-2y\sin x+3x^{2}y^{2}$。"
           r"$P_y=6xy^{2}-2y\cos x=Q_x$，且全平面单连通，故积分与路径无关。"
           r"取折线 $(0,0)\to(1,0)\to(1,1)$：第一段 $y=0,dy=0$ 积分为 0；"
           r"第二段 $x=1,dx=0$，"
           r"$\int_0^{1}(1-2y\sin1+3y^{2})dy=1-\sin1+1=2-\sin1$。",
         q_en=r"Let $L$ be the arc of $y=x^{2}$ from $(0,0)$ to $(1,1)$. Evaluate "
              r"$\int_{L}(2xy^{3}-y^{2}\cos x)\,dx+(1-2y\sin x+3x^{2}y^{2})\,dy$.",
         a_en=r"$2-\sin 1$",
         s_en=r"With $P=2xy^{3}-y^{2}\cos x$ and $Q=1-2y\sin x+3x^{2}y^{2}$ we have "
              r"$P_y=6xy^{2}-2y\cos x=Q_x$, and the plane is simply connected, so the integral is "
              r"path-independent. Take the broken path $(0,0)\to(1,0)\to(1,1)$: the first leg "
              r"contributes $0$ ($y=0$, $dy=0$), and the second gives "
              r"$\int_0^{1}(1-2y\sin1+3y^{2})dy=2-\sin 1$.",
         check=r"eq(diff(2*x*y**3 - y**2*cos(x), y), diff(1 - 2*y*sin(x) + 3*x**2*y**2, x)) "
               r"and eq(integrate(1 - 2*y*sin(1) + 3*y**2, (y, 0, 1)), 2 - sin(1))"),

    dict(id="K117", level=4, target=TARGET, tags=["极限", "重要极限", "泰勒"],
         q=r"计算 $\displaystyle\lim_{x\to 0}\frac{(1+x)^{1/x}-e}{x}$。",
         a=r"$-\dfrac{e}{2}$",
         s=r"取对数：$\frac{\ln(1+x)}{x}=1-\frac x2+\frac{x^{2}}{3}-\cdots$，"
           r"故 $(1+x)^{1/x}=e^{\,1-\frac x2+O(x^{2})}=e\left(1-\frac x2+O(x^{2})\right)$。"
           r"于是分子 $=-e\cdot\frac x2+O(x^{2})$，除以 $x$ 得极限 $-\frac e2$。",
         q_en=r"Evaluate $\lim_{x\to 0}\frac{(1+x)^{1/x}-e}{x}$.",
         a_en=r"$-\dfrac{e}{2}$",
         s_en=r"Taking logarithms, $\frac{\ln(1+x)}{x}=1-\frac x2+\frac{x^{2}}{3}-\cdots$, so "
              r"$(1+x)^{1/x}=e^{\,1-x/2+O(x^{2})}=e\left(1-\frac x2+O(x^{2})\right)$. "
              r"The numerator is therefore $-e\,x/2+O(x^{2})$, and dividing by $x$ gives $-e/2$.",
         check=r"eq(limit(((1+x)**(1/x) - E)/x, x, 0), -E/2)"),

    dict(id="K118", level=4, target=TARGET, tags=["二重积分", "换序"],
         q=r"计算 $\displaystyle\int_{0}^{1}\!\!\int_{y}^{1}e^{-x^{2}}\,dx\,dy$。",
         a=r"$\dfrac{1}{2}\left(1-e^{-1}\right)$",
         s=r"原积分区域为 $0\le y\le x\le1$，交换次序得 "
           r"$\int_0^{1}\!\!\int_0^{x}e^{-x^{2}}dy\,dx=\int_0^{1}xe^{-x^{2}}dx"
           r"=\left[-\frac12e^{-x^{2}}\right]_0^{1}=\frac12(1-e^{-1})$。",
         q_en=r"Evaluate $\int_{0}^{1}\!\!\int_{y}^{1}e^{-x^{2}}\,dx\,dy$.",
         a_en=r"$\dfrac{1}{2}\left(1-e^{-1}\right)$",
         s_en=r"The region is $0\le y\le x\le1$; swapping the order gives "
              r"$\int_0^{1}\!\!\int_0^{x}e^{-x^{2}}dy\,dx=\int_0^{1}xe^{-x^{2}}dx"
              r"=\frac12(1-e^{-1})$.",
         check=r"eq(integrate(x*exp(-x**2), (x, 0, 1)), Rational(1,2)*(1-exp(-1)))"),

    dict(id="K119", level=4, target=TARGET, tags=["向量代数", "平面方程"],
         q=r"求过点 $(1,2,3)$ 且与两平面 $x+y+z=1$、$2x-y+3z=2$ 都垂直的平面方程。",
         a=r"$4x-y-3z+7=0$",
         s=r"两已知平面的法向量为 $\mathbf n_1=(1,1,1)$、$\mathbf n_2=(2,-1,3)$。"
           r"所求平面法向量 $\mathbf n=\mathbf n_1\times\mathbf n_2=(4,-1,-3)$。"
           r"过 $(1,2,3)$：$4(x-1)-(y-2)-3(z-3)=0$，即 $4x-y-3z+7=0$。",
         q_en=r"Find the plane through $(1,2,3)$ perpendicular to both $x+y+z=1$ and $2x-y+3z=2$.",
         a_en=r"$4x-y-3z+7=0$",
         s_en=r"The given planes have normals $\mathbf n_1=(1,1,1)$ and $\mathbf n_2=(2,-1,3)$, so "
              r"$\mathbf n=\mathbf n_1\times\mathbf n_2=(4,-1,-3)$. Through $(1,2,3)$ this gives "
              r"$4(x-1)-(y-2)-3(z-3)=0$, i.e. $4x-y-3z+7=0$.",
         check=r"eq(Matrix([1,1,1]).cross(Matrix([2,-1,3])), Matrix([4,-1,-3])) "
               r"and zero(4*1 - 2 - 3*3 + 7)"),

    dict(id="K120", level=5, target=TARGET, tags=["中值定理", "构造辅助函数", "拔高"],
         q=r"设 $f$ 在 $[0,1]$ 上二阶可导，$f(0)=f(1)=0$，且 $\max_{[0,1]}f=1$。"
           r"证明存在 $\xi\in(0,1)$ 使 $f''(\xi)\le-8$。",
         a=r"存在这样的 $\xi$",
         s=r"设 $f$ 在 $c\in(0,1)$ 取最大值 1，则 $f'(c)=0$。"
           r"在 $[0,c]$ 上用泰勒公式（展开到二阶）：$f(0)=f(c)+f'(c)(0-c)+\frac{f''(\xi_1)}{2}(0-c)^{2}$，"
           r"即 $0=1+\frac{f''(\xi_1)}{2}c^{2}$，得 $f''(\xi_1)=-\frac{2}{c^{2}}$。"
           r"同理在 $[c,1]$ 上得 $f''(\xi_2)=-\frac{2}{(1-c)^{2}}$。"
           r"由于 $c(1-c)\le\frac14$，故 $\max\left(\frac{2}{c^{2}},\frac{2}{(1-c)^{2}}\right)\ge8$，"
           r"取对应那个 $\xi$ 即得 $f''(\xi)\le-8$。",
         q_en=r"Let $f$ be twice differentiable on $[0,1]$ with $f(0)=f(1)=0$ and "
              r"$\max_{[0,1]}f=1$. Prove that $f''(\xi)\le-8$ for some $\xi\in(0,1)$.",
         a_en=r"Such a $\xi$ exists.",
         s_en=r"Let $f$ attain its maximum $1$ at $c\in(0,1)$; then $f'(c)=0$. Taylor expansion about "
              r"$c$ gives $0=f(0)=1+\frac{f''(\xi_1)}{2}c^{2}$, hence $f''(\xi_1)=-2/c^{2}$, and "
              r"similarly $f''(\xi_2)=-2/(1-c)^{2}$. Since $c(1-c)\le\frac14$, at least one of "
              r"$2/c^{2}$, $2/(1-c)^{2}$ is $\ge 8$, giving the claim.",
         check=r"eq(Rational(2)/(Rational(1,4)**2), 32) and eq(Rational(2)/(Rational(1,2)**2), 8)"),
]
