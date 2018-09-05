# Android environment
import unittest, os
from appium import webdriver

class TestTodoList(unittest.TestCase):

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps['udid'] = 'D1CGAPF710704160'
        self.desired_caps['platformName'] = 'android'
        self.desired_caps['deviceName'] = 'TA-1000_00CN'
        self.desired_caps['appPackage'] = 'br.inatel.todolist'
        self.desired_caps['appActivity'] = 'MainActivity'
        self.screenshot_dir = os.getenv('SCREENSHOT_PATH', '') or os.getcwd() + "/screenshots"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

    def testAddTodo(self):
        self.driver.save_screenshot(self.screenshot_dir + "1_app_launch.png")

        self.driver.find_element_by_id("br.inatel.todolist:id/fab").click()
        self.driver.save_screenshot(self.screenshot_dir + "2_modal_lauch.png")

        self.driver.find_element_by_accessibility_id("itemText").send_keys("teste 01")
        self.driver.save_screenshot(self.screenshot_dir + "3_text_writed.png")

        self.driver.find_element_by_id("android:id/button1").click()
        self.driver.save_screenshot(self.screenshot_dir + "4_creted_todo.png")

    def testCheckTodos(self):
        try:
            self.driver.implicitly_wait(3)
            todo_items = self.driver.find_elements_by_class_name('android.widget.RelativeLayout')

            for todo_item in todo_items:
                ckbox = todo_item.find_element_by_class_name('android.widget.CheckBox')
                if ckbox.get_attribute('checked') == 'false':
                    ckbox.click()
                self.assertTrue(ckbox.get_attribute('checked') == 'true', "CHECK TODOS")

            self.driver.save_screenshot(self.screenshot_dir + "5_checked_todos.png")
        except Exception as ex:
            print('--->')
            print(str(ex))
            raise ex


    def testRemoveTodos(self):
        self.driver.implicitly_wait(3)
        todo_items = self.driver.find_elements_by_class_name('android.widget.RelativeLayout')

        for todo_item in todo_items:
            rm_button = todo_item.find_element_by_class_name('android.widget.ImageButton')
            rm_button.click()

        todo_items = self.driver.find_elements_by_class_name('android.widget.RelativeLayout')
        print(todo_items)
        print(len(todo_items))
        self.assertTrue(len(todo_items) == 0, "REMOVE TODOS")

        self.driver.save_screenshot(self.screenshot_dir + "6_removed_todos.png")

if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as ex:
        print('________________')
        print(ex)

