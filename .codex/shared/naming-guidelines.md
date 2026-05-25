# 命名指針

このファイルは、設計、実装、レビューで共通利用する命名規則です。

対象:
- `dev-orchestrator`
- `requirements-analyst`
- `code-architect`
- `implementation-engineer`
- `design-reviewer`

各担当は、このファイルを前提として判断し、命名上の重要な判断や逸脱を成果物に明示すること。

## 基本方針

- ドメイン語彙を優先し、汎用語より対象や責務が具体的に分かる名前を使うこと。
- 動作を表す名前は、下記の推奨動詞から選ぶこと。
- 型名、DTO 名、プロパティ名、ファイル名も同じ語彙体系で揃えること。
- 既存 API との互換性を壊す名前変更は、影響範囲と移行方針を確認してから行うこと。
- `Build` は Builder パターンの `Build()` を除き使用しないこと。
- 非同期処理は必ず `Async` 接尾辞で統一し、`AsyncXxx` のような接頭辞は禁止すること。
- DTO / Model 変換は原則 `ToXxx` を使い、`ConvertXxx` は DTO 変換に使わないこと。

## 基本命名規則

| 分類 | 使用する命名 | 用途・意味 | 例 | 禁止例 |
| --- | --- | --- | --- | --- |
| 作成 | `Create` / `Add` | 新規生成 | `CreateOrder()` | `BuildOrder()` |
| 取得 | `Get` | 必ず取得 | `GetUser()` | `FetchUserData()` |
| 検索 | `Find` | 見つからない可能性あり | `FindUserById()` | `SearchUser()` |
| 条件検索 | `Search` | 複数条件検索 | `SearchProducts()` | `FindAll()` |
| 更新 | `Update` | 更新処理 | `UpdateProfile()` | `SaveProfile()` |
| 削除 | `Delete` / `Remove` | 削除処理 | `DeleteSession()` | `ClearSession()` |
| 存在確認 | `Exists` | 存在判定 | `ExistsUser()` | `CheckUser()` |
| bool 判定 | `Is` | 状態判定 | `IsEnabled()` | `CheckEnabled()` |
| bool 保持 | `Has` | 保有判定 | `HasPermission()` | `ContainsPermission()` |
| bool 可能 | `Can` | 実行可能判定 | `CanExecute()` | `AbleToExecute()` |
| bool 推奨 | `Should` | 条件判定 | `ShouldReload()` | `NeedReload()` |
| 非同期 | `Async` suffix | async 処理 | `LoadFileAsync()` | `AsyncLoadFile()` |
| イベント発火 | `On` | イベント通知 | `OnCompleted()` | `RaiseCompleted()` |
| イベント処理 | `Handle` | イベントハンドラ専用 | `HandleButtonClick()` | `HandleData()` |
| 変換 | `ConvertTo` / `To` | 型変換 | `ConvertToEntity()` / `ToEntity()` | `BuildEntity()` |
| DTO 変換 | `To` | DTO / Model 変換 | `ToResponse()` | `ConvertResponse()` |
| パース | `Parse` | 構文解析 | `ParseJson()` | `ReadJson()` |
| シリアライズ | `Serialize` | 文字列化 | `SerializeObject()` | `ConvertObject()` |
| デシリアライズ | `Deserialize` | 復元 | `DeserializeJson()` | `ParseObject()` |
| 読込 | `Load` | 外部読込 | `LoadConfiguration()` | `GetConfiguration()` |
| 外部取得 | `Fetch` / `Retrieve` | API / DB 取得 | `FetchApiResult()` | `GetApiData()` |
| 読み込み | `Read` | ファイル等読込 | `ReadTextFile()` | `LoadText()` |
| 保存 | `Save` | 保存 | `SaveSettings()` | `StoreSettings()` |
| 永続化 | `Persist` / `Store` | DB 保存 | `PersistEntity()` | `SaveEntity()` |
| 出力 | `Write` | 書込 | `WriteLog()` | `SaveLog()` |
| 外部出力 | `Export` | Export 処理 | `ExportCsv()` | `WriteCsv()` |
| 条件抽出 | `Filter` | 条件絞込 | `FilterActiveUsers()` | `ExtractUsers()` |
| 投影 | `Select` | 一部選択 | `SelectUserNames()` | `GetNames()` |
| 内部抽出 | `Extract` | 解析抽出 | `ExtractTextFromPdf()` | `GetPdfText()` |
| 集約 | `Collect` | 情報収集 | `CollectMetrics()` | `GatherMetrics()` |
| 検出 | `Detect` | 状態検出 | `DetectAnomalies()` | `CheckAnomalies()` |
| 解決 | `Resolve` | 依存 / 型解決 | `ResolveDependency()` | `GetDependency()` |
| Try 系 | `TryXxx` | 失敗可能処理 | `TryParseDate()` | `ParseOrNull()` |
| 起動 | `Start` | 開始処理 | `StartServer()` | `RunServer()` |
| 停止 | `Stop` | 停止処理 | `StopService()` | `EndService()` |
| 再起動 | `Restart` | 再起動 | `RestartApplication()` | `ReloadApplication()` |
| 送信 | `Send` | 送信 | `SendEmail()` | `ExecuteMail()` |
| 接続開始 | `Open` | 開始 | `OpenConnection()` | `ConnectOpen()` |
| 接続終了 | `Close` | 終了 | `CloseWindow()` | `ShutdownWindow()` |
| 生成 | `Generate` | 動的生成 | `GenerateToken()` | `BuildToken()` |
| 初期化 | `Initialize` | 初期化 | `InitializeContext()` | `SetupContext()` |
| 組立 | `Compose` | 合成構築 | `ComposeMessage()` | `BuildMessage()` |
| 集約構築 | `Aggregate` | 集約生成 | `AggregateItems()` | `BuildItems()` |
| フォーマット | `Format` | 表示文字列生成 | `FormatMessage()` | `BuildMessage()` |
| Query 生成 | `CreateQuery` | Query 作成 | `CreateQuery()` | `BuildQuery()` |
| コレクション戻り値 | 複数形 | List 返却 | `GetUsers()` | `GetUserList()` |

## 略語禁止ルール

| 禁止略語 | 推奨 |
| --- | --- |
| `Calc` | `Calculate` |
| `Exec` | `Execute` |
| `Proc` | `Process` |
| `Msg` | `Message` |
| `Info` | `Information` |
| `Num` | `Number` |
| `Str` | `String` |
| `Ctx` | `Context` |
| `Repo` | `Repository` |
| `Auth` | `Authentication` |
| `Config` | `Configuration` |
| `Env` | `Environment` |

## 曖昧語禁止ルール

| 禁止ワード | 理由 | 推奨例 |
| --- | --- | --- |
| `Do` | 処理内容不明 | `Create`, `Update`, `Delete` |
| `Process` | 抽象的 | `ConvertTo`, `Filter`, `ExecuteBatch` |
| `Manage` | 管理対象不明 | `UpdateUserSettings` |
| `Common` | 汎用すぎる | 責務を具体化 |
| `Helper` | 役割不明 | 責務を具体化 |
| `Util` | 意味不明 | 責務を具体化 |
| `Data` | 内容不明 | `UserProfile`, `OrderResult` |
| `Info` | 内容不明 | `UserDetails`, `Metadata` |
| `Run` | 処理内容不明 | `Start`, `ExecuteJob` |
| `Task` | 責務不明 | `ImportOrdersTask` のように対象を具体化 |
| `Object` | 対象不明 | 具体型名を使用 |
| `Item` | 対象不明 | `OrderItem`, `MenuItem` のように対象を具体化 |
| `Stuff` | 意味不明 | 対象を具体化 |
| `Thing` | 意味不明 | 対象を具体化 |
| `Build` | 責務が曖昧 | `Create`, `Generate`, `Compose`, `ConvertTo`, `CreateQuery` |

## 運用ルール

### `requirements-analyst`

- 要件整理時に、命名に使う主要ドメイン語彙を明示すること。
- 同義語が複数ある場合は、どの語を正とするか決めること。

### `code-architect`

- クラス、モジュール、公開 API、DTO、主要メソッドの命名方針を設計成果物へ含めること。
- `Get` / `Find` / `Search`、`Save` / `Persist` など混同しやすい動詞は、今回の設計でどれを使うか明示すること。
- 命名規則により却下した案があれば理由を残すこと。

### `implementation-engineer`

- 新規追加する型名、メソッド名、変数名、ファイル名にこの指針を適用すること。
- 既存命名との互換性のために逸脱する場合は、逸脱箇所と理由を必ずまとめること。

### `design-reviewer`

- 命名違反をレビュー対象に含めること。
- 指摘時は、違反しているルール、問題点、推奨リネームを明示すること。
- hard violation と suggestion を区別すること。

### `dev-orchestrator`

- 命名方針が論点になる場合は、要件整理で語彙を固定し、設計とレビューに引き継ぐこと。
- 工程ごとの要約に、命名上の重要判断と未解決事項を含めること。

## 補助チェック

機械的に拾える違反は、命名レビュー用スキルのチェッカーで確認できる。

```bash
python3 .codex/skills/naming-review/scripts/check_naming_guidelines.py
```

このチェッカーは補助用途であり、ドメイン語彙の妥当性や責務の自然さまでは自動判定できない。最終判断は設計レビューで行うこと。
