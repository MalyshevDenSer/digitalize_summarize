from fastapi import FastAPI, Form
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
def index_page():
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    return Response(login_page, media_type='text/html')


@app.post('/login')
def process_login_page(username = Form(...), password = Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response('Я вас не знаю', media_type='text/html')
    return Response(f'Привет {username}, твой баланс {user["balance"]}', media_type='text/html')
