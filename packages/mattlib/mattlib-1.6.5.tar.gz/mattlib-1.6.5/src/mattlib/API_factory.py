def API_factory(service_type):
    if service_type == 'graph':
        from . microsoft.GraphAPI import GraphAPI
        return GraphAPI()
    if service_type == 'azure':
        from . microsoft.AzureAPI import AzureAPI
        return AzureAPI()
    if service_type == 'entraid':
        from . microsoft.EntraIdAPI import EntraIdAPI
        return EntraIdAPI()
    if service_type == 'salesforce':
        from . salesforce.SalesForceAPI import SalesForceAPI 
        return SalesForceAPI()
    if service_type == 'gcp':
        from . google.GCPAPI import GCPAPI
        return GCPAPI()
    if service_type == 'google_workspace':
        from . google.GoogleWorkspaceAPI import GoogleWorkspaceAPI
        return GoogleWorkspaceAPI()
    if service_type == 'adobe':
        from . adobe.AdobeAPI import AdobeAPI
        return AdobeAPI()
    if service_type == 'docusign':
        from . docusign.DocusignAPI import DocusignAPI
        return DocusignAPI()
    if service_type == 'snow':
        from . snow.snowAPI import snowAPI
        return snowAPI()
        
