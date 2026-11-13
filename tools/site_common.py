"""Shared rendering and browser assets for both offline course editions."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

STATIC = Path(__file__).resolve().parent / 'static'


def inline(text):
    """Escape mathematical inequalities while preserving authored inline links.

    Treating course text as raw HTML silently eats expressions such as 0<y<1.
    Only the small set of markup actually supported by the course is retained.
    """
    parts = re.split(r'(<a href="[^"<>]+">|</a>|</?(?:b|i|em|strong|code|sub|sup)>|<br\s*/?>)', text)
    rendered = []
    for i, part in enumerate(parts):
        if not i % 2:
            rendered.append(html.escape(html.unescape(part), quote=False))
        elif part.startswith('<a href="'):
            target = html.unescape(part[9:-2])
            if urlsplit(target).scheme in ('', 'https', 'http', 'mailto'):
                rendered.append(f'<a href="{html.escape(target, quote=True)}">')
            else:
                rendered.append(html.escape(part, quote=False))
        else:
            rendered.append(part)
    return ''.join(rendered)


PRINT_SCRIPT = """<script>(()=>{'use strict';let printed=null;
addEventListener('beforeprint',()=>{if(printed!==null)return;
printed=[...document.querySelectorAll('details:not([open])')];printed.forEach(d=>d.open=true)});
addEventListener('afterprint',()=>{if(printed===null)return;
printed.forEach(d=>d.open=false);printed=null});})();</script>"""

MESSAGES = {
    'zh': {
        'widgets': {
            'fixed': '固定点 (1,1)', 'unit': '单位边长对应 90 像素',
            'secant': '割线斜率', 'tangent': '切线斜率', 'area': '面积',
            'expectation': '期望', 'variance': '方差', 'sum': '概率和',
            'probability': '概率；横轴：正面次数 k', 'factor': '单步倍率',
            'last': '末步', 'range': '纵轴范围约', 'time': '横轴 t=0…10',
            'clt': '正面比例：直方图与正态密度共用纵轴',
            'theorySD': '理论 σ', 'sampleSD': '样本 σ', 'mean': '样本均值',
            'density': '概率密度', 'groups': '组', 'newton': '牛顿迭代：切线零点作为下一步',
            'iteration': '迭代', 'converged': '已收敛', 'limit': '达到迭代上限',
            'cycle': '检测到循环', 'flat': '导数接近零，停止',
            'escaped': '迭代离开显示范围，停止', 'residual': '末次残差',
            'eigen': '灰：单位圆；绿：像；橙：半轴方向与长度 |λ|',
            'areaFactor': '面积倍率', 'semiaxes': '半轴长度',
        },
        'concepts': {
            'key': 'math-concepts-v1', 'total': '总进度：', 'items': ' 项',
            'confirmReset': '清空全部勾选记录？',
            'confirmImport': '用备份替换当前勾选记录？',
            'saved': '记录已保存在本机浏览器。建议定期导出备份。',
            'volatile': '浏览器无法保存记录，本页勾选在关闭后可能丢失。请导出备份。',
            'corrupt': '已忽略格式异常的旧记录，可导入备份恢复。',
            'invalid': '无法导入：请选择本课程导出的有效 JSON 备份。当前记录未改动。',
            'imported': '已导入备份。', 'exported': '已导出备份。',
        },
    },
    'en': {
        'widgets': {
            'fixed': 'Fixed point (1,1)', 'unit': 'One unit corresponds to 90 pixels',
            'secant': 'secant slope', 'tangent': 'tangent slope', 'area': 'area',
            'expectation': 'mean', 'variance': 'variance', 'sum': 'probability sum',
            'probability': 'Probability; horizontal axis: number of heads k', 'factor': 'step multiplier',
            'last': 'last step', 'range': 'Vertical range about', 'time': 'horizontal axis t=0…10',
            'clt': 'Heads proportion: histogram and normal density share a vertical scale',
            'theorySD': 'theoretical σ', 'sampleSD': 'sample σ', 'mean': 'sample mean',
            'density': 'Probability density', 'groups': 'groups',
            'newton': 'Newton iteration: each tangent zero is the next iterate',
            'iteration': 'Iterates', 'converged': 'converged', 'limit': 'iteration limit reached',
            'cycle': 'cycle detected', 'flat': 'derivative near zero; stopped',
            'escaped': 'iterate left the displayed range; stopped', 'residual': 'last residual',
            'eigen': 'Gray: unit circle; green: image; orange: semiaxes, lengths |λ|',
            'areaFactor': 'area factor', 'semiaxes': 'semiaxis lengths',
        },
        'concepts': {
            'key': 'math-concepts-en-v1', 'total': 'Total progress: ', 'items': ' items',
            'confirmReset': 'Clear all check marks?',
            'confirmImport': 'Replace the current check marks with this backup?',
            'saved': 'Saved in this browser. Export a backup regularly.',
            'volatile': 'Browser storage is unavailable. Ticks may be lost when you close this page. Export a backup.',
            'corrupt': 'Malformed stored progress was ignored. You can restore a backup.',
            'invalid': 'Import failed: select a valid JSON backup exported by this course. Current progress is unchanged.',
            'imported': 'Backup imported.', 'exported': 'Backup exported.',
        },
    },
}


def script_source(name, language):
    source = (STATIC / f'{name}.js').read_text(encoding='utf-8')
    return source.replace('__MESSAGES__', json.dumps(MESSAGES[language][name], ensure_ascii=False))


def concept_controls(language):
    if language == 'zh':
        export, restore, reset = '导出勾选备份', '导入备份（替换勾选）', '清空全部勾选记录'
        note = '备份可在中英文清单间转移，也可迁移到另一浏览器；练习输入不包含在备份中。'
    else:
        export, restore, reset = 'Export progress', 'Import backup (replace ticks)', 'Clear all check marks'
        note = 'Backups work across both editions and browsers. Exercise text is not included.'
    return (f'<p>{note}</p><div class="progress-actions">'
            f'<button id="export" type="button">{export}</button>'
            f'<label for="import">{restore}</label><input id="import" type="file" accept=".json,application/json">'
            f'<button id="reset" type="button">{reset}</button></div>'
            '<p id="storage-status" role="status" aria-live="polite"></p>')
