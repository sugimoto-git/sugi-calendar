# 変更履歴

## Webアプリケーション化

- **目的:** コマンドラインツールを、誰でも簡単に使えるWebアプリケーションに変更しました。
- **フレームワーク:** PythonのWebフレームワークであるFlaskを導入しました。

## 主な変更点

1.  **`main.py` -> `app.py`:**
    -   スクリプト名を`app.py`に変更し、Flaskアプリケーションのロジックを実装しました。

2.  **Webサーバー機能:**
    -   `app.py`にHTTPサーバー機能を追加し、ブラウザからアクセスできるようにしました。
    -   `http://localhost:5000` でアプリケーションが起動します。

3.  **認証フローの変更:**
    -   デスクトップアプリケーション用の認証から、Webアプリケーション用のOAuth 2.0認証フローに更新しました。
    -   初回アクセス時にGoogleアカウントでの認証が求められます。

4.  **UIの追加:**
    -   シンプルなHTMLフォームを実装し、ブラウザから直接`events.csv`ファイルをアップロードしてカレンダーに登録できるようにしました。

5.  **依存関係の管理:**
    -   `Flask`ライブラリを追加しました。
    -   プロジェクトの依存関係を`requirements.txt`ファイルにまとめました。

## 実行方法

1.  **仮想環境のアクティベート:**
    ```bash
    source venv/bin/activate
    ```

2.  **Webアプリケーションの起動:**
    ```bash
    python app.py
    ```

3.  **ブラウザでアクセス:**
    -   `http://localhost:5000` を開きます。

## 【重要】`credentials.json`の更新

-   **既存の`credentials.json`は使用できません。**
-   [Google Cloud Platform](https://console.cloud.google.com/)で新しいOAuthクライアントIDを**「ウェブ アプリケーション」**として作成し直す必要があります。
-   作成後、承認済みのリダイレクトURIに `http://localhost:5000/oauth2callback` と `http://127.0.0.1:5000/oauth2callback` を追加してください。
-   新しい認証情報をダウンロードし、既存の`credentials.json`を上書きしてください。
