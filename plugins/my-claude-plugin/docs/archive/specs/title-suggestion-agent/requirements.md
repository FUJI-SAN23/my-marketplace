# Requirements Document

## Project Description (Input)
タイトルを提案するエージェントの作成

## Introduction
本仕様は、記事・文書のコンテンツを入力として受け取り、適切なタイトル候補を複数提案するAIエージェントの要件を定義する。エージェントはユーザーのフィードバックを反映して提案を改善し、最終的に選択しやすい形式でタイトルを提示する。article-facilitator / article-writer などの既存スキルと連携し、記事制作ワークフローの一部として機能することを想定する。

## Requirements

### Requirement 1: コンテンツ入力と解析
**Objective:** As a コンテンツ作成者, I want エージェントに記事本文・要約・キーワードなどのコンテンツ情報を渡せる, so that 入力内容に合致したタイトルを提案してもらえる

#### Acceptance Criteria
1. When ユーザーが記事本文またはArticleContextを提供したとき, the Title Suggestion Agent shall テキストを解析してトピック・キーワード・文体を抽出する
2. When 本文に加えてターゲット読者・媒体・トーンが指定されたとき, the Title Suggestion Agent shall それらの条件を提案生成時に優先的に反映する
3. If 入力テキストが空または著しく短い（100文字未満）とき, the Title Suggestion Agent shall 不足情報の補完を求めるメッセージをユーザーに提示する
4. The Title Suggestion Agent shall ArticleContext（article-facilitatorが出力するJSONスキーマ）を入力フォーマットとしてサポートする

### Requirement 2: タイトル候補の生成
**Objective:** As a コンテンツ作成者, I want 複数のタイトルバリエーションを一度に受け取れる, so that 最適な表現を選択・比較できる

#### Acceptance Criteria
1. When コンテンツ解析が完了したとき, the Title Suggestion Agent shall 異なるアプローチ（問いかけ型・断言型・ノウハウ型・数字型など）で最低5件のタイトル候補を生成する
2. The Title Suggestion Agent shall 各候補に対してアプローチの種別と選定理由を1〜2文で付記する
3. When ユーザーが特定のスタイル（例：「SEO重視」「キャッチコピー風」）を指定したとき, the Title Suggestion Agent shall 指定スタイルに特化した追加候補を3件以上生成する
4. The Title Suggestion Agent shall 生成する各タイトルを40文字以内に収める（日本語の場合）

### Requirement 3: 提案の評価・スコアリング
**Objective:** As a コンテンツ作成者, I want 各タイトル候補の品質評価を確認できる, so that 根拠を持って最終タイトルを決定できる

#### Acceptance Criteria
1. The Title Suggestion Agent shall 各候補に対してクリック誘引度・明瞭さ・コンテンツ整合性の3軸でスコア（1〜5）を算出する
2. When スコアリングが完了したとき, the Title Suggestion Agent shall 総合スコアの高い順にタイトルを並べて表示する
3. If いずれの候補も総合スコアが3未満のとき, the Title Suggestion Agent shall 品質基準を満たす候補が不十分である旨を警告し、追加生成を提案する

### Requirement 4: ユーザーフィードバックへの対応
**Objective:** As a コンテンツ作成者, I want 気に入った候補を基にさらに改善・派生案を生成してもらえる, so that 反復的に最適なタイトルへ近づけられる

#### Acceptance Criteria
1. When ユーザーが特定の候補を選択してフィードバック（例：「もっと短く」「疑問形にして」）を与えたとき, the Title Suggestion Agent shall そのフィードバックを反映した派生候補を3件以上生成する
2. When ユーザーが「これで決定」と確定操作をしたとき, the Title Suggestion Agent shall 選択されたタイトルをArticleContextのtitleフィールドに反映した更新済みコンテキストを出力する
3. The Title Suggestion Agent shall 1セッション内での提案履歴を保持し、ユーザーが過去の候補に戻れるようにする

### Requirement 5: 出力フォーマットと統合
**Objective:** As a 記事制作ワークフロー, I want タイトル提案結果を後続スキルで利用可能な形式で受け取れる, so that article-writer / article-editor などのスキルとシームレスに連携できる

#### Acceptance Criteria
1. The Title Suggestion Agent shall 最終出力をMarkdown形式とArticleContext JSON形式の両方で提供する
2. When article-writerまたはarticle-facilitatorのArticleContextが入力として渡されたとき, the Title Suggestion Agent shall 既存フィールドを保持しつつtitleフィールドのみを更新したArticleContextを返す
3. Where 複数言語対応が有効なとき, the Title Suggestion Agent shall 指定言語でタイトル候補を生成する（デフォルト：日本語）
4. The Title Suggestion Agent shall レスポンスを60秒以内に返す
