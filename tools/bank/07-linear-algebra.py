# -*- coding: utf-8 -*-
"""原创题库 · 线性代数"""
TOPIC = "线性代数"

PROBLEMS = [
    dict(id="A01", level=1, tags=["行列式"], q=r"计算 $\begin{vmatrix}1&2\\3&4\end{vmatrix}$。",
         a=r"$-2$",
         s=r"$1\cdot4-2\cdot3=4-6=-2$。",
         check=r"eq(det(Matrix([[1,2],[3,4]])), -2)"),

    dict(id="A02", level=2, tags=["行列式"], q=r"计算 $\begin{vmatrix}1&2&3\\4&5&6\\7&8&10\end{vmatrix}$。",
         a=r"$-3$",
         s=r"按第一行展开：$1(50-48)-2(40-42)+3(32-35)=2+4-9=-3$。",
         check=r"eq(det(Matrix([[1,2,3],[4,5,6],[7,8,10]])), -3)"),

    dict(id="A03", level=1, tags=["特征值"], q=r"求 $\begin{pmatrix}2&0\\0&3\end{pmatrix}$ 的特征值。",
         a=r"$\lambda_1=2,\ \lambda_2=3$",
         s=r"对角矩阵的特征值就是对角元。也可由 $\lambda^{2}-5\lambda+6=0$ 解得。",
         check=r"all(any(eq(v, k) for k in (2, 3)) for v in Matrix([[2,0],[0,3]]).eigenvals().keys())"),

    dict(id="A04", level=2, tags=["特征值"], q=r"求 $\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值。",
         a=r"$\lambda_1=3,\ \lambda_2=-1$",
         s=r"$|\lambda I-A|=(\lambda-1)^{2}-4=0$，得 $\lambda=1\pm2$。",
         check=r"all(any(eq(v, k) for k in (3, -1)) for v in Matrix([[1,2],[2,1]]).eigenvals().keys())"),

    dict(id="A05", level=2, tags=["矩阵乘法"], q=r"计算 $\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix}$。",
         a=r"$\begin{pmatrix}2&1\\4&3\end{pmatrix}$",
         s=r"右乘交换矩阵相当于交换两列，故结果是把原矩阵两列对调。",
         check=r"Matrix([[1,2],[3,4]])*Matrix([[0,1],[1,0]]) == Matrix([[2,1],[4,3]])"),

    dict(id="A06", level=3, tags=["逆矩阵"], q=r"求 $\begin{pmatrix}1&2\\3&4\end{pmatrix}$ 的逆矩阵。",
         a=r"$\begin{pmatrix}-2&1\\ \frac32&-\frac12\end{pmatrix}$",
         s=r"$A^{-1}=\frac{1}{|A|}A^{*}$，$|A|=-2$，伴随矩阵为 $\begin{pmatrix}4&-2\\-3&1\end{pmatrix}$。",
         check=r"eq(Matrix([[1,2],[3,4]]).inv(), Matrix([[-2, 1],[Rational(3,2), Rational(-1,2)]]))"),

    dict(id="A07", level=2, tags=["矩阵的秩"], q=r"求 $\begin{pmatrix}1&2&3\\2&4&6\end{pmatrix}$ 的秩。",
         a=r"$1$",
         s=r"第二行是第一行的 2 倍，故秩为 1。",
         check=r"eq(Matrix([[1,2,3],[2,4,6]]).rank(), 1)"),

    dict(id="A08", level=2, tags=["线性相关"], q=r"判断向量组 $(1,2,3)$、$(2,4,6)$ 是否线性相关。",
         a=r"线性相关（第二个是第一个的 2 倍）",
         s=r"以它们为行作矩阵，秩为 1 $<2$，故线性相关。",
         check=r"eq(Matrix([[1,2,3],[2,4,6]]).rank(), 1)"),

    dict(id="A09", level=2, tags=["线性方程组"], q=r"解方程组 $\begin{cases}x+y=3\\ x-y=1\end{cases}$。",
         a=r"$x=2,\ y=1$",
         s=r"两式相加得 $2x=4$，故 $x=2$；代回得 $y=1$。",
         check=r"zero((x+y-3).subs({x: 2, y: 1})) and zero((x-y-1).subs({x: 2, y: 1}))"),

    dict(id="A10", level=2, tags=["迹", "行列式"], q=r"求 $\begin{pmatrix}2&1\\1&3\end{pmatrix}$ 的迹与行列式。",
         a=r"$\operatorname{tr}=5$，$\det=5$",
         s=r"迹为主对角元之和 $2+3=5$；行列式 $2\cdot3-1\cdot1=5$。",
         check=r"eq(Matrix([[2,1],[1,3]]).trace(), 5) and eq(Matrix([[2,1],[1,3]]).det(), 5)"),

    dict(id="A11", level=4, tags=["凯莱-哈密顿定理"], q=r"验证 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$ 满足 $A^{2}-5A-2I=O$。",
         a=r"成立",
         s=r"$\operatorname{tr}A=5$、$\det A=-2$，特征多项式为 $\lambda^{2}-5\lambda-2$，由凯莱-哈密顿定理即得。",
         check=r"zero(Matrix([[1,2],[3,4]])**2 - 5*Matrix([[1,2],[3,4]]) - 2*eye(2))"),

    dict(id="A12", level=1, tags=["内积", "正交"], q=r"判断 $(1,0)$ 与 $(0,1)$ 是否正交。",
         a=r"正交，内积为 $0$",
         s=r"内积 $1\cdot0+0\cdot1=0$。",
         check=r"eq(Matrix([1,0]).dot(Matrix([0,1])), 0)"),

    dict(id="A13", level=3, tags=["正定"], q=r"判断二次型 $x^{2}+2y^{2}$ 是否正定。",
         a=r"正定",
         s=r"对应矩阵 $\begin{pmatrix}1&0\\0&2\end{pmatrix}$ 的特征值 $1,2$ 均大于 0，故正定。",
         check=r"all(v > 0 for v in Matrix([[1,0],[0,2]]).eigenvals().keys())"),

    dict(id="A14", level=3, tags=["可对角化"], q=r"判断 $\begin{pmatrix}2&1\\0&3\end{pmatrix}$ 是否可对角化。",
         a=r"可对角化（两个相异特征值）",
         s=r"特征值 $2,3$ 互异，$n$ 阶矩阵有 $n$ 个相异特征值必可对角化。",
         check=r"eq(len(Matrix([[2,1],[0,3]]).eigenvals()), 2)"),

    dict(id="A15", level=2, tags=["行列式性质"], q=r"验证 $|AB|=|A||B|$，其中 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$、$B=\begin{pmatrix}2&0\\1&3\end{pmatrix}$。",
         a=r"$|A|=-2$，$|B|=6$，$|AB|=-12$，等式成立",
         s=r"直接计算 $AB$ 的行列式与两者行列式之积即可。",
         check=r"eq(det(Matrix([[1,2],[3,4]])*Matrix([[2,0],[1,3]])), det(Matrix([[1,2],[3,4]]))*det(Matrix([[2,0],[1,3]])))"),

    dict(id="A16", level=3, tags=["转置性质"], q=r"验证 $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$。",
         a=r"成立",
         s=r"取 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$、$B=\begin{pmatrix}2&0\\1&3\end{pmatrix}$ 直接验证。",
         check=r"zero((Matrix([[1,2],[3,4]])*Matrix([[2,0],[1,3]])).T - Matrix([[2,0],[1,3]]).T*Matrix([[1,2],[3,4]]).T)"),

    dict(id="A17", level=3, tags=["特征向量"], q=r"验证 $\begin{pmatrix}1\\1\end{pmatrix}$ 是 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 的特征向量，并求对应特征值。",
         a=r"是，对应特征值 $\lambda=3$",
         s=r"$A\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}3\\3\end{pmatrix}=3\begin{pmatrix}1\\1\end{pmatrix}$。",
         check=r"eq(Matrix([[2,1],[1,2]])*Matrix([1,1]), 3*Matrix([1,1]))"),

    dict(id="A18", level=3, tags=["秩-零化度"], q=r"求 $3\times3$ 矩阵 $\begin{pmatrix}1&2&3\\4&5&6\\7&8&9\end{pmatrix}$ 的零空间维数。",
         a=r"$1$",
         s=r"该矩阵秩为 2（第三行是前两行的线性组合），故零化度 $=3-2=1$。",
         check=r"eq(3 - Matrix([[1,2,3],[4,5,6],[7,8,9]]).rank(), 1)"),

    dict(id="A19", level=2, tags=["齐次方程组"], q=r"判断齐次方程组 $x+2y=0,\ 2x+4y=0$ 是否有非零解。",
         a=r"有非零解（系数行列式为 0）",
         s=r"$\begin{vmatrix}1&2\\2&4\end{vmatrix}=0$，故有非零解，解空间维数为 1。",
         check=r"eq(det(Matrix([[1,2],[2,4]])), 0)"),

    dict(id="A20", level=3, tags=["矩阵幂"], q=r"设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^{3}$。",
         a=r"$\begin{pmatrix}1&3\\0&1\end{pmatrix}$",
         s=r"$A$ 是幂幺矩阵，$A^{n}=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。",
         check=r"eq(Matrix([[1,1],[0,1]])**3, Matrix([[1,3],[0,1]]))"),

    dict(id="A21", level=2, tags=["对称矩阵"], q=r"判断 $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 是否为对称矩阵。",
         a=r"是对称矩阵",
         s=r"$A^{\mathsf T}=A$。对称矩阵的特征值全为实数，且有正交特征向量组。",
         check=r"zero(Matrix([[2,1],[1,2]]) - Matrix([[2,1],[1,2]]).T)"),

    dict(id="A22", level=1, tags=["向量范数"], q=r"求向量 $(3,4)$ 的欧几里得范数。",
         a=r"$5$",
         s=r"$\sqrt{3^{2}+4^{2}}=\sqrt{25}=5$。",
         check=r"eq(sqrt(3**2 + 4**2), 5)"),

    dict(id="A23", level=2, tags=["行列式性质", "上三角"], q=r"计算上三角矩阵 $\begin{pmatrix}1&2&3\\0&4&5\\0&0&6\end{pmatrix}$ 的行列式。",
         a=r"$24$",
         s=r"三角形矩阵的行列式等于主对角元之积 $1\cdot4\cdot6=24$。",
         check=r"eq(det(Matrix([[1,2,3],[0,4,5],[0,0,6]])), 24)"),

    dict(id="A24", level=3, tags=["投影"], q=r"求向量 $(1,1)$ 在 $(1,0)$ 方向上的投影系数。",
         a=r"投影系数为 $1$，投影向量为 $(1,0)$",
         s=r"$\frac{\langle(1,1),(1,0)\rangle}{\langle(1,0),(1,0)\rangle}=\frac11=1$。",
         check=r"eq(Matrix([1,0]).dot(Matrix([1,1]))/Matrix([1,0]).dot(Matrix([1,0])), 1)"),

    dict(id="A25", level=3, tags=["相似"], q=r"判断 $\begin{pmatrix}1&0\\0&2\end{pmatrix}$ 与 $\begin{pmatrix}2&0\\0&1\end{pmatrix}$ 是否相似。",
         a=r"相似",
         s=r"两者特征值集合相同（都是 $1,2$）且各有 $2$ 个线性无关特征向量，故都相似于同一个对角矩阵。",
         check=r"all(any(eq(v, k) for k in (1, 2)) for v in Matrix([[1,0],[0,2]]).eigenvals().keys()) and all(any(eq(v, k) for k in (1, 2)) for v in Matrix([[2,0],[0,1]]).eigenvals().keys())"),

    dict(id="A26", level=4, tags=["行列式", "范德蒙德"], q=r"计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\1&2&3\\1&4&9\end{vmatrix}$。",
         a=r"$2$",
         s=r"范德蒙德行列式 $=\prod_{1\le i&lt;j\le3}(x_j-x_i)=(2-1)(3-1)(3-2)=2$，这里 $x=(1,2,3)$（转置不影响行列式值）。",
         check=r"eq(det(Matrix([[1,1,1],[1,2,3],[1,4,9]])), (2-1)*(3-1)*(3-2))"),
]
