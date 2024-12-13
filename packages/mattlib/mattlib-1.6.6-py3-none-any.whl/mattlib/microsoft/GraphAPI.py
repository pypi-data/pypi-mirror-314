from .BaseMicrosoftAPI import BaseMicrosoftAPI
import requests

class GraphAPI(BaseMicrosoftAPI):
    def connect(self, tenant_ID, app_ID, secret_key):
       super().connect(tenant_ID, app_ID, secret_key,
                        'https://graph.microsoft.com/.default')

    def list_users(self, properties=None):
        if properties:
            parameters = ','.join(properties)
            url = f'https://graph.microsoft.com/v1.0/users?$top=999&$select={parameters}'
        else:
            properties = ['businessPhones', 'displayName', 'givenName', 'jobTitle', 'mail',
                'mobilePhone', 'officeLocation', 'preferredLanguage', 'surname', 'department', 'city',
                'userPrincipalName', 'id','onPremisesUserPrincipalName','onPremisesSamAccountName',
                'onPremisesExtensionAttributes', 'assignedLicenses', 'accountEnabled']
            parameters = ','.join(properties)
            url = f'https://graph.microsoft.com/v1.0/users?$select={parameters}'

        response = self.call_api(url)
        return response

    def list_subscribed_skus(self):
        url = 'https://graph.microsoft.com/v1.0/subscribedSkus'
        response = self.call_api(url)
        return response

    def list_organizations(self):
        url = 'https://graph.microsoft.com/v1.0/organization'
        response = self.call_api(url)
        return response

    def getMailboxUsageDetail(self, period=7):
        url = f"https://graph.microsoft.com/v1.0/reports/"\
              f"getMailboxUsageDetail(period='D{period}')"
        
        response = self.call_api_stream(url)
        return response
    
    def getMailboxUsageStorage(self, period=7):
        url = f"https://graph.microsoft.com/v1.0/reports/"\
              f"getMailboxUsageStorage(period='D{period}')"
        
        response = self.call_api_stream(url)
        return response

    def getSkypeForBusinessOrganizerActivityUserCounts(self, period=7):
        url = f"https://graph.microsoft.com/v1.0/reports/"\
              f"getSkypeForBusinessOrganizerActivityUserCounts(period='D{period}')"
        
        response = self.call_api_stream(url)
        return response

    def getOffice365ActiveUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getOffice365ActiveUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getOffice365ActiveUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getYammerDeviceUsageUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getYammerDeviceUsageUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getYammerDeviceUsageUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getYammerActivityUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getYammerActivityUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getYammerActivityUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getSkypeForBusinessDeviceUsageUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getSkypeForBusinessDeviceUsageUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getSkypeForBusinessDeviceUsageUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getSkypeForBusinessActivityUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getSkypeForBusinessActivityUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getSkypeForBusinessActivityUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getSharePointSiteUsageDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getSharePointSiteUsageDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getSharePointSiteUsageDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getSharePointActivityUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getSharePointActivityUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getSharePointActivityUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getEmailAppUsageUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getEmailAppUsageUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getEmailAppUsageUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getOneDriveUsageAccountDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getOneDriveUsageAccountDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getOneDriveUsageAccountDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getOneDriveActivityUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getOneDriveActivityUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getOneDriveActivityUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getTeamsUserActivityUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getTeamsUserActivityUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getTeamsUserActivityUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getTeamsDeviceUsageUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getTeamsDeviceUsageUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getTeamsDeviceUsageUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def getEmailActivityUserDetail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getEmailActivityUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getEmailActivityUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def get_details(self, listParamsExtract=[
                'getOneDriveUsageAccountDetail',
                'getOneDriveActivityUserDetail',
                'getTeamsDeviceUsageUserDetail',
                'getTeamsUserActivityUserDetail',
                'getEmailActivityUserDetail',
                'getEmailAppUsageUserDetail',
                'getSharePointActivityUserDetail',
                'getSharePointSiteUsageDetail',
                'getSkypeForBusinessActivityUserDetail',
                'getSkypeForBusinessDeviceUsageUserDetail',
                'getYammerActivityUserDetail',
                'getYammerDeviceUsageUserDetail',
                'getOffice365ActiveUserDetail',
                'getSkypeForBusinessOrganizerActivityUserCounts',
                'getMailboxUsageDetail','getMailboxUsageStorage'
            ], paramsData=('period', '7')):
        
        results = []

        supported_paramsExtract = [
            'getOneDriveUsageAccountDetail',
            'getOneDriveActivityUserDetail',
            'getTeamsDeviceUsageUserDetail',
            'getTeamsUserActivityUserDetail',
            'getEmailActivityUserDetail',
            'getEmailAppUsageUserDetail',
            'getSharePointActivityUserDetail',
            'getSharePointSiteUsageDetail',
            'getSkypeForBusinessActivityUserDetail',
            'getSkypeForBusinessDeviceUsageUserDetail',
            'getYammerActivityUserDetail',
            'getYammerDeviceUsageUserDetail',
            'getOffice365ActiveUserDetail'
        ]

        if paramsData[0] == 'period':
            supported_paramsExtract+=['getSkypeForBusinessOrganizerActivityUserCounts',\
                'getMailboxUsageDetail','getMailboxUsageStorage']

        for item in listParamsExtract:

            if item not in supported_paramsExtract:
                print(f'Parameter not supported {item} \n'\
                    f'Supported parameters: {supported_paramsExtract}')
                return None

            else:
                urls = {
                'period': f"https://graph.microsoft.com/v1.0/reports/"\
                            f"{item}(period='D{paramsData[1]}')",
                'date': f"https://graph.microsoft.com/v1.0/reports/"\
                        f"{item}(date={paramsData[1]})"
                }

                url = urls.get(paramsData[0])
                response = self.call_api_stream(url)
                results.append((item, response))

        return results

    def office365_active_user_detail(self, params=('period', '7')):
        urls = {
            'period': f"https://graph.microsoft.com/v1.0/reports/"\
                      f"getOffice365ActiveUserDetail(period='D{params[1]}')",
            'date': f"http://graph.microsoft.com/v1.0/reports/"\
                    f"getOffice365ActiveUserDetail(date={params[1]})"
        }

        url = urls.get(params[0])
        response = self.call_api_stream(url)
        return response

    def office365_mailbox_usage_detail(self, period=7):
        supported_periods = [7, 30, 90, 180]
        if period not in supported_periods:
            print(f'office_365_mailbox_usage_detail: please use one of'\
                  f'supported periods: {period}')
            # raise error
            return None
        else:
            url = f"https://graph.microsoft.com/v1.0/reports/"\
                  f"getMailboxUsageDetail(period='D{period}')"
            response = self.call_api_stream(url)
            return response

    def m365_app_user_detail(self, period=90):
        supported_periods = [7, 30, 90, 180]
        if period not in supported_periods:
            print(f'm365_app_user_detail: please use one of'\
                  f'supported periods: {period}')
            return None
        else:
            url = f"https://graph.microsoft.com/v1.0/reports/"\
                  f"getM365AppUserDetail(period='D{period}')"
            response = self.call_api_stream(url)
            return response

    def methods(self):
        methods = [
            {
                'method_name': 'list_users',
                'method': self.list_users,
                'format': 'json'
            },
            {
                'method_name': 'list_subscribed_skus',
                'method': self.list_subscribed_skus,
                'format': 'json'
            },
            {
                'method_name': 'list_organizations',
                'method': self.list_organizations,
                'format': 'json'
            },
            {
                'method_name': 'getOneDriveUsageAccountDetail',
                'method': self.getOneDriveUsageAccountDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getOneDriveActivityUserDetail',
                'method': self.getOneDriveActivityUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getTeamsUserActivityUserDetail',
                'method': self.getTeamsUserActivityUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getTeamsDeviceUsageUserDetail',
                'method': self.getTeamsDeviceUsageUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getEmailActivityUserDetail',
                'method': self.getEmailActivityUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getEmailAppUsageUserDetail',
                'method': self.getEmailAppUsageUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getSharePointActivityUserDetail',
                'method': self.getSharePointActivityUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getSharePointSiteUsageDetail',
                'method': self.getSharePointSiteUsageDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getSkypeForBusinessActivityUserDetail',
                'method': self.getSkypeForBusinessActivityUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getSkypeForBusinessDeviceUsageUserDetail',
                'method': self.getSkypeForBusinessDeviceUsageUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getYammerActivityUserDetail',
                'method': self.getYammerActivityUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getYammerDeviceUsageUserDetail',
                'method': self.getYammerDeviceUsageUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getOffice365ActiveUserDetail',
                'method': self.getOffice365ActiveUserDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getSkypeForBusinessOrganizerActivityUserCounts',
                'method': self.getSkypeForBusinessOrganizerActivityUserCounts,
                'format': 'csv'
            },
            {
                'method_name': 'getMailboxUsageDetail',
                'method': self.getMailboxUsageDetail,
                'format': 'csv'
            },
            {
                'method_name': 'getMailboxUsageStorage',
                'method': self.getMailboxUsageStorage,
                'format': 'csv'
            },
            {
                'method_name': 'm365_app_user_detail',
                'method': self.m365_app_user_detail,
                'format': 'csv'
            }
        ]
        return methods
