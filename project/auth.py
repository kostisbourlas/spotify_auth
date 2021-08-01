import base64
import requests
import datetime

import settings


def authorize_credentials():
    client_creds_b64 = _encode_credentials()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(settings.TOKEN_URL, headers=headers, data=data)

    return response


def get_auth_response(response):

    if is_request_valid(response):
        now = datetime.datetime.now()

        access_token = response.json()['access_token']
        expires_in = response.json()['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        is_expired = expires < now


def is_request_valid(response):
    return response.status_code in range(200, 299)


def _encode_credentials():
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET

    client_creds = '{}:{}'.format(client_id, client_secret)
    client_creds = client_creds.encode()
    client_creds_b64 = base64.b64encode(client_creds)

    return client_creds_b64
