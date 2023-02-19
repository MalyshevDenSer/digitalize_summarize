from typing import Optional

import base64
from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response
import os
from dotenv import load_dotenv
import json
import hmac
import hashlib

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
PASSWORD_SALT = os.getenv('PASSWORD_SALT')
app = FastAPI()


def sign_data(data: str) -> str:
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    username_base64, sign = username_signed.split('.')
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username


def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_hash = users[username]['password']
    return password_hash == stored_hash


users = {
    'maldenser@yandex.ru': {
        'name': 'Denis',
        'password': '0785be1ca4ad9208e788c154e9ffbafe6ebaf11d0fb7879abbff81d0239e4fc4',
        'balance': 5000
    },
    'den@yandex.ru': {
        'name': 'Den',
        'password': '03eea00fd233ebe4355f6d732e278019b2dbedc5b60d9cb4ff48d93c132dfa5e',
        'balance': 0
    }
}


@app.get('/')
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type='text/html')
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type='text/html')
        response.delete_cookie(key="username")
        return response
    else:
        return Response(f"Привет, {users[valid_username]['name']}!", media_type='text/html')



@app.post('/login')
def process_login_page(username=Form(...), password=Form(...)):
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
            json.dumps({
                "success": False,
                "message": "Я вас не знаю!"
            }),
            media_type='application/json')
    response = Response(json.dumps({
                "success": True,
                "message": f"Привет {username}, твой баланс {user['balance']}"
            }),
        media_type='application/json')
    username_signed = base64.b64encode(username.encode()).decode() + '.' + sign_data(username)
    print('au2')
    response.set_cookie(key='username', value=username_signed)
    return response
