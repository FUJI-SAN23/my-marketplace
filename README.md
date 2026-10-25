# my-marketplace

Claude Code 向けのプラグインを管理するリポジトリです。

## 正本とアーカイブ

記事制作スキルの正本は、この `my-marketplace` リポジトリの `plugins/my-claude-plugin/` です。今後の機能追加・修正・検証資料の更新はここで行います。

旧 `02learning/09Bibliotheca-skills` は2026-10-25に `04_Archives/09Bibliotheca-skills` へ移動しました（パスはローカルのworkspace基準）。旧フォルダはGit履歴・原資料の参照用に保持し、開発・配布元としては使用しません。統合済みの設計履歴と検証資料はこのリポジトリにも保存されています。

## プラグイン

### my-claude-plugin

記事作成ワークフローを支援するスキル集です。企画・タイトル提案・執筆・レビュー・編集指示・サムネイル生成の各工程をスキルとして提供します。

## スキル一覧

スキルはパイプライン設計になっており、前工程の成果物を次工程のスキルが参照します。

```
article-facilitator
       ↓ ArticleContext を出力
article-title-suggestion（任意）
       ↓ 確定タイトル付き ArticleContext
article-writer
       ↓ ArticleDraft を出力
   ┌───┴───┐
article-reviewer  article-editor  article-thumbnail
```

### article-facilitator

記事の企画・構成をファシリテートし、**ArticleContext** を生成します。

- ユーザーとの対話でテーマ・想定読者・目的・構成案を確定する
- 1回のターンで最大2つまでの質問に制限し、ユーザーの負担を最小化する
- 構成案の合意が取れるまで本文生成を開始しない（フェーズゲート G1）

**起動タイミング**: 「記事の構成を考えたい」「企画を整理して」

### article-writer

ArticleContext をもとに記事の本文ドラフト（**ArticleDraft**）を生成します。

- 確定タイトル（未確定ならタイトル案3本）・導入文・本文・まとめ・不足情報リスト・推測箇所リストを出力する
- ユーザー提供の体験談・一次情報は `【一次情報】` タグで明示する
- 推測で補った箇所には `（確認要）` マーカーを付与する
- 部分修正モードをサポート（指定セクションのみ再生成）

**起動タイミング**: 「ドラフトを生成して」「本文を作成して」

### article-reviewer

ArticleDraft をレビューし、改善コメントと事実確認リストを生成します。**本文は変更しません。**

- 読みやすさ・冗長表現・論理の飛躍・抜け漏れ・要出典の 5観点でレビューする
- 数字・固有名詞・手順・規約などを事実確認リストとして一覧化する

**起動タイミング**: 「レビューして」「校正して」「事実確認リストを作って」

### article-editor

ArticleDraft に画像・図表・コールアウトなどの**編集指示（ト書き）**を挿入します。**本文は変更しません。**

- H2/H3 を走査し、checklist.md の基準に従って編集指示の種別と必要性を判定する
- 編集指示は blockquote 形式で挿入し、本文と明確に区別する
- 1セクションにつき最大 1件、全体の 50% 以内に抑える

**起動タイミング**: 「編集指示を入れて」「画像の挿入箇所を指定して」

### article-thumbnail

ArticleContext（または ArticleDraft）を参照し、サムネイル画像生成プロンプトを 3パターン以上生成します。

- Nanobanana（Gemini 画像生成）向けの英語自然言語叙述文プロンプトを出力する
- ビジュアルイメージ・テキストレイアウト・カラートーン・構図余白の 4要素を必ず含める
- ArticleDraft がある場合はタイトル案からサムネイル掲載テキスト候補も提案する

**起動タイミング**: 「サムネイルを作って」「サムネイル用のプロンプトを生成して」

## ディレクトリ構成

```
my-marketplace/
└── plugins/
    └── my-claude-plugin/
        └── skills/
            ├── article-facilitator/
            │   └── SKILL.md
            ├── article-title-suggestion/
            │   └── SKILL.md
            ├── article-writer/
            │   ├── SKILL.md
            │   └── template.md        # 出力テンプレートと表記規約
            ├── article-reviewer/
            │   ├── SKILL.md
            │   └── checklist.md       # レビュー 5観点の判定基準
            ├── article-editor/
            │   ├── SKILL.md
            │   └── checklist.md       # 編集指示の挿入判定基準
            └── article-thumbnail/
                └── SKILL.md
```

## 使い方

各スキルはスラッシュコマンドで呼び出します。

```
/my-claude-plugin:article-facilitator   # 企画・構成の確定
/my-claude-plugin:article-title-suggestion # タイトル提案・確定（任意）
/my-claude-plugin:article-writer        # ドラフト生成
/my-claude-plugin:article-reviewer      # レビュー
/my-claude-plugin:article-editor        # 編集指示の挿入
/my-claude-plugin:article-thumbnail     # サムネイルプロンプト生成
```

### 推奨フロー

1. `/my-claude-plugin:article-facilitator` で記事の企画・構成を固め、ArticleContext を出力する
2. `/my-claude-plugin:article-writer` でドラフトを生成する
3. `/my-claude-plugin:article-reviewer` でレビューを受け、必要に応じて `/my-claude-plugin:article-writer` で部分修正する
4. `/my-claude-plugin:article-editor` で画像・図表の挿入箇所に編集指示を追加する
5. `/my-claude-plugin:article-thumbnail` でサムネイル用プロンプトを生成する

各スキルは前工程の成果物（ArticleContext / ArticleDraft）が会話履歴に存在するかをフェーズゲートで確認します。存在しない場合は前工程スキルの実行を案内します。

## タイトル提案の統合

`/my-claude-plugin:article-title-suggestion` を企画後または執筆後に任意で実行できます。5件以上の候補、3軸の参考スコア、フィードバックによる3件以上の派生案を提示し、ユーザーの明示的な決定後に確定タイトルを引き継ぎます。

Markdown の `タイトル（確定）` と JSON の `title` は同じ値です。writer は確定タイトルをそのまま使い、reviewer・editor・thumbnail も最新値を参照します。執筆後に確定した場合は writer に「確定タイトルを反映して」と依頼するとタイトル部分のみ更新します。タイトル提案を省略した従来のフローも使えます。

詳細: [プラグインREADME](./plugins/my-claude-plugin/README.md) / [統合検証](./plugins/my-claude-plugin/docs/integration-verification.md)
