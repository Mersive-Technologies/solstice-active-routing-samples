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

def configure_primary(host, password):
    auth_result = auth(host, password)
    access_token = auth_result['access_token']
    configure_session(host, access_token)

def connect_pod_to_primary(sink='', host=HOST, password='', mode='fullscreen'):
    auth_result = auth(sink, password)
    access_token = auth_result['access_token']
    configure_session(sink, access_token)
    create_reverse_connection(sink, host, access_token, mode)

def connect_primary_to_pod(sink='', host=HOST, password='', mode='fullscreen'):
    auth_result = auth(host, password)
    access_token = auth_result['access_token']
    create_connection(sink, host, access_token, mode)

def configure_session(pod_ip, access_token):

    # Configure session parameters

    payload = {}
    payload['presence'] = False
    payload['message'] = 'Sharing!'
    payload['background'] = '#F95127'
    payload['foreground'] = '#FFFFFF'
    # print(payload)

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    r = requests.patch('https://' + pod_ip + ':5443/v2/content/activerouting', headers=headers, data=json.dumps(payload), verify=False)

    print(f'Status code: {r.status_code}')
    print(f'Result: {r.json()}')

def create_reverse_connection(sink='', host=HOST, access_token='', mode='normal'):

    payload = {}
    payload['post'] = mode
    payload['message'] = 'Testing from API'
    payload['foreground'] = '#FFFFFF'
    payload['background'] = '#F95127'
    payload['resolution'] = '1920x1080'
    payload['sink'] = host

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    r = requests.post('https://' + sink + ':5443/v2/content/activerouting/connections', headers=headers, data=json.dumps(payload), verify=False)

    print(f'Status code: {r.status_code}')
    print(f'Result: {r.json()}')

def create_connection(sink, host=HOST, access_token='', mode='fullscreen'):

    print(sink, host, mode)
    payload = {}
    payload['post'] = mode
    payload['message'] = 'Testing from API'
    payload['foreground'] = '#FFFFFF'
    payload['background'] = '#F95127'
    payload['resolution'] = '1920x1080'
    payload['sink'] = sink

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    r = requests.post('https://' + host + ':5443/v2/content/activerouting/connections', headers=headers, data=json.dumps(payload), verify=False)

    print(f'Status code: {r.status_code}')
    print(f'Result: {r.json()}')

def delete_sessions(host, password):

    print(f'Autenticating to: {host}')
    auth_response = auth(host, password)

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + auth_response['access_token']}
    r = requests.delete('https://' + host + ':5443/v2/content/activerouting/connections', headers=headers, verify=False)

    print(f'Status code: {r.status_code}')
    print(f'Result: {r.json()}')

# This will configure each pod and share each pod back to the primary using the normal post mode.
# The primary will display two posts like a normal Solstice display would.
# Each pod has a notch that displays that it is sharing.
configure_primary(SINKS[0], PASSWORD)
connect_pod_to_primary(sink=SINKS[0], host=HOST, password=PASSWORD, mode='normal')
configure_primary(SINKS[1], PASSWORD)
connect_pod_to_primary(sink=SINKS[1], host=HOST, password=PASSWORD, mode='normal')

# To delete the session, send the DELETE request to each of the pods in a room
input('Press enter to reset')
delete_sessions(HOST, PASSWORD) # This seems ok to do first, doesn't really matter
delete_sessions(SINKS[0], PASSWORD)
delete_sessions(SINKS[1], PASSWORD)

# This will configure the primary pod, and then mirror it's content to each pod
input('Attempting to hit all pods after a 1-to-many share. Press enter to continue.')
configure_primary(HOST, PASSWORD)
connect_primary_to_pod(sink=SINKS[1], host=HOST, password=PASSWORD, mode='fullscreen')
connect_primary_to_pod(sink=SINKS[0], host=HOST, password=PASSWORD, mode='fullscreen')

# To delete the session, send the DELETE request to each of the pods in a room
# Technically, this probably isn't necessary if the one-to-many scenario is the last use
# of a room. However, it's difficult to know this, and so going to each pod and resetting it
# is a simpler operation and shouldn't cause any harm.
input('Press enter to reset')
delete_sessions(HOST, PASSWORD) # This seems ok to do first, doesn't really matter
delete_sessions(SINKS[0], PASSWORD)
delete_sessions(SINKS[1], PASSWORD)