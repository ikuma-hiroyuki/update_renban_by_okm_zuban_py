import os

import requests
from dotenv import load_dotenv

load_dotenv()


def line_notify(message):
    token = os.getenv('LINE_TOKEN')
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    requests.post(url, headers=headers, data={f'message': {message}})
