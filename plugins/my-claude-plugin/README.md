# my-claude-plugin

記事作成ワークフローを支援する Claude Code スキル集です。

企画・タイトル提案・執筆・レビュー・編集指示・サムネイル生成の各工程をスキルとして提供し、一貫した記事制作フローを実現します。

## スキル一覧

| スキル | 役割 | 入力 | 出力 |
|--------|------|------|------|
| [article-facilitator](./skills/article-facilitator/) | 企画・構成のファシリテート | ユーザーとの対話 | ArticleContext |
| [article-title-suggestion](./skills/article-title-suggestion/) | タイトル候補・評価・確定 | ArticleContext / 本文 | 候補・確定タイトル付き ArticleContext |
| [article-writer](./skills/article-writer/) | 本文ドラフト生成 | ArticleContext | ArticleDraft |
| [article-reviewer](./skills/article-reviewer/) | ドラフトのレビュー（読み取り専用） | ArticleDraft | レビューコメント・事実確認リスト |
| [article-editor](./skills/article-editor/) | 編集指示の挿入（読み取り専用） | ArticleDraft | 注釈付きドラフト |
| [article-thumbnail](./skills/article-thumbnail/) | サムネイルプロンプト生成 | ArticleContext / ArticleDraft | 画像生成プロンプト（3パターン以上） |

## ディレクトリ構成

```
my-claude-plugin/
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

## 推奨フロー

```
/my-claude-plugin:article-facilitator  →  /my-claude-plugin:article-writer  →  /my-claude-plugin:article-reviewer
                                          →  /my-claude-plugin:article-editor
                                          →  /my-claude-plugin:article-thumbnail
```

1. `/my-claude-plugin:article-facilitator` — 記事の企画・構成を固め、**ArticleContext** を出力する
2. `/my-claude-plugin:article-writer` — ArticleContext をもとに本文ドラフト（**ArticleDraft**）を生成する
3. 必要に応じて以下のスキルを並行して実行する
   - `/my-claude-plugin:article-reviewer` — 5観点でレビューし、事実確認リストを作成する
   - `/my-claude-plugin:article-editor` — 画像・図表・コールアウトの挿入箇所に編集指示を追加する
   - `/my-claude-plugin:article-thumbnail` — サムネイル用の画像生成プロンプトを 3パターン以上生成する

各スキルは前工程の成果物（ArticleContext / ArticleDraft）が会話履歴に存在するかをフェーズゲートで確認します。存在しない場合は前工程スキルの実行を案内します。

## タイトル提案の統合

`/my-claude-plugin:article-title-suggestion` を企画後または執筆後に任意で実行できます。5件以上の候補、3軸の参考スコア、フィードバックによる3件以上の派生案を提示し、ユーザーの明示的な決定後に確定タイトルを引き継ぎます。

Markdown の `タイトル（確定）` と JSON の `title` は同じ値です。writer は確定タイトルをそのまま使い、reviewer・editor・thumbnail も最新値を参照します。執筆後に確定した場合は writer に「確定タイトルを反映して」と依頼するとタイトル部分のみ更新します。タイトル提案を省略した従来のフローも使えます。

詳細: [受け渡し契約](./references/article-context.md) / [統合検証](./docs/integration-verification.md) / [設計履歴](./docs/archive/README.md) / [サンプル](./examples/)

## 実会話での検証

タイトル提案・短縮案・確定から執筆、レビュー、編集、サムネイルまで、Claude Code上の同一会話で確認済みです。検証範囲・実応答・再照合手順は [実会話検証](./docs/live-flow-verification.md) を参照してください。
