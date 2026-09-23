/* 经典难题与猜想数据（LBLB）
 * window.CLASSIC_PROBLEMS = { conjectures: [...] }
 * 字段：id / name / status / content(支持 $LaTeX$) / progress / key_papers / last_update / query
 * status 取值：'未解决' | '部分解决' | '已解决'
 * 状态结论由人工维护；key_papers 中的「最新论文」与 last_update 由 经典难题更新器.py 从 arXiv 自动刷新。
 */
window.CLASSIC_PROBLEMS = {
 "updatedAt": "2026-09-18",
 "note": "状态结论人工维护；「最后更新 / 最新论文」由 经典难题更新器.py 运行后写入。",
 "conjectures": [
  {
   "id": "p_vs_np",
   "name": "P 对 NP",
   "status": "未解决",
   "content": "$P$ 与 $NP$ 是否相等：「可快速验证」是否等于「可快速求解」？",
   "progress": "千禧年七大难题之一。绝大多数计算机科学家相信 $P\\neq NP$；若 $P=NP$，现代密码体系将大面积崩塌。",
   "key_papers": [
    "J{é}rome Clech (2026). Ontological free will as incompressible information adjunction: A noncomputability boundary beyond P versus NP. https://arxiv.org/abs/2609.15464v1",
    "Lijie Chen, Jiatu Li, Igor C. Oliveira 等 (2026). A Theory for Probabilistic Polynomial-Time Reasoning. https://arxiv.org/abs/2602.09302v1",
    "Swathi D, N Sadagopan (2025). Secure Domination in Bisplit graphs -- A Structural and algorithmic study. https://arxiv.org/abs/2512.23989v2"
   ],
   "last_update": "2026-09-18",
   "query": "P versus NP"
  },
  {
   "id": "riemann",
   "name": "黎曼猜想",
   "status": "未解决",
   "content": "黎曼 $\\zeta$ 函数的非平凡零点全部位于实部 $\\mathrm{Re}\\,s=\\tfrac{1}{2}$ 的直线上。",
   "progress": "千禧年难题。与素数精确分布等价；数值已验证超过 $10^{13}$ 个零点，无一反例。",
   "key_papers": [
    "Marco Desogus (2026). The Three Gates: A Rooted-Operator Approach to Weil Positivity. https://arxiv.org/abs/2609.20367v1",
    "Yuichiro Toma (2026). Extreme values of Euler-Kronecker constants of cubic abelian fields. https://arxiv.org/abs/2609.18569v1",
    "Y. Kenan Yılmaz (2026). Generalized DCCQ: From Binary Quotients to Multinomial Simplex Geometry and Critical-Strip Coordinates. https://arxiv.org/abs/2609.17899v1"
   ],
   "last_update": "2026-09-18",
   "query": "Riemann hypothesis"
  },
  {
   "id": "poincare",
   "name": "庞加莱猜想",
   "status": "已解决",
   "content": "单连通的闭三维流形同胚于三维球面 $S^3$。",
   "progress": "佩雷尔曼 2002–2003 用带手术的里奇流完成证明，并拒绝菲尔兹奖与百万奖金。是千禧年难题中唯一被解决者。",
   "key_papers": [
    "G. Perelman (2002). The entropy formula for the Ricci flow and its geometric applications. https://arxiv.org/abs/math/0211159"
   ],
   "last_update": "2026-09-18",
   "query": "Perelman Ricci flow Poincare conjecture"
  },
  {
   "id": "hodge",
   "name": "霍奇猜想",
   "status": "未解决",
   "content": "光滑射影代数簇上，整系数 Hodge 类是否都能由代数子簇的上同调类线性组合表示？",
   "progress": "千禧年难题。对部分特殊情形（如曲线、Abel 簇的某些类）已知成立，一般情形未解决。",
   "key_papers": [
    "Patrick Brosnan (2026). Discriminants of Hermitian forms, maximal degenerations and Kontsevich's tropical approach to the Hodge conjecture. https://arxiv.org/abs/2609.14169v1",
    "David Favero, Tyler L. Kelly (2026). The Chern character of a coherent sheaf on a smooth projective hypersurface. https://arxiv.org/abs/2609.12759v1",
    "Jake Huryn, William C. Newman (2026). On the torsion in the Chow motive of an Enriques surface. https://arxiv.org/abs/2609.04360v1"
   ],
   "last_update": "2026-09-18",
   "query": "Hodge conjecture"
  },
  {
   "id": "yang_mills",
   "name": "杨–米尔斯存在性与质量间隙",
   "status": "未解决",
   "content": "四维时空上是否存在满足 Wightman 公理、且具有正质量间隙的 Yang–Mills 理论严格解？",
   "progress": "千禧年难题。物理上质量间隙已被实验证实，严格数学构造仍缺失。",
   "key_papers": [],
   "last_update": "2026-09-18",
   "query": "Yang-Mills existence mass gap"
  },
  {
   "id": "navier_stokes",
   "name": "纳维–斯托克斯方程光滑性",
   "status": "未解决",
   "content": "三维不可压 Navier–Stokes 方程在给定光滑初值下，解是否总存在且处处光滑（不产生有限时间奇点）？",
   "progress": "千禧年难题。近年有研究团队声称给出三维有限时间爆破的解析证明并完成 Lean 4 形式化，仍处独立复核与优先权争议阶段，克雷研究所未颁奖。",
   "key_papers": [
    "Runlong Yu (2026). Finite-Window Computational Anti-Phantom Theorems for Scale-Critical Navier-Stokes Defects. https://arxiv.org/abs/2606.15456v1",
    "Runlong Yu (2026). Critical Ledgers and Scale-Defect Cascades for Navier-Stokes. https://arxiv.org/abs/2606.13887v1",
    "Runlong Yu (2026). Invisible Defect Cascades for Navier-Stokes Regularity. https://arxiv.org/abs/2606.12756v1"
   ],
   "last_update": "2026-09-18",
   "query": "Navier-Stokes regularity"
  },
  {
   "id": "bsd",
   "name": "贝赫–斯温纳顿-戴尔猜想",
   "status": "未解决",
   "content": "椭圆曲线 $E$ 的 $L$ 函数在 $s=1$ 处零点的阶数，是否等于 $E$ 的有理点群秩？",
   "progress": "千禧年难题。已有大量数值与理论支持（Gross–Zagier、Kolyvagin 给出秩 0/1 的部分结论），一般情形未解决。",
   "key_papers": [
    "Bo-Hae Im, Minseo Shin (2026). Tunnell-type criteria for variants of the congruent number problem. https://arxiv.org/abs/2609.19085v1",
    "Barinder S. Banwait, Xiaoyu Huang (2026). On the Identification of Elliptic Curves That Admit Infinitely Many Twists Satisfying the Birch-Swinnerton-Dyer Conjecture. https://arxiv.org/abs/2601.16044v3",
    "Dominik Bullach, David Burns (2025). On Euler systems and Nekovář-Selmer complexes. https://arxiv.org/abs/2509.13894v2"
   ],
   "last_update": "2026-09-18",
   "query": "Birch Swinnerton-Dyer conjecture"
  },
  {
   "id": "goldbach",
   "name": "哥德巴赫猜想",
   "status": "未解决",
   "content": "每个大于 2 的偶数都是两个素数之和。",
   "progress": "陈景润 1966/1973 证明「1+2」（充分大偶数 = 素数 + 至多两个素数之积）；已计算机验证至 $4\\times10^{18}$ 以内全部成立，「1+1」仍未解决。",
   "key_papers": [
    "Marco Cantarini (2026). Averages of diagonal Elliott-Halberstam problem twisted by Möbius function with Sobolev and Hölder-Zygmund weights. https://arxiv.org/abs/2607.09110v1",
    "Jiamin Li, Jianya Liu (2026). Theorem $(1+1.9)$ on the Goldbach Conjecture. https://arxiv.org/abs/2606.05224v2",
    "Michael Harm, Daniel R. Johnston (2026). The reverse Goldbach problem and a refined Zsiflaw--Legeis theorem. https://arxiv.org/abs/2605.21876v2"
   ],
   "last_update": "2026-09-18",
   "query": "Goldbach conjecture"
  },
  {
   "id": "weak_goldbach",
   "name": "弱哥德巴赫猜想（三素数定理）",
   "status": "已解决",
   "content": "每个大于 5 的奇数都是三个素数之和。",
   "progress": "Helfgott 2013 给出完整证明（借助计算机辅助验证小范围），弱哥德巴赫猜想已解决。",
   "key_papers": [
    "H. A. Helfgott (2013). The ternary Goldbach conjecture is true. https://arxiv.org/abs/1312.7748"
   ],
   "last_update": "2026-09-18",
   "query": "ternary Goldbach conjecture Helfgott"
  },
  {
   "id": "twin_prime",
   "name": "孪生素数猜想",
   "status": "未解决",
   "content": "相差 2 的素数对（孪生素数）有无穷多。",
   "progress": "张益唐 2013 证明存在无穷多对素数间隔小于 7000 万；经 Maynard 与 Polymath8b 压缩到 246。差距为 2 仍开放。",
   "key_papers": [
    "Y. Zhang (2014). Bounded gaps between primes. https://arxiv.org/abs/1305.6369",
    "J. Maynard (2015). Small gaps between primes. https://arxiv.org/abs/1311.4600",
    "D. H. J. Polymath (2014). New equidistribution estimates of Zhang type. https://arxiv.org/abs/1407.4897",
    "Ahmet M. Güloğlu, Asimina S. Hamakiotes, Sung Min Lee 等 (2026). Average twin prime conjecture for elliptic curves in arithmetic progressions. https://arxiv.org/abs/2608.29938v1",
    "Tushar Pandey (2026). An intermediate conjecture between Goldbach and Dubner: every even number is the sum of a prime and a twin prime. https://arxiv.org/abs/2608.02381v2",
    "Jiamin Li, Jianya Liu (2026). Theorem $(1+1.9)$ on the Goldbach Conjecture. https://arxiv.org/abs/2606.05224v2"
   ],
   "last_update": "2026-09-18",
   "query": "twin prime conjecture"
  },
  {
   "id": "collatz",
   "name": "考拉兹猜想（3x+1）",
   "status": "未解决",
   "content": "任取正整数：偶数除以 2，奇数乘 3 加 1，反复操作是否最终总能到达 1？",
   "progress": "陶哲轩 2019 证明「几乎所有」初值的轨道最终远小于初值；已验证至 $2^{68}$ 以内。一般情形未解决。",
   "key_papers": [
    "T. Tao (2019). Almost all orbits of the Collatz map attain almost bounded values. https://arxiv.org/abs/1909.03562",
    "Oliver Kramer (2026). Adaptive Search in Collatz Exponent-Code Space via 2-adic and 3-adic Constraints. https://arxiv.org/abs/2607.10041v1",
    "Jennifer Williams (2026). A Coordinate System for Collatz Dynamics. https://arxiv.org/abs/2607.01718v1",
    "Tong Niu (2026). Parity vectors and paradoxical sequences in the accelerated Collatz map. https://arxiv.org/abs/2605.13886v2"
   ],
   "last_update": "2026-09-18",
   "query": "Collatz conjecture"
  },
  {
   "id": "abc",
   "name": "abc 猜想",
   "status": "部分解决",
   "content": "对任意 $\\varepsilon>0$，仅有限多个互素三元组 $(a,b,c)$ 满足 $a+b=c$ 且 $c>\\mathrm{rad}(abc)^{1+\\varepsilon}$。",
   "progress": "望月新一 2012 提出「宇宙际 Teichmüller 理论」给出证明；主流学界尚未达成共识，Scholze 与 Stix 指出关键推论存在缺口。",
   "key_papers": [
    "Hector Pasten (2026). Improved bounds for Szpiro's conjecture. https://arxiv.org/abs/2609.17390v1",
    "R. Laniewski (2026). Radical defects, Wieferich primes, and the $abc$ conjecture. https://arxiv.org/abs/2609.00039v1",
    "N. A. Carella (2026). Note on the Exceptional Set in the ABC Conjecture. https://arxiv.org/abs/2608.16764v2"
   ],
   "last_update": "2026-09-18",
   "query": "abc conjecture"
  },
  {
   "id": "catalan",
   "name": "卡塔兰猜想",
   "status": "已解决",
   "content": "方程 $x^a-y^b=1$（$x,y,a,b$ 为正整数，$a,b>1$）只有一组解：$3^2-2^3=1$。",
   "progress": "Mihăilescu 2002 用分圆域与 Baker 理论完成证明。",
   "key_papers": [
    "R. Balasubramanian, Pandey Prem Prakash (2009). Catalan's Conjecture over Number Fields. https://arxiv.org/abs/0901.4305v5"
   ],
   "last_update": "2026-09-18",
   "query": "Catalan conjecture Mihailescu"
  },
  {
   "id": "four_color",
   "name": "四色定理",
   "status": "已解决",
   "content": "任何平面地图都能用四种颜色染色，使相邻区域颜色不同。",
   "progress": "Appel–Haken 1976 用计算机检查上千种可约构型完成证明；2005 年 Gonthier 用 Coq 完成形式化验证。",
   "key_papers": [
    "Yuta Inoue, Ken-ichi Kawarabayashi, Rintaro Matsuo 等 (2026). Three-edge-coloring apex cubic graphs. https://arxiv.org/abs/2608.22870v1",
    "Kamal Santra (2026). An Improved Upper Bound for the Strong Odd Chromatic Number of Planar Graphs. https://arxiv.org/abs/2608.03522v1",
    "Scott Baldridge, Louis H. Kauffman, Ben McCarty (2026). A counterexample for the polar conjecture of Spencer-Brown. https://arxiv.org/abs/2607.22398v1"
   ],
   "last_update": "2026-09-18",
   "query": "four color theorem"
  },
  {
   "id": "fermat",
   "name": "费马大定理",
   "status": "已解决",
   "content": "对整数 $n\\ge3$，方程 $x^n+y^n=z^n$ 无非零整数解。",
   "progress": "怀尔斯 1994–1995 借助谷山–志村–韦伊猜想（半稳定情形）完成证明，358 年悬案终结。",
   "key_papers": [
    "A. Wiles (1995). Modular elliptic curves and Fermat's Last Theorem. Annals of Mathematics."
   ],
   "last_update": "2026-09-18",
   "query": "Fermat last theorem modular"
  },
  {
   "id": "continuum",
   "name": "连续统假设",
   "status": "已解决",
   "content": "是否存在基数严格介于自然数集与实数集之间？（$2^{\\aleph_0}=\\aleph_1$ 是否成立）",
   "progress": "在 ZFC 框架内不可判定：Gödel 1940 证明 CH 与 ZFC 相容，Cohen 1963 用力迫法证明 $\\neg$CH 也与 ZFC 相容——独立于 ZFC。",
   "key_papers": [
    "P. J. Cohen (1966). Set Theory and the Continuum Hypothesis."
   ],
   "last_update": "2026-09-18",
   "query": "continuum hypothesis independence"
  },
  {
   "id": "euler_mascheroni",
   "name": "欧拉–马歇罗尼常数 γ 的有理性",
   "status": "未解决",
   "content": "常数 $\\gamma=\\lim_{n\\to\\infty}\\bigl(\\sum_{k=1}^{n}\\tfrac1k-\\ln n\\bigr)$ 是否是无理数？",
   "progress": "连 γ 是有理数还是无理数都未知（极可能无理）。与黎曼假设有深刻关联。",
   "key_papers": [],
   "last_update": "2026-09-18",
   "query": "Euler-Mascheroni constant irrational"
  },
  {
   "id": "odd_zeta",
   "name": "奇数值黎曼 ζ 函数的无理性",
   "status": "部分解决",
   "content": "$\\zeta(3),\\zeta(5),\\zeta(7),\\dots$ 是否全部为无理数？",
   "progress": "$\\zeta(3)$ 无理由 Apéry 1978 证明；Zudilin 2001 证明 $\\zeta(5),\\zeta(7),\\zeta(9),\\zeta(11)$ 中至少一个无理。一般情形开放。",
   "key_papers": [],
   "last_update": "2026-09-18",
   "query": "odd zeta values irrational"
  },
  {
   "id": "odd_perfect",
   "name": "奇完全数",
   "status": "未解决",
   "content": "是否存在奇数 $n$，其真因子之和恰好等于 $n$？",
   "progress": "至今一个奇完全数都未找到，也未证明不存在；已知任何奇完全数都大于 $10^{1500}$。",
   "key_papers": [
    "Pascal Ochem, Joshua Zelinsky (2026). On odd perfect numbers with exactly one even exponent greater than 2. https://arxiv.org/abs/2607.19746v1",
    "Marco Mantovanelli (2026). Certified Minimal-Prime Branch Closures for Odd Perfect Numbers. https://arxiv.org/abs/2607.04365v1",
    "Jan Florek (2025). The enumeration of plane (3,6)-triangulations and the form of odd perfect numbers. https://arxiv.org/abs/2504.13316v3"
   ],
   "last_update": "2026-09-18",
   "query": "odd perfect number"
  },
  {
   "id": "perfect_cuboid",
   "name": "完美长方体",
   "status": "未解决",
   "content": "是否存在长、宽、高、三条面对角线与体对角线均为整数的长方体？",
   "progress": "欧拉砖（面对角线整数）大量存在；体对角线也为整数的「完美长方体」是否存在仍未知。",
   "key_papers": [
    "Ricky Cipollini (2026). Elimination of René Peschmann's 968 Remaining Hard Fibers for the Perfect Cuboid Problem. https://arxiv.org/abs/2609.14526v1",
    "René Peschmann (2026). Exponent-one blockers and a Mordell-Weil construction of Euler bricks. https://arxiv.org/abs/2605.00573v1",
    "René Peschmann (2026). A torsion-intersection proof of perfect-cuboid nonexistence on 1,072 explicit master-tuple fibers. https://arxiv.org/abs/2604.28072v1"
   ],
   "last_update": "2026-09-18",
   "query": "perfect cuboid"
  },
  {
   "id": "kepler",
   "name": "开普勒猜想",
   "status": "已解决",
   "content": "三维空间中相同大小球体的最密堆积密度是否为 $\\pi/\\sqrt{18}\\approx0.7405$？",
   "progress": "Hales 1998 给出计算机辅助证明，2017 年 Flyspeck 项目用交互式定理证明器完成形式化验证。",
   "key_papers": [
    "Qidong He (2026). Unified criteria for crystallization in hard-core lattice systems with applications to polyomino fluids and multi-component mixtures. https://arxiv.org/abs/2602.05294v3",
    "Thomas Hales (2024). The Formal Proof of the Kepler Conjecture: a critical retrospective. https://arxiv.org/abs/2402.08032v1",
    "R. Ganesh, Amna Khairi Nasr (2023). Correlations in randomly stacked solids. https://arxiv.org/abs/2306.13569v1"
   ],
   "last_update": "2026-09-18",
   "query": "Kepler conjecture"
  },
  {
   "id": "kakeya_3d",
   "name": "三维 Kakeya 猜想",
   "status": "已解决",
   "content": "三维空间中每个包含各方向单位线段的集合（Kakeya 集），其 Hausdorff 维数与 Minkowski 维数是否均为 3？",
   "progress": "王虹与 Joshua Zahl 2025 年发表约百页证明，陶哲轩称之为「百年一遇」的证明。",
   "key_papers": [
    "H. Wang, J. Zahl (2025). A proof of the three-dimensional Kakeya conjecture (arXiv preprint)."
   ],
   "last_update": "2026-09-18",
   "query": "Kakeya conjecture three dimensional"
  },
  {
   "id": "sphere_packing",
   "name": "八维/二十四维球堆积",
   "status": "已解决",
   "content": "$E_8$ 格是否为八维最密球堆积？Leech 格是否为二十四维最密球堆积？",
   "progress": "Viazovska 2016 证明 $E_8$ 情形，2017 与 Cohn 等合作证明 Leech 情形；Viazovska 获 2022 菲尔兹奖。",
   "key_papers": [
    "M. Viazovska (2017). The sphere packing problem in dimension 8. https://arxiv.org/abs/1603.04246"
   ],
   "last_update": "2026-09-18",
   "query": "sphere packing dimension 8 Leech lattice"
  },
  {
   "id": "graph_isomorphism",
   "name": "图同构问题是否属于 P",
   "status": "未解决",
   "content": "是否存在多项式时间算法判定两个图是否同构？",
   "progress": "Babai 2015 给出拟多项式时间算法；是否有多项式时间算法仍开放，通常相信是 NP 中间问题。",
   "key_papers": [],
   "last_update": "2026-09-18",
   "query": "graph isomorphism quasi-polynomial"
  },
  {
   "id": "ramsey_r55",
   "name": "拉姆齐数 R(5,5)",
   "status": "未解决",
   "content": "$R(5,5)$ 的精确值是多少？（保证 5 人团或 5 人独立集所需的最小人数）",
   "progress": "已知 $43\\le R(5,5)\\le 48$，精确值未定；计算量巨大。",
   "key_papers": [
    "Vigleik Angeltveit, Brendan D. McKay (2024). $R(5,5)\\le 46$. https://arxiv.org/abs/2409.15709v2",
    "Lachlan Ge, Yasiru Jayasooriya, Alex Qiu 等 (2022). Study of Exoo's Lower Bound for Ramsey number $R(5,5)$. https://arxiv.org/abs/2212.12630v3",
    "Colton Magnant, Ingo Schiermeyer (2019). Gallai-Ramsey number for $K_{5}$. https://arxiv.org/abs/1901.03622v1"
   ],
   "last_update": "2026-09-18",
   "query": "Ramsey number R(5,5)"
  },
  {
   "id": "one_way",
   "name": "单向函数存在性",
   "status": "未解决",
   "content": "是否存在易于计算、但难以求逆的函数族（单向函数）？",
   "progress": "与 $P\\neq NP$ 密切相关。若证明不存在，现代密码学根基动摇。",
   "key_papers": [
    "Jose Carrasco, Jens Eisert, Soumik Ghosh 等 (2026). Instantiating Microcrypt: Obstacles and opportunities via tailored state certification. https://arxiv.org/abs/2609.15842v1",
    "Satyadev Nandakumar, Akhil S, Chandra Shekhar Tiwari (2026). Resource bounded Kučera-Gács Theorems. https://arxiv.org/abs/2605.21546v1",
    "John M. Hitchcock, Adewale Sekoni, Hadi Shafei (2025). Counting Martingales for Measure and Dimension in Complexity Classes. https://arxiv.org/abs/2508.07619v1"
   ],
   "last_update": "2026-09-18",
   "query": "one-way functions existence"
  },
  {
   "id": "legendre",
   "name": "勒让德猜想",
   "status": "未解决",
   "content": "对任意正整数 $n$，$n^2$ 与 $(n+1)^2$ 之间是否恒存在素数？",
   "progress": "兰道四问题之一。素数定理可证区间内素数平均个数为正，但逐 $n$ 普遍成立未证。",
   "key_papers": [],
   "last_update": "2026-09-18",
   "query": "Legendre's conjecture primes"
  },
  {
   "id": "n2p1",
   "name": "n²+1 型素数无穷性",
   "status": "未解决",
   "content": "形如 $n^2+1$ 的素数是否有无穷多个？",
   "progress": "兰道四问题之一。是 Bunyakovsky 猜想与 Bateman–Horn 猜想的一部分；无穷性未证。",
   "key_papers": [],
   "last_update": "2026-09-18",
   "query": "primes of the form n^2+1"
  },
  {
   "id": "mersenne",
   "name": "梅森素数无穷性",
   "status": "未解决",
   "content": "形如 $2^p-1$（$p$ 为素数）的素数是否有无穷多个？",
   "progress": "梅森素数是目前已知最大素数的来源；无穷性完全未知。",
   "key_papers": [],
   "last_update": "2026-09-18",
   "query": "Mersenne primes infinite"
  },
  {
   "id": "hilbert10",
   "name": "希尔伯特第 10 问题",
   "status": "已解决",
   "content": "是否存在一般算法判定任意整数（丢番图）方程是否有整数解？",
   "progress": "Matiyasevich 1970 证明不存在这样的算法（结合 Davis、Putnam、Robinson 的工作）——答案是否定的。",
   "key_papers": [
    "Zhi-Wei Sun (2026). Ten unknowns for Hilbert's tenth problem over the integers. https://arxiv.org/abs/2609.01594v2",
    "Zhi-Wei Sun (2026). On Diophantine equations over the integer rings of quadratic fields. https://arxiv.org/abs/2608.03992v1",
    "Gabriel Istrate, Mihai Prunescu, Joseph M. Shunia (2026). Undecidability, Chaos and Universality in Arithmetic Terms. https://arxiv.org/abs/2606.09336v2"
   ],
   "last_update": "2026-09-18",
   "query": "Hilbert tenth problem"
  },
  {
   "id": "godel",
   "name": "哥德尔不完备定理",
   "status": "已解决",
   "content": "任何包含算术的、一致且递归可公理化的形式系统，都存在无法在系统内判定真假的命题。",
   "progress": "Gödel 1931 年证明：数学公理系统在「一致性」与「完备性」之间不可兼得。",
   "key_papers": [
    "Mir Faizal, Lawrence M. Krauss, Arshid Shabir 等 (2025). Can quantum gravity be both consistent and complete?. https://arxiv.org/abs/2505.11773v3",
    "Dragutin Mihailovic, Darko Kapor, Sinisa Crvenkovic 等 (2021). Physics as the science of the possible: Discovery in the age of Godel (1.1 Generality of physics). https://arxiv.org/abs/2104.08515v1",
    "Arun Uday (2018). A dual identity based symbolic understanding of the Godel's incompleteness theorems, P-NP problem, Zeno's paradox and Continuum Hypothesis. https://arxiv.org/abs/1807.09600v1"
   ],
   "last_update": "2026-09-18",
   "query": "Godel incompleteness"
  },
  {
   "id": "cfdg",
   "name": "有限单群分类",
   "status": "已解决",
   "content": "所有有限单群是否都被完整分类（素数阶循环群、交错群、李型群与 26 个散在群）？",
   "progress": "分类定理约于 1980 年代完成（官方修订版 2004）；被称为数学史上最长的证明（数万页、数百人参与）。",
   "key_papers": [
    "Tianjiao Nie, Ao Zhang, Yusen Tang 等 (2026). FormaTheoria: Constructing Large-Scale Lean Theories from Mathematical Literature $-$ Toward the Formalization of the Classification of Finite Simple Groups. https://arxiv.org/abs/2608.10894v1",
    "Youlong Ding (2026). Linear-Time Verification of Rings and Fields. https://arxiv.org/abs/2608.07272v1",
    "Evgeny Khukhro, Pavel Shumyatsky (2026). On finite groups containing an element whose Engel sink is small. https://arxiv.org/abs/2605.08607v3"
   ],
   "last_update": "2026-09-18",
   "query": "classification of finite simple groups"
  }
 ]
};
