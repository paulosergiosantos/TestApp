from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, os

class TestMeuVivoLogin(unittest.TestCase):

    def testLogin(self):
        firefox = webdriver.Firefox()
        firefox.get ('https://www.vivo.com.br')
        cpf = firefox.find_element_by_id('cpfOuEmail')
        cpf.clear()
        cpf.send_keys('00000000000')
        senhaI = firefox.find_element_by_id('senhaText')
        senhaH = firefox.find_element_by_id('senhaHeader')
        senhaI.clear()
        firefox.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', senhaI, '......')
        firefox.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', senhaH, '000000')
        firefox.find_element_by_id('btnEntrar').click()
        produtoSelecionado = WebDriverWait(firefox, 40).until(
            EC.presence_of_element_located((By.ID, "produtoSelecionado"))
        )
        print(produtoSelecionado.text)
        produtoSelecionadoInfo = str(produtoSelecionado.text)
        btnFechar = WebDriverWait(firefox, 10).until(
            EC.presence_of_element_located((By.ID, "btnFechar"))
        )
        firefox.execute_script('''
            arguments[0].click();
            ''', btnFechar)
        firefox.find_element_by_id('perfilContasTitle').click()
        iconNavbarExit = WebDriverWait(firefox, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "icon-navbar_exit"))
        )
        firefox.execute_script('''
            arguments[0].click();
            ''', iconNavbarExit)
        btnSim = WebDriverWait(firefox, 10).until(
            EC.presence_of_element_located((By.ID, "btnSim"))
        )
        btnSim.click()
        firefox.quit()
        self.assertEqual(produtoSelecionadoInfo, "(35) 99956-4692")
        

if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as ex:
        print("Exception: ", ex)

