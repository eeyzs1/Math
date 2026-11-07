"""Build the complete source-file classification index and staged curriculum.
The curriculum is a plan; it must never be counted as authored lessons.
"""
from pathlib import Path
import csv, re, json, html, collections
root=Path(__file__).resolve().parents[1]
E=html.escape
course=json.loads((root/'assets/course.json').read_text(encoding='utf-8'))
rows=list(csv.DictReader((root/'assets/msc2020.csv').open(encoding='latin1'),delimiter='\t'))
codes=[r['code'] for r in rows]
assert len(codes)==len(set(codes))
tex=(root/'assets/msc2020.tex').read_text(encoding='utf-8')
assert set(re.findall(r'\\label\{([^}]+)\}',tex))==set(codes)
major=[r for r in rows if re.fullmatch(r'\d{2}-XX',r['code'])]
middle=[r for r in rows if re.fullmatch(r'\d{2}[A-Z]xx',r['code'])]
general=[r for r in rows if re.fullmatch(r'\d{2}-\d{2}',r['code'])]
leaves=[r for r in rows if re.fullmatch(r'\d{2}[A-Z]\d{2}',r['code'])]
assert len(rows)==len(major)+len(middle)+len(general)+len(leaves)
count={'total':len(rows),'major':len(major),'middle':len(middle),'subject_leaf':len(leaves),'general_leaf':len(general)}
(root/'assets/classification-audit.json').write_text(json.dumps(count,indent=2),encoding='utf-8')

def page(title,body):
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><link rel="stylesheet" href="../assets/style.css"></head><body><main><nav><a href="../index.html">数学地图</a><a href="../reference/classification.html">完整分类</a><a href="../reference/curriculum.html">分级课程总纲</a><a href="../reference/concepts.html">核心概念</a></nav>{body}</main></body></html>'''

# Preserve official descriptions; no unverified machine-translated research vocabulary.
index='<header><p class="tag">MSC2020 / 完整源文件索引</p><h1>数学研究分类索引</h1><p>一级中文名称请对照 README；本页保留官方英文分类名与说明，避免把未经核对的专业术语翻译当成权威译名。</p></header>'
index+=f'''<section class="panel"><h2>范围与核对结果</h2><p>已逐条收入官方下载 CSV 的 {len(rows):,} 条记录，并核对 TeX 标签集合完全相同：{len(major)} 个大类、{len(middle)} 个中类、{len(leaves):,} 个专题末级条目和 {len(general)} 个通用末级条目。通用条目包括综述、历史、教材、软件等，不应被当成独立知识分支。</p><p>官网介绍页写的是 63 / 529 / 6,022；与当前下载文件的实际计数存在差异。本页采用下载文件的实际计数。这里的“完整”指所下载 CSV 与 TeX 的全部编码一致覆盖，不表示数学存在一份永远完备的分类。</p><p>分类索引不是已完成教程列表。现有教程正文仍为{sum(len(m[-1]) for m in course)}节；研究专题大多尚未编写。</p></section>'''
index+='''<section class="panel"><label for="search"><b>按编码或英文关键词筛选</b></label><input id="search" type="search" placeholder="例如 11A / prime / topology" style="display:block;width:100%;padding:12px;font:inherit"><output id="search-count" aria-live="polite">输入关键词可搜索全部条目</output><p>搜索会展开匹配条目。清空后可按大类、中类逐级浏览。浏览器查找时，请先展开相应大类。</p></section><div id="tree">'''
for m in major:
 prefix=m['code'][:2]
 index+=f'<details class="major panel" id="{m["code"]}"><summary><b>{m["code"]} · {E(m["text"])}</b></summary>'
 g=[r for r in general if r['code'].startswith(prefix)]
 index+='<details class="minor"><summary>通用条目：教材、综述、历史、软件等</summary>'
 for r in g:index+=f'<p class="entry" id="{r["code"]}"><b>{r["code"]}</b> {E(r["description"])}</p>'
 index+='</details>'
 for sub in [r for r in middle if r['code'].startswith(prefix)]:
  index+=f'<details class="minor" id="{sub["code"]}"><summary><b>{sub["code"]} · {E(sub["text"])}</b></summary>'
  for r in leaves:
   if r['code'].startswith(sub['code'][:3]):index+=f'<p class="entry" id="{r["code"]}"><b>{r["code"]}</b> {E(r["description"])}</p>'
  index+='</details>'
 index+='</details>'
index+=r'''</div><footer><p>来源：<a href="https://msc2020.org/">MSC2020</a>，Mathematical Reviews 与 zbMATH。<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>。本页将 CSV 重排为树状索引；保留原始英文内容，添加中文使用说明和计数审计。来源文件：<a href="../assets/msc2020.csv">CSV</a>、<a href="../assets/msc2020.tex">TeX</a>。</p></footer>
<script>
'use strict';const input=document.getElementById('search');let timer;
// 启动时一次性预索引小写文本，避免每次输入重新取 textContent（6600+ 条目）。
const majors=[...document.querySelectorAll('.major')].map(m=>({el:m,txt:m.querySelector('summary').textContent.toLowerCase(),subs:[...m.querySelectorAll('.minor')].map(s=>({el:s,txt:s.querySelector('summary').textContent.toLowerCase(),leaves:[...s.querySelectorAll('.entry')].map(e=>({el:e,txt:e.textContent.toLowerCase()}))}))}));
function filter(){const q=input.value.toLowerCase().trim();const exact=/^\d{2}[a-z]\d{2}$|^\d{2}-\d{2}$/.test(q);let matched=0;
for(const major of majors){
 const majorMatch=q&&major.txt.includes(q);let majorVisible=false;
 for(const sub of major.subs){
 const subMatch=q&&sub.txt.includes(q);let visible=false;
 for(const leaf of sub.leaves){const hit=exact?leaf.el.id.toLowerCase()===q:(!q||majorMatch||subMatch||leaf.txt.includes(q));leaf.el.hidden=!hit;if(hit){visible=true;matched++;}}
 sub.el.hidden=!visible;sub.el.open=!!q&&visible;majorVisible=majorVisible||visible;}
 major.el.hidden=!majorVisible;major.el.open=!!q&&majorVisible;}
 document.getElementById('search-count').textContent=q?`匹配 ${matched} 个末级条目（包括所属大类或中类名称匹配）`:'已显示所有分类，可逐级展开';}
input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(filter,120)});
function revealHash(){if(!location.hash)return;let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)))}catch(e){return}if(target){for(let p=target.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;if(target.tagName==='DETAILS')target.open=true;requestAnimationFrame(()=>target.scrollIntoView());}}
window.addEventListener('hashchange',revealHash);revealHash();
</script>'''
(root/'reference/classification.html').write_text(page('MSC2020 完整分类索引 · 数学理解课',index),encoding='utf-8')
# Every stage is a curriculum objective, not an automatically generated claim of mastery.
paths={
'00-preparation':[
'整数、有理数、四则运算与数量级；用单位和估算检查结果',
'分数、比例、百分数、幂、根式与对数；解释运算规则的适用条件',
'一次和二次方程、不等式、函数定义域、图像与复合；从文字问题列式',
'三角函数、弧度、恒等式、指数与对数函数；在符号、图像、语言间转换',
'综合衔接：量纲、极限直觉与向量；完成分析、线性代数入学诊断，转入专业主线'],
'01-foundations':[
'集合、映射、命题、量词与反例；区分逆、否与逆否命题',
'直接证明、反证、归纳、递归、等价关系与商集；写完整证明',
'朴素集合论、基数、可数性、关系与一阶语言；分清语法与语义',
'公理集合论、模型论、可计算性、形式证明；研究完备性与不完备性定理的假设',
'选择逻辑的一个专题研讨：重建定理证明、比较模型与方法；在导师反馈下提出小问题'],
'02-algebra':[
'等式变形、多项式、因式分解与复数；每次变形检查解集',
'群、子群、同态、商群；环、理想、商环；域扩张基础',
'群作用、Sylow理论、模、有限域、Galois理论；连接方程与对称',
'交换代数、表示论、范畴与同调代数；按方向补Noether条件、链复形和导出函子',
'选择表示论、交换代数或其他代数方向，复现专题论文的核心引理；K理论等另立长期专修路线'],
'03-number-theory':[
'整除、gcd、Euclid算法、同余、素数；给出基本论证',
'中国剩余定理、Fermat与Euler定理、乘法阶、二次剩余、简单丢番图方程',
'二次互反律、连分数、算术函数；补复分析与抽象代数后分流',
'解析方向：Dirichlet级数与素数分布；代数方向：数域、整数环、理想与局部域',
'选定解析数论或代数数论的小专题，重做已有结果；算术几何需额外补代数几何'],
'04-linear-algebra':[
'向量、线性组合、方程组、消元与矩阵；解释几何意义',
'向量空间、基、维数、核与像、秩零化度；用映射语言证明',
'行列式、特征值、对角化、内积、正交投影和最小二乘',
'谱定理、奇异值分解、Jordan标准形、张量与多重线性；区分精确代数与数值条件',
'选谱理论、矩阵分析或张量专题；复现结果并构造边界反例，连接泛函分析或数值分析'],
'05-geometry':[
'欧氏公理、相似、全等、圆与坐标；从图示走向证明',
'解析几何、仿射与射影观点、凸性；理解不同变换下的不变量',
'曲线曲面、曲率、流形与切空间；补多元微积分与拓扑',
'按方向选择黎曼几何与联络、代数几何与簇/概形、或凸几何；专修线之间不强求串行',
'选择一个几何专题：重建局部到整体的证明或一个具体例子；阅读现代论文并说明依赖条件'],
'06-analysis':[
'函数、极限、连续、导数、积分；从图形与数值建立直觉',
'实数完备性、数列与级数、严格极限、微积分定理；写ε-δ证明',
'多元微积分、度量空间、一致收敛、Lebesgue测度与积分、复分析',
'泛函分析、算子理论、Fourier与调和分析；按专题延伸特殊函数、位势或多复变',
'选择分析小专题，核对每个极限交换所需条件；复现一个非平凡定理及反例'],
'07-topology':[
'开闭集、连续、同胚、连通；在具体空间中作例子',
'度量空间、拓扑空间、紧致、积与商、分离性；避免只靠橡皮直觉',
'基本群、覆盖空间、同伦、同调；学习用代数不变量区别空间',
'上同调、流形、微分拓扑与几何拓扑；按方向补代数或微分几何',
'选定低维拓扑、同伦论等专题，完成具体空间计算与论文证明讲解'],
'08-combinatorics':[
'乘加原理、排列组合、容斥、鸽巢原理与基本图论',
'递推、生成函数、树、连通、匹配、平面图与基本图算法',
'极值方法、概率方法、Ramsey思想与组合设计；练习构造与计数双证',
'按方向专修代数组合、谱图论、加性组合或极值图论；补相应代数和概率工具',
'重建一个极值界或构造，分析最佳性；用计算探索小规模情形并写严格证明'],
'09-probability':[
'样本空间、事件、条件概率、独立、Bayes公式；从模型到计算',
'随机变量、分布、期望、方差、联合分布、条件期望直觉与基本极限定理',
'测度概率、收敛方式、大数定律与中心极限定理证明；明确可积条件',
'鞅、Markov过程、Brown运动、随机积分；按方向选大偏差或随机微分方程',
'研究某一随机模型：证明界、模拟并核对理论；说明经验结果不能替代理论证明'],
'10-statistics':[
'分布描述、抽样、偏差、相关与因果；阅读和质疑统计结论',
'估计、置信区间、假设检验、线性回归、实验设计；解释不确定性',
'似然、充分性、渐近理论、广义线性模型、Bayes与决策理论',
'按方向专修非参数、高维、因果推断、时间序列或计算统计；检查可识别性和模型假设',
'复现一项方法研究：理论条件、模拟和真实数据验证；分析覆盖率、偏差与失效情形'],
'11-differential-equations':[
'微分方程、初值、指数增长、方向场、平衡与简单数值解',
'一阶与二阶线性ODE、方程组、存在唯一性、相平面与稳定性',
'热/波/Laplace方程、边界与初值、Fourier方法、变分与弱解入门',
'按方向选择非线性PDE、动力系统、分岔混沌、遍历、积分或差分方程',
'选择一个具体方程，证明存在性、估计或长期行为的一个结果；核对解空间与边界条件'],
'12-numerical':[
'舍入、截断、误差与残差、二分与欧拉法；检验计算是否可信',
'插值、数值积分、线性方程求解、迭代法、条件数与稳定性',
'数值ODE/PDE、稀疏矩阵、特征值算法、误差估计与收敛阶',
'按方向专修有限元、有限体积、谱方法、自适应算法或高性能计算',
'复现算法论文：推导误差界并设计可重复基准；报告失败例、复杂度与实现偏差'],
'13-optimization':[
'目标、变量、约束、可行域、局部与全局最优；简单梯度迭代',
'凸集与凸函数、线性规划、对偶、最优性条件、KKT适用条件',
'整数规划、组合优化、非线性优化、动态规划；变分与控制基础',
'按方向选择凸分析、随机优化、最优控制、鲁棒控制或运筹调度',
'在清晰假设下证明算法收敛或控制性质，并以基准问题比较性能与失败范围'],
'14-computation':[
'算法、复杂度与信息量；逻辑、组合和概率工具预备',
'自动机、形式语言、可计算性、归约、P/NP与基本算法设计',
'按支线学习复杂性、信息熵/互信息、信道编码、纠错码与现代密码安全定义',
'选随机算法、复杂性、编码或密码专修；密码方向还需数论与概率安全归约',
'重现算法界、编码构造或安全证明；区分实验更快与渐近改进，区分经验安全与证明'],
'15-mathematical-physics':[
'量纲、牛顿方程、振荡与守恒；明确数学变量与物理解释',
'分析力学、连续介质和基本场方程；补向量分析、ODE/PDE',
'按支线学习Hamilton体系、流体/弹性、热与电磁、量子或相对论的数学基础',
'选择谱方法、微分几何、统计力学或非线性PDE工具；每条物理支线有独立先修',
'在一个明确模型内复现数学结果并说明物理边界；天体物理与地球物理需另补领域知识'],
'16-modeling':[
'问题定义、变量、单位、假设、验证与灵敏度；建立可检查的简单模型',
'无量纲化、参数估计、增长/网络/随机模型；区分拟合和外推',
'按支线学习生物系统、经济博弈、金融随机模型、网络或社会系统',
'可识别性、不确定性量化、模型比较与机制检验；补对应领域知识和因果方法',
'完成一个开放数据或机制模型项目；外部验证、失败分析、可重复代码和独立评议缺一不可'],
'17-history':[
'数系、公理、定义、证明与反例；尊重不同空间和前提',
'古典几何、代数与微积分的概念发展；区分现代重述与历史原意',
'无穷、严密化、形式化与基础危机；阅读原文及可靠的历史研究',
'按方向研究数学哲学、史学方法、概念学习与数学教育研究设计',
'基于原始史料或教育数据提出窄问题；公开证据链、反对解释和方法限制']}
levels=['L0 · 入门与直觉','L1 · 本科核心','L2 · 高阶本科与证明训练','L3 · 研究生专题','L4 · 研究训练']
checks=[
'能解释关键词，独立完成计算，并给出例子和反例。',
'能在不给提示时选择方法、检查前提，写出完整解答。',
'能重建关键定理的证明，辨别假设不可删的地方，并完成综合题。',
'能读教材或专题讲义，补齐省略步骤，做出可核查的专题报告。',
'能读懂选定方向论文、复现已有结果并接受同行反馈；是否产生原创结果需真实研究检验。']
overview=f'<header><h1>从基础到研究训练：课程总纲</h1><p>这是课程设计，不是“全部教程已写完”的声明。{sum(len(m[-1]) for m in course)}节入门正文已经可读；本页的高阶单元尚未编写。分类索引中的6000余条记录也不等于6000门互不相关的课程。</p></header>'
overview+='''<section class="panel"><h2>“大师”怎样理解</h2><p>没有公认的“大师课程结业线”。本项目把可检查的上限设为某一方向的研究准备与初步研究训练：能读论文、补证明、复现结果、提出小问题并接受反馈。数学各方向跨度很大，通常需要建立广泛基础后选择少数方向深入。</p><p>升级依据是作品与解题证据，不是浏览进度。读完一课不自动等于掌握，完成总纲也不等于完成教材。</p><h2>课程正文的完成标准</h2><p>每个主题应有：明确先修和目标、概念直觉、准确的定义、定理条件、必要证明、至少一个完整例题、基础与迁移练习、提示与完整解析、常见错误、可信来源。适合可视化的主题另加可操控图形，并说明图形不能替代证明。</p></section><h2>各方向的分级路径</h2><div class="grid">'''
for folder,title,subs,pre,source,lessons in course:
 text=f'<header><h1>{E(title)}：分级课程路线</h1><p>本分支现有 {len(lessons)} 节入门短课。以下每级包含多个待展开主题，不能把两节课视为L0或L1已全部完成。</p><p>入门先修：{E(pre)}</p><a href="index.html">阅读现有课程正文</a></header>'
 for i,topic in enumerate(paths[folder]):
  text+=f'<article><p class="tag">规划中 / 未计入已完成课数</p><h2>{levels[i]}</h2><p>{E(topic)}</p><h3>阶段验收</h3><p>{checks[i]}</p>'
  if i>0:text+='<p>进入前：通过前一级的独立解题或报告验收；若跨入其他方向，还需补相应分析、代数、概率或领域知识。</p>'
  text+='</article>'
 text+='<footer><p>不要按清单盲目跳级。每次学习后记录哪些题能独立解决、哪些证明仍需要提示，再确定下一课。研究阶段宜加入读书组或接受专业指导。</p></footer>'
 (root/folder/'curriculum.html').write_text(page(title+'分级课程 · 数学理解课',text),encoding='utf-8')
 p=root/folder/'index.html';s=p.read_text(encoding='utf-8')
 marker='<p class="curriculum-link"><a href="curriculum.html">查看从入门到研究训练的分级路线 →</a></p>'
 if 'class="curriculum-link"' not in s:s=s.replace('</header>',marker+'</header>',1)
 p.write_text(s,encoding='utf-8')
 overview+=f'<a class="card" href="../{folder}/curriculum.html"><h3>{E(title)}</h3><p>L0 入门 → L1 核心 → L2 证明 → L3 专题 → L4 研究训练</p></a>'
overview+='</div><footer><p>这是教学分级，不是大学统一课程标准；具体顺序会随方向和你的学习反馈调整。</p></footer>'
(root/'reference/curriculum.html').write_text(page('分级课程总纲 · 数学理解课',overview),encoding='utf-8')
# 核心概念自查清单：数据在 assets/concepts.json（手工维护）；勾选进度存浏览器 localStorage。
concepts=json.loads((root/'assets/concepts.json').read_text(encoding='utf-8'))
assert set(concepts)=={m[0] for m in course},'concepts.json 的模块键与课程数据不一致'
cp=f'<header><p class="tag">CONCEPT CHECKLIST</p><h1>核心概念自查清单</h1><p>对应 {sum(len(m[-1]) for m in course)} 节课，每项按“能解释、能推导、能迁移”口径自查：先闭卷作答，做到再勾选；次日、3 天、7 天后回看重做。勾选只保存在本机浏览器，不上传、不写入仓库。</p><p id="total" aria-live="polite"></p><button id="reset" type="button">清空全部勾选记录</button></header>'
for folder,title,subs,pre,source,lessons in course:
 n=concepts[folder]
 assert len(n)==len(lessons),f'{folder} 的概念条目数与课程数不一致'
 cp+=f'<section class="panel" data-module="{folder}"><h2>{E(title)} <span class="muted" data-count></span></h2><p><a href="../{folder}/index.html">分支首页</a> · <a href="../{folder}/curriculum.html">分级路线</a></p>'
 for lesson,c in zip(lessons,n):
  items=''.join(f'<li><label><input type="checkbox" id="{folder}-{c["file"]}-{i}"> {E(t)}</label></li>' for i,t in enumerate(c['items'],1))
  cp+=f'<div class="concept"><h3><a href="../{folder}/lessons/{c["file"]}.html">{int(c["file"]):02d} · {E(lesson[0])}</a> <span class="muted" data-count></span></h3><ul>{items}</ul></div>'
 cp+='</section>'
cp+=r'''<footer><p>清单覆盖现有 __N__ 节正文课；L1–L4 的更高阶目标见<a href="curriculum.html">分级课程总纲</a>。勾选是自评快照，不等于掌握：以能否闭卷重做、讲清条件和给出自己的例子为准。</p></footer>
<script>
'use strict';
const KEY='math-concepts-v1';let state={};
try{state=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}};
function refresh(){let total=0,done=0;
for(const sec of document.querySelectorAll('[data-module]')){let sd=0,st=0;
for(const d of sec.querySelectorAll('.concept')){let ld=0,lt=0;
for(const b of d.querySelectorAll('input')){b.checked=!!state[b.id];total++;st++;lt++;if(b.checked){done++;sd++;ld++}}
d.querySelector('[data-count]').textContent=ld+'/'+lt}
sec.querySelector('[data-count]').textContent=sd+'/'+st}
document.getElementById('total').textContent='总进度：'+done+' / '+total+' 项'}
for(const b of document.querySelectorAll('.concept input'))b.addEventListener('change',()=>{state[b.id]=b.checked;save();refresh()});
document.getElementById('reset').addEventListener('click',()=>{if(confirm('清空全部勾选记录？')){state={};save();refresh()}});
refresh();
</script>'''
cp=cp.replace('__N__',str(sum(len(m[-1]) for m in course)))
(root/'reference/concepts.html').write_text(page('核心概念自查清单 · 数学理解课',cp),encoding='utf-8')
# Make the new work visible while keeping the existing entry page and README intact.
p=root/'index.html';s=p.read_text(encoding='utf-8')
marker='<section class="panel" id="extended-atlas"><h2>完整分类与长期路线</h2><p><a href="reference/classification.html">打开MSC2020完整源文件分类索引</a> · <a href="reference/curriculum.html">查看各分支从基础到研究训练的总纲</a></p><p>分类索引可按编码或英文关键词搜索。分级路线为规划，高阶正文尚未写完。</p></section>'
if 'id="extended-atlas"' not in s:s=s.replace('<h2>数学的分支地图</h2>',marker+'<h2>数学的分支地图</h2>')
p.write_text(s,encoding='utf-8')
p=root/'README.md';s=p.read_text(encoding='utf-8');section=f'''
## 完整分类与从基础到研究的课程规划

- [完整 MSC2020 分类索引](reference/classification.html)：收入官网下载 CSV 的全部 **{count["total"]:,} 条编码记录**，包含{count["major"]}个大类、{count["middle"]}个中类、{count["subject_leaf"]:,}个专题末级条目和{count["general_leaf"]}个通用末级条目；已与官方 TeX 的全部标签集合核对一致。保留英文专业名，可离线搜索编码或关键词。分类名称完整收录不等于对应教程已经完成。
- **计数说明**：[官网介绍](https://msc2020.org/)写63个大类、529个中类、6,022个末级类；当前下载文件实测计数不同。本项目报告源文件实测结果，未自行补造分类。审计结果在 `assets/classification-audit.json`。
- [分级课程总纲](reference/curriculum.html)：每个模块都有 L0 入门、L1 本科核心、L2 高阶与证明、L3 研究生专题、L4 研究训练的目标与验收要求。以上是**待展开的教学规划**，现有正文仍为{sum(len(m[-1]) for m in course)}节。
- [核心概念自查清单](reference/concepts.html)：{sum(len(m[-1]) for m in course)} 节课逐项“能解释 / 能推导 / 能迁移”自评，勾选进度仅保存在本机浏览器（localStorage）。
- 研究训练意味着在特定方向读论文、复现证明或算法、提出问题和接受反馈。没有覆盖全部数学的“大师结业线”，读完资料也不能保证原创研究能力。

重建：先运行 `python tools/build_course.py`，再运行 `python tools/extend_atlas.py`；验证先 `pip install -r requirements.txt`，再运行 `python tools/verify_course.py`（需要 Playwright 与本机 Chrome/Chromium）。分级课程内容在 `tools/extend_atlas.py` 中维护；`MISSION.md`、`NOTES.md`、`RESOURCES.md`、`assets/concepts.json`（概念清单数据）与 `learning-records/` 为手工维护文档，重建不会覆盖。
'''
if '## 完整分类与从基础到研究的课程规划' in s:s=s.split('## 完整分类与从基础到研究的课程规划')[0].rstrip()
p.write_text(s+'\n'+section,encoding='utf-8')
print('Classification index:',count,'; staged routes:',len(paths))
