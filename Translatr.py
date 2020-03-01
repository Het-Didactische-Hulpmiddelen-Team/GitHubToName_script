#!/usr/bin/env python3

import requests
from optparse import OptionParser


# github account name to student name translation ######################################################################
def github_to_name():
    # check if alternative input is defined
    if alternative_input is None:
        github_to_name_response = requests.get('http://server.arne.tech:82/user/{}'.format(github_username),
                                               headers=headers)
        # check if API call was successful
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
            return github_to_name_string[0][0]

    # use alternative input for mappings
    else:
        result = ""
        if github_username.lower() in name_mappings:
            result += name_mappings.get(github_username)
        return result


# student name to github account name translation ######################################################################
def name_to_github():
    # check if alternative input is provided
    if alternative_input is None:
        # build name
        name_new = "{} {}".format(student_firstname, student_lastname)
        # call GitHub to Name (Translatr) API
        name_to_github_response = requests.get('http://server.arne.tech:82/name/{}'.format(name_new), headers=headers)
        # check if API call was successful
        if name_to_github_response.status_code is not 200:
            raise Exception('Translatr API call error, contact DHT (status code {})'
                            .format(name_to_github_response.status_code))
        name_to_github_string = name_to_github_response.json()

        # build username
        if len(name_to_github_string) == 0:
            return ""
        else:
            return name_to_github_string[0][1][11:]

    # use alternative input for mappings
    else:
        name = "{} {}".format(student_firstname, student_lastname)
        for key, value in name_mappings.items():
            if value == name:
                return key


# script options #######################################################################################################
parser = OptionParser()
parser.add_option("-u", "--github_username", dest="github_username",
                  help="translate github account name to student name")
parser.add_option("-n", "--name", dest="student_name",
                  help="translate student name to github account name (e.g. Firstname Lastname)", nargs=2)
parser.add_option("-i", "--alternative_input", dest="alternative_input",
                  help="give a path to an alternative input (txt file, 3 rows: GitHub_username Firstname Lastname)")
(options, args) = parser.parse_args()
github_username = options.github_username
alternative_input = options.alternative_input

# handle name input
if options.student_name is not None:
    student_firstname = options.student_name[0]
    student_lastname = options.student_name[1]

# GitHub login - LOGIN CREDENTIALS HERE ################################################################################
username = ''
headers = {'Authorization': 'token '}

# alternative mappings input handled here ##############################################################################
name_mappings = {}
if alternative_input is not None:
    input_file = open(alternative_input, "r")
    for line in input_file:
        split = line.split(" ")
        name_mappings[split[0].lower()] = '{} {}'.format(split[1], split[2].rstrip())

if github_username is not None:
    print(github_to_name())
else:
    if student_firstname is not None and student_lastname is not None:
        print(name_to_github())
