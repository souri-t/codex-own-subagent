# 図面管理

このディレクトリには、PlantUML と draw.io を使って作成する図のソースと成果物を配置します。

## 構成

- `plantuml/`
  PlantUML の `.puml` ソースを配置します。
- `screens/`
  画面設計図やワイヤーフレームの `.drawio` ソースを配置します。
- `architecture/`
  UI 以外でも、自由配置や視覚調整が重要な draw.io 図を配置します。
- `flows/`
  画面遷移や自由度の高いフロー図の `.drawio` ソースを配置します。
- `exports/`
  MkDocs や仕様書に埋め込むための `.svg` や `.png` を配置します。

## 運用ルール

- テキストベースで管理しやすい設計図は PlantUML を優先します。
- UI、レイアウト、自由図形、視覚調整が重要な図は draw.io を使います。
- PlantUML 図は `.puml` で管理します。
- draw.io 図は `.drawio` で管理します。
- 公開用や埋め込み用の画像は `exports/` に分けます。
- 図の作成方針は `.codex/shared/drawio-guidelines.md` を参照します。
- PlantUML の設計指針は `skills/plantuml-design/SKILL.md` を参照します。
