# Android environment
import unittest, os
from appium import webdriver

class TestCalc(unittest.TestCase):

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps['udid'] = '4df1730065835fb7'
        self.desired_caps['platformName'] = 'android'
        self.desired_caps['deviceName'] = 'Inatel(GT-I9300)'
        self.desired_caps['appPackage'] = 'br.com.m4u.recarga.vivo'
        self.desired_caps['appActivity'] = 'br.com.m4u.recarga.vivo.activity.UninstallActivity'
        self.screenshot_dir = os.getenv('SCREENSHOT_PATH', '') or os.getcwd() + "/screenshots"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

    def testCarga(self):
        self.driver.save_screenshot(self.screenshot_dir + "1_app_launch.png")
        textElements = self.driver.find_elements_by_class_name('android.widget.TextView')
        print(textElements)
        elements1 = self.driver.find_elements_by_xpath("//*[not(*)]")
        for e in elements1:
            print(e.__getattribute__('id'), e.get_attribute("resourceId"))
 
if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as ex:
        print('________________')
        print(ex)

