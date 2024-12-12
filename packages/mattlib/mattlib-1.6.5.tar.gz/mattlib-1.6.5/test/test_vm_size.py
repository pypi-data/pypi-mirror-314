import os, mattlib

def unique_dict(array, key):
    size = len(array)
    unique_key = []
    unique = []
    for i in range(size):
        if array[i][key] not in unique_key:
            unique_key.append(array[i][key])
            unique.append(array[i])
    return unique

api = mattlib.AzureAPI(app_ID=os.getenv('AMBEV_AZURE_APP_ID'),
                        tenant_ID=os.getenv('AMBEV_AZURE_TENANT_ID'),
                        secret_key=os.getenv('AMBEV_AZURE_SECRET_KEY'))

_locations = api.list_locations()
_locations = [
	{
		"subscription": _loc['id'].split('/')[2],
		"location": _loc['id'].split('/')[-1]
	}
	for _loc in _locations
]
locations = unique_dict(_locations, 'location')
_instance_types = api.list_virtual_machine_sizes(locations=locations)
