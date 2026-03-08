# my-marketplace

Claude Code 向けのプラグインを管理するリポジトリです。

## プラグイン

### my-claude-plugin

記事作成ワークフローを支援するスキル集です。企画・執筆・レビュー・編集指示・サムネイル生成の各工程をスキルとして提供します。

## スキル一覧

スキルはパイプライン設計になっており、前工程の成果物を次工程のスキルが参照します。

```
article-facilitator
       ↓ ArticleContext を出力
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

- タイトル案 3本・導入文・本文・まとめ・不足情報リスト・推測箇所リストを出力する
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
/article-facilitator   # 企画・構成の確定
/article-writer        # ドラフト生成
/article-reviewer      # レビュー
/article-editor        # 編集指示の挿入
/article-thumbnail     # サムネイルプロンプト生成
```

### 推奨フロー

1. `/article-facilitator` で記事の企画・構成を固め、ArticleContext を出力する
2. `/article-writer` でドラフトを生成する
3. `/article-reviewer` でレビューを受け、必要に応じて `/article-writer` で部分修正する
4. `/article-editor` で画像・図表の挿入箇所に編集指示を追加する
5. `/article-thumbnail` でサムネイル用プロンプトを生成する

各スキルは前工程の成果物（ArticleContext / ArticleDraft）が会話履歴に存在するかをフェーズゲートで確認します。存在しない場合は前工程スキルの実行を案内します。
