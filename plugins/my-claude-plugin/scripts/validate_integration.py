"""パッケージの静的検証。自然言語スキルの動作テストではない。依存: PyYAML。"""
from pathlib import Path
import json
import re
import yaml

plugin = Path(__file__).resolve().parents[1]
root = plugin.parents[1]
manifest = json.loads((plugin / '.claude-plugin/plugin.json').read_text())
market = json.loads((root / '.claude-plugin/marketplace.json').read_text())
entry = next(x for x in market['plugins'] if x['name'] == manifest['name'])
assert (root / entry['source']).resolve() == plugin
expected = {'article-facilitator', 'article-title-suggestion', 'article-writer',
            'article-reviewer', 'article-editor', 'article-thumbnail'}
skills = sorted((plugin / 'skills').glob('*/SKILL.md'))
assert {p.parent.name for p in skills} == expected
for path in skills:
    text = path.read_text()
    metadata = yaml.safe_load(text.split('---', 2)[1])
    assert metadata['name'] == path.parent.name, path
    assert isinstance(metadata['description'], str) and metadata['description'].strip(), path
    assert '../../references/article-context.md' in text, path
    assert '<!-- フェーズ' not in text, path
# 履歴資料は旧パスを意図的に保持。現行文書の相対リンクだけを検証する。
paths = [root / 'README.md', root / 'plugins/README.md', plugin / 'README.md']
paths += list((plugin / 'skills').rglob('*.md'))
paths += list((plugin / 'references').rglob('*.md'))
paths += [plugin / 'docs/integration-verification.md', plugin / 'docs/archive/README.md']
for path in paths:
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        assert (path.parent / target.split('#')[0]).exists(), (path, target)
# Eの既存キー・型の保持、およびFのゲート前提を参照サンプルで確認。
def json_block(path):
    return json.loads(re.search(r'```json\n(.*?)\n```', path.read_text(), re.S)[1])
before = json_block(plugin / 'examples/input/scenario-e.md')
after = json_block(plugin / 'examples/output/scenario-e-titles.md')
assert {k: v for k, v in after.items() if k != 'title'} == before
assert after['title'] == '家計管理は支出の記録から始めよう'
for filename in ['scenario-e-titles.md', 'scenario-f-titles.md']:
    text = (plugin / 'examples/output' / filename).read_text()
    ids = set()
    for line in text.splitlines():
        if not line.startswith('| R'):
            continue
        cells = [v.strip() for v in line.strip('|').split('|')]
        ident, title, count = cells[:3]
        assert ident not in ids
        ids.add(ident)
        assert len(title) == int(count) <= 40
        scores = list(map(int, cells[5:8]))
        assert all(1 <= x <= 5 for x in scores)
        assert abs(float(cells[8]) - sum(scores) / 3) <= 0.005
    assert len([i for i in ids if i.startswith('R1-')]) >= 5
    if filename.startswith('scenario-f'):
        assert len([i for i in ids if i.startswith('R2-')]) >= 3
print('PASS: manifests, 6 skill names/frontmatter, current relative links, E/F reference data')
