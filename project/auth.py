import base64
import requests
import datetime

import settings


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    is_access_token_expired = True
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    token_url = settings.TOKEN_URL


    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def _encode_credentials(self):
        """
        Return a base64 encoded string
        """

        if self.client_id is None or self.client_secret is None:
            raise Exception("You have not provided user's credentials")

        client_creds = '{}:{}'.format(self.client_id, self.client_secret)
        client_creds = client_creds.encode()
        client_creds_b64 = base64.b64encode(client_creds)

        return client_creds_b64

    def get_post_params(self):
        """
        Returns headers and data required for POST request
        """

        client_creds_b64 = self._encode_credentials()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }
        data = {
            "grant_type": "client_credentials"
        }

        return headers, data


    def authorize_credentials(self):
        """
        Authenticates user's credentials. Returns True whether 
        the response is 200 or False in every other situation
        """

        headers, data = self.get_post_params()

        response = requests.post(self.token_url, headers=headers, data=data)

        if not self.is_request_successful(response):
            return False

        self.handle_successful_auth(response)

        return True


    def is_request_successful(self, response):
        return response.status_code in range(200, 299)

    def handle_successful_auth(self, response):
        now = datetime.datetime.now()

        expires_in = response.json()['expires_in']

        self.access_token = response.json()['access_token']
        self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
        self.is_access_token_expired = self.access_token_expires < now
