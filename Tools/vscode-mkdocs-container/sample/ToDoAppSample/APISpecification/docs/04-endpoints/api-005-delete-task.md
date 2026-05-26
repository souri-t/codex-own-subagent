# API-005 タスク削除

## 概要

| 項目 | 内容 |
|------|------|
| メソッド | `DELETE` |
| パス | `/tasks/{taskId}` |
| 説明 | タスクを削除する |

## リクエスト例

`DELETE /tasks/TSK-000123`

## レスポンス例

```json
{
  "taskId": "TSK-000123",
  "result": "deleted"
}
```

## 備考

- 削除済み、または存在しないタスクに対しては `404 Not Found`
