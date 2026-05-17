# OwnSubagent

Codex 用の開発サブエージェント構成を管理するリポジトリです。

このリポジトリで目指すのは、1人のエージェントが全部やる構成ではなく、開発工程ごとに責務を分けたチーム構成です。中心にはオーケストレーターを置き、その配下に要件整理、設計、実装、レビュー、テスト設計の担当をぶら下げます。

## 方針

- 正本は `.codex/agents/` に置く
- GitHub Copilot 向け定義は廃止し、このリポジトリでは扱わない
- エージェントは役割ごとに単一責務で分ける
- 実装の前に、要件整理とコード設計を必ず挟む
- レビューは実装者と分離し、設計指針への準拠を独立に確認する
- 実行環境が必要な場合は、可能な限り `docker compose` で構築できる形を標準とする

## 目指す構成

```text
.codex/
  agents/
    dev-orchestrator.toml
    requirements-analyst.toml
    drawio-designer.toml
    code-architect.toml
    implementation-engineer.toml
    design-reviewer.toml
    test-designer.toml
  shared/
    design-guidelines.md
    drawio-guidelines.md
skills/
  drawio-designer/
    SKILL.md
  plantuml-design/
    SKILL.md
docs/
  index.md
  requirements/
    index.md
  specifications/
    index.md
  decisions/
    index.md
  diagrams/
    README.md
    plantuml/
    screens/
    architecture/
    flows/
    exports/
src/
  README.md
tests/
  README.md
  unit/
  integration/
  e2e/
```

## エージェント構成

### 1. `dev-orchestrator`

全体進行を担当するオーケストレーターです。

責務:
- ユーザー依頼を受け取る
- どの担当に何を渡すかを判断する
- 各担当の出力を次の担当へ引き継ぐ
- 必要に応じて差し戻しする
- 最終結果を統合してユーザーへ返す

やること:
- タスクの開始条件と終了条件を揃える
- 各サブエージェントの責務が混ざらないよう制御する
- 要件、設計、実装、レビュー、テスト設計の成果物をつなぐ

やらないこと:
- 自分で詳細設計を確定しない
- 自分で本実装を書ききらない
- 自分でレビュー判定を代行しない

### 2. `requirements-analyst`

要件を整理する担当です。

責務:
- ユーザー要求を整理する
- 目的、制約、前提、非機能要件を明確化する
- 曖昧な点を洗い出す
- 実装対象と非対象を分ける
- 完了条件を定義する

成果物の例:
- 要件サマリ
- ユースケース
- 制約一覧
- スコープ定義
- 受け入れ条件

やらないこと:
- クラス設計を決めること
- コードを書くこと
- テストケース詳細を作り込むこと

### 3. `drawio-designer`

draw.io を使った図の設計担当です。

責務:
- 画面設計図を作る
- UI レイアウトを作る
- 視覚調整が重要な構成図を作る
- 自由度の高い画面遷移図やフロー図を作る
- 仕様書に埋め込むための図のソースと export を整備する
- 図のテンプレートや再利用図形の方向性を整理する

成果物の例:
- ワイヤーフレーム
- 画面遷移図
- UI モック
- 視覚調整を伴う構成図
- 処理フロー図

やらないこと:
- コード実装を行うこと
- クラス設計を単独で確定すること
- 見た目だけ整えて意味の確認を省略すること
- PlantUML 向きの構造図や振る舞い図を主担当として抱え込むこと

### 4. `code-architect`

コード設計者です。コードは書かず、構造を考える担当です。

責務:
- 要件を満たすためのクラス設計を考える
- モジュール分割、責務分離、依存関係を設計する
- データフローとインターフェースを定義する
- システム構成やレイヤ構成を整理する
- 実装時の設計指針を明文化する
- PlantUML でクラス図、シーケンス図、状態遷移図、コンポーネント図を設計資産として残す

成果物の例:
- クラス一覧と責務
- モジュール構成
- インターフェース方針
- データの流れ
- 実装ルール
- `docs/diagrams/plantuml/` 配下の `.puml`

やらないこと:
- 本番コードを書くこと
- その場で場当たり的に設計を変えながら実装すること
- レビュー最終判定を行うこと

### 5. `implementation-engineer`

コーディング担当です。

責務:
- 要件整理と設計方針に沿って実装する
- 変更対象を必要最小限に絞る
- 既存コードとの整合を保つ
- 実装結果と設計との差分を明示する

やること:
- 必要なコード変更
- 必要最小限の補助的リファクタ
- 実装上の判断理由の記録

やらないこと:
- 要件を独断で変更すること
- 設計方針を無断で破ること
- 自分でレビュー完了扱いにすること

### 6. `design-reviewer`

コードレビュアーです。設計指針に沿っているかを確認します。

責務:
- 実装が要件整理と設計方針に従っているか確認する
- 責務分離、依存関係、境界設計の崩れを検出する
- 回帰リスクや保守性リスクを指摘する
- 指摘事項を根拠付きで返す

レビュー観点:
- 設計意図との整合
- クラス責務の過不足
- レイヤ違反や依存逆転違反
- 拡張性、保守性、可読性
- 実装都合による設計逸脱

やらないこと:
- 自分で修正コードを書く前提でレビューすること
- 要件整理の担当を兼ねること
- テスト設計を主導すること

### 7. `test-designer`

テスト設計担当です。

責務:
- 要件と設計に基づいて必要なテスト観点を整理する
- 正常系、異常系、境界値、回帰観点を設計する
- 何を自動テストにし、何を手動確認にするかを決める
- テスト不足のリスクを明示する

成果物の例:
- テスト観点一覧
- テストケース案
- 優先度付き確認項目
- 回帰確認観点

やらないこと:
- 本実装を書くこと
- 設計レビューの代替をすること
- テスト実行そのものを主責務にすること

## 関係図

```text
dev-orchestrator
├── requirements-analyst
├── drawio-designer
├── code-architect
├── implementation-engineer
├── design-reviewer
└── test-designer
```

## 基本フロー

### 標準フロー

`dev-orchestrator`
-> `requirements-analyst`
-> `drawio-designer`
-> `code-architect`
-> `implementation-engineer`
-> `design-reviewer`
-> `test-designer`
-> `dev-orchestrator`

### 設計までで止める場合

`dev-orchestrator`
-> `requirements-analyst`
-> `drawio-designer`
-> `code-architect`

### 実装レビューだけしたい場合

`dev-orchestrator`
-> `design-reviewer`

### テスト観点だけ欲しい場合

`dev-orchestrator`
-> `requirements-analyst`
-> `drawio-designer`
-> `code-architect`
-> `test-designer`

## 担当間の受け渡し

### `requirements-analyst` -> `code-architect`

渡すもの:
- 目的
- スコープ
- 制約
- 受け入れ条件

保存先:
- `docs/requirements/`

### `requirements-analyst` -> `drawio-designer`

渡すもの:
- 目的
- 読み手
- 図の種類
- スコープ
- 図に含める要素

保存先:
- `docs/diagrams/`

### `drawio-designer` -> `code-architect`

渡すもの:
- 画面設計図
- 構成図
- フロー図
- 図で明らかになった曖昧点

保存先:
- `docs/diagrams/`

### `code-architect` -> `implementation-engineer`

渡すもの:
- クラス設計
- モジュール分割
- 依存関係
- 実装ルール
- 設計上の禁止事項

保存先:
- `docs/specifications/`
- 必要に応じて `docs/decisions/`
- PlantUML 図: `docs/diagrams/plantuml/`

### `implementation-engineer` -> `design-reviewer`

渡すもの:
- 実装差分
- 設計との差分
- 妥協した点と理由

保存先:
- 実装コード: `src/`
- テストコード: `tests/`

### `code-architect` / `implementation-engineer` -> `test-designer`

渡すもの:
- 要件
- 設計意図
- 実装範囲
- リスクが高い箇所

参照先:
- `docs/requirements/`
- `docs/specifications/`
- `src/`
- `tests/`

## 開発アセット配置

### `docs/requirements/`

要件文書を置く場所です。

主に使う担当:
- `requirements-analyst`

### `docs/specifications/`

仕様書を置く場所です。

主に使う担当:
- `code-architect`
- `implementation-engineer`
- `design-reviewer`

補足:
- 後から MkDocs で管理する前提です。

### `docs/diagrams/`

draw.io で作成した図のソースと export を置く場所です。

主に使う担当:
- `drawio-designer`
- `code-architect`
- `design-reviewer`

補足:
- PlantUML の `.puml` ソースもここで管理します。
- PlantUML は構造図、振る舞い図、差分レビューしやすい設計図に使います。
- draw.io は UI、レイアウト、自由図形、視覚調整が必要な図に使います。
- 仕様書から参照する画像もここで管理します。

### `docs/decisions/`

設計判断や採用理由を記録する場所です。

主に使う担当:
- `code-architect`
- `dev-orchestrator`

### `src/`

本番コードを置く場所です。

主に使う担当:
- `implementation-engineer`

### `tests/`

テストコードを置く場所です。

主に使う担当:
- `implementation-engineer`
- `test-designer`

## 設計ルール

- 要件整理とコード設計は分離する
- コード設計者はコードを書かない
- 実装者は設計指針を勝手に変更しない
- レビュアーは設計指針への準拠確認を主責務にする
- テスト設計者は実装詳細よりも仕様とリスクを起点に考える
- オーケストレーターは役割の混線を防ぐ

## 共通設計指針

設計指針はエージェント定義に重複して直接書かず、共通ファイルで管理します。

管理場所:
- `.codex/shared/design-guidelines.md`

このファイルを共通で参照する担当:
- `dev-orchestrator`
- `code-architect`
- `implementation-engineer`
- `design-reviewer`

意図:
- 設計者、実装者、レビュアーで判断基準を揃える
- ルール変更時の修正箇所を 1 か所に集約する
- レビュー指摘と設計判断が同じ根拠に基づくようにする

含まれる方針の例:
- 型・データ構造
- 制御フロー
- null の扱い
- 実行環境は可能な限り `docker compose` を優先すること

## draw.io 運用指針

draw.io を AI と組み合わせて使うときの運用指針は共通ファイルで管理します。

管理場所:
- `.codex/shared/drawio-guidelines.md`

このファイルを主に参照する担当:
- `dev-orchestrator`
- `drawio-designer`
- `code-architect`
- 必要に応じて `design-reviewer`

意図:
- 図の作成方法を属人化させない
- AI を使った図生成の品質を安定させる
- `.drawio` ソース、テンプレート、ライブラリ、export の扱いを揃える

## ディレクトリ運用

### `.codex/agents/`

Codex 用エージェント定義の正本を置く場所です。

ここに置くもの:
- オーケストレーター
- 要件整理担当
- draw.io デザイン担当
- コード設計担当
- 実装担当
- レビュー担当
- テスト設計担当

### `.codex/shared/`

複数エージェントが共通で参照する設計指針やポリシーを置く場所です。

### `skills/`

特定の作業能力を再利用しやすい形でまとめる場所です。

現時点では、draw.io を使った図作成能力と、PlantUML を使った設計能力をスキルとして切り出しています。

運用:
- repo の `skills/` を正本とします。
- Codex に自動発見させるには `~/.codex/skills/` へ配置します。
- 更新時は repo 側を修正し、必要に応じて `~/.codex/skills/` へ同期します。

例:
```bash
mkdir -p ~/.codex/skills
cp -R skills/drawio-designer ~/.codex/skills/
cp -R skills/plantuml-design ~/.codex/skills/
```

## 現在の状態

現時点で存在する主要ファイル:

- `.codex/agents/dev-orchestrator.toml`
- `.codex/agents/requirements-analyst.toml`
- `.codex/agents/drawio-designer.toml`
- `.codex/agents/code-architect.toml`
- `.codex/agents/implementation-engineer.toml`
- `.codex/agents/design-reviewer.toml`
- `.codex/agents/test-designer.toml`
- `.codex/shared/design-guidelines.md`
- `.codex/shared/drawio-guidelines.md`
- `skills/drawio-designer/SKILL.md`
- `skills/plantuml-design/SKILL.md`

この構成だけで、要件整理から設計、実装、レビュー、テスト設計までを分担できる前提です。
