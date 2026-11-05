from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1]
# 每个单元：标题、直觉与定义、推导例题、练习、解析。
data=[
('01-foundations','数学基础与证明','整数、分数与比例；集合与映射；命题逻辑；证明方法；集合论、公理与可计算性','四则运算','discrete',[
('全称命题与反例','数学里的“所有”是一项很强的承诺。命题“对每个整数 n，n²+n 是偶数”用 ∀ 表示全称；要推翻它，只需找出一个反例；验证很多例子却不能证明它。','n²+n=n(n+1)。相邻两个整数必有一个为偶数，所以乘积为偶数。这解释了无穷多个情形，而非只检查几个数。','“每个素数都是奇数”对吗？如何修正？','不对：2 是素数且是偶数。修正为“每个大于 2 的素数都是奇数”。大于 2 的偶数有因子 2，故不是素数。'),
('归纳法像一排多米诺骨牌','归纳法有两个不可省略的步骤：起点成立；对任意 k，若第 k 项成立，则第 k+1 项成立。它用于自然数索引的命题。','证明 1+…+n=n(n+1)/2。n=1 成立。假设 k 时成立，再加 k+1，得到 k(k+1)/2+(k+1)=(k+1)(k+2)/2，正好是下一项。','证明前 n 个正奇数之和为 n²。','起点 1=1²。若前 k 项和为 k²，再加第 k+1 个奇数 2k+1，就得 (k+1)²。只写出结果而没有假设和推进步骤，还不是完整归纳证明。')]),
('02-algebra','代数与结构','初等代数；多项式；群论；环论；域论；交换代数；表示论；范畴论与同调代数','分数、等式与基础证明','discrete',[
('等式变形为何要检查条件','解方程是在寻找使等式成立的输入。可逆变形保持解集；不可逆变形可能引入或丢失解。除以一个式子前必须确认它非零。','x²=x 可写为 x(x−1)=0，于是 x=0 或 x=1。若直接两边除以 x，只会留下 x=1，漏掉零解。','解 (x−2)(x+3)=0，并解释为什么能分成两个方程。','在实数中，两个非零数的乘积非零，所以积为零至少有一个因子为零。解为 2 和 −3。这个性质不能无条件推广到任意代数结构。'),
('群：把对称当作运算','群由一个集合和一种运算组成，满足封闭、结合律、单位元和逆元。它抽象了“做一个动作，再做一个动作”。群不要求交换律。','正三角形绕中心旋转 0°、120°、240°形成一个群。120°接着240°等于360°，对应单位动作。每个旋转都有能撤销它的旋转。','只保留 0° 和 120°，还能构成旋转群吗？','不能。120°与120°复合成240°，不在集合内，违反封闭性。研究结构时先检查集合与运算，而非只数元素。')]),
('03-number-theory','数论','整除与同余；素数；丢番图方程；解析数论；代数数论；算术几何','整数、代数与证明','discrete',[
('欧几里得算法','最大公约数是两个整数共有的最大正因子。关键事实是 gcd(a,b)=gcd(b,a−qb)，因为两组数的公因子完全相同。','48=2×18+12，18=1×12+6，12=2×6。最后一个非零余数是6，因此 gcd(48,18)=6。每次余数变小，过程最终结束。','计算 gcd(84,30)，并解释余数变换为什么可靠。','84=2×30+24，30=24+6，24=4×6，故为6。若 d 同时整除 a,b，也整除 a−qb；反过来同样成立。'),
('同余：只看除法余数','a≡b (mod m) 表示 m 整除 a−b，其中 m 为正整数。同余适合表达时钟和周期，能相加相乘，但约分需要条件。','17≡5 (mod 12)，因此17小时后与5小时后落在同一个钟点。在模6下，2×1≡2×4，却不能除以2得到1≡4。','求 7 的100次方除以10的余数。','7¹,7²,7³,7⁴ 的末位依次为7,9,3,1，每4次循环。100是4的倍数，所以余数为1。')]),
('04-linear-algebra','线性代数','线性方程组；向量空间；线性映射；矩阵；特征值；内积与谱分解；多重线性代数','初等代数、坐标平面','linear',[
('线性组合与张成','向量既可看成箭头，也可看成有序数据。av+bw 是线性组合。所有线性组合组成张成空间；这回答“这些方向能到达哪里”。','v=(1,0)，w=(0,1)。任意(x,y)=xv+yw，故它们张成平面。如果 w=(2,0)，所有组合都在横轴上，不能到达(0,1)。','(1,1) 与 (2,2) 能张成平面吗？用一个到不了的点说明。','不能。组合总为(a+2b,a+2b)，两坐标相等，到不了(1,0)。它们线性相关，第二个方向没有增加自由度。'),
('行列式作为面积倍率','二维矩阵 A 的两列是两个基向量变换后的位置。det(A)=ad−bc 是有向面积倍率；绝对值是面积缩放，符号记录方向。','A=diag(2,3) 把单位正方形变成宽2高3的矩形，行列式为6。若两列平行，图形压成一条线，面积为0，变换不可逆。','矩阵的两列是(1,2)和(2,4)，能否从输出唯一恢复输入？','不能，行列式1×4−2×2=0。第二列是第一列的两倍，例如输入(2,0)与(0,1)输出相同。')]),
('05-geometry','几何学','欧氏几何；解析几何；射影几何；微分几何；黎曼几何；代数几何；凸几何','代数、坐标与基础证明','pre',[
('距离如何变成方程','平面两点的欧氏距离由勾股定理给出：d²=(x₂−x₁)²+(y₂−y₁)²。坐标把形状约束翻译成代数。','到原点距离为 r 的点满足 x²+y²=r²，这就是圆。中心移到(a,b)，则变成(x−a)²+(y−b)²=r²。','写出中心(2,−1)、半径3的圆方程，并判断(5,−1)是否在圆上。','(x−2)²+(y+1)²=9。代入(5,−1)得9+0=9，因此在圆上。'),
('曲率：局部转弯有多急','直线不转弯；圆处处以相同程度转弯。半径 R 的圆曲率是1/R。对光滑平面曲线，曲率描述单位弧长上切线方向的变化率。','半径2与半径10的圆曲率分别为1/2与1/10。大圆的一小段更像直线。一般曲线要用微积分定义曲率，不能只凭视觉判断。','半径变为原来的3倍，圆的曲率怎样改变？','κ新=1/(3R)=κ旧/3。曲率单位是长度的倒数，不是长度或面积。')]),
('06-analysis','微积分与数学分析','函数与极限；微分；积分；实分析；复分析；测度论；调和分析；泛函分析；非标准分析','函数、代数、坐标','calculus',[
('导数是局部变化率','平均变化率是 Δy/Δx。固定起点 x，让增量 h 趋近0，若比值极限存在，就是导数 f′(x)。它是曲线局部线性近似的斜率。','f(x)=x² 时，[f(x+h)−f(x)]/h=2x+h（h≠0）。令h趋近0得 f′(x)=2x。x=1处斜率是2，而不是函数值1。','不用直接套公式，求 f(x)=3x+2 在任意 x 的导数。','差商=[3(x+h)+2−(3x+2)]/h=3。极限为3。函数值随位置变化，斜率却恒定。'),
('积分把局部量累积起来','定积分可从许多小矩形的有向面积之和的极限理解。对连续函数，若 F′=f，则从 a 到 b 的积分为 F(b)−F(a)。','∫₀² x dx=[x²/2]₀²=2，也等于底2高2三角形的面积。曲线在横轴下方时定积分计负值。','∫₋₁¹ x dx 是多少？它是否等于曲线与横轴围成的总面积？','定积分为0，因为左右正负抵消。总几何面积为1，需要积分 |x|。面积直觉必须区分有向与无向。')]),
('07-topology','拓扑学','点集拓扑；连续与同胚；紧致性；连通性；代数拓扑；微分拓扑；几何拓扑','集合、映射；进阶需分析和代数','topology',[
('同胚：保留连续结构','同胚是连续双射且逆映射也连续。它保留拓扑结构，却不要求保留距离和角度。橡皮形变只是直觉，严格判断依靠映射。','实数直线到正实数的 f(x)=eˣ 是同胚：它连续且一一对应，逆映射 ln(x) 也连续。两个集合长度的直觉完全不同，拓扑结构却相同。','f(x)=2x 能证明实数直线与自身同胚吗？列出需要核对的条件。','可以。它是双射、连续，逆映射 x/2 也连续。只验证双射不够。'),
('连通：不能拆成两块','拓扑意义的连通指空间不能写为两个不交、非空、相对开集的并。在实数里区间是连通的。它比“图上看起来连着”更精确。','集合(0,1)∪(2,3) 可直接拆成这两个非空开部分，因此不连通。连续映射将连通空间送到连通集合，这是介值现象的背景。','连续函数在区间上取到值−1与1，能否跳过0？','不能。介值定理保证中间至少有一点取值0。若定义域不是区间，或函数不连续，这个结论可能失效。')]),
('08-combinatorics','组合数学与图论','计数；递推；生成函数；图论；极值组合；设计理论；离散几何','整数与基础证明','discrete',[
('计数时先问顺序是否重要','从 n 个不同对象中无放回选 k 个，有顺序时是 n!/(n−k)!；无顺序时每组被重复计数k!次，故组合数 C(n,k)=n!/[k!(n−k)!]。','5人选2人担任不同职务，有5×4=20种；只选2人组成小组则20/2=10种。差别来自同一组的两种排列。','6人中选3人小组有多少种？如果设队长、副队长和记录员呢？','小组 C(6,3)=20；三个不同职务为6×5×4=120。前提都是每人最多入选一次。'),
('握手引理','图由顶点和边组成。无向图中顶点度数是与它相接的边端数。每条边贡献两个端点，因此所有度数之和等于2倍边数。','若一个图度数依次为3,2,2,1，度数和8，边数必为4。奇度顶点的个数必为偶数，否则总和为奇数。','可能有一个无向图，其度数为3,3,3,2吗？','不可能。度数和为11，不是偶数。这是必要条件；度数和为偶数并不保证任意度数序列都可实现。')]),
('09-probability','概率论','概率空间；条件概率；随机变量；分布；大数定律；极限定理；随机过程；随机分析','分数、集合；进阶需分析','statistics',[
('条件概率改变了样本空间','在已知 B 发生时，P(A|B)=P(A∩B)/P(B)，要求P(B)>0。直觉是把注意力缩小到B，再看其中有多少属于A。','公平骰子已知点数是偶数，可能结果是{2,4,6}。其中大于3的有4与6，所以条件概率为2/3，而非原来的1/2。','公平骰子已知大于3，点数为偶数的概率是多少？','可能结果{4,5,6}，其中{4,6}为偶数，故2/3。条件必须先处理，再计数。'),
('独立与互斥不同','独立意味着 P(A∩B)=P(A)P(B)；互斥意味着交集为空。两个概率均为正的互斥事件不可能独立。','一次掷骰子的“出现1”和“出现2”互斥；交集概率0，但概率乘积为1/36，所以不独立。两次独立投币的正面事件则可以同时发生。','两次独立公平投币，至少一次正面的概率是多少？','反面事件是两次均反面，概率1/4，因此所求3/4。不能把1/2+1/2直接当答案，因为两次正面被重计。')]),
('10-statistics','统计学','描述统计；抽样；参数估计；假设检验；回归；贝叶斯统计；实验设计；多元与非参数统计','概率、代数','statistics',[
('平均数会隐藏什么','平均数是总和除以个数；中位数是排序后的中间位置。它们回答不同问题。描述一组数据还应看离散程度、异常值和抽样方式。','收入数据1,2,3,4,90，均值20，中位数3。多数人都远低于均值，说明单个中心指标不足以描述分布。','把90改成900，中位数与平均数各如何变化？','中位数仍为3，平均数变为182。中位数对单个极端值更稳健；这不意味着任何场景都应舍弃均值。'),
('相关不能独自证明因果','两个量同时变化，可能由因果、共同原因或选择机制导致。随机对照试验通过随机分配，尽量平衡混杂因素；仍需检查执行与样本。','夏天冰淇淋销量与溺水人数可能一起上升。温度使人们更常买冰淇淋和游泳，是共同原因。仅凭相关就禁止冰淇淋并不能推出会减少溺水。','喝咖啡的人考试成绩更高，能直接推断咖啡提高成绩吗？','不能。学习时间、睡眠、样本选择等都可能混杂。先明确因果问题，再考虑随机试验或合适的观察研究设计。')]),
('11-differential-equations','微分方程与动力系统','常微分方程；偏微分方程；积分方程；差分方程；稳定性；分岔；混沌；遍历理论','导数、积分；系统需线性代数','ode',[
('从变化规律到指数增长','y′=ky 表示变化速率正比于当前数量。给定初值 y(0)=y₀，解为 y=y₀eᵏᵗ。方程描述规律，初值选择具体轨迹。','取k=0.1且y₀=100，则y(t)=100e⁰·¹ᵗ。验证时求导得到10e⁰·¹ᵗ，恰是0.1y，并检查t=0时为100。','y′=−2y，y(0)=3 的解是什么？长期如何变化？','y=3e⁻²ᵗ。随t趋于正无穷它趋于0，但在任何有限时刻仍为正。模型可能不适合离散的少量个体。'),
('平衡点不等于稳定点','自治方程 y′=f(y) 的平衡点满足 f(y*)=0。稳定性研究稍微偏离后会怎样，不是只看能否停在那里。','y′=y(1−y) 的平衡点是0和1。0<y<1时向上，y>1时向下，因此正半轴附近轨迹趋向1；0的小正扰动则远离0。','对 y′=−y，0是吸引还是排斥平衡点？用解解释。','吸引。y(t)=y(0)e⁻ᵗ，从正负两边都趋向0。这个判断以正向时间演化为准。')]),
('12-numerical','数值分析与科学计算','误差；插值与逼近；数值线性代数；数值积分；方程求根；微分方程数值解；计算可靠性','代数、微积分','calculus',[
('二分法为何可靠','连续函数在区间两端异号时至少有一个零点。二分法保留异号的一半。它不承诺唯一零点，但每步都把包围区间长度减半。','对 f(x)=x²−2，从[1,2]开始。中点1.5函数值0.25为正，保留[1,1.5]；再取1.25，值为负，保留[1.25,1.5]。','初始区间长1，二分10次后区间多长？中点误差上界是多少？','区间长1/1024，中点距离区间内任一根最多1/2048。必须保证连续性和保留区间内有根。'),
('欧拉法是局部直线预测','求解 y′=f(t,y) 时，用 yₙ₊₁=yₙ+h f(tₙ,yₙ) 前进一步。这是切线近似，步长与稳定性都会影响结果。','y′=y，y(0)=1，步长0.5时，两步得到1.5、2.25；精确y(1)=e≈2.718。局部估计会累积误差。','对 y′=−2y，用h=1和h=0.25，单步倍率分别多少？说明什么？','倍率分别是−1与0.5。前者产生不衰减振荡，后者衰减。精确解始终指数衰减，所以步长过大会改变定性行为。')]),
('13-optimization','优化、运筹与控制','凸优化；线性规划；整数规划；变分法；最优控制；博弈论；调度与决策','代数；进阶需微积分与线性代数','calculus',[
('最优值取决于可行域','优化问题由变量、目标函数和约束组成。目标再好，违反约束也不是候选解。局部最优只和附近比，全局最优和所有可行点比。','在0≤x≤5下最小化(x−3)²，最优点为3；若约束改成0≤x≤2，最优点变为2。无约束驻点未必可行。','在0≤x≤1下最小化(x−2)²，答案是什么？','x=1，目标值1。因为区间内x越靠近2，平方距离越小。机械地令导数为0会得到不可行点2。'),
('梯度下降为何会过冲','对可微函数，梯度给出局部上升最快方向；下降迭代 x新=x−ηf′(x)，η为正步长。它不是对所有函数都保证全局最优的魔法。','f(x)=x²时迭代为x新=(1−2η)x。若0<η<1，绝对倍率小于1，故趋向0；η=1时只来回跳；η>1则通常发散。','η=0.25、x₀=4，前两次迭代是多少？','倍率1/2，所以x₁=2、x₂=1。函数值从16降为4再降为1。收敛条件来自这个具体二次函数。')]),
('14-computation','理论计算机科学与信息数学','算法与复杂性；自动机；可计算性；信息论；编码理论；密码学','逻辑、组合、概率','discrete',[
('算法复杂度看增长','复杂度描述输入规模变大时资源怎样增长。O(n)是渐近上界，不是精确秒数；分析时要说明最坏、平均还是其他情形。','有序数组二分搜索每次把候选数量减半。n=1024时约10次缩减就剩1项，体现对数增长；无序逐项搜索最坏要看全部n项。','输入规模翻倍，线性算法与平方算法的主导工作量分别约变几倍？','分别约2倍和4倍，前提是比较主导项且规模足够大。实际运行还受常数、硬件和输入影响。'),
('信息量与惊讶程度','概率p事件的自信息为−log₂p，比特为单位。罕见事件发生时带来更多信息；熵是自信息的概率加权平均。','公平硬币每个结果的信息量1比特，熵1。确定性结果概率1，信息量为0。二元变量p=1/2时熵最大，越偏向一个结果越可预测。','四个等概率结果，观察一个结果有多少比特的信息？','−log₂(1/4)=2比特。它对应区分四种结果需要两次理想二元选择。')]),
('15-mathematical-physics','数学物理','经典力学；流体与连续介质；电磁与光学；热与统计物理；量子数学；相对论与场论','微积分、线性代数、微分方程','ode',[
('守恒量连接局部与整体','无阻尼弹簧满足 m x″=−kx。动能与势能之和 E=mx′²/2+kx²/2 是守恒量。这里假设m,k为正常数且没有外力。','对E求导得 E′=mx′x″+kxx′=x′(mx″+kx)=0。方程让括号为零，于是能量不变。这是从运动规律推导守恒，而非额外猜测。','加入阻尼 c x′（c>0）后，能量变化率是什么？','方程mx″+cx′+kx=0，代入得到E′=−cx′²≤0。机械能耗散，不能再沿用无阻尼的守恒结论。'),
('量纲分析先检查公式是否可能','物理等式两边的量纲必须一致。量纲正确不保证公式正确，但量纲错误足以否决它。长度L、时间T、质量M可以组合。','速度量纲L/T，加速度L/T²。自由落体位移的候选式gt量纲L/T，不是长度；gt²量纲L，至少通过量纲检查，系数仍需动力学确定。','弹簧周期可能正比√(m/k)吗？已知F=kx。','k的量纲是(M L/T²)/L=M/T²，故√(m/k)量纲T。它通过检查；完整周期2π√(m/k)需要解方程。')]),
('16-modeling','数学建模与交叉应用','模型与验证；生物数学；经济与金融数学；网络与社会系统；系统科学；数据建模','代数、概率；进阶需微分方程','ode',[
('模型必须写出假设','模型是为特定问题保留关键机制的简化。应声明变量、单位、参数、假设、适用范围，并用新数据检查；拟合好不等于机制正确。','用人口模型N′=rN隐含人均增长率恒定、资源不限制等假设。它可能适合短期，却会在长期预测无限增长。资源有限时可考虑逻辑斯谛模型。','若用“距离=速度×时间”预测通勤，需要哪些假设？','速度应是全程平均速度，或假设匀速；还应明确是否包含等待、绕路。参数应从对应路线和时段估计，并检查预测误差。'),
('灵敏度：参数错一点会怎样','模型输出常依赖不确定参数。灵敏度分析固定其他条件，改变一个参数，观察输出变化；它揭示最值得测准的量。','复利模型A=P(1+r)ⁿ（每期利率恒定）。P翻倍使A翻倍；利率影响则会经过n期累积。长期外推对增长率假设尤其敏感。','当P=100、n=2时，r=0.1与0.2分别给出多少？能把它当收益保证吗？','分别121与144。不能，这是固定利率假设下的算术结果，现实收益率、费用和风险需要另外建模。')]),
('17-history','数学史、哲学与数学素养','数系扩张；证明观念；公理方法；无穷；数学哲学；数学教育与交流','好奇心、基础代数','discrete',[
('数系扩张是在修补运算边界','自然数适合计数，但3−5不在自然数内；整数容纳减法，有理数容纳非零数相除；实数补充极限结构；复数允许平方等于−1。','x²=2在有理数中无解，在实数中有±√2。x²+1=0在实数中无解，在复数中有±i。说“无解”必须说明在哪个数系。','x+3=1在自然数与整数中分别怎样？','自然数中无解，整数中解为−2。运算规则和解的集合依赖讨论的对象范围。'),
('公理、定义和定理分工不同','定义约定术语，公理给定体系的基本假设，定理由它们逻辑推出。证明有效性取决于前提，不能把图示或权威当成证明。','欧氏平面三角形内角和为180°；球面上的测地三角形可以超过180°。例如北极与赤道上相差90°的两点构成三个直角的球面三角形。','球面例子推翻欧氏几何了吗？','没有。它改变了空间与“直线”的含义，前提不相同。比较数学命题时要同时比较定义与假设。')])]
sources={
'discrete':('Oscar Levin：Discrete Mathematics — An Open Introduction','https://discrete.openmathbooks.org/dmoi4.html'),
'pre':('OpenStax：Precalculus 2e','https://openstax.org/details/books/precalculus-2e'),
'linear':('Jim Hefferon：Linear Algebra','https://hefferon.net/linearalgebra/'),
'calculus':('OpenStax：Calculus Volume 1','https://openstax.org/details/books/calculus-volume-1'),
'statistics':('OpenStax：Introductory Statistics 2e','https://openstax.org/details/books/introductory-statistics-2e'),
'ode':('MIT OCW：Differential Equations','https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/'),
 'topology':('MIT OCW：Introduction to Topology','https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/')}
# MISSION.md、NOTES.md、RESOURCES.md 与 learning-records/ 为手工维护文档，本脚本不再覆盖。
(root/'assets/sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
data.insert(0,('00-preparation','算术、函数与预备知识','数与运算；分数和比例；幂与对数；方程与不等式；函数；三角函数','四则运算；不会可从本页开始','pre',[
('函数是输入与输出的规则','函数为定义域中的每个输入指定唯一输出。定义域不是装饰：f(x)=1/x在实数中要排除0。图像把输入横放、输出竖放，便于看变化。','f(x)=2x+1时，输入3得到7。若问输出7对应什么输入，就解2x+1=7，得到3。函数求值和解方程是两个方向的问题。','f(x)=x²，f(−2)是多少？输出4是否只有一个输入？','f(−2)=4；输入2也得到4。每个输入输出唯一，不代表每个输出只有一个输入。'),
('比例变化与百分数','百分数是以100为分母的比例。增加20%意味着乘1.2，而非无条件加20；连续变化的基数会变。','100元先涨20%变120元，再降20%得到96元。两次百分比基数分别是100和120，不能直接抵消。','价格80元先降25%再涨25%，最后多少？','80×0.75×1.25=75元。一般先增r再减r，总倍率是1−r²。')]))
# 课程结构完整保存，以便扩展和重新生成。
(root/'assets/course.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
css='''*{box-sizing:border-box}body{margin:0;background:#f5f3ed;color:#203438;font:17px/1.85 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1000px;margin:auto;padding:35px 24px 80px}header{padding:36px 0;border-bottom:2px solid #b9c9c5}h1{font-size:clamp(30px,5vw,50px);line-height:1.3}h2{font-size:27px;margin-top:35px}h3{font-size:20px}a{color:#086a67;text-underline-offset:4px}nav{display:flex;gap:20px;flex-wrap:wrap}.tag{font-size:13px;letter-spacing:2px;color:#556260}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(265px,1fr));gap:18px}.card,article,.panel{background:#fffdf8;border:1px solid #d6dfd8;border-radius:12px;padding:24px;margin-top:18px}.formula{border-left:4px solid #c3773e;padding:16px 22px;background:#f3ede2}details{border-top:1px solid #d6dfd8;margin-top:14px;padding-top:12px}summary,button{cursor:pointer}button{font:inherit;border:1px solid #086a67;background:#086a67;color:white;padding:9px 18px;border-radius:6px}button:focus-visible,a:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid #bb6223;outline-offset:4px}textarea{width:100%;min-height:110px;padding:12px;font:inherit}input[type=range]{width:min(100%,440px)}svg{width:100%;height:auto;max-height:340px;background:#f4f7f4}output{display:block;font-variant-numeric:tabular-nums}.muted{color:#586967}footer{margin-top:45px;border-top:1px solid #bccbc4;padding-top:20px}li{margin:8px 0}@media print{body{background:white;color:black}main{max-width:none}button,input,textarea,.screen-only{display:none}article,.card,.panel{break-inside:avoid}details>*{display:block}a{color:black}}
'''
(root/'assets/style.css').write_text(css,encoding='utf-8')
def page(title,body,prefix='../'):
 home=f'<a href="{prefix}index.html">数学地图</a>' if prefix else ''
 return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · 数学理解课</title><link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/widgets.js"></script></head><body><main><nav>{home}<a href="{prefix}reference/glossary.html">符号速查</a><a href="{prefix}reference/labs.html">交互实验室</a></nav>{body}<footer>每课建议 15–25 分钟。先独立作答，再展开解析；次日、3 天后、7 天后闭卷重做。遇到不懂的步骤，可以把题目和你的推理发给我继续讲解。</footer></main></body></html>'
rows=[]; cards=[]
for folder,title,subs,pre,source,lessons in data:
 d=root/folder;d.mkdir(exist_ok=True);(d/'lessons').mkdir(exist_ok=True)
 links=''; plans=''
 for i,topic in enumerate(subs.split('；')):
  plans+=f'<li><b>{html.escape(topic)}</b>：'+(f'先掌握本分支 {len(lessons)} 节入门课的定义与例题。' if i==0 else '建议在前一阶段能解释定义并独立举例后学习。')+'</li>'
 for i,(name,concept,example,q,a) in enumerate(lessons,1):
  filename=f'{i:02}.html'; links+=f'<li><a href="lessons/{filename}">{i:02} · {name}</a></li>'
  nav=f'<a href="../index.html">返回分支路线</a>'
  if i>1:nav+=f' · <a href="{i-1:02d}.html">上一课</a>'
  if i<len(lessons):nav+=f' · <a href="{i+1:02d}.html">下一课</a>'
  # 按单元选择真正相关的教材；其他列为基础背景而非逐条引用。
  name_s,url=sources[source]
  body=f'<header><p class="tag">{title} / LESSON {i:02}</p><h1>{name}</h1><p>本课目标：用自己的话解释“{name.split("：")[0]}”，并独立完成下方迁移题。</p><p>先修：{pre}。先试读例题；若符号吃力，回到预备知识。</p></header><article><h2>先理解，再写符号</h2><p>{concept}</p><h2>一步步推导</h2><p class="formula">{example}</p><h2>停下来试一试</h2><p>{q}</p><label for="answer">写下答案和理由（此框不自动评分，也不保存）</label><textarea id="answer" placeholder="先写推理，再看解析。"></textarea><details><summary>查看解析与自评标准</summary><p>{a}</p><p>自评：结论是否正确？是否交代条件？能否不看例题解释关键步骤？只记住答案还需重做。</p></details><h2>闭卷回想</h2><p>合上解析：写下本课的一个定义、例题里关键的一步，以及这个结论所需的条件。再把例题中的一个数字改掉重算。</p><p><a href="../../reference/labs.html">到实验室探索相关图形</a>，将观察写成猜想，再用定义验证。</p><h2>延伸阅读</h2><p>基础背景：<a href="{url}">{name_s}</a>。这些英文原教材用于进一步核对定义；本课为独立中文讲解，不是原书译文。分支首页列出后续方向。</p></article><p>{nav}</p>'
  (d/'lessons'/filename).write_text(page(name,body,'../../'),encoding='utf-8')
 body=f'<header><p class="tag">BRANCH {folder[:2]} / 入门单元</p><h1>{title}</h1><p>先修：{pre}</p><p>本分支已有 {len(lessons)} 节可学习的入门课；下面的子领域是后续路线，尚未展开成完整专著。</p></header><h2>开始学习</h2><ol>{links}</ol><h2>子领域路线（由浅入深的建议顺序）</h2><ol>{plans}</ol><h2>学到什么程度再前进</h2><p>完成两课练习，能讲出每个结论的条件，并自己给出一个例子或反例。进阶子领域往往需要交叉先修，不能只按名称顺序硬读。</p><p><a href="../reference/labs.html">交互实验室</a> · <a href="../RESOURCES.md">拓展书目与分支来源</a></p>'
 (d/'index.html').write_text(page(title,body),encoding='utf-8')
 rows.append(f'| [{title}]({folder}/index.html) | {subs} | {pre} |')
 cards.append(f'<a class="card" href="{folder}/index.html"><span class="tag">{folder[:2]}</span><h2>{title}</h2><p>{subs}</p></a>')
readme=f'''# 数学理解课

目标：增强数学素养，理解概念为什么这样定义、结论为什么成立，并能用它们解释问题。

双击打开 [HTML 学习首页](index.html)。所有讲解、图形和交互均可离线使用，无需安装依赖；外部教材需要联网。推荐现代 Chrome、Edge 或 Firefox。

## 如何划分数学

数学没有唯一、公认且互不重叠的“全部主分支”清单。这里采用 **17 个学习方向 + 1 个预备模块**，覆盖基础、纯数学、计算与应用，并将相近研究领域归组。代数几何、随机分析等交叉领域可能属于多个方向；数学史与数学教育作为素养方向单列。此地图参考 [MSC2020](https://msc2020.org/) 的研究分类，但学习分组不是 MSC 官方分级。

## 分支与子领域

| 分支 / 教程入口 | 主要子领域 | 入门先修 |
|---|---|---|
'''+ '\n'.join(rows)+'''

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

[交互实验室](reference/labs.html) 提供割线趋近切线、线性变换面积、二项分布和步长稳定性实验；每个实验都有预测问题与解释。[符号速查](reference/glossary.html) 用于随时复习；学完一课后到[核心概念清单](reference/concepts.html)逐项勾选自评。

## 当前内容与边界

当前版本共有 {len(data)} 个模块、{sum(len(x[-1]) for x in data)} 节中文入门短课，每课包含概念、推导例题、练习及折叠解析。每个模块都有子领域路线。它是一套可以马上开始的全景入门课程，**不是所有子领域的完整教材**；路线中的高阶主题尚未展开。学习记录初始为空，不会假定你已经掌握任何内容。练习输入不保存，也不自动判定证明是否正确。

## 教材设计与维护

先检索并读完 [teach skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md)，借鉴短课、反馈、间隔检索与学习记录设计。此处按用户要求把课程放在各分支目录内。skill 只在本次读取使用，没有全局安装。

- [学习使命](MISSION.md)、[教学偏好](NOTES.md)、[资料来源](RESOURCES.md)、[维护清单](CHECKLIST.md)。
- `learning-records/` 保存你日后提交的真实学习反馈。
- `assets/` 保存共享样式、脚本与课程数据。
- 修改 `tools/build_course.py` 后运行 `python tools/build_course.py` 可重建课程；不要同时手动修改生成的课程页面。
'''
(root/'README.md').write_text(readme,encoding='utf-8')
body=f'<header><p class="tag">THE MATHEMATICS ATLAS</p><h1>从看懂公式，走向理解数学。</h1><p>{len(data)} 个模块 · {sum(len(x[-1]) for x in data)} 节入门短课 · 4 个交互实验</p><p>先建立直觉，再明确条件，用推导和练习检验理解。</p></header><section class="panel"><h2>从哪里开始？</h2><p>先闭卷回答：① 100 先涨20%再跌20%是多少？② x²=x 有哪些实数解？③ 骰子已知为偶数，大于3的概率是多少？</p><details><summary>核对答案与起点</summary><p>①96，不熟悉从00开始；②0和1，不熟悉从02开始并补01的证明；③2/3，不熟悉从09开始。三题只是定位起点，不能据此断言掌握整个分支。</p></details><p><a href="00-preparation/index.html">从预备知识开始 →</a>　<a href="reference/labs.html">打开交互实验室 →</a></p><p>建议路线：预备 → 证明 → 代数 → 线性代数 / 几何 → 微积分，再按兴趣选择概率、离散、拓扑或应用。</p></section><h2>数学的分支地图</h2><div class="grid">'+''.join(cards)+'</div>'
(root/'index.html').write_text(page('数学的分支地图',body,''),encoding='utf-8')
# MISSION.md、NOTES.md、RESOURCES.md、learning-records/ 为手工维护文档，重建时不再生成或覆盖。
terms=[('∀ / ∃','对所有 / 至少存在一个；交换量词顺序可能改变命题。'),('⇒ / ⇔','推出 / 等价；逆命题不自动成立。'),('∈ / ⊆','元素属于集合 / 集合包含于集合。'),('f: A → B','定义域为A、陪域为B的函数；实际取到的值组成像集。'),('lim / f′ / ∫','极限 / 导数 / 积分；使用前先检查存在条件。'),('向量 / 矩阵','向量描述数据或方向；矩阵表示给定基下的线性映射。'),('P(A|B)','在B发生条件下A的概率，要求P(B)>0。'),('定义 / 定理 / 猜想','术语约定 / 已由假设证明的结论 / 待证明或推翻的判断。'),('例子 / 反例','例子帮助理解；反例可推翻全称命题，有限个正例通常不能证明全称命题。')]
(root/'reference/glossary.html').write_text(page('数学符号与方法速查','<h1>数学符号与方法速查</h1>'+''.join(f'<article><h2>{a}</h2><p>{b}</p></article>' for a,b in terms)),encoding='utf-8')
(root/'reference/labs.html').write_text(page('交互实验室','''<header><p class="tag">EXPLORE → CONJECTURE → PROVE</p><h1>让概念动起来</h1><p>先预测，再拖动滑块。图像用于发现规律，推导用于解释为什么。</p></header>
<section class="panel" id="derivative"><h2>01 · 割线怎样趋近切线</h2><p>曲线 y=x²，固定点(1,1)，另一个点(1+h,(1+h)²)。预测：h趋近0时，割线斜率会趋近多少？</p><label for="h">增量 h（0.01–1）</label><input id="h" type="range" min="0.01" max="1" step="0.01" value="0.7"><output id="h-out" aria-live="polite"></output><svg id="derivative-svg" viewBox="0 0 600 320" role="img" aria-label="抛物线以及经过两个点的割线"></svg><p>差商=2+h，所以极限为2。这里滑块不能取0，因为差商在h=0时没有定义；导数是极限。蓝色是曲线，橙色是割线，虚线是切线。</p><a href="../06-analysis/lessons/01.html">回到导数课</a></section>
<section class="panel"><h2>02 · 行列式怎样缩放面积</h2><p>变换 A=diag(a,1)。预测：a=0或a为负数时，会发生什么？</p><label for="a">横向倍率 a（−2–2）</label><input id="a" type="range" min="-2" max="2" step="0.1" value="1.5"><output id="a-out" aria-live="polite"></output><svg id="linear-svg" viewBox="0 0 600 320" role="img" aria-label="单位正方形与线性变换后的矩形"></svg><p>虚线是原正方形。填色矩形面积=|a|，有向面积=a。a=0时压成线，负数时翻到另一侧。这个实验只演示对角矩阵，不代表一般矩阵只有缩放。</p><a href="../04-linear-algebra/lessons/02.html">回到行列式课</a></section>
<section class="panel"><h2>03 · 二项分布怎样改变形状</h2><p>独立重复投币10次，每次正面概率p。柱形表示恰好k次正面的理论概率，不是一次随机抽样。预测：p从0.5变到0.9时，峰往哪移？</p><label for="p">正面概率 p（0–1）</label><input id="p" type="range" min="0" max="1" step="0.01" value="0.5"><output id="p-out" aria-live="polite"></output><svg id="prob-svg" viewBox="0 0 600 320" role="img" aria-label="十次独立投币正面次数的概率分布"></svg><p>P(X=k)=C(10,k)pᵏ(1−p)¹⁰⁻ᵏ。期望=10p，方差=10p(1−p)。相同期望不意味着相同波动。p=0与p=1时分布集中在一个结果。</p><a href="../09-probability/lessons/02.html">回到独立性课</a></section>
<section class="panel"><h2>04 · 步长能改变系统的表现</h2><p>对 y′=−2y，y(0)=1，用欧拉法计算到t=10：y下一步=(1−2h)y。预测：h=1时，数值解还会衰减吗？</p><label for="step">步长 h（0.1–1.2）</label><input id="step" type="range" min="0.1" max="1.2" step="0.1" value="0.5"><output id="step-out" aria-live="polite"></output><svg id="euler-svg" viewBox="0 0 600 320" role="img" aria-label="欧拉数值解与精确指数衰减解的比较"></svg><p>蓝线是精确解，橙线是数值解。0&lt;h&lt;1时数值幅度衰减；h=1时振荡不衰减；h&gt;1时会发散。图的纵轴按数据自动缩放，请同时看上方数值。</p><a href="../12-numerical/lessons/02.html">回到数值方法课</a></section>'''),encoding='utf-8')
js='''"use strict";
const $=id=>document.getElementById(id);
function path(points,color,dash=''){return `<polyline points="${points.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="3" stroke-dasharray="${dash}"/>`;}
const axes=(x=65,y=270)=>`<path d="M25 ${y}H580M${x} 15V290" stroke="#5f7470" fill="none"/><text x="565" y="300">x</text>`;
function render(){
 if(!$('h'))return;
 let h=+$('h').value, pts=[];const xy=(x,y)=>[65+x*200,270-y*55];
 for(let x=0;x<=2.21;x+=.03)pts.push(xy(x,x*x));
 $('derivative-svg').innerHTML=axes()+path(pts,'#086a67')+path([xy(0,-1),xy(2.3,3.6)],'#697c78','6 5')+path([xy(.5,1-(2+h)*.5),xy(2,1+(2+h))],'#bd6029')+[xy(1,1),xy(1+h,(1+h)**2)].map(p=>`<circle cx="${p[0]}" cy="${p[1]}" r="5" fill="#bd6029"/>`).join('')+'<text x="280" y="220">固定点 (1,1)</text>';
 $('h-out').textContent=`h=${h.toFixed(2)}；割线斜率=${(2+h).toFixed(2)}；切线斜率=2`;
 let a=+$('a').value, x=300, y=250,s=90;
 $('linear-svg').innerHTML=axes(x,y)+`<rect x="300" y="160" width="90" height="90" fill="none" stroke="#677c77" stroke-dasharray="6 4"/><rect x="${Math.min(x,x+a*s)}" y="160" width="${Math.abs(a*s)}" height="90" fill="#147d7866" stroke="#086a67"/><text x="30" y="35">单位边长对应 90 像素</text>`;
 $('a-out').textContent=`a=${a.toFixed(1)}；det(A)=${a.toFixed(1)}；面积=${Math.abs(a).toFixed(1)}`;
 let p=+$('p').value, bars='',sum=0;function choose(n,k){let c=1;for(let j=1;j<=k;j++)c=c*(n-j+1)/j;return c;}
 for(let k=0;k<=10;k++){let v=choose(10,k)*p**k*(1-p)**(10-k);sum+=v;bars+=`<rect x="${40+k*48}" y="${270-v*230}" width="32" height="${v*230}" fill="#086a67"><title>k=${k}，概率=${v.toFixed(5)}</title></rect><text x="${45+k*48}" y="295">${k}</text>`;}
 $('prob-svg').innerHTML=bars+'<text x="30" y="25">概率（纵轴 0–1）；横轴：正面次数 k</text>';
 $('p-out').textContent=`p=${p.toFixed(2)}；期望=${(10*p).toFixed(2)}；方差=${(10*p*(1-p)).toFixed(2)}；概率和=${sum.toFixed(6)}`;
 let step=+$('step').value;if(!(step>0))step=0.1;let arr=[[0,1]],v=1;for(let j=1;j*step<=10+1e-9;j++){v*=1-2*step;arr.push([j*step,v]);}
 const scale=Math.max(1,...arr.map(x=>Math.abs(x[1]))),pos=(t,v)=>[45+t*52,155-v/scale*120];let exact=[];for(let t=0;t<=10;t+=.05)exact.push(pos(t,Math.exp(-2*t)));
 $('euler-svg').innerHTML=axes(45,155)+path(exact,'#086a67')+path(arr.map(([t,v])=>pos(t,v)),'#bd6029')+`<text x="40" y="25">纵轴范围约 ±${scale.toFixed(2)}；横轴 t=0…10</text>`;
 $('step-out').textContent=`h=${step.toFixed(1)}；单步倍率=${(1-2*step).toFixed(2)}；末步 t=${arr.at(-1)[0].toFixed(1)}，y≈${v.toFixed(5)}`;
}
for(const el of document.querySelectorAll('input[type=range]'))el.addEventListener('input',render);render();
// 打印时自动展开全部折叠解析，打印后还原（新版浏览器已不受 details>*{display:block} 影响）。
let printed=[];
addEventListener('beforeprint',()=>{printed=[...document.querySelectorAll('details:not([open])')];printed.forEach(d=>d.open=true)});
addEventListener('afterprint',()=>{printed.forEach(d=>d.open=false);printed=[]});
'''
(root/'assets/widgets.js').write_text(js,encoding='utf-8')
# RESOURCES.md 为手工维护文档（含分类数据署名），本脚本不再生成。
print('Built',len(data),'modules,',sum(len(x[-1]) for x in data),'lessons')
# MSC 二位大类对照用于核查地图覆盖范围；不把研究分类误当成教学顺序。
import csv
msc=[r for r in csv.DictReader((root/'assets/msc2020.csv').open(encoding='latin1'),delimiter='\t') if r['code'].endswith('-XX')]
groups={
'17-history':'00 01 97','01-foundations':'03','08-combinatorics':'05','02-algebra':'06 08 12 13 16 17 18 19 20 22',
'03-number-theory':'11','05-geometry':'14 51 52 53','04-linear-algebra':'15',
'06-analysis':'26 28 30 31 32 33 40 41 42 43 44 46 47 58',
'11-differential-equations':'34 35 37 39 45','13-optimization':'49 90 93',
'07-topology':'54 55 57','09-probability':'60','10-statistics':'62','12-numerical':'65',
'14-computation':'68 94','15-mathematical-physics':'70 74 76 78 80 81 82 83 85 86',
'16-modeling':'91 92'}
# 中文译名按编码显式映射，不依赖 CSV 行序；键集合与 CSV 大类严格核对，错配即报错。
cn={'00':'综合与总论','01':'数学史与传记','03':'数理逻辑与基础','05':'组合数学','06':'序、格与有序代数结构','08':'一般代数系统','11':'数论','12':'域论与多项式','13':'交换代数','14':'代数几何','15':'线性与多重线性代数、矩阵','16':'结合环与代数','17':'非结合环与代数','18':'范畴与同调代数','19':'K理论','20':'群论及推广','22':'拓扑群与李群','26':'实函数','28':'测度与积分','30':'单复变函数','31':'位势论','32':'多复变与解析空间','33':'特殊函数','34':'常微分方程','35':'偏微分方程','37':'动力系统与遍历理论','39':'差分与函数方程','40':'序列、级数与可和性','41':'逼近与展开','42':'欧氏空间调和分析','43':'抽象调和分析','44':'积分变换与算子演算','45':'积分方程','46':'泛函分析','47':'算子理论','49':'变分、最优控制与优化','51':'几何','52':'凸与离散几何','53':'微分几何','54':'一般拓扑','55':'代数拓扑','57':'流形与胞腔复形','58':'整体分析与流形上的分析','60':'概率与随机过程','62':'统计','65':'数值分析','68':'计算机科学','70':'质点与系统力学','74':'可变形固体力学','76':'流体力学','78':'光学与电磁理论','80':'经典热力学与传热','81':'量子理论','82':'统计力学与物质结构','83':'相对论与引力','85':'天文与天体物理','86':'地球物理','90':'运筹与数学规划','91':'博弈、经济、金融与社会行为科学','92':'生物与其他自然科学','93':'系统与控制','94':'信息通信与电路','97':'数学教育'}
assert set(cn)=={r['code'][:2] for r in msc},'MSC 大类编码与中文译名映射不一致，请核对 assets/msc2020.csv'
lookup={code:key for key,val in groups.items() for code in val.split()}
titles={x[0]:x[1] for x in data}
extra='\n## MSC2020 全部 63 个二位大类对照\n\n为避免遗漏，下面列出研究分类的全部二位大类，映射到本课程文件夹。**对照代表路线覆盖，不代表这些研究领域已各有完整课程。** 例如K理论、李群、特殊函数、天体物理均是待扩展方向。00是综合类而非单一研究分支。中文标题为便于学习的简译。\n\n| MSC | 领域 | 对应文件夹 |\n|---|---|---|\n'
for r in msc:
 code=r['code'][:2];folder=lookup[code]
 extra+=f'| {code} | {cn[code]} | [{titles[folder]}]({folder}/index.html) |\n'
(root/'README.md').write_text((root/'README.md').read_text(encoding='utf-8')+extra,encoding='utf-8')
# 将每个分支的完整分类范围写入首页，方便发现尚未展开的子领域。
for folder in groups:
 path=root/folder/'index.html';s=path.read_text(encoding='utf-8')
 names=[f'{code} · {cn[code]}' for code in sorted(cn) if lookup[code]==folder]
 insert='<section class="panel"><h2>研究方向补充索引</h2><p>以下为本文件夹归组的 MSC 大类，作为后续课程扩展范围；跨分支主题可同时查阅其他文件夹。</p><ul>'+''.join(f'<li>{n}</li>' for n in names)+'</ul></section>'
 s=s.replace('<h2>学到什么程度再前进</h2>',insert+'<h2>学到什么程度再前进</h2>');path.write_text(s,encoding='utf-8')
