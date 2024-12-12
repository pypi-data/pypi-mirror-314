import sys
sys.path.append('../mattlib')
from mattlib.BaseAPI import BaseAPI
import pandas as pd
import requests as rq
import numpy as np
import concurrent.futures

# Authorization must contain fields:
#    url
#    username
#    password

class snowAPI(BaseAPI):
    required_info = [
        ("url", "str"),
        ("username", "str"),
        ("password", "str")
    ]

    def connect(self,url, username, password):
        self.url = f"https://sam.4matt.com.br/{url.rstrip()}"
        self.username = username.rstrip()
        self.password = password.rstrip()
        rq.get(self.url, headers={"Accept": "application/json"}, auth=(self.username, self.password)).json()


    def format_users_dataframe(self, data):
        base_url = f"{self.url}/customers/3/users"
        user_info_list = self.fetch_user_data_parallel(data, base_url, self.username, self.password)
        df = pd.json_normalize([item for item in user_info_list if item is not None])
        df_dc_filtered = df[['Body.StatusCode', 'Body.FullName', 'Body.OrgChecksum']]
        df_dc_filtered = df_dc_filtered.rename(columns={
            'Body.StatusCode': 'Status',
            'Body.FullName': 'Nome completo',
            'Body.OrgChecksum': 'onPremisesSamAccountName'
        })
        df_dc_filtered = df_dc_filtered[['onPremisesSamAccountName', 'Status', 'Nome completo']]
        df_dc_filtered = df_dc_filtered[df_dc_filtered['Nome completo'].str.strip() != '']
        data = df_dc_filtered.dropna(subset=['Nome completo'])
        return data
    
    def get_user_info(self,base_url, user_id, login, password):
        url = f"{base_url}/{user_id}/"
        response = None  # Definindo um valor padrão
        
        try:
            response = rq.get(url, headers={"Accept": "application/json"}, auth=(login, password), timeout=None)
        except rq.ConnectionError as e:
            print(f"Erro de conexão: {e}")
        except rq.Timeout as e:
            print(f"Tempo de espera expirado: {e}")

        return response
    
    def fetch_user_data_parallel(self,df, base_url, login, password):
        user_data_list = []
        
        def fetch_user_data_single(user_id):
            response = self.get_user_info(base_url, user_id, login, password)
            if response:
                if response.status_code == 200:
                    return response.json()  
                else:
                    print(f"Falha ao obter dados para o usuário {user_id}. Status Code: {response.status_code}")
            else:
                print(f"Falha ao obter dados para o usuário {user_id}. Resposta nula.")

            return None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_user_data_single, user_id) for user_id in df['Body.Id']]
            
            for future in concurrent.futures.as_completed(futures):
                user_data = future.result()
                user_data_list.append(user_data)
        
        return user_data_list

    def users(self,batch_size=1000,num=0):
        url =  self.url + '/users?$inlinecount=allpages'
        data = pd.DataFrame()
        while True:
            response = rq.get(url, headers={"Accept": "application/json"}, auth=(self.username, self.password)).json()
            for meta_item in response['Meta']:
                if 'Name' in meta_item and meta_item['Name'] == 'Count':
                    count_value = meta_item['Value']
                    break
            if num > count_value:
                break
            body = pd.json_normalize(response['Body'])
            data = pd.concat([data, body])
            num += batch_size
            url = f"{url}&$top={batch_size}&$skip={num}"
        data = self.format_users_dataframe(data)
        return data
    
    def methods(self):
        methods = [
            {
                'method_name': 'users',
                'method': self.users,
                'format': 'json'
            },
        ]
        return methods