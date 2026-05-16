---
name: drawio-designer
description: 画面設計図、構成図、画面遷移図、業務フロー図などを draw.io で作成または更新するときに使う。構造化された要件を図の計画、レイヤ構成、再利用ライブラリ、MkDocs 向け成果物へ落とし込む作業に向く。
---

# Draw.io Designer

このスキルは、draw.io を使った図の設計と運用を支援します。

## 使う場面

- 画面設計図を作りたい
- システム構成図を作りたい
- 画面遷移図や業務フロー図を整理したい
- 仕様書に埋め込む図を作りたい
- draw.io を AI と組み合わせて使いたい

## 進め方

1. まず図の入力条件を文章で揃える
2. 図の種類を選ぶ
3. ページ分割とレイヤ構成を決める
4. 再利用図形やテンプレートの必要性を判断する
5. `.drawio` ソースと export 先を決める
6. AI を使う場合は、生成後に人が意味と構造を確認する

## 最初に揃える入力

- 図の種類
- 読み手
- 目的
- スコープ
- 含める要素
- 含めない要素
- 出力形式

## 保存先

- 画面設計: `docs/diagrams/screens/`
- 構成図: `docs/diagrams/architecture/`
- フロー図: `docs/diagrams/flows/`
- export: `docs/diagrams/exports/`

## 詳細ガイド

- draw.io 運用指針: [../../.codex/shared/drawio-guidelines.md](../../.codex/shared/drawio-guidelines.md)
