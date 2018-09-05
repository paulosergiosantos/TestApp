import sys
import requests
import json
import logging
import http
from constants_jira import PROJECT_POC_KEY, ISSUE_BUG_NAME, CT_TANGENTE_90, ISSUELINKTYPE_CREATE_BY

JIRA_ISSUE_URL = 'http://basetestejira.inatel.br:8080/rest/api/latest/issue/'
JIRA_ISSUELINK_URL = 'http://basetestejira.inatel.br:8080/rest/api/latest/issueLink/'
JIRA_AUTH = {'Authorization': 'Basic 000'}
JIRA_CONTENT = {'Content-Type': 'application/json'}
JIRA_ACCEPT = {'Accept': 'application/json'}

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
    issuetype = None
    summary = None
    description = None
    def __init__(self, project, issuetype, summary, description):
        self.project = project
        self.issuetype = issuetype
        self.summary = summary
        self.description = description
 
class IssueData:
    fields = None
    def __init__(self, fields):
        self.fields = fields

class WardIssue:
    key: None
    def __init__(self, key):
        self.key = key

class IssueLinkType:
    name: None
    def __init__(self, name):
        self.name = name

class IssueLink:
    type: None
    inwardIssue: None
    outwardIssue: None
    def __init__(self, type, inwardIssue, outwardIssue):
        self.type = type
        self.inwardIssue = inwardIssue
        self.outwardIssue = outwardIssue

class Response:
    STATUS_OK = "OK"
    STATUS_ERROR = "ERROR"

    status: None
    key: None
    description: None
    def __init__(self, status, key, description=""):
        self.status = status
        self.key = key
        self.description = description

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

class CreateIssueHandler():

    def createIssue(self, project, issuetype, summary, description):
        fields = Fields(project, issuetype, summary, description)
        issueData = IssueData(fields)

        post_url = JIRA_ISSUE_URL
        post_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}
        post_data = json.dumps(issueData.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = post_headers, data = post_data)
        print("Status Code:", response.status_code)
        response_content = response.json()
        print("%s:%s" % ("Issue criada com sucesso" if response.status_code == 201 else "Erro na criação da issue", response_content))
        return Response(
            Response.STATUS_OK if response.status_code == 201 else Response.STATUS_ERROR, 
            response_content['key'] if response.status_code == 201 else str(response.status_code),
            response_content)

    def createIssueWithRawData(self, projectKey, issuetypeName, summary, description):
        project = Project(projectKey)
        issuetype = IssueType(issuetypeName)
        return self.createIssue(project, issuetype, summary, description)

    def createIssueLink(self, issueLinkType, inwardIssue, outwardIssue):
        issueLink = IssueLink(issueLinkType, inwardIssue, outwardIssue)
        post_url = JIRA_ISSUELINK_URL
        post_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}
        post_data = json.dumps(issueLink.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = post_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("%s" % ("Link criado com sucesso" if response.status_code == 201 else "Erro na criação do link"))

    def createIssueLinkWithRawData(self, typeName, inIssueKey, outIssueKey):
        issueLinkType = IssueLinkType(typeName)
        inwardIssue = WardIssue(inIssueKey)
        outwardIssue = WardIssue(outIssueKey)
        self.createIssueLink(issueLinkType, inwardIssue, outwardIssue)        

if __name__ == '__main__':
    #enable_log()
    createIssueHandler = CreateIssueHandler()
    project_id = PROJECT_POC_KEY
    issueetype_id = ISSUE_BUG_NAME
    summary = CT_TANGENTE_90.description
    project = Project(project_id)
    issuetype = IssueType(issueetype_id)
    description = (
        "tan(90)=Limiteexcedido' != 'tan(90)=Valor inexistente'\n"
        "- tan(90)=Limiteexcedido\n"
        "+ tan(90)=Valor inexistente\n"
        ": Resultado do teste de Tangente de 90º"
    )
    response = createIssueHandler.createIssue(project, issuetype, summary, description)
    createIssueHandler.createIssueLinkWithRawData(ISSUELINKTYPE_CREATE_BY, CT_TANGENTE_90.key, response.key)
    sys.exit
