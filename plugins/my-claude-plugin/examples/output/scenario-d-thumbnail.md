# シナリオD 出力: サムネイルプロンプト（フルパイプライン v2）

**入力**: シナリオD（ArticleContext + ArticleDraft 両方存在）
**生成スキル**: article-thumbnail
**テーマ**: 会社員が副業でコンテンツ販売を始める方法

---

## 起動宣言

```
サムネイル画像生成プロンプトの生成を開始します。

参照コンテキスト：
- ArticleContext: 存在する
- ArticleDraft:   存在する（タイトル案を参照します）
```

---

## サムネイルプロンプト案

---

### パターン 1: ビジネス成長グラフ風

**選択理由:** 「月収 500 円→3万円」という数字の変化をビジュアルで訴求することで、30代会社員の「自分にも実現できる」という期待感を刺激するパターン。ハウツー記事のサムネイルとして最も直感的に内容を伝えられる。

**プロンプト（Nanobanana / Gemini Image）:**

> A clean, professional infographic-style thumbnail featuring an upward-trending bar chart rendered in a flat design style. The bars transition from muted gray on the left to vibrant gold on the right, symbolizing income growth over four months. A small desk worker silhouette stands beside the tallest bar. Bold white text reading "副業コンテンツ販売で月3万円突破の秘訣" is placed in the upper-left quadrant with a soft dark overlay behind it for legibility. The background is a deep navy blue with a subtle diagonal grid pattern. Lighting is soft and even with a slight spotlight on the tallest bar to draw focus. Aspect ratio 16:9, no watermarks, no text clutter outside the designated area.

**要素別メモ:**
- ビジュアルイメージ: 上昇する棒グラフ（左端グレー→右端ゴールド）、小さな人物シルエット
- テキストレイアウト: 左上に太字白文字「副業コンテンツ販売で月3万円突破の秘訣」、背後に半透明ダークオーバーレイ
- カラートーン: ネイビーブルー背景、ゴールドアクセント、信頼感と成功感の演出
- 構図・余白: 右側にグラフを配置、左上1/3をテキスト領域として確保

---

### パターン 2: 体験談・リアリティ重視

**選択理由:** 「私が実際に経験した話」という一次情報の強みを活かし、人物のストーリー感でリアリティを演出するパターン。体験談を重視する読者層（自分と似た境遇の人の話を聞きたい会社員）に刺さりやすい。

**プロンプト（Nanobanana / Gemini Image）:**

> A warm, slightly cinematic thumbnail depicting a salaried worker in their early 30s sitting at a home desk in the evening, illuminated by the soft glow of a laptop screen. The person looks determined and focused, typing on a keyboard. The background blurs softly into a cozy home office environment. Bold text in a clean sans-serif font reading "「誰でも向け」をやめたら月収が変わった" appears at the top of the image in off-white, with a thin charcoal underline for emphasis. A small gold badge in the lower-right corner reads "実体験". Warm amber and muted teal color palette to evoke authenticity and calm determination. Rule-of-thirds composition with the subject occupying the right two-thirds, leaving the left upper area for the title text.

**要素別メモ:**
- ビジュアルイメージ: 夜の自宅デスクで作業する30代会社員、ノートPC画面の光
- テキストレイアウト: 上部にオフホワイトの太字「「誰でも向け」をやめたら月収が変わった」、細いアンダーライン付き
- カラートーン: ウォームアンバー＋ミュートティール、温かみと誠実さの演出
- 構図・余白: 三分割法で人物を右2/3、左上をテキスト領域に開ける

---

### パターン 3: ステップ・ロードマップ感

**選択理由:** 「5ステップ」という構成案をビジュアルで表現し、「手順が明快で実行できる」という安心感を与えるパターン。ハウツー系記事を探している読者が「具体的な手順を教えてくれそう」と感じやすい。

**プロンプト（Nanobanana / Gemini Image）:**

> A flat design thumbnail with five numbered circular icons arranged in a horizontal flow from left to right, connected by thin arrow lines. Each circle contains a simple icon representing a step: a magnifying glass, a target cursor, a pencil, a rocket, and a checkmark. The background is a clean white with a light sky-blue gradient at the top. Bold black text reading "副業コンテンツ販売を始める5ステップ" sits prominently at the top-center in a sans-serif typeface at approximately 48pt equivalent. Below the main title, smaller text reads "会社員向け完全ガイド" in mid-gray. The style is modern and clean, suitable for a business how-to article. No photographs, icon-based illustration only. Ample white space at the bottom for breathing room.

**要素別メモ:**
- ビジュアルイメージ: 5つのステップアイコンを矢印でつないだフラットデザイン図解
- テキストレイアウト: 上部中央に太字「副業コンテンツ販売を始める5ステップ」（約48pt相当）、その下に「会社員向け完全ガイド」を小さく
- カラートーン: 白背景＋スカイブルーグラデーション、クリーンで読みやすい印象
- 構図・余白: 上部1/4をタイトル領域、中央にアイコン列、下部に余白

---

## サムネイル掲載テキスト候補

ArticleDraft のタイトル案を参照して、サムネイル向けに短縮・調整したテキストを提案します。

| # | テキスト案 | 文字数 | 推奨パターン |
|---|-----------|--------|------------|
| 1 | 副業コンテンツ販売で月3万円突破の秘訣 | 18字 | パターン 1 |
| 2 | 「誰でも向け」をやめたら月収が変わった | 19字 | パターン 2 |
| 3 | 副業コンテンツ販売を始める5ステップ | 17字 | パターン 3 |

*サムネイルのテキストは16〜24字以内を目安にしています。*

---

## 検証チェックリスト

- [x] 3パターンのプロンプトが生成された（要件 6.5）
- [x] 各パターンにコンセプト名が付与されている（要件 6.6）
- [x] 各パターンに選択理由が付与されている（要件 6.6）
- [x] ビジュアルイメージ・テキストレイアウト・カラートーン・構図余白の4要素が含まれる（要件 6.3）
- [x] ArticleContext のテーマ・読者・目的がコンセプトに反映されている（要件 6.4）
- [x] プロンプトが自然言語叙述文で記述されている（要件 6.7）
- [x] テキストレイアウトに表示テキスト内容・フォント・配置位置が具体的に記述されている（要件 6.7）
- [x] ArticleDraft のタイトル案を参照したテキスト候補が提案されている（要件 6.8）
- [x] ArticleContext・ArticleDraft の本文は変更されていない（read-only）
