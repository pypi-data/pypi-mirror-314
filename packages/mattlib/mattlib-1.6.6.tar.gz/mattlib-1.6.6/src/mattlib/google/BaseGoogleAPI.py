import sys
sys.path.append('../mattlib')
from mattlib.BaseAPI import BaseAPI
from google.oauth2 import service_account
import googleapiclient.discovery
import json

class BaseGoogleAPI(BaseAPI):
    def connect(self, credentials_file, subject=None):
       if credentials_file == None:
           raise Exception('Necessário arquivo .json com credenciais do clente')
       self.credentials = self.get_credentials(credentials_file, subject)

    def get_credentials(self, credentials_file, subject=None):
        credentials = service_account.Credentials\
            .from_service_account_file(
                credentials_file,
                scopes=self.scopes,
                subject = subject)
        return credentials

    def call_api(self, call_function, args, data_key):
        assets = []
        while True:
            response = call_function(**args).execute()
            
            data = response[data_key]
            assets += data
            if 'nextPageToken' not in response.keys():
                break
            args['pageToken'] = response['nextPageToken']
        return assets

