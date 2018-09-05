# Android environment
import unittest, os
from appium import webdriver
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

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
        #self.imprimirTodosElements()

    def imprimirTodosElements(self):
        #textElements = self.driver.find_elements_by_class_name('android.widget.TextView')
        #print(textElements)
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for e in elements:
            print(e.__getattribute__('id'), e.get_attribute("resourceId"))

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
        for i in range(9, -1, -1):
            numero_id = 'com.sec.android.app.popupcalculator:id/bt_0' + str(i)
            print(numero_id)
            numero = self.driver.find_element_by_id(numero_id)
            numero.click()
        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        resultadoVisor = resultadoVisor.replace(",", "").replace(".","")
        self.assertEqual(resultadoVisor, "9876543210", "Resultado do teste de Visualização dos Digitos")

    #Simula um erro    
    def testFormatacaoDecimal(self):
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
        self.assertEqual(resultadoVisor, "4.321,05", "Resultado do teste Formatacao Decimal")       

 
    def testAdicao(self):
        resultadoVisor = self.realizarOperacao([2], [4], "add")
        self.assertEqual(resultadoVisor, "2+4=6", "Resultado do teste de Adicao")

    def testSubtracao(self):
        resultadoVisor = self.realizarOperacao([4], [2], "sub")
        self.assertEqual(resultadoVisor, "4" + u"\u2212" + "2=2", "Resultado do teste de Subtracao")

    def testMultiplicacao(self):
        resultadoVisor = self.realizarOperacao([4], [2,0], "mul")
        self.assertEqual(resultadoVisor, "4" + u"\u00D7" + "20=80", "Resultado do teste de Multiplicacao")

    def testDivisao(self):
        resultadoVisor = self.realizarOperacao([4,0], [2], "div")
        self.assertEqual(resultadoVisor, "40÷2=20", "Resultado do teste de Divisao")

    #Simula um caso de erro: mensagem da divisao por zero diferente da emitida pela calculadora
    def testDivisaoZero(self):
        resultadoVisor = self.realizarOperacao([4], [0], "div")
        self.assertEqual(resultadoVisor, "4÷0=Divisão por zero", "Resultado do teste de Divisao por Zero")
   
    def testPorcentagem(self):
        resultadoVisor = self.realizarOperacao([4,0,0], [2,0], "persentage")
        self.assertEqual(resultadoVisor, "400%" + u"\u00D7" + "20=80", "Resultado do teste de Porcentagem")   

   
    def testPotencia(self):
        resultadoVisor = self.realizarOperacao([2], [3], "x_y")
        self.assertEqual(resultadoVisor, "2^(3)=8", "Resultado do teste de Potenciacao")  

    def testRaizQuadrada(self):
        resultadoVisor = self.realizarOperacao([9], [], "root", True)
        self.assertEqual(resultadoVisor, u"\u221A" + "(9)=3", "Resultado do teste de Raiz Quadrada")  
 
    def testCoseno(self):
        resultadoVisor = self.realizarOperacao([9,0], [], "cos", True)
        self.assertEqual(resultadoVisor, "cos(90)=0", "Resultado do teste de Coseno")  

    def testSeno(self):
        resultadoVisor = self.realizarOperacao([9,0], [], "sin", True)
        self.assertEqual(resultadoVisor, "sin(90)=1", "Resultado do teste de Seno")  
        
    def testTangente(self):
        resultadoVisor = self.realizarOperacao([4,5], [], "tan", True)
        self.assertEqual(resultadoVisor, "tan(45)=1", "Resultado do teste de Tangente") 

    #Simula um caso de erro: mensagem de calculo de tangente impossivel diferente da calculadora.
    def testTangenteImpossivel(self):
        resultadoVisor = self.realizarOperacao([9,0], [], "tan", True)
        self.assertEqual(resultadoVisor, "tan(90)=Valor inexistente", "Resultado do teste de Tangente de 90º") 

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    try:
        result = unittest.main()
        print("Tipo do REsultado:", type(result))
    except Exception as ex:
        print('________________')
        print(str(ex))