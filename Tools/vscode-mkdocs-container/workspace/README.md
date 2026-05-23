# MkDocs + PlantUML 日本語執筆環境

この README では、ドキュメントの「プレビューを開始」と「静的 HTML の出力（配布用）」の方法のみを説明します。

## サンプルプロジェクト

- sample/APISpecification: API仕様書のサンプルプロジェクト
- sample/ExternalDesign: 外部設計書のサンプルプロジェクト

## 新しいプロジェクトを開始する場合

```bash
mkdocs new my-project
cd my-project
```

### 構成

- `mkdocs.yml`: MkDocsの設定（PlantUMLプラグイン設定済み）
- `docs/`: ドキュメントのソースファイル（Markdown）


## ビルド方法

### プレビューを開始

```bash
cd my-project
mkdocs serve -a 0.0.0.0:8000
```

ブラウザで `http://localhost:8000` にアクセスしてプレビューを確認する。

### 静的HTMLの出力方法（配布用）

```bash
cd my-project
mkdocs build
```

実行後に `site/` ディレクトリが生成されます。生成された `site/` ディレクトリをそのまま配布してください。PlantUML の図はビルド時に画像として埋め込まれます。

## 使用可能なプラグイン

- **Material for MkDocs**: 美しいテーマ
- **PlantUML Markdown**: ` ```plantuml ` ブロックで図を描画
- **i18n**: 日本語対応設定
