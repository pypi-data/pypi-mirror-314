from urllib.parse import urlencode,quote
import sys
sys.path.append('../mattlib')
from mattlib.BaseAPI import BaseAPI
import requests
import json
import base64
import time
import jwt

class AdobeAPI(BaseAPI):
    required_info = [
        ("client_ID", "str"),
        ("client_secret", "str"),
        ("organization_ID", "str"),
        ("api_key","str"),
        ("tech_acc_id","str"),
        ("key","str")

    ]

    def connect(self, client_ID, client_secret, key, organization_ID, api_key, tech_acc_id):
        self.organization_ID = organization_ID.rstrip()
        self.client_ID = client_ID.rstrip()
        self.client_secret = client_secret.rstrip()
        self.key = key.rstrip()
        self.api_key = key.rstrip()
        self.tech_acc_id = tech_acc_id.rstrip()
        self.jwt_token = self.create_jwt()
        self.headers = self.__get_auth_user()
    
    def create_jwt(self):
        current_sec_time = int(round(time.time()))
        expiry_time = current_sec_time + (60*60*24)
        ims_server = "ims-na1.adobelogin.com"
        payload = {
            "exp" : expiry_time,
            "iss" : self.organization_ID,
            "sub" : self.tech_acc_id,
            "aud" : "https://" + ims_server + "/c/" + self.client_ID    ,
            "https://" + ims_server + "/s/ent_user_sdk" : True
        }
        self.jwt_token = jwt.encode(payload, self.api_key, algorithm="RS256")
        return self.jwt_token

    def __get_auth_user(self):    
        url = 'https://ims-na1.adobelogin.com/ims/exchange/jwt/'
        scopes = [
            "openid",
            "user_management_sdk",
            "AdobeID",
            'exchange_jwt'
        ]
        payload = {
            'client_id': self.client_ID,
            'client_secret': self.client_secret,
            'jwt_token': self.jwt_token,
            'client_secret_type': 'client_credentials',
            'scope': ' '.join(scopes)
        }
        response = requests.post(url, data=payload)
        print(response)
        token = response.json().get('access_token')
        if token != None:
            headers = {
                'Authorization': 'Bearer ' + token,
                'X-Api-Key': self.client_ID  
            }
            return headers
        else:
            print(response.text)
            raise Exception(f'Adobe authentication failed.\n'\
                            f'Response: {response}')
    def list_users(self):
        url = f'https://usermanagement.adobe.io/v2/usermanagement/users/' + self.organization_ID + '/0'
        response = self.call_api(url)
        return response

    def list_groups(self):
        url = f'https://usermanagement.adobe.io/v2/usermanagement/groups/' + self.organization_ID + '/0' 
        response = self.call_api(url)
        return response
    
    # passar como parâmetro o campo onde está a informação
    def call_api(self, url):
        # necessário inserir número da página na URL 
        response = requests.get(url, headers=self.headers)
        response = json.loads(response.text)
        # necessário verificar campo "lastPage"
        # necessário realizar requisições em laço, salvar resultado
        # em um array
        return response

    def methods(self):
        methods = [
            {
                'method_name': 'list_users',
                'method': self.list_users,
                'format': 'json'
            },
            {
                'method_name': 'list_groups',
                'method': self.list_groups,
                'format': 'json'
            },
        ]
        return methods
