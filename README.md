# sepa-reminder

このプロジェクトは、指定したLINEグループへ定期的にリマインダーメッセージを送信するLINE Botです。GitHub Actionsを活用し、メッセージ送信を自動化しています。

## 概要

このボットは、以下のような目的で使えます：
* 特定の曜日と時刻に、LINEグループへ自動でメッセージを送る。
* 日常のグループ内会話には返信せず、必要な時だけ発言する。

## 機能

* [cite_start]**定期メッセージ送信**: 火曜日、土曜日、日曜日のJST 21:00に「鍵とネット誰ですか？」というメッセージをLINEグループへ送ります[cite: 1].
* **LINE Bot API利用**: LINE Messaging APIのプッシュメッセージ機能を使ってメッセージを送信します.
* **安全な情報管理**: LINEのアクセストークンやグループIDは、GitHub Secretsで安全に管理されます.
* **自動実行**: GitHub Actionsによって、設定したスケジュールで自動的にボットが動作します.

## 構成ファイル

* [cite_start]`main.py`: スケジュール処理の記述がありますが、実際のリマインダー送信は`send_reminder.py`で行われます[cite: 1].
* [cite_start]`send_reminder.py`: LINEへ実際にメッセージを送信するスクリプトで、GitHub Actionsから呼び出されます[cite: 1].
* `webhook_server.py`: LINEからのイベントを受信し、グループIDなどをログに表示するための一時的なサーバーです。ボットの自動返信をオフにする設定も可能です.
* [cite_start]`requirements.txt`: このプロジェクトが必要とするPythonライブラリの一覧です[cite: 2].
* `.github/workflows/line_reminder.yml` (例): GitHub Actionsのワークフロー定義ファイル。ボットの実行スケジュールや環境を設定します.
* `.env`: ローカルでの環境変数管理に使いますが、GitHub ActionsではSecretsを利用します.
* [cite_start]`.gitignore`: Gitのバージョン管理から除外するファイルやフォルダーを指定します[cite: 1].

## セットアップガイド

### 1. LINE Developers Consoleでの準備

1.  **LINE Developers Consoleでチャネルを作成し、Messaging APIを有効にします。**
2.  **チャネルアクセストークンを発行し、この値を控えておきましょう。**

### 2. 環境変数の取得とGitHubでの設定

ボットがメッセージを送るために必要な情報をGitHub Secretsに登録します。

1.  **本番用グループIDの取得**
    * **ターミナル1で `webhook_server.py` を実行します。**
        プロジェクトのルートフォルダーで `python webhook_server.py` と入力・実行し、このターミナルは閉じずに置いておきます。
    * **ターミナル2で `ngrok` を実行します。**
        新しくターミナルを開き、`ngrok http 5000` と入力・実行します。表示される `https://` で始まるURLをコピーしておきます。
    * **LINE Developers ConsoleでWebhook URLを設定します。**
        LINE Developers Consoleの対象チャネルの「Messaging API」タブにある「Webhook設定」で、コピーしたNgrokのURLに `/callback` を付け足して入力し、「検証」ボタンで成功を確認後、「Webhookの利用」をオンにします。
    * **LINEグループでメッセージを送信します。**
        ボットを招待したい本番のLINEグループ（または新たに作ったテストグループ）で、何かメッセージを送ってみましょう。
    * **グループIDを確認します。**
        ターミナル1（`webhook_server.py`を実行している方）のログに「`📌 グループID: gXXXXXXXXXXXXXXXXX`」と表示される文字列を正確にメモします。
    * **一時サーバーを停止します。**
        グループIDの確認が終わったら、両方のターミナルで `Ctrl + C` を押してサーバーとNgrokを停止します。

2.  **GitHub Secretsの設定**
    * GitHubリポジトリの「Settings」タブを開き、「Secrets and variables」→「Actions」へ進みます。
    * 以下のシークレットを**引用符なしで**追加または更新します。
        * `LINE_ACCESS_TOKEN`: LINE Developers Consoleで発行したチャネルアクセストークン。
        * `LINE_GROUP_ID`: 上記で取得した本番環境のLINEグループID。

### 3. コードとワークフローの準備

リポジトリ内のコードが最新の状態であることを確認し、GitHubに反映させます。

1.  **Pythonファイルの最終確認:**
    * `send_reminder.py` が最新の修正（`LINE_GROUP_ID` の定義と使用）になっているか確認します。
    * `webhook_server.py` は、メッセージ受信時の自動返信（`line_bot_api.reply_message` の行）をコメントアウトして無効化しておくことを推奨します。

2.  **GitHub Actionsワークフローファイルの確認:**
    * `.github/workflows/` 内の `.yml` ファイルが、`send_reminder.py` を実行し、環境変数を正しく渡す設定になっていることを確認します。

3.  **変更をコミットしてプッシュします。**
    * ローカルでの修正内容をすべてコミットし、GitHubリポジトリにプッシュします。

## 動作確認

1.  **GitHub Actionsで手動実行してみましょう**
    * GitHubリポジトリの「Actions」タブを開き、「LINEリマインダーボット」ワークフローを選択します。
    * 「Run workflow」ボタンをクリックして手動で実行し、ジョブが成功することを確認します。
    * **本番環境のLINEグループにテストメッセージが届くか確認してください。**

2.  **自動実行を待ちましょう**
    * 手動実行でメッセージが届くことを確認できたら、あとは設定されたスケジュール（火・土・日 JST 21:00）で自動的にメッセージが送信されるのを待つだけです。

---
