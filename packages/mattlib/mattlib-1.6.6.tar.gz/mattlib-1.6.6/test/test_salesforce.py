import os
import pandas as pd
import mattlib

auth = {
    'type': 'username-password',
    'domain': os.getenv('SALESFORCE_DOMAIN'),
    'consumer-key': os.getenv('SALESFORCE_CONSUMER_KEY'),
    'consumer-secret': os.getenv('SALESFORCE_CONSUMER_SECRET'),
    'username': os.getenv('SALESFORCE_USERNAME'),
    'password': os.getenv('SALESFORCE_PASSWORD')
}
api = mattlib.SalesForceAPI(auth)
users = api.user()
udf = pd.json_normalize(users.json()['records'])

profiles = api.profile()
pdf = pd.json_normalize(profiles.json()['records'])

userLicenses = api.userLicense()
uldf = pd.json_normalize(userLicenses.json()['records'])
