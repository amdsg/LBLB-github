# -*- coding: utf-8 -*-
"""原创题库 · 多元微积分"""
TOPIC = "多元微积分"

PROBLEMS = [
    dict(id="M01", level=2, tags=["偏导数"], q=r"设 $z=x^{2}y+xy^{2}$，求 $\dfrac{\partial z}{\partial x}$。",
         a=r"$2xy+y^{2}$",
         s=r"对 $x$ 求偏导时把 $y$ 视为常数：$z_x=2xy+y^{2}$。",
         check=r"eq(diff(x**2*y + x*y**2, x), 2*x*y + y**2)"),

    dict(id="M02", level=3, tags=["混合偏导"], q=r"设 $z=e^{xy}$，求 $\dfrac{\partial^{2}z}{\partial x\partial y}$。",
         a=r"$e^{xy}(1+xy)$",
         s=r"先对 $x$ 求偏导得 $ye^{xy}$，再对 $y$ 求导得 $e^{xy}+xy\,e^{xy}$。",
         check=r"eq(diff(exp(x*y), x, y), exp(x*y)*(1+x*y))"),

    dict(id="M03", level=2, tags=["全微分"], q=r"求 $z=x^{2}+y^{2}$ 的全微分。",
         a=r"$dz=2x\,dx+2y\,dy$",
         s=r"$dz=z_x\,dx+z_y\,dy$。",
         check=r"eq(diff(x**2+y**2, x), 2*x) and eq(diff(x**2+y**2, y), 2*y)"),

    dict(id="M04", level=4, tags=["隐函数求偏导"], q=r"设 $x^{2}+y^{2}+z^{2}=1$，求 $\dfrac{\partial z}{\partial x}$。",
         a=r"$-\dfrac{x}{z}$",
         s=r"由 $F=x^{2}+y^{2}+z^{2}-1$，$\frac{\partial z}{\partial x}=-\frac{F_x}{F_z}=-\frac{2x}{2z}$。",
         check=r"zero(2*x + 2*z*(-x/z))"),

    dict(id="M05", level=2, tags=["二重积分"], q=r"计算 $\displaystyle\iint_{D}(x+y)\,dx\,dy$，其中 $D=[0,1]\times[0,1]$。",
         a=r"$1$",
         s=r"$\int_{0}^{1}\!\!\int_{0}^{1}(x+y)\,dx\,dy=\int_{0}^{1}\left(\frac12+y\right)dy=\frac12+\frac12=1$。",
         check=r"eq(integrate(x+y, (x, 0, 1), (y, 0, 1)), 1)"),

    dict(id="M06", level=3, tags=["二重积分", "对称性"], q=r"计算 $\displaystyle\iint_{D}xy\,dx\,dy$，其中 $D$ 为单位圆盘 $x^{2}+y^{2}\le1$。",
         a=r"$0$",
         s=r"用极坐标：$\int_{0}^{2\pi}\!\!\int_{0}^{1}r^{3}\cos\theta\sin\theta\,dr\,d\theta$，对 $\theta$ 的积分为 0（奇函数）。",
         check=r"eq(integrate(r**3*cos(t)*sin(t), (r, 0, 1), (t, 0, 2*pi)), 0)"),

    dict(id="M07", level=4, tags=["广义二重积分"], q=r"计算 $\displaystyle\iint_{x>0,\,y>0}e^{-(x^{2}+y^{2})}\,dx\,dy$。",
         a=r"$\dfrac{\pi}{4}$",
         s=r"化为极坐标 $\int_{0}^{\pi/2}\!\!\int_{0}^{\infty}e^{-r^{2}}r\,dr\,d\theta=\frac{\pi}{2}\cdot\frac12$。",
         check=r"eq(integrate(exp(-(x**2+y**2)), (x, 0, oo), (y, 0, oo)), pi/4)"),

    dict(id="M08", level=4, tags=["三重积分", "球坐标"], q=r"用球坐标计算单位球 $x^{2}+y^{2}+z^{2}\le1$ 的体积。",
         a=r"$\dfrac{4\pi}{3}$",
         s=r"$V=\int_{0}^{2\pi}\!\!\int_{0}^{\pi}\!\!\int_{0}^{1}r^{2}\sin\varphi\,dr\,d\varphi\,d\theta=\frac{4\pi}{3}$。",
         check=r"eq(integrate(r**2*sin(t), (r, 0, 1), (t, 0, pi), (u, 0, 2*pi)), 4*pi/3)"),

    dict(id="M09", level=2, tags=["梯度"], q=r"求 $f=x^{2}+y^{2}+z^{2}$ 在点 $(1,1,1)$ 处的梯度。",
         a=r"$\nabla f=(2,2,2)$",
         s=r"$\nabla f=(2x,2y,2z)$，代入 $(1,1,1)$。",
         check=r"all(eq(diff(x**2+y**2+z**2, s).subs({x: 1, y: 1, z: 1}), 2) for s in (x, y, z))"),

    dict(id="M10", level=4, tags=["方向导数"], q=r"求 $f=x^{2}+y^{2}$ 在点 $(1,1)$ 沿方向 $\left(\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right)$ 的方向导数。",
         a=r"$2\sqrt2$",
         s=r"$\nabla f(1,1)=(2,2)$，方向导数 $=(2,2)\cdot\left(\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right)=\frac{4}{\sqrt2}=2\sqrt2$。",
         check=r"eq(Rational(4)/sqrt(2), 2*sqrt(2))"),

    dict(id="M11", level=3, tags=["无条件极值"], q=r"求 $f=x^{2}+y^{2}-2x-4y+5$ 的极小值点与极小值。",
         a=r"极小值点 $(1,2)$，极小值 $0$",
         s=r"令 $f_x=2x-2=0$、$f_y=2y-4=0$ 得 $(1,2)$；$f_{xx}=2>0$ 且 $f_{xx}f_{yy}-f_{xy}^{2}=4>0$，故为极小。",
         check=r"zero(diff(x**2+y**2-2*x-4*y+5, x).subs({x: 1, y: 2})) and zero(diff(x**2+y**2-2*x-4*y+5, y).subs({x: 1, y: 2})) and eq((x**2+y**2-2*x-4*y+5).subs({x: 1, y: 2}), 0)"),

    dict(id="M12", level=4, tags=["条件极值", "拉格朗日乘数"], q=r"在约束 $x+y=1$ 下求 $x^{2}+y^{2}$ 的最小值。",
         a=r"最小值 $\dfrac12$，在 $\left(\frac12,\frac12\right)$ 处取得",
         s=r"拉格朗日函数 $L=x^{2}+y^{2}+\lambda(x+y-1)$，令 $L_x=2x+\lambda=0$、$L_y=2y+\lambda=0$ 得 $x=y=\frac12$。",
         check=r"eq((x**2+y**2).subs({x: Rational(1,2), y: Rational(1,2)}), Rational(1,2)) and zero(diff(x**2+y**2, x).subs(x, Rational(1,2)) - diff(x**2+y**2, y).subs(y, Rational(1,2)))"),

    dict(id="M13", level=4, tags=["格林公式"], q=r"用格林公式计算 $\displaystyle\oint_{L}x\,dy-y\,dx$，$L$ 为单位圆周逆时针方向。",
         a=r"$2\pi$",
         s=r"$\oint x\,dy-y\,dx=\iint_{D}\left(\frac{\partial x}{\partial x}-\frac{\partial(-y)}{\partial y}\right)dA=\iint_{D}2\,dA=2\pi$。",
         check=r"eq(integrate(2, (y, -sqrt(1-x**2), sqrt(1-x**2)), (x, -1, 1)), 2*pi)"),

    dict(id="M14", level=2, tags=["散度"], q=r"求向量场 $\mathbf F=(x,y,z)$ 的散度。",
         a=r"$\nabla\cdot\mathbf F=3$",
         s=r"$\operatorname{div}\mathbf F=\frac{\partial x}{\partial x}+\frac{\partial y}{\partial y}+\frac{\partial z}{\partial z}=3$。",
         check=r"eq(diff(x, x) + diff(y, y) + diff(z, z), 3)"),

    dict(id="M15", level=3, tags=["旋度"], q=r"求向量场 $\mathbf F=(-y,\ x,\ 0)$ 的旋度。",
         a=r"$(0,0,2)$",
         s=r"旋度的 $z$ 分量 $=\frac{\partial F_y}{\partial x}-\frac{\partial F_x}{\partial y}=1-(-1)=2$，另外两个分量均为 0。",
         check=r"eq(diff(x, x) - diff(-y, y), 2)"),

    dict(id="M16", level=3, tags=["链式法则"], q=r"设 $z=(x+y)^{2}+(x-y)^{2}$，求 $\dfrac{\partial z}{\partial x}$。",
         a=r"$4x$",
         s=r"$z=2x^{2}+2y^{2}$，故 $z_x=4x$。也可用链式法则逐项求导。",
         check=r"eq(diff((x+y)**2+(x-y)**2, x), 4*x)"),

    dict(id="M17", level=4, tags=["交换积分次序"], q=r"计算 $\displaystyle\int_{0}^{1}\!\!\int_{x}^{1}e^{y^{2}}\,dy\,dx$。",
         a=r"$\dfrac{e-1}{2}$",
         s=r"交换次序得 $\int_{0}^{1}\!\!\int_{0}^{y}e^{y^{2}}dx\,dy=\int_{0}^{1}ye^{y^{2}}dy=\frac{e-1}{2}$。",
         check=r"eq(integrate(y*exp(y**2), (y, 0, 1)), (E-1)/2)"),

    dict(id="M18", level=4, tags=["体积", "极坐标"], q=r"求曲面 $z=1-x^{2}-y^{2}$ 与平面 $z=0$ 所围立体的体积。",
         a=r"$\dfrac{\pi}{2}$",
         s=r"$V=\iint_{x^{2}+y^{2}\le1}(1-x^{2}-y^{2})dA=\int_{0}^{2\pi}\!\!\int_{0}^{1}(1-r^{2})r\,dr\,d\theta=\frac{\pi}{2}$。",
         check=r"eq(integrate((1-r**2)*r, (r, 0, 1), (t, 0, 2*pi)), pi/2)"),

    dict(id="M19", level=2, tags=["混合偏导", "可交换"], q=r"验证 $z=x^{3}y^{2}-xy^{3}$ 的二阶混合偏导相等。",
         a=r"$z_{xy}=z_{yx}=6x^{2}y-3y^{2}$",
         s=r"$z_x=3x^{2}y^{2}-y^{3}$，$z_y=2x^{3}y-3xy^{2}$；再各求一次偏导，两者相同。",
         check=r"eq(diff(x**3*y**2 - x*y**3, x, y), diff(x**3*y**2 - x*y**3, y, x))"),

    dict(id="M20", level=4, tags=["全微分近似"], q=r"用全微分近似计算 $\sqrt{1.02^{2}+1.97^{2}}$（保留到 $10^{-3}$）。",
         a=r"$\approx\dfrac{4.96}{\sqrt5}\approx2.2182$",
         s=r"取 $f=\sqrt{x^{2}+y^{2}}$，基点 $(1,2)$、$f=\sqrt5$；$df=\frac{x\,dx+y\,dy}{f}=\frac{0.02-0.06}{\sqrt5}=-\frac{0.04}{\sqrt5}$。",
         check=r"approx(sqrt(5) - Rational(4,100)/sqrt(5), sqrt(Rational(102,100)**2 + Rational(197,100)**2), tol=1e-3)"),

    dict(id="M21", level=3, tags=["二重积分", "极坐标"], q=r"计算 $\displaystyle\iint_{D}(x^{2}+y^{2})\,dx\,dy$，$D$ 为单位圆盘。",
         a=r"$\dfrac{\pi}{2}$",
         s=r"$=\int_{0}^{2\pi}\!\!\int_{0}^{1}r^{2}\cdot r\,dr\,d\theta=2\pi\cdot\frac14=\frac{\pi}{2}$。",
         check=r"eq(integrate(r**2*r, (r, 0, 1), (t, 0, 2*pi)), pi/2)"),

    dict(id="M22", level=3, tags=["偏导数", "复合"], q=r"设 $z=f(u,v)$ 且 $u=x+y$、$v=x-y$（$f$ 可微），写出 $\dfrac{\partial z}{\partial x}$。",
         a=r"$\dfrac{\partial z}{\partial x}=f_u+f_v$",
         s=r"链式法则：$z_x=f_u\cdot u_x+f_v\cdot v_x=f_u\cdot1+f_v\cdot1$。",
         check=r"eq(diff((x+y)**2+(x-y)**2, x), 2*(x+y) + 2*(x-y)) and eq(2*(x+y)+2*(x-y), 4*x)"),

    dict(id="M23", level=4, tags=["高斯公式"], q=r"用高斯公式计算 $\displaystyle\oiint_{S}\mathbf F\cdot d\mathbf S$，其中 $\mathbf F=(x,y,z)$、$S$ 为单位球面。",
         a=r"$4\pi$",
         s=r"由 $\nabla\cdot\mathbf F=3$ 及高斯公式，积分等于 $3\times$（单位球体积）$=3\cdot\frac{4\pi}{3}=4\pi$。",
         check=r"eq(3*integrate(r**2*sin(t), (r, 0, 1), (t, 0, pi), (u, 0, 2*pi)), 4*pi)"),

    dict(id="M24", level=4, tags=["极值", "判别式"], q=r"判断 $f=x^{2}-y^{2}$ 在 $(0,0)$ 处是否有极值。",
         a=r"没有极值，$(0,0)$ 是鞍点",
         s=r"$f_x=2x$、$f_y=-2y$ 在原点为 0；但 $f_{xx}f_{yy}-f_{xy}^{2}=2\cdot(-2)-0=-4<0$，为鞍点。",
         check=r"eq(2*(-2) - 0, -4) and eq(diff(x**2-y**2, x).subs({x: 0, y: 0}), 0)"),

    dict(id="M25", level=3, tags=["曲线积分", "路径无关"], q=r"验证 $\displaystyle\int(x+2y)\,dx+(2x+y)\,dy$ 与路径无关，并说明理由。",
         a=r"与路径无关，因为 $\dfrac{\partial P}{\partial y}=2=\dfrac{\partial Q}{\partial x}$ 且全平面单连通",
         s=r"$P=x+2y$、$Q=2x+y$，$P_y=2=Q_x$，满足路径无关条件。",
         check=r"eq(diff(x+2*y, y), diff(2*x+y, x))"),

    dict(id="M26", level=4, tags=["含参积分", "莱布尼茨公式"], q=r"计算 $\displaystyle\int_{0}^{1}\frac{x^{b}-x^{a}}{\ln x}\,dx$（$a,b>0$）。",
         a=r"$\ln\dfrac{1+b}{1+a}$",
         s=r"注意 $\frac{x^{b}-x^{a}}{\ln x}=\int_{a}^{b}x^{t}\,dt$。交换积分次序："
           r"$\int_{a}^{b}\!\!\int_{0}^{1}x^{t}\,dx\,dt=\int_{a}^{b}\frac{dt}{1+t}=\ln\frac{1+b}{1+a}$。"
           r"结果为正，与 $0&lt;x<1$ 时被积函数恒正一致。",
         check=r"eq(integrate((x**b-x**a)/log(x), (x, 0, 1)), log((1+b)/(1+a)))"),
]
