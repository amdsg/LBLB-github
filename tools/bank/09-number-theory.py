# -*- coding: utf-8 -*-
"""原创题库 · 数论与组合"""
TOPIC = "数论与组合"

PROBLEMS = [
    dict(id="N01", level=2, tags=["欧拉函数"], q=r"求 $\varphi(12)$。",
         a=r"$4$",
         s=r"与 12 互素且不超过 12 的正整数为 $1,5,7,11$，共 4 个。也可由 $\varphi(12)=12\left(1-\frac12\right)\left(1-\frac13\right)=4$。",
         check=r"eq(totient(12), 4)"),

    dict(id="N02", level=2, tags=["费马小定理"], q=r"求 $2^{10}\bmod 11$。",
         a=r"$1$",
         s=r"11 是素数且 $\gcd(2,11)=1$，由费马小定理 $2^{10}\equiv1\pmod{11}$。",
         check=r"eq(2**10 % 11, 1)"),

    dict(id="N03", level=1, tags=["最大公约数"], q=r"求 $\gcd(48,18)$。",
         a=r"$6$",
         s=r"辗转相除：$48=2\cdot18+12$，$18=1\cdot12+6$，$12=2\cdot6+0$，故 $\gcd=6$。",
         check=r"eq(gcd(48,18), 6)"),

    dict(id="N04", level=3, tags=["中国剩余定理"], q=r"求满足 $x\equiv2\pmod3$、$x\equiv3\pmod5$、$x\equiv2\pmod7$ 的最小正整数 $x$。",
         a=r"$x=23$",
         s=r"满足前两式的最小正解为 8，再每隔 15 取一个；$8,23,38,\dots$ 中满足 $\equiv2\pmod7$ 的最小者是 23。",
         check=r"eq(23 % 3, 2) and eq(23 % 5, 3) and eq(23 % 7, 2)"),

    dict(id="N05", level=4, tags=["组合恒等式"], q=r"验证 $\sum_{k=0}^{4}\binom{4}{k}^{2}=\binom{8}{4}$。",
         a=r"两边都等于 $70$",
         s=r"左边 $=1+16+36+16+1=70$；右边 $\binom84=70$。一般地有范德蒙德恒等式 $\sum\binom{n}{k}^{2}=\binom{2n}{n}$。",
         check=r"eq(sum(binomial(4,k)**2 for k in range(5)), binomial(8,4))"),

    dict(id="N06", level=1, tags=["二项式系数"], q=r"计算 $\binom{10}{3}$。",
         a=r"$120$",
         s=r"$\binom{10}{3}=\frac{10\cdot9\cdot8}{3!}=120$。",
         check=r"eq(binomial(10,3), 120)"),

    dict(id="N07", level=1, tags=["素性判断"], q=r"判断 97 是否为素数。",
         a=r"是素数",
         s=r"$\sqrt{97}<10$，只需用 $2,3,5,7$ 试除：均不能整除，故 97 为素数。",
         check=r"isprime(97)"),

    dict(id="N08", level=2, tags=["辗转相除"], q=r"求 $\gcd(1071,462)$。",
         a=r"$21$",
         s=r"$1071=2\cdot462+147$，$462=3\cdot147+21$，$147=7\cdot21+0$，故 $\gcd=21$。",
         check=r"eq(gcd(1071,462), 21)"),

    dict(id="N09", level=2, tags=["同余方程"], q=r"解同余方程 $3x\equiv1\pmod7$。",
         a=r"$x\equiv5\pmod7$",
         s=r"$3$ 在模 7 下的逆元是 5（因 $3\cdot5=15\equiv1$），故 $x\equiv5$。",
         check=r"eq(3*5 % 7, 1)"),

    dict(id="N10", level=2, tags=["约数个数"], q=r"求 36 的正约数个数。",
         a=r"$9$",
         s=r"$36=2^{2}\cdot3^{2}$，约数个数为 $(2+1)(2+1)=9$。",
         check=r"eq(divisor_count(36), 9)"),

    dict(id="N11", level=2, tags=["二项式恒等式"], q=r"计算 $\sum_{k=0}^{5}(-1)^{k}\binom{5}{k}$。",
         a=r"$0$",
         s=r"由 $(1-1)^{5}=0$ 的二项式展开即得。",
         check=r"eq(sum((-1)**k*binomial(5,k) for k in range(6)), 0)"),

    dict(id="N12", level=3, tags=["欧拉定理"], q=r"验证 $5^{\varphi(12)}\equiv1\pmod{12}$。",
         a=r"$\varphi(12)=4$，$5^{4}=625\equiv1\pmod{12}$",
         s=r"$\gcd(5,12)=1$，由欧拉定理 $5^{\varphi(12)}\equiv1$；直接算 $625=52\cdot12+1$。",
         check=r"eq(5**4 % 12, 1) and eq(totient(12), 4)"),

    dict(id="N13", level=3, tags=["斐波那契", "卡西尼恒等式"], q=r"验证卡西尼恒等式 $F_5^{2}-F_4F_6=(-1)^{6}$（$F_1=F_2=1$）。",
         a=r"$F_4=3,\ F_5=5,\ F_6=8$，$25-24=1=(-1)^{6}$",
         s=r"卡西尼恒等式：$F_{n}^{2}-F_{n-1}F_{n+1}=(-1)^{n+1}$，取 $n=5$ 时右边为 $1$。",
         check=r"eq(5**2 - 3*8, (-1)**(5+1))"),

    dict(id="N14", level=2, tags=["帕斯卡恒等式"], q=r"验证 $\binom{6}{2}=\binom{5}{1}+\binom{5}{2}$。",
         a=r"两边都等于 $15$",
         s=r"帕斯卡恒等式 $\binom{n}{k}=\binom{n-1}{k-1}+\binom{n-1}{k}$，即杨辉三角的递推规律。",
         check=r"eq(binomial(6,2), binomial(5,1)+binomial(5,2))"),

    dict(id="N15", level=3, tags=["组合计数", "排除法"], q=r"从 5 名男生、4 名女生中选 3 人，要求至少有 1 名女生，共有多少种选法？",
         a=r"$74$",
         s=r"用排除法：$\binom93-\binom53=84-10=74$。",
         check=r"eq(binomial(9,3)-binomial(5,3), 74)"),

    dict(id="N16", level=2, tags=["素因数分解"], q=r"分解 $360$ 的素因数，并写出 $360$ 中因子 2 的指数。",
         a=r"$360=2^{3}\cdot3^{2}\cdot5$，2 的指数为 $3$",
         s=r"$360=36\cdot10=2^{2}3^{2}\cdot2\cdot5=2^{3}3^{2}5$。",
         check=r"eq(2**3 * 3**2 * 5, 360) and eq(factorint(360)[2], 3)"),

    dict(id="N17", level=1, tags=["阶乘"], q=r"计算 $5!$。",
         a=r"$120$",
         s=r"$5!=5\cdot4\cdot3\cdot2\cdot1=120$。",
         check=r"eq(factorial(5), 120)"),

    dict(id="N18", level=3, tags=["组合恒等式"], q=r"验证 $\sum_{k=0}^{5}k\binom{5}{k}=5\cdot2^{4}$。",
         a=r"两边都等于 $80$",
         s=r"由 $k\binom{n}{k}=n\binom{n-1}{k-1}$ 得 $\sum k\binom nk=n2^{n-1}=5\cdot16=80$。",
         check=r"eq(sum(k*binomial(5,k) for k in range(6)), 5*2**4)"),

    dict(id="N19", level=2, tags=["同余性质"], q=r"验证 $(7\cdot9)\bmod5=\left((7\bmod5)(9\bmod5)\right)\bmod5$。",
         a=r"两边都等于 $3$",
         s=r"同余式可以相乘：$7\equiv2$、$9\equiv4\pmod5$，$2\cdot4=8\equiv3$；而 $63\equiv3$。",
         check=r"eq(7*9 % 5, (7 % 5)*(9 % 5) % 5)"),

    dict(id="N20", level=3, tags=["容斥原理"], q=r"求 1 到 100 中能被 3 或 5 整除的整数个数。",
         a=r"$47$",
         s=r"容斥：$\lfloor\frac{100}{3}\rfloor+\lfloor\frac{100}{5}\rfloor-\lfloor\frac{100}{15}\rfloor=33+20-6=47$。",
         check=r"eq(33+20-6, 100//3 + 100//5 - 100//15)"),

    dict(id="N21", level=3, tags=["完全数", "约数和"], q=r"求 6 的全体正约数之和，并说明 6 是完全数。",
         a=r"$\sigma(6)=12=2\cdot6$，故 6 是完全数",
         s=r"约数 $1,2,3,6$ 之和为 12，等于 $2\times6$（即真约数之和等于自身）。",
         check=r"eq(divisor_sigma(6), 12)"),

    dict(id="N22", level=2, tags=["二项式定理"], q=r"计算 $\sum_{k=0}^{10}\binom{10}{k}$。",
         a=r"$1024$",
         s=r"$\sum\binom nk=2^{n}=2^{10}=1024$。",
         check=r"eq(sum(binomial(10,k) for k in range(11)), 1024)"),

    dict(id="N23", level=4, tags=["模幂运算", "欧拉定理"], q=r"求 $7^{100}\bmod 13$。",
         a=r"$9$",
         s=r"$\varphi(13)=12$，$100\equiv4\pmod{12}$，故 $7^{100}\equiv7^{4}=2401\equiv9\pmod{13}$（$2401=184\cdot13+9$）。",
         check=r"eq(pow(7,100,13), 9)"),

    dict(id="N24", level=3, tags=["最小公倍数"], q=r"求 $\operatorname{lcm}(12,18)$。",
         a=r"$36$",
         s=r"$12=2^{2}\cdot3$、$18=2\cdot3^{2}$，各素因子取最高次幂得 $2^{2}3^{2}=36$。",
         check=r"eq(lcm(12,18), 36)"),

    dict(id="N25", level=4, tags=["互素", "最大公约数"], q=r"求 $\gcd(2^{10}-1,\ 2^{6}-1)$（提示：$2^{m}-1$ 与 $2^{n}-1$ 的公约数对应 $2^{\gcd(m,n)}-1$）。",
         a=r"$2^{\gcd(10,6)}-1=2^{2}-1=3$",
         s=r"$\gcd(10,6)=2$，故所求为 $2^{2}-1=3$；可直接验证 $1023=3\cdot341$、$63=3\cdot21$，且 $341,21$ 互素。",
         check=r"eq(gcd(2**10 - 1, 2**6 - 1), 2**gcd(10,6) - 1)"),

    dict(id="N26", level=4, tags=["威尔逊定理"], q=r"验证威尔逊定理在 $p=7$ 时成立，即 $6!\equiv-1\pmod7$。",
         a=r"$6!=720=103\cdot7-1\equiv-1\pmod7$",
         s=r"威尔逊定理：$p$ 为素数当且仅当 $(p-1)!\equiv-1\pmod p$。",
         check=r"eq(factorial(6) % 7, 6) and eq((6 % 7), -1 % 7)"),
]
