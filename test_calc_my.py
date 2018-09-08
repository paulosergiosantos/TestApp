# Android environment
import unittest
import os
import sys
import logging
import datetime

from appium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

from convert_img_to_base64 import ImgToBase64
from create_issue_jira_prod import JiraIssueHandler
from create_issue_jira_prod import Response
from create_issue_jira_prod import IssueLinkType

from constants_jira_prod import PROJECT_POC_KEY, ISSUE_BUG_NAME, ISSUE_TESTEXEC_NAME, ISSUE_TESTEXEC_KEY
from constants_jira_prod import TEST_STATUS_IN_PROGRESS_ID, TEST_STATUS_RETESTING_ID, TEST_STATUS_DONE_ID
from constants_jira_prod import TEST_RESOLUTION_TESTED
from constants_jira_prod import TESTRUN_STATUS_TODO, TESTRUN_STATUS_EXECUTING, TESTRUN_STATUS_PASS, TESTRUN_STATUS_FAIL, TESTRUN_STATUS_ABORTED
from constants_jira_prod import CT_DIGITACAO, CT_FORMATACAO_DECIMAL
from constants_jira_prod import CT_ADICAO, CT_SUBTRACAO, CT_MULTIPLICACAO, CT_DIVISAO, CT_DIVISAO_ZERO
from constants_jira_prod import CT_SENO, CT_COSENO, CT_TANGENTE, CT_TANGENTE_90
from constants_jira_prod import CT_PORCENTAGEM, CT_POTENCIACAO, CT_RAIZ_QUADRADA
from constants_jira_prod import MAP_METODO_CASO_TESTE, CASO_TESTE_KEYS

LOGGER.setLevel(logging.INFO)

class TestCalc(unittest.TestCase):

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps['udid'] = '35da55e8'
        self.desired_caps['platformName'] = 'android'
        self.desired_caps['deviceName'] = 'PSSantos'
        self.desired_caps['appPackage'] = 'com.sec.android.app.popupcalculator'
        self.desired_caps['appActivity'] = 'com.sec.android.app.popupcalculator.Calculator'
        self.screenshot_dir = os.getenv('SCREENSHOT_PATH', '') or os.getcwd() + "/"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.casoDeTeste = MAP_METODO_CASO_TESTE.get(self._testMethodName)
        self.testRunStatus = TESTRUN_STATUS_PASS
        #self.imprimirTodosElements()

    def habilitarCalcCientifica(self):
        self.driver.find_element_by_accessibility_id("Mais opções").click()
        self.driver.find_element_by_id("android:id/title").click()

    def imprimirTodosElements(self):
        #textElements = self.driver.find_elements_by_class_name('android.widget.TextView')
        #print(textElements)
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        [print(e.__getattribute__('id'), e.get_attribute("resourceId")) for e in elements]

    def iniciarCasoTeste(self, casoDeTeste):
        jiraIssueHandler.changeIssueTransition(casoDeTeste.key, TEST_STATUS_IN_PROGRESS_ID)
        testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
        jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_EXECUTING)

    def finalizarCasoTeste(self, casoDeTeste, testRunStatus):
        jiraIssueHandler.changeIssueTransition(casoDeTeste.key, TEST_STATUS_DONE_ID, TEST_RESOLUTION_TESTED)
        testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
        jiraIssueHandler.changeIssueTestRunStatus(testRunId, testRunStatus)

    def criarBugJira(self, casoDeTeste, exception):
        response = jiraIssueHandler.createIssueWithRawData(PROJECT_POC_KEY, ISSUE_BUG_NAME, casoDeTeste.description, str(exception))
        if (response.status == Response.STATUS_OK):
            #jiraIssueHandler.createIssueLinkWithRawData(ISSUELINKTYPE_BLOCKS_BY, casoDeTeste.key, response.key)
            testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
            jiraIssueHandler.addDefectToTestrun(testRunId, response.key)
            imageFileName = self.screenshot_dir + self._testMethodName + ".png"
            imageData = ImgToBase64().convertToBase64(imageFileName)
            jiraIssueHandler.addAttachmentToTestrun(testRunId, imageData, self._testMethodName + ".png")

    def getResultadoVisor(self):
        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        return resultadoVisor

    def clickNumero(self, numArray):
        numIdPrefix = "com.sec.android.app.popupcalculator:id/bt_0"
        click = lambda num: self.driver.find_element_by_id(numIdPrefix + str(num)).click()
        [click(i) for i in numArray]

    def clickOperador(self, operador):
        self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_' + str(operador)).click()

    def realizarOperacao(self, digitos1, digitos2, operador, primeiroOperador=False):
        if (primeiroOperador):
            self.clickOperador(operador)
        self.clickNumero(digitos1)
        if (not primeiroOperador):
            self.clickOperador(operador)
        self.clickNumero(digitos2)
        self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_equal').click()
        resultadoVisor = self.getResultadoVisor().replace("\n", "").replace(" ","")

        return resultadoVisor

    def testDigitacao(self):
        try:
            self.iniciarCasoTeste(self.casoDeTeste)
            self.clickNumero([i for i in range(9, -1, -1)])
            resultadoVisor = self.getResultadoVisor().replace(",", "").replace(".","")
            self.assertEqual(resultadoVisor, "9876543210", self.casoDeTeste.description)
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)

    #Simula um erro: formatacao decimal não está em portugues
    def testFormatacaoDecimal(self):
        try:
            self.iniciarCasoTeste(self.casoDeTeste)
            self.clickNumero([i for i in range(4, 0, -1)])
            self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_dot').click()
            self.clickNumero([0,5])
            resultadoVisor = self.getResultadoVisor()
            self.assertEqual(resultadoVisor, "4.321,05", self.casoDeTeste.description)
        except AssertionError as exception:
            self.driver.save_screenshot(self.screenshot_dir + self._testMethodName + ".png")
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)

    def testAdicao(self):
        try:
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([2], [4], "add")
            self.assertEqual(resultadoVisor, "2+4=6", self.casoDeTeste.description)
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)

    def testSubtracao(self):
        try:
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([4], [2], "sub")
            self.assertEqual(resultadoVisor, "4" + u"\u2212" + "2=2", CT_SUBTRACAO.description)
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)

    def testMultiplicacao(self):
        try:
            self.iniciarCasoTeste(CT_MULTIPLICACAO)
            resultadoVisor = self.realizarOperacao([4], [2,0], "mul")
            self.assertEqual(resultadoVisor, "4" + u"\u00D7" + "20=80", CT_MULTIPLICACAO.description)
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)

    def testDivisao(self):
        try:
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([4,0], [2], "div")
            self.assertEqual(resultadoVisor, "40÷2=20", self.casoDeTeste.description)
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)        

    #Simula um caso de erro: mensagem da divisao por zero diferente da emitida pela calculadora
    def testDivisaoZero(self):
        self.iniciarCasoTeste(self.casoDeTeste)
        resultadoVisor = self.realizarOperacao([4], [0], "div")
        try:
            self.assertEqual(resultadoVisor, "4÷0=Divisão por zero", self.casoDeTeste.description)
        except AssertionError as exception:
            self.driver.save_screenshot(self.screenshot_dir + self._testMethodName + ".png")
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise            
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)    

    def testCoseno(self):
        try:
            self.habilitarCalcCientifica()
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([9,0], [], "cos", True)
            self.assertEqual(resultadoVisor, "cos(90)=0", self.casoDeTeste.description)  
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus) 
    
    def testSeno(self):
        try:
            self.habilitarCalcCientifica()
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([9,0], [], "sin", True)
            self.assertEqual(resultadoVisor, "sin(90)=1", self.casoDeTeste.description) 
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus) 
    
    def testTangente(self):
        try:
            self.habilitarCalcCientifica()
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([4,5], [], "tan", True)
            self.assertEqual(resultadoVisor, "tan(45)=1", self.casoDeTeste.description)
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus) 

    #Simula um caso de erro: mensagem de calculo de tangente impossivel diferente da calculadora.
    def testTangente90(self):
        try:
            self.habilitarCalcCientifica()
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([9,0], [], "tan", True)
            self.assertEqual(resultadoVisor, "tan(90)=Valor inexistente", self.casoDeTeste.description) 
        except AssertionError as exception:
            self.driver.save_screenshot(self.screenshot_dir + self._testMethodName + ".png")
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)

    def testPorcentagem(self):
        try:
            self.habilitarCalcCientifica()
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([4,0,0], [2,0], "persentage")
            self.assertEqual(resultadoVisor, "400%" + u"\u00D7" + "20=80", self.casoDeTeste.description)   
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus) 

    def testPotenciacao(self):
        try:
            self.habilitarCalcCientifica()
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([2], [3], "x_y")
            self.assertEqual(resultadoVisor, "2^(3)=8", self.casoDeTeste.description)  
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus) 

    def testRaizQuadrada(self):
        try:
            self.habilitarCalcCientifica()
            self.iniciarCasoTeste(self.casoDeTeste)
            resultadoVisor = self.realizarOperacao([9], [], "root", True)
            self.assertEqual(resultadoVisor, u"\u221A" + "(9)=3", self.casoDeTeste.description)  
        except AssertionError as exception:
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise 
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus) 

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    try:
        dateTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        jiraIssueHandler = JiraIssueHandler()
        testExecIssue = jiraIssueHandler.createIssueWithRawData(PROJECT_POC_KEY, ISSUE_TESTEXEC_NAME, "Rodada de Teste Calculadora - {}".format(dateTime))
        ISSUE_TESTEXEC_KEY = testExecIssue.key
        jiraIssueHandler.addTestToTestExecution(ISSUE_TESTEXEC_KEY, CASO_TESTE_KEYS)
        for key in CASO_TESTE_KEYS:
            jiraIssueHandler.changeIssueTransition(key, TEST_STATUS_RETESTING_ID)
            testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, key)
            jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_TODO)

        result = unittest.main()
    except Exception as ex:
        print(str(ex))
    finally:
        sys.exit(0)