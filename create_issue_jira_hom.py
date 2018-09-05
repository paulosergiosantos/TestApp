import sys
import requests
import json
import logging
import http

JIRA_URL = 'http://basetestejira.inatel.br:8080/rest/api/latest/issue/'
JIRA_AUTH = {'Authorization': 'Basic dXN1YXJpbzpzZW5oYQ=='}
JIRA_CONTENT = {'Content-Type': 'application/json'}
JIRA_ACCEPT = {'Accept': 'application/json'}
PROJECT_ID = sys.argv[1]
ISSUETYPE_ID = sys.argv[2]
ASSIGNEE_NAME = 'paulosergio'
COMPONENT_SOTWARE_ID = '13302'
TASK_TITLE= sys.argv[3]
CUSTOM_FIELD_10430 = 'High'
CUSTOM_FIELD_10432 = 'Open'
CUSTOM_FIELD_10431 = sys.argv[4]

class Project:
    key = None
    def __init__(self, key):
        self.key = key

class IssueType:
    name = None
    def __init__(self, name):
        self.name = name

class Assignee:
    name = None
    def __init__(self, name):
        self.name = name

class Component:
    id = None
    def __init__(self, id):
        self.id = id

class CustomField:
    value = None
    def __init__(self, value):
        self.value = value

class Fields:
    project = None
    summary = None
    issuetype = None
    customfield_10430 = None
    customfield_10431 = None
    customfield_10432 = None
    #assignee = None
    #components = None
    def __init__(self, project, summary, issuetype, customfield_10430, customfield_10432, customfield_10431):
        self.project = project
        self.summary = summary
        self.issuetype = issuetype
        self.customfield_10430 = customfield_10430
        self.customfield_10431 = customfield_10431
        self.customfield_10432 = customfield_10432

class IssueData:
    fields = None
    def __init__(self, fields):
        self.fields = fields

def obj_to_dict(obj):
   return obj.__dict__

def enable_log(enable=False):
    if enable:
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

enable_log()
project = Project(PROJECT_ID)
issuetype = IssueType(ISSUETYPE_ID)
assignee = Assignee(ASSIGNEE_NAME)
components = [Component(COMPONENT_SOTWARE_ID)]
summary = TASK_TITLE
severity = CustomField(CUSTOM_FIELD_10430)
status = CustomField(CUSTOM_FIELD_10432)
testcase = CUSTOM_FIELD_10431

fields = Fields(project, summary, issuetype, severity, status, testcase)
issueData = IssueData(fields)

post_url = JIRA_URL
post_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}
post_data = json.dumps(issueData.__dict__, default = obj_to_dict)

response = requests.post(post_url, headers = post_headers, data = post_data)
response_content = json.loads(response.content)
print("Status Code:", response.status_code)
print("%s:%s" % ("Issue criada com sucesso" if response.status_code == 201 else "Erro na criação da issue", response_content))
response_data = response.json()
"""
print(json.dumps(response_data, sort_keys=True,
                 indent=4, separators=(',', ': ')))

print(post_data)
print(json.dumps(post_data, sort_keys=True,
                 indent=4,separators=(',', ': ')))
"""
