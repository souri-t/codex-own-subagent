---
name: code-review
description: Git のマージ先ブランチに対する merge base から HEAD までの差分を基準に、Codex でコードレビューするときに使う。レビュー対象の切り出し、差分の要約、確認順、レビュー依頼文の定型化が必要なときに向く。
---

# Code Review

このスキルは、`最終的にマージされる差分` を基準にレビュー対象を揃えるためのものです。

## 基本方針

- レビュー対象は `target branch` に対する `merge base..HEAD`
- まず `PR 全体の差分` を把握し、その後にファイル単位で深掘る
- コミット履歴は補助情報として使い、最終判断は最終差分で行う
- 差分だけで判断できない場合は、変更ファイル全体と関連呼び出し元まで読む

## 使う場面

- ブランチのレビュー対象を機械的に揃えたい
- Codex に PR レビューを依頼するときの前提を固定したい
- `main` や `develop` 向けに何をレビュー対象にするか毎回迷いたくない

## 手順

1. マージ先ブランチを決める
2. `merge base` を計算する
3. 差分の要約を確認する
4. 高リスク箇所から読む
5. 必要な関連コードとテストを読む
6. 指摘を重大度順にまとめる

## まず実行するコマンド

ターゲットブランチを明示する場合:

```bash
.codex/skills/code-review/scripts/review-diff.sh origin/main
```

ターゲットブランチを省略する場合:

```bash
.codex/skills/code-review/scripts/review-diff.sh
```

このスクリプトは以下を表示します。

- target branch
- merge base
- 対象コミット一覧
- `--stat`
- `--name-status`
- そのままレビューに使える `git diff` コマンド

## Codex への依頼文

以下の形式で依頼するとぶれにくいです。

```text
target branch は origin/main。
merge base..HEAD をレビュー対象にしてコードレビューしてください。
最初に重大な指摘を列挙し、その後に open questions と testing gaps を出してください。
差分だけで判断できない箇所は、変更ファイル全体と関連呼び出し元も確認してください。
```

## レビュー観点

- 仕様逸脱
- バグ混入
- 例外処理漏れ
- テスト不足
- パフォーマンス劣化
- セキュリティや権限の問題
- 既存呼び出し側との互換性

## 深掘りの順番

優先度が高い順:

1. public API、外部 I/F、DB schema、認可まわり
2. 分岐の多いロジック、状態遷移、非同期処理
3. テストの追加・削除・期待値変更
4. UI やドキュメントだけの変更

## 注意点

- `branch point の古い固定コミット` ではなく、`現在の target branch との merge base` を使う
- `git diff A...B` の三点記法は文脈を誤解しやすいので、レビュー時は `merge base` を明示して `base..HEAD` で考える
- generated file や lockfile を含む場合は、レビュー優先度を下げるが無視はしない
- stacked PR の場合は親 PR の先頭を `target branch` とみなす
