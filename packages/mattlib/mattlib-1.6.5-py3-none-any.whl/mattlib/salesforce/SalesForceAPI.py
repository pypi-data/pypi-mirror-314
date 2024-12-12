import sys
sys.path.append('../mattlib')
from mattlib.BaseAPI import BaseAPI
import requests
import os
import json
import time

# Authorization must contain fields:
#    type
#    domain
#    consumer-key
#    consumer-secret
#    username
#    password

class SalesForceAPI(BaseAPI):
    required_info = [
        ("type", "str"),
        ("domain", "str"),
        ("consumer_key", "str"),
        ("consumer_secret", "str"),
        ("username", "str"),
        ("password", "str")
    ]
        
    def connect(self,type, domain, consumer_key, consumer_secret, username, password):
        self.type = type.rstrip()
        self.domain = domain.rstrip()
        self.consumer_key = consumer_key.rstrip()
        self.consumer_secret = consumer_secret.rstrip()
        self.username = username.rstrip()
        self.password = password.rstrip()
        self.url = f'https://{self.domain}.my.salesforce.com'
        if self.type == 'username-password':
            self.__get_auth_user()
        if type == 'web server':
            self.headers = self.__get_auth_web_server(authorization)
        # headers must be: 
        # { 'Authorization': <token>, 'X-PrettyPrint': 1 }

    def __get_auth_user(self):
        domain = self.domain
        auth = {
            'grant_type': 'password',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret,
            'username': self.username,
            'password': self.password
        }
        url = f'{self.url}/services/oauth2/token'
        response = requests.post(url, data=auth)
        token = response.json().get('access_token')
        if token != None:
            self.headers = {'Authorization': f'Bearer {token}'}
            response = self.methods()[0]['method']()
            return 
        else:
            raise Exception(f"SalesForceAPI authentication failed.\n "\
                  f"Response: {response}")

    def __get_auth_web_server(self, authorization):
        pass

    def user(self, fields=None):
        if not fields:
            fields = [
                'Id', 'FirstName', 
                'LastName', 'Username', 'Email',
                'IsActive', 'LastLoginDate',
                'UserType', 'ProfileId'
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+User'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response

    def profile(self, fields=None):
        if not fields:
            fields = [
                'Id', 'Name', 'UserLicenseId'
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+Profile'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response

    def permission_set_license(self, fields=None):
        if not fields:
            fields = [
                'Id', 'PermissionSetLicenseKey', 'DeveloperName', 'MasterLabel', 'TotalLicenses',
                'UsedLicenses', 'Status'
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+PermissionSetLicense'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response

    def tenant_usage_entitlement(self, fields=None):
        if not fields:
            fields = [
                'Setting', 'MasterLabel', 'AmountUsed', 'CurrentAmountAllowed', 'Frequency', 
                'IsPersistentResource', 'UsageDate', 'StartDate','EndDate'
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+TenantUsageEntitlement'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response

    def active_feature_license_metric(self, fields=None):
        if not fields:
            fields = [
                'ActiveUserCount', 'AssignedUserCount', 'FeatureType',
                'MetricsDate', 'TotalLicenseCount'
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+ActiveFeatureLicenseMetric'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response
    
    def user_license(self, fields=None):
        if not fields:
            fields = [
                'Id', 'LicenseDefinitionKey', 'Name', 'MasterLabel',
                'TotalLicenses', 'UsedLicenses', 'Status', 
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+UserLicense'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response
           

    def call_api(self, url):
        values = []
        i = 0
        while url != None:
            try:
                response = requests.get(url, headers=self.headers)
                response = json.loads(response.text)
            except:
                raise Exception(f"SalesForceAPI failed.\n "\
                  f"Response: {response}")

            values += response['records']
            if 'nextRecordsUrl' in response.keys():
                url_aux = response['nextRecordsUrl']
                url = f'{self.url}{url_aux}'
            else:
                url = None
        return values

    def methods(self):
        methods = [
            {
                'method_name': 'user',
                'method': self.user,
                'format': 'json'
            },
            {
                'method_name': 'profile',
                'method': self.profile,
                'format': 'json'
            },
            {
                'method_name': 'permission_set_license',
                'method': self.permission_set_license,
                'format': 'json'
            },
            {
                'method_name': 'tenant_usage_entitlement',
                'method': self.tenant_usage_entitlement,
                'format': 'json'
            },
            {
                'method_name': 'active_feature_license_metric',
                'method': self.active_feature_license_metric,
                'format': 'json'
            },
            {
                'method_name': 'user_license',
                'method': self.user_license,
                'format': 'json'
            },
        ]
        return methods
