#!/usr/bin/env python3

""" HELP ###############################################################################################################
script functionality:
    - clone all repositories from a certain organisation
    - all repo's will be put in a directory with the name(s) of the student(s) who own(s) the repository

script options:
    - "h" help, gives information about the options
    - "o" organisation, directly choose the organisation you want to clone
    - "p" path, give the path where the organisation can be cloned on your pc
    - "i" alternative input, give a path to an alternative input txt file (must be according to the template)
#####################################################################################################################"""

import os
import requests
from optparse import OptionParser


# check if api call was successful #####################################################################################
def check_request(status):
    if status is not 200:
        raise Exception('API call error, check your login credentials (status code {})'.format(status))


# repository cloning function ##########################################################################################
def clone_repos():
    # check if organisation has been provided directly
    if organisation is None:
        # request all organisations from github api
        response_orgs = requests.get('https://api.github.com/user/orgs', headers=headers)
        check_request(response_orgs.status_code)
        orgs = response_orgs.json()

        # request which organisation will be cloned (interactive input)
        for count, org in enumerate(orgs):
            organisation_name = org["login"]
            item = "{}. {}".format(count, organisation_name)
            print(item)

        org_input = input("Which organisation? (give number):")
        org_input = int(org_input)
        selected_org = orgs[org_input]
    else:
        # direct api call (when organisation directly provided with)
        response_org = requests.get('https://api.github.com/orgs/{}'.format(organisation), headers=headers)
        check_request(response_org.status_code)
        selected_org = response_org.json()

    # get the organisation name
    dir_name = selected_org["login"]

    # check if output path has been provided directly
    if path is None:
        # request where to clone repos | PUT DEFAULT PATH HERE #########################################################
        path_input = input("Where to clone repos? (absolute path, ending on /):")
        # path_input = 'default_path/'
    else:
        # direct output path
        path_input = path

    # create main folder
    try:
        os.mkdir(path_input + dir_name)
    except FileExistsError:
        raise Exception("There already exists a directory with this name! (path: {}{})".format(path_input, dir_name))

    # get repositories in organisation
    get_repos_link = 'https://api.github.com/orgs/{}/repos'.format(selected_org["login"])
    response_repos = requests.get(get_repos_link, headers=headers)
    check_request(response_repos.status_code)
    repos = response_repos.json()

    # clone all repos in the organisation
    for count, repo in enumerate(repos):
        # build the repo url
        repo_url = repo["html_url"]
        repo_url += '.git'

        # get contributors of the repo
        get_repo_contributors_link = 'https://api.github.com/repos/{}/collaborators'.format(repo['full_name'])
        get_repo_contributors = requests.get(get_repo_contributors_link, headers=headers)
        check_request(get_repo_contributors.status_code)
        repo_contributors = get_repo_contributors.json()

        # if there are other owners of the organisation (courses with multiple lecturers for example), put them here: ##
        # otherwise they show up in the directory names of the repos!
        owners = [username]

        # build directory name
        directory_name = ''
        for repoContributor in repo_contributors:
            # check of contributor has right permissions
            if repoContributor['permissions']['admin']:
                # translate names
                contributor_name = github_to_name(repoContributor['login']).replace(" ", "")

                # check if length of name is 0, this is the case when the name does not exist in the GitHub to Name
                # translation database
                if len(contributor_name) > 0 and repoContributor['login'].strip() not in owners:
                    directory_name += contributor_name + "_"

        # remove last '_'
        directory_name = directory_name[:-1]

        # check if directory name is empty
        if not directory_name.strip():
            directory_name += 'no_student_names_found'

        # clone repo
        os.system("git clone {} {}{}/{}/{}".format(repo_url, path_input, dir_name, directory_name, repo['name']))


# github account name to student name translation ######################################################################
def github_to_name(github):
    # check if alternative input has been provided
    if alternative_input is None:
        # call the GitHub to Name (Translatr) API to translate the names
        github_to_name_response = requests.get('http://server.arne.tech:82/user/{}'.format(github), headers=headers)
        if github_to_name_response.status_code is not 200:
            raise Exception('Translatr API call error, contact DHT (status code {})'
                            .format(github_to_name_response.status_code))
        github_to_name_string = github_to_name_response.json()

        # build name
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

    # use alternative input
    else:
        result = ""
        if github.lower() in name_mappings:
            result += "{}_".format(name_mappings.get(github))
        result = result[:-1]
        return result


# script options #######################################################################################################
parser = OptionParser()
parser.add_option("-o", "--organisation", dest="organisation",
                  help="organisation to be cloned")
parser.add_option("-p", "--path", dest="path", help="path where to clone repos to")
parser.add_option("-i", "--alternative_input", dest="alternative_input",
                  help="path to an alternative input (txt file, 3 rows: GitHub_username Firstname Lastname)")

(options, args) = parser.parse_args()
organisation = options.organisation
path = options.path
alternative_input = options.alternative_input

# GitHub login - LOGIN CREDENTIALS HERE ################################################################################
username = ''  # GitHub username
headers = {'Authorization': 'token '}  # GitHub token
# example (https://github.com/settings/tokens)
# headers = {'Authorization': 'token abcd1234abcd1234abcd1234abcd1234abcd1234'}


# alternative mappings input handled here ##############################################################################
name_mappings = {}
if alternative_input is not None:
    input_file = open(alternative_input, "r")
    for line in input_file:
        split = line.split(" ")
        name_mappings[split[0].lower()] = '{} {}'.format(split[1], split[2].rstrip())


clone_repos()
