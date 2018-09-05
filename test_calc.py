# Android environment
import unittest, os
from appium import webdriver

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

    def testSomaCorreta(self):
        self.driver.save_screenshot(self.screenshot_dir + "1_app_launch.png")
        #textElements = self.driver.find_elements_by_class_name('android.widget.TextView')
        #print(textElements)
        #elements1 = self.driver.find_elements_by_xpath("//*[not(*)]")
        #for e in elements1:
            #print(e.__getattribute__('id'), e.get_attribute("resourceId"))
        numero2= self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_02')
        numero4 = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_04')
        operadorSoma = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_add')
        operadorIgual = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_equal')
        numero2.click()
        operadorSoma.click()
        numero4.click()
        operadorIgual.click()
        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        resultadoVisor = resultadoVisor.replace("\n", "").replace(" ","")
        #print("Operação final no Visor: ", resultadoVisor)
        #print("%s" % "Ok" if resultadoVisor == "2+4=6" else "Nok")
        #self.assertTrue(resultadoVisor == "2+4=6", "Resultado do teste de Soma")
        self.assertEqual(resultadoVisor, "2+4=6", "Resultado do teste de Soma")

    def testSomaErrada(self):
        self.driver.save_screenshot(self.screenshot_dir + "1_app_launch.png")
        numero2= self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_02')
        numero4 = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_04')
        operadorSoma = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_add')
        operadorIgual = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_equal')
        numero2.click()
        operadorSoma.click()
        numero4.click()
        operadorIgual.click()
        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        resultadoVisor = resultadoVisor.replace("\n", "").replace(" ","")
        self.assertEqual(resultadoVisor, "2+4=8", "Resultado do teste de Soma")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    try:
        result = unittest.main()
        print(result)
    except Exception as ex:
        print('________________')
        print(ex)

