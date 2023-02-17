from typing import Optional

import base64
from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response
import os
from dotenv import load_dotenv
import hmac
import hashlib

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
app = FastAPI()


def sign_data(data: str) -> str:
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()

def get_username_from_signed_string(username_signed : str) -> Optional[str]:
    username_base64, sign = username_signed.split('.')
    username = base64.b16decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username
users = {
    'maldenser@yandex.ru': {
        'name': 'Denis',
        'password': '123',
        'balance': 5000
    },
    'den@yandex.ru': {
        'name': 'Den',
        'password': '456',
        'balance': 0
    }
}


@app.get('/')
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    if username and users.get(username) is not None:
        valid_username = get_username_from_signed_string(username)
        if not valid_username:
            response = Response(login_page, media_type='text/html')
            response.delete_cookie(key="username")
            return response
        return Response(f'Привет {users[username]["name"]}!', media_type='text/html')
    else:
        response = Response(login_page, media_type='text/html')
        response.delete_cookie(key="username")
        return response


@app.post('/login')
def process_login_page(username=Form(...), password=Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response('Я вас не знаю', media_type='text/html')
    response = Response(f'Привет {username}, твой баланс {user["balance"]}', media_type='text/html')
    username_signed = base64.b64encode(username.encode()).decode() + '.' + sign_data(username)
    response.set_cookie(key='username', value=username_signed)
    return response
