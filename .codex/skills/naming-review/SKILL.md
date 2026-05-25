---
name: naming-review
description: 命名規則ガイドラインに沿って、設計、実装、差分、ファイル名の名前付けをレビューするときに使う。禁止略語、曖昧語、Async suffix、動詞の使い分け、DTO変換名の確認が必要なときに向く。
---

# Naming Review

このスキルは、リポジトリ共通の命名規則をレビューや設計相談に使うためのものです。

## まず参照するもの

- `.codex/shared/naming-guidelines.md`

必要に応じて、要件整理や設計資料に書かれたドメイン語彙も確認すること。

## 使う場面

- 差分や PR の命名だけを重点的に見たい
- 設計段階でクラス名、DTO 名、メソッド名の候補を整理したい
- `Get` / `Find` / `Search` の使い分けを確認したい
- `Save` / `Persist`、`Load` / `Read`、`ConvertTo` / `To` の使い分けを確認したい
- 禁止略語や曖昧語を機械的に洗い出したい

## 進め方

1. まず `.codex/shared/naming-guidelines.md` を読み、今回関係する規則だけに絞る
2. 対象が差分なら、変更された型名、メソッド名、プロパティ名、変数名、ファイル名を優先して見る
3. 対象が設計なら、公開 API、DTO、主要ユースケースの命名候補を先に揃える
4. 指摘時は、違反ルール、問題点、推奨リネームを 1 セットで出す
5. 既存互換性のために残す名前と、今すぐ直すべき名前を分ける

## 補助コマンド

禁止略語、曖昧語、`Build`、`Check`、`Async` の一部ルールは補助スクリプトで確認できる。

```bash
python3 .codex/skills/naming-review/scripts/check_naming_guidelines.py
```

特定パスだけを見る場合:

```bash
python3 .codex/skills/naming-review/scripts/check_naming_guidelines.py src tests
```

JSON 出力にする場合:

```bash
python3 .codex/skills/naming-review/scripts/check_naming_guidelines.py --json
```

## 出力ルール

- まず hard violation を列挙する
- 次に rename suggestion を出す
- ルール違反でないが迷いやすい名前は open question として分ける
- 推奨名は、できるだけ既存のドメイン語彙に揃える
