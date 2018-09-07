import sys
import requests
import json
import logging
import http
from constants_jira import PROJECT_POC_KEY, ISSUE_BUG_NAME, ISSUE_TESTEXEC_KEY, CT_TANGENTE_90, ISSUELINKTYPE_CREATE_BY
from constants_jira import TEST_STATUS_IN_PROGRESS_ID, TESTRUN_STATUS_FAIL, TESTRUN_STATUS_PASS, TESTRUN_STATUS_EXECUTING

JIRA_ISSUE_URL = 'http://basetestejira.inatel.br:8080/rest/api/latest/issue/'
JIRA_ISSUELINK_URL = 'http://basetestejira.inatel.br:8080/rest/api/latest/issueLink/'
JIRA_ISSUE_TRANSITION_URL = 'http://basetestejira.inatel.br:8080/rest/api/latest/issue/{}/transitions'
JIRA_ISSUELINK_DEFECT_URL = 'http://basetestejira.inatel.br:8080/rest/raven/1.0/api/testrun/{}/defect'
JIRA_ISSUE_CHANGE_STATUS_URL = 'http://basetestejira.inatel.br:8080/rest/raven/1.0/api/testrun/{}/status?status={}'
JIRA_GET_TESTRUN_ID_URL = 'http://basetestejira.inatel.br:8080/rest/raven/1.0/api/testrun?testExecIssueKey={}&testIssueKey={}'

JIRA_AUTH = {'Authorization': 'Basic cGF1bG9zZXJnaW86MGx1YXBSMDFudWo='}
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

class Transition():
    id: None
    def __init__(self, id):
        self.id = id

class IssueTransition():
    transition: None
    def __init__(self, transition):
        self.transition = transition

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

    def changeIssueTransition(self, issueKey, transitionId):
        transition = Transition(transitionId)
        issueTransition = IssueTransition(transition)
        post_url = JIRA_ISSUE_TRANSITION_URL.format(issueKey)
        post_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}
        post_data = json.dumps(issueTransition.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = post_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("%s:%s(%s)" % ("Sucesso na alteracao do status da issue" if response.status_code == 204 else "Erro na alteracao do status da issue", issueKey, transitionId))

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

    def createIssueLinkDefect(self, testRunIssueId, issueBugKey):
        issueBugKeyArr = [issueBugKey]
        post_url = JIRA_ISSUELINK_DEFECT_URL.format(testRunIssueId)
        post_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}
        post_data = json.dumps(issueBugKeyArr)
        print(post_data)
        response = requests.post(post_url, headers = post_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("%s" % ("Defeito criado com sucesso" if response.status_code == 200 else "Erro na criação do defeito"))   

    def changeIssueTestRunStatus(self, testRunIssueId, status):
        put_url = JIRA_ISSUE_CHANGE_STATUS_URL.format(testRunIssueId, status)
        post_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}
        post_data = {}
        print(post_data)
        response = requests.put(put_url, headers = post_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("%s" % ("Status alterado com sucesso" if response.status_code == 200 else "Erro na alteracao do status"))  

    def getTestRunId(self, testExecIssueKey, testIssueKey):
        get_url = JIRA_GET_TESTRUN_ID_URL.format(testExecIssueKey, testIssueKey)
        get_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}
        response = requests.get(get_url, headers = get_headers)
        print("Status Code:", response.status_code)
        testRunId = 0
        if (response.status_code == 200):
            response_content = response.json()
            testRunId = response_content['id']
        print("Id da TestExecutionKey(%s) e TestIssueKey(%s): %s" % (testExecIssueKey, testIssueKey, str(testRunId)))        
        return testRunId

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
    #createIssueHandler.createIssueLinkWithRawData(ISSUELINKTYPE_CREATE_BY, CT_TANGENTE_90.key, response.key)
    testRunId = createIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, CT_TANGENTE_90.key)
    createIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_EXECUTING)
    createIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_PASS)
    createIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_FAIL)
    createIssueHandler.changeIssueTransition(CT_TANGENTE_90.key, TEST_STATUS_IN_PROGRESS_ID)
    createIssueHandler.createIssueLinkDefect(testRunId, response.key)
    
    
    sys.exit
