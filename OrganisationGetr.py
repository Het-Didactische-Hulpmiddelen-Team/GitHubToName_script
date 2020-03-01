#!/usr/bin/env python3

import requests

# GitHub login - LOGIN CREDENTIALS HERE ################################################################################
username = ''
headers = {'Authorization': 'token '}

# request all organisations ############################################################################################
response_orgs = requests.get('https://api.github.com/user/orgs', headers=headers)
if response_orgs.status_code is not 200:
    raise Exception('API call error, check your login credentials (status code {})'.format(response_orgs.status_code))
orgs = response_orgs.json()

# print all organisations
for org in orgs:
    organisation_name = org["login"]
    print(organisation_name)
