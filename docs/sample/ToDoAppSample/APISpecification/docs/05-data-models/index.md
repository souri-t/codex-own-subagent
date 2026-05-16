# データモデル

## Task

| 項目名 | 型 | 必須 | 説明 |
|--------|----|------|------|
| `taskId` | string | Yes | タスク ID |
| `title` | string | Yes | タスクタイトル |
| `description` | string | No | タスク詳細 |
| `status` | string | Yes | `open` / `completed` / `archived` |
| `priority` | integer | No | `1` 高、`2` 中、`3` 低 |
| `dueAt` | string | No | 期限日時 |
| `reminderAt` | string | No | 通知予定日時 |
| `labels` | array | No | ラベル一覧 |
| `createdAt` | string | Yes | 作成日時 |
| `updatedAt` | string | Yes | 更新日時 |

## Label

| 項目名 | 型 | 必須 | 説明 |
|--------|----|------|------|
| `labelId` | string | Yes | ラベル ID |
| `labelName` | string | Yes | ラベル名 |
| `colorCode` | string | No | 表示色 |

## PagedTasksResponse

| 項目名 | 型 | 必須 | 説明 |
|--------|----|------|------|
| `items` | array | Yes | タスク一覧 |
| `page` | integer | Yes | 現在ページ |
| `pageSize` | integer | Yes | ページサイズ |
| `totalCount` | integer | Yes | 総件数 |

## ステータス値

| 値 | 説明 |
|----|------|
| `open` | 未完了 |
| `completed` | 完了済み |
| `archived` | アーカイブ済み |
