class CasoTesteJira():
    key: None
    description: None
    def __init__(self, key, description):
        self.key = key
        self.description = description


CT_FORMATACAO_DECIMAL = CasoTesteJira("POC-510", "Resultado do teste Formatacao Decimal")
CT_SUBTRACAO = CasoTesteJira("POC-545", "Resultado do teste de Subtracao")
CT_ADICAO = CasoTesteJira("POC-549", "Resultado do teste de Adicao")
CT_DIGITACAO = CasoTesteJira("POC-550", "Resultado do teste de Digitacao")
CT_DIVISAO = CasoTesteJira("POC-551", "Resultado do teste de Divisao")
CT_PORCENTAGEM = CasoTesteJira("POC-552", "Resultado do teste de Porcentagem")
CT_DIVISAO_ZERO = CasoTesteJira("POC-563", "Resultado do teste de Divisao por Zero")
CT_MULTIPLICACAO = CasoTesteJira("POC-565", "Resultado do teste de Multiplicacao")
CT_COSENO = CasoTesteJira("POC-566", "Resultado do teste de Coseno")
CT_SENO = CasoTesteJira("POC-567", "Resultado do teste de Seno")
CT_TANGENTE = CasoTesteJira("POC-568", "Resultado do teste de Tangente")
CT_POTENCIACAO = CasoTesteJira("POC-569", "Resultado do teste de Potenciacao")
CT_RAIZ_QUADRADA = CasoTesteJira("POC-570", "Resultado do teste de Raiz Quadrada")
CT_TANGENTE_90 = CasoTesteJira("POC-571", "Resultado do teste de Tangente de 90")

PROJECT_POC_KEY = "POC"
ISSUE_BUG_NAME = "Bug"
ISSUE_TESTEXEC_KEY = "POC-546"

ISSUELINKTYPE_BLOCKS_BY = "Blocks"
ISSUELINKTYPE_CAUSED_BY = "Problem/Incident"
ISSUELINKTYPE_CREATE_BY = "Defect"
TEST_STATUS_BACKLOG_ID = "11"
TEST_STATUS_IN_PROGRESS_ID = "31"
TEST_STATUS_DONE_ID = "41"

TESTRUN_STATUS_TODO="TODO"
TESTRUN_STATUS_EXECUTING="EXECUTING"
TESTRUN_STATUS_PASS="PASS"
TESTRUN_STATUS_FAIL="FAIL"
TESTRUN_STATUS_ABORTED="ABORTED"
