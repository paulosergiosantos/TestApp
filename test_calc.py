# Android environment
import unittest, os
from appium import webdriver
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from create_issue_jira_hom import CreateIssueHandler
from create_issue_jira_hom import Response
from create_issue_jira_hom import IssueLinkType
from constants_jira import CT_DIVISAO_ZERO, CT_FORMATACAO_DECIMAL, CT_TANGENTE_90
from constants_jira import CT_ADICAO, CT_SUBTRACAO, CT_MULTIPLICACAO, CT_DIVISAO
from constants_jira import CT_SENO, CT_COSENO, CT_TANGENTE
from constants_jira import CT_DIGITACAO, CT_PORCENTAGEM, CT_POTENCIACAO, CT_RAIZ_QUADRADA
from constants_jira import PROJECT_POC_KEY, ISSUE_BUG_NAME, ISSUE_TESTEXEC_KEY, ISSUELINKTYPE_CREATE_BY, ISSUELINKTYPE_BLOCKS_BY
from constants_jira import TEST_STATUS_DONE_ID, TEST_STATUS_IN_PROGRESS_ID, TEST_STATUS_BACKLOG_ID
from constants_jira import TESTRUN_STATUS_TODO, TESTRUN_STATUS_EXECUTING, TESTRUN_STATUS_PASS, TESTRUN_STATUS_FAIL, TESTRUN_STATUS_ABORTED

LOGGER.setLevel(logging.INFO)

class TestCalc(unittest.TestCase):

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps['udid'] = '4df1730065835fb7'
        self.desired_caps['platformName'] = 'android'
        self.desired_caps['deviceName'] = 'Inatel(GT-I9300)'
        self.desired_caps['appPackage'] = 'com.sec.android.app.popupcalculator'
        self.desired_caps['appActivity'] = 'com.sec.android.app.popupcalculator.Calculator'
        self.screenshot_dir = os.getenv('SCREENSHOT_PATH', '') or os.getcwd() + "/screenshots"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.createIssueHandler = CreateIssueHandler()
        #self.imprimirTodosElements()

    def imprimirTodosElements(self):
        #textElements = self.driver.find_elements_by_class_name('android.widget.TextView')
        #print(textElements)
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for e in elements:
            print(e.__getattribute__('id'), e.get_attribute("resourceId"))

    def iniciarCasoTeste(self, casoDeTeste):
        self.createIssueHandler.changeIssueTransition(casoDeTeste.key, TEST_STATUS_IN_PROGRESS_ID)
        testRunId = self.createIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
        self.createIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_EXECUTING)

    def finalizarCasoTeste(self, casoDeTeste, testRunStatus):
        self.createIssueHandler.changeIssueTransition(casoDeTeste.key, TEST_STATUS_DONE_ID)
        testRunId = self.createIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
        self.createIssueHandler.changeIssueTestRunStatus(testRunId, testRunStatus)

    def criarBugJira(self, casoDeTeste, exception):
            response = self.createIssueHandler.createIssueWithRawData(PROJECT_POC_KEY, ISSUE_BUG_NAME, casoDeTeste.description, str(exception))
            if (response.status == Response.STATUS_OK):
                #self.createIssueHandler.createIssueLinkWithRawData(ISSUELINKTYPE_BLOCKS_BY, casoDeTeste.key, response.key)
                testRunId = self.createIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
                self.createIssueHandler.createIssueLinkDefect(testRunId, response.key)

    def realizarOperacao(self, digitos1, digitos2, operador, primeiroOperador=False):
        if (primeiroOperador):
            operadorElement = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_' + str(operador))
            operadorElement.click()  

        for digito in digitos1:
            digitoElement = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_0' + str(digito))
            digitoElement.click()

        if (not primeiroOperador):
            operadorElement = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_' + str(operador))
            operadorElement.click()   

        for digito in digitos2:
            digitoElement = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_0' + str(digito))
            digitoElement.click()

        operadorIgualElement = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_equal')
        operadorIgualElement.click()

        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        resultadoVisor = resultadoVisor.replace("\n", "").replace(" ","")

        return resultadoVisor
    
    def testDigitosCorretos(self):
        self.iniciarCasoTeste(CT_DIGITACAO)
        for i in range(9, -1, -1):
            numero_id = 'com.sec.android.app.popupcalculator:id/bt_0' + str(i)
            print(numero_id)
            numero = self.driver.find_element_by_id(numero_id)
            numero.click()
        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        resultadoVisor = resultadoVisor.replace(",", "").replace(".","")
        testRunStatus = TESTRUN_STATUS_PASS

        try:
            self.assertEqual(resultadoVisor, "9876543210", CT_DIGITACAO.description)
        except AssertionError as exception:
            self.criarBugJira(CT_DIGITACAO, exception)
            testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(CT_DIGITACAO, testRunStatus)
    
    def testAdicao(self):
        self.iniciarCasoTeste(CT_ADICAO)
        resultadoVisor = self.realizarOperacao([2], [4], "add")
        self.assertEqual(resultadoVisor, "2+4=6", CT_ADICAO.description)
        self.finalizarCasoTeste(CT_ADICAO, TESTRUN_STATUS_PASS)

    def testSubtracao(self):
        self.iniciarCasoTeste(CT_SUBTRACAO)
        resultadoVisor = self.realizarOperacao([4], [2], "sub")
        self.assertEqual(resultadoVisor, "4" + u"\u2212" + "2=2", CT_SUBTRACAO.description)
        self.finalizarCasoTeste(CT_SUBTRACAO, TESTRUN_STATUS_PASS)

    def testMultiplicacao(self):
        self.iniciarCasoTeste(CT_MULTIPLICACAO)
        resultadoVisor = self.realizarOperacao([4], [2,0], "mul")
        self.assertEqual(resultadoVisor, "4" + u"\u00D7" + "20=80", CT_MULTIPLICACAO.description)
        self.finalizarCasoTeste(CT_MULTIPLICACAO, TESTRUN_STATUS_PASS)

    def testDivisao(self):
        self.iniciarCasoTeste(CT_DIVISAO)
        resultadoVisor = self.realizarOperacao([4,0], [2], "div")
        self.assertEqual(resultadoVisor, "40÷2=20", CT_DIVISAO.description)
        self.finalizarCasoTeste(CT_DIVISAO, TESTRUN_STATUS_PASS)
   
    def testPorcentagem(self):
        self.iniciarCasoTeste(CT_PORCENTAGEM)
        resultadoVisor = self.realizarOperacao([4,0,0], [2,0], "persentage")
        self.assertEqual(resultadoVisor, "400%" + u"\u00D7" + "20=80", CT_PORCENTAGEM.description)   
        self.finalizarCasoTeste(CT_PORCENTAGEM, TESTRUN_STATUS_PASS)

    def testPotencia(self):
        self.iniciarCasoTeste(CT_POTENCIACAO)
        resultadoVisor = self.realizarOperacao([2], [3], "x_y")
        self.assertEqual(resultadoVisor, "2^(3)=8", CT_POTENCIACAO.description)  
        self.finalizarCasoTeste(CT_POTENCIACAO, TESTRUN_STATUS_PASS)

    def testRaizQuadrada(self):
        self.iniciarCasoTeste(CT_RAIZ_QUADRADA)
        resultadoVisor = self.realizarOperacao([9], [], "root", True)
        self.assertEqual(resultadoVisor, u"\u221A" + "(9)=3", CT_RAIZ_QUADRADA.description)  
        self.finalizarCasoTeste(CT_RAIZ_QUADRADA, TESTRUN_STATUS_PASS)
 
    def testCoseno(self):
        self.iniciarCasoTeste(CT_COSENO)
        resultadoVisor = self.realizarOperacao([9,0], [], "cos", True)
        self.assertEqual(resultadoVisor, "cos(90)=0", CT_COSENO.description)  
        self.finalizarCasoTeste(CT_COSENO, TESTRUN_STATUS_PASS)

    def testSeno(self):
        self.iniciarCasoTeste(CT_SENO)
        resultadoVisor = self.realizarOperacao([9,0], [], "sin", True)
        self.assertEqual(resultadoVisor, "sin(90)=1", CT_SENO.description) 
        self.finalizarCasoTeste(CT_SENO, TESTRUN_STATUS_PASS) 

    def testTangente(self):
        self.iniciarCasoTeste(CT_TANGENTE)
        resultadoVisor = self.realizarOperacao([4,5], [], "tan", True)
        self.assertEqual(resultadoVisor, "tan(45)=1", CT_TANGENTE.description)
        #self.createIssueHandler.createIssue("POC", "Rodada de Teste", "Resultado do teste de Tangente", "")
        self.finalizarCasoTeste(CT_TANGENTE, TESTRUN_STATUS_PASS)
    
    #Simula um erro: formatacao decimal não está em portugues
    def testFormatacaoDecimal(self):
        self.iniciarCasoTeste(CT_FORMATACAO_DECIMAL)
        for i in range(4, 0, -1):
            numero_id = 'com.sec.android.app.popupcalculator:id/bt_0' + str(i)
            print(numero_id)
            numero = self.driver.find_element_by_id(numero_id)
            numero.click()
        separadorDecimal = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_dot')
        numero0= self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_00')
        numero5 = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_05')
        separadorDecimal.click()
        numero0.click()
        numero5.click()
        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        testRunStatus = TESTRUN_STATUS_PASS

        try:
            self.assertEqual(resultadoVisor, "4.321,05", CT_FORMATACAO_DECIMAL.description)
        except AssertionError as exception:
            self.criarBugJira(CT_FORMATACAO_DECIMAL, exception)
            testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(CT_FORMATACAO_DECIMAL, testRunStatus)

    #Simula um caso de erro: mensagem da divisao por zero diferente da emitida pela calculadora
    def testDivisaoZero(self):
        self.iniciarCasoTeste(CT_DIVISAO_ZERO)
        resultadoVisor = self.realizarOperacao([4], [0], "div")
        testRunStatus = TESTRUN_STATUS_PASS

        try:
            self.assertEqual(resultadoVisor, "4÷0=Divisão por zero", CT_DIVISAO_ZERO.description)
        except AssertionError as exception:
            self.criarBugJira(CT_DIVISAO_ZERO, exception)
            testRunStatus = TESTRUN_STATUS_FAIL
            raise
        except Exception as exception:
            testRunStatus = TESTRUN_STATUS_ABORTED
            raise            
        finally:
            self.finalizarCasoTeste(CT_DIVISAO_ZERO, testRunStatus)            


    #Simula um caso de erro: mensagem de calculo de tangente impossivel diferente da calculadora.
    def testTangenteImpossivel(self):
        self.iniciarCasoTeste(CT_TANGENTE_90)
        resultadoVisor = self.realizarOperacao([9,0], [], "tan", True)
        testRunStatus = TESTRUN_STATUS_PASS

        try:
            self.assertEqual(resultadoVisor, "tan(90)=Valor inexistente", CT_TANGENTE_90.description) 
        except AssertionError as exception:
            self.criarBugJira(CT_TANGENTE_90, exception)
            testRunStatus = TESTRUN_STATUS_FAIL
            raise
        except Exception as exception:
            testRunStatus = TESTRUN_STATUS_ABORTED
            raise              
        finally:
            self.finalizarCasoTeste(CT_TANGENTE_90, testRunStatus)            

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    try:
        casosDeTeste = [
            CT_DIGITACAO, CT_FORMATACAO_DECIMAL, CT_TANGENTE_90, CT_DIVISAO_ZERO, 
            CT_ADICAO, CT_SUBTRACAO, CT_MULTIPLICACAO, CT_DIVISAO, CT_PORCENTAGEM, 
            CT_COSENO, CT_SENO ,CT_TANGENTE, 
            CT_POTENCIACAO, CT_RAIZ_QUADRADA
            ]
        createIssueHandler = CreateIssueHandler()
        for casoDeTeste in casosDeTeste:
            createIssueHandler.changeIssueTransition(casoDeTeste.key, TEST_STATUS_BACKLOG_ID)
            testRunId = createIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
            createIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_TODO)
            
        result = unittest.main()
    except Exception as ex:
        print(str(ex))