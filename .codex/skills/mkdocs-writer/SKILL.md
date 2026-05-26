---
name: mkdocs-writer
description: MkDocs 用の仕様書、設計書、運用手順書、画面仕様、API 仕様などを作成または更新するときに使う。sample/ToDoAppSample の `mkdocs.yml` と `docs/` 配下のサンプル文書を参照しながら、見出し構成、ページ粒度、表やコードブロックの置き方を揃えて、日本語 Markdown をブレ少なく書く作業に向く。
---

# MkDocs Writer

このスキルは、MkDocs で管理する文書を、リポジトリ内の sample に寄せて一貫性高く作るためのものです。

## 使う場面

- MkDocs 用の新しい文書一式を作りたい
- 既存の `docs/` 配下にページを追加したい
- `mkdocs.yml` の `nav` を整理したい
- API 仕様書、外部仕様書、画面仕様、運用手順書を同じ調子で整えたい
- sample を参照しながら、ブレの少ない日本語 Markdown を書きたい

## 最初にやること

1. 対象の `mkdocs.yml` と `docs/` 配下の構成を確認する
2. 今書く文書がどの種別に近いかを決める
3. 近い sample を先に読む
4. sample のページ粒度と見出し構成に寄せてページを切る
5. `mkdocs.yml` の `nav` と実ファイル名を必ず同期する

sample の選び方と優先参照先は [references/sample-documents.md](references/sample-documents.md) を使うこと。

## 基本方針

- 1ページ 1責務を基本にする
- `index.md` は一覧、要約、導線に寄せる
- 詳細ページは、概要から先に書いてから詳細へ降りる
- 比較、属性、入出力、制約は文章だけで済ませず、表や箇条書きを使う
- 実データ例やリクエスト例がある場合はコードブロックで固定する
- 用語、見出し名、ファイル名、`nav` 表記を揃える
- sample から外れるのは、対象文書の都合で理由があるときだけにする

## sample の使い分け

- API 仕様書に近い場合:
  `Tools/vscode-mkdocs-container/sample/ToDoAppSample/APISpecification/`
- 画面仕様や外部仕様書に近い場合:
  `Tools/vscode-mkdocs-container/sample/ToDoAppSample/ExternalDesignDocument/`
- どちらにも近い場合:
  1冊に詰め込まず、文書を分ける案を先に検討する

## 書き方ルール

- ページタイトルは `#` で 1 つに絞る
- 大項目は `##`、必要なときだけ `###` を使う
- 表で書ける内容は、長文段落より表を優先する
- 列挙は同じ粒度で揃える
- 画面仕様は、レイアウト、主要要素、操作イベントを分けて書く
- API 仕様は、概要、リクエスト例、レスポンス例、バリデーションや制約を分けて書く
- アーキテクチャや機能一覧は、概要ページと詳細ページを分離する

必要に応じて [references/page-templates.md](references/page-templates.md) の雛形を使うこと。

## 更新時の進め方

1. 既存の `mkdocs.yml` と近いページを確認する
2. 近い sample と既存ページの両方に合わせる
3. 新規ページ追加時は、必要な `index.md` の追加も検討する
4. 関連ページ間の用語とリンクを揃える
5. `mkdocs build` や `mkdocs serve` を使える環境なら確認する

## 参照先

- sample の選定と読む順番: [references/sample-documents.md](references/sample-documents.md)
- ページ雛形: [references/page-templates.md](references/page-templates.md)
- 執筆環境の前提: [../../../Tools/vscode-mkdocs-container/README.md](../../../Tools/vscode-mkdocs-container/README.md)
