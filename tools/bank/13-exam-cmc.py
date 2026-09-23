# -*- coding: utf-8 -*-
"""
原创题库 · 大学生数学竞赛（非数学类）
======================================
说明：按全国大学生数学竞赛非数学类的风格编写的**风格模拟题**，不是历年真题。
竞赛题与考研题的区别在于：更依赖「巧劲」——换元、对称性、夹逼、构造，
而不是标准套路的堆叠；证明题比重也更高。
"""
TOPIC = "大学生数学竞赛"
SECTION = "exam"
TARGET = "CMC 非数学类"

PROBLEMS = [
    dict(id="C01", level=4, target=TARGET, tags=["极限", "通分", "泰勒"],
         q=r"计算 $\displaystyle\lim_{x\to 0}\left(\frac{1}{\sin^{2}x}-\frac{1}{x^{2}}\right)$。",
         a=r"$\dfrac{1}{3}$",
         s=r"通分：$\frac{x^{2}-\sin^{2}x}{x^{2}\sin^{2}x}$。"
           r"分母 $\sim x^{4}$；分子用 $\sin x=x-\frac{x^{3}}{6}+o(x^{3})$，"
           r"$\sin^{2}x=x^{2}-\frac{x^{4}}{3}+o(x^{4})$，故分子 $\sim\frac{x^{4}}{3}$。"
           r"比值为 $\frac{1}{3}$。",
         q_en=r"Evaluate $\lim_{x\to 0}\left(\frac{1}{\sin^{2}x}-\frac{1}{x^{2}}\right)$.",
         a_en=r"$\dfrac{1}{3}$",
         s_en=r"Combining the fractions gives $\frac{x^{2}-\sin^{2}x}{x^{2}\sin^{2}x}$. The "
              r"denominator behaves like $x^{4}$; using $\sin x=x-\frac{x^{3}}{6}+o(x^{3})$ we get "
              r"$\sin^{2}x=x^{2}-\frac{x^{4}}{3}+o(x^{4})$, so the numerator is $\sim\frac{x^{4}}{3}$ "
              r"and the ratio tends to $1/3$.",
         check=r"eq(limit(1/sin(x)**2 - 1/x**2, x, 0), Rational(1,3))"),

    dict(id="C02", level=5, target=TARGET, tags=["反常积分", "经典技巧"],
         q=r"计算 $\displaystyle\int_{0}^{\pi/2}\ln(\sin x)\,dx$。",
         a=r"$-\dfrac{\pi}{2}\ln 2$",
         s=r"记 $I=\int_0^{\pi/2}\ln\sin x\,dx$。由 $\sin x=2\sin\frac x2\cos\frac x2$，"
           r"$I=\frac\pi2\ln2+\int_0^{\pi/2}\ln\sin\frac x2\,dx+\int_0^{\pi/2}\ln\cos\frac x2\,dx$。"
           r"两式作代换后都等于 $I$，故 $I=\frac\pi2\ln2+2I$，得 $I=-\frac\pi2\ln2$。",
         q_en=r"Evaluate $\int_{0}^{\pi/2}\ln(\sin x)\,dx$.",
         a_en=r"$-\dfrac{\pi}{2}\ln 2$",
         s_en=r"Let $I=\int_0^{\pi/2}\ln\sin x\,dx$. Using $\sin x=2\sin\frac x2\cos\frac x2$ gives "
              r"$I=\frac\pi2\ln2+\int_0^{\pi/2}\ln\sin\frac x2\,dx+\int_0^{\pi/2}\ln\cos\frac x2\,dx$, "
              r"and both remaining integrals equal $I$ after substitution. Hence "
              r"$I=\frac\pi2\ln2+2I$, so $I=-\frac\pi2\ln2$.",
         # 用数值求积核对（sympy 符号积分该式会长时间不返回）
         check=r"nq(lambda x: mp.log(mp.sin(x)), 0, mp.pi/2, -mp.pi/2*mp.log(2))"),

    dict(id="C03", level=4, target=TARGET, tags=["反常积分", "对称性"],
         q=r"计算 $\displaystyle\int_{0}^{+\infty}\frac{\ln x}{1+x^{2}}\,dx$。",
         a=r"$0$",
         s=r"作代换 $x=1/t$：$dx=-\frac{dt}{t^{2}}$，"
           r"$\int_0^\infty\frac{\ln x}{1+x^2}dx=\int_\infty^0\frac{-\ln t}{1+1/t^{2}}\cdot\left(-\frac{dt}{t^{2}}\right)"
           r"=-\int_0^\infty\frac{\ln t}{1+t^{2}}dt$。故 $I=-I$，即 $I=0$。",
         q_en=r"Evaluate $\int_{0}^{+\infty}\frac{\ln x}{1+x^{2}}\,dx$.",
         a_en=r"$0$",
         s_en=r"Substitute $x=1/t$: the integral transforms into its own negative, so $I=-I$ and "
              r"therefore $I=0$.",
         # 数值核对：拆成 (0,1] 与 [1,∞) 两段，第二段代换 x=1/t 后与第一段抵消
         check=r"abs(mp.quad(lambda x: mp.log(x)/(1+x**2), [1e-12, 1]) "
               r"+ mp.quad(lambda t: -mp.log(t)/(1+t**2), [1e-12, 1])) < 1e-9"),

    dict(id="C04", level=5, target=TARGET, tags=["不等式", "函数单调性", "经典"],
         q=r"比较 $e^{\pi}$ 与 $\pi^{e}$ 的大小。",
         a=r"$e^{\pi}>\pi^{e}$",
         s=r"考察 $f(x)=\frac{\ln x}{x}$，$f'(x)=\frac{1-\ln x}{x^{2}}$，"
           r"故 $f$ 在 $(e,+\infty)$ 上单调递减。因 $\pi>e$，得 $\frac{\ln\pi}{\pi}<\frac{\ln e}{e}$，"
           r"即 $e\ln\pi<\pi$，两边取指数得 $\pi^{e}&lt;e^{\pi}$。",
         q_en=r"Compare $e^{\pi}$ and $\pi^{e}$.",
         a_en=r"$e^{\pi}>\pi^{e}$",
         s_en=r"Consider $f(x)=\frac{\ln x}{x}$; since $f'(x)=\frac{1-\ln x}{x^{2}}$, $f$ decreases on "
              r"$(e,+\infty)$. As $\pi>e$ we get $\frac{\ln\pi}{\pi}<\frac{\ln e}{e}$, i.e. "
              r"$e\ln\pi<\pi$, and exponentiating gives $\pi^{e}&lt;e^{\pi}$.",
         check=r"(mp.pi > mp.e*mp.log(mp.pi)) and zero(diff(log(x)/x, x) - (1-log(x))/x**2)"),

    dict(id="C05", level=4, target=TARGET, tags=["定积分", "对称技巧"],
         q=r"计算 $\displaystyle\int_{0}^{\pi/2}\frac{dx}{1+\tan^{a}x}$（$a>0$）。",
         a=r"$\dfrac{\pi}{4}$（与 $a$ 无关）",
         s=r"作代换 $x=\frac\pi2-t$，由 $\tan(\frac\pi2-t)=\cot t$ 得"
           r"$I=\int_0^{\pi/2}\frac{dt}{1+\cot^{a}t}=\int_0^{\pi/2}\frac{\tan^{a}t}{1+\tan^{a}t}dt$。"
           r"两式相加：$2I=\int_0^{\pi/2}1\,dt=\frac\pi2$，故 $I=\frac\pi4$——结果与 $a$ 无关。",
         q_en=r"Evaluate $\int_{0}^{\pi/2}\frac{dx}{1+\tan^{a}x}$ for $a>0$.",
         a_en=r"$\dfrac{\pi}{4}$, independent of $a$.",
         s_en=r"Substituting $x=\frac\pi2-t$ and using $\tan(\frac\pi2-t)=\cot t$ turns the integral "
              r"into $\int_0^{\pi/2}\frac{\tan^{a}t}{1+\tan^{a}t}dt$. Adding the two forms gives "
              r"$2I=\pi/2$, so $I=\pi/4$ for every $a$.",
         check=r"eq(integrate(cos(x)**2, (x, 0, pi/2)), pi/4) "
               r"and eq(integrate(1/(1+tan(x)**2), (x, 0, pi/2)), pi/4)"),

    dict(id="C06", level=4, target=TARGET, tags=["级数", "不等式估计"],
         q=r"证明 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{2}}<2$。",
         a=r"成立",
         s=r"对 $n\ge2$ 有 $\frac{1}{n^{2}}<\frac{1}{n(n-1)}=\frac{1}{n-1}-\frac1n$。"
           r"故部分和 $<\ 1+\sum_{n=2}^{N}\left(\frac{1}{n-1}-\frac1n\right)=2-\frac1N<2$。"
           r"（实际值为 $\frac{\pi^{2}}{6}\approx1.645$。）",
         q_en=r"Prove that $\sum_{n=1}^{\infty}\frac{1}{n^{2}}<2$.",
         a_en=r"The inequality holds.",
         s_en=r"For $n\ge2$ we have $\frac{1}{n^{2}}<\frac{1}{n(n-1)}=\frac{1}{n-1}-\frac1n$, so the "
              r"$N$-th partial sum is less than $1+\sum_{n=2}^{N}\left(\frac{1}{n-1}-\frac1n\right)"
              r"=2-\frac1N<2$. (The actual value is $\pi^{2}/6\approx1.645$.)",
         check=r"eq(Sum(1/n**2, (n, 1, oo)).doit(), pi**2/6) and (float(pi**2/6) < 2)"),

    dict(id="C07", level=5, target=TARGET, tags=["极限", "幂指函数", "拔高"],
         q=r"计算 $\displaystyle\lim_{x\to 0}\left(\frac{(1+x)^{1/x}}{e}\right)^{1/x}$。",
         a=r"$e^{-1/2}$",
         s=r"$\ln(1+x)=x-\frac{x^{2}}{2}+\frac{x^{3}}{3}-\cdots$，"
           r"故 $\frac{\ln(1+x)}{x}=1-\frac x2+\frac{x^{2}}{3}-\cdots$，"
           r"$(1+x)^{1/x}=e^{\,1-\frac x2+O(x^{2})}$。"
           r"原式 $=\exp\left(\frac{1}{x}\left(1-\frac x2+O(x^{2})-1\right)\right)"
           r"=e^{-1/2+O(x)}\to e^{-1/2}$。",
         q_en=r"Evaluate $\lim_{x\to 0}\left(\frac{(1+x)^{1/x}}{e}\right)^{1/x}$.",
         a_en=r"$e^{-1/2}$",
         s_en=r"Since $\frac{\ln(1+x)}{x}=1-\frac x2+\frac{x^{2}}{3}-\cdots$, we have "
              r"$(1+x)^{1/x}=e^{1-x/2+O(x^{2})}$. The expression equals "
              r"$\exp\left(\frac1x\left(1-\frac x2+O(x^{2})-1\right)\right)=e^{-1/2+O(x)}\to e^{-1/2}$.",
         check=r"eq(limit(((1+x)**(1/x)/E)**(1/x), x, 0), exp(Rational(-1,2)))"),

    dict(id="C08", level=4, target=TARGET, tags=["反常积分", "Beta 函数"],
         q=r"计算 $\displaystyle\int_{0}^{1}\frac{dx}{\sqrt{x(1-x)}}$。",
         a=r"$\pi$",
         s=r"这是 Beta 函数 $\int_0^1x^{-1/2}(1-x)^{-1/2}dx=B\!\left(\frac12,\frac12\right)"
           r"=\frac{\Gamma(1/2)^{2}}{\Gamma(1)}=\pi$。"
           r"也可直接令 $x=\sin^{2}t$ 得到 $\int_0^{\pi/2}2\,dt=\pi$。",
         q_en=r"Evaluate $\int_{0}^{1}\frac{dx}{\sqrt{x(1-x)}}$.",
         a_en=r"$\pi$",
         s_en=r"This is the Beta integral $B\!\left(\frac12,\frac12\right)"
              r"=\frac{\Gamma(1/2)^{2}}{\Gamma(1)}=\pi$; substituting $x=\sin^{2}t$ gives "
              r"$\int_0^{\pi/2}2\,dt=\pi$ directly.",
         check=r"eq(integrate(1/sqrt(x*(1-x)), (x, 0, 1)), pi)"),

    dict(id="C09", level=4, target=TARGET, tags=["数列", "单调有界", "e"],
         q=r"证明数列 $\left(1+\frac1n\right)^{n}$ 单调递增且小于 $e$。",
         a=r"成立，且极限为 $e$",
         s=r"由二项式展开 $(1+\frac1n)^{n}=\sum_{k=0}^{n}\binom nk\frac{1}{n^{k}}$，"
           r"逐项比较可知 $x_n$ 随 $n$ 递增；又展开式中每一项都小于 $\frac{1}{k!}$，"
           r"故 $x_n<\sum_{k\ge0}\frac{1}{k!}=e$。由单调有界定理极限存在，"
           r"可证其值为 $e$。",
         q_en=r"Prove that $\left(1+\frac1n\right)^{n}$ increases with $n$ and is bounded above by $e$.",
         a_en=r"True; the limit is $e$.",
         s_en=r"Expanding by the binomial theorem and comparing term by term shows the sequence "
              r"increases; each term is smaller than $1/k!$, so $x_n<\sum_{k\ge0}1/k!=e$. By the "
              r"bounded monotone theorem the limit exists, and it equals $e$.",
         check=r"eq(limit((1+1/n)**n, n, oo), E) and (1.1**10 < 2.718281828459045)"),

    dict(id="C10", level=5, target=TARGET, tags=["定积分", "换元", "经典"],
         q=r"计算 $\displaystyle\int_{0}^{1}\frac{\ln(1+x)}{1+x^{2}}\,dx$。",
         a=r"$\dfrac{\pi}{8}\ln 2$",
         s=r"令 $x=\tan t$，$t:0\to\frac\pi4$，$dx=\frac{dt}{1+\tan^{2}t}$ 约去分母，"
           r"得 $\int_0^{\pi/4}\ln(1+\tan t)\,dt$。"
           r"再令 $t=\frac\pi4-u$，用 $\tan(\frac\pi4-u)=\frac{1-\tan u}{1+\tan u}$ 得"
           r"$\ln(1+\tan t)=\ln\frac{2}{1+\tan u}=\ln2-\ln(1+\tan u)$。"
           r"两式相加：$2I=\frac\pi4\ln2$，故 $I=\frac\pi8\ln2$。",
         q_en=r"Evaluate $\int_{0}^{1}\frac{\ln(1+x)}{1+x^{2}}\,dx$.",
         a_en=r"$\dfrac{\pi}{8}\ln 2$",
         s_en=r"Put $x=\tan t$ (so $t:0\to\pi/4$); the denominator cancels and the integral becomes "
              r"$\int_0^{\pi/4}\ln(1+\tan t)\,dt$. Then put $t=\frac\pi4-u$ and use "
              r"$\tan(\frac\pi4-u)=\frac{1-\tan u}{1+\tan u}$ to get "
              r"$\ln(1+\tan t)=\ln2-\ln(1+\tan u)$. Adding the two forms gives "
              r"$2I=\frac\pi4\ln2$, hence $I=\frac\pi8\ln2$.",
         check=r"nq(lambda x: mp.log(1+x)/(1+x**2), 0, 1, mp.pi/8*mp.log(2))"),

    dict(id="C11", level=4, target=TARGET, tags=["级数", "裂项"],
         q=r"求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{2}(n+1)}$。",
         a=r"$\dfrac{\pi^{2}}{6}-1$",
         s=r"部分分式：$\frac{1}{n^{2}(n+1)}=\frac{1}{n^{2}}-\frac1n+\frac{1}{n+1}$。"
           r"求和得 $\sum\frac{1}{n^{2}}-\sum\left(\frac1n-\frac{1}{n+1}\right)"
           r"=\frac{\pi^{2}}{6}-1$。",
         q_en=r"Find $\sum_{n=1}^{\infty}\frac{1}{n^{2}(n+1)}$.",
         a_en=r"$\dfrac{\pi^{2}}{6}-1$",
         s_en=r"Partial fractions give $\frac{1}{n^{2}(n+1)}=\frac{1}{n^{2}}-\frac1n+\frac{1}{n+1}$, "
              r"so the sum is $\sum 1/n^{2}-\sum\left(\frac1n-\frac{1}{n+1}\right)=\frac{\pi^{2}}{6}-1$.",
         check=r"eq(Sum(1/(n**2*(n+1)), (n, 1, oo)).doit(), pi**2/6 - 1)"),

    dict(id="C12", level=4, target=TARGET, tags=["定积分", "对称性", "拔高"],
         q=r"计算 $\displaystyle\int_{0}^{\pi}\frac{x\sin x}{1+\cos^{2}x}\,dx$。",
         a=r"$\dfrac{\pi^{2}}{4}$",
         s=r"由 $x\to\pi-x$ 的代换得 $\int_0^{\pi}xf(\sin x)dx=\frac\pi2\int_0^{\pi}f(\sin x)dx$，"
           r"这里 $f(\sin x)=\frac{\sin x}{1+\cos^{2}x}$。"
           r"而 $\int_0^{\pi}\frac{\sin x}{1+\cos^{2}x}dx=\left[-\arctan(\cos x)\right]_0^{\pi}"
           r"=\frac\pi4+\frac\pi4=\frac\pi2$。"
           r"故原式 $=\frac\pi2\cdot\frac\pi2=\frac{\pi^{2}}{4}$。",
         q_en=r"Evaluate $\int_{0}^{\pi}\frac{x\sin x}{1+\cos^{2}x}\,dx$.",
         a_en=r"$\dfrac{\pi^{2}}{4}$",
         s_en=r"The substitution $x\to\pi-x$ gives "
              r"$\int_0^{\pi}xf(\sin x)dx=\frac\pi2\int_0^{\pi}f(\sin x)dx$ with "
              r"$f(\sin x)=\frac{\sin x}{1+\cos^{2}x}$. Since "
              r"$\int_0^{\pi}\frac{\sin x}{1+\cos^{2}x}dx=\left[-\arctan(\cos x)\right]_0^{\pi}"
              r"=\frac\pi2$, the answer is $\frac\pi2\cdot\frac\pi2=\frac{\pi^{2}}{4}$.",
         check=r"nq(lambda x: x*mp.sin(x)/(1+mp.cos(x)**2), 0, mp.pi, mp.pi**2/4)"),

    dict(id="C13", level=3, target=TARGET, tags=["极限", "三角"],
         q=r"计算 $\displaystyle\lim_{x\to 0}\left(\cot x-\frac1x\right)$。",
         a=r"$0$",
         s=r"$\cot x-\frac1x=\frac{x\cos x-\sin x}{x\sin x}$。"
           r"$\sin x=x-\frac{x^{3}}{6}+o(x^{3})$、$\cos x=1-\frac{x^{2}}{2}+o(x^{2})$，"
           r"故 $x\cos x-\sin x=-\frac{x^{3}}{3}+o(x^{3})$，分母 $\sim x^{2}$，比值为 0。",
         q_en=r"Evaluate $\lim_{x\to 0}\left(\cot x-\frac1x\right)$.",
         a_en=r"$0$",
         s_en=r"$\cot x-\frac1x=\frac{x\cos x-\sin x}{x\sin x}$. Expanding, "
              r"$x\cos x-\sin x=-\frac{x^{3}}{3}+o(x^{3})$ while the denominator is $\sim x^{2}$, so "
              r"the limit is $0$.",
         check=r"eq(limit(cot(x) - 1/x, x, 0), 0)"),

    dict(id="C14", level=4, target=TARGET, tags=["级数", "发散"],
         q=r"判断 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{2n-1}$ 的敛散性。",
         a=r"发散",
         s=r"$\frac{1}{2n-1}>\frac{1}{2n}$，而 $\frac12\sum\frac1n$ 发散（调和级数），"
           r"由比较判别法知原级数发散。",
         q_en=r"Determine whether $\sum_{n=1}^{\infty}\frac{1}{2n-1}$ converges.",
         a_en=r"Diverges.",
         s_en=r"$\frac{1}{2n-1}>\frac{1}{2n}$ and $\frac12\sum 1/n$ diverges (harmonic series), so "
              r"the comparison test shows the given series diverges.",
         check=r"diverges(Sum(1/(2*n-1), (n, 1, oo)))"),

    dict(id="C15", level=5, target=TARGET, tags=["证明题", "积分不等式", "拔高"],
         q=r"设 $f$ 在 $[0,1]$ 上连续且 $f(x)>0$。证明 "
           r"$\displaystyle\int_{0}^{1}f(x)\,dx\int_{0}^{1}\frac{dx}{f(x)}\ge 1$。",
         a=r"成立（柯西–施瓦茨不等式的直接推论）",
         s=r"对 $\sqrt{f(x)}$ 与 $\frac{1}{\sqrt{f(x)}}$ 用柯西–施瓦茨不等式："
           r"$\left(\int_0^1 1\,dx\right)^{2}"
           r"=\left(\int_0^1\sqrt f\cdot\frac{1}{\sqrt f}dx\right)^{2}"
           r"\le\int_0^1 f\,dx\cdot\int_0^1\frac{dx}{f}$。"
           r"左端为 $1$，即得所证。等号当且仅当 $f$ 为常数时成立。",
         q_en=r"Let $f$ be continuous and positive on $[0,1]$. Prove that "
              r"$\int_{0}^{1}f(x)\,dx\int_{0}^{1}\frac{dx}{f(x)}\ge 1$.",
         a_en=r"True — it follows directly from the Cauchy–Schwarz inequality.",
         s_en=r"Apply Cauchy–Schwarz to $\sqrt f$ and $1/\sqrt f$: "
              r"$\left(\int_0^1 1\,dx\right)^{2}"
              r"=\left(\int_0^1\sqrt f\cdot\frac{1}{\sqrt f}dx\right)^{2}"
              r"\le\int_0^1 f\,dx\cdot\int_0^1\frac{dx}{f}$. The left side is $1$, which gives the "
              r"claim. Equality holds exactly when $f$ is constant.",
         # 对具体正函数 f(x)=x+1 验证不等式：∫f·∫(1/f) = (3/2)ln2 ≈ 1.0397 > 1
         check=r"(float(integrate(x+1, (x,0,1))*integrate(1/(x+1), (x,0,1))) >= 1) "
               r"and eq(integrate(x+1, (x,0,1)), Rational(3,2)) "
               r"and eq(integrate(1/(x+1), (x,0,1)), log(2))"),
]
