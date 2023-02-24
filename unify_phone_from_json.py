from fastapi import Request, Response, FastAPI, Form, Query, Cookie
import json

app = FastAPI()
PHONE_FORMAT = ((1, ' '), (2, '('), (6, ')'), (7, ' '), (11, '-'), (14, '-'))


@app.post('/unify_phone_from_json')
async def unify_phone_from_json(info: Request):
    req_info = await info.json()
    if not req_info.get('phone'):
        return Response(json.dumps({"success": False}), media_type='application/json')
    return unify_phone_number(req_info['phone'])


@app.post('/unify_phone_from_form')
async def unify_phone_from_form(phone: str = Form()):
    return unify_phone_number(phone)


@app.get('/unify_phone_from_query')
async def unify_phone_from_query(phone):
    return unify_phone_number(phone)


@app.get('/unify_phone_from_cookies')
async def unify_phone_from_cookies(phone=Cookie(default=None)):
    return unify_phone_number(phone)


def unify_phone_number(phone_sybmols):
    list_of_digits = [i for i in phone_sybmols if i.isdigit()]
    if list_of_digits[0] not in ['7', '8', '9'] or len(list_of_digits) > 11:
        return Response(''.join(list_of_digits), media_type='text/html')
    if list_of_digits[0] == '9':
        list_of_digits.insert(0, '8')
    elif list_of_digits[0] == '7':
        list_of_digits[0] = '8'
    for i in PHONE_FORMAT:
        list_of_digits.insert(i[0], i[1])
    return Response(''.join(list_of_digits), media_type='text/html')