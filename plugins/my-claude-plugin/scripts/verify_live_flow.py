"""保存した実応答の照合。モデル実行や新しい応答の保証は行わない。"""
from pathlib import Path
import json
import re
import hashlib

plugin = Path(__file__).resolve().parents[1]
evidence = json.loads((plugin / 'docs/live-flow-2026-10-25/evidence.json').read_text())
records = {r['case']: r for r in evidence['records']}
assert len(records) == 11
for r in records.values():
    assert not r['is_error'] and not r['permission_denials'], r['case']
for path, expected_hash in evidence['source_sha256'].items():
    assert hashlib.sha256((plugin / path).read_bytes()).hexdigest() == expected_hash, f'検証後に変更あり: {path}'
def response(name):
    return records[name]['response']
def block(text, language):
    return re.search(r'```' + language + r'\n(.*?)\n```', text, re.S)[1]
for name, minimum in [('01-propose', 5), ('02-refine', 3)]:
    rows = []
    for line in response(name).splitlines():
        if not line.startswith('| R'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) != 9:  # 履歴の要約表は除外
            continue
        assert len(cells[1]) == int(cells[2]) <= 40
        scores = list(map(int, cells[5:8]))
        assert all(1 <= n <= 5 for n in scores)
        assert abs(float(cells[8]) - sum(scores) / 3) < .005
        rows.append((sum(scores), scores[2], cells[0]))
    assert len(rows) >= minimum
    assert rows == sorted(rows, key=lambda r: (-r[0], -r[1], r[2]))
    assert re.search(r'selectedTitle\*\*: null', response(name))
before = json.loads(block(records['01-propose']['prompt'], 'json'))
after = json.loads(block(response('03-confirm'), 'json'))
title = after.pop('title')
assert after == before
assert f'**タイトル（確定）**: {title}' in response('03-confirm')
draft = response('05-write-approved')
assert draft.startswith('# ' + title + '\n')
assert '（別案:' not in draft
assert title in response('06-review')
assert '## レビューコメント' in response('06-review') and '## 事実確認リスト' in response('06-review')
original_article = draft.split('\n---\n\n確定タイトル')[0].strip()
editor = response('07-editor')
edited_article = editor[editor.index('# ' + title):editor.index('## 編集指示サマリー')]
edited_article = re.sub(r'^>.*\n?', '', edited_article, flags=re.M).rstrip()
edited_article = re.sub(r'\n---\s*$', '', edited_article)
def nonblank(text):
    return '\n'.join(line for line in text.splitlines() if line.strip())
assert nonblank(original_article) == nonblank(edited_article)
for name, target in [('08-thumbnail', title), ('boundary-no-draft', '支出記録で家計管理')]:
    text = response(name)
    assert len(re.findall(r'^### パターン [1-3]:', text, re.M)) == 3
    assert '1280×720' in text and target in text and '第一候補' in text
late_prompt = records['boundary-late-title']['prompt']
old = late_prompt.split('## ArticleDraft\n\n')[1]
expected = re.sub(r'^# .*\n.*別案.*\n', '# ' + title + '\n', old)
assert block(response('boundary-late-title'), 'markdown').strip() == expected.strip()
assert not re.search(r'^\| R\d+-\d+', response('boundary-no-input'), re.M)
print('PASS: 11実応答、検証対象ハッシュ、候補・採点、確定Context、H1、editor原文保持、thumbnail、執筆後の反映')
print('会話の意味・入力なしの案内・reviewerの非改稿等はレポート記載の目視評価を併用。')
