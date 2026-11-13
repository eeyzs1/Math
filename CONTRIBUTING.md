# 维护与验证 / Maintenance

课程网页可直接离线打开，维护脚本需要 Python 3.10 或更新版本。修改课程正文后，请同时更新中英文和概念自查，不要手改生成的 HTML。

The course works offline without dependencies. Maintenance scripts require Python 3.10 or later. Update both editions and their self-checks together, then regenerate HTML.

## 文件归属 / Source ownership

| 维护源文件 / Source | 生成物 / Generated output |
|---|---|
| `tools/build_course.py` | 中文课程页面、`assets/course.json`、共享 CSS、来源数据与 `README.md` 主体 |
| `assets/course.en.json`、`tools/build_course_en.py` | 英文课程页面 |
| `tools/extend_atlas.py`、`tools/extend_atlas_en.py` | 分类索引、L0–L4 规划页面、概念清单页面与 README 中文附录 |
| `assets/concepts.json`、`assets/concepts.en.json` | 概念自查文案；条目 `file` 必须按课序为 `01`、`02`…… |
| `tools/static/*.js`、`tools/site_common.py` | `assets/widgets*.js`、`assets/concepts*.js`；共享逻辑与本地化文案 |
| `RESOURCES.md`、`RESOURCES.en.md` | `reference/resources*.html` |

`README.en.md`、`MISSION*.md`、`NOTES*.md`、`CHECKLIST*.md`、`REVIEW*.md` 和 `learning-records/` 为手工维护。`assets/msc2020.csv` 保留 latin1 编码，TeX 保留 UTF-8。

## 常用命令 / Commands

从仓库根目录运行；生成器与验证脚本也支持由其他工作目录以绝对路径调用。

```sh
python tools/build_all.py
python -m unittest discover -s tests
python tools/verify_course.py --static-only
```

首次执行浏览器检查 / First browser check:

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python tools/verify_course.py
```

完整检查默认覆盖中英文。优先使用 Playwright 自带 Chromium，也可使用已安装的 Chrome/Edge，或通过 `MATH_BROWSER_PATH` 指定可执行文件。Linux CI 用 `python -m playwright install --with-deps chromium` 安装系统依赖。自动化检查生成的预览图在 `assets/`，已排除出版本控制。

Full checks cover both editions. Browser discovery tries bundled Chromium, installed Chrome and Edge; `MATH_BROWSER_PATH` can specify an executable. Preview PNGs in `assets/` are ignored by Git.

## 新增或调整课程 / Changing lessons

1. 在 `tools/build_course.py` 中维护中文五字段：标题、概念、例题、练习、解析；英文同步到 `assets/course.en.json`。
2. 同步两份 `concepts*.json`。保留既有课程和概念项的顺序；勾选 ID 来自“模块、课号、概念项序号”，重排会改变已有进度的含义。新项应追加。
3. 正文中的 `<`、`>` 和 `&` 会正确转义；支持受控的行内链接和格式。不要依赖任意 HTML。
4. 重建并验证后检查差异；再次重建不应产生额外变化。按需要提交，推送后 GitHub Actions 会再次构建并检查生成物是否同步。

Checkbox IDs depend on module, lesson and item order. Append new items to preserve existing progress. Rebuild and verify before committing; CI checks for stale generated files.

## 学习记录备份 / Progress backups

概念清单可导出 `math-progress.json`，格式为 `{"version":1,"checked":["checkbox-id",...]}`。两种语言使用相同 ID，备份可以互导，但各页面仍保留原有独立的本地存储键。导入有效备份会替换勾选；已有勾选时会要求确认，非法备份不改变当前记录。

Both editions share checkbox IDs and accept each other's backups, while retaining their original separate storage keys. Import replaces ticks after confirmation when progress already exists. Invalid files leave progress unchanged. Exercise text is never saved or exported.

文件方式打开页面时，浏览器对 localStorage 的可用性及作用范围可能不同，迁移浏览器或更改访问方式前请导出备份。界面会报告存储失败。

For file URLs, browser storage availability and scope can vary. Export a backup before changing browser or access method; storage errors are shown in the UI.
