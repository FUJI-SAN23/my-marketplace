# Research & Design Decisions

---
**Purpose**: Capture discovery findings, architectural investigations, and rationale that inform the technical design.

---

## Summary

- **Feature**: `title-suggestion-agent`
- **Discovery Scope**: Extension（既存 article-agent パイプラインへの新スキル追加）
- **Key Findings**:
  - 既存パイプラインは Claude Code Skills（SKILL.md）パターンで統一されており、新スキルは同パターンで追加可能
  - ArticleContext は会話履歴への Markdown ブロック埋め込みで状態共有されており、title-suggestion-agent も同方式を踏襲する
  - `ArticleDraft.titleCandidates` に3件のタイトルが存在するが専用評価機能がなく、title-suggestion-agent が補完する立ち位置
  - ArticleContext の既存スキーマに `title` フィールドが存在しないため、オプションフィールドとして拡張が必要

## Research Log

### 既存 ArticleContext スキーマの調査

- **Context**: 要件 4.2 / 5.2 が「ArticleContext の title フィールドを更新」と定めているが、既存スキーマに title フィールドが見当たらない
- **Sources Consulted**: `.kiro/specs/article-agent/design.md` の Logical Data Model
- **Findings**:
  - `ArticleContext` は theme / targetAudience / purpose / keyMessages / primaryExperiences / style / outline / confirmedAt の8フィールドで構成
  - `titleCandidates` は `ArticleDraft` に存在（3本固定）
  - ArticleContext 側に確定タイトルを保持するフィールドは未定義
- **Implications**: ArticleContext インターフェースに `title?: string` をオプションフィールドとして追加する拡張が必要。既存スキルの後方互換性は optional 定義で担保できる

### 既存スキルの統合パターン調査

- **Context**: title-suggestion-agent をパイプラインのどこに位置付けるか
- **Sources Consulted**: `.claude/skills/article-facilitator/SKILL.md`、`.kiro/specs/article-agent/design.md`
- **Findings**:
  - スキルはすべて `description` キーワードによる自動起動を採用
  - 状態共有は会話内 Markdown ブロック（ArticleContext / ArticleDraft）
  - article-writer は既に3本のタイトル案を生成するが、スコアリング・反復改善はサポートしていない
- **Implications**: title-suggestion-agent は article-writer の後または独立して起動できる補完スキルとして位置付ける。フロー内で必須ではなくオプショナル

### スコアリング手法の検討

- **Context**: 要件 3.1 はクリック誘引度・明瞭さ・コンテンツ整合性の3軸スコアリングを要求
- **Findings**:
  - 外部 API（SEO ツール等）を使わずに LLM 自身が評価を行うことが、コスト・導入複雑性の観点で最適
  - スコアは LLM の出力として構造化（1〜5 の整数）し、根拠を自然言語で付記する
  - 客観スコアではなく相対評価であることをユーザーに明示することでリスクを低減できる
- **Implications**: scoring は LLM 内部評価として設計し、外部依存ゼロを維持する

## Architecture Pattern Evaluation

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| 独立スキル（採用） | 既存パイプラインとは独立して起動可能な Claude Code Skill | 既存スキルへの変更不要、任意のタイミングで起動可能 | パイプライン全体の整合性は利用者責任 | 既存 article-agent パターンと一貫性が高い |
| article-writer 内統合 | article-writer のタイトル生成ロジックを拡充 | 1スキルで完結 | article-writer の責務が増大、単一責任原則に反する | 採用しない |
| 外部スコアリング API 連携 | SEO ツール・見出し分析 API を活用 | 客観指標の取得 | 外部依存・コスト・認証管理が必要、v1 のスコープを超える | 将来検討 |

## Design Decisions

### Decision: ArticleContext への title フィールド追加

- **Context**: 確定タイトルをワークフロー全体で共有するフィールドが必要
- **Alternatives Considered**:
  1. ArticleDraft.titleCandidates の先頭要素を確定タイトルとして扱う
  2. ArticleContext に `title?: string` を追加する
- **Selected Approach**: `ArticleContext` に `title?: string` をオプションフィールドとして追加
- **Rationale**: ArticleContext は記事の「確定情報」を保持する集約ルートであり、確定タイトルはここに置くのが意味的に正しい。既存スキルは optional フィールドを無視するため後方互換性も維持できる
- **Trade-offs**: ArticleContext スキーマの変更が必要だが、既存スキルへの影響はゼロ
- **Follow-up**: article-writer と article-thumbnail の SKILL.md に「title フィールドが設定されている場合はそれを最終タイトルとして参照する」旨を追記することを推奨

### Decision: セッション履歴の保持方式

- **Context**: 要件 4.3 は「1セッション内での提案履歴を保持し、ユーザーが過去の候補に戻れるようにする」
- **Alternatives Considered**:
  1. 会話内に `## TitleSuggestionSession` ブロックを都度出力して状態を保持（他スキルと同じ方式）
  2. JSON 形式でセッション状態をファイルに書き出す
- **Selected Approach**: 会話内 Markdown ブロックへの都度出力
- **Rationale**: 既存スキルと一貫性を保つ。外部ファイル依存を避けることで環境差異を排除できる
- **Trade-offs**: 会話が長くなるとコンテキストウィンドウを消費するが、タイトル提案程度のデータ量では問題にならない

## Risks & Mitigations

- LLM スコアリングの主観性 — ユーザーへの「参考指標」と明示し、最終判断はユーザーに委ねることを SKILL.md に明記する
- article-facilitator / article-writer が未実行の状態での起動 — 入力バリデーションで ArticleContext または記事本文の存在を確認し、不足時は前工程への案内メッセージを返す（要件 1.3）
- 40文字制限（日本語）の厳密適用 — LLM が制限を超えるタイトルを生成した場合、SKILL.md に「40文字を超える場合は自動的に短縮する or 短縮候補を提示する」と明記する

## References

- 既存設計ドキュメント: [article-agent/design.md](../article-agent/design.md)
- 既存スキル定義: [article-facilitator/SKILL.md](../../../.claude/skills/article-facilitator/SKILL.md)
