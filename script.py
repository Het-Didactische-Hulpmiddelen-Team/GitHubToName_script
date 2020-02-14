import os
import requests
from requests.auth import HTTPBasicAuth
import json
import sys
from optparse import OptionParser


# repository cloning function
def clone_repos():
    # request all organisations
    # response_orgs = requests.get('https://api.github.com/user/orgs', auth=HTTPBasicAuth(username, password))
    response_orgs = requests.get('https://api.github.com/user/orgs', headers=headers)
    orgs = response_orgs.json()

    # request which organisation
    counter = 0
    for org in orgs:
        organisation_name = org["login"]
        item = "{}. {}".format(counter, organisation_name)
        print(item)
        counter += 1

    org_input = input("Which organisation? (give number):")
    org_input = int(org_input)
    selected_org = orgs[org_input]
    dir_name = selected_org["login"]

    # request where to clone repos | PUT DEFAULT PATH HERE #############################################################
    path_input = input("Where to clone repos? (absolute path, ending on /):")
    # path_input = ''
    # ##################################################################################################################

    # create main folder
    try:
        os.mkdir(path_input + dir_name)
    except FileExistsError:
        print("There already exists a directory with this name!")

    # get repositories in organisation
    get_repos_link = 'https://api.github.com/orgs/{}/repos'.format(selected_org["login"])
    # response_repos = requests.get(get_repos_link, auth=HTTPBasicAuth(username, password))
    response_repos = requests.get(get_repos_link, headers=headers)
    repos = response_repos.json()

    counter = 0
    for repo in repos:
        repo_url = repo["html_url"]
        repo_url += '.git'

        # get contributors
        get_repo_contributors_link = 'https://api.github.com/repos/{}/collaborators'.format(repo['full_name'])
        # get_repo_contributors = requests.get(get_repo_contributors_link, auth=HTTPBasicAuth(username, password))
        get_repo_contributors = requests.get(get_repo_contributors_link, headers=headers)
        repo_contributors = get_repo_contributors.json()

        # create directory name
        directory_name = ''
        for repoContributor in repo_contributors:
            if repoContributor['permissions']['admin']:
                contributor_name = github_to_name(repoContributor['login']).replace(" ", "")
                if len(contributor_name) > 0 and repoContributor['login'].strip() != username.strip():
                    directory_name += contributor_name + "_"
        directory_name = directory_name[:-1]

        # clone repo
        # print("git clone {} {}{}/{}/{}".format(repo_url, path_input, dir_name, directory_name, repo['name']))
        os.system("git clone {} {}{}/{}/{}".format(repo_url, path_input, dir_name, directory_name, repo['name']))
        counter += 1


#   github account name to student name translation
def github_to_name(github):
    # github_to_name_response = requests.get('http://server.arne.tech:80/user/{}'.format(github),
    #                                       auth=HTTPBasicAuth(username, password))
    github_to_name_response = requests.get('http://server.arne.tech:80/user/{}'.format(github), headers=headers)
    github_to_name_string = github_to_name_response.json()
    if len(github_to_name_string) == 1:
        return github_to_name_string[0][0]
    elif len(github_to_name_string) == 0:
        return ""
    else:
        result = ""
        for element in github_to_name_string:
            if len(element[0]) > 0:
                result += element[0] + "_"
        result = result[:-1]
        return result


#   student name to github account name translation
def name_to_github(name):
    name_split = name.split("_")
    name_new = "{} {}".format(name_split[0], name_split[1])
    # name_to_github_response = requests.get('http://server.arne.tech:80/name/{}'.format(name_new),
    #                                       auth=HTTPBasicAuth(username, password))
    name_to_github_response = requests.get('http://server.arne.tech:80/name/{}'.format(name_new), headers=headers)
    name_to_github_string = name_to_github_response.json()
    if len(name_to_github_string) == 0:
        return ""
    else:
        return name_to_github_string[0][1][11:]


# startup parameters
parser = OptionParser()
parser.add_option("-c", "--clone", action="store_true", dest="clone", default=True,
                  help="activates cloning mode (default)")
parser.add_option("-t", "--translate", dest="github_username",
                  help="translate github account name to student name")
parser.add_option("-r", "--reverse_translate", dest="student_name",
                  help="translate student name to github account name (e.g. Firstname_Lastname)")
(options, args) = parser.parse_args()
clone = options.clone
github_username = options.github_username
student_name = options.student_name

# GitHub login (fallback) LOGIN CREDENTIALS HERE #######################################################################
# username = input("GitHub username:")
# password = input("GitHub password:") # DEPRECATED!
username = ''
headers = {'Authorization': 'token '}
# ######################################################################################################################

if github_username is not None:
    print(github_to_name(github_username))
else:
    if student_name is not None:
        print(name_to_github(student_name))
    else:
        clone_repos()

# vragen
# Voornaam achternaam schijden door underscore of gewoon spatie?
# clonen goed? mappen structuur enzo
# soms andere lectoren mee in organisatie?
# meerdere repos per leerling?