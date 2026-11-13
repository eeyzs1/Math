# 维护 Checklist

文件归属、完整命令与备份格式见 [CONTRIBUTING.md](CONTRIBUTING.md)。本表用于每次修改后的快速核对。

## 课程或概念改动

- [ ] 中文改 `tools/build_course.py`，英文同步 `assets/course.en.json`。
- [ ] 同步 `assets/concepts.json` 与 `assets/concepts.en.json`；模块/课号/条目数对应，既有条目不重排，新条目追加。
- [ ] 新课具备概念条件、完整例题、练习、解析和先修说明；新增模块还须同步两份 atlas 的 L0–L4 路线及 MSC 映射。
- [ ] 交互逻辑改 `tools/static/*.js`，本地化文案改 `tools/site_common.py`，不直接改 `assets/*.js`。

## 固定验证

```sh
python tools/build_all.py
python -m unittest discover -s tests
python tools/verify_course.py
```

首次运行浏览器检查需 `python -m pip install -r requirements.txt` 与 `python -m playwright install chromium`。仅静态检查可用 `python tools/verify_course.py --static-only`，不需要 Playwright。`verify_course_en.py` 保留为英文静态检查入口。

- [ ] 全部验证通过，生成物与维护源文件一并检查差异。
- [ ] 抽查首页、改动课程、实验室与概念清单；需要时检查导出/导入。
- [ ] 再次重建不应引入额外差异；检查后按需要提交。CI 会验证 Linux 下重建一致性。

## 自动检查范围

- 双语模块、课程字段、概念课号/顺序与稳定 ID；正文与生成页可见文字一致。
- 全站 HTML 本地链接、URL 解码后的目标和片段锚点、重复 ID、模板残留、英文翻译残留。
- CSV/TeX 分类编码集合及审计计数，分类搜索与过滤后的 hash 深链。
- 两语言全部实验端点、概率归一化、抽样均值/标准差、密度共用刻度、牛顿真实曲线、特征半轴。
- 学习记录持久化、跨语言备份、非法备份不覆盖、损坏记录与存储不可用。
- 打印前确实展开、重复事件后还原；全部 364 页在 320px 宽度无横向溢出。

## 分类源数据更新

- [ ] CSV 保留 latin1，TeX 使用 UTF-8；核对分类集合与两语映射后重建。
- [ ] 计数从文件动态生成，无需手改验证器；核对 README 中引用的官网说明是否仍准确。
- [ ] 原始分类描述中的 TeX 字面量按官方内容保留；页面编码完整不等于相应教材已经完成。
