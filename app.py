from flask import Flask, jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth
from numpy import random

# Flaskクラスのインスタンスを現在のファイル名で作成
api = Flask(__name__)
# 日本語文字化け対策
api.config['JSON_AS_ASCII'] = False
# authインスタンスを作成
auth = HTTPBasicAuth()

users = {
  "user1": "xzy9uh46",
  "user2": "ue2cbky8"
}

@api.route('/')
def index():
  return "This is a OMIKUJI-API!!\n\nusage: curl -u username:password http://127.0.0.1:5000/omikuji\n"

@auth.get_password
def get_pw(username):
  if username in users:
    return users.get(username)
  return None

# GET
@api.route('/omikuji', methods=['GET'])
@auth.login_required
def omikuji():
  # 確率は観音百籤による（浅草寺のくじ配分）
  omikuji = random.choice(['大吉', '吉', '半吉', '小吉', '末小吉', '末吉', '凶'], p=[0.17, 0.35, 0.05, 0.04, 0.03, 0.06, 0.3])
  return make_response(jsonify({'fortune': omikuji}))

# エラー処理
@api.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

# コマンドラインから実行した時
if __name__ == '__main__':
    api.run()
