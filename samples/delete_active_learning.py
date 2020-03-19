import json
import requests
import config

HOST = config.HOST
PASSWORD = config.PASSWORD

def auth(host, password):
    print(f'Autenticating to: {host}')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = f'grant_type=password&username=admin&password={password}'
    r = requests.post('https://' + host + ':5443/v2/token', headers=headers, data=payload, verify=False)
    print(f'Status code: {r.status_code}')
    print(f'Response: {r.json()}')
    return r.json()


def delete_sessions(host):

    print(f'Autenticating to: {host}')
    auth_response = auth(HOST, PASSWORD)

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + auth_response['access_token']}
    r = requests.delete('https://' + HOST + ':5443/v2/content/activerouting/connections', headers=headers, verify=False)

    print(f'Status code: {r.status_code}')
    print(f'Result: {r.json()}')


delete_sessions(HOST)