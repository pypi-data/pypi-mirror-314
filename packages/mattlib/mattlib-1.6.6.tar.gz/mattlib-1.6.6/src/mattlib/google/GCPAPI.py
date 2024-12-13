from .BaseGoogleAPI import BaseGoogleAPI
import googleapiclient.discovery

class GCPAPI(BaseGoogleAPI):
    required_info = [
            ('credentials_file', 'str')
            ]
   
    def connect(self, credentials_file):
        self.scopes = ['https://www.googleapis.com/auth/cloud-platform']
        super().connect(credentials_file)

    def list_project_assets(self, project):
        security_center = googleapiclient\
            .discovery.build('securitycenter',
                             'v1',
                             credentials=self.credentials)
        args = {
            'parent': f'projects/{project}',
            'pageSize': 1000
        }
        data = self.call_api(security_center.projects()\
            .assets()\
            .list,
            args, 'listAssetsResults')
        return data

    def methods(self):
        m = [
            {
                'method_name': 'list_project_assets',
                'method': self.list_project_assets,
                'format': 'json'
            }
        ]
        return m

