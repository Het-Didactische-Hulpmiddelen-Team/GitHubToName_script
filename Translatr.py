#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
from optparse import OptionParser


#   github account name to student name translation ####################################################################
def github_to_name():
    if alternative_input is None:
        # github_to_name_response = requests.get('http://server.arne.tech:82/user/{}'.format(github),
        #                                       auth=HTTPBasicAuth(username, password))
        github_to_name_response = requests.get('http://server.arne.tech:82/user/{}'.format(github_username),
                                               headers=headers)
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
        if github_username.lower() in name_mappings:
            result += "{}_".format(name_mappings.get(github_username))
        result = result[:-1]
        return result


#   student name to github account name translation ####################################################################
def name_to_github():
    if alternative_input is None:
        name_new = "{} {}".format(student_firstname, student_lastname)
        # name_to_github_response = requests.get('http://server.arne.tech:82/name/{}'.format(name_new),
        #                                       auth=HTTPBasicAuth(username, password))
        name_to_github_response = requests.get('http://server.arne.tech:82/name/{}'.format(name_new), headers=headers)
        name_to_github_string = name_to_github_response.json()

        if len(name_to_github_string) == 0:
            return ""
        else:
            return name_to_github_string[0][1][11:]
    else:
        name = "{} {}".format(student_firstname, student_lastname)
        for key, value in name_mappings.items():
            if value == name:
                return key


# startup parameters ###################################################################################################
parser = OptionParser()
parser.add_option("-u", "--github_username", dest="github_username",
                  help="translate github account name to student name")
parser.add_option("-n", "--name", dest="student_name",
                  help="translate student name to github account name (e.g. Firstname Lastname)", nargs=2)
parser.add_option("-i", "--alternative_input", dest="alternative_input", help="give a path to an alternative input (txt file, 3 rows: GitHub_username Firstname Lastname)")
(options, args) = parser.parse_args()
github_username = options.github_username
alternative_input = options.alternative_input

if options.student_name is not None:
    student_firstname = options.student_name[0]
    student_lastname = options.student_name[1]

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

if github_username is not None:
    print(github_to_name())
else:
    if student_firstname is not None and student_lastname is not None:
        print(name_to_github())
