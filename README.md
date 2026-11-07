# 数学理解课

目标：增强数学素养，理解概念为什么这样定义、结论为什么成立，并能用它们解释问题。

双击打开 [HTML 学习首页](index.html)。所有讲解、图形和交互均可离线使用，无需安装依赖；外部教材需要联网。推荐现代 Chrome、Edge 或 Firefox。

## 如何划分数学

数学没有唯一、公认且互不重叠的“全部主分支”清单。这里采用 **17 个学习方向 + 1 个预备模块**，覆盖基础、纯数学、计算与应用，并将相近研究领域归组。代数几何、随机分析等交叉领域可能属于多个方向；数学史与数学教育作为素养方向单列。此地图参考 [MSC2020](https://msc2020.org/) 的研究分类，但学习分组不是 MSC 官方分级。

## 分支与子领域

| 分支 / 教程入口 | 主要子领域 | 入门先修 |
|---|---|---|
| [算术、函数与预备知识](00-preparation/index.html) | 数与运算；分数和比例；幂与对数；方程与不等式；函数；三角函数 | 四则运算；不会可从本页开始 |
| [数学基础与证明](01-foundations/index.html) | 整数、分数与比例；集合与映射；命题逻辑；证明方法；集合论、公理与可计算性 | 四则运算 |
| [代数与结构](02-algebra/index.html) | 初等代数；多项式；群论；环论；域论；交换代数；表示论；范畴论与同调代数 | 分数、等式与基础证明 |
| [数论](03-number-theory/index.html) | 整除与同余；素数；丢番图方程；解析数论；代数数论；算术几何 | 整数、代数与证明 |
| [线性代数](04-linear-algebra/index.html) | 线性方程组；向量空间；线性映射；矩阵；特征值；内积与谱分解；多重线性代数 | 初等代数、坐标平面 |
| [几何学](05-geometry/index.html) | 欧氏几何；解析几何；射影几何；微分几何；黎曼几何；代数几何；凸几何 | 代数、坐标与基础证明 |
| [微积分与数学分析](06-analysis/index.html) | 函数与极限；微分；积分；实分析；复分析；测度论；调和分析；泛函分析；非标准分析 | 函数、代数、坐标 |
| [拓扑学](07-topology/index.html) | 点集拓扑；连续与同胚；紧致性；连通性；代数拓扑；微分拓扑；几何拓扑 | 集合、映射；进阶需分析和代数 |
| [组合数学与图论](08-combinatorics/index.html) | 计数；递推；生成函数；图论；极值组合；设计理论；离散几何 | 整数与基础证明 |
| [概率论](09-probability/index.html) | 概率空间；条件概率；随机变量；分布；大数定律；极限定理；随机过程；随机分析 | 分数、集合；进阶需分析 |
| [统计学](10-statistics/index.html) | 描述统计；抽样；参数估计；假设检验；回归；贝叶斯统计；实验设计；多元与非参数统计 | 概率、代数；组合数见 08 |
| [微分方程与动力系统](11-differential-equations/index.html) | 常微分方程；偏微分方程；积分方程；差分方程；稳定性；分岔；混沌；遍历理论 | 导数、积分；第 7 课相平面需线性代数（特征值见 04 第 07 课） |
| [数值分析与科学计算](12-numerical/index.html) | 误差；插值与逼近；数值线性代数；数值积分；方程求根；微分方程数值解；计算可靠性 | 代数、微积分 |
| [优化、运筹与控制](13-optimization/index.html) | 凸优化；线性规划；整数规划；变分法；最优控制；博弈论；调度与决策 | 代数；进阶需微积分与线性代数 |
| [理论计算机科学与信息数学](14-computation/index.html) | 算法与复杂性；自动机；可计算性；信息论；编码理论；密码学 | 逻辑、组合、概率 |
| [数学物理](15-mathematical-physics/index.html) | 经典力学；流体与连续介质；电磁与光学；热与统计物理；量子数学；相对论与场论 | 微积分、线性代数、微分方程 |
| [数学建模与交叉应用](16-modeling/index.html) | 模型与验证；生物数学；经济与金融数学；网络与社会系统；系统科学；数据建模 | 代数；需 06 导数与 11 微分方程基础 |
| [数学史、哲学与数学素养](17-history/index.html) | 数系扩张；证明观念；公理方法；无穷；数学哲学；数学教育与交流 | 好奇心、基础代数 |

## 推荐学习路径

1. 若分数、百分数、函数尚不熟悉，从 00 开始；否则先做首页诊断题。
2. 第一条主线：00 预备 → 01 基础与证明 → 02 初等代数 → 04 线性代数、05 几何 → 06 微积分。
3. 离散支线：01 → 03 数论、08 组合图论 → 14 计算与信息。
4. 不确定性支线：00、01 → 09 概率 → 10 统计；进阶概率需 06 的测度论。
5. 连续与应用支线：04、06 → 11 微分方程 → 12 数值、13 优化 → 15 数学物理、16 建模。
6. 抽象方向：01、02、06 → 07 拓扑；再进入代数几何、泛函分析等。17 数学史与哲学可穿插阅读。

这里的先修指入门课；研究级子领域需要更长准备。例如代数几何需要抽象代数与拓扑，随机分析需要测度概率与实分析。

## 每课怎样学

用 15–25 分钟完成一课：读直觉 → 手推例题 → 独立写练习 → 看解析 → 用自己的话复述。次日、3 天后、7 天后不看答案重做；复习时混合一个旧分支的题。每周建议 3 次学习、1 次复习，速度以能解释为准。

[交互实验室](reference/labs.html) 提供割线趋近切线、线性变换面积、二项分布、步长稳定性、抽样分布、牛顿迭代与特征值椭圆七个实验；每个实验都有预测问题与解释。[符号速查](reference/glossary.html) 用于随时复习；学完一课后到[核心概念清单](reference/concepts.html)逐项勾选自评。

## 当前内容与边界

当前版本共有 18 个模块、139 节中文入门短课，每课包含概念、推导例题、练习及折叠解析。每个模块都有子领域路线。它是一套可以马上开始的全景入门课程，**不是所有子领域的完整教材**；路线中的高阶主题尚未展开。学习记录初始为空，不会假定你已经掌握任何内容。练习输入不保存，也不自动判定证明是否正确。

## 教材设计与维护

先检索并读完 [teach skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md)，借鉴短课、反馈、间隔检索与学习记录设计。此处按用户要求把课程放在各分支目录内。skill 只在本次读取使用，没有全局安装。

- [学习使命](MISSION.md)、[教学偏好](NOTES.md)、[资料来源](RESOURCES.md)、[维护清单](CHECKLIST.md)。
- `learning-records/` 保存你日后提交的真实学习反馈。
- `assets/` 保存共享样式、脚本与课程数据。
- 修改 `tools/build_course.py` 后运行 `python tools/build_course.py` 可重建课程；不要同时手动修改生成的课程页面。

## MSC2020 全部 63 个二位大类对照

为避免遗漏，下面列出研究分类的全部二位大类，映射到本课程文件夹。**对照代表路线覆盖，不代表这些研究领域已各有完整课程。** 例如K理论、李群、特殊函数、天体物理均是待扩展方向。00是综合类而非单一研究分支。中文标题为便于学习的简译。

| MSC | 领域 | 对应文件夹 |
|---|---|---|
| 00 | 综合与总论 | [数学史、哲学与数学素养](17-history/index.html) |
| 01 | 数学史与传记 | [数学史、哲学与数学素养](17-history/index.html) |
| 03 | 数理逻辑与基础 | [数学基础与证明](01-foundations/index.html) |
| 05 | 组合数学 | [组合数学与图论](08-combinatorics/index.html) |
| 06 | 序、格与有序代数结构 | [代数与结构](02-algebra/index.html) |
| 08 | 一般代数系统 | [代数与结构](02-algebra/index.html) |
| 11 | 数论 | [数论](03-number-theory/index.html) |
| 12 | 域论与多项式 | [代数与结构](02-algebra/index.html) |
| 13 | 交换代数 | [代数与结构](02-algebra/index.html) |
| 14 | 代数几何 | [几何学](05-geometry/index.html) |
| 15 | 线性与多重线性代数、矩阵 | [线性代数](04-linear-algebra/index.html) |
| 16 | 结合环与代数 | [代数与结构](02-algebra/index.html) |
| 17 | 非结合环与代数 | [代数与结构](02-algebra/index.html) |
| 18 | 范畴与同调代数 | [代数与结构](02-algebra/index.html) |
| 19 | K理论 | [代数与结构](02-algebra/index.html) |
| 20 | 群论及推广 | [代数与结构](02-algebra/index.html) |
| 22 | 拓扑群与李群 | [代数与结构](02-algebra/index.html) |
| 26 | 实函数 | [微积分与数学分析](06-analysis/index.html) |
| 28 | 测度与积分 | [微积分与数学分析](06-analysis/index.html) |
| 30 | 单复变函数 | [微积分与数学分析](06-analysis/index.html) |
| 31 | 位势论 | [微积分与数学分析](06-analysis/index.html) |
| 32 | 多复变与解析空间 | [微积分与数学分析](06-analysis/index.html) |
| 33 | 特殊函数 | [微积分与数学分析](06-analysis/index.html) |
| 34 | 常微分方程 | [微分方程与动力系统](11-differential-equations/index.html) |
| 35 | 偏微分方程 | [微分方程与动力系统](11-differential-equations/index.html) |
| 37 | 动力系统与遍历理论 | [微分方程与动力系统](11-differential-equations/index.html) |
| 39 | 差分与函数方程 | [微分方程与动力系统](11-differential-equations/index.html) |
| 40 | 序列、级数与可和性 | [微积分与数学分析](06-analysis/index.html) |
| 41 | 逼近与展开 | [微积分与数学分析](06-analysis/index.html) |
| 42 | 欧氏空间调和分析 | [微积分与数学分析](06-analysis/index.html) |
| 43 | 抽象调和分析 | [微积分与数学分析](06-analysis/index.html) |
| 44 | 积分变换与算子演算 | [微积分与数学分析](06-analysis/index.html) |
| 45 | 积分方程 | [微分方程与动力系统](11-differential-equations/index.html) |
| 46 | 泛函分析 | [微积分与数学分析](06-analysis/index.html) |
| 47 | 算子理论 | [微积分与数学分析](06-analysis/index.html) |
| 49 | 变分、最优控制与优化 | [优化、运筹与控制](13-optimization/index.html) |
| 51 | 几何 | [几何学](05-geometry/index.html) |
| 52 | 凸与离散几何 | [几何学](05-geometry/index.html) |
| 53 | 微分几何 | [几何学](05-geometry/index.html) |
| 54 | 一般拓扑 | [拓扑学](07-topology/index.html) |
| 55 | 代数拓扑 | [拓扑学](07-topology/index.html) |
| 57 | 流形与胞腔复形 | [拓扑学](07-topology/index.html) |
| 58 | 整体分析与流形上的分析 | [微积分与数学分析](06-analysis/index.html) |
| 60 | 概率与随机过程 | [概率论](09-probability/index.html) |
| 62 | 统计 | [统计学](10-statistics/index.html) |
| 65 | 数值分析 | [数值分析与科学计算](12-numerical/index.html) |
| 68 | 计算机科学 | [理论计算机科学与信息数学](14-computation/index.html) |
| 70 | 质点与系统力学 | [数学物理](15-mathematical-physics/index.html) |
| 74 | 可变形固体力学 | [数学物理](15-mathematical-physics/index.html) |
| 76 | 流体力学 | [数学物理](15-mathematical-physics/index.html) |
| 78 | 光学与电磁理论 | [数学物理](15-mathematical-physics/index.html) |
| 80 | 经典热力学与传热 | [数学物理](15-mathematical-physics/index.html) |
| 81 | 量子理论 | [数学物理](15-mathematical-physics/index.html) |
| 82 | 统计力学与物质结构 | [数学物理](15-mathematical-physics/index.html) |
| 83 | 相对论与引力 | [数学物理](15-mathematical-physics/index.html) |
| 85 | 天文与天体物理 | [数学物理](15-mathematical-physics/index.html) |
| 86 | 地球物理 | [数学物理](15-mathematical-physics/index.html) |
| 90 | 运筹与数学规划 | [优化、运筹与控制](13-optimization/index.html) |
| 91 | 博弈、经济、金融与社会行为科学 | [数学建模与交叉应用](16-modeling/index.html) |
| 92 | 生物与其他自然科学 | [数学建模与交叉应用](16-modeling/index.html) |
| 93 | 系统与控制 | [优化、运筹与控制](13-optimization/index.html) |
| 94 | 信息通信与电路 | [理论计算机科学与信息数学](14-computation/index.html) |
| 97 | 数学教育 | [数学史、哲学与数学素养](17-history/index.html) |


## 完整分类与从基础到研究的课程规划

- [完整 MSC2020 分类索引](reference/classification.html)：收入官网下载 CSV 的全部 **6,603 条编码记录**，包含63个大类、534个中类、5,503个专题末级条目和503个通用末级条目；已与官方 TeX 的全部标签集合核对一致。保留英文专业名，可离线搜索编码或关键词。分类名称完整收录不等于对应教程已经完成。
- **计数说明**：[官网介绍](https://msc2020.org/)写63个大类、529个中类、6,022个末级类；当前下载文件实测计数不同。本项目报告源文件实测结果，未自行补造分类。审计结果在 `assets/classification-audit.json`。
- [分级课程总纲](reference/curriculum.html)：每个模块都有 L0 入门、L1 本科核心、L2 高阶与证明、L3 研究生专题、L4 研究训练的目标与验收要求。以上是**待展开的教学规划**，现有正文仍为139节。
- [核心概念自查清单](reference/concepts.html)：139 节课逐项“能解释 / 能推导 / 能迁移”自评，勾选进度仅保存在本机浏览器（localStorage）。
- 研究训练意味着在特定方向读论文、复现证明或算法、提出问题和接受反馈。没有覆盖全部数学的“大师结业线”，读完资料也不能保证原创研究能力。

重建：先运行 `python tools/build_course.py`，再运行 `python tools/extend_atlas.py`；验证先 `pip install -r requirements.txt`，再运行 `python tools/verify_course.py`（需要 Playwright 与本机 Chrome/Chromium）。分级课程内容在 `tools/extend_atlas.py` 中维护；`MISSION.md`、`NOTES.md`、`RESOURCES.md`、`assets/concepts.json`（概念清单数据）与 `learning-records/` 为手工维护文档，重建不会覆盖。
