# Sample Documents

このスキルでは、まずリポジトリ内 sample を見てから書き始めることを基本とします。

## 最初に見る共通参照先

- 執筆環境の前提:
  `Tools/vscode-mkdocs-container/README.md`
- sample 全体の入口:
  `Tools/vscode-mkdocs-container/sample/ToDoAppSample/README.md`

## API 仕様書を書くとき

起点にする場所:

- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/mkdocs.yml`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/docs/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/docs/02-common-specifications/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/docs/04-endpoints/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/docs/04-endpoints/api-003-create-task.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/docs/05-data-models/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/docs/06-error-handling/index.md`

見る観点:

- `mkdocs.yml` の `nav` で章構成と粒度を合わせる
- 共通仕様は `index.md` に集約する
- エンドポイントごとの詳細は 1 API 1ページで分ける
- リクエスト例、レスポンス例、制約を固定の順で置く

向いている文書:

- REST API 仕様書
- バックエンド連携仕様
- データモデル定義
- エラー設計

## 外部仕様書や画面仕様を書くとき

起点にする場所:

- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/ExternalDesignDocument/mkdocs.yml`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/ExternalDesignDocument/docs/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/ExternalDesignDocument/docs/02-system-architecture/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/ExternalDesignDocument/docs/03-features/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/ExternalDesignDocument/docs/04-screen-design/index.md`
- `Tools/vscode-mkdocs-container/sample/ToDoAppSample/ExternalDesignDocument/docs/04-screen-design/s002-task-list.md`

見る観点:

- 機能一覧は `index.md` に寄せる
- 画面詳細は 1 画面 1ページで分ける
- レイアウト、画面要素、操作イベントを分けて書く
- 構成図や画面図は本文に埋め込んで、文章は補足に徹する

向いている文書:

- 外部仕様書
- 画面設計書
- 機能仕様書
- システム構成の説明ページ

## どちらを選ぶか迷うとき

- API の入出力と契約が中心なら API 仕様書 sample を使う
- ユーザー操作、画面、機能説明が中心なら外部仕様書 sample を使う
- 両方を同じ本に押し込めず、文書を分冊する案を先に検討する

## sample から外してよいケース

- 既存プロジェクトにすでに別の `mkdocs.yml` 構成がある
- 規約上、見出し名や章分けが固定されている
- sample の粒度では不足し、明確な追加理由がある

その場合でも、表の使い方、ページ分割、`nav` とファイル名の整合はできるだけ合わせる。
