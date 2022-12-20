import requests
import urllib
import json

def apiMeliController(method,endpoint,access_token,body):
    # # # method = 'POST'
    # # # endpoint = 'oauth/token/'
    url = f"https://api.mercadolibre.com/{endpoint}"

    # # #   body = {'grant_type': 'refresh_token', 
    # # #         'client_id': '7220664084350595',
    # # #         'client_secret':'zIE8Xy9gvqxagaiPUUE4HNcATtDNlcwQ',
    # # #         'refresh_token':'TG-6344a96ef4363300011251b3-116499542'}
    #payload= urllib.parse.urlencode(body)
    payload = ''
    if body != '':
        payload = json.dumps(body)

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization':f'Bearer {access_token}'
    }

    response = requests.request(method, url, headers=headers, data=payload)

    return response