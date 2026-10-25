# Research & Design Decisions

---
**Purpose**: ディスカバリーフェーズで収集した知見・アーキテクチャ検討・設計判断の根拠を記録する。
**Usage**: `design.md` に反映した結論は本ファイルで詳細な調査ログとして保持する。

---

## Summary

- **Feature**: `article-agent`
- **Discovery Scope**: New Feature（グリーンフィールド）、Complex Integration（Claude Code Skills マルチスキル構成）
- **Key Findings**:
  - Claude Code Skills（SKILL.md ベース）は各スキルに独立した責務と説明文を持たせることで、自動呼び出しと明示呼び出しの両方に対応する
  - スキル間の状態共有はデータベース不要で、会話履歴に埋め込む ArticleContext Markdown ブロックが最適解
  - 「パイプライン with フェーズゲート」パターンが要件 2.5（構成合意前にドラフト生成禁止）を自然に実現する

---

## Research Log

### Claude Code Skills アーキテクチャの調査

- **Context**: このフィーチャーは Claude Code Skills として実装される。SKILL.md モデルの理解が設計の起点。
- **Sources Consulted**: Claude API ドキュメント（Extend Claude with skills）、ChatGPT との事前相談記録
- **Findings**:
  - スキルは `.claude/skills/<skill-name>/SKILL.md` として定義する
  - SKILL.md は `name`・`description`・本文（指示）の3要素で構成される
  - `description` の記述品質が自動呼び出しの精度に直結する
  - スキルはプロジェクト単位（`.claude/skills/`）またはユーザー単位（`~/.claude/skills/`）で管理可能
  - 複数スキルは会話コンテキストを共有するが、typed shared state は持たない
- **Implications**:
  - 各スキルは自身の起動条件を description で正確に記述する必要がある
  - スキル間のデータ受け渡しは、ArticleContext のような明示的な Markdown フォーマットブロックで行う

### 状態共有メカニズムの調査

- **Context**: 3スキルが順番に動作する際、前フェーズの成果物を次スキルが正しく参照する必要がある
- **Findings**:
  - Claude Code Skills では会話履歴が暗黙的な共有メモリとして機能する
  - JSON 形式のオブジェクトは機械可読性が高いが、ユーザーが確認・編集しにくい
  - Markdown 形式の構造化ブロック（`## ArticleContext` セクション）は視認性・編集性・コピー&ペースト適性が高い
- **Implications**:
  - article-facilitator は `## ArticleContext` という見出しを持つ Markdown ブロックを出力の最後に必ず含める
  - article-writer は会話履歴から `## ArticleContext` を探してから生成を開始する
  - article-reviewer も同様に ArticleContext と ArticleDraft の両方を会話から参照する

---

## Architecture Pattern Evaluation

| オプション | 説明 | 強み | リスク / 制限 | 備考 |
|-----------|------|------|--------------|------|
| 単一スキル | 1つの SKILL.md ですべての役割をカバー | 実装が最もシンプル | モノリシック、ToBe 7役への拡張が困難 | v1 限定の場合のみ検討可 |
| **パイプライン（フェーズゲート）** | 3スキルを順次実行、各フェーズで承認ゲート | フェーズ分離明確、ToBe 拡張容易、要件 2.5 を自然に実現 | ユーザーが各フェーズを明示的に進める必要あり | **採択** |
| 完全自律マルチエージェント | スキルがサブエージェントを起動して並列処理 | ToBe ビジョンに最も近い | v1 には過剰、設計複雑度が高い | v2+ で検討 |

---

## Design Decisions

### Decision: パイプラインパターン with フェーズゲートの採択

- **Context**: 要件 2.5「While 構成案の合意が取れていないとき、Article Agent shall 本文ドラフト生成を開始しない」という明示的なフェーズゲート要件がある
- **Alternatives Considered**:
  1. 単一スキル — シンプルだが 7役 ToBe への拡張が困難
  2. 完全自律マルチエージェント — ToBe ビジョンに近いが v1 には複雑すぎる
- **Selected Approach**: 3スキル（article-facilitator / article-writer / article-reviewer）をパイプライン構成で実装
- **Rationale**: フェーズ分離が要件 2.5 のフェーズゲートを自然に実現し、かつ ToBe の 7役への段階的拡張に適している
- **Trade-offs**: ユーザーが各スキルを明示的に呼び出すか、description による自動起動に依存する
- **Follow-up**: 各スキルの description を最適化して自動起動精度を検証する

---

### Decision: ArticleContext を Markdown ブロックとして会話に埋め込む

- **Context**: スキル間で状態（テーマ・読者・目的・構成案）を受け渡す必要がある。Claude Code Skills はデータベースや typed state を持たない。
- **Alternatives Considered**:
  1. JSON オブジェクト出力 — 機械可読性は高いが、ユーザーが確認・編集しにくい
  2. Markdown 構造化ブロック — 視認性・編集性が高く、コピー&ペースト適性もある
- **Selected Approach**: `## ArticleContext` という見出しを持つ Markdown ブロックを会話に出力
- **Rationale**: Claude Code Skills の会話インターフェース paradigm と整合し、ユーザーが確認・修正しやすい
- **Trade-offs**: JSON より機械的なパース精度はやや低いが、ユーザーレビューと編集のしやすさが上回る
- **Follow-up**: ArticleContext フォーマットを article-facilitator/SKILL.md に正規定義として記述する

---

### Decision: v1 は外部 API を使用しない（Markdown のみ出力）

- **Context**: 要件 6.1-6.5（スコープ外）で外部 Web 調査・画像生成・CMS 自動投稿を明示的に除外
- **Selected Approach**: すべての入出力は Markdown テキストのみ。外部 API 呼び出しなし。
- **Rationale**: スコープを絞ることで v1 の品質安定化に集中できる。外部依存がないため障害リスクもゼロ。
- **Trade-offs**: 事実確認は「リスト提示」に留まり、自動確認はできない
- **Follow-up**: v2.0 で WebSearch 連携を設計する際に本判断を再評価する

---

## Risks & Mitigations

- **コンテキストドリフト**: article-writer が ArticleContext を正しく読み取れない場合、構成とドラフトがずれる → `## ArticleContext` の区切りフォーマットを厳格に定義し、article-writer の SKILL.md で「最後の ArticleContext ブロックを参照」と明記する
- **品質のばらつき**: 同じ入力でも異なる品質のドラフトが生成される → article-writer/template.md で出力構造を厳格に定義することで一貫性を確保する
- **フェーズゲートのバイパス**: ユーザーが facilitation をスキップして article-writer を直接呼び出す → article-writer の SKILL.md で「ArticleContext ブロックが会話になければ先にファシリテーションを実行」と定義する
- **reviewer の越権**: article-reviewer がレビューを超えてドラフトを書き換える → article-reviewer/checklist.md で「read-only、コメントのみ提示」の役割制約を明記する
- **サムネイルプロンプトのツール依存性**: Nanobanana のプロンプト形式を調査済み（OQ-1 解決）。自然言語叙述文形式が正解であることを確認。テキストは直接レンダリング可能なため、具体的な文字内容・スタイル・位置の指定が有効。

---

## Open Questions（v2 article-thumbnail）

### OQ-1: Nanobanana のプロンプト仕様 【解決済み 2026-03-06】

- **結論**:
  - Nanobanana = Google DeepMind の Gemini 画像生成モデルのコードネーム（Gemini 3 Pro Image）
  - **形式**: 自然言語叙述文。タグの羅列（"dog, park, 4k"）は NG
  - **推奨構造**: Subject → Composition → Action → Style → Lighting → Constraints の順
  - **テキストレンダリング**: 画像内テキストを直接描画可能。文字内容・フォント・位置・サイズを文章で指定できる（Pro の強み）
  - **サムネイル適性**: テキストオーバーレイ（太字・白縁取り・ドロップシャドウ）・構図制御が得意
- **設計への反映**:
  - `ThumbnailPromptElements.textLayout` は「意図のみ」ではなく「テキスト内容・スタイル・位置を具体的に記述する」に変更
  - 要件 6.3・design.md の注記を修正（「ツール側依存」→「直接指定可能」）
- **Sources**:
  - [Nano-Banana Pro: Prompting Guide & Strategies - DEV Community](https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n)
  - [Gemini 3 Pro Image – Google DeepMind](https://deepmind.google/models/gemini-image/pro/)
  - [Nano Banana Pro Prompt Guide - Leonardo.Ai](https://leonardo.ai/news/nano-banana-prompt-guide/)

---

## References

- Claude Code Skills ドキュメント: https://docs.anthropic.com/en/docs/claude-code/slash-commands
- EARS フォーマットガイドライン: `.kiro/settings/rules/ears-format.md`
- cc-sdd リポジトリ: https://github.com/gotalab/cc-sdd
- ChatGPT との事前設計相談記録（2026-03-04）
