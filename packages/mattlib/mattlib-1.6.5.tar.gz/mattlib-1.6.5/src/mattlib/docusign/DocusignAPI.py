import sys
sys.path.append('../mattlib')
from mattlib.BaseAPI import BaseAPI
import requests
import os
import json
import time

# Authorization must contain fields:
#    client_id
#    client_secret
#    base_url


class DocusignAPI(BaseAPI):
    required_info = [
        ("client_id", "str"),
        ("client_secret", "str"),
        ("base_url", "str"),
    ]
        
    def connect(self,client_id, client_secret, base_url):
        self.client_id = client_id.rstrip()
        self.client_secret = client_secret.rstrip()
        self.base_url = base_url.rstrip()
        self.scope = 'signature'
        self.headers = self.__get_auth_user()

    def __get_auth_user(self):
        auth = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        url = "https://account-d.docusign.com/oauth/token"
        response = requests.post(url, data=auth)

        if response.status_code == 200:
            token = response.json().get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            return headers

        else:
            print(f"DocusignAPI authentication failed.\n "\
                    f"Response: {response.text}")

    def accounts(self):
        request_url = f'{self.base_url}+/restapi/v2/accounts'
        response = self.call_api(request_url)
        return response


    def call_api(self, url):
        response = requests.get(url, headers=self.headers)
        response = json.loads(response.text)
        return response

    def methods(self):
        methods = [
            {
                'method_name': 'accounts',
                'method': self.accounts,
                'format': 'json'
            },
        ]
        return methods
