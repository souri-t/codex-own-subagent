# 共通仕様

## リクエスト共通ルール

| 項目 | 仕様 |
|------|------|
| HTTPメソッド | `GET` `POST` `PATCH` `DELETE` |
| Content-Type | `application/json` |
| Accept | `application/json` |
| 日時形式 | ISO 8601（例: `2026-04-25T09:30:00+09:00`） |
| 真偽値 | `true` / `false` |

## 共通ヘッダー

| ヘッダー名 | 必須 | 内容 |
|------------|------|------|
| `Authorization` | Yes | `Bearer <JWT>` |
| `X-Request-Id` | No | トレース用リクエストID |
| `Content-Type` | POST/PATCH時にYes | `application/json` |

## ページネーション

一覧取得 API はクエリパラメータでページングを行います。

| パラメータ | 必須 | 説明 | 初期値 |
|------------|------|------|--------|
| `page` | No | 1始まりのページ番号 | `1` |
| `pageSize` | No | 1ページあたりの件数（最大100） | `20` |
| `sort` | No | ソート対象項目 | `dueAt` |
| `order` | No | `asc` または `desc` | `desc` |

## クエリ仕様

| パラメータ | 必須 | 型 | 説明 |
|------------|------|----|------|
| `status` | No | string | `open` `completed` `archived` |
| `labelId` | No | string | ラベル ID による絞り込み |
| `keyword` | No | string | タイトル、説明の部分一致検索 |
