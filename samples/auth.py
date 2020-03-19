import json
import requests
import config

def auth(host, password):
    print(f'Autenticating to: {host}')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = f'grant_type=password&username=admin&password={password}'
    r = requests.post('https://' + host + ':5443/v2/token', headers=headers, data=payload, verify=False)
    print(f'Status code: {r.status_code}')
    print(f'Response: {r.json()}')
    return r.json()

auth(config.HOST, config.PASSWORD)