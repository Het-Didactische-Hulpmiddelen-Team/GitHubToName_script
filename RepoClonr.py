#!/usr/bin/env python3

import os
import requests
from requests.auth import HTTPBasicAuth
import json
import sys
from optparse import OptionParser


# repository cloning function ##########################################################################################
def clone_repos():
    if organisation is None:
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
    else:
        response_org = requests.get('https://api.github.com/orgs/{}'.format(organisation), headers=headers)
        selected_org = response_org.json()

    dir_name = selected_org["login"]

    if path is None:
        # request where to clone repos | PUT DEFAULT PATH HERE #########################################################
        path_input = input("Where to clone repos? (absolute path, ending on /):")
        # path_input = ''
    else:
        path_input = path

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

        # if there are other owners of the organisation (courses with multiple lecturers for example), put them here:
        owners = [username]
        # owners.add("")

        # create directory name
        directory_name = ''
        for repoContributor in repo_contributors:
            if repoContributor['permissions']['admin']:
                contributor_name = github_to_name(repoContributor['login']).replace(" ", "")
                if len(contributor_name) > 0 and repoContributor['login'].strip() not in owners:
                    directory_name += contributor_name + "_"
        directory_name = directory_name[:-1]

        if directory_name.strip():
            # clone repo
            print("git clone {} {}{}/{}/{}".format(repo_url, path_input, dir_name, directory_name, repo['name']))
            # os.system("git clone {} {}{}/{}/{}".format(repo_url, path_input, dir_name, directory_name, repo['name']))

        counter += 1


#   github account name to student name translation ####################################################################
def github_to_name(github):
    if alternative_input is None:
        # github_to_name_response = requests.get('http://server.arne.tech:82/user/{}'.format(github),
        #                                       auth=HTTPBasicAuth(username, password))
        github_to_name_response = requests.get('http://server.arne.tech:82/user/{}'.format(github), headers=headers)
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
    else:
        result = ""
        if github.lower() in name_mappings:
            result += "{}_".format(name_mappings.get(github))
        result = result[:-1]
        return result


# startup parameters ###################################################################################################
parser = OptionParser()
parser.add_option("-o", "--organisation", dest="organisation",
                  help="organisation to be cloned")
parser.add_option("-p", "--path", dest="path", help="path where to clone repos to")
parser.add_option("-i", "--alternative_input", dest="alternative_input", help="give a path to an alternative input (txt file, 3 rows: GitHub_username Firstname Lastname)")

(options, args) = parser.parse_args()
organisation = options.organisation
path = options.path
alternative_input = options.alternative_input

# GitHub login (fallback) LOGIN CREDENTIALS HERE #######################################################################
# username = input("GitHub username:")
# password = input("GitHub password:") # DEPRECATED!
username = ''
headers = {'Authorization': 'token '}

name_mappings = {}
if alternative_input is not None:
    input_file = open(alternative_input, "r")
    for line in input_file:
        split = line.split(" ")
        name_mappings[split[0].lower()] = '{} {}'.format(split[1], split[2].rstrip())

clone_repos()
