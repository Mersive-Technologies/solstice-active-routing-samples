import json
import requests
import config

HOST = config.HOST
PASSWORD = config.PASSWORD
SINKS = config.SINKS

def auth(host, password):
    print(f'Autenticating to: {host}')
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = f'grant_type=password&username=admin&password={password}'
    r = requests.post('https://' + host + ':5443/v2/token', headers=headers, data=payload, verify=False)
    print(f'Status code: {r.status_code}')
    print(f'Response: {r.json()}')
    return r.json()

def create_multi_connections(sinks):
    auth_result = auth(HOST, PASSWORD)
    access_token = auth_result['access_token']

    configure_session(access_token)

    for sink in sinks:
        loop_set_connections(sink, access_token)

def configure_session(access_token):


    # Configure session parameters

    payload = {}
    payload['presence'] = False
    payload['message'] = 'Sharing!'
    payload['background'] = '#F95127'
    payload['foreground'] = '#FFFFFF'
    print(payload)

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    r = requests.patch('https://' + HOST + ':5443/v2/content/activerouting', headers=headers, data=json.dumps(payload), verify=False)

    print(f'Status code: {r.status_code}')
    print(f'Result: {r.json()}')

def loop_set_connections(sink, access_token):

    payload = {}
    payload['post'] = 'normal'  
    payload['message'] = 'Testing from API'
    payload['foreground'] = '#FFFFFF'
    payload['background'] = '#F95127'
    payload['resolution'] = '1920x1080'
    payload['sink'] = sink

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    r = requests.post('https://' + HOST + ':5443/v2/content/activerouting/connections', headers=headers, data=json.dumps(payload), verify=False)

    print(f'Status code: {r.status_code}')
    print(f'Result: {r.json()}')

create_multi_connections(SINKS)