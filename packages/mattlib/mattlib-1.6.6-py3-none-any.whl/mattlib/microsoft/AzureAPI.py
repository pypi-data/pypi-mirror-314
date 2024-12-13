from .BaseMicrosoftAPI import BaseMicrosoftAPI

class AzureAPI(BaseMicrosoftAPI):
    def connect(self, tenant_ID, app_ID, secret_key):
       super().connect(tenant_ID, app_ID, secret_key,
                        'https://management.core.windows.net/.default')
       self.subscriptions = None
       self.resource_groups = None
       self.servers = None

    def list_subscriptions(self):
        url = 'https://management.azure.com/'\
              'subscriptions?api-version=2020-01-01'
        response = self.call_api(url)
        self.subscriptions = [item['subscriptionId'] for item in response]
        return response

    def subscription_ids(self):
        subscriptions = self.list_subscriptions()
        return [item['subscriptionId'] for item in subscriptions]
    
    def list_consumption(self):
        subscription_ids = self.subscription_ids()
        all_responses = []
        for subscription in subscription_ids:
            subscription_url = subscription
            url = f"https://management.azure.com/subscriptions/{subscription_url}/providers/Microsoft.Consumption/usageDetails?api-version=2017-11-30"
            response = self.call_api(url)
            all_responses.append(response)
        
        return all_responses

    def list_usage_details(self, subscriptions=None):
        subscriptions = self.subscription_ids()

        usage_details = []
        for subscription in subscriptions:
            url = f"https://management.azure.com/subscriptions/{subscription}/providers/Microsoft.Consumption/usageDetails?api-version=2017-11-30"
            usage_details += self.call_api(url)
        return usage_details

    def list_virtual_networks(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions
#            subscriptions = self.subscription_ids()

        virtual_networks = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'providers/Microsoft.Network/'\
                  f'virtualNetworks?api-version=2021-03-01'
            virtual_networks += self.call_api(url)
        return virtual_networks

    def list_resource_groups(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions
#            subscriptions = self.subscription_ids()
        resource_groups = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'resourcegroups?api-version=2021-04-01'
            resource_groups += self.call_api(url)
        return resource_groups

    def resource_groups_id(self,subscriptions):
        resource_groups = self.list_resource_groups(subscriptions)
        return [item['id'] for item in resource_groups]

    def list_virtual_machines(self, subscriptions=None, status=False):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions
#            subscriptions = self.subscription_ids()

        virtual_machines = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'providers/Microsoft.Compute/'\
                  f'virtualMachines?api-version=2021-03-01&statusOnly={status}'
            virtual_machines += self.call_api(url)
        return virtual_machines



    def list_public_ip_addresses(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions
#            subscriptions = self.subscription_ids()

        public_ips = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'providers/Microsoft.Network/'\
                  f'publicIPAddresses?api-version=2021-02-01'
            public_ips += self.call_api(url)
        return public_ips

    def list_locations(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions
        
        locations = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'locations?api-version=2020-01-01'
            locations += self.call_api(url)
        return locations

    # Microsoft states this API is deprecated.
    def list_virtual_machine_sizes(self, subscriptions=None, locations=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        if locations is None:
            locations = self.list_locations()

        sizes = []
        for location in locations:
            subscription = location['subscription']
            location_name = location['location']
            url = f'https://management.azure.com/subscriptions/'\
                  f'{subscription}/providers/Microsoft.Compute/locations/'\
                  f'{location_name}/vmSizes?api-version=2021-07-01'
            result = self.call_api(url)
            if result:
                sizes += result
        return sizes

    def list_network_interfaces(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        net_interfaces = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Network/'\
                  f'networkInterfaces?api-version=2021-03-01'
            net_interfaces += self.call_api(url)
        return net_interfaces



    def list_application_gateways(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        app_gateways = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Network/'\
                  f'applicationGateways?api-version=2021-05-01'
            app_gateways += self.call_api(url)
        return app_gateways

    def list_databricks_workspaces(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        databricks_workspaces = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Databricks/'\
                  f'workspaces?api-version=2018-04-01'
            databricks_workspaces += self.call_api(url)
        return databricks_workspaces

    def list_factories(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        factories = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.DataFactory/'\
                  f'factories?api-version=2018-06-01'
            factories += self.call_api(url)
        return factories

    def list_mssql_servers(self, resource_groups=None):

        if self.subscriptions is None:
            self.subscriptions = self.subscription_ids()
        subscriptions = self.subscriptions

        if resource_groups is None:
            if self.resource_groups is None:
                self.resource_groups = self.resource_groups_id(subscriptions)
            resource_groups = self.resource_groups

        subs = []
        rgs = []
        for row in resource_groups:
            splited = row.split('/')
            subs.append(splited[2].lower())
            rgs.append(splited[4].lower())

        servers = []
        for i in range(len(subs)):
                url = f'https://management.azure.com/subscriptions/{subs[i]}'\
                    f'/resourceGroups/{rgs[i]}/providers/Microsoft.Sql/'\
                    f'servers?api-version=2021-11-01-preview'
                servers += self.call_api(url)
        return servers

    def list_mariadb_servers(self):

        if self.subscriptions is None:
            self.subscriptions = self.subscription_ids()
        subscriptions = self.subscriptions

        mariadb_servers = []
        for sub in subscriptions:
                url = f'https://management.azure.com/subscriptions/{sub}'\
                    f'/providers/Microsoft.DBforMariaDB/'\
                    f'servers?api-version=2018-06-01-preview'
                mariadb_servers += self.call_api(url)
        return mariadb_servers

    def list_mysql_servers(self, resource_groups=None):

        if self.subscriptions is None:
            self.subscriptions = self.subscription_ids()
        subscriptions = self.subscriptions

        mysql_servers = []
        for sub in subscriptions:
                url = f'https://management.azure.com/subscriptions/{sub}'\
                    f'/providers/Microsoft.DBforMySQL/'\
                    f'servers?api-version=2017-12-01-preview'
                mysql_servers += self.call_api(url)
        return mysql_servers

    def list_postgresql_servers(self, resource_groups=None):

        if self.subscriptions is None:
            self.subscriptions = self.subscription_ids()
        subscriptions = self.subscriptions

        postgresql_servers = []
        for sub in subscriptions:
                url = f'https://management.azure.com/subscriptions/{sub}'\
                    f'/providers/Microsoft.DBforPostgreSQL/'\
                    f'servers?api-version=2017-12-01-preview'
                postgresql_servers += self.call_api(url)
        return postgresql_servers

    def servers_ids(self,resource_groups):
        servers = self.list_mssql_servers(resource_groups)
        return [item['id'] for item in servers]

    def list_mariadb_databases(self):
        server_ids = self.list_mariadb_servers()
        server_ids = [server['id'] for server in server_ids]
        subs = []
        rgs = []
        server_names = []
        for server in server_ids:
            splited = server.split('/')
            subs.append(splited[2].lower())
            rgs.append(splited[4].lower())
            server_names.append(splited[8].lower())

        mariadb_databases = []
        for i in range(len(server_names)):
            url = f'https://management.azure.com/subscriptions/{subs[i]}'\
                f'/resourceGroups/{rgs[i]}/'\
                f'providers/Microsoft.DBforMariaDB'\
                f'/servers/{server_names[i]}/'\
                f'databases?api-version=2018-06-01-preview'
            mariadb_databases += self.call_api(url)
        return mariadb_databases

    def list_mysql_databases(self):
        server_ids = self.list_mysql_servers()
        server_ids = [server['id'] for server in server_ids]
        subs = []
        rgs = []
        server_names = []
        for server in server_ids:
            splited = server.split('/')
            subs.append(splited[2].lower())
            rgs.append(splited[4].lower())
            server_names.append(splited[8].lower())

        mysql_databases = []
        for i in range(len(server_names)):
            url = f'https://management.azure.com/subscriptions/{subs[i]}'\
                f'/resourceGroups/{rgs[i]}/'\
                f'providers/Microsoft.DBforMySQL'\
                f'/servers/{server_names[i]}/'\
                f'databases?api-version=2017-12-01-preview'
            mysql_databases += self.call_api(url)
        return mysql_databases

    def list_postgresql_databases(self):
        server_ids = self.list_postgresql_servers()
        server_ids = [server['id'] for server in server_ids]
        subs = []
        rgs = []
        server_names = []
        for server in server_ids:
            splited = server.split('/')
            subs.append(splited[2].lower())
            rgs.append(splited[4].lower())
            server_names.append(splited[8].lower())

        postgresql_databases = []
        for i in range(len(server_names)):
            url = f'https://management.azure.com/subscriptions/{subs[i]}'\
                f'/resourceGroups/{rgs[i]}/'\
                f'providers/Microsoft.DBforPostgreSQL'\
                f'/servers/{server_names[i]}/'\
                f'databases?api-version=2017-12-01'
            postgresql_databases += self.call_api(url)
        return postgresql_databases

    def list_mssql_databases(self, servers=None):

        if self.subscriptions is None:
            self.subscriptions = self.subscription_ids()
        subscriptions = self.subscriptions

        if self.resource_groups is None:
            self.resource_groups = self.resource_groups_id(subscriptions)
        resource_groups = self.resource_groups

        if servers is None:
            if self.servers is None:
                self.servers = self.servers_ids(resource_groups)
            servers = self.servers        

        subs = []
        rgs = []
        server_names = []
        for row in servers:
            splited = row.split('/')
            subs.append(splited[2].lower())
            rgs.append(splited[4].lower())
            server_names.append(splited[8].lower())

        databases = []
        for i in range(len(server_names)):
                    url = f'https://management.azure.com/subscriptions/{subs[i]}'\
                        f'/resourceGroups/{rgs[i]}/providers/Microsoft.Sql/servers/{server_names[i]}/'\
                        f'databases?api-version=2021-11-01-preview'
                    databases += self.call_api(url)
        return databases

    def list_resources(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        resources = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'resources?api-version=2021-04-01'
            resources += self.call_api(url)
        return resources

    def list_app_service_plans(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        app_service_plans = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Web/'\
                  f'serverfarms?api-version=2022-03-01'
            app_service_plans += self.call_api(url)
        return app_service_plans

    def list_web_apps(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscription_ids()
            subscriptions = self.subscriptions

        web_apps = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Web/'\
                  f'sites?api-version=2022-03-01'
            web_apps += self.call_api(url)
        return web_apps
    def methods(self):
        methods = [
            {
                'method_name': 'list_usage_details',
                'method': self.list_usage_details,
                'format': 'json'
            },
            {
                'method_name': 'list_subscriptions',
                'method': self.list_subscriptions,
                'format': 'json'
            },
            {
                'method_name': 'list_consumption',
                'method': self.list_consumption,
                'format': 'json'
            },
            {
                'method_name': 'list_virtual_networks',
                'method': self.list_virtual_networks,
                'format': 'json'
            },
            {
                'method_name': 'list_resource_groups',
                'method': self.list_resource_groups,
                'format': 'json'
            },
            {
                'method_name': 'list_virtual_machines',
                'method': self.list_virtual_machines,
                'format': 'json'
            },
            {
                'method_name': 'list_public_ip_addresses',
                'method': self.list_public_ip_addresses,
                'format': 'json'
            },
            {
                'method_name': 'list_locations',
                'method': self.list_locations,
                'format': 'json'
            },
            {
                'method_name': 'list_virtual_machine_sizes',
                'method': self.list_virtual_machine_sizes,
                'format': 'json'
            },
            {
                'method_name': 'list_virtual_machines',
                'method': self.list_virtual_machines,
                'format': 'json'
            },
            {
                'medthod_name': 'list_app_service_plans',
                'method': self.list_app_service_plans,
                'format': 'json',
            },
            {
                'medthod_name': 'list_web_apps',
                'method': self.list_web_apps,
                'format': 'json',
            },
            {
                'method_name': 'list_mariadb_servers',
                'method': self.list_mariadb_servers,
                'format': 'json'
            },
            {
                'method_name': 'list_mysql_servers',
                'method': self.list_mysql_servers,
                'format': 'json'
            },
            {
                'method_name': 'list_postgresql_servers',
                'method': self.list_postgresql_servers,
                'format': 'json'
            },
            {
                'method_name': 'list_mssql_servers',
                'method': self.list_mssql_servers,
                'format': 'json'
            },
            {
                'method_name': 'list_mariadb_databases',
                'method': self.list_mariadb_databases,
                'format': 'json'
            },
            {
                'method_name': 'list_msql_databases',
                'method': self.list_mysql_databases,
                'format': 'json'
            },
            {
                'method_name': 'list_postgreql_databases',
                'method': self.list_postgresql_databases,
                'format': 'json'
            },
        ]
        return methods
