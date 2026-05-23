# MkDocs + PlantUML 日本語執筆環境

このプロジェクトは、VS CodeのDevContainerを使用して、日本語対応のMkDocsドキュメント執筆環境を即座に構築するためのテンプレートです。

## セットアップ方法

1.  このディレクトリをVS Codeで開きます。
2.  「Reopen in Container」のポップアップが表示されたら選択するか、コマンドパレットから `Dev Containers: Reopen in Container` を実行します。
3.  コンテナの起動完了後、ターミナルで以下のコマンドを実行してプレビューを開始します。
    ```bash
    mkdocs serve -a 0.0.0.0:8000
    ```
4.  ブラウザで `http://localhost:8000` にアクセスします。

## 構成

- `.devcontainer/`: VS Codeの開発コンテナ設定
- `mkdocs.yml`: MkDocsの設定（PlantUMLプラグイン設定済み）
- `docs/`: ドキュメントのソースファイル（Markdown）

## 使用可能なプラグイン

- **Material for MkDocs**: 美しいテーマ
- **PlantUML Markdown**: ` ```plantuml ` ブロックで図を描画
- **i18n**: 日本語対応設定

## 静的HTMLの出力方法（配布用）

サーバーを起動せずに、配布用の静的HTMLファイル一式を出力するには以下のコマンドを実行します。

```bash
mkdocs build
```

実行後、プロジェクト直下に `site/` ディレクトリが生成されます。このディレクトリ内のファイル一式をWebサーバーにアップロードするか、そのまま配布することで閲覧が可能です。

> **注意**: PlantUMLの図はビルド時に画像として埋め込まれる（またはリンクされる）ため、`site/` ディレクトリをそのまま配布するだけで図も表示されます。
