from fastapi import Request, FastAPI

app = FastAPI()
PHOHE_FORMAT = {1: ' ', 2: '(', 6: ')', 7: ' ', 11: '-', 14: '-'}


@app.post('/unify_phone_from_json')
async def main(info: Request):
    req_info = await info.json()
    if not req_info.get('phone'):
        return {'status': 'FALSE'}
    unifdied_phone_number = unify_phone_number(req_info['phone'])
    return unifdied_phone_number


def unify_phone_number(phone_sybmols):
    list_of_digits = [i for i in phone_sybmols if i.isdigit()]
    if list_of_digits[0] not in ['7', '8', '9']:
        return ''.join(list_of_digits)
    if list_of_digits[0] == '9':
        list_of_digits.insert(0, '8')
    elif list_of_digits[0] == '7':
        list_of_digits[0] = '8'
    for i in PHOHE_FORMAT.keys():
        list_of_digits.insert(i, PHOHE_FORMAT.get(i))
    return''.join(list_of_digits)
