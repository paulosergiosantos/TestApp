import os
import unittest
import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSitesVivo(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.screenshot_dir = os.getenv('SCREENSHOT_PATH', '') or os.getcwd() + "/"
        self.screenShotIndex = 0
        #firefox = webdriver.Firefox()

    def saveScreenShot(self):
        self.screenShotIndex += 1
        self.browser.save_screenshot(self.screenshot_dir + self._testMethodName + "_{}".format(self.screenShotIndex) + ".png")

    def testLoginMeuVivo(self):
        self.browser.get("https://www.vivo.com.br")

        self.saveScreenShot()

        cpf = self.browser.find_element_by_id('cpfOuEmail')
        cpf.clear()
        cpf.send_keys('00000000000')
        senhaI = self.browser.find_element_by_id('senhaText')
        senhaH = self.browser.find_element_by_id('senhaHeader')
        senhaI.clear()
        self.browser.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', senhaI, '......')
        self.browser.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', senhaH, '000000')
        self.browser.find_element_by_id('btnEntrar').click()

        self.saveScreenShot()

        produtoSelecionado = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.ID, "produtoSelecionado"))
        )
        print(produtoSelecionado.text)
        produtoSelecionadoInfo = str(produtoSelecionado.text)
        btnFechar = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "btnFechar"))
        )
        self.browser.execute_script('''arguments[0].click();''', btnFechar)

        self.saveScreenShot()

        self.browser.find_element_by_id('perfilContasTitle').click()
        iconNavbarExit = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "icon-navbar_exit"))
        )
        self.browser.execute_script('''arguments[0].click();''', iconNavbarExit)
        btnSim = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "btnSim"))
        )
        btnSim.click()
        self.assertEqual(produtoSelecionadoInfo, "(35) 99956-4692")

    def testAuraInit(self):
        self.browser.get("https://www.vivo.com.br")

        self.saveScreenShot()

        self.browser.find_element_by_id('launch_button').click()
        self.browser.find_element_by_id('btnComecar').click()
        auraWelcomeMsg = self.browser.find_element_by_id('aura-welcome-msg')
        welcomeMsg = auraWelcomeMsg.find_elements_by_tag_name("p")
        self.saveScreenShot()
        self.assertEqual(len(welcomeMsg), 3)
        self.assertEqual(welcomeMsg[0].text, 'Olá! Como posso ajudar?')
        self.assertEqual(welcomeMsg[1].text, 'Você pode me perguntar coisas do tipo:')
        self.assertEqual(welcomeMsg[2].text, '"Como consigo a segunda via da minha conta?"')
        
    def testAuraProcura(self):
        self.browser.get("https://www.vivo.com.br")

        self.saveScreenShot()

        self.browser.find_element_by_id('launch_button').click()
        self.browser.find_element_by_id('btnComecar').click()
        self.saveScreenShot()
        self.browser.find_element_by_id("chatSend").send_keys("PREÇO")

        self.saveScreenShot()

        self.browser.find_element_by_id("fab_send").click()
        auraDesambiguacao = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "aura_desambiguacao"))
        )
        porFavorP = auraDesambiguacao.find_element_by_tag_name("p")
        quickReplyOptions = auraDesambiguacao.find_elements_by_id("quick_reply_option")

        self.saveScreenShot()

        self.assertEqual(porFavorP.text, "Por favor, escolha a opção que pretende:")
        self.assertEqual(quickReplyOptions[0].text, "Comprar Aparelho")
        self.assertEqual(quickReplyOptions[1].text, "Pontos Valoriza")
        self.assertEqual(quickReplyOptions[2].text, "Vivo Renova")
    
    def validarConexao(self, site):
        print(site)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.browser.get(site)
        self.saveScreenShot()
        httpResponse = requests.get(site, headers = headers)
        self.assertEqual(httpResponse.status_code, 200)

    def testVivoComBr(self):
        self.validarConexao("https://www.vivo.com.br")

    def testMeuVivoComBr(self):
        self.validarConexao("https://meuvivo.vivo.com.br")

    def testLoginVivoComBr(self):
        self.validarConexao("https://login.vivo.com.br")

    def testAppstoreVivoComBr(self):
        self.validarConexao("https://appstore.vivo.com.br")

    def testLojaOnlineVivoComBr(self):
        self.validarConexao("https://lojaonline.vivo.com.br")

    def testForumVivoComBr(self):
        self.validarConexao("https://forum.vivo.com.br")

    def testAssineVivoComBr(self):
        self.validarConexao("https://assine.vivo.com.br")

    def testTransformaVivoComBr(self):
        self.validarConexao("https://vivotransforma.com.br")

    def testTelefonicaComBr(self):
        self.validarConexao("http://www.telefonica.com.br")

    def testMobileConnectTelefonicaCom(self):
        self.validarConexao("https://br.mobileconnect.telefonica.com")

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as ex:
        print("Exception: ", ex)
    finally:
        print("Testes finalizados")

