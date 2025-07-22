# 🔔 LINEリマインドBot

## 機能

* **定期メッセージ送信**: 火曜日、土曜日、日曜日のJST 21:00に「鍵とネット誰ですか？」というメッセージをLINEグループへ送信します。
* **LINE Bot API利用**: LINE Messaging APIのプッシュメッセージ機能を使ってメッセージを送信します。
* **安全な情報管理**: LINEのアクセストークンやグループIDは、GitHub Secretsで安全に管理されます。
* **自動実行**: GitHub Actionsによって、設定したスケジュールで自動的にボットが動作します。

---

## 構成ファイル

* `main.py`: スケジュール処理の記述がありますが、実際のリマインダー送信は `send_reminder.py` で行われます。
* `send_reminder.py`: LINEへ実際にメッセージを送信するスクリプトで、GitHub Actionsから呼び出されます。
* `webhook_server.py`: LINEからのイベントを受信し、グループIDなどをログに表示するための一時的なサーバーです。ボットの自動送信をオフにする設定も可能です。
* `requirements.txt`: このプロジェクトが必要とするPythonライブラリの一覧です。
* `.github/workflows/line_reminder.yml`: GitHub Actionsのワークフロー定義ファイル。ボットの実行スケジュールや環境を設定します。
* `.env`: ローカルでの環境変数管理に使いますが、GitHub ActionsではSecretsを利用します。
* `.gitignore`: Gitのバージョン管理から除外するファイルやフォルダーを指定します。

---

## セットアップガイド

### 1. LINE Botの準備

* LINE DevelopersコンソールでMessaging APIチャネルを作成します。
* チャネルアクセストークンを取得（長期トークン推奨）。
* Botを対象のLINEグループに招待し、グループIDを取得します（`webhook_server.py`などで取得可能）。

### 2. 環境変数の設定（GitHub Secrets）

リポジトリの **Settings > Secrets** から以下の2つを登録してください。

| Key                         | 説明                |
| --------------------------- | ----------------- |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINEチャネルのアクセストークン |
| `GROUP_ID`                  | メッセージを送る対象グループのID |

### 3. GitHub Actionsのスケジュール実行

`line_reminder.yml` には以下のようなスケジュールが記述されています。

```yaml
schedule:
  - cron: '0 12 * * 2,6,0'  # JST 21:00に対応（UTCで12:00）
```

これにより、毎週 **火・土・日曜日の21:00（日本時間）** にメッセージが自動送信されます。

---

## ローカルでのテスト（任意）

```bash
pip install -r requirements.txt
python send_reminder.py
```

※ `.env` ファイルに必要な環境変数（`LINE_CHANNEL_ACCESS_TOKEN`, `GROUP_ID`）を記載してください。

---

## 注意事項

* グループIDの取得にはBotがグループに追加されている必要があります。
* 長期トークンの有効期限や、Botの権限設定に注意してください。
* 複数のBotを運用する場合は、アクセストークンとグループIDを適切に切り分けて管理してください。

---

## ライセンス

MIT License
