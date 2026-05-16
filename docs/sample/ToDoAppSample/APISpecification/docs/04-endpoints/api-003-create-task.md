# API-003 タスク新規登録

## 概要

| 項目 | 内容 |
|------|------|
| メソッド | `POST` |
| パス | `/tasks` |
| 説明 | タスクを新規登録する |

## リクエストボディ例

```json
{
  "title": "牛乳を買う",
  "description": "仕事帰りにスーパーで購入する",
  "priority": 2,
  "dueAt": "2026-04-26T18:00:00+09:00",
  "labelIds": ["LBL-001"]
}
```

## レスポンス例

```json
{
  "taskId": "TSK-000123",
  "result": "created"
}
```

## バリデーション

- `title` は必須
- `priority` は `1` から `3`
- 未登録の `labelIds` が含まれる場合は `400 Bad Request`
