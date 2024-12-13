from .BaseMicrosoftAPI import BaseMicrosoftAPI
from datetime import datetime, timedelta

class EntraIdAPI(BaseMicrosoftAPI):
    def connect(self, tenant_ID, app_ID, secret_key):
       super().connect(tenant_ID, app_ID, secret_key,
                        'https://graph.microsoft.com/.default')
       self.subscriptions = None
       self.resource_groups = None
       self.servers = None

    def _strip_app_display_name(self, response):
        if 'value' in response:
            for item in response['value']:
                if 'appDisplayName' in item and isinstance(item['appDisplayName'], str):
                    item['appDisplayName'] = item['appDisplayName'].strip()
        return response


    def listAppsDisplayName(self):
        now = datetime.utcnow()
        set_end_date = now - timedelta(days=30)
        start_date = set_end_date.isoformat() + 'Z'
        end_date = now.isoformat() + 'Z'
        params = {
        '$filter': f"createdDateTime ge {start_date} and createdDateTime le {end_date}",
        '$select': 'appDisplayName,createdDateTime',
        '$orderby': 'appDisplayName'
        }
        url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
        response = self.call_api(url,params,ignore=False)
        return self._strip_app_display_name(response)
    
    def listAuditLogsPerMonth(self):
        now = datetime.utcnow()
        set_end_date = now - timedelta(days=30)
        start_date = set_end_date.isoformat() + 'Z'
        end_date = now.isoformat() + 'Z'
        params = {
        '$filter': f"createdDateTime ge {start_date} and createdDateTime le {end_date}",
        }
        url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
        response = self.call_api(url,params,ignore=False)
        return self._strip_app_display_name(response)
    
    def listAuditLogsPerDay(self):
        now = datetime.utcnow()
        set_end_date = now - timedelta(days=2)
        start_date = set_end_date.isoformat() + 'Z'
        end_date = now.isoformat() + 'Z'
        params = {
        '$filter': f"createdDateTime ge {start_date} and createdDateTime le {end_date}",
        }
        url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
        response = self.call_api(url,params,ignore=True)
        return self._strip_app_display_name(response)

    def methods(self):
        methods = [
            {
                'method_name': 'listAppsDisplayName',
                'method': self.listAppsDisplayName,
                'format': 'json'
            },
            {
                'method_name': 'listAuditLogsPerMonth',
                'method': self.listAuditLogsPerMonth,
                'format': 'json'
            },
            {
                'method_name': 'listAuditLogsPerDay',
                'method': self.listAuditLogsPerDay,
                'format': 'json'
            }
        ]
        return methods
