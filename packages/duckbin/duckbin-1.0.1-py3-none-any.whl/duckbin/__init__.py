# duckbin/__init__.py
# python setup.py sdist bdist_wheel
# twine upload dist/*

import requests

BASE_URL = "https://bin.freeutka.xyz/api/index.php"

def post(text: str) -> str:
    response = requests.post(BASE_URL, data={'text': text})
    if response.status_code == 200:
        data = response.json()
        if 'text_link' in data:
            return data['text_link']
        else:
            raise Exception(f"Error: {data.get('error', 'Unknown error')}")
    else:
        raise Exception("Failed to connect to the API.")

def get(link: str) -> str:
    text_id = link.split('=')[-1] 
    response = requests.get(BASE_URL, params={'id': text_id})
    if response.status_code == 200:
        data = response.json()
        if 'text' in data:
            return data['text']
        else:
            raise Exception(f"Error: {data.get('error', 'Unknown error')}")
    else:
        raise Exception("Failed to connect to the API.")
