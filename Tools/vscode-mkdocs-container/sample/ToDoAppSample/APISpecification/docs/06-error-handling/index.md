# エラー設計

## エラーレスポンス形式

```json
{
  "code": "TASK_NOT_FOUND",
  "message": "The specified task was not found.",
  "details": [
    {
      "field": "taskId",
      "reason": "TSK-999999 does not exist."
    }
  ]
}
```

## ステータスコード一覧

| ステータス | 用途 |
|------------|------|
| `400 Bad Request` | リクエスト形式不正、入力値不正 |
| `401 Unauthorized` | 認証失敗 |
| `403 Forbidden` | 権限不足 |
| `404 Not Found` | 対象データなし |
| `409 Conflict` | 更新競合 |
| `500 Internal Server Error` | 想定外エラー |

## 代表的な業務エラー

| エラーコード | 説明 | 発生条件 |
|--------------|------|----------|
| `TASK_NOT_FOUND` | タスクが存在しない | 指定 ID が未登録 |
| `INVALID_TASK_STATUS` | 不正な状態値 | `status` が規定外 |
| `TASK_CONFLICT` | 更新競合 | 先行更新が存在する |
| `TOKEN_EXPIRED` | トークン期限切れ | JWT の `exp` 超過 |
| `INVALID_ROLE` | 権限不足 | 要求ロールを満たさない |

## リトライ方針

- `400` `401` `403` `404` はクライアント修正後に再実行する
- `409` は最新状態を取得して再試行可否を判断する
- `500` は `X-Request-Id` を控えて運用担当へ連絡する
