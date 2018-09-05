class CasoTesteJira():
    key: None
    description: None
    def __init__(self, key, description):
        self.key = key
        self.description = description

CT_DIVISAO_ZERO = CasoTesteJira("POC-563", "Resultado do teste de Divisao por Zero")
CT_FORMATACAO_DECIMAL = CasoTesteJira("POC-510", "Resultado do teste Formatacao Decimal")
CT_TANGENTE_90 = CasoTesteJira("POC-571", "Resultado do teste de Tangente de 90")
PROJECT_POC_KEY = "POC"
ISSUE_BUG_NAME = "Bug"

ISSUELINKTYPE_CAUSED_BY = "Problem/Incident"
ISSUELINKTYPE_CREATE_BY = "Defect"