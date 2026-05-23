---
name: cyclomatic-complexity
description: C#、Kotlin、Java、Python のサイクロマティック複雑度を Lizard ベースで解析するときに使う。複雑度の高い関数の抽出、閾値超過の洗い出し、差分対象だけの確認、改善候補の要約が必要なときに向く。
---

# Cyclomatic Complexity

このスキルは、Lizard を使って C#、Kotlin、Java、Python のサイクロマティック複雑度を揃えて確認するためのものです。
専用のサブエージェント `complexity_analyst` から使う前提にします。

## 使う場面

- 複雑度の高い関数を上位から確認したい
- 閾値を超えるメソッドだけを一覧したい
- PR や差分対象だけを軽く確認したい
- リファクタリング候補を機械的に抽出したい

## 前提

- `lizard` が使えること
- 未導入なら次を実行

```bash
python3 -m pip install lizard
```

## まず実行するコマンド

リポジトリ全体を解析する場合:

```bash
python3 .codex/skills/cyclomatic-complexity/scripts/analyze_complexity.py
```

差分対象だけを解析する場合:

```bash
python3 .codex/skills/cyclomatic-complexity/scripts/analyze_complexity.py --mode diff --git-ref origin/main
```

閾値を 15 にして上位 20 件を見る場合:

```bash
python3 .codex/skills/cyclomatic-complexity/scripts/analyze_complexity.py --threshold 15 --top 20
```

JSON も保存する場合:

```bash
python3 .codex/skills/cyclomatic-complexity/scripts/analyze_complexity.py --json-out complexity-report.json
```

## Codex の進め方

1. まず対象範囲を決める
2. `complexity_analyst` がスクリプトを実行する
3. 閾値超過と上位 hotspot を確認する
4. 高複雑度の理由を読み、分割案や条件整理案を提案する
5. 必要なら `diff` モードで変更影響だけ再確認する

## 既定の見方

- `1-10`: 許容
- `11-15`: 注意
- `16-20`: 高い
- `21+`: 要改善

## 注意点

- 生成物は除外する
  - `bin/`, `obj/`, `build/`, `dist/`, `.venv/`, `node_modules/`
- 複雑度は警告の入口であり、単独で品質を断定しない
- 大きな `switch` や分岐表現は、仕様都合で複雑度が上がる場合がある
