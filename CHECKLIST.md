# 维护 Checklist

本仓库一半是生成物、一半是手工文档。先分清，再动手。

## 文件归属速查

| 类别 | 文件 | 怎么改 |
|---|---|---|
| 生成器 | `tools/build_course.py`、`tools/extend_atlas.py` | 直接改，改完重建 |
| 生成的页面 | `index.html`、`NN-*/`（含 lessons、curriculum）、`reference/*.html`、`README.md`、`assets/style.css`、`assets/widgets.js`、`assets/course.json`、`assets/sources.json`、`assets/classification-audit.json` | **不要手改**，改生成器后重建 |
| 手工维护 | `MISSION.md`、`NOTES.md`、`RESOURCES.md`、`learning-records/`、`CHECKLIST.md` | 直接改，重建不会覆盖 |
| 源数据 | `assets/msc2020.csv`（latin1）、`assets/msc2020.tex`（UTF-8） | 替换官方下载文件，保持原编码 |
| 验证 | `tools/verify_course.py`、`requirements.txt` | 直接改 |

## 每次改动后的固定流程

- [ ] `python tools/build_course.py`
- [ ] `python tools/extend_atlas.py`（顺序不能反：build 会重写页面，extend 负责追加分类与分级路线）
- [ ] `python tools/verify_course.py` 全绿（首次先 `pip install -r requirements.txt`）
- [ ] 浏览器抽查：`index.html` 首页、任一课程页、`reference/labs.html` 拖滑块、`reference/classification.html` 搜索
- [ ] `git add -A && git commit && git push`

## 新增一节课

- [ ] 在 `tools/build_course.py` 对应模块的数据元组末尾追加 `(标题, 直觉与定义, 推导例题, 练习, 解析)`
- [ ] 无需改任何计数或导航：上一课/下一课链接、"N 节课"文案、首页与 README 的模块/课数都是动态生成
- [ ] 走固定流程重建 + 验证 + 提交

## 新增一个模块

- [ ] `build_course.py` 的 `data` 里加元组：`(目录名, 标题, 子领域；分号分隔, 先修, 教材key, 课程列表)`
- [ ] 教材 key 必须在 `sources` 字典中（现有：discrete/pre/linear/calculus/statistics/ode/topology）；新增来源需同步补 `RESOURCES.md`（手工文档）
- [ ] 目录名用 `NN-slug` 格式（两位数字前缀）
- [ ] 若对应 MSC 研究大类：更新 `groups` 映射；`cn` 是"编码→译名"字典，与 CSV 大类集合有断言核对，错配会直接报错
- [ ] 在 `tools/extend_atlas.py` 的 `paths` 里为新模块加 5 级分级路线（L0–L4）
- [ ] 检查 README"推荐学习路径"一节是否需要把新模块挂进某条路线（该段在 build 模板里，不是手写正文）
- [ ] 固定流程重建 + 验证 + 提交

## 更新 MSC2020 源数据

- [ ] 替换 `assets/msc2020.csv` 与 `assets/msc2020.tex`
- [ ] `build_course.py` 会断言 `cn` 字典与 CSV 63 个大类集合一致；`extend_atlas.py` 会断言 CSV 编码与 TeX label 集合一致——任一失败先核对数据再改映射
- [ ] `assets/classification-audit.json` 与 README 计数自动重算；若总数变化，`tools/verify_course.py` 里 `.major==63`、`.entry==6006` 等断言需同步更新
- [ ] README"计数说明"里官网宣称数（63/529/6,022）与实测数的差异描述是否仍成立

## verify_course.py 自动覆盖的范围

- 全站本地链接目标存在（rglob 所有 HTML 的 href/src）
- labs 四个滑块的端点值（h=0.01、a=0/−2、p=0/1、step=1.2）输出无 NaN
- 答案 `<details>` 可展开；390px 视口无横向溢出
- classification：63 大类、6006 条目、编码精确搜索、无结果、清空恢复、hash 深链定位
- 每个模块 curriculum 页恰有 5 级；页面 JS 无未捕获报错
- 输出 3 张 QA 截图到 `assets/`（已 gitignore，勿提交）

## 已知遗留（低优先级，按需处理）

- [ ] 全站无 `<meta name="description">`（离线使用无影响；若公网部署，在两个生成器的 `page()` 模板补）
- [ ] 分支页的 `../RESOURCES.md` 链接在浏览器中会以纯文本打开（可接受；或改为 HTML 页）
- [ ] classification 个别条目残留 TeX 字面量（如 `\{For ...\}`），属官方源数据内容
- [ ] 无实验的页面也加载 `widgets.js`（2.7KB、defer，影响可忽略）
- [ ] labs 的二项分布实验无基线坐标轴（柱形直接落在底边）
