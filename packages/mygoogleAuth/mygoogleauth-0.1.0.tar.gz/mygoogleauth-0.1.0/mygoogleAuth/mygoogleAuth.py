import os
import json
import threading
from flask import redirect, url_for, request
from flask_login import UserMixin, LoginManager, login_user, logout_user
import requests
from oauthlib.oauth2 import WebApplicationClient
from werkzeug.middleware.proxy_fix import ProxyFix

# ログの基本設定
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class User(UserMixin):
    def __init__(self, auth_type, id_, name, email, profile_pic):
        self.auth_type = auth_type
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def to_dict(self):
        """ユーザーオブジェクトを辞書形式に変換"""
        return {
            "auth_type": self.auth_type, 
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile_pic": self.profile_pic
        }

    @staticmethod
    def from_dict(data):
        """辞書データからユーザーオブジェクトを作成"""
        return User(
            auth_type=data["auth_type"],
            id_=data["id"],
            name=data["name"],
            email=data["email"],
            profile_pic=data.get("profile_pic")
        )

class mygoogleAuth:

    auth_type = None

    def __init__(self, endpoint_callback:str=None, users_file:str=None):
        # 環境変数からGoogle OAuth2設定を読み込み
        self.GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
        self.GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
        self.GOOGLE_DISCOVERY_URL = os.getenv('GOOGLE_DISCOVERY_URL', 'https://accounts.google.com/.well-known/openid-configuration')

        # OAuth2クライアントのセットアップ
        self.client = WebApplicationClient(self.GOOGLE_CLIENT_ID)

        # ユーザー管理のためのJSONファイルパス
        if users_file :
            self.users_file = users_file
        else :
            # self.users_file = os.path.join(os.path.dirname(__file__), '..', 'mygoogleAuth_users.json')
            self.users_file = 'mygoogleAuth_users.json'

        # ユーザー管理のためのロック
        self.lock = threading.Lock()

        # ユーザー情報をロード
        self.users = self.load_users()

        # Google Discoveryドキュメントをロード
        self.google_provider_cfg    = requests.get(self.GOOGLE_DISCOVERY_URL).json()
        self.authorization_endpoint = self.google_provider_cfg.get("authorization_endpoint")
        self.token_endpoint         = self.google_provider_cfg.get("token_endpoint")
        self.userinfo_endpoint      = self.google_provider_cfg.get("userinfo_endpoint")
        self.endpoint_callback      = endpoint_callback

        # LINE API設定
        self.LINE_LOGIN_URL         = "https://access.line.me/oauth2/v2.1/authorize"
        self.LINE_TOKEN_URL         = "https://api.line.me/oauth2/v2.1/token"
        self.LINE_PROFILE_URL       = "https://api.line.me/v2/profile"
        self.LINE_REDIRECT_URI      = None #login_by_lineで設定する
        self.LINE_CLIENT_ID         = os.getenv('LINE_CLIENT_ID')
        self.LINE_CLIENT_SECRET     = os.getenv('LINE_CLIENT_SECRET')


    def setup_login_manager(self, app) :
        self.app = app
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app, x_proto=1, x_host=1)  # ProxyFixを追加
        self.login_manager = LoginManager()
        self.login_manager.init_app(app)
        self.login_manager.login_view = 'login'  # 未認証時にリダイレクトするビューを設定

        # Flask-Loginのuser_loaderを登録
        self.login_manager.user_loader(self.load_user)

    def load_users(self):
        """JSONファイルからユーザー情報をロード"""
        if not os.path.exists(self.users_file):
            return {}
        with self.lock:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    return {user_id: User.from_dict(info) for user_id, info in data.items()}
                except json.JSONDecodeError:
                    return {}

    def save_users(self):
        """ユーザー情報をJSONファイルに保存"""
        with self.lock:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                data = {user_id: user.to_dict() for user_id, user in self.users.items()}
                json.dump(data, f, ensure_ascii=False, indent=4)

    def load_user(self, user_id):
        """Flask-Loginがユーザーをロードするために呼び出す関数"""
        return self.users.get(user_id)

    def login(self):
        self.auth_type = "google"
        logger.debug("Generated redirect URI:", url_for(self.endpoint_callback, _external=True))
        request_uri = self.client.prepare_request_uri(
            self.authorization_endpoint,
            redirect_uri=url_for(self.endpoint_callback, _external=True),
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)


    def callback(self):
        code = request.args.get("code") # 認証コードを取得
        if not code:
            return None, "認証コードが提供されていません。"

        if self.auth_type == "google" :
            # トークンリクエストの準備
            token_url, headers, body = self.client.prepare_token_request(
                self.token_endpoint,
                authorization_response=request.url,
                redirect_url=url_for(self.endpoint_callback, _external=True),
                code=code,
            )
            # トークンリクエストを送信
            token_response = requests.post(
                token_url,
                headers=headers,
                data=body,
                auth=(self.GOOGLE_CLIENT_ID, self.GOOGLE_CLIENT_SECRET),
            )
            # トークンを解析
            self.client.parse_request_body_response(token_response.text)
            # ユーザー情報を取得
            uri, headers, body = self.client.add_token(self.userinfo_endpoint)
            userinfo_response = requests.get(uri, headers=headers, data=body)
            userinfo = userinfo_response.json()
            # メールが確認されているかチェック
            if not userinfo.get("email_verified"):
                return None, "ユーザーのメールが利用できないか、Googleによって確認されていません。"

        elif self.auth_type == "line" :
            state = request.args.get("state")
            # トークン取得
            token_data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.LINE_REDIRECT_URI,
                "client_id": self.LINE_CLIENT_ID,
                "client_secret": self.LINE_CLIENT_SECRET,
            }
            token_res = requests.post(self.LINE_TOKEN_URL, data=token_data)
            token_json = token_res.json()
            access_token = token_json.get("access_token")

            # プロフィール取得
            headers = {"Authorization": f"Bearer {access_token}"}
            profile_res = requests.get(self.LINE_PROFILE_URL, headers=headers)
            profile = profile_res.json()
            userinfo = {
                "sub"       : profile['userId'], 
                "name"      : profile['displayName'], 
                "email"     : "NONE", 
                "picture"   : profile['pictureUrl']
            }

        user = self.get_or_create_user(
            auth_type   = self.auth_type,
            id_         = userinfo["sub"],
            name        = userinfo["name"],
            email       = userinfo["email"],
            profile_pic = userinfo["picture"],
        )

        login_user(user)
        return user, None


    def login_by_line(self, redirect_uri, state="abcde"):
        self.auth_type = "line"
        self.LINE_REDIRECT_URI = redirect_uri
        line_auth_url = (
            f"{self.LINE_LOGIN_URL}?response_type=code"
            f"&client_id={self.LINE_CLIENT_ID}"
            f"&redirect_uri={self.LINE_REDIRECT_URI}"
            f"&state={state}"
            f"&scope=profile%20openid%20email"
        )
        return redirect(line_auth_url)



    def get_or_create_user(self, auth_type, id_, name, email, profile_pic):
        """自分のユーザーファイルにユーザー登録（or取得）"""
        user = self.users.get(id_)
        if not user:
            user = User(auth_type=auth_type, id_=id_, name=name, email=email, profile_pic=profile_pic)
            self.users[id_] = user
            self.save_users()
        return user

    def logout(self):
        logout_user()
        self.auth_type = None

    def get_userid_byemail(self, email) :
        for key, item in self.users.items() :
            if item["email"] == email :
                return key
        return None

    def get_user(self, id_):
        return self.users.get(id_)
