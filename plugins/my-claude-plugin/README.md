# my-claude-plugin

記事作成ワークフローを支援する Claude Code スキル集です。

企画・執筆・レビュー・編集指示・サムネイル生成の各工程をスキルとして提供し、一貫した記事制作フローを実現します。

## スキル一覧

| スキル | 役割 | 入力 | 出力 |
|--------|------|------|------|
| [article-facilitator](./skills/article-facilitator/) | 企画・構成のファシリテート | ユーザーとの対話 | ArticleContext |
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
/article-facilitator  →  /article-writer  →  /article-reviewer
                                          →  /article-editor
                                          →  /article-thumbnail
```

1. `/article-facilitator` — 記事の企画・構成を固め、**ArticleContext** を出力する
2. `/article-writer` — ArticleContext をもとに本文ドラフト（**ArticleDraft**）を生成する
3. 必要に応じて以下のスキルを並行して実行する
   - `/article-reviewer` — 5観点でレビューし、事実確認リストを作成する
   - `/article-editor` — 画像・図表・コールアウトの挿入箇所に編集指示を追加する
   - `/article-thumbnail` — サムネイル用の画像生成プロンプトを 3パターン以上生成する

各スキルは前工程の成果物（ArticleContext / ArticleDraft）が会話履歴に存在するかをフェーズゲートで確認します。存在しない場合は前工程スキルの実行を案内します。
