import json
import requests

class ClockifyApi:
	def __init__(self, api_key):
		self.api_key = api_key.rstrip()
		header = {'x-api-key': self.api_key}

	def get_shared_report_ID(headers = None, report_ID = None, parameters = None):
		if report_ID != None:
			url = 'https://reports.api.clockify.me/v1/shared-reports/' + report_ID
			response = call_api(url, headers, parameters)
			response = response['timeentries']
			return response
		else:
			raise Exception(f' Para extrair o relatorio é necessario o ID do mesmo.\n')
		
	def call_api(self, url, parameters):
		try:
			response = requests.get(url, headers=headers)
			response = json.loads(response.content)
			return response
		except:
			raise Exception(f'No connection adapters were found')

