# API-001 タスク一覧取得

## 概要

| 項目 | 内容 |
|------|------|
| メソッド | `GET` |
| パス | `/tasks` |
| 説明 | タスク一覧を取得する |

## リクエスト

`GET /tasks?page=1&pageSize=20&status=open&sort=dueAt&order=asc`

### クエリパラメータ

| パラメータ | 必須 | 型 | 説明 |
|------------|------|----|------|
| `page` | No | integer | ページ番号 |
| `pageSize` | No | integer | 取得件数 |
| `status` | No | string | `open` `completed` `archived` |
| `labelId` | No | string | ラベルによる絞り込み |
| `keyword` | No | string | タイトル、説明の部分一致検索 |

## レスポンス例

```json
{
  "items": [
    {
      "taskId": "TSK-000123",
      "title": "牛乳を買う",
      "description": "仕事帰りにスーパーで購入する",
      "status": "open",
      "priority": 2,
      "dueAt": "2026-04-26T18:00:00+09:00",
      "updatedAt": "2026-04-25T09:30:00+09:00"
    }
  ],
  "page": 1,
  "pageSize": 20,
  "totalCount": 1
}
```

## 備考

- レスポンス形式は `PagedTasksResponse` を参照する
- 最大取得件数は `100` 件とする
