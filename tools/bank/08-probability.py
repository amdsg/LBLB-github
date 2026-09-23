# -*- coding: utf-8 -*-
"""原创题库 · 概率与统计"""
TOPIC = "概率与统计"

PROBLEMS = [
    dict(id="P01", level=1, tags=["古典概型"], q=r"从 52 张扑克牌中任取一张，求取到红桃的概率。",
         a=r"$\dfrac{13}{52}=\dfrac14$",
         s=r"红桃共 13 张，样本空间 52 张等可能，故概率为 $\frac{13}{52}$。",
         check=r"eq(Rational(13,52), Rational(1,4))"),

    dict(id="P02", level=1, tags=["组合数"], q=r"计算 $\binom{5}{2}$。",
         a=r"$10$",
         s=r"$\binom52=\frac{5!}{2!\,3!}=10$。",
         check=r"eq(binomial(5,2), 10)"),

    dict(id="P03", level=2, tags=["排列数"], q=r"计算 $A_5^3=\dfrac{5!}{(5-3)!}$。",
         a=r"$60$",
         s=r"$\frac{5!}{2!}=60$。",
         check=r"eq(factorial(5)/factorial(2), 60)"),

    dict(id="P04", level=2, tags=["二项分布"], q=r"设 $X\sim B\left(5,\frac13\right)$，求 $P(X=2)$。",
         a=r"$\dfrac{80}{243}$",
         s=r"$P(X=2)=\binom52\left(\frac13\right)^{2}\left(\frac23\right)^{3}=10\cdot\frac19\cdot\frac{8}{27}$。",
         check=r"eq(binomial(5,2)*Rational(1,3)**2*Rational(2,3)**3, Rational(80,243))"),

    dict(id="P05", level=1, tags=["数学期望"], q=r"掷一枚均匀骰子，求点数的数学期望。",
         a=r"$\dfrac72=3.5$",
         s=r"$E[X]=\sum_{k=1}^{6}k\cdot\frac16=\frac{21}{6}=\frac72$。",
         check=r"eq(sum(Rational(k,6) for k in range(1,7)), Rational(7,2))"),

    dict(id="P06", level=2, tags=["方差"], q=r"掷一枚均匀骰子，求点数的方差。",
         a=r"$\dfrac{35}{12}$",
         s=r"$E[X^{2}]=\frac{91}{6}$，$\operatorname{Var}=E[X^{2}]-(E[X])^{2}=\frac{91}{6}-\frac{49}{4}=\frac{35}{12}$。",
         check=r"eq(sum(Rational(k*k,6) for k in range(1,7)) - Rational(7,2)**2, Rational(35,12))"),

    dict(id="P07", level=2, tags=["条件概率"], q=r"设 $P(B)=\frac12$、$P(AB)=\frac14$，求 $P(A\mid B)$。",
         a=r"$\dfrac12$",
         s=r"$P(A\mid B)=\frac{P(AB)}{P(B)}=\frac{1/4}{1/2}=\frac12$。",
         check=r"eq(Rational(1,4)/Rational(1,2), Rational(1,2))"),

    dict(id="P08", level=4, tags=["贝叶斯公式"], q=r"某病患病率 $1\%$；患者检测阳性率 $99\%$，非患者误报阳性率 $5\%$。若某人检测为阳性，求其患病的概率。",
         a=r"$\dfrac16\approx16.7\%$",
         s=r"$P(D\mid +)=\frac{0.01\times0.99}{0.01\times0.99+0.99\times0.05}=\frac{0.0099}{0.0594}=\frac16$。"
           r"误报带来的假阳性远多于真阳性，这正是筛查结果需要复检的原因。",
         check=r"eq(Rational(99,10000)/(Rational(99,10000)+Rational(99,100)*Rational(5,100)), Rational(1,6))"),

    dict(id="P09", level=2, tags=["独立性"], q=r"设 $A$、$B$ 相互独立，$P(A)=\frac12$、$P(B)=\frac13$，求 $P(AB)$。",
         a=r"$\dfrac16$",
         s=r"独立时 $P(AB)=P(A)P(B)=\frac12\cdot\frac13$。",
         check=r"eq(Rational(1,2)*Rational(1,3), Rational(1,6))"),

    dict(id="P10", level=3, tags=["超几何分布"], q=r"袋中 5 白 3 黑共 8 球，任取 2 个，求两个都是白球的概率。",
         a=r"$\dfrac{5}{14}$",
         s=r"$\frac{\binom52}{\binom82}=\frac{10}{28}=\frac5{14}$。",
         check=r"eq(binomial(5,2)/binomial(8,2), Rational(5,14))"),

    dict(id="P11", level=2, tags=["期望的线性性"], q=r"掷一枚均匀骰子得 $X$，求 $E[2X+3]$。",
         a=r"$10$",
         s=r"$E[2X+3]=2E[X]+3=2\cdot\frac72+3=10$。",
         check=r"eq(2*Rational(7,2)+3, 10)"),

    dict(id="P12", level=2, tags=["圆排列"], q=r"5 个人围成一圈就座，共有多少种坐法？",
         a=r"$24$",
         s=r"圆排列数为 $(n-1)!$，故为 $4!=24$。",
         check=r"eq(factorial(4), 24)"),

    dict(id="P13", level=2, tags=["二项式定理"], q=r"计算 $\sum_{k=0}^{5}\binom{5}{k}$。",
         a=r"$32$",
         s=r"由二项式定理取 $x=y=1$ 得 $\sum\binom{n}{k}=2^{n}=32$。",
         check=r"eq(sum(binomial(5,k) for k in range(6)), 2**5)"),

    dict(id="P14", level=3, tags=["几何分布"], q=r"每次试验成功概率 $p=\frac14$，求首次成功所需试验次数的期望。",
         a=r"$4$",
         s=r"几何分布期望为 $\frac1p=4$。",
         check=r"eq(1/Rational(1,4), 4)"),

    dict(id="P15", level=2, tags=["方差性质"], q=r"已知 $\operatorname{Var}[X]=\frac{35}{12}$，求 $\operatorname{Var}[3X]$。",
         a=r"$\dfrac{105}{4}$",
         s=r"$\operatorname{Var}[aX]=a^{2}\operatorname{Var}[X]=9\cdot\frac{35}{12}=\frac{105}{4}$。",
         check=r"eq(Rational(9)*Rational(35,12), Rational(105,4))"),

    dict(id="P16", level=3, tags=["全概率公式"], q=r"甲袋取球概率 $\frac13$、乙袋 $\frac23$；甲袋中白球概率 $\frac12$、乙袋 $\frac14$。求任取一球为白球的概率。",
         a=r"$\dfrac13$",
         s=r"全概率公式：$\frac13\cdot\frac12+\frac23\cdot\frac14=\frac16+\frac16=\frac13$。",
         check=r"eq(Rational(1,3)*Rational(1,2) + Rational(2,3)*Rational(1,4), Rational(1,3))"),

    dict(id="P17", level=3, tags=["泊松分布"], q=r"设 $X\sim P(3)$，求 $P(X=2)$。",
         a=r"$\dfrac{9e^{-3}}{2}$",
         s=r"$P(X=k)=\frac{\lambda^{k}e^{-\lambda}}{k!}$，代入 $\lambda=3,k=2$。",
         check=r"eq(exp(-3)*3**2/factorial(2), exp(-3)*Rational(9,2))"),

    dict(id="P18", level=3, tags=["泊松分布", "规范性"], q=r"验证泊松分布的概率和为 1，即 $\sum_{k\ge0}\frac{3^{k}e^{-3}}{k!}=1$。",
         a=r"$1$",
         s=r"由 $e^{3}=\sum_{k\ge0}\frac{3^{k}}{k!}$，乘以 $e^{-3}$ 即得。",
         check=r"eq(Sum(exp(-3)*3**k/factorial(k), (k, 0, oo)).doit(), 1)"),

    dict(id="P19", level=3, tags=["协方差", "相关系数"], q=r"已知 $\operatorname{Var}[X]=4$、$\operatorname{Var}[Y]=9$、$\rho_{XY}=0.5$，求 $\operatorname{Cov}(X,Y)$。",
         a=r"$3$",
         s=r"$\rho=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}$，故 $\operatorname{Cov}=0.5\cdot2\cdot3=3$。",
         check=r"eq(Rational(1,2)*sqrt(4)*sqrt(9), 3)"),

    dict(id="P20", level=3, tags=["中心极限定理"], q=r"总体均值 $10$、标准差 $2$，抽容量 $n=100$ 的样本，求样本均值的标准差。",
         a=r"$0.2$",
         s=r"样本均值标准差为 $\frac{\sigma}{\sqrt n}=\frac{2}{10}=0.2$。",
         check=r"eq(2/sqrt(100), Rational(1,5))"),

    dict(id="P21", level=4, tags=["极大似然估计"], q=r"10 次独立试验中成功 7 次，求成功概率 $p$ 的极大似然估计，并验证似然函数在此取极值。",
         a=r"$\hat p=\dfrac{7}{10}$",
         s=r"对数似然 $\ell(p)=7\ln p+3\ln(1-p)$，$\ell'(p)=\frac{7}{p}-\frac{3}{1-p}=0$ 得 $p=\frac{7}{10}$。",
         check=r"zero(diff(7*log(a) + 3*log(1-a), a).subs(a, Rational(7,10)))"),

    dict(id="P22", level=2, tags=["组合对称性"], q=r"验证 $\binom{7}{3}=\binom{7}{4}$。",
         a=r"相等，均为 $35$",
         s=r"$\binom{n}{k}=\binom{n}{n-k}$，对应「选出 $k$ 个」与「留下 $n-k$ 个」的一一对应。",
         check=r"eq(binomial(7,3), binomial(7,4))"),

    dict(id="P23", level=3, tags=["独立重复试验"], q=r"某事件每次发生概率 $0.1$，独立重复 3 次，求至少发生一次的概率。",
         a=r"$\dfrac{271}{1000}$",
         s=r"$1-(0.9)^{3}=1-0.729$，注意用对立事件计算更方便。",
         check=r"eq(1-Rational(9,10)**3, Rational(271,1000))"),

    dict(id="P24", level=2, tags=["二阶矩"], q=r"掷一枚均匀骰子得 $X$，求 $E[X^{2}]$。",
         a=r"$\dfrac{91}{6}$",
         s=r"$E[X^{2}]=\sum k^{2}\cdot\frac16=\frac{91}{6}\approx15.17$。",
         check=r"eq(sum(Rational(k**2,6) for k in range(1,7)), Rational(91,6))"),

    dict(id="P25", level=4, tags=["生日问题"], q=r"求 23 人中至少两人生日相同的概率（一年按 365 天计）。",
         a=r"$\approx0.5073$",
         s=r"用对立事件：$P(\text{全不同})=\frac{365\cdot364\cdots(365-22)}{365^{23}}$，"
           r"$1$ 减去它约为 $0.5073$，故「23 人即过半」是著名反直觉结论。",
         check=r"approx(1 - factorial(365)/(factorial(365-23)*365**23), 0.507297234323986, tol=1e-12)"),

    dict(id="P26", level=3, tags=["协方差", "独立性"], q=r"设 $X$、$Y$ 独立，$E[X]=E[Y]=\frac12$、$E[XY]=\frac14$，求 $\operatorname{Cov}(X,Y)$。",
         a=r"$0$",
         s=r"$\operatorname{Cov}=E[XY]-E[X]E[Y]=\frac14-\frac14=0$，与独立性一致。",
         check=r"eq(Rational(1,4) - Rational(1,2)*Rational(1,2), 0)"),
]
