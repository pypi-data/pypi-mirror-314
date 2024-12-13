import requests
import os
import json

# Authorization must contain fields:
#    type
#    domain
#    consumer-key
#    consumer-secret
#    username
#    password

class SalesForceAPI:
    def __init__(self, authorization):
        self.url = f'https://{authorization["domain"]}.my.salesforce.com'
        if authorization['type'] == 'username-password':
            self.headers = self.__get_auth_user(authorization)
        if authorization['type'] == 'web server':
            self.headers = self.__get_auth_web_server(authorization)
        # headers must be: 
        # { 'Authorization': <token>, 'X-PrettyPrint': 1 }

    def __get_auth_user(self, authorization):
        domain = authorization['domain']
        auth = {
            'grant_type': 'password',
            'client_id': authorization['consumer-key'].rstrip(),
            'client_secret': authorization['consumer-secret'].rstrip(),
            'username': authorization['username'].rstrip(),
            'password': authorization['password'].rstrip()
        }
        url = f'{self.url}/services/oauth2/token'
        response = requests.post(url, data=auth)
        token = response.json().get('access_token')
        if token != None:
            headers = {'Authorization': f'Bearer {token}'}
            return headers
        else:
            raise Exception(f'SalesForceAPI authentication failed.\n'\
                            f'Response: {response}')

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

    def PermissionSetLicense(self, fields=None):
        if not fields:
            fields = [
                'Id', 'PermissionSetLicenseKey', 'DeveloperName', 'TotalLicenses',
                'UsedLicenses', 'Status'
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+PermissionSetLicense'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response

    def TenantUsageEntitlement(self, fields=None):
        if not fields:
            fields = [
                'MasterLabel', 'AmountUsed', 'CurrentAmountAllowed', 'Frequency', 
                'IsPersistentResource', 'UsageDate' 
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+TenantUsageEntitlement'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response

    def ActiveFeatureLicenseMetric(self, fields=None):
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
    
    def userLicense(self, fields=None):
        if not fields:
            fields = [
                'Id', 'LicenseDefinitionKey', 'Name',
                'TotalLicenses', 'UsedLicenses', 'Status', 
            ]
        fields = ',+'.join(fields)
        query = f'SELECT+{fields}+from+UserLicense'
        request_url = f'{self.url}/services/data/v53.0/query?q={query}'
        response = self.call_api(request_url)
        return response
           

    def call_api(self, url):
        response = requests.get(url, headers=self.headers)
        return response
