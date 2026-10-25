# Bibliotheca 統合検証 — 2026-10-25

## 再確認した差分と統合内容

共通のスキル関連9ファイルは6件一致、writer・reviewer・thumbnailの3件に確定タイトル対応の差分があった。タイトル提案スキルは固有だが、解析から確定までの5工程はコメントのみだった。設計書をもとに指示を補完した。

- article-title-suggestion のディレクトリ名・frontmatter・呼び出し名を一致させた。
- 6スキルで共通の [受け渡し契約](../references/article-context.md) を参照する。
- writer のテンプレート、thumbnail のドラフトなし分岐、editor の原文保持を含めて確定タイトルを扱う。
- JSONとMarkdown、未知フィールドの保持、確定値の衝突、未確定の従来動作、執筆後の確定を定義した。
- 元設計の到達不能な警告条件を平均点1〜5で修正した。
- [設計履歴](archive/README.md)、A〜Dサンプルを保存し、[E](../examples/input/scenario-e.md)・[F](../examples/input/scenario-f.md)の参照入出力を追加した。

## 検証の区別

静的検証はパッケージ構造・記述の整合性の確認。E/Fは期待出力であり、Claude Codeによる生成ログではない。旧レポートのチェックマークも今回の動作確認を意味しない。

## 手動回帰シナリオ（統合時の計画。実施済み範囲は実会話検証を参照）

| ケース | 期待結果 |
|---|---|
| 入力なし・本文99文字 / 100文字 | 前者は停止、100文字は候補生成 |
| 有効なContext＋短い本文 / 空Context | 前者は生成、後者だけなら停止 |
| 通常 / スタイル指定 | 5件以上 / さらに3件以上、40文字以内、理由・3軸・平均付き |
| 全候補平均3未満 / 同点 | 品質警告 / 整合性、IDの順に決定 |
| 派生案・過去ラウンド参照 | 3件以上、IDと履歴を保持 |
| 好意的反応 / 曖昧な確定 | 未確定のまま / 対象確認 |
| Markdown / JSON確定 | タイトルのみ更新、他フィールド・未知キー保持 |
| 二つの表現が競合 | 採用値を確認する |
| title空・null・未指定 | writerは従来3案、thumbnailは従来分岐 |
| 確定タイトルあり・構成未承認 | writerは停止、確認日時を捏造しない |
| 確定済み・ドラフトなし | writerの別案行なし、thumbnailは確定値を第一候補にする |
| 執筆後の確定 | titleスキルは本文を保持、writerに反映依頼時だけH1・別案行を変更 |
| reviewer / editor | 最新タイトルを参照、本文不一致を指摘し原文を保持 |
| 本文のみで確定 | サマリーと履歴のみ、架空のContextなし |

## 静的検証コマンド

リポジトリルートから実行する。Python検証にはPyYAMLが必要。

```sh
claude plugin validate .
claude plugin validate plugins/my-claude-plugin
python3 plugins/my-claude-plugin/scripts/validate_integration.py
git diff --check
```

統合直後は動的検証未実施だった。その後の実行範囲・実応答は [実会話検証](live-flow-verification.md) に記録。全シナリオ網羅や応答時間の保証は行わない。インストール・公開・pushは実施していない。

## 今回の静的検証結果

- Claude CLI の marketplace・plugin validate: 両方とも成功（警告あり）。
- 名前・frontmatter・相対リンク・E/F参照データ: 成功。
- 警告は既存のプラグイン名 `my-claude-plugin` が公式製品名に似る点と、既存manifestのversion未指定。既存の識別子とバージョン運用を保つため変更していない。インストール行に関する助言も表示された。
- 統合元は変更せず、削除・移動なし。Git履歴のマージは行わずファイル単位で統合した。

### 実行環境と最終確認

統合先の既定PythonではPyYAML未導入によるModuleNotFoundErrorが発生した。PyYAML導入済みのPython 3.10.19で同じ統合先スクリプトを実行して成功した。再現時は使用するPython環境に `python3 -m pip install PyYAML` で依存関係を用意する（今回、環境へのインストールは行っていない）。

統合先で `git diff --check` は成功。統合元は全ファイルのSHA-256比較で変更なしを確認した。変更は既存11ファイルの更新と31ファイルの追加。コミット・push・公開は行っていない。

## 追記: 実会話検証

2026-10-25、同一セッション8ターンと独立3ケースを実行し、タイトル提案から後続工程への受け渡しを確認した。スキル修正を要する不具合なし。詳細・実応答・未実施ケースは [実会話検証](live-flow-verification.md) を参照。
