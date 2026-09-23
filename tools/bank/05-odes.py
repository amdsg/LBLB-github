# -*- coding: utf-8 -*-
"""原创题库 · 常微分方程"""
TOPIC = "常微分方程"

PROBLEMS = [
    dict(id="O01", level=2, tags=["可分离变量"], q=r"求解 $\dfrac{dy}{dx}=2xy$。",
         a=r"$y=Ce^{x^{2}}$",
         s=r"分离变量 $\frac{dy}{y}=2x\,dx$，两端积分得 $\ln|y|=x^{2}+C$。",
         check=r"zero(diff(a*exp(x**2), x) - 2*x*a*exp(x**2))"),

    dict(id="O02", level=1, tags=["可分离变量"], q=r"求解 $\dfrac{dy}{dx}=\dfrac{y}{x}$（$x>0$）。",
         a=r"$y=Cx$",
         s=r"分离变量 $\frac{dy}{y}=\frac{dx}{x}$，积分得 $\ln|y|=\ln x+C$。",
         check=r"zero(diff(a*x, x) - a*x/x)"),

    dict(id="O03", level=3, tags=["一阶线性", "积分因子"], q=r"求解 $y'+y=e^{x}$。",
         a=r"$y=\dfrac{e^{x}}{2}+Ce^{-x}$",
         s=r"积分因子 $e^{x}$，$(ye^{x})'=e^{2x}$，积分得 $ye^{x}=\frac{e^{2x}}{2}+C$。",
         check=r"zero(diff(exp(x)/2 + a*exp(-x), x) + (exp(x)/2 + a*exp(-x)) - exp(x))"),

    dict(id="O04", level=2, tags=["二阶常系数", "相异实根"], q=r"求解 $y''-3y'+2y=0$。",
         a=r"$y=C_1e^{x}+C_2e^{2x}$",
         s=r"特征方程 $r^{2}-3r+2=0$ 得 $r=1,2$，两相异实根。",
         check=r"zero(diff(a*exp(x)+b*exp(2*x), x, 2) - 3*diff(a*exp(x)+b*exp(2*x), x) + 2*(a*exp(x)+b*exp(2*x)))"),

    dict(id="O05", level=3, tags=["二阶常系数", "重根"], q=r"求解 $y''-4y'+4y=0$。",
         a=r"$y=(C_1+C_2x)e^{2x}$",
         s=r"特征方程 $(r-2)^{2}=0$ 有二重根 $r=2$，故通解含因子 $x$。",
         check=r"zero(diff((a+b*x)*exp(2*x), x, 2) - 4*diff((a+b*x)*exp(2*x), x) + 4*(a+b*x)*exp(2*x))"),

    dict(id="O06", level=2, tags=["二阶常系数", "共轭复根"], q=r"求解 $y''+y=0$。",
         a=r"$y=C_1\cos x+C_2\sin x$",
         s=r"特征方程 $r^{2}+1=0$ 得 $r=\pm i$，对应 $\cos x$ 与 $\sin x$。",
         check=r"zero(diff(a*cos(x)+b*sin(x), x, 2) + (a*cos(x)+b*sin(x)))"),

    dict(id="O07", level=2, tags=["可分离变量"], q=r"求解 $\dfrac{dy}{dx}=y^{2}$。",
         a=r"$y=-\dfrac{1}{x+C}$",
         s=r"$\frac{dy}{y^{2}}=dx$，积分得 $-\frac1y=x+C$，即 $y=-\frac{1}{x+C}$（另有常数解 $y\equiv0$）。",
         check=r"zero(diff(-1/(x+a), x) - (-1/(x+a))**2)"),

    dict(id="O08", level=3, tags=["非齐次特解"], q=r"求 $y''+y=2e^{x}$ 的一个特解。",
         a=r"$y^{*}=e^{x}$",
         s=r"试设 $y=Ae^{x}$ 代入得 $Ae^{x}+Ae^{x}=2e^{x}$，故 $A=1$。",
         check=r"zero(diff(exp(x), x, 2) + exp(x) - 2*exp(x))"),

    dict(id="O09", level=3, tags=["齐次方程", "变量代换"], q=r"求解 $\dfrac{dy}{dx}=\dfrac{x+y}{x}$（$x>0$）。",
         a=r"$y=x(\ln x+C)$",
         s=r"令 $y=ux$，则 $u+xu'=1+u$，即 $u'=\frac1x$，积分得 $u=\ln x+C$。",
         check=r"zero(diff(x*(log(x)+a), x) - (x + x*(log(x)+a))/x)"),

    dict(id="O10", level=2, tags=["初值问题"], q=r"求解初值问题 $y'=y$，$y(0)=1$。",
         a=r"$y=e^{x}$",
         s=r"通解 $y=Ce^{x}$，代入 $y(0)=1$ 得 $C=1$。",
         check=r"zero(diff(exp(x), x) - exp(x)) and eq(exp(0), 1)"),

    dict(id="O11", level=3, tags=["一阶线性"], q=r"求解 $y'-y=x$。",
         a=r"$y=Ce^{x}-x-1$",
         s=r"积分因子 $e^{-x}$，$(ye^{-x})'=xe^{-x}$，积分得 $ye^{-x}=-(x+1)e^{-x}+C$。",
         check=r"zero(diff(-x-1+a*exp(x), x) - (-x-1+a*exp(x)) - x)"),

    dict(id="O12", level=3, tags=["全微分方程"], q=r"验证 $x^{2}+xy+y^{2}=C$ 是 $(2x+y)\,dx+(x+2y)\,dy=0$ 的通解。",
         a=r"是。因为 $\dfrac{\partial u}{\partial x}=2x+y,\ \dfrac{\partial u}{\partial y}=x+2y$，其中 $u=x^{2}+xy+y^{2}$",
         s=r"只需验证 $du=(2x+y)dx+(x+2y)dy$，故方程即 $du=0$。",
         check=r"zero(diff(x**2+x*y+y**2, x) - (2*x+y)) and zero(diff(x**2+x*y+y**2, y) - (x+2*y))"),

    dict(id="O13", level=4, tags=["欧拉方程"], q=r"求解欧拉方程 $x^{2}y''+xy'-y=0$（$x>0$）。",
         a=r"$y=C_1x+\dfrac{C_2}{x}$",
         s=r"设 $y=x^{r}$ 代入得 $r(r-1)+r-1=r^{2}-1=0$，故 $r=\pm1$。",
         check=r"zero(x**2*diff(a*x+b/x, x, 2) + x*diff(a*x+b/x, x) - (a*x+b/x))"),

    dict(id="O14", level=3, tags=["降阶"], q=r"求解 $y''=y'$。",
         a=r"$y=C_1e^{x}+C_2$",
         s=r"令 $p=y'$，则 $p'=p$ 得 $p=C_1e^{x}$，再积分一次得 $y=C_1e^{x}+C_2$。",
         check=r"zero(diff(a*exp(x)+b, x, 2) - diff(a*exp(x)+b, x))"),

    dict(id="O15", level=2, tags=["应用", "指数增长"], q=r"人口模型 $\dfrac{dP}{dt}=kP$，$P(0)=P_0$，求 $P(t)$。",
         a=r"$P=P_0e^{kt}$",
         s=r"可分离变量，积分得 $\ln P=kt+\ln P_0$。",
         check=r"zero(diff(a*exp(k*t), t) - k*a*exp(k*t)) and eq(a*exp(k*0), a)"),

    dict(id="O16", level=4, tags=["阻尼振动", "共轭复根"], q=r"求解 $y''+2y'+5y=0$。",
         a=r"$y=e^{-x}\left(C_1\cos 2x+C_2\sin 2x\right)$",
         s=r"特征方程 $r^{2}+2r+5=0$ 得 $r=-1\pm2i$。",
         check=r"zero(diff(exp(-x)*(a*cos(2*x)+b*sin(2*x)), x, 2) + 2*diff(exp(-x)*(a*cos(2*x)+b*sin(2*x)), x) + 5*exp(-x)*(a*cos(2*x)+b*sin(2*x)))"),

    dict(id="O17", level=3, tags=["非齐次特解"], q=r"求 $y''-y=e^{2x}$ 的一个特解。",
         a=r"$y^{*}=\dfrac{e^{2x}}{3}$",
         s=r"设 $y=Ae^{2x}$，代入得 $4A-A=1$，故 $A=\frac13$。",
         check=r"zero(diff(exp(2*x)/3, x, 2) - exp(2*x)/3 - exp(2*x))"),

    dict(id="O18", level=3, tags=["一阶线性", "积分因子"], q=r"求解 $y'+\dfrac{y}{x}=x$（$x>0$）。",
         a=r"$y=\dfrac{x^{2}}{3}+\dfrac{C}{x}$",
         s=r"积分因子 $x$，$(xy)'=x^{2}$，积分得 $xy=\frac{x^{3}}{3}+C$。",
         check=r"zero(diff(x**2/3 + a/x, x) + (x**2/3 + a/x)/x - x)"),

    dict(id="O19", level=3, tags=["全微分方程"], q=r"验证 $u=e^{x}\cos y$ 的全微分给出 $e^{x}\cos y\,dx-e^{x}\sin y\,dy$。",
         a=r"$\dfrac{\partial u}{\partial x}=e^{x}\cos y,\quad \dfrac{\partial u}{\partial y}=-e^{x}\sin y$",
         s=r"分别对 $x$、$y$ 求偏导即得。",
         check=r"zero(diff(exp(x)*cos(y), x) - exp(x)*cos(y)) and zero(diff(exp(x)*cos(y), y) + exp(x)*sin(y))"),

    dict(id="O20", level=3, tags=["二阶常系数", "重根"], q=r"求解 $y''+6y'+9y=0$。",
         a=r"$y=(C_1+C_2x)e^{-3x}$",
         s=r"特征方程 $(r+3)^{2}=0$，二重根 $r=-3$。",
         check=r"zero(diff((a+b*x)*exp(-3*x), x, 2) + 6*diff((a+b*x)*exp(-3*x), x) + 9*(a+b*x)*exp(-3*x))"),

    dict(id="O21", level=4, tags=["积分因子"], q=r"求解 $y\,dx-x\,dy=0$，并说明积分因子 $\dfrac{1}{x^{2}}$ 的作用。",
         a=r"$y=Cx$",
         s=r"乘以 $\frac{1}{x^{2}}$ 后得 $\frac{y\,dx-x\,dy}{x^{2}}=d\!\left(\frac yx\right)=0$，故 $\frac yx=C$。",
         check=r"zero(diff(a*x/x, x))"),

    dict(id="O22", level=4, tags=["共振", "非齐次特解"], q=r"求 $y''+y=\sin x$ 的一个特解。",
         a=r"$y^{*}=-\dfrac{x\cos x}{2}$",
         s=r"右端 $\sin x$ 对应特征根 $\pm i$，发生共振，故试设 $y=x(A\cos x+B\sin x)$，代入得 $A=-\frac12,\ B=0$。",
         check=r"zero(diff(-x*cos(x)/2, x, 2) + (-x*cos(x)/2) - sin(x))"),

    dict(id="O23", level=4, tags=["可分离变量"], q=r"求解 $\dfrac{dy}{dx}=e^{x-y}$。",
         a=r"$y=\ln\left(e^{x}+C\right)$",
         s=r"分离变量 $e^{y}dy=e^{x}dx$，积分得 $e^{y}=e^{x}+C$，取对数。",
         check=r"zero(diff(log(exp(x)+a), x) - exp(x - log(exp(x)+a)))"),

    dict(id="O24", level=3, tags=["一阶线性", "三角"], q=r"求解 $y'+y=\cos x$。",
         a=r"$y=\dfrac{\sin x+\cos x}{2}+Ce^{-x}$",
         s=r"积分因子 $e^{x}$，$(ye^{x})'=e^{x}\cos x$，而 $\int e^{x}\cos x\,dx=\frac{e^{x}(\sin x+\cos x)}{2}$。",
         check=r"zero(diff((sin(x)+cos(x))/2 + a*exp(-x), x) + (sin(x)+cos(x))/2 + a*exp(-x) - cos(x))"),

    dict(id="O25", level=3, tags=["应用", "牛顿冷却"], q=r"冷却定律 $\dfrac{dT}{dt}=-k(T-20)$，$T(0)=100$，求 $T(t)$。",
         a=r"$T=20+80e^{-kt}$",
         s=r"令 $u=T-20$，则 $u'=-ku$，得 $u=Ce^{-kt}$；由 $T(0)=100$ 定 $C=80$。",
         check=r"zero(diff(20+80*exp(-k*t), t) + k*((20+80*exp(-k*t)) - 20)) and eq(20+80*exp(-k*0), 100)"),

    dict(id="O26", level=2, tags=["直接积分"], q=r"求解 $y''=6x$。",
         a=r"$y=x^{3}+C_1x+C_2$",
         s=r"两次积分：$y'=3x^{2}+C_1$，$y=x^{3}+C_1x+C_2$。",
         check=r"zero(diff(x**3 + a*x + b, x, 2) - 6*x)"),
]
