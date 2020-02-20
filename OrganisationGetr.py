#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth

# GitHub login (fallback) LOGIN CREDENTIALS HERE #######################################################################
# username = input("GitHub username:")
# password = input("GitHub password:") # DEPRECATED!
username = ''
headers = {'Authorization': 'token '}

# request all organisations ############################################################################################
# response_orgs = requests.get('https://api.github.com/user/orgs', auth=HTTPBasicAuth(username, password))
response_orgs = requests.get('https://api.github.com/user/orgs', headers=headers)
orgs = response_orgs.json()

for org in orgs:
    organisation_name = org["login"]
    print(organisation_name)
