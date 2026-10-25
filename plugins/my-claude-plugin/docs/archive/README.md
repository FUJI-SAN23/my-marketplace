# 統合元の設計・検証資料

Bibliotheca の設計書は `specs/` に原文のまま保存した履歴資料。examples の A〜D と旧検証記録も統合元から引き継いだ。過去のチェックマークは今回の実行結果ではない。

現行仕様は [タイトル受け渡し契約](../../references/article-context.md) と各 SKILL.md、今回の検証は [統合検証](../integration-verification.md) を参照する。

旧設計との差分:
- title-suggestion-agent は設計ID・旧配置名。現行スキル名とディレクトリは article-title-suggestion。
- `.claude/skills/` は旧配置。現行はプラグイン直下の `skills/`。
- 旧設計の「合計3〜15なのに3未満で警告」は到達不能なため、現行の総合点は平均1〜5、全候補3未満で警告。
- JSON専用という旧要件に対し、現行は既存のMarkdownを標準にしてJSONも受理する。
- 元の未完了タスクは履歴のまま保持。今回追加した指示の完成とホスト上の動的検証の完了を混同しない。
- Kiro の開発コマンド・設定・steering、CLAUDE.md、package.json は記事スキルの実行に不要なため取り込まない。
