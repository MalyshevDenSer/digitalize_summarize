from typing import Optional

from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response

app = FastAPI()

users = {
    'maldenser@yandex.ru' : {
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
        return Response(f'Привет {users[username]["name"]}!', media_type='text/html')
    else:
        response = Response(login_page, media_type='text/html')
        response.delete_cookie(key="username")
        return response


@app.post('/login')
def process_login_page(username = Form(...), password = Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response('Я вас не знаю', media_type='text/html')
    response = Response(f'Привет {username}, твой баланс {user["balance"]}', media_type='text/html')
    response.set_cookie(key='username', value=username)
    return response
