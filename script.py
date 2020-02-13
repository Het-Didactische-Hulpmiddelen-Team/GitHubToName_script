import os
import mysql.connector
from mysql.connector import Error
import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import getpass

# database connection (not working)
''' 
try:
    connection = mysql.connector.connect(host='193.191.177.132',
                                         port='3306',
                                         database='dht',
                                         user='dht',
                                         password='mvghetdhtmvghetdht')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor = cursor.close()
        connection.close()
        print("MySQL connection is closed")
'''

# GitHub login
username = input("GitHub username:")
password = input("GitHub password:")

# dummy data input
mappings = open("userMappings", "r")
line = mappings.readline()

convertedMappings = {}
while line:
    mapping = line.split()
    name = '{} {}'.format(mapping[0], mapping[1])
    link = mapping[2]
    convertedMappings.update({name: link})
    line = mappings.readline()

# request all organisations
responseOrgs = requests.get('https://api.github.com/user/orgs', auth=HTTPBasicAuth(username, password))
orgs = responseOrgs.json()

# request which organisation
counter = 0
for org in orgs:
    organisationName = org["login"]
    item = "{}. {}".format(counter, organisationName)
    print(item)
    counter += 1

orgInput = input("Which organisation? (give number):")
orgInput = int(orgInput)
selectedOrg = orgs[orgInput]

# request where to clone repos /Users/rubenclaes/Desktop/
pathInput = input("Where to clone repos? (absolute path, ending on /):")
dirName = selectedOrg["login"]

# create main folder
try:
    os.mkdir(pathInput + dirName)
except FileExistsError:
    print("There already exists a directory with this name!")

# get repositories in organisation
getReposLink = 'https://api.github.com/orgs/{}/repos'.format(selectedOrg["login"])
responseRepos = requests.get(getReposLink, auth=HTTPBasicAuth(username, password))
repos = responseRepos.json()

counter = 0
for repo in repos:
    repoUrl = repo["html_url"]
    repoUrl += '.git'

    # get contributors
    getRepoContributorsLink = 'https://api.github.com/repos/{}/collaborators'.format(repo['full_name'])
    getRepoContributors = requests.get(getRepoContributorsLink, auth=HTTPBasicAuth(username, password))
    repoContributors = getRepoContributors.json()

    # create directory name
    directoryName = ''
    for repoContributor in repoContributors:
        if repoContributor['permissions']['admin']:
            directoryName += repoContributor['login'] + '_'

    directoryName = directoryName[:-1]

    # clone repo
    os.system("git clone {} {}{}/{}/{}".format(repoUrl, pathInput, dirName, directoryName, repo['name']))
    counter += 1

