"# mygoogleAuth" 

## 概要
google認証を簡単に実装するための便利ライブラリです。

## 使い方

### 事前準備

Google Cloud Console でプロジェクトを作成する
- [Google Cloud Console](https://console.cloud.google.com/) にアクセスし、新しいプロジェクトを作成します。
- OAuth 2.0 クライアント ID を設定します。
- リダイレクト URI を設定します（例: https://127.0.0.1:5000/login/callback ）<br>
  ※ httpsじゃないと認証がとおりません
- クライアント ID と クライアント シークレット を`.env`ファイルに書き込む。

### pip

```
pip install mygoogleAuth
```

### .envファイルの中身
```
FLASK_SECRET_KEY = "abcdefg"
GOOGLE_CLIENT_ID = "64************ntent.com"
GOOGLE_CLIENT_SECRET = "*******************"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### ファイル構成

```
your_project/
├── app.py
├── .env.py
└── templates/
    ├── index.html
    └── subpage.html
```

