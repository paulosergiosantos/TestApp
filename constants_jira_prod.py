class CasoTesteJira():
    key: None
    description: None
    def __init__(self, key, description):
        self.key = key
        self.description = description

CT_DIGITACAO = CasoTesteJira("PV-116", "Resultado do teste de Digitacao")
CT_FORMATACAO_DECIMAL = CasoTesteJira("PV-102", "Resultado do teste Formatacao Decimal")
CT_ADICAO = CasoTesteJira("PV-103", "Resultado do teste de Adicao")
CT_SUBTRACAO = CasoTesteJira("PV-111", "Resultado do teste de Subtracao")
CT_DIVISAO = CasoTesteJira("PV-113", "Resultado do teste de Divisao")
CT_MULTIPLICACAO = CasoTesteJira("PV-112", "Resultado do teste de Multiplicacao")
CT_DIVISAO_ZERO = CasoTesteJira("PV-117", "Resultado do teste de Divisao por Zero")
CT_COSENO = CasoTesteJira("PV-115", "Resultado do teste de Coseno")
CT_SENO = CasoTesteJira("PV-114", "Resultado do teste de Seno")
CT_TANGENTE = CasoTesteJira("PV-106", "Resultado do teste de Tangente")
CT_TANGENTE_90 = CasoTesteJira("PV-107", "Resultado do teste de Tangente de 90")
CT_PORCENTAGEM = CasoTesteJira("PV-118", "Resultado do teste de Porcentagem")
CT_POTENCIACAO = CasoTesteJira("PV-119", "Resultado do teste de Potenciacao")
CT_RAIZ_QUADRADA = CasoTesteJira("PV-120", "Resultado do teste de Raiz Quadrada")

MAP_METODO_CASO_TESTE = {
    "testDigitacao": CT_DIGITACAO,
    "testFormatacaoDecimal": CT_FORMATACAO_DECIMAL,
    "testAdicao": CT_ADICAO,
    "testSubtracao": CT_SUBTRACAO,
    "testMultiplicacao": CT_MULTIPLICACAO,
    "testDivisao": CT_DIVISAO,
    "testDivisaoZero": CT_DIVISAO_ZERO,
    "testCoseno": CT_COSENO,
    "testSeno": CT_SENO,
    "testTangente": CT_TANGENTE,
    "testTangente90": CT_TANGENTE_90,
    "testPorcentagem": CT_PORCENTAGEM,
    "testPotenciacao": CT_POTENCIACAO,
    "testRaizQuadrada": CT_RAIZ_QUADRADA,
}

CASO_TESTE_KEYS = [casoTeste.key for method, casoTeste in MAP_METODO_CASO_TESTE.items()]

PROJECT_POC_KEY = "PV"
ISSUE_BUG_NAME = "Bug"
ISSUE_TESTEXEC_NAME = "Test Execution"
ISSUE_TESTEXEC_KEY = "PV-108"

ISSUELINKTYPE_BLOCKS_BY = "Blocks"
ISSUELINKTYPE_CAUSED_BY = "Problem/Incident"
ISSUELINKTYPE_CREATE_BY = "Defect"

#TEST_STATUS_BACKLOG_ID = "41"
TEST_STATUS_IN_PROGRESS_ID = "51"#"11"
TEST_STATUS_READY_TO_TEST_ID = "21"
TEST_STATUS_TESTING_ID = "31"
TEST_STATUS_RETESTING_ID = "51"
TEST_STATUS_DONE_ID = "41"

TESTEXEC_STATUS_OPEN = "51"
TESTEXEC_STATUS_IN_PROGRESS = "41"
TESTEXEC_STATUS_DONE = "31"

TEST_RESOLUTION_PASSED = "Passed"
TEST_RESOLUTION_FAILED = "Failed"
TEST_RESOLUTION_BLOCKED = "Blocked"
TEST_RESOLUTION_TESTED = "Tested"

TESTRUN_STATUS_TODO="TODO"
TESTRUN_STATUS_EXECUTING="EXECUTING"
TESTRUN_STATUS_PASS="PASS"
TESTRUN_STATUS_FAIL="FAIL"
TESTRUN_STATUS_ABORTED="ABORTED"

JIRA_SERVER_URL = "http://jira.inatel.br/jira"
JIRA_ISSUE_URL = JIRA_SERVER_URL + "/rest/api/latest/issue"
JIRA_ISSUELINK_URL = JIRA_SERVER_URL + "/rest/api/latest/issueLink"
JIRA_ISSUE_TRANSITION_URL = JIRA_SERVER_URL + "/rest/api/latest/issue/{}/transitions"
JIRA_TESTRUN_ADD_DEFECT_URL = JIRA_SERVER_URL + "/rest/raven/1.0/api/testrun/{}/defect"
JIRA_TESTRUN_ADD_ATTACHMENT_URL = JIRA_SERVER_URL + "/rest/raven/1.0/api/testrun/{}/attachment"
JIRA_TESTRUN_CHANGE_STATUS_URL = JIRA_SERVER_URL + "/rest/raven/1.0/api/testrun/{}/status?status={}"
JIRA_TESTRUN_GET_ID_URL = JIRA_SERVER_URL + "/rest/raven/1.0/api/testrun?testExecIssueKey={}&testIssueKey={}"
JIRA_TESTEXEC_ADD_TEST_URL = JIRA_SERVER_URL + "/rest/raven/1.0/api/testexec/{}/test"

JIRA_AUTH = {'Authorization': 'Basic dXN1YXJpbzpzZW5oYQ=='}
JIRA_CONTENT = {'Content-Type': 'application/json'}
JIRA_ACCEPT = {'Accept': 'application/json'}

if __name__ == '__main__':
    print(CASO_TESTE_KEYS)